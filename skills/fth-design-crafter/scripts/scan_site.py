#!/usr/bin/env python3
"""Scan public websites for the colors, fonts, and gradients they actually use.

Reads the HTML and up to --max-css stylesheets per URL (read-only, one request per
file). With several URLs it also maps which accent hues the competitors occupy, so a
new palette can take a deliberate position instead of repeating the category default.

Examples:
    python scan_site.py https://example.com
    python scan_site.py https://a.com https://b.com https://c.com --json > landscape.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import colorlib as cl  # noqa: E402

UA = "Mozilla/5.0 (compatible; fth-skills-design-scan/1.0; read-only)"
COLOR_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b|(?:rgba?|hsla?|oklch)\([^)]*\)", re.I)
DECL_RE = re.compile(r"(?<![-\w])(color|background(?:-color)?|border(?:-[a-z]+)?-color|border|fill|stroke|outline(?:-color)?|--[\w-]+)\s*:\s*([^;{}]+)", re.I)
FONT_FAMILY_RE = re.compile(r"font-family\s*:\s*([^;{}]+)", re.I)
FONT_FACE_RE = re.compile(r"@font-face\s*{[^}]*?font-family\s*:\s*([^;}]+)", re.I | re.S)
GRADIENT_RE = re.compile(r"(?:repeating-)?(?:linear|radial|conic)-gradient\(", re.I)
GENERIC = {"serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui", "ui-sans-serif", "ui-serif", "ui-monospace",
           "-apple-system", "blinkmacsystemfont", "segoe ui", "helvetica neue", "helvetica", "arial", "apple color emoji",
           "segoe ui emoji", "segoe ui symbol", "noto color emoji", "inherit", "initial", "unset", "var",
           "sfmono-regular", "sf mono", "menlo", "monaco", "consolas", "liberation mono", "liberation sans", "courier new", "courier",
           "ubuntu", "cantarell", "oxygen"}


class _Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stylesheets: list[str] = []
        self.font_links: list[str] = []
        self.css: list[str] = []
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and a.get("href"):
            rel = (a.get("rel") or "").lower()
            href = a["href"]
            if "stylesheet" in rel or href.endswith(".css") or ("fonts.googleapis" in href and "/css" in href):
                self.stylesheets.append(href)
            if any(h in href for h in ("fonts.googleapis", "use.typekit", "api.fontshare", "fonts.bunny")):
                self.font_links.append(href)
        if tag == "style":
            self._in_style = True
        if a.get("style"):
            self.css.append("x{" + a["style"] + "}")

    def handle_endtag(self, tag):
        if tag == "style":
            self._in_style = False

    def handle_data(self, data):
        if self._in_style:
            self.css.append(data)


def fetch(url: str, limit: int = 3_000_000) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,text/css,*/*"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read(limit).decode(resp.headers.get_content_charset() or "utf-8", errors="replace")


def families(value: str) -> list[str]:
    out = []
    for part in value.split(","):
        name = part.strip().strip("'\"").strip()
        low = name.lower()
        if low.endswith(" fallback") or " adjusted" in low or low.startswith("__"):
            continue  # framework-generated metric fallbacks, not real design choices
        if name and not low.startswith("var(") and low not in GENERIC:
            out.append(name)
    return out


def scan_css(css: str, colors: Counter, fonts: Counter, faces: set, stats: dict) -> None:
    stats["gradients"] += len(GRADIENT_RE.findall(css))
    for prop, value in DECL_RE.findall(css):
        if GRADIENT_RE.search(value):
            continue
        for raw in COLOR_RE.findall(value):
            hx = cl.normalize_hex(raw)
            if hx:
                colors[hx] += 1
        if prop.startswith("--"):
            stats["custom_properties"] += 1
    for value in FONT_FAMILY_RE.findall(css):
        for name in families(value):
            fonts[name] += 1
    for value in FONT_FACE_RE.findall(css):
        for name in families(value):
            faces.add(name)


def merge_similar(colors: Counter, threshold: float = 0.02) -> list[tuple[str, int]]:
    merged: list[list] = []
    for hx, n in colors.most_common():
        for group in merged:
            if cl.delta_e(hx, group[0]) < threshold:
                group[1] += n
                break
        else:
            merged.append([hx, n])
    return [(h, n) for h, n in merged]


def classify(palette: list[tuple[str, int]]) -> dict:
    neutrals, accents = [], []
    for hx, n in palette:
        L, C, H = cl.to_oklch(hx)
        (neutrals if C < 0.04 else accents).append({"hex": hx, "count": n, "L": round(L, 3), "C": round(C, 3), "H": round(H)})
    light = [c for c in neutrals if c["L"] > 0.9]
    dark = [c for c in neutrals if c["L"] < 0.3]
    theme = "dark" if dark and light and dark[0]["count"] > light[0]["count"] * 1.5 else "light"
    bg_pool, text_pool = (dark, light) if theme == "dark" else (light, dark)
    return {
        "accents": accents[:8],
        "neutrals": neutrals[:8],
        "likely_background": (bg_pool or neutrals or [{}])[0].get("hex"),
        "likely_text": (text_pool or neutrals or [{}])[0].get("hex"),
        "likely_theme": theme,
    }


def scan(url: str, max_css: int) -> dict:
    result = {"url": url, "errors": []}
    try:
        html = fetch(url)
    except Exception as err:  # noqa: BLE001 - report every network/decoding error
        result["errors"].append(f"fetch failed: {err}")
        return result
    col = _Collector()
    col.feed(html)
    colors, fonts, faces = Counter(), Counter(), set()
    stats = {"gradients": 0, "custom_properties": 0, "stylesheets_read": 0}
    for css in col.css:
        scan_css(css, colors, fonts, faces, stats)
    for href in col.stylesheets[:max_css]:
        full = urllib.parse.urljoin(url, href)
        try:
            scan_css(fetch(full), colors, fonts, faces, stats)
            stats["stylesheets_read"] += 1
        except Exception as err:  # noqa: BLE001
            result["errors"].append(f"css {full}: {err}")
    palette = merge_similar(colors)
    result.update({
        "stats": stats,
        "palette": classify(palette),
        "fonts": [{"family": f, "uses": n, "self_hosted": f in faces} for f, n in fonts.most_common(8)],
        "font_services": sorted(set(col.font_links)),
    })
    return result


def landscape(results: list[dict]) -> dict:
    bins: dict[int, list[str]] = {}
    fonts = Counter()
    for r in results:
        seen_bins = set()
        for acc in r.get("palette", {}).get("accents", [])[:3]:
            b = cl.hue_bin(acc["hex"])
            if b is not None and b not in seen_bins:
                seen_bins.add(b)
                bins.setdefault(b, []).append(urllib.parse.urlparse(r["url"]).netloc)
        for f in r.get("fonts", [])[:2]:
            fonts[f["family"]] += 1
    occupied = {cl.HUE_NAMES[b]: sites for b, sites in sorted(bins.items())}
    free = [cl.HUE_NAMES[b] for b in range(12) if b not in bins]
    return {"occupied_accent_hues": occupied, "free_accent_hues": free, "shared_fonts": [f for f, n in fonts.most_common() if n > 1]}


def to_markdown(results: list[dict], land: dict | None) -> str:
    out = []
    for r in results:
        out.append(f"## {r['url']}")
        if r["errors"]:
            out.append("Errors: " + "; ".join(r["errors"][:3]))
        if "palette" not in r:
            out.append("")
            continue
        p = r["palette"]
        out.append(f"- Theme: {p['likely_theme']} | background {p['likely_background']} | text {p['likely_text']} | gradients: {r['stats']['gradients']} | stylesheets read: {r['stats']['stylesheets_read']}")
        out.append("- Accents: " + (", ".join(f"`{a['hex']}` ×{a['count']} ({cl.HUE_NAMES[cl.hue_bin(a['hex'])]})" for a in p["accents"][:5]) or "none"))
        out.append("- Neutrals: " + (", ".join(f"`{n['hex']}` ×{n['count']}" for n in p["neutrals"][:5]) or "none"))
        out.append("- Fonts: " + (", ".join(f"{f['family']} ×{f['uses']}" for f in r["fonts"][:4]) or "none found (may load via JS)"))
        out.append("")
    if land:
        out.append("## Landscape")
        out.append("- Occupied accent hues: " + (", ".join(f"{h} ({', '.join(s)})" for h, s in land["occupied_accent_hues"].items()) or "none"))
        out.append("- Free accent hues: " + ", ".join(land["free_accent_hues"]))
        out.append("- Fonts shared by several sites: " + (", ".join(land["shared_fonts"]) or "none"))
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("urls", nargs="+")
    p.add_argument("--max-css", type=int, default=6, help="Stylesheets to read per site (default 6)")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    results = [scan(u, args.max_css) for u in args.urls]
    land = landscape(results) if len(results) > 1 else None
    if args.json:
        print(json.dumps({"sites": results, "landscape": land}, indent=2, ensure_ascii=False))
    else:
        print(to_markdown(results, land))
    return 0 if any("palette" in r for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
