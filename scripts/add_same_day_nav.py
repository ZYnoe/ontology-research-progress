#!/usr/bin/env python3
"""Add a same-day navigation block to every entry page.

Entries sharing a date get links to each other (e.g. 2026-08-06.html and
2026-08-06-graphrag.html), so visitors can jump between same-day pages
without going back to the index. The block is inserted right after the
breadcrumb and is idempotent: existing blocks are replaced.

Usage:
    python3 scripts/add_same_day_nav.py

This runs automatically after `md2html.py` converts a note; run it manually
after editing an entry HTML page by hand.
"""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = ROOT / "entries"

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)
DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
TITLE_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\s*[·\-—:]\s*")
BREADCRUMB_RE = re.compile(r'(<p class="breadcrumb">.*?</p>)', re.DOTALL)
NAV_BLOCK_RE = re.compile(
    r"<!-- same-day-nav-start -->.*?<!-- same-day-nav-end -->\n*",
    re.DOTALL,
)

NAV_START = "<!-- same-day-nav-start -->"
NAV_END = "<!-- same-day-nav-end -->"


def parse_entry(path):
    text = path.read_text(encoding="utf-8")
    match = TITLE_RE.search(text)
    title = match.group(1).strip() if match else path.stem
    title = TITLE_PREFIX_RE.sub("", title).strip()
    date_match = DATE_RE.search(path.name)
    if not date_match:
        return None
    return {
        "path": path,
        "date": date_match.group(0),
        "title": title or path.stem,
        "url": path.name,
    }


def build_nav(date, siblings):
    if not siblings:
        return ""
    links = " · ".join(
        f'<a href="{html.escape(s["url"], quote=True)}">'
        f"{html.escape(s['title'])}</a>"
        for s in siblings
    )
    return (
        f"{NAV_START}\n"
        '<nav class="same-day-nav">\n'
        f'<span class="same-day-label">Other entries on {date}:</span> {links}\n'
        "</nav>\n"
        f"{NAV_END}"
    )


def inject_nav(text, nav):
    """Insert or replace the nav block after the breadcrumb."""
    if nav == "":
        return NAV_BLOCK_RE.sub("", text)
    if NAV_BLOCK_RE.search(text):
        return NAV_BLOCK_RE.sub(lambda _: nav + "\n", text)
    match = BREADCRUMB_RE.search(text)
    if not match:
        return text
    rest = text[match.end() :].lstrip("\n")
    return text[: match.end()] + "\n" + nav + "\n" + rest


def main():
    entries = []
    for path in sorted(ENTRIES_DIR.glob("*.html")):
        entry = parse_entry(path)
        if entry:
            entries.append(entry)

    by_date = {}
    for entry in entries:
        by_date.setdefault(entry["date"], []).append(entry)

    changed = 0
    for entry in entries:
        siblings = [s for s in by_date[entry["date"]] if s["url"] != entry["url"]]
        nav = build_nav(entry["date"], siblings)
        text = entry["path"].read_text(encoding="utf-8")
        new_text = inject_nav(text, nav)
        if new_text != text:
            entry["path"].write_text(new_text, encoding="utf-8")
            changed += 1
    print(f"Updated same-day navigation in {changed} entries.")


if __name__ == "__main__":
    main()
