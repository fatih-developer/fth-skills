#!/usr/bin/env python3
"""Lint a DESIGN.md against the google-labs-code/design.md spec, plus fth-skills rules.

Mirrors the official linter rules that matter for generation (broken-ref,
missing-primary, missing-typography, contrast-ratio, orphaned-tokens, section-order,
duplicate sections, unknown component properties, dimension units) and adds:

* no-gradient  (error)   gradients in any token value
* dark-twins   (warning) a `<role>-dark` color without `<role>`, or core roles
                         missing a dark twin once any dark twin exists
* prose-ref    (warning) `{group.token}` references in the prose that do not resolve
* default-font (info)    overused or AI-favorite families from ai_defaults.json
* placeholder  (error)   unfilled {{template}} values

Standard library only (uses PyYAML when installed, otherwise a small parser for the
front-matter subset DESIGN.md uses). With --official it also runs
`npx @google/design.md lint` when Node is available and reports both.

Examples:
    python lint_design_md.py design/DESIGN.md
    python lint_design_md.py design/DESIGN.md --json
    python lint_design_md.py design/DESIGN.md --official
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import colorlib as cl  # noqa: E402

CANONICAL = ["Overview", "Colors", "Typography", "Layout", "Elevation & Depth", "Shapes", "Components", "Do's and Don'ts"]
ALIASES = {"Brand & Style": "Overview", "Layout & Spacing": "Layout", "Elevation": "Elevation & Depth"}
KNOWN_TOP = {"version", "name", "description", "omitted", "colors", "typography", "rounded", "spacing", "components"}
COMPONENT_PROPS = {"backgroundColor", "textColor", "typography", "rounded", "padding", "size", "height", "width"}
TYPO_PROPS = {"fontFamily", "fontSize", "fontWeight", "lineHeight", "letterSpacing", "fontFeature", "fontVariation"}
MD3_FAMILIES = {"primary", "secondary", "tertiary", "error", "surface", "background", "outline"}
DIMENSION_RE = re.compile(r"^-?\d*\.?\d+(px|em|rem)$")
REF_RE = re.compile(r"\{([a-zA-Z][\w-]*(?:\.[\w-]+)+)\}")
GRADIENT_RE = re.compile(r"(?:repeating-)?(?:linear|radial|conic)-gradient\(", re.I)


# --------------------------------------------------------------------------- YAML subset


def _parse_scalar(raw: str):
    s = raw.strip()
    if not s:
        return None
    if s[0] == '"':
        return json.loads(s)
    if s[0] == "'":
        return s[1:-1].replace("''", "'")
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    if re.fullmatch(r"-?\d*\.\d+", s):
        return float(s)
    if s in ("true", "false"):
        return s == "true"
    if s in ("null", "~"):
        return None
    return s


def _strip_comment(line: str) -> str:
    out, quote = [], None
    for i, ch in enumerate(line):
        if quote:
            out.append(ch)
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
            out.append(ch)
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            break
        else:
            out.append(ch)
    return "".join(out).rstrip()


def parse_yaml_subset(text: str):
    """Parse nested mappings, scalars, and simple lists (enough for DESIGN.md front matter)."""
    lines = [(len(l) - len(l.lstrip(" ")), l.strip()) for l in (_strip_comment(x) for x in text.splitlines()) if l.strip()]
    pos = 0

    def block(indent: int):
        nonlocal pos
        if pos < len(lines) and lines[pos][1].startswith("- "):
            items = []
            while pos < len(lines) and lines[pos][0] == indent and lines[pos][1].startswith("- "):
                content = lines[pos][1][2:]
                pos += 1
                if re.match(r"^[\w\-'\"& ]+:\s", content + " ") and not content.startswith(("'", '"')):
                    key, _, rest = content.partition(":")
                    item = {key.strip(): _parse_scalar(rest)}
                    while pos < len(lines) and lines[pos][0] > indent and not lines[pos][1].startswith("- "):
                        k, _, v = lines[pos][1].partition(":")
                        item[k.strip()] = _parse_scalar(v)
                        pos += 1
                    items.append(item)
                else:
                    items.append(_parse_scalar(content))
            return items
        mapping = {}
        while pos < len(lines) and lines[pos][0] == indent:
            key, sep, rest = lines[pos][1].partition(":")
            if not sep:
                raise ValueError(f"cannot parse line: {lines[pos][1]!r}")
            key = key.strip().strip("'\"")
            pos += 1
            if rest.strip():
                mapping[key] = _parse_scalar(rest)
            elif pos < len(lines) and lines[pos][0] > indent:
                mapping[key] = block(lines[pos][0])
            else:
                mapping[key] = None
        return mapping

    return block(lines[0][0]) if lines else {}


def load_front_matter(text: str) -> tuple[dict | None, str, str | None]:
    """Return (front matter, body, error)."""
    if not text.startswith("---"):
        return None, text, None
    parts = re.split(r"^---\s*$", text, maxsplit=2, flags=re.M)
    if len(parts) < 3:
        return None, text, "front matter is not closed with a line containing exactly '---'"
    raw, body = parts[1], parts[2]
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(raw) or {}
    except ImportError:
        try:
            data = parse_yaml_subset(raw)
        except (ValueError, json.JSONDecodeError) as err:
            return None, body, f"front matter could not be parsed: {err}"
    except Exception as err:  # noqa: BLE001 - yaml.YAMLError without importing its type eagerly
        return None, body, f"front matter is not valid YAML: {str(err).splitlines()[0]}"
    if not isinstance(data, dict):
        return None, body, "front matter must be a mapping"
    return data, body, None


# --------------------------------------------------------------------------- rules


def sections(body: str) -> list[str]:
    out, fence = [], None
    for line in body.splitlines():
        m = re.match(r"^\s*(`{3,}|~{3,})", line)
        if m:
            fence = None if fence and m.group(1)[0] == fence[0] else (fence or m.group(1))
            continue
        if fence is None and line.startswith("## "):
            out.append(line[3:].strip())
    return out


def resolve(data: dict, path: str):
    node = data
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def color_family(name: str) -> str:
    n = re.sub(r"^on-", "", name)
    n = re.sub(r"^inverse-", "", n)
    n = re.sub(r"^on-", "", n)
    n = re.sub(r"-container.*$", "", n)
    n = re.sub(r"-fixed.*$", "", n)
    return re.sub(r"-(dim|bright|tint|variant)$", "", n)


def lint_text(text: str) -> dict:
    findings: list[dict] = []

    def add(severity, rule, message, path=None):
        f = {"severity": severity, "rule": rule, "message": message}
        if path:
            f["path"] = path
        findings.append(f)

    data, body, err = load_front_matter(text)
    if err:
        add("error", "front-matter", err)
    data = data or {}
    colors = data.get("colors") or {}
    typography = data.get("typography") or {}
    components = data.get("components") or {}

    # Sections
    heads = sections(body)
    canonical = [ALIASES.get(h, h) for h in heads]
    seen = set()
    for h in canonical:
        if h in seen:
            add("error", "duplicate-section", f"Duplicate section heading '## {h}'.")
        seen.add(h)
    known = [h for h in canonical if h in CANONICAL]
    for a, b in zip(known, known[1:]):
        if CANONICAL.index(a) > CANONICAL.index(b):
            add("warning", "section-order", f"Section '{a}' appears before '{b}'. Expected order: {', '.join(CANONICAL)}")
            break

    # Top-level keys
    for key in data:
        if key not in KNOWN_TOP:
            add("warning", "unknown-key", f"Top-level key '{key}' is not part of the schema; export commands ignore it.", key)

    # Colors
    if colors and "primary" not in colors:
        add("warning", "missing-primary", "Colors are defined but there is no 'primary' color.")
    if colors and not typography:
        add("warning", "missing-typography", "Colors are defined but no typography tokens exist.")
    for name, value in colors.items():
        if isinstance(value, str) and GRADIENT_RE.search(value):
            continue  # reported once by the token walk below
        if isinstance(value, str) and not value.startswith("{") and cl.parse_color(value) is None and "color-mix" not in value and "transparent" not in value:
            add("warning", "color-format", f"colors.{name} value '{value}' could not be parsed as a color.", f"colors.{name}")

    # Typography
    for level, spec in typography.items():
        if not isinstance(spec, dict):
            continue
        for prop, value in spec.items():
            if prop not in TYPO_PROPS:
                add("warning", "unknown-typography-property", f"typography.{level}.{prop} is not a typography property.", f"typography.{level}")
            if prop in ("fontSize", "letterSpacing"):
                is_ref = isinstance(value, str) and value.startswith("{")  # token reference or {{placeholder}}
                if not is_ref and not (isinstance(value, str) and DIMENSION_RE.match(value)):
                    add("warning", "dimension", f"typography.{level}.{prop} '{value}' needs a px, em, or rem unit.", f"typography.{level}")
    for name, value in (data.get("rounded") or {}).items():
        if isinstance(value, str) and "{{" not in value and not DIMENSION_RE.match(value):
            add("error", "dimension", f"rounded.{name} '{value}' needs a px, em, or rem unit.", f"rounded.{name}")

    # References anywhere in tokens
    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                yield from walk(v, f"{path}.{k}" if path else k)
        elif isinstance(node, str):
            yield path, node

    for path, value in walk({k: data[k] for k in data if k in KNOWN_TOP}, ""):
        if "{{" in value:
            add("error", "placeholder", f"{path} is an unfilled template placeholder: {value}", path)
            continue
        if GRADIENT_RE.search(value):
            add("error", "no-gradient", f"{path} contains a gradient; tokens must be single flat values.", path)
        for ref in REF_RE.findall(value):
            if resolve(data, ref) is None:
                add("error", "broken-ref", f"{path} references {{{ref}}}, which is not defined.", path)

    # Components
    referenced = set()
    for comp, props in components.items():
        if not isinstance(props, dict):
            continue
        for prop, value in props.items():
            if prop not in COMPONENT_PROPS:
                add("warning", "unknown-component-property", f"components.{comp}.{prop} is not a known component property.", f"components.{comp}")
            if isinstance(value, str):
                referenced.update(REF_RE.findall(value))
        bg, fg = props.get("backgroundColor"), props.get("textColor")
        if bg and fg:
            def color_of(v):
                ref = REF_RE.fullmatch(v)
                return resolve(data, ref.group(1)) if ref else v
            b, f = color_of(bg), color_of(fg)
            if isinstance(b, str) and isinstance(f, str) and cl.parse_color(b) and cl.parse_color(f):
                ratio = cl.contrast_ratio(f, b)
                if ratio < 4.5:
                    add("warning", "contrast-ratio", f"components.{comp}: textColor ({f}) on backgroundColor ({b}) is {ratio:.2f}:1, below 4.5:1.", f"components.{comp}")
    if components:
        ref_colors = {r.split(".", 1)[1] for r in referenced if r.startswith("colors.")}
        families = {color_family(r) for r in ref_colors}
        for name in colors:
            fam = color_family(name)
            if name in ref_colors or fam in families or fam in MD3_FAMILIES:
                continue
            add("warning", "orphaned-tokens", f"'{name}' is defined but never referenced by any component.", f"colors.{name}")

    # Optional sections (mirrors the official missing-sections rule)
    omitted = {(o.get("section") if isinstance(o, dict) else str(o)).lower() for o in (data.get("omitted") or []) if o}
    for section in ("spacing", "rounded"):
        if colors and not data.get(section) and section not in omitted:
            add("info", "missing-sections", f"No '{section}' section defined; agents will fall back to their defaults.", section)

    # Dark twins
    darks = {n[: -len("-dark")] for n in colors if n.endswith("-dark")}
    for base in sorted(darks - set(colors)):
        add("warning", "dark-twins", f"'{base}-dark' has no light counterpart '{base}'.", f"colors.{base}-dark")
    if darks:
        for base in ("background", "surface", "on-surface", "primary", "on-primary"):
            if base in colors and base not in darks:
                add("warning", "dark-twins", f"'{base}' has no '{base}-dark' twin while other dark tokens exist.", f"colors.{base}")

    # Prose references
    for ref in sorted(set(REF_RE.findall(body))):
        if ref.split(".")[0] in ("colors", "typography", "rounded", "spacing", "components") and resolve(data, ref) is None:
            add("warning", "prose-ref", f"The prose references {{{ref}}}, which is not a token.")

    # Fonts
    try:
        defaults = json.loads((HERE / "ai_defaults.json").read_text(encoding="utf-8"))
        flagged = set(defaults["fonts"]["overused"]) | set(defaults["fonts"]["ai_favorites"])
        for fam in sorted({s.get("fontFamily") for s in typography.values() if isinstance(s, dict)} & flagged):
            add("info", "default-font", f"'{fam}' is an overused or AI-favorite family; keep it only with a stated reason.")
    except (OSError, KeyError, json.JSONDecodeError):
        pass

    counts = {k: len(data.get(k) or {}) for k in ("colors", "typography", "rounded", "spacing", "components")}
    add("info", "token-summary", "Defines " + ", ".join(f"{v} {k}" for k, v in counts.items()) + ".")
    summary = {s: sum(1 for f in findings if f["severity"] == s) for s in ("error", "warning", "info")}
    return {"findings": findings, "summary": {"errors": summary["error"], "warnings": summary["warning"], "infos": summary["info"]}}


def lint_file(path: Path) -> dict:
    return lint_text(Path(path).read_text(encoding="utf-8"))


def run_official(path: Path) -> dict | None:
    npx = shutil.which("npx")
    if not npx:
        return None
    try:
        res = subprocess.run([npx, "-y", "@google/design.md", "lint", str(path)], capture_output=True, text=True, timeout=180)
        return json.loads(res.stdout)
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError):
        return None


def format_report(report: dict, title: str = "DESIGN.md lint") -> str:
    s = report["summary"]
    lines = [f"{title}: {s['errors']} error(s), {s['warnings']} warning(s), {s.get('infos', 0)} info"]
    for f in report["findings"]:
        lines.append(f"  [{f['severity']}] {f.get('rule', '')}: {f['message']}")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("file")
    p.add_argument("--json", action="store_true")
    p.add_argument("--official", action="store_true", help="Also run `npx @google/design.md lint` when available")
    args = p.parse_args()
    report = lint_file(Path(args.file))
    official = run_official(Path(args.file)) if args.official else None
    if args.json:
        print(json.dumps({"fth": report, "official": official}, indent=2, ensure_ascii=False))
    else:
        print(format_report(report))
        if args.official:
            print(format_report(official, "official @google/design.md lint") if official else "official linter unavailable (needs Node/npx and network)")
    errors = report["summary"]["errors"] + ((official or {}).get("summary", {}).get("errors", 0))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
