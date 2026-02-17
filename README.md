# UK Curriculum as a Knowledge Graph

A Neo4j knowledge graph of the England National Curriculum (KS1–KS3, ages 5–14), with every statutory subject structured as concepts, objectives, domains, and prerequisite relationships. Includes a KS2 STA test framework layer linking assessed content domain codes to curriculum concepts.

## What's in the graph

| Layer | Nodes | Notes |
|---|---|---|
| Programmes | 38 | One per subject × key stage (or year group) |
| Domains | 225 | Strand/topic groupings within each programme |
| Objectives | 1,193 | Statutory and non-statutory requirements |
| Concepts | 1,032 | Teachable/testable knowledge, skills, processes |
| Prerequisites | 898 relationships | With confidence, type, strength, and rationale |
| Content Domain Codes | 268 | KS2 STA test framework codes (Maths, Reading, GPS) |

**Subjects covered (KS1–KS2):** Art & Design, Computing, Design & Technology, English (KS1 + Y3–Y6), Geography, History, Languages, Mathematics (Y1–Y6), Music, Physical Education, Science

**Subjects covered (KS3):** Art & Design, Citizenship, Computing, Design & Technology, English, Geography, History, Languages, Mathematics, Music, Physical Education, Science

## Graph model

```
Curriculum
  └─[HAS_KEY_STAGE]─▶ KeyStage
       └─[HAS_YEAR]─▶ Year
            └─[HAS_PROGRAMME]─▶ Programme ─[FOR_SUBJECT]─▶ Subject
                  │                └─[SOURCED_FROM]─▶ SourceDocument
                  ├─[HAS_DOMAIN]─▶ Domain
                  │     └─[CONTAINS]─▶ Objective
                  │           └─[TEACHES]─▶ Concept
                  └─[HAS_CONCEPT]─▶ Concept
                                       ↕
                              [PREREQUISITE_OF]

TestFramework
  └─[HAS_PAPER]─▶ TestPaper
       └─[INCLUDES_CONTENT]─▶ ContentDomainCode
             ├─[ASSESSES]─▶ Programme
             └─[ASSESSES_DOMAIN]─▶ Domain
```

### Node properties (key fields)

**Concept**
- `concept_id`, `concept_name`, `concept_type` (`knowledge` | `skill` | `process` | `attitude` | `content`)
- `complexity_level` (1–5 within key stage)
- `description`, `source_reference`

**Objective**
- `objective_id`, `objective_text`, `is_statutory` (boolean)
- `non_statutory_guidance`, `examples`
- `source_reference` — human-readable DfE citation

**Domain**
- `domain_id`, `domain_name`, `structure_type`, `curriculum_context`
- `source_reference`

**PREREQUISITE_OF relationship**
- `confidence` (`explicit` | `inferred` | `suggested`)
- `relationship_type` (`foundational` | `developmental` | `instructional` | `cognitive` | `enabling` | `supportive` | `logical` | `temporal`)
- `strength` (0.0–1.0), `rationale`

**ContentDomainCode**
- `code` (e.g. `4C7`, `2a`, `G3.1`)
- `description`, `strand`, `year_group`, `paper`

## Data sources

All content extracted from official DfE documents:

- [National Curriculum programmes of study (2013)](https://www.gov.uk/government/collections/national-curriculum)
- [KS2 Mathematics Test Framework 2016](https://www.gov.uk/government/publications/key-stage-2-mathematics-test-framework)
- [KS2 English Reading Test Framework 2016](https://www.gov.uk/government/publications/key-stage-2-english-reading-test-framework)
- [KS2 English Grammar, Punctuation and Spelling Test Framework 2016](https://www.gov.uk/government/publications/key-stage-2-english-grammar-punctuation-and-spelling-test-framework)

Source PDFs are in `data/curriculum-documents/`. Provenance for test framework data is documented in `data/extractions/test-frameworks/PROVENANCE.md`.

## Prerequisites

- Python 3.10+
- [Neo4j Desktop](https://neo4j.com/download/) with a local DBMS running at `neo4j://127.0.0.1:7687`
- `neo4j` Python driver: `pip install neo4j`

The scripts hardcode `neo4j` / `password123` as credentials — change in each script if needed.

## Setup and import

```bash
# 1. Create Neo4j constraints and indexes (one-off)
python3 scripts/create_schema.py

# 2. Validate extraction JSONs before touching the database
python3 scripts/validate_extractions.py

# 3. Import curriculum (clears and reimports)
python3 scripts/import_curriculum.py

# 4. Import KS2 test framework layer
python3 scripts/import_test_frameworks.py

# 5. Post-import schema validation (21 checks)
python3 scripts/validate_schema.py
```

See `scripts/README.md` for full workflow details.

## Example queries

**All prerequisites for a concept (upstream chain)**
```cypher
MATCH path = (prereq:Concept)-[:PREREQUISITE_OF*]->(target:Concept {concept_id: 'MA-KS3-C042'})
RETURN path
```

**Most foundational concepts (most things depend on them)**
```cypher
MATCH (c:Concept)<-[:PREREQUISITE_OF]-(other:Concept)
RETURN c.concept_name, c.key_stage, count(other) AS dependents
ORDER BY dependents DESC
LIMIT 20
```

**Objectives linked to a KS2 Maths test framework code**
```cypher
MATCH (code:ContentDomainCode {code: '4C7'})-[:ASSESSES]->(p:Programme)
      <-[:HAS_PROGRAMME]-(:Year)<-[:HAS_YEAR]-(:KeyStage)
MATCH (p)-[:HAS_DOMAIN]->(d:Domain)-[:CONTAINS]->(o:Objective)
RETURN code.code, code.description, o.objective_text
```

**Cross-subject prerequisite chains (KS1 → KS3)**
```cypher
MATCH path = (start:Concept)-[:PREREQUISITE_OF*]->(end:Concept)
WHERE start.key_stage = 'KS1' AND end.key_stage = 'KS3'
RETURN path
ORDER BY length(path) DESC
LIMIT 5
```

**All content domain codes assessed in Year 5**
```cypher
MATCH (code:ContentDomainCode {year_group: 5})
RETURN code.code, code.strand, code.description
ORDER BY code.code
```

## Repository layout

```
data/
  curriculum-documents/     Source PDFs + metadata.json
  extractions/
    primary/                KS1–KS2 extraction JSONs (26 files)
    secondary/              KS3 extraction JSONs (12 files)
    test-frameworks/        KS2 STA test framework JSONs + PROVENANCE.md
    _quarantine/            Files pending review before import

docs/
  CURRICULUM_ANALYSIS.md
  extraction_inventory.md

scripts/
  create_schema.py          One-off: Neo4j constraints and indexes
  validate_extractions.py   Pre-import JSON validation
  import_curriculum.py      Main curriculum importer
  import_test_frameworks.py KS2 test framework importer
  validate_schema.py        Post-import graph validation (21 checks)
  README.md                 Script workflow and notes
```

## Potential uses

- **Adaptive assessment** — test a concept, trace prerequisites backward to find gaps
- **Learning path generation** — shortest/optimal routes through the curriculum graph
- **Curriculum coverage analysis** — which concepts are most foundational, most advanced, most connected
- **AI tutoring** — structured ontology for explaining why prerequisites matter
- **KS2 SATs preparation** — map test framework content domain codes to specific curriculum concepts
