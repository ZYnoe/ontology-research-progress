---
name: research-log
description: Maintain the ontology research progress site in this repository — add or update daily research entries, convert Markdown notes into HTML entry pages, regenerate the homepage index, and publish to GitHub Pages. Use when the user asks to write today's research note, add or update a log entry, convert a .md note to HTML, fix the entry list, or commit and push site changes.
---

# Research Log

This repository is a static research journal published at
https://zynoe.github.io/ontology-research-progress/ (GitHub Pages, repo
`ZYnoe/ontology-research-progress`, branch `main`). There is no build step:
entries are plain HTML files in `entries/`, `index.html` lists them, and
`assets/` holds shared CSS/JS.

## Standard workflow: add a note

1. Write the note as Markdown in `notes/`, named `YYYY-MM-DD[-slug].md`.
   Start from `templates/note-template.md` if the user does not provide
   content structure.
   - The first `# Heading` becomes the entry title and is removed from the
     body.
   - The date comes from the file name (fallback: today's date).
   - Several notes can share a date — give each a unique slug, e.g.
     `2026-08-06-chunking.md` and `2026-08-06-graphrag.md`.
2. Convert it:

   ```bash
   python3 scripts/md2html.py notes/2026-08-06.md
   ```

   This writes `entries/<same name>.html` and regenerates `index.html`. Use
   `-o PATH` to override the output and `--no-index` to skip the index
   update. It also refreshes the same-day navigation block on every entry
   page (links between entries that share a date).
3. Inspect the generated page and the index before committing.
4. Commit and push to GitHub (`main`) so Pages updates.

## Editing entries by hand

- Copy `templates/entry-template.html`. Keep `<title>` as
  `YYYY-MM-DD · Title` (the index strips this prefix) and keep the
  breadcrumb/footer links (`../index.html`, `../assets/style.css`).
- Regenerate the index after any change: `python3 scripts/update_index.py`.
- Refresh same-day navigation links after hand edits:
  `python3 scripts/add_same_day_nav.py` (idempotent; also run automatically
  by `md2html.py`).
- The "Jump to a date" widget filters the homepage entry list by date in place
  (it no longer navigates). Entries carry a `data-date` attribute emitted by
  `update_index.py`, so always regenerate `index.html` with that script after
  adding or removing entries.

## Supported Markdown

Headings, paragraphs, fenced code blocks, blockquotes, ordered and unordered
lists with nesting, horizontal rules, inline code, bold, italic, links, and
images. Unsupported syntax (e.g. tables, task lists) renders as plain text.

## Pitfalls

- Converting two notes with the same file name overwrites the first output.
  Use distinct date-slug names for same-day notes.
- `demo.md` is a demo, not an entry; convert it only with `-o /tmp/...` so it
  does not overwrite a dated entry.
- `entries/2026-08-07.html` is intentionally untracked (removed from the repo
  earlier). Do not add it unless the user asks. The local index may list it,
  creating a dead link on the live site — flag this instead of silently
  changing it.
- Git writes (`git add`/`commit`/`push`) fail inside the sandbox because
  `.git` is read-only there; re-run them with escalated permissions.
- When the task involves research content (pipeline, models, open questions),
  read `references/research-context.md` before answering.

## Research context

For the current state of the research itself — PDF extraction, chunking,
embedding, RAG/GraphRAG plans, and the 표준어휘 2025-2 classification plan —
see [references/research-context.md](references/research-context.md).
