#!/usr/bin/env python3
"""Find and check Google Fonts candidates beyond the overused defaults.

Uses the public Google Fonts metadata (cached for 7 days) so that "popular" and
"supports Turkish" are measured, not guessed. Standard library only.

Examples:
    python find_fonts.py search --category serif --variable --limit 15
    python find_fonts.py search --category sans-serif --axes wdth --min-weights 5
    python find_fonts.py search --category display --query slab
    python find_fonts.py check "Bricolage Grotesque" "Literata" "Satoshi"
    python find_fonts.py css "Literata:400,600" "Schibsted Grotesk:500,700"
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
METADATA_URL = "https://fonts.google.com/metadata/fonts"
CACHE = Path.home() / ".cache" / "fth-skills" / "google-fonts-metadata.json"
CACHE_TTL = 7 * 24 * 3600
CATEGORIES = {
    "serif": "Serif",
    "sans-serif": "Sans Serif",
    "sans": "Sans Serif",
    "display": "Display",
    "handwriting": "Handwriting",
    "monospace": "Monospace",
    "mono": "Monospace",
}


def load_defaults() -> dict:
    return json.loads((HERE / "ai_defaults.json").read_text(encoding="utf-8"))


def load_metadata(path: str | None) -> list[dict]:
    """Return the family list from a local file, a fresh cache, or the network."""
    if path:
        raw = Path(path).read_text(encoding="utf-8")
    elif CACHE.exists() and time.time() - CACHE.stat().st_mtime < CACHE_TTL:
        raw = CACHE.read_text(encoding="utf-8")
    else:
        req = urllib.request.Request(METADATA_URL, headers={"User-Agent": "fth-skills-design-system/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8")
        except OSError as err:
            if CACHE.exists():
                print(f"[warn] network failed ({err}); using stale cache", file=sys.stderr)
                raw = CACHE.read_text(encoding="utf-8")
            else:
                sys.exit(f"Cannot load Google Fonts metadata ({err}). Pass --metadata <file> or check network access.")
        else:
            CACHE.parent.mkdir(parents=True, exist_ok=True)
            CACHE.write_text(raw, encoding="utf-8")
    if raw.startswith(")]}'"):
        raw = raw.split("\n", 1)[1]
    return json.loads(raw)["familyMetadataList"]


def weights(fam: dict) -> list[int]:
    fonts = fam.get("fonts") or {}
    return sorted({int(k.rstrip("i")) for k in fonts if k.rstrip("i").isdigit()})


def axes(fam: dict) -> list[str]:
    return [a["tag"] for a in fam.get("axes") or []]


def turkish(fam: dict) -> bool:
    # ğ ş ı İ live in Latin Extended-A, which Google Fonts ships as the latin-ext subset.
    return "latin-ext" in (fam.get("subsets") or [])


def flags(fam: dict, defaults: dict, cutoff: int) -> list[str]:
    out = []
    name = fam["family"]
    f = defaults["fonts"]
    if name in f["overused"]:
        out.append("overused")
    if name in f["ai_favorites"]:
        out.append("ai-favorite")
    if fam.get("popularity", 9999) <= cutoff:
        out.append(f"top-{cutoff}")
    if not turkish(fam):
        out.append("no-turkish")
    if fam.get("isBrandFont"):
        out.append("vendor-brand")
    return out


def describe(fam: dict, defaults: dict, cutoff: int) -> dict:
    return {
        "family": fam["family"],
        "category": fam.get("category"),
        "classifications": fam.get("classifications") or [],
        "popularity_rank": fam.get("popularity"),
        "weights": weights(fam),
        "axes": axes(fam),
        "turkish": turkish(fam),
        "open_source": fam.get("isOpenSource"),
        "designers": fam.get("designers") or [],
        "added": fam.get("dateAdded"),
        "flags": flags(fam, defaults, cutoff),
        "url": "https://fonts.google.com/specimen/" + fam["family"].replace(" ", "+"),
    }


def search(args, fams, defaults) -> list[dict]:
    cutoff = args.skip_top
    cat = CATEGORIES.get(args.category.lower()) if args.category else None
    if args.category and not cat:
        sys.exit(f"Unknown category '{args.category}'. Use one of: {', '.join(sorted(set(CATEGORIES)))}")
    blocked = set(defaults["fonts"]["overused"]) | set(defaults["fonts"]["ai_favorites"])
    out = []
    for fam in fams:
        if cat and fam.get("category") != cat:
            continue
        if args.classification and args.classification.lower() not in [c.lower() for c in fam.get("classifications") or []]:
            continue
        if args.query and args.query.lower() not in (fam["family"] + " " + " ".join(fam.get("designers") or [])).lower():
            continue
        if not args.allow_defaults and (fam["family"] in blocked or fam.get("popularity", 9999) <= cutoff):
            continue
        if not args.no_turkish and not turkish(fam):
            continue
        if fam.get("isNoto") and not args.include_noto:
            continue
        if fam.get("isBrandFont") and not args.allow_defaults:
            continue  # vendor brand families (Google Sans, Roboto Flex, ...)
        if fam.get("primaryScript") and not args.include_other_scripts:
            continue  # designed primarily for a non-Latin script
        if args.variable and "wght" not in axes(fam):
            continue
        if args.axes and not set(args.axes.split(",")) <= set(axes(fam)):
            continue
        if len(weights(fam)) < args.min_weights:
            continue
        out.append(fam)
    key = {"popularity": lambda f: f.get("popularity", 9999), "trending": lambda f: f.get("trending", 9999), "newest": lambda f: f.get("dateAdded", ""), "name": lambda f: f["family"]}[args.sort]
    out.sort(key=key, reverse=args.sort == "newest")
    return [describe(f, defaults, cutoff) for f in out[: args.limit]]


def css_url(specs: list[str]) -> str:
    """Build a Google Fonts css2 URL from 'Family:400,700' specs."""
    parts = []
    for spec in specs:
        family, _, ws = spec.partition(":")
        fam = "family=" + urllib.parse.quote_plus(family.strip())
        if ws:
            fam += ":wght@" + ";".join(sorted({w.strip() for w in ws.split(",")}, key=int))
        parts.append(fam)
    return "https://fonts.googleapis.com/css2?" + "&".join(parts) + "&display=swap"


def print_table(rows: list[dict]) -> None:
    if not rows:
        print("No matches. Relax a filter (category, --axes, --min-weights) or raise --limit.")
        return
    for r in rows:
        w = f"{r['weights'][0]}-{r['weights'][-1]}" if r["weights"] else "?"
        print(f"- {r['family']} | {r['category']} | rank {r['popularity_rank']} | weights {w} ({len(r['weights'])}) | axes {','.join(r['axes']) or '-'} | TR {'yes' if r['turkish'] else 'NO'}" + (f" | flags: {', '.join(r['flags'])}" if r["flags"] else ""))
        print(f"  {r['url']}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--metadata", help="Use a local copy of the Google Fonts metadata JSON")
    p.add_argument("--json", action="store_true", help="Print JSON instead of a list")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="List candidate families")
    s.add_argument("--category", help="serif, sans-serif, display, handwriting, monospace")
    s.add_argument("--classification", help="Google classification tag, e.g. Display")
    s.add_argument("--query", help="Substring of family or designer name")
    s.add_argument("--variable", action="store_true", help="Require a variable weight axis")
    s.add_argument("--axes", help="Require axes, comma separated (e.g. wdth,opsz)")
    s.add_argument("--min-weights", type=int, default=3, help="Minimum number of static weights (default 3)")
    s.add_argument("--skip-top", type=int, default=None, help="Exclude the N most popular families (default from ai_defaults.json)")
    s.add_argument("--allow-defaults", action="store_true", help="Do not exclude overused, AI-favorite, or top-N families")
    s.add_argument("--no-turkish", action="store_true", help="Do not require Turkish (latin-ext) support")
    s.add_argument("--include-noto", action="store_true", help="Include Noto families")
    s.add_argument("--include-other-scripts", action="store_true", help="Include families designed primarily for non-Latin scripts")
    s.add_argument("--sort", choices=["popularity", "trending", "newest", "name"], default="popularity")
    s.add_argument("--limit", type=int, default=20)

    c = sub.add_parser("check", help="Report facts and flags for named families")
    c.add_argument("families", nargs="+")

    u = sub.add_parser("css", help="Print a Google Fonts css2 URL for 'Family:400,700' specs")
    u.add_argument("specs", nargs="+")

    args = p.parse_args()
    if args.cmd == "css":
        print(css_url(args.specs))
        return 0

    defaults = load_defaults()
    fams = load_metadata(args.metadata)
    cutoff = defaults["popularity_cutoff"]

    if args.cmd == "search":
        if args.skip_top is None:
            args.skip_top = cutoff
        rows = search(args, fams, defaults)
    else:
        by_name = {f["family"].lower(): f for f in fams}
        rows = []
        for name in args.families:
            fam = by_name.get(name.lower())
            if fam:
                rows.append(describe(fam, defaults, cutoff))
            else:
                extra = [k for k in ("overused", "ai_favorites") if name in defaults["fonts"][k]]
                rows.append({"family": name, "on_google_fonts": False, "flags": extra,
                             "note": "Not on Google Fonts: verify license, Turkish glyphs (ğ ş ı İ), and hosting manually."})
    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    elif args.cmd == "search":
        print_table(rows)
    else:
        for r in rows:
            if r.get("on_google_fonts") is False:
                print(f"- {r['family']}: not on Google Fonts" + (f" | flags: {', '.join(r['flags'])}" if r["flags"] else "") + f"\n  {r['note']}")
            else:
                print_table([r])
    return 0


if __name__ == "__main__":
    sys.exit(main())
