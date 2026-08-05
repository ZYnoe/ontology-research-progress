#!/usr/bin/env python3
"""根据 entries/ 目录下的 HTML 记录，重新生成 index.html 中的记录列表。

用法:
    python3 scripts/update_index.py

约定:
    - 每篇记录位于 entries/YYYY-MM-DD.html，文件名中的日期即记录日期
    - 建议记录 <title> 写成 "YYYY-MM-DD · 标题"（脚本会自动去掉日期前缀）
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
    out = [f'<p class="entry-count">共 {len(entries)} 篇记录</p>']
    if not entries:
        out.append(
            '<p class="empty">还没有记录。添加第一篇后运行 '
            "<code>python3 scripts/update_index.py</code>。</p>"
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
            out.append(f"<h3>{current_year} 年</h3>")
        if entry["month"] != current_month:
            if ul_open:
                out.append("</ul>")
                ul_open = False
            current_month = entry["month"]
            out.append(f"<h4>{current_month} 月</h4>")
        if not ul_open:
            out.append("<ul>")
            ul_open = True
        out.append(
            f'<li><a href="{entry["url"]}">'
            f'{entry["date"]} · {entry["title"]}</a></li>'
        )
    if ul_open:
        out.append("</ul>")
    return out


def main():
    ENTRIES_DIR.mkdir(exist_ok=True)
    entries = []
    for path in ENTRIES_DIR.glob("*.html"):
        entry = parse_entry(path)
        if entry:
            entries.append(entry)
    entries.sort(key=lambda e: e["date"], reverse=True)

    index_text = INDEX_FILE.read_text(encoding="utf-8")
    if START_MARKER not in index_text or END_MARKER not in index_text:
        raise SystemExit(
            "index.html 中找不到条目标记（<!-- entries-start --> / "
            "<!-- entries-end -->）"
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
    print(f"已更新 {INDEX_FILE.name}，共 {len(entries)} 篇记录。")


if __name__ == "__main__":
    main()
