"""Small, dependency-free color helpers shared by the fth-design-crafter scripts.

Covers CSS color parsing, WCAG 2 contrast, OKLab/OKLCH conversion, perceptual
distance, gamut mapping, and tonal ramps. Only the Python standard library is used.
"""

from __future__ import annotations

import math
import re

RGB = tuple[float, float, float]  # sRGB components in 0..1

_HEX_RE = re.compile(r"^#([0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
_FUNC_RE = re.compile(r"^(rgba?|hsla?|oklch)\(\s*([^)]*)\)$", re.I)

NAMED = {
    "white": "#ffffff",
    "black": "#000000",
}


# --------------------------------------------------------------------------- parsing


def _num(token: str, scale: float = 1.0) -> float:
    token = token.strip()
    if token.endswith("%"):
        return float(token[:-1]) / 100.0 * scale
    return float(token)


def parse_color(value: str) -> RGB | None:
    """Parse #hex, rgb()/rgba(), hsl()/hsla(), oklch(), white/black. Alpha is ignored."""
    v = value.strip().lower()
    v = NAMED.get(v, v)
    m = _HEX_RE.match(v)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h[:3])
        h = h[:6]
        return tuple(int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]
    m = _FUNC_RE.match(v)
    if not m:
        return None
    name, args = m.group(1), m.group(2)
    parts = [p for p in re.split(r"[\s,/]+", args) if p]
    try:
        if name.startswith("rgb") and len(parts) >= 3:
            vals = [_num(p, 255) / 255 if p.endswith("%") else float(p) / 255 for p in parts[:3]]
            return tuple(max(0.0, min(1.0, x)) for x in vals)  # type: ignore[return-value]
        if name.startswith("hsl") and len(parts) >= 3:
            h = float(parts[0].replace("deg", "")) % 360
            s = _num(parts[1]) if parts[1].endswith("%") else float(parts[1]) / 100
            l = _num(parts[2]) if parts[2].endswith("%") else float(parts[2]) / 100
            return hsl_to_rgb(h, s, l)
        if name == "oklch" and len(parts) >= 3:
            L = _num(parts[0]) if parts[0].endswith("%") else float(parts[0])
            C = float(parts[1].rstrip("%")) * (0.004 if parts[1].endswith("%") else 1)
            H = float(parts[2].replace("deg", ""))
            return clip_rgb(oklab_to_rgb(*oklch_to_oklab(L, C, H)))
    except ValueError:
        return None
    return None


def hsl_to_rgb(h: float, s: float, l: float) -> RGB:
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    r, g, b = [(c, x, 0), (x, c, 0), (0, c, x), (0, x, c), (x, 0, c), (c, 0, x)][int(h // 60) % 6]
    return (r + m, g + m, b + m)


def to_hex(rgb: RGB) -> str:
    return "#" + "".join(f"{round(max(0.0, min(1.0, c)) * 255):02x}" for c in rgb)


def normalize_hex(value: str) -> str | None:
    rgb = parse_color(value)
    return to_hex(rgb) if rgb else None


# --------------------------------------------------------------------------- WCAG


def _linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _gamma(c: float) -> float:
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def relative_luminance(rgb: RGB) -> float:
    r, g, b = (_linear(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg: str | RGB, bg: str | RGB) -> float:
    a = parse_color(fg) if isinstance(fg, str) else fg
    b = parse_color(bg) if isinstance(bg, str) else bg
    if a is None or b is None:
        raise ValueError(f"cannot parse colors: {fg!r}, {bg!r}")
    la, lb = relative_luminance(a), relative_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# --------------------------------------------------------------------------- OKLab / OKLCH


def rgb_to_oklab(rgb: RGB) -> tuple[float, float, float]:
    r, g, b = (_linear(c) for c in rgb)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(x) ** (1 / 3), x) for x in (l, m, s))
    return (
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    )


def oklab_to_rgb(L: float, a: float, b: float) -> RGB:
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return (_gamma(r) if r > 0 else r * 12.92, _gamma(g) if g > 0 else g * 12.92, _gamma(bb) if bb > 0 else bb * 12.92)


def oklab_to_oklch(L: float, a: float, b: float) -> tuple[float, float, float]:
    return (L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360)


def oklch_to_oklab(L: float, C: float, H: float) -> tuple[float, float, float]:
    return (L, C * math.cos(math.radians(H)), C * math.sin(math.radians(H)))


def to_oklch(color: str | RGB) -> tuple[float, float, float]:
    rgb = parse_color(color) if isinstance(color, str) else color
    if rgb is None:
        raise ValueError(f"cannot parse color: {color!r}")
    return oklab_to_oklch(*rgb_to_oklab(rgb))


def in_gamut(rgb: RGB, eps: float = 1e-4) -> bool:
    return all(-eps <= c <= 1 + eps for c in rgb)


def clip_rgb(rgb: RGB) -> RGB:
    return tuple(max(0.0, min(1.0, c)) for c in rgb)  # type: ignore[return-value]


def oklch_to_hex(L: float, C: float, H: float) -> str:
    """Convert OKLCH to hex, reducing chroma until the color fits in sRGB."""
    L = max(0.0, min(1.0, L))
    lo, hi = 0.0, C
    rgb = oklab_to_rgb(*oklch_to_oklab(L, C, H))
    if in_gamut(rgb):
        return to_hex(rgb)
    for _ in range(24):
        mid = (lo + hi) / 2
        if in_gamut(oklab_to_rgb(*oklch_to_oklab(L, mid, H))):
            lo = mid
        else:
            hi = mid
    return to_hex(clip_rgb(oklab_to_rgb(*oklch_to_oklab(L, lo, H))))


def delta_e(c1: str | RGB, c2: str | RGB) -> float:
    """Euclidean distance in OKLab (0 = identical; about 0.02 is barely noticeable)."""
    a = parse_color(c1) if isinstance(c1, str) else c1
    b = parse_color(c2) if isinstance(c2, str) else c2
    if a is None or b is None:
        raise ValueError(f"cannot parse colors: {c1!r}, {c2!r}")
    return math.dist(rgb_to_oklab(a), rgb_to_oklab(b))


def similar(candidate: str, reference: str, threshold: float) -> bool:
    """True when two colors read as the same choice, not just two near-whites or near-blacks.

    Besides a small OKLab distance, the candidate must carry a comparable amount of
    chroma and, for chromatic references, point to a similar hue.
    """
    if delta_e(candidate, reference) >= threshold:
        return False
    _, c1, h1 = to_oklch(candidate)
    _, c2, h2 = to_oklch(reference)
    if c2 < 0.004:  # achromatic reference: plain white/black are not signatures
        return c1 < 0.004 and delta_e(candidate, reference) < threshold / 3
    if c1 < c2 * 0.5:
        return False
    return min(abs(h1 - h2), 360 - abs(h1 - h2)) <= 30


# --------------------------------------------------------------------------- derived colors

RAMP_STEPS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]
_RAMP_L = {50: 0.975, 100: 0.945, 200: 0.89, 300: 0.81, 400: 0.71, 500: 0.62, 600: 0.54, 700: 0.46, 800: 0.38, 900: 0.30, 950: 0.22}


def ramp(seed: str) -> dict[int, str]:
    """Tonal ramp around a seed color: fixed OKLCH lightness steps, the seed's hue, tapered chroma."""
    L0, C0, H = to_oklch(seed)
    out = {}
    for step in RAMP_STEPS:
        L = _RAMP_L[step]
        taper = 1 - min(1.0, abs(L - 0.6) / 0.45) * 0.8
        out[step] = oklch_to_hex(L, C0 * taper, H)
    return out


def shift_lightness(color: str, delta: float) -> str:
    L, C, H = to_oklch(color)
    return oklch_to_hex(L + delta, C, H)


def mix(c1: str, c2: str, t: float) -> str:
    """Mix in OKLab: t=0 -> c1, t=1 -> c2."""
    a = rgb_to_oklab(parse_color(c1))  # type: ignore[arg-type]
    b = rgb_to_oklab(parse_color(c2))  # type: ignore[arg-type]
    return to_hex(clip_rgb(oklab_to_rgb(*(x + (y - x) * t for x, y in zip(a, b)))))


def hue_bin(color: str, bins: int = 12) -> int | None:
    """Hue bucket index (0..bins-1), or None for near-neutral colors."""
    L, C, H = to_oklch(color)
    if C < 0.03:
        return None
    return int(((H + 360 / bins / 2) % 360) // (360 / bins))


HUE_NAMES = ["pink", "red", "orange", "yellow", "lime", "green", "teal", "cyan", "sky", "blue", "violet", "magenta"]


def _cli() -> int:
    import argparse
    import json

    p = argparse.ArgumentParser(description="Color helpers: tonal ramps, contrast, OKLCH, distance.")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("ramp", help="Tonal ramp (50-950) around a seed color")
    r.add_argument("color")
    c = sub.add_parser("contrast", help="WCAG contrast ratio of two colors")
    c.add_argument("fg")
    c.add_argument("bg")
    o = sub.add_parser("oklch", help="OKLCH coordinates of colors")
    o.add_argument("colors", nargs="+")
    d = sub.add_parser("distance", help="OKLab distance of two colors")
    d.add_argument("a")
    d.add_argument("b")
    args = p.parse_args()
    if args.cmd == "ramp":
        print(json.dumps(ramp(args.color), indent=2))
    elif args.cmd == "contrast":
        ratio = contrast_ratio(args.fg, args.bg)
        verdict = "AAA text" if ratio >= 7 else "AA text" if ratio >= 4.5 else "large text / UI only" if ratio >= 3 else "fails"
        print(f"{ratio:.2f}:1 ({verdict})")
    elif args.cmd == "oklch":
        for col in args.colors:
            L, C, H = to_oklch(col)
            print(f"{col}: oklch({L:.3f} {C:.3f} {H:.1f})")
    else:
        print(f"{delta_e(args.a, args.b):.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
