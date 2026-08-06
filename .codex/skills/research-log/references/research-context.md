# Research Context

Snapshot of the research state this site tracks. Update this file whenever a
milestone or open question changes.

## Goal

Build an ontology / knowledge graph from Korean materials-research data —
starting from the 소재 연구데이터 표준어휘 2025-2 standard vocabulary and
literature PDFs — and support downstream retrieval over it.

## Pipeline status

Done:

- PDF text extraction works (docling / PyMuPDF class tooling available in the
  environment).
- Chunking implemented in two ways: semantic chunking and word-count
  (fixed-size) chunking.
- Chunked text is embedded with an embedding model; the
  extraction → chunking → embedding pipeline is in place.

Open question:

- Whether to invest in different RAG techniques, e.g. GraphRAG. Decision
  rule: run a GraphRAG pilot only if the research questions need multi-hop
  entity-relation reasoning; otherwise improve chunking/retrieval quality on
  the plain vector pipeline first.

## Planned next work

- Compare retrieval quality of semantic vs. word-count chunking on a small
  test set.
- Classify the 표준어휘 2025-2 terms into a taxonomy (facet assignment,
  genus–differentia parsing of official definitions, Korean morphology,
  embedding clusters, LLM induction, EMMO/PMDco mapping, agreement-based
  merge).
- Decide on GraphRAG based on the decision rule above.

## Conventions

- Notes mix English and Korean; keep Korean technical terms as-is.
- A method plan for the 2025-2 classification exists locally at
  `entries/2026-08-07.html`, but that file is intentionally not published to
  the repo (see SKILL.md pitfalls).
