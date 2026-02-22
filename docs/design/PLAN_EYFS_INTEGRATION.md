# Plan: Extending the Graph Downward to EYFS

**Date:** 2026-02-22
**Status:** Draft for review
**Scope:** Early Years Foundation Stage (Reception, age 4-5)

---

## Context

The graph currently covers KS1-KS4 (Y1-Y11, ages 5-16). This plan covers what comes *before*: the Early Years Foundation Stage (EYFS).

EYFS is structurally different from KS1-4. The National Curriculum programmes of study do not begin until KS1. EYFS has its own statutory framework (DfE, separate from the NC), organised around **7 Areas of Learning and Development** rather than subjects, and assessed via **17 Early Learning Goals (ELGs)** rather than programmes of study with objectives.

This creates a modelling decision: do we use the same Programme→Domain→Objective→Concept hierarchy, or introduce EYFS-specific node types?

---

## What Exists in the EYFS Statutory Framework

### Source Documents (all GOV.UK)

| Document | URL | Status |
|----------|-----|--------|
| EYFS Statutory Framework (group/school) | https://www.gov.uk/government/publications/early-years-foundation-stage-framework--2 | Current (Sep 2025 revision adds safeguarding only) |
| Development Matters (non-statutory guidance) | https://www.gov.uk/government/publications/development-matters--2 | Current (Sep 2023 revision) |
| EYFS Profile 2024 specification | https://assets.publishing.service.gov.uk/media/65f081f8133c220019cd3935/EYFSP_2024_specification_v1.1.pdf | Current |

### Structure

The EYFS framework defines:

**3 Prime Areas** (time-sensitive — if not achieved by age 5, much harder later):
1. Communication and Language (2 ELGs)
2. Personal, Social and Emotional Development (3 ELGs)
3. Physical Development (2 ELGs)

**4 Specific Areas** (strengthen and apply the prime areas):
4. Literacy (3 ELGs)
5. Mathematics (2 ELGs)
6. Understanding the World (3 ELGs)
7. Expressive Arts and Design (2 ELGs)

**Total: 17 Early Learning Goals** — each describing what children at the expected level of development will achieve by end of Reception.

**Development Matters** provides progression statements across three age bands:
- Birth to 3
- 3 and 4 year olds
- Children in Reception

### Key Differences from KS1+

| Aspect | KS1-4 | EYFS |
|--------|-------|------|
| Governing document | National Curriculum PoS (DFE-00180-2013 etc.) | EYFS Statutory Framework (separate) |
| Organisational unit | Subject (English, Maths, Science...) | Area of Learning (Communication & Language, PSED...) |
| Content structure | Programmes → Domains → Objectives → Concepts | Educational Programmes → ELGs (flat, ~3 bullet points each) |
| Assessment | Teacher assessment + tests (KS2, KS4) | EYFS Profile: Expected / Emerging per ELG |
| Depth | 50-200+ objectives per subject/KS | 17 ELGs total across all areas |
| Year groups | Multiple per KS | Single (Reception only in scope for graph) |
| Statutory status | Objectives are statutory | ELGs are statutory; educational programmes are statutory; everything else is guidance |
| Pedagogy | Subject-specific, increasingly abstract | Play-based, exploratory, concrete-only |

---

## The Mapping Question

The most important architectural decision: how EYFS Areas of Learning map to KS1 Subjects, and therefore how EYFS concepts can serve as prerequisites to KS1 concepts.

### EYFS Area → KS1 Subject Mapping

| EYFS Area of Learning | Maps to KS1 Subject(s) | Mapping quality |
|----------------------|------------------------|-----------------|
| **Communication and Language** | English (Spoken Language domain) | Strong — C&L ELGs directly feed KS1 spoken language objectives |
| **Literacy** | English (Reading, Writing domains) | Strong — Word Reading ELG feeds directly into phonics; Writing ELG feeds handwriting + composition |
| **Mathematics** | Mathematics (Number, Geometry) | Strong — Number ELG feeds Y1 number/place value; Numerical Patterns feeds counting in multiples |
| **Understanding the World: Past and Present** | History | Moderate — ELG 13 is a precursor to chronological understanding |
| **Understanding the World: People, Culture and Communities** | Geography, RE | Moderate — ELG 14 covers maps, communities, other countries |
| **Understanding the World: The Natural World** | Science | Strong — ELG 15 directly feeds KS1 Science (observation, seasons, living things) |
| **Expressive Arts and Design** | Art & Design, Music, D&T | Moderate — ELG 16 feeds art/DT; ELG 17 feeds music/drama |
| **Personal, Social and Emotional Development** | No direct KS1 subject | Weak — PSED has no NC subject equivalent; feeds classroom readiness |
| **Physical Development** | PE (partial) | Moderate — Gross motor feeds PE; fine motor feeds handwriting (English) |

### Cross-cutting EYFS→KS1 Prerequisites

Several KS1 concepts implicitly assume EYFS skills:
- **Phonics (EN-KS1):** Assumes ELG 9 (Word Reading) — letter sounds, digraphs, sound-blending
- **Number bonds (MA-Y1-C008):** Assumes ELG 11 (Number) — deep understanding of numbers to 10, subitising to 5
- **Handwriting (EN-KS1-D005):** Assumes ELG 7 (Fine Motor Skills) — tripod grip, letter formation
- **Counting to 100 (MA-Y1-C001):** Assumes ELG 12 (Numerical Patterns) — counting beyond 20
- **Listening and responding (EN-KS1-O001):** Assumes ELG 1 (Listening, Attention and Understanding)
- **Science observation (SC-KS1):** Assumes ELG 15 (Natural World) — observation skills, vocabulary

---

## Recommendation: Phase it

### Phase 1 (this plan): Docs only — lightweight integration

Add the EYFS layer with:
- Research documentation of the statutory framework (all 17 ELGs, gov.uk sources)
- EYFS→KS1 mapping analysis
- Layer README describing future integration path
- **No extraction JSONs**, no import script, no graph nodes yet

**Rationale:** EYFS is structurally different enough from the NC that we need to make considered modelling decisions before extracting. The docs capture the source material and mapping analysis needed for Phase 2.

### Phase 2 (future): EYFS extraction and import

Create extraction JSONs and import EYFS into the graph. Two approaches:

**Option A: Use existing model (Programme→Domain→Objective→Concept)**
- Treat each EYFS Area of Learning as a Subject
- Create a single Programme per area (Reception)
- Create Domains grouping related ELGs
- Map ELGs to Objectives
- Extract Concepts from ELG bullet points + Development Matters guidance
- Pro: Consistent with existing architecture, simpler queries
- Con: Forces EYFS into a structure it wasn't designed for; concept density will be thin

**Option B: EYFS-specific model (EarlyLearningGoal node type)**
- Add `:EarlyLearningGoal` as a new node label
- Link directly: `(:Year {year_id: 'EYFS'})-[:HAS_ELG]->(:EarlyLearningGoal)`
- ELGs link to KS1 Concepts via `(:EarlyLearningGoal)-[:PREREQUISITE_OF]->(:Concept)`
- Pro: Faithful to EYFS structure; clear semantic distinction
- Con: New node type, new relationships, query complexity

**Recommended: Option A** — it keeps the graph model uniform and the EYFS content is small enough (17 ELGs, ~50-80 concepts) that forcing it into the Programme model won't create problems. The cross-KS prerequisite pattern already works for KS3→KS4; the same pattern (EYFS→KS1) is a natural extension.

### Phase 2 Extraction Approach

Follow the KS1 extraction pattern exactly:
- **One JSON per area of learning** (7 files), stored in `layers/eyfs/data/extractions/`
- **ID pattern:** `EY-R-D001` (EY = Early Years, R = Reception)
- **Concept extraction source:** ELG bullet points + Development Matters Reception statements + Birth to 5 Matters guidance
- **Prerequisites:** Within-EYFS prerequisites (e.g., listening → speaking) + EYFS→KS1 cross-stage links
- **Complexity levels:** 1-2 only (no complexity 3-5 at EYFS)

### Phase 3 (future): Extend learner profiles downward

Add an EYFS/Reception year entry to learner profiles:
- Content guideline: pre-reader, all content must be audio + images, no text on screen
- Pedagogy profile: play-based, very short sessions (5-10 min), concrete only
- Feedback profile: warm, simple, no metacognitive prompts
- Interaction types: voice-only responses, drag-and-drop, physical manipulation analogues

### Phase 4 (far future): Birth to 3 and 3-4 year olds

Development Matters covers two pre-Reception age bands. These would be separate from the graph's current scope (the platform targets ages 5-14) but could be added if the scope extends to younger children.

---

## Estimated Work

| Phase | Type | Effort |
|-------|------|--------|
| 1. Docs only (this plan) | Documentation | Small — research docs + README + plan |
| 2. EYFS extraction + import | Data extraction + code | Medium — 7 JSON files + import script + schema update |
| 3. Learner profiles for EYFS | Data + code | Small — 1 new year entry across 3-4 JSON files |
| 4. Birth to 3 / 3-4 age bands | Research + extraction | Large — different structure, out of current scope |

---

## Open Questions

1. **Year node ID:** Should EYFS use `year_id: "EYFS"` or `year_id: "R"` (Reception) or `year_id: "Y0"`? Recommendation: `"EYFS"` — it's the standard abbreviation and avoids confusion with Y0 which isn't a real year group.

2. **KeyStage node:** Should EYFS be its own KeyStage? The EYFS framework is separate from the National Curriculum. Recommendation: Yes — create `(:KeyStage {key_stage_id: 'EYFS', name: 'Early Years Foundation Stage'})` to maintain structural consistency.

3. **YEAR_PRECEDES chain:** Should we add `(:Year {year_id: 'EYFS'})-[:PRECEDES]->(:Year {year_id: 'Y1'})`? Recommendation: Yes, in Phase 2 when the node exists.

4. **Prime vs Specific distinction:** Should this be captured as a property on EYFS domains/subjects? Recommendation: Yes — `area_type: "prime"` or `area_type: "specific"` as a property on the Subject or Programme node.

5. **GLD subset:** Should the GLD-qualifying ELGs (12 of 17) be flagged? Recommendation: Yes — `contributes_to_gld: true` as a property on the relevant Objective or Concept nodes.

6. **Development Matters statements:** Should these be extracted as separate fine-grained concepts, or just referenced in teaching guidance? Recommendation: Reference in teaching guidance (Phase 2) — the Development Matters statements are non-statutory and very brief, better suited as enrichment than as standalone concepts.

7. **Subject naming:** EYFS areas have long names ("Personal, Social and Emotional Development"). Should we use abbreviations (PSED, C&L, UW, EAD) as subject_id? Recommendation: Use abbreviations for IDs (`CL`, `PSED`, `PD`, `LIT`, `MA`, `UW`, `EAD`) but full names for `name` property.
