# Demo note: markdown → HTML

This file shows every feature the converter supports. Try it with:

```bash
python3 scripts/md2html.py demo.md -o /tmp/demo.html --no-index
```

## Text formatting

Plain **bold**, *italic*, and `inline code` all work, as do
[links](https://example.com) and images:

![placeholder](https://placehold.co/600x100?text=Demo+image)

## Lists

Unordered:

- Extract text from PDF
- Chunk it semantically
- Embed the chunks

Ordered, with nesting:

1. Extraction
   - PyMuPDF
   - pdfplumber
2. Chunking
   - Semantic
   - Word count
3. Embedding

## Blockquote

> A quote can contain `code` and **bold** too.

## Code block

```python
def chunk(text, size=500):
    return [text[i:i + size] for i in range(0, len(text), size)]
```

## Horizontal rule

---

That is the end of the demo.
