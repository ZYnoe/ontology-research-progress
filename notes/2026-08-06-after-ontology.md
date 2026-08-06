# Ontology-Constrained KG Construction

> **Working assumption:** we supply our own ontology up front.

## 1. What is a knowledge graph?

A way of storing facts as a network. In RDF, the atomic unit is a **triple** —
*subject, predicate, object* — where each triple is one labeled edge between
two nodes. (The object may also be a literal rather than an entity.)

## 2. What separates a KG from a plain graph?

No single accepted answer. The criterion I adopt here is a **schema layer**:
the graph carries not just instance facts but a vocabulary defining what kinds
of things exist and how they may relate.

> Under this view, the instance-level portion of the graph is the **ABox**.
> Note that most definitions (e.g. Hogan et al. 2021) place schema *and*
> instances inside the KG — ABox/TBox is a split within it, not a boundary
> around it.

## 3. Ontology

An ontology supplies the terminology:

| Component | DL box | Note |
|---|---|---|
| Classes, class axioms | TBox | subsumption, equivalence, disjointness |
| Property axioms | RBox | domain/range, chains, characteristics |
| Individual assertions | ABox | typing and relation facts |

**Caveat — OWL has no constraints.** Open-world semantics + no unique name
assumption mean OWL axioms license *inferences*, they do not reject data.
Validation belongs to **SHACL / ShEx**.

### However —

OWL uses "ontology" differently from the DL convention. An `owl:Ontology` is a
**document** (a set of axioms plus annotations), and that document is free to
contain individual assertions alongside class axioms. The TBox/ABox split is
conceptual, not enforced by the serialization.

## 4. Given an ontology, schema-constrained extraction is possible

Prior art, positioned honestly:

- **MatKG** (Venugopal & Olivetti, *Sci Data* 2024) — NER over a large corpus
  with a fixed entity-type list; relations derived from statistical
  co-occurrence, yielding a *pseudo-ontological* schema. Schema is an output,
  not a constraint. ~70k entities, 5.4M triples.
- **MatKG-2** (NeurIPS 2023 workshop) — LLM committees for ontology induction;
  closer to our setting.
- **Ours** — the ontology (CMSO / ASMO / EMMO / MDS-Onto) is fixed *before*
  extraction and constrains the predicate space, with IRI provenance per triple.

> Open question: GraphRAG induces its own entity types from text rather than
> consuming a given ontology. Where does that leave the "verifiable prior"
> claim — complement or competitor?