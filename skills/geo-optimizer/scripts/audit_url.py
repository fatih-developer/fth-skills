#!/usr/bin/env python3
"""Run basic, dependency-free discovery and HTML checks for a public URL."""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen


USER_AGENT = "ai-geo-optimizer-audit/1.0"
TIMEOUT = 15


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title_parts: list[str] = []
        self.in_title = False
        self.h1_count = 0
        self.html_lang = ""
        self.meta: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.json_ld: list[str] = []
        self.in_json_ld = False
        self.json_ld_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        tag = tag.lower()
        if tag == "html":
            self.html_lang = values.get("lang", "")
        elif tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "meta":
            self.meta.append(values)
        elif tag == "link":
            self.links.append(values)
        elif tag == "script" and values.get("type", "").lower() == "application/ld+json":
            self.in_json_ld = True
            self.json_ld_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        elif tag == "script" and self.in_json_ld:
            self.in_json_ld = False
            self.json_ld.append("".join(self.json_ld_parts).strip())

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self.in_json_ld:
            self.json_ld_parts.append(data)


def fetch(url: str) -> dict[str, object]:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,*/*;q=0.8"})
    try:
        with urlopen(request, timeout=TIMEOUT) as response:
            body = response.read().decode(response.headers.get_content_charset() or "utf-8", "replace")
            return {
                "requested_url": url,
                "final_url": response.geturl(),
                "status": response.status,
                "content_type": response.headers.get("Content-Type", ""),
                "x_robots_tag": response.headers.get("X-Robots-Tag", ""),
                "body": body,
                "error": "",
            }
    except HTTPError as exc:
        return {"requested_url": url, "final_url": exc.geturl(), "status": exc.code, "body": "", "error": str(exc)}
    except (URLError, TimeoutError, ValueError) as exc:
        return {"requested_url": url, "final_url": url, "status": 0, "body": "", "error": str(exc)}


def meta_value(items: list[dict[str, str]], *names: str) -> str:
    wanted = {name.lower() for name in names}
    for item in items:
        key = (item.get("name") or item.get("property") or "").lower()
        if key in wanted:
            return item.get("content", "").strip()
    return ""


def canonical_value(items: list[dict[str, str]], base_url: str) -> str:
    for item in items:
        rel_tokens = set(re.split(r"\s+", item.get("rel", "").lower().strip()))
        if "canonical" in rel_tokens and item.get("href"):
            return urljoin(base_url, item["href"])
    return ""


def parse_json_ld(blocks: list[str]) -> tuple[int, list[str]]:
    valid = 0
    errors: list[str] = []
    for index, block in enumerate(blocks, start=1):
        if not block:
            errors.append(f"Block {index} is empty")
            continue
        try:
            json.loads(block)
            valid += 1
        except json.JSONDecodeError as exc:
            errors.append(f"Block {index}: {exc.msg} at line {exc.lineno}, column {exc.colno}")
    return valid, errors


def analyze(url: str) -> dict[str, object]:
    page = fetch(url)
    final_url = str(page["final_url"])
    parser = PageParser()
    body = str(page.get("body", ""))
    if body:
        parser.feed(body)

    title = re.sub(r"\s+", " ", "".join(parser.title_parts)).strip()
    valid_json_ld, json_ld_errors = parse_json_ld(parser.json_ld)
    split = urlsplit(final_url)
    origin = f"{split.scheme}://{split.netloc}"
    robots_url = urljoin(origin, "/robots.txt")
    robots = fetch(robots_url)
    robots_body = str(robots.get("body", ""))
    sitemap_matches = re.findall(r"(?im)^\s*Sitemap\s*:\s*(\S+)\s*$", robots_body)
    sitemap_url = sitemap_matches[0] if sitemap_matches else urljoin(origin, "/sitemap.xml")
    sitemap = fetch(sitemap_url)

    issues: list[dict[str, str]] = []
    if int(page["status"]) != 200:
        issues.append({"priority": "High", "message": f"Page returned HTTP {page['status']}"})
    if not title:
        issues.append({"priority": "High", "message": "Missing HTML title"})
    if not meta_value(parser.meta, "description"):
        issues.append({"priority": "Medium", "message": "Missing meta description"})
    if not canonical_value(parser.links, final_url):
        issues.append({"priority": "Medium", "message": "Missing canonical link"})
    if not parser.html_lang:
        issues.append({"priority": "Medium", "message": "Missing html lang attribute"})
    if parser.h1_count == 0:
        issues.append({"priority": "Medium", "message": "No h1 found in response HTML"})
    robots_meta = meta_value(parser.meta, "robots", "googlebot", "bingbot")
    if "noindex" in robots_meta.lower() or "noindex" in str(page.get("x_robots_tag", "")).lower():
        issues.append({"priority": "Critical", "message": "Page exposes a noindex directive"})
    if json_ld_errors:
        issues.append({"priority": "High", "message": "One or more JSON-LD blocks are invalid"})
    if int(robots["status"]) != 200:
        issues.append({"priority": "High", "message": f"robots.txt returned HTTP {robots['status']}"})
    if int(sitemap["status"]) != 200:
        issues.append({"priority": "High", "message": f"Sitemap returned HTTP {sitemap['status']}"})

    return {
        "page": {
            "requested_url": page["requested_url"],
            "final_url": final_url,
            "status": page["status"],
            "content_type": page.get("content_type", ""),
            "title": title,
            "description": meta_value(parser.meta, "description"),
            "canonical": canonical_value(parser.links, final_url),
            "lang": parser.html_lang,
            "h1_count": parser.h1_count,
            "robots_meta": robots_meta,
            "x_robots_tag": page.get("x_robots_tag", ""),
            "json_ld_blocks": len(parser.json_ld),
            "valid_json_ld_blocks": valid_json_ld,
            "json_ld_errors": json_ld_errors,
            "error": page.get("error", ""),
        },
        "discovery": {
            "robots_url": robots_url,
            "robots_status": robots["status"],
            "declared_sitemaps": sitemap_matches,
            "checked_sitemap_url": sitemap_url,
            "sitemap_status": sitemap["status"],
        },
        "issues": issues,
        "limitations": [
            "Checks response HTML only; it does not execute JavaScript.",
            "It does not validate platform-specific crawler policy or semantic schema accuracy.",
            "A successful fetch does not guarantee indexing, ranking, recommendation, or citation.",
        ],
    }


def print_text(result: dict[str, object]) -> None:
    page = result["page"]
    discovery = result["discovery"]
    assert isinstance(page, dict) and isinstance(discovery, dict)
    print(f"Page: {page['final_url']} (HTTP {page['status']})")
    print(f"Title: {page['title'] or '[missing]'}")
    print(f"Description: {page['description'] or '[missing]'}")
    print(f"Canonical: {page['canonical'] or '[missing]'}")
    print(f"Language: {page['lang'] or '[missing]'}; H1 count: {page['h1_count']}")
    print(f"JSON-LD: {page['valid_json_ld_blocks']}/{page['json_ld_blocks']} valid")
    print(f"robots.txt: HTTP {discovery['robots_status']} ({discovery['robots_url']})")
    print(f"sitemap: HTTP {discovery['sitemap_status']} ({discovery['checked_sitemap_url']})")
    issues = result["issues"]
    assert isinstance(issues, list)
    if issues:
        print("Issues:")
        for issue in issues:
            print(f"- [{issue['priority']}] {issue['message']}")
    else:
        print("Issues: none detected by basic checks")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Public, preview, or local HTTP(S) URL")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()
    if not args.url.startswith(("http://", "https://")):
        parser.error("url must start with http:// or https://")
    result = analyze(args.url)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
