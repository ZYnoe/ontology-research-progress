#!/usr/bin/env python3
"""Regenerate the entry list in index.html from the HTML files in entries/.

Usage:
    python3 scripts/update_index.py

Conventions:
    - Each entry lives at entries/YYYY-MM-DD[-slug].html; the date is taken
      from the filename, so several entries may share a date
    - Write each entry's <title> as "YYYY-MM-DD · Title" (the script strips the
      date prefix automatically)
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = ROOT / "entries"
INDEX_FILE = ROOT / "index.html"

START_MARKER = "<!-- entries-start -->"
END_MARKER = "<!-- entries-end -->"

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)
DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
TITLE_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\s*[·\-—:]\s*")
MONTH_NAMES = [
    "",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def parse_entry(path):
    text = path.read_text(encoding="utf-8")
    match = TITLE_RE.search(text)
    title = match.group(1).strip() if match else ""
    title = TITLE_PREFIX_RE.sub("", title).strip()
    date_match = DATE_RE.search(path.name)
    if not date_match:
        return None
    year, month, day = (int(g) for g in date_match.groups())
    return {
        "date": f"{year:04d}-{month:02d}-{day:02d}",
        "year": year,
        "month": month,
        "title": title or path.stem,
        "url": f"entries/{path.name}",
    }


def build_html(entries):
    count = len(entries)
    label = "entry" if count == 1 else "entries"
    out = [f'<p class="entry-count" id="entry-count">{count} {label} total</p>']
    if not entries:
        out.append(
            '<p class="empty">No entries yet. Add your first one and run '
            "<code>python3 scripts/update_index.py</code>.</p>"
        )
        return out

    current_year = None
    current_month = None
    ul_open = False
    for entry in entries:
        if entry["year"] != current_year:
            if ul_open:
                out.append("</ul>")
                ul_open = False
            current_year = entry["year"]
            current_month = None
            out.append(f"<h3>{current_year}</h3>")
        if entry["month"] != current_month:
            if ul_open:
                out.append("</ul>")
                ul_open = False
            current_month = entry["month"]
            out.append(f"<h4>{MONTH_NAMES[current_month]}</h4>")
        if not ul_open:
            out.append("<ul>")
            ul_open = True
        out.append(
            f'<li data-date="{entry["date"]}"><a href="{entry["url"]}">'
            f'{entry["date"]} · {entry["title"]}</a></li>'
        )
    if ul_open:
        out.append("</ul>")
    return out


def entry_sort_key(entry):
    """Newest date first; within a date, the plain YYYY-MM-DD.html entry
    comes first, then additional pages alphabetically by file name."""
    date_key = tuple(-int(part) for part in entry["date"].split("-"))
    is_base = entry["url"].endswith(f"{entry['date']}.html")
    return (date_key, 0 if is_base else 1, entry["url"])


def main():
    ENTRIES_DIR.mkdir(exist_ok=True)
    entries = []
    for path in ENTRIES_DIR.glob("*.html"):
        entry = parse_entry(path)
        if entry:
            entries.append(entry)
    entries.sort(key=entry_sort_key)

    index_text = INDEX_FILE.read_text(encoding="utf-8")
    if START_MARKER not in index_text or END_MARKER not in index_text:
        raise SystemExit(
            "Could not find the entry markers (<!-- entries-start --> / "
            "<!-- entries-end -->) in index.html"
        )

    head, _, tail = index_text.partition(START_MARKER)
    _, _, tail = tail.partition(END_MARKER)
    new_text = (
        head
        + START_MARKER
        + "\n"
        + "\n".join(build_html(entries))
        + "\n"
        + END_MARKER
        + tail
    )
    INDEX_FILE.write_text(new_text, encoding="utf-8")
    print(f"Updated {INDEX_FILE.name} with {len(entries)} entries.")


if __name__ == "__main__":
    main()
