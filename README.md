# Ontology Research Progress

Track research progress in HTML and publish it via GitHub Pages, so it is
accessible from any device.

## Directory structure

```
index.html                     # Homepage: jump to a date + list of all entries
entries/YYYY-MM-DD[-slug].html # Research logs; several pages may share a date
templates/entry-template.html  # Template for new entries
scripts/update_index.py        # Scans entries/ and regenerates the homepage index
scripts/md2html.py             # Converts a Markdown note into an entry page
assets/                        # Shared styles and scripts
templates/note-template.md     # Markdown template for new entries
```

## Adding a new entry

1. Copy the template: `cp templates/entry-template.html entries/2026-08-06.html`
2. Edit `entries/2026-08-06.html`:
   - Set `<title>` to `2026-08-06 · Entry title`
   - Set the `<h1>` title and the `.entry-date` date
   - Write the log: progress today / issues encountered / next steps
3. Regenerate the homepage index:

   ```bash
   python3 scripts/update_index.py
   ```

4. Commit and push:

   ```bash
   git add .
   git commit -m "add progress 2026-08-06"
   git push
   ```

## Adding a new entry from Markdown (optional)

Prefer writing notes in Markdown? Convert one directly into an entry page:

```bash
python3 scripts/md2html.py notes/2026-08-06.md
```

- Start from `templates/note-template.md`, or write your own: the first
  `# Heading` becomes the entry title.
- If the file name starts with `YYYY-MM-DD`, that date is used; otherwise
  today's date is used.
- The output keeps the input file name, so several notes on the same day each
  become their own page without overwriting each other:

  ```bash
  python3 scripts/md2html.py notes/2026-08-06-chunking.md
  python3 scripts/md2html.py notes/2026-08-06-graphrag.md
  ```

  The index is regenerated automatically (use `--no-index` to skip that).
- Supported syntax: headings, paragraphs, fenced code blocks, blockquotes,
  lists (with nesting), horizontal rules, inline code, bold, italic, links,
  and images.
- A demo note showing all supported syntax lives in `demo.md` (convert it
  with `-o` to a scratch path so it does not overwrite a dated entry).

## Enabling GitHub Pages

1. Push the code to GitHub (repository: `ZYnoe/ontology-research-progress`)
2. Open the repository Settings → Pages
3. Source: **Deploy from a branch**, Branch: `main`, directory `/ (root)`
4. After saving, the site will be published at
   `https://ZYnoe.github.io/ontology-research-progress/`

> This is a pure static site with no build step; GitHub publishes the HTML in
> the repository directly.

## Using the homepage

- In "Jump to a date", pick a date and click "View log" to filter the entry
  list below to that date; click "Show all" to restore the full list. If
  there is no entry for the date, a hint is shown instead.
- All entries are listed by year and month below; click one to open it.
