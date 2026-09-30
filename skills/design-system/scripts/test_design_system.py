"""Offline tests for the design-system scripts (standard library only).

Run: python -m unittest test_design_system -v   (from this scripts/ folder)
"""

from __future__ import annotations

import copy
import http.server
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import build_specimen as bs  # noqa: E402
import colorlib as cl  # noqa: E402
import find_fonts as ff  # noqa: E402
import scan_site as ss  # noqa: E402

TEMPLATE = HERE.parent / "templates" / "directions.template.json"


def fake_metadata() -> dict:
    fam = lambda name, pop, subsets=("latin", "latin-ext"), cat="Sans Serif", **kw: {  # noqa: E731
        "family": name, "category": cat, "popularity": pop, "subsets": list(subsets), "classifications": [],
        "fonts": {"400": {}, "600": {}, "700": {}}, "axes": [{"tag": "wght", "min": 100, "max": 900}],
        "isOpenSource": True, "isNoto": False, "isBrandFont": kw.get("brand", False), "primaryScript": kw.get("script", ""),
        "designers": ["X"], "dateAdded": "2020-01-01", "trending": 1,
    }
    return {"familyMetadataList": [
        fam("Inter", 5), fam("Space Grotesk", 59), fam("Quiet Grotesk", 300), fam("Latin Only Sans", 400, subsets=("latin",)),
        fam("Brand Flex", 80, brand=True), fam("Telugu Sans", 150, script="Telu"), fam("Paper Serif", 250, cat="Serif"),
    ]}


class ColorTests(unittest.TestCase):
    def test_contrast_known_values(self):
        self.assertAlmostEqual(cl.contrast_ratio("#000", "#fff"), 21.0, places=2)
        self.assertAlmostEqual(cl.contrast_ratio("#767676", "#ffffff"), 4.54, places=2)

    def test_parse_formats(self):
        self.assertEqual(cl.normalize_hex("rgb(255 0 0 / 50%)"), "#ff0000")
        self.assertEqual(cl.normalize_hex("hsl(210, 50%, 40%)"), "#336699")
        self.assertIsNotNone(cl.normalize_hex("oklch(62% 0.15 250)"))
        self.assertIsNone(cl.parse_color("linear-gradient(red, blue)"))

    def test_oklch_round_trip(self):
        for hx in ("#1f5d4c", "#a3321c", "#27406b", "#f5f6f3"):
            self.assertLess(cl.delta_e(hx, cl.oklch_to_hex(*cl.to_oklch(hx))), 0.005)

    def test_similar_ignores_plain_neutrals_but_catches_cream(self):
        self.assertTrue(cl.similar("#f8f6f1", "#F4F1EA", 0.035))
        self.assertFalse(cl.similar("#f2f3f5", "#F4F1EA", 0.035))
        self.assertTrue(cl.similar("#6b6ef2", "#6366F1", 0.035))

    def test_ramp_is_monotonic(self):
        values = [cl.to_oklch(h)[0] for h in cl.ramp("#1f5d4c").values()]
        self.assertEqual(values, sorted(values, reverse=True))


class FontTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump(fake_metadata(), self.tmp)
        self.tmp.close()

    def run_ff(self, *args):
        return subprocess.run([sys.executable, str(HERE / "find_fonts.py"), "--metadata", self.tmp.name, *args], capture_output=True, text=True)

    def test_search_excludes_defaults_brand_script_and_non_turkish(self):
        out = self.run_ff("--json", "search").stdout
        names = [r["family"] for r in json.loads(out)]
        self.assertEqual(sorted(names), ["Paper Serif", "Quiet Grotesk"])

    def test_check_flags(self):
        rows = json.loads(self.run_ff("--json", "check", "Inter", "Latin Only Sans", "Satoshi").stdout)
        self.assertIn("overused", rows[0]["flags"])
        self.assertIn("no-turkish", rows[1]["flags"])
        self.assertFalse(rows[2]["on_google_fonts"])

    def test_css_url(self):
        self.assertEqual(ff.css_url(["Paper Serif:600,400"]), "https://fonts.googleapis.com/css2?family=Paper+Serif:wght@400;600&display=swap")


class SpecimenTests(unittest.TestCase):
    def setUp(self):
        self.spec = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        self.defaults = bs.load_defaults()

    def test_template_directions_pass(self):
        for d in self.spec["directions"]:
            issues = bs.check_direction(d, self.defaults, None, None)
            self.assertFalse([i for i in issues if i["level"] in ("FAIL", "WARN")], (d["id"], issues))

    def test_gradient_is_rejected(self):
        d = copy.deepcopy(self.spec["directions"][0])
        d["colors"]["light"]["primary"] = "linear-gradient(90deg, #111, #222)"
        msgs = [i["message"] for i in bs.check_direction(d, self.defaults, None, None) if i["level"] == "FAIL"]
        self.assertTrue(any("flat color" in m for m in msgs))

    def test_low_contrast_fails(self):
        d = copy.deepcopy(self.spec["directions"][0])
        d["colors"]["light"]["text-muted"] = "#c8ccc6"
        msgs = [i["message"] for i in bs.check_direction(d, self.defaults, None, None) if i["level"] == "FAIL"]
        self.assertTrue(any("text-muted on bg" in m for m in msgs))

    def test_template_defaults_and_fonts_warn(self):
        d = copy.deepcopy(self.spec["directions"][0])
        d["colors"]["light"]["primary"] = "#6366f1"
        d["fonts"]["heading"]["family"] = "Space Grotesk"
        warns = [i["message"] for i in bs.check_direction(d, self.defaults, None, None) if i["level"] == "WARN"]
        self.assertTrue(any("template default" in m for m in warns))
        self.assertTrue(any("AI/template pick" in m for m in warns))

    def test_turkish_missing_fails_with_metadata(self):
        d = copy.deepcopy(self.spec["directions"][0])
        d["fonts"]["body"]["family"] = "Latin Only Sans"
        meta = {f["family"].lower(): f for f in fake_metadata()["familyMetadataList"]}
        msgs = [i["message"] for i in bs.check_direction(d, self.defaults, meta, None) if i["level"] == "FAIL"]
        self.assertTrue(any("latin-ext" in m for m in msgs))

    def test_similar_directions_warn(self):
        dirs = copy.deepcopy(self.spec["directions"][:2])
        dirs[1]["colors"]["light"]["primary"] = dirs[0]["colors"]["light"]["primary"]
        self.assertTrue(bs.compare_directions(dirs))

    def test_border_strong_meets_three_to_one(self):
        c = bs.complete_theme(self.spec["directions"][0]["colors"]["light"], False)
        self.assertGreaterEqual(cl.contrast_ratio(c["border-strong"], c["bg"]), 3)

    def test_render_and_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "specimen.html"
            r = subprocess.run([sys.executable, str(HERE / "build_specimen.py"), str(TEMPLATE), "--out", str(out)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            page = out.read_text(encoding="utf-8")
            self.assertNotIn("gradient(", page)
            self.assertIn('data-dir="c"', page)
            r = subprocess.run([sys.executable, str(HERE / "build_specimen.py"), str(TEMPLATE), "--export", "b", "--out-dir", tmp], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            for name in ("DESIGN.md", "tokens.css", "tailwind.theme.json", "design-tokens.json"):
                self.assertTrue((Path(tmp) / name).exists(), name)
            css = (Path(tmp) / "tokens.css").read_text(encoding="utf-8")
            self.assertIn("--primary: #a3321c;", css)
            self.assertIn('[data-theme="dark"]', css)
            self.assertNotIn("gradient(", css)


class ScanTests(unittest.TestCase):
    PAGE = """<html><head><link rel="stylesheet" href="/s.css"><link rel="preconnect" href="https://fonts.googleapis.com">
<style>:root{--brand:#1e64ff}body{color:#111;background:#fff;font-family:'Quiet Grotesk', system-ui, sans-serif}</style></head>
<body><div style="background: linear-gradient(90deg,#f00,#00f)">x</div></body></html>"""
    CSS = ".btn{background:#1e64ff;color:#fff}.alert{border-color:#1e64ff}h1{font-family:'Inter Fallback', 'Paper Serif', serif}"

    @classmethod
    def setUpClass(cls):
        page, css = cls.PAGE.encode(), cls.CSS.encode()

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):  # noqa: N802
                body, ctype = (css, "text/css") if self.path == "/s.css" else (page, "text/html")
                self.send_response(200)
                self.send_header("Content-Type", ctype + "; charset=utf-8")
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *a):
                pass

        cls.server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.url = f"http://127.0.0.1:{cls.server.server_port}/"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def test_scan_extracts_colors_fonts_and_gradients(self):
        r = ss.scan(self.url, 3)
        self.assertEqual(r["errors"], [])
        self.assertEqual(r["stats"]["gradients"], 1)
        self.assertEqual(r["stats"]["stylesheets_read"], 1)
        self.assertEqual(r["palette"]["accents"][0]["hex"], "#1e64ff")
        fonts = [f["family"] for f in r["fonts"]]
        self.assertIn("Quiet Grotesk", fonts)
        self.assertIn("Paper Serif", fonts)
        self.assertNotIn("Inter Fallback", fonts)

    def test_landscape(self):
        r = ss.scan(self.url, 3)
        land = ss.landscape([r, copy.deepcopy(r) | {"url": "http://other.test/"}])
        self.assertIn("blue", land["occupied_accent_hues"])
        self.assertIn("green", land["free_accent_hues"])


if __name__ == "__main__":
    unittest.main()
