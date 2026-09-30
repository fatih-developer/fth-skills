#!/usr/bin/env python3
"""Check 2-3 palette + typography directions and render a side-by-side demo page.

Input is a directions.json file (see templates/directions.template.json). The script:

* fills derived roles (hover, soft, elevated surfaces) from the colors you chose
* checks WCAG contrast for every text/background pair in light and dark themes
* rejects gradients, flags colors close to AI/template defaults, flags directions
  that are too similar to each other, and (with --landscape) accent hues that
  competitors already occupy
* flags overused or AI-favorite fonts and missing Turkish support
* writes a standalone specimen.html so people compare real UI, not swatches alone
* with --export <id>, writes DESIGN.md, tokens.css, tailwind.theme.json, and
  design-tokens.json for the chosen direction

Examples:
    python build_specimen.py directions.json --out design/specimen.html
    python build_specimen.py directions.json --landscape landscape.json --strict
    python build_specimen.py directions.json --export b --out-dir design/
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import sys
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import colorlib as cl  # noqa: E402

REQUIRED_ROLES = ["bg", "surface", "border", "text", "text-muted", "primary", "on-primary", "accent", "success", "warning", "danger"]
TEXT_PAIRS = [("text", "bg"), ("text", "surface"), ("text-muted", "bg"), ("text-muted", "surface"), ("on-primary", "primary")]
UI_PAIRS = [("border-strong", "bg"), ("primary", "bg"), ("accent", "bg"), ("success", "bg"), ("warning", "bg"), ("danger", "bg")]
SIMILAR_DIRECTIONS = 0.08
DEFAULT_SAMPLE = {
    "headline": "Güçlü bir başlık, sade bir sistem",
    "body": "Pijamalı hasta yağız şoföre çabucak güvendi. İstanbul, Iğdır ve Şırnak'tan gelen siparişler aynı gün hazırlanır.",
    "cta": "Siparişi başlat",
    "secondary": "Fiyatları gör",
}


# --------------------------------------------------------------------------- model


def load_defaults() -> dict:
    return json.loads((HERE / "ai_defaults.json").read_text(encoding="utf-8"))


def load_font_metadata() -> dict[str, dict] | None:
    """Use the find_fonts cache when present; never hit the network from here."""
    try:
        import find_fonts

        if find_fonts.CACHE.exists():
            return {f["family"].lower(): f for f in find_fonts.load_metadata(str(find_fonts.CACHE))}
    except Exception:  # noqa: BLE001 - metadata is optional
        return None
    return None


def complete_theme(colors: dict, dark: bool) -> dict:
    c = {k: cl.normalize_hex(v) or v for k, v in colors.items()}
    c.setdefault("bg-elevated", c["surface"])
    c.setdefault("surface-2", cl.mix(c["surface"], c["text"], 0.05))
    c.setdefault("primary-hover", cl.shift_lightness(c["primary"], 0.06 if dark else -0.06))
    c.setdefault("primary-soft", cl.mix(c["primary"], c["bg"], 0.86))
    c.setdefault("info", c["primary"])
    if "border-strong" not in c:
        # Input and control boundaries need 3:1 (WCAG 1.4.11); decorative dividers may stay softer.
        for step in range(21):
            cand = cl.mix(c["border"], c["text"], step / 20)
            if cl.contrast_ratio(cand, c["bg"]) >= 3:
                break
        c["border-strong"] = cand
    return c


def type_scale(t: dict) -> dict[str, dict]:
    base, ratio = float(t.get("base", 16)), float(t.get("ratio", 1.25))
    lh_body, lh_head = float(t.get("line_height_body", 1.55)), float(t.get("line_height_heading", 1.15))
    steps = {"caption": -1, "body": 0, "lead": 1, "h4": 2, "h3": 3, "h2": 4, "h1": 5, "display": 6}
    out = {}
    for role, n in steps.items():
        size = round(base * ratio ** n, 1)
        out[role] = {"size": f"{size:g}px", "line_height": lh_head if n >= 2 else lh_body, "weight": "heading" if n >= 2 else "body"}
    return out


def gf_url(fonts: dict) -> str:
    parts = []
    for slot in ("heading", "body", "mono"):
        f = fonts.get(slot)
        if not f:
            continue
        spec = "family=" + urllib.parse.quote_plus(f["family"])
        ws = sorted({int(w) for w in f.get("weights", [400])})
        spec += ":wght@" + ";".join(str(w) for w in ws)
        if spec not in parts:
            parts.append(spec)
    return "https://fonts.googleapis.com/css2?" + "&".join(parts) + "&display=swap"


def font_stack(f: dict | None, fallback: str) -> str:
    if not f:
        return fallback
    return f"'{f['family']}', {f.get('fallback', fallback)}"


# --------------------------------------------------------------------------- checks


def check_direction(d: dict, defaults: dict, meta: dict | None, landscape: dict | None) -> list[dict]:
    issues = []

    def add(level, msg):
        issues.append({"level": level, "message": msg})

    for theme in ("light", "dark"):
        raw = (d.get("colors") or {}).get(theme)
        if not raw:
            add("FAIL", f"{theme}: missing color set")
            continue
        missing = [r for r in REQUIRED_ROLES if r not in raw]
        if missing:
            add("FAIL", f"{theme}: missing roles {', '.join(missing)}")
            continue
        bad = [r for r, v in raw.items() if "gradient" in str(v).lower() or cl.parse_color(str(v)) is None]
        for r in bad:
            add("FAIL", f"{theme}: '{r}' must be one flat color (gradients and unparsable values are not allowed): {raw[r]}")
        if bad:
            continue
        c = complete_theme(raw, theme == "dark")
        for fg, bg in TEXT_PAIRS:
            ratio = cl.contrast_ratio(c[fg], c[bg])
            if ratio < 4.5:
                add("FAIL", f"{theme}: {fg} on {bg} is {ratio:.2f}:1 (text needs 4.5:1)")
        for fg, bg in UI_PAIRS:
            ratio = cl.contrast_ratio(c[fg], c[bg])
            if ratio < 3:
                add("FAIL", f"{theme}: {fg} on {bg} is {ratio:.2f}:1 (UI elements need 3:1)")
            elif ratio < 4.5 and fg in ("primary", "danger"):
                add("INFO", f"{theme}: {fg} on {bg} is {ratio:.2f}:1 — fine for fills and icons, too low for {fg}-colored body text")
        for role in ("primary", "accent", "bg"):
            for ref in defaults["colors"]:
                if cl.similar(c[role], ref["hex"], defaults["color_threshold"]):
                    add("WARN", f"{theme}: {role} {c[role]} is close to a template default ({ref['name']} {ref['hex']})")
        for pair in defaults["pairs"]:
            a, b = pair["colors"]
            for role in ("primary", "accent"):
                if cl.similar(c["bg"], a, 0.05) and cl.similar(c[role], b, 0.06):
                    add("WARN", f"{theme}: bg + {role} match the cliché pair '{pair['name']}'")
        if landscape and theme == "light":
            occupied = landscape.get("occupied_accent_hues") or {}
            b = cl.hue_bin(c["primary"])
            if b is not None and cl.HUE_NAMES[b] in occupied:
                add("INFO", f"primary hue '{cl.HUE_NAMES[b]}' is also used by {', '.join(occupied[cl.HUE_NAMES[b]])}; make sure that is intended")

    fonts = d.get("fonts") or {}
    if not fonts.get("heading") or not fonts.get("body"):
        add("FAIL", "fonts: both 'heading' and 'body' are required (they may be the same family)")
    for slot, f in fonts.items():
        name = f.get("family", "")
        if slot == "mono" and name in defaults["fonts"]["allowed_for_code"]:
            continue
        if name in defaults["fonts"]["overused"]:
            add("WARN", f"fonts: {slot} '{name}' is one of the most overused families; justify it or pick another")
        if name in defaults["fonts"]["ai_favorites"]:
            add("WARN", f"fonts: {slot} '{name}' is a frequent AI/template pick; justify it or pick another")
        fam = meta.get(name.lower()) if meta else None
        if meta is None:
            add("INFO", f"fonts: {slot} '{name}' not verified (run find_fonts.py once to cache Google Fonts metadata)")
        elif fam is None:
            add("INFO", f"fonts: {slot} '{name}' is not on Google Fonts; verify license, hosting, and Turkish glyphs manually")
        else:
            if "latin-ext" not in (fam.get("subsets") or []):
                add("FAIL", f"fonts: {slot} '{name}' has no latin-ext subset, so ğ ş ı İ will fall back to another font")
            if fam.get("popularity", 9999) <= defaults["popularity_cutoff"] and name not in defaults["fonts"]["overused"]:
                add("WARN", f"fonts: {slot} '{name}' is in the Google Fonts top {defaults['popularity_cutoff']} (rank {fam['popularity']})")
            available = {int(k.rstrip('i')) for k in (fam.get('fonts') or {}) if k.rstrip('i').isdigit()}
            missing_w = [w for w in f.get("weights", []) if int(w) not in available and not any(a['tag'] == 'wght' for a in fam.get('axes') or [])]
            if missing_w:
                add("FAIL", f"fonts: {slot} '{name}' has no weight(s) {missing_w}")
    return issues


def compare_directions(dirs: list[dict]) -> list[dict]:
    out = []
    for i, a in enumerate(dirs):
        for b in dirs[i + 1 :]:
            try:
                dist = cl.delta_e(a["colors"]["light"]["primary"], b["colors"]["light"]["primary"])
            except (KeyError, ValueError):
                continue
            if dist < SIMILAR_DIRECTIONS:
                out.append({"level": "WARN", "message": f"directions '{a['id']}' and '{b['id']}' have nearly the same primary color (ΔE {dist:.3f}); offer a real alternative"})
            if a["fonts"].get("heading", {}).get("family") == b["fonts"].get("heading", {}).get("family"):
                out.append({"level": "WARN", "message": f"directions '{a['id']}' and '{b['id']}' share the heading font; vary typography between directions"})
    return out


# --------------------------------------------------------------------------- HTML


CHROME_CSS = """
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font:15px/1.5 system-ui,-apple-system,'Segoe UI',sans-serif;background:#f6f6f4;color:#1d1d1b}
[data-theme=dark] body{background:#161615;color:#e9e9e6}
header.page{padding:24px 16px;max-width:1400px;margin:0 auto;display:flex;flex-wrap:wrap;gap:12px;align-items:baseline;justify-content:space-between}
header.page h1{font-size:20px;margin:0}header.page p{margin:4px 0 0;opacity:.75;max-width:70ch}
button.toggle{font:inherit;padding:8px 14px;border:1px solid currentColor;background:transparent;color:inherit;border-radius:6px;cursor:pointer}
main{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:16px;padding:0 16px 32px;max-width:1400px;margin:0 auto}
.direction{container-type:inline-size;background:var(--bg);color:var(--text);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;font-family:var(--font-body);font-size:var(--fs-body);line-height:var(--lh-body)}
.direction>*{padding:20px}.direction h2,.direction h3,.direction h4,.direction .display{font-family:var(--font-heading);font-weight:var(--w-heading);line-height:var(--lh-heading);margin:0 0 8px}
.meta{border-bottom:1px solid var(--border)}.meta .id{font:600 12px/1 system-ui,sans-serif;letter-spacing:.04em;color:var(--text-muted)}
.meta h2{font-size:var(--fs-h3)}.meta p{margin:6px 0;color:var(--text-muted)}.meta a{color:var(--primary);overflow-wrap:anywhere}
.swatches{display:grid;grid-template-columns:repeat(auto-fill,minmax(112px,1fr));gap:8px;border-bottom:1px solid var(--border)}
.sw{border:1px solid var(--border);border-radius:calc(var(--radius) / 2);overflow:hidden;background:var(--surface);font:12px/1.35 ui-monospace,monospace}
.sw i{display:block;height:44px}.sw span{display:block;padding:6px 8px;color:var(--text)}.sw .d{display:none}[data-theme=dark] .sw .l{display:none}[data-theme=dark] .sw .d{display:block}
.type{border-bottom:1px solid var(--border)}.type .display{font-size:min(var(--fs-display),13cqi)}.type h3{font-size:var(--fs-h2)}.type h4{font-size:var(--fs-h4)}
.type p{max-width:65ch;margin:0 0 8px}.type .lead{font-size:var(--fs-lead)}.type .caption{font-size:var(--fs-caption);color:var(--text-muted)}
.ui{display:grid;gap:14px;background:var(--surface);border-bottom:1px solid var(--border)}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.btn{font:inherit;font-weight:600;padding:10px 16px;border-radius:var(--radius);border:1px solid transparent;cursor:pointer;min-height:44px}
.btn.primary{background:var(--primary);color:var(--on-primary)}.btn.primary:hover{background:var(--primary-hover)}
.btn.secondary{background:transparent;color:var(--text);border-color:var(--border-strong)}
.btn:focus-visible,input:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
label{display:grid;gap:4px;font-size:var(--fs-caption);color:var(--text-muted)}
input{font:inherit;padding:10px 12px;border:1px solid var(--border-strong);border-radius:var(--radius);background:var(--bg);color:var(--text);min-height:44px}
.alert{padding:10px 12px;border-radius:var(--radius);border:1px solid;background:var(--bg)}
.alert b{margin-right:6px}.alert.success{border-color:var(--success)}.alert.success b{color:var(--success)}
.alert.warning{border-color:var(--warning)}.alert.warning b{color:var(--warning)}.alert.danger{border-color:var(--danger)}.alert.danger b{color:var(--danger)}
table{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums}th,td{text-align:left;padding:8px;border-bottom:1px solid var(--border)}
th{font-size:var(--fs-caption);color:var(--text-muted);font-weight:600}.tag{display:inline-block;padding:2px 8px;border-radius:999px;background:var(--primary-soft);color:var(--text);font-size:var(--fs-caption)}
.checks ul{margin:0;padding-left:18px}.checks li{margin:4px 0}.lvl{font:600 11px/1 system-ui,sans-serif;padding:2px 6px;border-radius:4px;margin-right:6px;border:1px solid currentColor}
.FAIL{color:var(--danger)}.WARN{color:var(--warning)}.INFO{color:var(--text-muted)}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""


def css_vars(c: dict, t: dict, fonts: dict, radius: str) -> str:
    v = [f"--{k}:{val}" for k, val in c.items()]
    for role, spec in t.items():
        v.append(f"--fs-{role}:{spec['size']}")
    v += [
        f"--lh-body:{t['body']['line_height']}", f"--lh-heading:{t['h1']['line_height']}",
        f"--font-heading:{font_stack(fonts.get('heading'), 'sans-serif')}", f"--font-body:{font_stack(fonts.get('body'), 'sans-serif')}",
        f"--w-heading:{max((fonts.get('heading') or {}).get('weights', [700]))}", f"--radius:{radius}",
    ]
    return ";".join(v)


def render_direction(d: dict, issues: list[dict], sample: dict) -> tuple[str, str]:
    esc = html.escape
    t = type_scale(d.get("type") or {})
    radius = d.get("radius", "6px")
    light = complete_theme(d["colors"]["light"], False)
    dark = complete_theme(d["colors"]["dark"], True)
    sel = f'.direction[data-dir="{esc(d["id"])}"]'
    css = f"{sel}{{{css_vars(light, t, d['fonts'], radius)}}}\n[data-theme=dark] {sel}{{{css_vars(dark, t, d['fonts'], radius)}}}\n"

    def measure(c, role):
        # Show the contrast that matters for each role, and say what it was measured against.
        if role in ("bg", "surface"):
            return cl.contrast_ratio(c["text"], c[role]), "text"
        if role == "primary":
            return cl.contrast_ratio(c["on-primary"], c["primary"]), "on-primary"
        if role == "on-primary":
            return cl.contrast_ratio(c["on-primary"], c["primary"]), "primary"
        return cl.contrast_ratio(c[role], c["bg"]), "bg"

    def swatch(role):
        labels = []
        for cls, c in (("l", light), ("d", dark)):
            ratio, against = measure(c, role)
            labels.append(f'<span class="{cls}">{role}<br>{c[role]}<br>{ratio:.1f}:1 vs {against}</span>')
        return f'<div class="sw"><i style="background:var(--{role})"></i>{"".join(labels)}</div>'

    roles = ["bg", "surface", "text", "text-muted", "border", "border-strong", "primary", "on-primary", "accent", "success", "warning", "danger"]
    sources = "".join(f'<li><a href="{esc(s)}">{esc(s)}</a></li>' for s in d.get("sources", []))
    rationale = "".join(f"<p>{esc(r)}</p>" for r in d.get("rationale", []))
    fonts_line = " · ".join(f"{slot}: {esc(f['family'])} ({', '.join(str(w) for w in f.get('weights', []))})" for slot, f in d["fonts"].items())
    checks = "".join(f'<li><span class="lvl {i["level"]}">{i["level"]}</span>{esc(i["message"])}</li>' for i in issues) or "<li>No issues found.</li>"
    body = f"""
<section class="direction" data-dir="{esc(d['id'])}" aria-labelledby="dir-{esc(d['id'])}">
  <div class="meta"><div class="id">DIRECTION {esc(d['id']).upper()}</div><h2 id="dir-{esc(d['id'])}">{esc(d.get('name', d['id']))}</h2>
    <p>{esc(d.get('summary', ''))}</p>{rationale}<p>{fonts_line}</p>{f'<ul>{sources}</ul>' if sources else ''}</div>
  <div class="swatches">{''.join(swatch(r) for r in roles)}</div>
  <div class="type"><div class="display">{esc(sample['headline'])}</div><h3>Başlık 2 — Heading two</h3><h4>Başlık 4 — ğüşıöç İĞÜŞÖÇ</h4>
    <p class="lead">{esc(sample['body'])}</p><p>{esc(sample['body'])}</p><p class="caption">Caption · 12 Ağustos 2026 · ₺1.249,90</p></div>
  <div class="ui"><div class="row"><button class="btn primary" type="button">{esc(sample['cta'])}</button><button class="btn secondary" type="button">{esc(sample['secondary'])}</button><span class="tag">Yeni</span></div>
    <label>E-posta<input type="email" placeholder="ad@ornek.com"></label>
    <div class="alert success" role="status"><b>Tamam</b>Değişiklikler kaydedildi.</div>
    <div class="alert warning" role="status"><b>Dikkat</b>Stok 3 adede düştü.</div>
    <div class="alert danger" role="alert"><b>Hata</b>Ödeme reddedildi.</div>
    <table><thead><tr><th>Sipariş</th><th>Durum</th><th>Tutar</th></tr></thead><tbody><tr><td>#10482</td><td>Hazırlanıyor</td><td>₺842,00</td></tr><tr><td>#10483</td><td>Kargoda</td><td>₺1.120,50</td></tr></tbody></table></div>
  <div class="checks"><h4>Checks</h4><ul>{checks}</ul></div>
</section>"""
    return css, body


def render_page(spec: dict, results: list[tuple[dict, list[dict]]], shared: list[dict]) -> str:
    esc = html.escape
    sample = {**DEFAULT_SAMPLE, **(spec.get("sample") or {})}
    css_parts, bodies, links = [], [], []
    for d, issues in results:
        c, b = render_direction(d, issues, sample)
        css_parts.append(c)
        bodies.append(b)
        links.append(f'<link rel="stylesheet" href="{esc(gf_url(d["fonts"]))}">')
    shared_html = "".join(f'<li>{esc(i["level"])}: {esc(i["message"])}</li>' for i in shared)
    return f"""<!doctype html>
<html lang="{esc(spec.get('language', 'tr'))}" data-theme="light">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(spec.get('project', 'Design'))} — directions</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{''.join(links)}
<style>{CHROME_CSS}{''.join(css_parts)}</style></head>
<body><header class="page"><div><h1>{esc(spec.get('project', 'Design'))} — palette and typography directions</h1>
<p>Generated {dt.date.today().isoformat()}. Compare the directions on real interface elements, in both themes, before choosing one.</p>
{f'<ul>{shared_html}</ul>' if shared_html else ''}</div>
<button class="toggle" type="button" onclick="var h=document.documentElement;h.dataset.theme=h.dataset.theme==='dark'?'light':'dark'">Toggle light / dark</button></header>
<main>{''.join(bodies)}</main></body></html>
"""


# --------------------------------------------------------------------------- export


def export(d: dict, out_dir: Path, project: str, issues: list[dict]) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    t = type_scale(d.get("type") or {})
    light = complete_theme(d["colors"]["light"], False)
    dark = complete_theme(d["colors"]["dark"], True)
    fonts = d["fonts"]
    radius = d.get("radius", "6px")

    def block(c):
        return "\n".join(f"  --{k}: {v};" for k, v in c.items())

    type_vars = "\n".join(f"  --fs-{r}: {s['size']};" for r, s in t.items())
    tokens_css = f"""/* {project} — generated by design-system/scripts/build_specimen.py (direction {d['id']}). Flat colors only; no gradients. */
@import url("{gf_url(fonts)}");

:root {{
{block(light)}
  --font-heading: {font_stack(fonts.get('heading'), 'sans-serif')};
  --font-body: {font_stack(fonts.get('body'), 'sans-serif')};
  --font-mono: {font_stack(fonts.get('mono'), 'ui-monospace, monospace')};
{type_vars}
  --lh-body: {t['body']['line_height']};
  --lh-heading: {t['h1']['line_height']};
  --radius: {radius};
}}

@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
{block(dark).replace('  --', '    --')}
  }}
}}

[data-theme="dark"] {{
{block(dark)}
}}
"""
    camel = lambda k: k.split("-")[0] + "".join(p.title() for p in k.split("-")[1:])  # noqa: E731
    tailwind = {"theme": {"extend": {
        "colors": {camel(k): f"var(--{k})" for k in light},
        "fontFamily": {"heading": ["var(--font-heading)"], "body": ["var(--font-body)"], "mono": ["var(--font-mono)"]},
        "fontSize": {r: [f"var(--fs-{r})", {"lineHeight": str(s["line_height"])}] for r, s in t.items()},
        "borderRadius": {"DEFAULT": "var(--radius)"},
    }}}
    tokens_json = {"schema_version": 1, "direction": d["id"], "name": d.get("name"), "colors": {"light": light, "dark": dark},
                   "fonts": fonts, "google_fonts_css": gf_url(fonts), "type_scale": t, "radius": radius}

    def rows(c):
        return "\n".join(f"| `--{k}` | `{light.get(k)}` | `{dark.get(k)}` | {cl.contrast_ratio(light[k], light['bg']):.2f}:1 |" for k in c)

    font_rows = "\n".join(f"| {slot} | {f['family']} | {', '.join(str(w) for w in f.get('weights', []))} | `{font_stack(f, 'sans-serif')}` |" for slot, f in fonts.items())
    scale_rows = "\n".join(f"| {r} | {s['size']} | {s['line_height']} | {s['weight']} |" for r, s in t.items())
    open_issues = "\n".join(f"- **{i['level']}** {i['message']}" for i in issues if i["level"] != "INFO") or "- None"
    sources = "\n".join(f"- {s}" for s in d.get("sources", [])) or "- (none recorded)"
    rationale = "\n".join(f"- {r}" for r in d.get("rationale", [])) or "- (add rationale)"
    design_md = f"""---
name: "{project} Design System"
version: "1.0.0"
status: "draft"
direction: "{d['id']} — {d.get('name', '')}"
generated: "{dt.date.today().isoformat()}"
---

# DESIGN.md — {project}

## 1. Design Intent

{d.get('summary', '(one paragraph: who the product is for and how the interface should feel)')}

### Why this direction

{rationale}

### Evidence

{sources}

## 2. Color System

Flat colors only. Gradients are not part of this system; use them only if a later, documented brand decision requires it.

| Token | Light | Dark | Contrast on light bg |
|---|---|---|---|
{rows(light)}

**Usage rules**

- `--primary` marks the main action and current selection; one primary action per view.
- `--accent` highlights and focus rings; never for large surfaces.
- `--success`, `--warning`, `--danger`, `--info` only carry state. Pair them with an icon or label so meaning does not depend on color alone.
- Body text uses `--text` or `--text-muted` only.

## 3. Typography

Google Fonts: `{gf_url(fonts)}`

| Slot | Family | Weights | CSS stack |
|---|---|---|---|
{font_rows}

| Role | Size | Line height | Weight |
|---|---|---|---|
{scale_rows}

- Keep body line length at 45–75 characters.
- Turkish characters (ğ ş ı İ) must render in the chosen families; test headings in uppercase (`İSTANBUL`).

## 4. Shape and Space

- Radius: `{radius}` for controls and panels.
- Spacing: 4px base scale (4, 8, 12, 16, 24, 32, 48, 64).

## 5. Open Checks

{open_issues}

## 6. Components and Layout

Continue this document from `templates/DESIGN.template.md` sections for components, layout, and UI rules.
"""
    files = {
        "tokens.css": tokens_css,
        "tailwind.theme.json": json.dumps(tailwind, indent=2, ensure_ascii=False) + "\n",
        "design-tokens.json": json.dumps(tokens_json, indent=2, ensure_ascii=False) + "\n",
        "DESIGN.md": design_md,
    }
    written = []
    for name, content in files.items():
        path = out_dir / name
        path.write_text(content, encoding="utf-8")
        written.append(path)
    return written


# --------------------------------------------------------------------------- main


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("directions", help="directions.json")
    p.add_argument("--out", default="specimen.html", help="Specimen HTML path (default specimen.html)")
    p.add_argument("--landscape", help="JSON from scan_site.py --json, to flag hues competitors already use")
    p.add_argument("--export", metavar="ID", help="Export the chosen direction instead of rendering the specimen")
    p.add_argument("--out-dir", default="design", help="Folder for --export files (default design/)")
    p.add_argument("--strict", action="store_true", help="Exit 1 when any FAIL is found")
    args = p.parse_args()

    spec = json.loads(Path(args.directions).read_text(encoding="utf-8"))
    dirs = spec.get("directions") or []
    if not dirs:
        sys.exit("directions.json has no directions")
    defaults = load_defaults()
    meta = load_font_metadata()
    land = None
    if args.landscape:
        land = json.loads(Path(args.landscape).read_text(encoding="utf-8")).get("landscape")
    results = [(d, check_direction(d, defaults, meta, land)) for d in dirs]
    shared = compare_directions(dirs)

    for d, issues in results:
        print(f"Direction {d['id']} — {d.get('name', '')}")
        for i in issues or [{"level": "OK", "message": "no issues"}]:
            print(f"  [{i['level']}] {i['message']}")
    for i in shared:
        print(f"[{i['level']}] {i['message']}")
    failed = any(i["level"] == "FAIL" for _, issues in results for i in issues)

    if args.export:
        match = [(d, i) for d, i in results if d["id"] == args.export]
        if not match:
            sys.exit(f"No direction with id '{args.export}'")
        d, issues = match[0]
        if any(i["level"] == "FAIL" for i in issues):
            print(f"Direction {d['id']} has FAIL checks; fix them before exporting.")
            return 1
        for path in export(d, Path(args.out_dir), spec.get("project", "Project"), issues):
            print(f"wrote {path}")
        return 0

    if any("FAIL" in i["message"] and "missing" in i["message"] for _, iss in results for i in iss):
        print("Some directions are incomplete; the specimen shows only complete ones.")
    renderable = [(d, iss) for d, iss in results if not any(i["level"] == "FAIL" and ("missing" in i["message"] or "flat color" in i["message"]) for i in iss)]
    Path(args.out).write_text(render_page(spec, renderable, shared), encoding="utf-8")
    print(f"wrote {args.out}")
    return 1 if (failed and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
