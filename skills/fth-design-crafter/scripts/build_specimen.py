#!/usr/bin/env python3
"""Check 2-3 palette + typography directions and render a side-by-side demo page.

Input is a directions.json file (see templates/directions.template.json). Color roles
use the DESIGN.md / Material 3 vocabulary (background, surface, on-surface, outline,
primary, on-primary, secondary, error, ...). The script:

* derives the remaining roles (on-* text colors, containers, outline, hover)
* checks WCAG contrast for every text/background pair in light and dark themes
* rejects gradients, flags colors close to AI/template defaults, flags directions
  that are too similar to each other, and (with --landscape) accent hues that
  competitors already occupy
* flags overused or AI-favorite fonts and missing Turkish support
* writes a standalone specimen.html so people compare real UI, not swatches alone
* with --export <id>, writes a spec-compliant DESIGN.md (google-labs-code/design.md),
  tokens.css, and tailwind.theme.json for the chosen direction, then lints DESIGN.md

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

REQUIRED_ROLES = ["background", "surface", "on-surface", "on-surface-variant", "outline-variant",
                  "primary", "on-primary", "secondary", "success", "warning", "error"]
TEXT_PAIRS = [("on-surface", "background"), ("on-surface", "surface"), ("on-surface-variant", "background"),
              ("on-surface-variant", "surface"), ("on-primary", "primary"), ("on-secondary", "secondary"),
              ("on-primary-container", "primary-container"), ("on-success", "success"), ("on-warning", "warning"),
              ("on-error", "error")]
UI_PAIRS = [("outline", "background"), ("primary", "background"), ("secondary", "background"),
            ("success", "background"), ("warning", "background"), ("error", "background")]
SWATCH_ROLES = ["background", "surface", "surface-container", "on-surface", "on-surface-variant", "outline-variant",
                "outline", "primary", "on-primary", "primary-container", "secondary", "success", "warning", "error"]
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


def best_on(color: str, candidates: list[str]) -> str:
    """The first candidate (in preference order) with 4.5:1 against `color`, else the highest-contrast one."""
    for c in candidates:
        if cl.contrast_ratio(c, color) >= 4.5:
            return c
    return max(candidates, key=lambda c: cl.contrast_ratio(c, color))


def complete_theme(colors: dict, dark: bool) -> dict:
    """Fill every derived role from the ones the direction defines (explicit values always win)."""
    c = {k: cl.normalize_hex(v) or v for k, v in colors.items()}
    text, bg = c["on-surface"], c["background"]
    ends = ["#ffffff", text] if not dark else [bg, text, "#000000"]
    c.setdefault("on-background", text)
    c.setdefault("surface-container", cl.mix(c["surface"], text, 0.05))
    if "outline" not in c:
        # Input and control boundaries need 3:1 (WCAG 1.4.11); decorative dividers may stay softer.
        cand = c["outline-variant"]
        for step in range(21):
            cand = cl.mix(c["outline-variant"], text, step / 20)
            if cl.contrast_ratio(cand, bg) >= 3:
                break
        c["outline"] = cand
    c.setdefault("primary-hover", cl.shift_lightness(c["primary"], 0.06 if dark else -0.06))
    c.setdefault("primary-container", cl.mix(c["primary"], bg, 0.86))
    c.setdefault("on-primary-container", text)
    for role in ("secondary", "success", "warning", "error"):
        c.setdefault(f"on-{role}", best_on(c[role], ends))
    return c


def typography_tokens(d: dict) -> dict[str, dict]:
    """DESIGN.md typography levels (spec-recommended names) from the direction's scale."""
    t = d.get("type") or {}
    base, ratio = float(t.get("base", 16)), float(t.get("ratio", 1.25))
    lh_body, lh_head = float(t.get("line_height_body", 1.55)), float(t.get("line_height_heading", 1.15))
    fonts = d["fonts"]
    hw = sorted(int(w) for w in fonts["heading"].get("weights", [700]))
    bw = sorted(int(w) for w in fonts["body"].get("weights", [400, 600]))
    size = lambda n: f"{max(11, round(base * ratio ** n))}px"  # noqa: E731
    head, body = fonts["heading"]["family"], fonts["body"]["family"]
    levels = {
        "headline-display": {"fontFamily": head, "fontSize": size(6), "fontWeight": hw[-1], "lineHeight": lh_head, "letterSpacing": "-0.02em"},
        "headline-lg": {"fontFamily": head, "fontSize": size(5), "fontWeight": hw[-1], "lineHeight": lh_head, "letterSpacing": "-0.01em"},
        "headline-md": {"fontFamily": head, "fontSize": size(4), "fontWeight": hw[-1], "lineHeight": lh_head},
        "headline-sm": {"fontFamily": head, "fontSize": size(3), "fontWeight": hw[0], "lineHeight": round(lh_head + 0.05, 2)},
        "title-md": {"fontFamily": head, "fontSize": size(2), "fontWeight": hw[0], "lineHeight": 1.25},
        "body-lg": {"fontFamily": body, "fontSize": size(1), "fontWeight": bw[0], "lineHeight": lh_body},
        "body-md": {"fontFamily": body, "fontSize": size(0), "fontWeight": bw[0], "lineHeight": lh_body},
        "body-sm": {"fontFamily": body, "fontSize": size(-1), "fontWeight": bw[0], "lineHeight": lh_body},
        "label-lg": {"fontFamily": body, "fontSize": size(0), "fontWeight": bw[-1], "lineHeight": 1.2},
        "label-md": {"fontFamily": body, "fontSize": size(-1), "fontWeight": bw[-1], "lineHeight": 1.2},
        "label-sm": {"fontFamily": body, "fontSize": size(-2), "fontWeight": bw[-1], "lineHeight": 1.2, "letterSpacing": "0.02em"},
    }
    if fonts.get("mono"):
        mw = sorted(int(w) for w in fonts["mono"].get("weights", [400]))
        levels["code-md"] = {"fontFamily": fonts["mono"]["family"], "fontSize": size(-1), "fontWeight": mw[0], "lineHeight": 1.5}
    return levels


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

    if not d.get("reference"):
        add("WARN", "no 'reference': add one sentence naming a specific real-world object or tradition the design follows (DESIGN.md Overview)")

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
            elif ratio < 4.5 and fg in ("primary", "error"):
                add("INFO", f"{theme}: {fg} on {bg} is {ratio:.2f}:1 — fine for fills and icons, too low for {fg}-colored body text")
        for role in ("primary", "secondary", "background"):
            for ref in defaults["colors"]:
                if cl.similar(c[role], ref["hex"], defaults["color_threshold"]):
                    add("WARN", f"{theme}: {role} {c[role]} is close to a template default ({ref['name']} {ref['hex']})")
        for pair in defaults["pairs"]:
            a, b = pair["colors"]
            for role in ("primary", "secondary"):
                if cl.similar(c["background"], a, 0.05) and cl.similar(c[role], b, 0.06):
                    add("WARN", f"{theme}: background + {role} match the cliché pair '{pair['name']}'")
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
.direction{container-type:inline-size;background:var(--color-background);color:var(--color-on-surface);border:1px solid var(--color-outline-variant);border-radius:var(--radius-lg);overflow:hidden;font-family:var(--font-body-md);font-size:var(--text-body-md);line-height:var(--leading-body-md)}
.direction>*{padding:20px}
.direction h2,.direction h3,.direction h4,.direction .display{font-family:var(--font-headline-lg);font-weight:var(--font-weight-headline-lg);line-height:var(--leading-headline-lg);margin:0 0 8px}
.meta{border-bottom:1px solid var(--color-outline-variant)}.meta .id{font:600 12px/1 system-ui,sans-serif;letter-spacing:.04em;color:var(--color-on-surface-variant)}
.meta h2{font-size:var(--text-headline-sm)}.meta p{margin:6px 0;color:var(--color-on-surface-variant)}.meta .ref{color:var(--color-on-surface);font-style:italic}
.meta a{color:var(--color-primary);overflow-wrap:anywhere}
.swatches{display:grid;grid-template-columns:repeat(auto-fill,minmax(112px,1fr));gap:8px;border-bottom:1px solid var(--color-outline-variant)}
.sw{border:1px solid var(--color-outline-variant);border-radius:var(--radius-sm);overflow:hidden;background:var(--color-surface);font:12px/1.35 ui-monospace,monospace}
.sw i{display:block;height:44px}.sw span{display:block;padding:6px 8px;color:var(--color-on-surface)}.sw .d{display:none}[data-theme=dark] .sw .l{display:none}[data-theme=dark] .sw .d{display:block}
.type{border-bottom:1px solid var(--color-outline-variant)}.type .display{font-family:var(--font-headline-display);font-weight:var(--font-weight-headline-display);font-size:min(var(--text-headline-display),13cqi);letter-spacing:var(--tracking-headline-display)}
.type h3{font-size:var(--text-headline-md)}.type h4{font-size:var(--text-title-md);font-weight:var(--font-weight-title-md)}
.type p{max-width:65ch;margin:0 0 8px}.type .lead{font-size:var(--text-body-lg)}.type .caption{font-size:var(--text-body-sm);color:var(--color-on-surface-variant)}
.type code{font-family:var(--font-code-md, ui-monospace, monospace);font-size:var(--text-code-md, 14px)}
.ui{display:grid;gap:14px;background:var(--color-surface);border-bottom:1px solid var(--color-outline-variant)}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.btn{font-family:var(--font-label-lg);font-size:var(--text-label-lg);font-weight:var(--font-weight-label-lg);padding:10px 16px;border-radius:var(--radius-md);border:1px solid transparent;cursor:pointer;min-height:44px}
.btn.primary{background:var(--color-primary);color:var(--color-on-primary)}.btn.primary:hover{background:var(--color-primary-hover)}
.btn.secondary{background:var(--color-surface);color:var(--color-on-surface);border-color:var(--color-outline)}
.btn:focus-visible,input:focus-visible{outline:3px solid var(--color-secondary);outline-offset:2px}
label{display:grid;gap:4px;font-size:var(--text-label-md);font-weight:var(--font-weight-label-md);color:var(--color-on-surface-variant)}
input{font:inherit;padding:10px 12px;border:1px solid var(--color-outline);border-radius:var(--radius-md);background:var(--color-background);color:var(--color-on-surface);min-height:44px}
.badges{display:flex;flex-wrap:wrap;gap:6px}.badge{font-size:var(--text-label-sm);font-weight:var(--font-weight-label-sm);padding:3px 8px;border-radius:var(--radius-sm)}
.badge.success{background:var(--color-success);color:var(--color-on-success)}.badge.warning{background:var(--color-warning);color:var(--color-on-warning)}.badge.error{background:var(--color-error);color:var(--color-on-error)}
.alert{padding:10px 12px;border-radius:var(--radius-md);border:1px solid var(--color-outline-variant);background:var(--color-background)}
.alert b{margin-right:6px}.alert.success{border-color:var(--color-success)}.alert.warning{border-color:var(--color-warning)}.alert.error{border-color:var(--color-error)}
table{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums}th,td{text-align:left;padding:8px;border-bottom:1px solid var(--color-outline-variant)}
th{font-size:var(--text-label-md);color:var(--color-on-surface-variant);font-weight:var(--font-weight-label-md)}
.tag{display:inline-block;padding:2px 8px;border-radius:var(--radius-full);background:var(--color-primary-container);color:var(--color-on-primary-container);font-size:var(--text-label-sm)}
.checks ul{margin:0;padding-left:18px}.checks li{margin:4px 0}.lvl{font:600 11px/1 system-ui,sans-serif;padding:2px 6px;border-radius:4px;margin-right:6px;border:1px solid currentColor}
.FAIL{color:var(--color-error)}.WARN{color:var(--color-on-surface)}.INFO{color:var(--color-on-surface-variant)}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""


def rounded_tokens(d: dict) -> dict[str, str]:
    r = float(str(d.get("radius", "6px")).rstrip("px") or 0)
    fmt = lambda v: f"{round(v):d}px"  # noqa: E731
    return {"none": "0px", "sm": fmt(r / 2), "md": fmt(r), "lg": fmt(r * 2), "full": "9999px"}


def css_vars(colors: dict, typo: dict, rounded: dict, fonts: dict | None = None) -> list[str]:
    """CSS custom properties named like the official design.md css-tailwind export."""
    v = [f"--color-{k}:{val}" for k, val in colors.items()]
    for level, spec in typo.items():
        fam = spec["fontFamily"]
        fallback = next((f.get("fallback", "sans-serif") for f in (fonts or {}).values() if f.get("family") == fam), "sans-serif")
        v += [f"--font-{level}:'{fam}', {fallback}", f"--text-{level}:{spec['fontSize']}",
              f"--leading-{level}:{spec['lineHeight']}", f"--font-weight-{level}:{spec['fontWeight']}"]
        if spec.get("letterSpacing"):
            v.append(f"--tracking-{level}:{spec['letterSpacing']}")
    v += [f"--radius-{k}:{val}" for k, val in rounded.items()]
    return v


def render_direction(d: dict, issues: list[dict], sample: dict) -> tuple[str, str]:
    esc = html.escape
    typo = typography_tokens(d)
    rounded = rounded_tokens(d)
    light = complete_theme(d["colors"]["light"], False)
    dark = complete_theme(d["colors"]["dark"], True)
    sel = f'.direction[data-dir="{esc(d["id"])}"]'
    css = (f"{sel}{{{';'.join(css_vars(light, typo, rounded, d['fonts']))}}}\n"
           f"[data-theme=dark] {sel}{{{';'.join(f'--color-{k}:{v}' for k, v in dark.items())}}}\n")

    def measure(c, role):
        # Show the contrast that matters for each role, and say what it was measured against.
        if role in ("background", "surface", "surface-container"):
            return cl.contrast_ratio(c["on-surface"], c[role]), "on-surface"
        if role in ("primary", "primary-container"):
            on = "on-" + role
            return cl.contrast_ratio(c[on], c[role]), on
        if role == "on-primary":
            return cl.contrast_ratio(c["on-primary"], c["primary"]), "primary"
        return cl.contrast_ratio(c[role], c["background"]), "background"

    def swatch(role):
        labels = []
        for cls, c in (("l", light), ("d", dark)):
            ratio, against = measure(c, role)
            labels.append(f'<span class="{cls}">{role}<br>{c[role]}<br>{ratio:.1f}:1 vs {against}</span>')
        return f'<div class="sw"><i style="background:var(--color-{role})"></i>{"".join(labels)}</div>'

    sources = "".join(f'<li><a href="{esc(s)}">{esc(s)}</a></li>' for s in d.get("sources", []))
    rationale = "".join(f"<p>{esc(r)}</p>" for r in d.get("rationale", []))
    ref = f'<p class="ref">{esc(d["reference"])}</p>' if d.get("reference") else ""
    fonts_line = " · ".join(f"{slot}: {esc(f['family'])} ({', '.join(str(w) for w in f.get('weights', []))})" for slot, f in d["fonts"].items())
    checks = "".join(f'<li><span class="lvl {i["level"]}">{i["level"]}</span>{esc(i["message"])}</li>' for i in issues) or "<li>No issues found.</li>"
    code = '<p><code>TR-4471-0930-B · 2026-08-12 14:05</code></p>' if "code-md" in typo else ""
    body = f"""
<section class="direction" data-dir="{esc(d['id'])}" aria-labelledby="dir-{esc(d['id'])}">
  <div class="meta"><div class="id">DIRECTION {esc(d['id']).upper()}</div><h2 id="dir-{esc(d['id'])}">{esc(d.get('name', d['id']))}</h2>
    {ref}<p>{esc(d.get('summary', ''))}</p>{rationale}<p>{fonts_line}</p>{f'<ul>{sources}</ul>' if sources else ''}</div>
  <div class="swatches">{''.join(swatch(r) for r in SWATCH_ROLES)}</div>
  <div class="type"><div class="display">{esc(sample['headline'])}</div><h3>Başlık 2 — Heading two</h3><h4>Başlık 4 — ğüşıöç İĞÜŞÖÇ</h4>
    <p class="lead">{esc(sample['body'])}</p><p>{esc(sample['body'])}</p>{code}<p class="caption">Caption · 12 Ağustos 2026 · ₺1.249,90</p></div>
  <div class="ui"><div class="row"><button class="btn primary" type="button">{esc(sample['cta'])}</button><button class="btn secondary" type="button">{esc(sample['secondary'])}</button><span class="tag">Yeni</span></div>
    <label>E-posta<input type="email" placeholder="ad@ornek.com"></label>
    <div class="badges"><span class="badge success">Teslim edildi</span><span class="badge warning">Gecikmede</span><span class="badge error">İade</span></div>
    <div class="alert success" role="status"><b>Tamam</b>Değişiklikler kaydedildi.</div>
    <div class="alert warning" role="status"><b>Dikkat</b>Stok 3 adede düştü.</div>
    <div class="alert error" role="alert"><b>Hata</b>Ödeme reddedildi.</div>
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
        import design_md
        import lint_design_md

        match = [(d, i) for d, i in results if d["id"] == args.export]
        if not match:
            sys.exit(f"No direction with id '{args.export}'")
        d, issues = match[0]
        if any(i["level"] == "FAIL" for i in issues):
            print(f"Direction {d['id']} has FAIL checks; fix them before exporting.")
            return 1
        written = design_md.export(d, Path(args.out_dir), spec.get("project", "Project"), issues)
        for path in written:
            print(f"wrote {path}")
        report = lint_design_md.lint_file(Path(args.out_dir) / "DESIGN.md")
        print(lint_design_md.format_report(report))
        return 1 if report["summary"]["errors"] else 0

    if any("FAIL" in i["message"] and "missing" in i["message"] for _, iss in results for i in iss):
        print("Some directions are incomplete; the specimen shows only complete ones.")
    renderable = [(d, iss) for d, iss in results if not any(i["level"] == "FAIL" and ("missing" in i["message"] or "flat color" in i["message"]) for i in iss)]
    Path(args.out).write_text(render_page(spec, renderable, shared), encoding="utf-8")
    print(f"wrote {args.out}")
    return 1 if (failed and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
