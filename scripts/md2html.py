#!/usr/bin/env python3
"""Convert a Markdown note into a site entry page.

Usage:
    python3 scripts/md2html.py notes/2026-08-08.md

Options:
    -o, --output PATH   Where to write the HTML (default: entries/<same name>.html)
    --no-index          Skip regenerating index.html

The entry title is taken from the first level-1 heading (`# Title`), otherwise
from the file name. If the file name starts with YYYY-MM-DD, that date is used
for the entry header. After generating the page, index.html is updated
automatically unless --no-index is given.

The output keeps the input file name, so several notes on the same day can be
converted without overwriting each other:

    notes/2026-08-06-chunking.md   -> entries/2026-08-06-chunking.html
    notes/2026-08-06-graphrag.md   -> entries/2026-08-06-graphrag.html

After writing the page, the homepage index and the same-day navigation blocks
on all entry pages are refreshed automatically.

Supported Markdown: headings, paragraphs, fenced code blocks, blockquotes,
unordered/ordered lists (with nesting), horizontal rules, inline code, bold,
italic, links, and images. Everything else stays plain text.
"""

import argparse
import html
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
LIST_ITEM_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")


# ---------------------------------------------------------------------------
# Inline formatting
# ---------------------------------------------------------------------------

def render_inline(text):
    """Escape HTML, then apply inline Markdown (code, links, bold, italic)."""
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(
        r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)",
        r'<img src="\2" alt="\1">',
        text,
    )
    text = re.sub(
        r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)",
        r'<a href="\2">\1</a>',
        text,
    )
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    return text


# ---------------------------------------------------------------------------
# Block parsing
# ---------------------------------------------------------------------------

def is_list_item(line):
    return bool(LIST_ITEM_RE.match(line))


def starts_block(line):
    """True if the line opens a new block (heading, list, quote, fence, hr)."""
    return bool(
        re.match(r"^(#{1,6})\s+", line)
        or re.match(r"^\s*```", line)
        or re.match(r"^\s*>\s?", line)
        or re.match(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$", line)
        or is_list_item(line)
    )


def render_blocks(lines):
    blocks = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        # Fenced code block
        fence = re.match(r"^```(\S*)\s*$", line.strip())
        if fence:
            lang = fence.group(1)
            buf = []
            i += 1
            while i < n and not re.match(r"^```", lines[i].strip()):
                buf.append(lines[i])
                i += 1
            i += 1  # skip the closing fence (or run out of lines)
            code = html.escape("\n".join(buf))
            cls = f' class="language-{html.escape(lang)}"' if lang else ""
            blocks.append(f"<pre><code{cls}>{code}</code></pre>")
            continue

        # Heading
        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading:
            level = len(heading.group(1))
            blocks.append(f"<h{level}>{render_inline(heading.group(2))}</h{level}>")
            i += 1
            continue

        # Horizontal rule
        if re.match(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$", line):
            blocks.append("<hr>")
            i += 1
            continue

        # Blockquote
        if line.lstrip().startswith(">"):
            quote_lines = []
            while i < n and lines[i].lstrip().startswith(">"):
                quote_lines.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            blocks.append(f"<blockquote>\n{render_blocks(quote_lines)}\n</blockquote>")
            continue

        # List
        if is_list_item(line):
            list_lines = []
            while i < n and lines[i].strip() and (
                is_list_item(lines[i]) or lines[i].startswith(("  ", "\t"))
            ):
                list_lines.append(lines[i])
                i += 1
            blocks.append(render_list(list_lines))
            continue

        # Paragraph
        paragraph = [line]
        i += 1
        while i < n and lines[i].strip() and not starts_block(lines[i]):
            paragraph.append(lines[i])
            i += 1
        blocks.append(f"<p>{render_inline(' '.join(paragraph))}</p>")

    return "\n".join(blocks)


# ---------------------------------------------------------------------------
# Lists (supports simple nesting by indentation)
# ---------------------------------------------------------------------------

def parse_list_items(lines):
    """Turn list lines into a tree of {indent, ordered, text, children} nodes."""
    root = []
    stack = []  # (indent, node) of open items
    for raw in lines:
        m = LIST_ITEM_RE.match(raw)
        if not m:
            # Continuation text of the current item (e.g. an indented wrap line)
            if stack:
                stack[-1][1]["text"] += " " + render_inline(raw.strip())
            continue
        indent = len(m.group(1))
        ordered = m.group(2)[0].isdigit()
        node = {
            "indent": indent,
            "ordered": ordered,
            "text": render_inline(m.group(3).strip()),
            "children": [],
        }
        while stack and stack[-1][0] >= indent:
            stack.pop()
        if stack:
            stack[-1][1]["children"].append(node)
        else:
            root.append(node)
        stack.append((indent, node))
    return root


def render_list(lines):
    def render(nodes):
        out = []
        i = 0
        while i < len(nodes):
            ordered = nodes[i]["ordered"]
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>")
            while i < len(nodes) and nodes[i]["ordered"] == ordered:
                node = nodes[i]
                item = node["text"]
                if node["children"]:
                    item += "\n" + render(node["children"])
                out.append(f"<li>{item}</li>")
                i += 1
            out.append(f"</{tag}>")
        return "\n".join(out)

    return render(parse_list_items(lines))


# ---------------------------------------------------------------------------
# Page assembly
# ---------------------------------------------------------------------------

def extract_title(lines):
    for line in lines:
        m = re.match(r"^#\s+(.*)$", line)
        if m:
            return m.group(1).strip()
    return None


def build_page(title, date_str, body):
    title_esc = html.escape(title)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{date_str} · {title_esc}</title>
  <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
  <div class="container">
    <p class="breadcrumb"><a href="../index.html">← Back to index</a></p>

    <header class="entry-header">
      <h1>{title_esc}</h1>
      <p class="entry-date">{date_str}</p>
    </header>

    <main class="card">
{body}
    </main>

    <footer class="site-footer">
      <p><a href="../index.html">← Back to index</a></p>
    </footer>
  </div>
</body>
</html>
"""


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Convert a Markdown note into a site entry HTML page."
    )
    parser.add_argument("input", type=Path, help="Markdown file to convert")
    parser.add_argument(
        "-o", "--output", type=Path,
        help="Output HTML file (default: entries/<same name>.html)",
    )
    parser.add_argument(
        "--no-index", action="store_true",
        help="Do not regenerate index.html after writing the entry",
    )
    args = parser.parse_args(argv)

    if not args.input.is_file():
        sys.exit(f"error: no such file: {args.input}")

    lines = args.input.read_text(encoding="utf-8").splitlines()

    title = extract_title(lines)
    if title is not None:
        # Drop the first H1 line; it becomes the page title in the header
        found = False
        clean = []
        for line in lines:
            if not found and re.match(r"^#\s+", line):
                found = True
                continue
            clean.append(line)
        lines = clean
    else:
        title = args.input.stem

    date_match = DATE_RE.search(args.input.name)
    date_str = date_match.group(0) if date_match else date.today().isoformat()

    output = args.output or (ROOT / "entries" / f"{args.input.stem}.html")
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_page(title, date_str, render_blocks(lines)), encoding="utf-8")
    print(f"Wrote {output}")

    if not args.no_index:
        from update_index import main as update_index
        update_index()
        from add_same_day_nav import main as add_same_day_nav
        add_same_day_nav()


if __name__ == "__main__":
    main()
