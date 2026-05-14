#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class DeckParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.in_title = False
        self.slide_count = 0
        self.script_srcs: list[str] = []
        self.link_hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        if tag == "title":
            self.in_title = True
        if "slide" in attr.get("class", "").split():
            self.slide_count += 1
        if tag == "script" and attr.get("src"):
            self.script_srcs.append(attr["src"])
        if tag == "link" and attr.get("href"):
            self.link_hrefs.append(attr["href"])

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data.strip()


def fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 1


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        return fail("usage: validate_deck.py path/to/index.html")

    path = Path(argv[1])
    if not path.exists():
        return fail(f"file not found: {path}")
    text = path.read_text(encoding="utf-8")

    if "<!doctype html" not in text.lower():
        return fail("missing <!doctype html>")
    if re.search(r"(localhost|127\.0\.0\.1|file://|/home/|/Users/)", text):
        return fail("contains local-only URL or path")
    if len(text.encode("utf-8")) > 1_500_000:
        return fail("deck is larger than 1.5 MB; split assets or simplify")

    parser = DeckParser()
    parser.feed(text)

    if not parser.title:
        return fail("missing <title>")
    if parser.slide_count < 3:
        return fail("expected at least 3 elements with class 'slide'")
    if parser.script_srcs:
        return fail(f"external script dependencies are not allowed: {parser.script_srcs}")

    remote_links = [
        href
        for href in parser.link_hrefs
        if href.startswith("http://") or href.startswith("https://")
    ]
    if remote_links:
        return fail(f"remote stylesheet/icon links are not allowed: {remote_links}")

    print(f"ok: {path} ({parser.slide_count} slides, title: {parser.title})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
