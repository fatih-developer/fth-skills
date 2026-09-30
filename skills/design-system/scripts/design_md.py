"""Write a DESIGN.md that follows the google-labs-code/design.md spec (version alpha).

Layout of the generated file:

* YAML front matter with the normative tokens: ``colors`` (light roles plus a
  ``-dark`` twin for every role), ``typography`` (spec-recommended level names),
  ``rounded``, ``spacing``, and ``components`` that reference every color so the
  official ``orphaned-tokens`` and ``contrast-ratio`` rules have what they need.
* The eight canonical ``##`` sections in spec order (Overview, Colors, Typography,
  Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts). Prose refers to
  tokens as ``{colors.primary}``.
* A trailing ``## Evidence`` section (unknown sections are allowed by the spec and
  ignored by its order check) with the reference, rationale, sources, and checks.

Also writes tokens.css (CSS custom properties named like the official
css-tailwind export, plus a dark-theme switch) and tailwind.theme.json (Tailwind v3,
bound to those variables).
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import build_specimen as bs
import colorlib as cl

ROLE_ORDER = [
    "background", "on-background", "surface", "on-surface", "on-surface-variant", "surface-container",
    "outline-variant", "outline", "primary", "on-primary", "primary-hover", "primary-container",
    "on-primary-container", "secondary", "on-secondary", "success", "on-success", "warning", "on-warning",
    "error", "on-error",
]
DEFAULT_SPACING = {"xs": "4px", "sm": "8px", "md": "16px", "lg": "24px", "xl": "32px", "2xl": "48px",
                   "3xl": "64px", "gutter": "24px", "margin": "16px", "max-width": "1200px"}
ROLE_NOTES = {
    "background": "the page canvas",
    "surface": "cards, panels, table rows, and dialogs",
    "surface-container": "a second tonal layer for grouped or selected areas",
    "on-surface": "all headings and body text",
    "on-surface-variant": "secondary text: captions, metadata, helper text",
    "outline-variant": "hairline dividers and decorative borders",
    "outline": "input and control boundaries (at least 3:1 against the background)",
    "primary": "the one main action per view and the current selection",
    "primary-container": "quiet emphasis such as tags and selected rows",
    "secondary": "focus rings and highlights; never a second call to action",
    "success": "completed and positive states, always with a label or icon",
    "warning": "attention states that need action soon, always with a label or icon",
    "error": "errors and destructive actions, always with a label or icon",
}
CORE_ROLES = ["background", "surface", "on-surface", "on-surface-variant", "outline-variant", "outline",
              "primary", "primary-container", "secondary", "success", "warning", "error"]
DEFAULT_DOS = [
    "Do use {colors.primary} for the single most important action on each screen.",
    "Do keep every color flat; hierarchy comes from tone, type, space, and borders.",
    "Do pair state colors ({colors.success}, {colors.warning}, {colors.error}) with a label or icon.",
    "Do keep body text at {typography.body-md} with 45-75 characters per line.",
    "Do test headings in uppercase Turkish (İSTANBUL, IĞDIR) and prices with ₺ before shipping a new font weight.",
]
DEFAULT_DONTS = [
    "Don't use gradients, glow, glass or blur effects, or decorative 3D shapes.",
    "Don't introduce colors or font sizes that are not tokens in this file.",
    "Don't use {colors.secondary} as a second call-to-action color.",
    "Don't put body text in {colors.primary} or any state color.",
    "Don't mix corner radii beyond the {rounded.sm} / {rounded.md} / {rounded.lg} scale in one view.",
]


# --------------------------------------------------------------------------- tokens


def build_tokens(d: dict) -> dict:
    light = bs.complete_theme(d["colors"]["light"], False)
    dark = bs.complete_theme(d["colors"]["dark"], True)
    roles = [r for r in ROLE_ORDER if r in light] + [r for r in light if r not in ROLE_ORDER]
    colors = {r: light[r] for r in roles}
    colors.update({f"{r}-dark": dark[r] for r in roles if r in dark})
    typography = bs.typography_tokens(d)
    rounded = bs.rounded_tokens(d)
    spacing = {**DEFAULT_SPACING, **(d.get("spacing") or {})}
    components = {}
    for suffix in ("", "-dark"):
        c = lambda role: "{colors." + role + suffix + "}"  # noqa: E731
        comps = {
            "page": {"backgroundColor": c("background"), "textColor": c("on-background")},
            "card": {"backgroundColor": c("surface"), "textColor": c("on-surface"), "rounded": "{rounded.lg}", "padding": spacing["lg"]},
            "card-meta": {"backgroundColor": c("surface"), "textColor": c("on-surface-variant"), "typography": "{typography.body-sm}"},
            "panel": {"backgroundColor": c("surface-container"), "textColor": c("on-surface"), "rounded": "{rounded.md}", "padding": spacing["md"]},
            "divider": {"backgroundColor": c("outline-variant"), "height": "1px"},
            "input": {"backgroundColor": c("background"), "textColor": c("on-surface"), "typography": "{typography.body-md}",
                      "rounded": "{rounded.md}", "padding": "12px", "height": "44px"},
            "input-border": {"backgroundColor": c("outline"), "height": "1px"},
            "button-primary": {"backgroundColor": c("primary"), "textColor": c("on-primary"), "typography": "{typography.label-lg}",
                               "rounded": "{rounded.md}", "padding": "12px", "height": "44px"},
            "button-primary-hover": {"backgroundColor": c("primary-hover"), "textColor": c("on-primary")},
            "button-secondary": {"backgroundColor": c("surface"), "textColor": c("on-surface"), "typography": "{typography.label-lg}",
                                 "rounded": "{rounded.md}", "padding": "12px", "height": "44px"},
            "focus-highlight": {"backgroundColor": c("secondary"), "textColor": c("on-secondary"), "width": "3px"},
            "tag": {"backgroundColor": c("primary-container"), "textColor": c("on-primary-container"),
                    "typography": "{typography.label-sm}", "rounded": "{rounded.full}", "padding": "4px"},
            "badge-success": {"backgroundColor": c("success"), "textColor": c("on-success"), "typography": "{typography.label-sm}", "rounded": "{rounded.sm}", "padding": "4px"},
            "badge-warning": {"backgroundColor": c("warning"), "textColor": c("on-warning"), "typography": "{typography.label-sm}", "rounded": "{rounded.sm}", "padding": "4px"},
            "badge-error": {"backgroundColor": c("error"), "textColor": c("on-error"), "typography": "{typography.label-sm}", "rounded": "{rounded.sm}", "padding": "4px"},
        }
        if "code-md" in typography:
            comps["code"] = {"backgroundColor": c("surface-container"), "textColor": c("on-surface"), "typography": "{typography.code-md}",
                             "rounded": "{rounded.sm}", "padding": "2px"}
        for name, props in comps.items():
            components[name + suffix] = props
    return {"light": light, "dark": dark, "roles": roles, "colors": colors, "typography": typography,
            "rounded": rounded, "spacing": spacing, "components": components}


# --------------------------------------------------------------------------- YAML


def _scalar(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return f"{v:g}" if isinstance(v, float) else str(v)
    return json.dumps(str(v), ensure_ascii=False)  # JSON strings are valid YAML double-quoted scalars


def to_yaml(data: dict, indent: int = 0) -> str:
    lines = []
    pad = "  " * indent
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{pad}{key}:")
            lines.append(to_yaml(value, indent + 1))
        else:
            lines.append(f"{pad}{key}: {_scalar(value)}")
    return "\n".join(lines)


# --------------------------------------------------------------------------- prose


def _names(d: dict) -> dict[str, str]:
    return {k: v for k, v in (d.get("color_names") or {}).items()}


def render(d: dict, project: str, issues: list[dict]) -> str:
    tok = build_tokens(d)
    light, dark, typo = tok["light"], tok["dark"], tok["typography"]
    names = _names(d)
    notes = {**ROLE_NOTES, **(d.get("color_notes") or {})}
    fonts = d["fonts"]
    front = {
        "version": "alpha",
        "name": f"{project} — {d.get('name', d['id'])}",
        "description": d.get("summary", ""),
        "colors": tok["colors"],
        "typography": typo,
        "rounded": tok["rounded"],
        "spacing": tok["spacing"],
        "components": tok["components"],
    }

    overview = [d.get("reference") or "(Add one sentence naming a specific real-world object or tradition this design follows.)", ""]
    if d.get("summary"):
        overview += [d["summary"], ""]
    if d.get("audience"):
        overview += [f"Audience: {d['audience']}", ""]
    overview.append(
        "Light is the default theme. Every color token has a `-dark` twin (for example `{colors.surface-dark}`) that replaces it "
        "when `[data-theme=\"dark\"]` is set or the system prefers a dark scheme. Components follow the same convention "
        "(`button-primary` / `button-primary-dark`)."
    )

    color_lines = [d.get("color_intro") or "A flat palette: every role is a single color, and hierarchy comes from tone, type, and space rather than effects.", ""]
    for role in CORE_ROLES:
        label = names.get(role, role.replace("-", " ").title())
        color_lines.append(f"- **{label}** {{colors.{role}}} (`{light[role]}`): {notes[role]}.")
    color_lines += ["", "### Dark theme", "", "| Token | Light | Dark |", "|---|---|---|"]
    color_lines += [f"| `{r}` | `{light[r]}` | `{dark[r]}` |" for r in tok["roles"]]
    color_lines += ["", "### Measured contrast", ""]
    for fg, bg in (("on-surface", "background"), ("on-surface-variant", "surface"), ("on-primary", "primary"), ("outline", "background")):
        color_lines.append(f"- `{fg}` on `{bg}`: {cl.contrast_ratio(light[fg], light[bg]):.1f}:1 light, {cl.contrast_ratio(dark[fg], dark[bg]):.1f}:1 dark.")

    type_lines = []
    for slot, role in (("heading", "headings and display text"), ("body", "body text, labels, and UI"), ("mono", "codes, IDs, and tabular data")):
        f = fonts.get(slot)
        if f:
            why = (d.get("type_notes") or {}).get(slot, "")
            type_lines.append(f"- **{f['family']}** for {role}" + (f": {why.rstrip('.')}." if why else "."))
    type_lines += [
        "",
        f"Load from Google Fonts: `{bs.gf_url(fonts)}`",
        "",
        "- {typography.headline-display} only for the one hero statement of a page; {typography.headline-lg} and {typography.headline-md} for page and section titles; {typography.headline-sm} and {typography.title-md} for card and panel titles.",
        "- {typography.body-md} is the default reading size; {typography.body-lg} for short lead paragraphs; {typography.body-sm} for captions and metadata.",
        "- {typography.label-lg} for buttons, {typography.label-md} for form labels and table headers, {typography.label-sm} for tags and badges.",
    ]
    if "code-md" in typo:
        type_lines.append("- {typography.code-md} for tracking codes, IDs, and other strings people copy or compare character by character.")
    type_lines += [
        "- Use tabular figures for prices, quantities, and tables.",
        "- All families support Turkish (latin-ext): ğ Ğ ş Ş ı İ and ₺ render in the brand fonts, not a fallback.",
    ]

    layout = d.get("layout") or {}
    layout_lines = [
        layout.get("model") or "Mobile-first. One column below 640px; a 12-column grid from 1024px with a maximum content width of {spacing.max-width}.",
        "",
        "Spacing follows a 4px base: {spacing.xs}, {spacing.sm}, {spacing.md}, {spacing.lg}, {spacing.xl}, {spacing.2xl}, {spacing.3xl}. "
        "Page margins are {spacing.margin} on mobile and grid gutters {spacing.gutter}. Related items sit {spacing.sm} apart; separate groups {spacing.lg} or more.",
    ]
    if layout.get("density"):
        layout_lines += ["", layout["density"]]

    elevation = d.get("elevation") or (
        "Depth comes from tonal layers, not shadows: {colors.background} for the page, {colors.surface} for cards and panels, "
        "{colors.surface-container} for grouped or selected areas, separated by hairline {colors.outline-variant} borders. "
        "Overlays (menus, dialogs) may use one small, neutral shadow. No gradients, glow, glass, or blur."
    )
    r = tok["rounded"]
    shapes = d.get("shapes") or (
        f"Controls (buttons, inputs) use {{rounded.md}} ({r['md']}); cards and panels use {{rounded.lg}} ({r['lg']}); "
        f"badges use {{rounded.sm}} ({r['sm']}); tags are pills ({{rounded.full}}). Nothing else is rounded; images and tables keep square corners."
    )

    comp_lines = [
        "The format has no border property, so `input-border` and `divider` carry border colors in `backgroundColor`.",
        "",
        "- **Buttons:** `button-primary` is the only filled action per view; hover darkens to `button-primary-hover`. `button-secondary` sits on {colors.surface} with a 1px {colors.outline} border. Minimum height 44px.",
        "- **Inputs:** `input` on {colors.background} with a 1px `input-border` ({colors.outline}); labels above in {typography.label-md}; errors below in {colors.error} with an icon.",
        "- **Focus:** a 3px {colors.secondary} outline with 2px offset (`focus-highlight`) on every interactive element.",
        "- **Cards and panels:** `card` for content blocks, `panel` for grouped or selected areas, `card-meta` for secondary text inside cards.",
        "- **Tags and badges:** `tag` for neutral labels; `badge-success`, `badge-warning`, `badge-error` for state, always with text.",
        "- **Tables:** rows separated by `divider`; headers in {typography.label-md} and {colors.on-surface-variant}; numbers right-aligned with tabular figures.",
    ]
    if "code-md" in typo:
        comp_lines.append("- **Codes:** `code` for IDs and tracking numbers.")

    dos = [*DEFAULT_DOS, *(d.get("dos") or [])]
    donts = [*DEFAULT_DONTS, *(d.get("donts") or [])]
    dd = [f"- {x}" for x in dos] + [f"- {x}" for x in donts]

    open_issues = [f"- **{i['level']}** {i['message']}" for i in issues if i["level"] != "INFO"] or ["- None open at export."]
    evidence = [
        f"Direction `{d['id']}` ({d.get('name', '')}), exported {dt.date.today().isoformat()} with design-system/scripts/build_specimen.py.",
        "",
        "Why this direction:",
        "",
        *([f"- {x}" for x in d.get("rationale", [])] or ["- (add rationale)"]),
        "",
        "Sources:",
        "",
        *([f"- {x}" for x in d.get("sources", [])] or ["- (none recorded)"]),
        "",
        "Open checks:",
        "",
        *open_issues,
    ]

    body = [
        f"# {project}",
        "",
        "## Overview", "", *overview, "",
        "## Colors", "", *color_lines, "",
        "## Typography", "", *type_lines, "",
        "## Layout", "", *layout_lines, "",
        "## Elevation & Depth", "", elevation, "",
        "## Shapes", "", shapes, "",
        "## Components", "", *comp_lines, "",
        "## Do's and Don'ts", "", *dd, "",
        "## Evidence", "", *evidence, "",
    ]
    return "---\n" + to_yaml(front) + "\n---\n\n" + "\n".join(body)


# --------------------------------------------------------------------------- CSS / Tailwind


def render_css(d: dict, project: str) -> str:
    tok = build_tokens(d)
    base = bs.css_vars(tok["light"], tok["typography"], tok["rounded"], d["fonts"])
    base += [f"--spacing-{k}:{v}" for k, v in tok["spacing"].items()]
    root = "\n".join(f"  {line.replace(':', ': ', 1)};" for line in base)
    dark = "\n".join(f"  --color-{k}: {v};" for k, v in tok["dark"].items())
    return f"""/* {project} — direction {d['id']}. Generated by design-system/scripts/design_md.py from DESIGN.md tokens.
   Variable names match `npx @google/design.md export --format css-tailwind`. Flat colors only. */
@import url("{bs.gf_url(d['fonts'])}");

:root {{
{root}
}}

@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
{dark.replace('  --', '    --')}
  }}
}}

[data-theme="dark"] {{
{dark}
}}
"""


def render_tailwind(d: dict) -> str:
    tok = build_tokens(d)
    theme = {
        "colors": {k: f"var(--color-{k})" for k in tok["light"]},
        "fontFamily": {k: [f"var(--font-{k})"] for k in tok["typography"]},
        "fontSize": {k: [f"var(--text-{k})", {"lineHeight": f"var(--leading-{k})", "fontWeight": f"var(--font-weight-{k})"}] for k in tok["typography"]},
        "borderRadius": {k: f"var(--radius-{k})" for k in tok["rounded"]},
        "spacing": {k: f"var(--spacing-{k})" for k in tok["spacing"]},
    }
    return json.dumps({"theme": {"extend": theme}}, indent=2, ensure_ascii=False) + "\n"


def export(d: dict, out_dir: Path, project: str, issues: list[dict]) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    files = {
        "DESIGN.md": render(d, project, issues),
        "tokens.css": render_css(d, project),
        "tailwind.theme.json": render_tailwind(d),
    }
    written = []
    for name, content in files.items():
        path = out_dir / name
        path.write_text(content, encoding="utf-8")
        written.append(path)
    return written
