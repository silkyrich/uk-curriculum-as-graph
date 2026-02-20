# UK Curriculum as a Knowledge Graph

A Neo4j knowledge graph of the England National Curriculum (KS1–KS3, ages 5–14), with every statutory subject structured as concepts, objectives, domains, prerequisite relationships, and disciplinary skill types. Built as the curriculum ontology layer for an adaptive learning platform.

## What's in the graph

| Layer | Nodes | Notes |
|---|---|---|
| **:Curriculum** | | **UK National Curriculum (England)** |
| Programmes | 38 | One per subject × key stage (or year group) |
| Domains | 225 | Strand/topic groupings within each programme |
| Objectives | 1,193 | Statutory and non-statutory requirements |
| Concepts | 1,032 | Teachable/testable knowledge, skills, processes |
| Prerequisites | 898 relationships | With confidence, type, strength, and rationale |
| **:Epistemic** | | **Disciplinary skills layer** |
| Epistemic skills | 105 | Across 6 subject types (Working Scientifically, etc.) |
| **:Assessment** | | **KS2 test framework layer** |
| Content Domain Codes | 268 | KS2 STA test framework codes (Maths, Reading, GPS) |
| **:Topic** | | **Content layer (humanities)** |
| Topics | 55 | Curriculum content choices (History, Geography) |
| **:Content** | | **Oak National Academy (skeleton)** |
| Oak Units/Lessons | 0 | Awaiting mapping files (v3.4 layer prepared) |
| **:CASE** | | **US academic standards (comparison layer)** |
| Jurisdictions | 2 | US-NGSS, US-CCSS |
| CASE Documents | 2 | NGSS Science, Common Core Math |
| CASE Items | 1,783 | Standards with 6-level hierarchy |

**Subjects covered (KS1–KS2):** Art & Design, Computing, Design & Technology, English (KS1 + Y3–Y6), Geography, History, Languages, Mathematics (Y1–Y6), Music, Physical Education, Science

**Subjects covered (KS3):** Art & Design, Citizenship, Computing, Design & Technology, English, Geography, History, Languages, Mathematics, Music, Physical Education, Science

## Graph model (v3.5)

### Core curriculum (:Curriculum namespace)
```
Curriculum
  └─[HAS_KEY_STAGE]─▶ KeyStage
       └─[HAS_YEAR]─▶ Year
            └─[HAS_PROGRAMME]─▶ Programme ─[FOR_SUBJECT]─▶ Subject
                  │                └─[SOURCED_FROM]─▶ SourceDocument
                  ├─[HAS_DOMAIN]─▶ Domain
                  │     └─[CONTAINS]─▶ Objective
                  │           └─[TEACHES]─▶ Concept
                  ├─[HAS_CONCEPT]─▶ Concept
                  │                    ↕ [PREREQUISITE_OF]
                  └─[DEVELOPS_SKILL]─▶ WorkingScientifically
                                       ReadingSkill
                                       HistoricalThinking
                                       GeographicalSkill
                                       MathematicalReasoning
                                       ComputationalThinking
                                           ↕ [PROGRESSION_OF]
```

### Assessment layer (:Assessment namespace)
```
TestFramework
  └─[HAS_PAPER]─▶ TestPaper
       └─[INCLUDES_CONTENT]─▶ ContentDomainCode
             ├─[ASSESSES]─▶ Programme
             ├─[ASSESSES_DOMAIN]─▶ Domain
             └─[ASSESSES_SKILL]─▶ ReadingSkill
```

### Topic layer (:Topic namespace)
```
Topic ─[TEACHES]─▶ Concept
```

### CASE standards layer (:CASE namespace, v3.5)
```
Jurisdiction ─[PUBLISHES]─▶ CFDocument
                              └─[CONTAINS_ITEM]─▶ CFItem
                                                    ├─[CHILD_OF]─▶ CFItem (hierarchy)
                                                    ├─[PRECEDES]─▶ CFItem (progressions)
                                                    └─[ALIGNS_TO]─▶ Concept/Objective (cross-layer)
```

### The epistemic skill layer

Every subject has two distinct kinds of content: **substantive knowledge** (the *what* — photosynthesis, fractions, the Tudors) and **disciplinary skills** (the *how the subject works* — Working Scientifically, historical source analysis, reading for inference). These are modelled as separate node types rather than conflating them into Concept nodes.

| Node type | Subject | Description |
|---|---|---|
| `WorkingScientifically` | Science | NC statutory strand: questioning, planning, observing, concluding (KS1–KS3) |
| `ReadingSkill` | English | Comprehension skills 2a–2h from KS2 test framework + KS1/KS3 equivalents |
| `HistoricalThinking` | History | Second-order disciplinary concepts: causation, significance, source analysis, interpretation |
| `GeographicalSkill` | Geography | NC skills strand: mapwork, fieldwork, GIS, geographical enquiry |
| `MathematicalReasoning` | Mathematics | NC aims: fluency, reasoning, problem solving — maps to P1/P2/P3 test structure |
| `ComputationalThinking` | Computing | CT pillars: abstraction, decomposition, pattern recognition, algorithm design |

`PROGRESSION_OF` relationships link the same skill across key stages (KS1→KS2→KS3). No supertype node — the relationship type `DEVELOPS_SKILL` / `ASSESSES_SKILL` carries the abstraction.

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

**Epistemic skill nodes (WorkingScientifically, ReadingSkill, etc.)**
- `skill_id`, `skill_name`, `description`
- `key_stage`, `complexity_level` (1–5 within key stage)
- `source_reference`, `strand`
- Type-specific: `test_code` (ReadingSkill), `paper` (MathematicalReasoning), `second_order` (HistoricalThinking)

**PREREQUISITE_OF relationship**
- `confidence` (`explicit` | `inferred` | `suggested`)
- `relationship_type` (`foundational` | `developmental` | `instructional` | `cognitive` | `enabling` | `supportive` | `logical` | `temporal`)
- `strength` (0.0–1.0), `rationale`

**ContentDomainCode**
- `code` (e.g. `4C7`, `2a`, `G3.1`)
- `description`, `strand`, `year_group`, `paper`

## Research foundation

The graph is designed as the curriculum ontology layer for an adaptive learning platform. The design decisions are grounded in the learning science literature. Key findings from the research:

### What the evidence says works

**Prerequisite-aware sequencing.** The "outer fringe" concept — always teaching at the boundary of what a student has already mastered — is the key innovation in ALEKS (Knowledge Space Theory) and the most effective sequencing principle in the ITS literature. This is a Cypher query on the prerequisite graph, not a separate system to build.

**Retrieval practice over re-study.** Every question a student answers is a learning event, not just an assessment event. Testing from memory strengthens retention more than reading or watching — even when the test is failed (Roediger & Karpicke, 2006).

**Productive failure before instruction.** Presenting a problem *before* explaining the concept produces significantly better conceptual understanding than instruction-first approaches (Sinha & Kapur meta-analysis, 2021: Cohen's d = 0.36–0.58). The prerequisite graph determines readiness: all prerequisites mastered, target concept not yet learned.

**Spacing and interleaving.** Spaced, interleaved practice outperforms blocked practice on delayed tests by 30–40%, despite feeling more difficult during learning. The fluency paradox: easy practice feels better but produces worse retention (Bjork, 2011).

**Informational feedback over controlling feedback.** Self-determination theory (Ryan & Deci, 2000): feedback that supports competence without controlling behaviour drives intrinsic motivation. "You were faster than two weeks ago" (informational, self-comparative) works. Leaderboards and progress bars visible to others (controlling, social-comparative) do not.

### What the evidence says doesn't work

**Visible progress bars and leaderboards** trigger social comparison. The 2024 "ghost effect" research (Jose et al., Frontiers in Education) found gamification produces students who are physically present but mentally absent — going through motions to collect points rather than engage with learning. Extroverted students benefit; introverted students are actively harmed.

**Expected tangible rewards** for intrinsically interesting activities undermine that motivation (Lepper, Greene & Nisbett, 1973 — the overjustification effect). Badges, unlockable games, and earned rewards are consistently net-negative for intrinsic motivation in subjects students would otherwise find interesting.

**LLMs without structured domain models** hallucinate and drift from curriculum. Independent evaluations of LLM-based tutors find 35% of generated hints are too general, incorrect, or solution-revealing. The productive architecture is LLM over structured domain model — the graph provides curriculum grounding, the LLM provides natural language.

### Platform design principles (evidence-grounded)

| Principle | Evidence basis |
|---|---|
| No visible progress bars or rankings | SDT; gamification ghost effect; social comparison theory |
| AI encouragement over rewards | SDT informational feedback; overjustification effect |
| Self-comparative feedback ("faster than 2 weeks ago") | Growth mindset; effort attribution research |
| Semi-random delight moments | Unexpected rewards avoid overjustification; variable ratio on learning events |
| Productive failure: challenge before explanation | Kapur meta-analysis; expertise reversal effect |
| Spaced retrieval practice | Bjork desirable difficulties; Roediger testing effect |
| Prerequisite gating | ALEKS outer fringe; KST; graph-based KT research |

Full research briefing: [`docs/research_briefing_learner_layer.md`](docs/research_briefing_learner_layer.md)
Annotated bibliography (18 sources): [`docs/research/SOURCES.md`](docs/research/SOURCES.md)

## Data sources

### UK National Curriculum (England)
All curriculum content extracted from official DfE documents:

- [National Curriculum programmes of study (2013)](https://www.gov.uk/government/collections/national-curriculum)
- [KS2 Mathematics Test Framework 2016](https://www.gov.uk/government/publications/key-stage-2-mathematics-test-framework)
- [KS2 English Reading Test Framework 2016](https://www.gov.uk/government/publications/key-stage-2-english-reading-test-framework)
- [KS2 English Grammar, Punctuation and Spelling Test Framework 2016](https://www.gov.uk/government/publications/key-stage-2-english-grammar-punctuation-and-spelling-test-framework)

Source PDFs are in `data/curriculum-documents/`. Provenance for test framework data is documented in `data/extractions/test-frameworks/PROVENANCE.md`.

### US Academic Standards (CASE layer)
CASE (IMS Global Competencies and Academic Standards Exchange) packages from:

- [OpenSALT](https://opensalt.net) — public CASE server (NGSS, Common Core Math)
- NGSS: Next Generation Science Standards (Achieve Inc, 2013)
- Common Core State Standards for Mathematics (CCSSO, 2010)

Fetched packages cached in `data/extractions/case/packages/`. Research notes on framework comparisons in `docs/research/case-standards/`.

## Prerequisites

- Python 3.10+
- Neo4j 5.x (local or cloud — Neo4j Aura Free works perfectly)
- `neo4j` Python driver: `pip install neo4j`

## Setup and import

### 1. Configure Neo4j connection

Set environment variables (use your Neo4j Aura credentials or local instance):

```bash
export NEO4J_URI="neo4j+s://xxxxx.databases.neo4j.io"  # or neo4j://127.0.0.1:7687 for local
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your-password-here"
```

### 2. Create schema constraints and indexes

```bash
python3 core/scripts/create_schema.py
```

### 3. Import all layers

**Quick start — import everything:**

```bash
python3 core/scripts/import_all.py
```

This imports all 6 layers in dependency order:
1. UK Curriculum (foundation)
2. Assessment
3. Epistemic Skills
4. Topics
5. CASE Standards
6. Oak Content

**Or import layers individually:**

```bash
python3 layers/uk-curriculum/scripts/import_curriculum.py
python3 layers/assessment/scripts/import_test_frameworks.py
python3 layers/epistemic-skills/scripts/import_epistemic_skills.py
python3 layers/topics/scripts/import_topics.py
python3 layers/case-standards/scripts/import_case_standards_v2.py --import
python3 layers/oak-content/scripts/import_oak_content.py --import
```

**Skip optional layers:**

```bash
python3 core/scripts/import_all.py --skip-case --skip-oak
```

### 4. Add visualization properties

```bash
python3 core/scripts/add_name_properties.py
python3 core/scripts/add_display_properties.py
```

### 5. Validate the graph

```bash
python3 core/scripts/validate_schema.py
```

All checks should PASS before using the graph.

## Layer documentation

Each layer has its own detailed README:
- `layers/uk-curriculum/README.md` — UK National Curriculum foundation
- `layers/assessment/README.md` — KS2 test frameworks
- `layers/epistemic-skills/README.md` — Disciplinary thinking skills
- `layers/topics/README.md` — Curriculum content choices (History, Geography)
- `layers/case-standards/README.md` — US/international standards comparison
- `layers/oak-content/README.md` — Oak National Academy content

**Quick reference**: See `CLAUDE.md` for a complete guide to the project structure and common tasks.

## Example queries

**All prerequisites for a concept (upstream chain)**
```cypher
MATCH path = (prereq:Concept)-[:PREREQUISITE_OF*]->(target:Concept {concept_id: 'MA-KS3-C042'})
RETURN path
```

**Outer fringe — concepts ready to learn (all prerequisites mastered)**
```cypher
// Replace student_mastered_ids with actual mastered concept IDs
WITH ['MA-Y4-C001', 'MA-Y4-C002'] AS mastered
MATCH (candidate:Concept)-[:PREREQUISITE_OF*]->(already:Concept)
WHERE already.concept_id IN mastered
  AND NOT candidate.concept_id IN mastered
  AND ALL(p IN [(candidate)<-[:PREREQUISITE_OF]-(prereq) | prereq.concept_id]
          WHERE prereq.concept_id IN mastered)
RETURN candidate.concept_name, candidate.key_stage
```

**Disciplinary skills a programme develops**
```cypher
MATCH (p:Programme {programme_id: 'PROG-Science-KS2'})-[:DEVELOPS_SKILL]->(s:WorkingScientifically)
RETURN s.skill_name, s.strand, s.complexity_level
ORDER BY s.complexity_level
```

**Reading skill progression KS1 → KS2 → KS3**
```cypher
MATCH path = (ks1:ReadingSkill {key_stage: 'KS1'})-[:PROGRESSION_OF*]->(ks3:ReadingSkill {key_stage: 'KS3'})
RETURN ks1.skill_name, [n IN nodes(path) | n.skill_name] AS progression
```

**Most foundational concepts (most things depend on them)**
```cypher
MATCH (c:Concept)<-[:PREREQUISITE_OF]-(other:Concept)
RETURN c.concept_name, c.key_stage, count(other) AS dependents
ORDER BY dependents DESC
LIMIT 20
```

**Cross-subject prerequisite chains (KS1 → KS3)**
```cypher
MATCH path = (start:Concept)-[:PREREQUISITE_OF*]->(end:Concept)
WHERE start.key_stage = 'KS1' AND end.key_stage = 'KS3'
RETURN path
ORDER BY length(path) DESC
LIMIT 5
```

**US vs UK curriculum structure comparison (CASE layer)**
```cypher
// NGSS 3D learning model structure
MATCH (f:Framework {framework_id: 'ngss-science-2013'})-[:HAS_DIMENSION]->(d:Dimension)
MATCH (d)-[r]->(child)
RETURN d.dimension_name, type(r) as relationship, count(child) as count
ORDER BY d.dimension_type
// Returns: Science and Engineering Practices (8), Disciplinary Core Ideas (41), Crosscutting Concepts (12)
```

**NGSS Science and Engineering Practices**
```cypher
MATCH (d:Dimension {dimension_type: 'practice'})-[:HAS_PRACTICE]->(p:Practice)
RETURN p.practice_number, p.practice_name
ORDER BY p.practice_number
// Shows all 8 SEPs: Asking Questions, Developing Models, etc.
```

**Compare NGSS Practices vs UK Working Scientifically**
```cypher
// NGSS Practices
MATCH (p:Practice)
RETURN p.practice_name AS ngss_practice
// vs UK Working Scientifically
MATCH (ws:WorkingScientifically {key_stage: 'KS3'})
RETURN ws.skill_name AS uk_skill
```

More CASE comparison queries in `data/extractions/case/README.md`.

## Repository layout (layer-based structure)

The project is organized into **layers** — each layer is a self-contained module with its own import scripts, data extractions, and documentation. Layers can be imported independently or removed cleanly.

```
layers/                          ← Layer-based organization (NEW)
  uk-curriculum/                 Foundation layer: UK National Curriculum
    scripts/import_curriculum.py
    data/extractions/primary/    KS1–KS2 JSONs (26 files)
    data/extractions/secondary/  KS3 JSONs (12 files)
    README.md

  assessment/                    Test Frameworks layer
    scripts/import_test_frameworks.py
    data/extractions/test-frameworks/
    README.md

  epistemic-skills/              Disciplinary skills layer
    scripts/import_epistemic_skills.py
    data/extractions/epistemic-skills/
    README.md

  topics/                        Topic layer (History, Geography)
    scripts/import_topics.py
    data/extractions/topics/
    README.md

  case-standards/                US/International standards comparison
    scripts/import_case_standards_v2.py
    data/extractions/case/
      case_sources.json
      packages/                  Cached CASE packages
      mappings/                  Cross-layer alignments
    README.md

  oak-content/                   Oak National Academy content
    scripts/import_oak_content.py
    data/extractions/oak/
      catalogue/                 API discovery cache
      mappings/                  Curriculum alignments
    README.md

core/                            ← Shared infrastructure
  scripts/
    neo4j_config.py              Shared Neo4j configuration
    create_schema.py             Schema constraints/indexes
    validate_schema.py           Graph integrity checks
    validate_extractions.py      JSON validation
    add_name_properties.py       Visualization setup
    add_display_properties.py    Visualization setup
    import_all.py                Import orchestrator (all layers)
  data/
    bloom/                       Neo4j Bloom perspectives
    curriculum-documents/        Source document metadata
  docs/
    graph_model_overview.md      Graph model documentation
  README.md

docs/                            ← Research and documentation
  research_briefing_learner_layer.md
  user_stories_child_experience.md
  research/
    case-standards/              CASE framework research
    [18 cached papers + SOURCES.md]
  CURRICULUM_ANALYSIS.md
  extraction_inventory.md
  graph_model_v2.md

scripts/                         ← Legacy location (deprecated, see layers/)
data/                            ← Legacy location (deprecated, see layers/)
migrations/                      Cypher migration scripts
CLAUDE.md                        AI agent navigation guide
```

**NEW**: See `CLAUDE.md` for the complete guide to navigating this project, including common tasks, troubleshooting, and layer architecture.
