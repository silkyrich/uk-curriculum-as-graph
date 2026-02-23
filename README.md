# UK Curriculum as a Knowledge Graph

A Neo4j knowledge graph of the England National Curriculum (EYFS through KS4, ages 4-16), with every statutory subject structured as concepts, objectives, domains, prerequisite relationships, disciplinary skill types, concept clusters, thinking lenses, and teaching packs. Built as the curriculum ontology layer for an adaptive learning platform.

## What's in the graph

| Layer | Nodes | Notes |
|---|---|---|
| **UK National Curriculum** | | **Foundation layer (KS1-KS4)** |
| Programmes | 55+ | One per subject x key stage (or year group) |
| Domains | 316 | Strand/topic groupings within each programme |
| Objectives | 1,559+ | Statutory and non-statutory requirements |
| Concepts | 1,278+ | Teachable/testable knowledge, skills, processes |
| Prerequisites | 1,354+ rels | With confidence, type, strength, and rationale |
| **EYFS** | | **Early Years Foundation Stage (Reception)** |
| Programmes | 7 | One per area of learning |
| Objectives | 51 | Covering 17 Early Learning Goals |
| Concepts | 53 | EYFS-to-KS1 prerequisite links included |
| **Concept Grouping** | | **Derived lesson clusters** |
| ConceptClusters | 626 | Introduction (167) and practice (459) types |
| CO_TEACHES | 1,827 rels | Co-teachability signal between concepts |
| **ThinkingLens** | | **Cross-subject cognitive framing** |
| ThinkingLens nodes | 10 | Patterns, Cause & Effect, Scale, Systems, etc. |
| APPLIES_LENS | 1,222 rels | Ranked lens assignments (~2 per cluster) |
| **Content Vehicles** | | **Choosable teaching packs** |
| ContentVehicle nodes | ~61 | Topic studies, case studies, investigations, text studies, worked examples |
| DELIVERS | ~120 rels | Many-to-many: vehicles deliver concepts |
| **Epistemic Skills** | | **Disciplinary skills layer** |
| Epistemic skills | 105 | Across 6 subject types (Working Scientifically, etc.) |
| **Assessment** | | **KS2 test framework layer** |
| Content Domain Codes | 268 | KS2 STA test framework codes (Maths, Reading, GPS) |
| **Topics** | | **Content layer (humanities)** |
| Topics | 55 | Curriculum content choices (History, Geography) |
| **Learner Profiles** | | **Age-appropriate design constraints** |
| InteractionType | 33 | UI/pedagogical patterns per year group |
| ContentGuideline | 11 | Reading level, vocabulary constraints per year |
| PedagogyProfile | 11 | Session structure, scaffolding per year |
| FeedbackProfile | 11 | Tone, gamification safety per year |
| PedagogyTechnique | 5 | Desirable difficulty techniques with evidence |
| **CASE Standards** | | **US academic standards (comparison layer)** |
| Jurisdictions | 2 | US-NGSS, US-CCSS |
| CASE Documents | 2 | NGSS Science, Common Core Math |
| CASE Items | 1,783 | Standards with 6-level hierarchy |
| **Visualization** | | **Neo4j Bloom perspectives** |
| Bloom perspectives | 5 | With icons, styleRules, and search templates |

**Total: ~5,600+ nodes** in Neo4j Aura cloud database.

**Subjects covered (KS1-KS2):** Art & Design, Computing, Design & Technology, English (KS1 + Y3-Y6), Geography, History, Languages, Mathematics (Y1-Y6), Music, Physical Education, Science

**Subjects covered (KS3):** Art & Design, Citizenship, Computing, Design & Technology, English, Geography, History, Languages, Mathematics, Music, Physical Education, Science

**Subjects covered (KS4):** Art & Design, Biology, Business, Chemistry, Citizenship, Computing, Design & Technology, Drama, English Language, English Literature, Food Preparation & Nutrition, Geography, History, Languages (MFL), Mathematics, Media Studies, Music, Physical Education, Physics, Religious Studies

**EYFS (Reception):** Communication & Language, Personal Social & Emotional Development, Physical Development, Literacy, Mathematics, Understanding the World, Expressive Arts & Design

## Graph model (v3.8)

### Core curriculum
```
Curriculum
  +--[HAS_KEY_STAGE]--> KeyStage
       +--[HAS_YEAR]--> Year --[PRECEDES]--> Year
            +--[HAS_PROGRAMME]--> Programme --[FOR_SUBJECT]--> Subject
                  |                +--[SOURCED_FROM]--> SourceDocument
                  +--[HAS_DOMAIN]--> Domain
                  |     +--[CONTAINS]--> Objective
                  |     |     +--[TEACHES]--> Concept
                  |     +--[HAS_CLUSTER]--> ConceptCluster
                  |     |     +--[GROUPS]--> Concept
                  |     |     +--[SEQUENCED_AFTER]--> ConceptCluster
                  |     |     +--[APPLIES_LENS {rank, rationale}]--> ThinkingLens
                  |     +--[HAS_VEHICLE]--> ContentVehicle
                  |           +--[DELIVERS]--> Concept
                  |           +--[IMPLEMENTS]--> Topic (optional)
                  +--[HAS_CONCEPT]--> Concept
                  |                    <--> [PREREQUISITE_OF]
                  |                    <--> [CO_TEACHES]
                  +--[DEVELOPS_SKILL]--> WorkingScientifically / ReadingSkill /
                                         HistoricalThinking / GeographicalSkill /
                                         MathematicalReasoning / ComputationalThinking
                                             <--> [PROGRESSION_OF]
```

### Learner profiles (linked from Year)
```
Year --[HAS_CONTENT_GUIDELINE]--> ContentGuideline
     --[HAS_PEDAGOGY_PROFILE]--> PedagogyProfile --[USES_TECHNIQUE]--> PedagogyTechnique
     --[HAS_FEEDBACK_PROFILE]--> FeedbackProfile       |                    <--> [REQUIRES]
     --[SUPPORTS_INTERACTION]--> InteractionType --[PRECEDES]--> InteractionType
                                                 --[SUPPORTS_LEARNING_OF]--> Subject
```

### Assessment layer
```
TestFramework
  +--[HAS_PAPER]--> TestPaper
       +--[INCLUDES_CONTENT]--> ContentDomainCode
             +--[ASSESSES]--> Programme
             +--[ASSESSES_DOMAIN]--> Domain
             +--[ASSESSES_SKILL]--> ReadingSkill
```

### Topic layer
```
Topic --[TEACHES]--> Concept
```

### CASE standards layer (US comparison)
```
Framework --[HAS_DIMENSION]--> Dimension
                                +--[HAS_PRACTICE]--> Practice
                                +--[HAS_CORE_IDEA]--> CoreIdea
PerformanceExpectation --[USES_PRACTICE]--> Practice
                       --[USES_CORE_IDEA]--> CoreIdea
Practice --[ALIGNS_TO]--> Concept  (cross-layer)
```

### The epistemic skill layer

Every subject has two distinct kinds of content: **substantive knowledge** (the *what* -- photosynthesis, fractions, the Tudors) and **disciplinary skills** (the *how the subject works* -- Working Scientifically, historical source analysis, reading for inference). These are modelled as separate node types rather than conflating them into Concept nodes.

| Node type | Subject | Description |
|---|---|---|
| `WorkingScientifically` | Science | NC statutory strand: questioning, planning, observing, concluding (KS1-KS3) |
| `ReadingSkill` | English | Comprehension skills 2a-2h from KS2 test framework + KS1/KS3 equivalents |
| `HistoricalThinking` | History | Second-order disciplinary concepts: causation, significance, source analysis, interpretation |
| `GeographicalSkill` | Geography | NC skills strand: mapwork, fieldwork, GIS, geographical enquiry |
| `MathematicalReasoning` | Mathematics | NC aims: fluency, reasoning, problem solving -- maps to P1/P2/P3 test structure |
| `ComputationalThinking` | Computing | CT pillars: abstraction, decomposition, pattern recognition, algorithm design |

`PROGRESSION_OF` relationships link the same skill across key stages (KS1->KS2->KS3). Concept-level `DEVELOPS_SKILL` links provide fine-grained skill integration (34 Science, 18 Geography, 18 History).

### Concept clusters and thinking lenses

**ConceptClusters** sit between Domain and Concept. Each cluster groups 1-5 concepts into a teachable lesson unit. Two types: `introduction` (first exposure, ~167) and `practice` (fluency/application, ~459). Clusters chain via `SEQUENCED_AFTER` within each domain.

**ThinkingLens** nodes provide cross-subject cognitive framing. 10 lenses adapted from NGSS Crosscutting Concepts + UK-specific frames: Patterns, Cause & Effect, Scale/Proportion/Quantity, Systems & System Models, Energy & Matter, Structure & Function, Stability & Change, Continuity & Change, Perspective & Interpretation, Evidence & Argument. Each lens has a `key_question` and `agent_prompt` for direct LLM instruction.

Every cluster has 1-3 `APPLIES_LENS` relationships with `rank` (1 = primary) and `rationale` explaining why that lens fits that specific cluster.

### Content vehicles

**ContentVehicle** nodes are choosable teaching packs that deliver curriculum concepts with rich metadata. Vehicle types:
- **topic_study** (History) -- sources, key figures, perspectives, period
- **case_study** (Geography) -- location, data points, themes, contrasting cases
- **investigation** (Science) -- enquiry type, variables, equipment, safety
- **text_study** (English) -- genre, suggested texts, grammar focus, writing outcome
- **worked_example_set** (Maths) -- CPA stage, manipulatives, representations, difficulty levels

Many-to-many: one vehicle delivers multiple concepts, one concept can be delivered by multiple vehicles. This enables teacher choice.

### Node properties (key fields)

**Concept**
- `concept_id`, `concept_name`, `concept_type` (`knowledge` | `skill` | `process` | `attitude` | `content`)
- `complexity_level` (1-5 within key stage)
- `teaching_weight` (1-6), `co_teach_hints`, `is_keystone`, `prerequisite_fan_out`
- `description`, `source_reference`

**ConceptCluster**
- `cluster_id`, `name`, `cluster_type` (`introduction` | `practice`)
- `is_keystone`, `teaching_weight`, `thinking_lens_primary`
- `teaching_guidance`, `common_misconceptions`

**ContentVehicle**
- `vehicle_id`, `name`, `vehicle_type`, `subject`, `key_stage`
- `definitions`, `assessment_guidance`, `success_criteria`
- Subject-specific: `sources`, `perspectives` (History), `enquiry_type`, `equipment` (Science), etc.

**Objective**
- `objective_id`, `objective_text`, `is_statutory` (boolean)
- `non_statutory_guidance`, `examples`
- `source_reference` -- human-readable DfE citation

**PREREQUISITE_OF relationship**
- `confidence` (`explicit` | `inferred` | `suggested`)
- `relationship_type` (`foundational` | `developmental` | `instructional` | `cognitive` | `enabling` | `supportive` | `logical` | `temporal`)
- `strength` (0.0-1.0), `rationale`

## Research foundation

The graph is designed as the curriculum ontology layer for an adaptive learning platform. The design decisions are grounded in the learning science literature. Key findings from the research:

### What the evidence says works

**Prerequisite-aware sequencing.** The "outer fringe" concept -- always teaching at the boundary of what a student has already mastered -- is the key innovation in ALEKS (Knowledge Space Theory) and the most effective sequencing principle in the ITS literature. This is a Cypher query on the prerequisite graph, not a separate system to build.

**Retrieval practice over re-study.** Every question a student answers is a learning event, not just an assessment event. Testing from memory strengthens retention more than reading or watching -- even when the test is failed (Roediger & Karpicke, 2006).

**Productive failure before instruction.** Presenting a problem *before* explaining the concept produces significantly better conceptual understanding than instruction-first approaches (Sinha & Kapur meta-analysis, 2021: Cohen's d = 0.36-0.58). The prerequisite graph determines readiness: all prerequisites mastered, target concept not yet learned.

**Spacing and interleaving.** Spaced, interleaved practice outperforms blocked practice on delayed tests by 30-40%, despite feeling more difficult during learning. The fluency paradox: easy practice feels better but produces worse retention (Bjork, 2011).

**Informational feedback over controlling feedback.** Self-determination theory (Ryan & Deci, 2000): feedback that supports competence without controlling behaviour drives intrinsic motivation. "You were faster than two weeks ago" (informational, self-comparative) works. Leaderboards and progress bars visible to others (controlling, social-comparative) do not.

### What the evidence says doesn't work

**Visible progress bars and leaderboards** trigger social comparison. The 2024 "ghost effect" research (Jose et al., Frontiers in Education) found gamification produces students who are physically present but mentally absent -- going through motions to collect points rather than engage with learning. Extroverted students benefit; introverted students are actively harmed.

**Expected tangible rewards** for intrinsically interesting activities undermine that motivation (Lepper, Greene & Nisbett, 1973 -- the overjustification effect). Badges, unlockable games, and earned rewards are consistently net-negative for intrinsic motivation in subjects students would otherwise find interesting.

**LLMs without structured domain models** hallucinate and drift from curriculum. Independent evaluations of LLM-based tutors find 35% of generated hints are too general, incorrect, or solution-revealing. The productive architecture is LLM over structured domain model -- the graph provides curriculum grounding, the LLM provides natural language.

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

Full research briefing: [`docs/design/RESEARCH_BRIEFING.md`](docs/design/RESEARCH_BRIEFING.md)
Annotated bibliography (18 sources): [`docs/research/SOURCES.md`](docs/research/SOURCES.md)

## Data sources

### UK National Curriculum (England)
All curriculum content extracted from official DfE documents:

- [National Curriculum programmes of study (2013)](https://www.gov.uk/government/collections/national-curriculum)
- [KS2 Mathematics Test Framework 2016](https://www.gov.uk/government/publications/key-stage-2-mathematics-test-framework)
- [KS2 English Reading Test Framework 2016](https://www.gov.uk/government/publications/key-stage-2-english-reading-test-framework)
- [KS2 English Grammar, Punctuation and Spelling Test Framework 2016](https://www.gov.uk/government/publications/key-stage-2-english-grammar-punctuation-and-spelling-test-framework)

### EYFS (Early Years Foundation Stage)
- [EYFS Statutory Framework](https://www.gov.uk/government/publications/early-years-foundation-stage-framework--2)
- [Development Matters](https://www.gov.uk/government/publications/development-matters--2)

Source PDFs are in `data/curriculum-documents/`. Provenance for test framework data is documented in `data/extractions/test-frameworks/PROVENANCE.md`.

### US Academic Standards (CASE layer)
CASE (IMS Global Competencies and Academic Standards Exchange) packages from:

- [OpenSALT](https://opensalt.net) -- public CASE server (NGSS, Common Core Math)
- NGSS: Next Generation Science Standards (Achieve Inc, 2013)
- Common Core State Standards for Mathematics (CCSSO, 2010)

Fetched packages cached in `data/extractions/case/packages/`. Research notes on framework comparisons in `docs/research/case-standards/`.

## Prerequisites

- Python 3.10+
- Neo4j 5.x (local or cloud -- Neo4j Aura Free works perfectly)
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

### 3. Import all layers (dependency order)

```bash
# 1. UK Curriculum (foundation -- must be first)
python3 layers/uk-curriculum/scripts/import_curriculum.py

# 2. EYFS (extends curriculum to Reception year)
python3 layers/eyfs/scripts/import_eyfs.py

# 3. Concept grouping signals (enriches Concept nodes)
python3 core/migrations/compute_lesson_grouping_signals.py

# 4. ThinkingLens nodes (must exist before cluster generation)
python3 layers/uk-curriculum/scripts/import_thinking_lenses.py

# 5. Concept clusters (derived from graph topology + thinking lenses)
python3 layers/uk-curriculum/scripts/generate_concept_clusters.py

# 6. Cross-domain CO_TEACHES relationships
python3 core/migrations/create_cross_domain_co_teaches.py

# 7. Assessment (optional, depends on UK curriculum)
python3 layers/assessment/scripts/import_test_frameworks.py

# 8. Epistemic Skills (optional, depends on UK curriculum)
python3 layers/epistemic-skills/scripts/import_epistemic_skills.py

# 9. Concept-level skill links (run after epistemic skills)
python3 core/migrations/create_concept_skill_links.py

# 10. Topics (optional, depends on UK curriculum)
python3 layers/topics/scripts/import_topics.py

# 11. Content Vehicles (optional, depends on UK curriculum + Topics)
python3 layers/content-vehicles/scripts/import_content_vehicles.py

# 12. CASE Standards (optional, independent)
python3 layers/case-standards/scripts/import_case_standards_v2.py --import

# 13. Learner Profiles (optional, depends on UK curriculum Year nodes)
python3 layers/learner-profiles/scripts/import_learner_profiles.py

# 14. Visualization properties (recommended, run last)
python3 layers/visualization/scripts/apply_formatting.py
```

### 4. Validate the graph

```bash
python3 core/scripts/validate_schema.py
```

All checks should PASS before using the graph.

## Simulated teacher reviews

The `generated/` directory contains outputs from simulated teacher evaluations -- AI agents given teacher personas who assess whether the graph contains enough structured information to generate course materials (lesson plans, teaching sequences, assessment).

| Directory | Graph version | What was tested |
|---|---|---|
| `generated/teachers/` | v3 | Initial 5-subject probe (Y1 English, Y3 Maths, Y5 Science, Y7 Maths, Y9 Science) |
| `generated/teachers-v2/` | v3 | Same 5 subjects, improved query helper |
| `generated/teachers-v3/` | v4 | 5 teachers (Y2 Maths, Y4 English, Y5 Science, KS3 Biology, KS3 Geography) |
| `generated/teachers-v4/` | v5 | Same 5 teachers, with Content Vehicles and ThinkingLens |
| `generated/teachers-v5/` | v6 | Full curriculum: Y3 (all subjects), Y4 (all subjects), Y5 (all subjects) |

**Latest scores (v6):** 5.2/10 for course material generation, ~8.5/10 as a curriculum map. The gap is in rich teaching metadata -- the graph captures WHAT to teach but needs more structured data on worked examples, difficulty levels, and assessment items to fully support material generation. See `generated/teachers-v5/v6_group_report.md` for the full synthesis and 7 prioritised schema proposals.

## Layer documentation

Each layer has its own detailed README:
- `layers/uk-curriculum/README.md` -- UK National Curriculum foundation
- `layers/eyfs/README.md` -- Early Years Foundation Stage (Reception)
- `layers/assessment/README.md` -- KS2 test frameworks
- `layers/epistemic-skills/README.md` -- Disciplinary thinking skills
- `layers/topics/README.md` -- Curriculum content choices (History, Geography)
- `layers/content-vehicles/README.md` -- Teaching packs (Content Vehicles)
- `layers/learner-profiles/README.md` -- Age-appropriate design layer + agent query patterns
- `layers/case-standards/README.md` -- US/international standards comparison
- `layers/visualization/README.md` -- Neo4j Bloom perspectives
- `layers/oak-content/README.md` -- Oak National Academy content (skeleton)

**Quick reference**: See `CLAUDE.md` for a complete guide to the project structure and common tasks.

## Example queries

**All prerequisites for a concept (upstream chain)**
```cypher
MATCH path = (prereq:Concept)-[:PREREQUISITE_OF*]->(target:Concept {concept_id: 'MA-KS3-C042'})
RETURN path
```

**Outer fringe -- concepts ready to learn (all prerequisites mastered)**
```cypher
WITH ['MA-Y4-C001', 'MA-Y4-C002'] AS mastered
MATCH (candidate:Concept)-[:PREREQUISITE_OF*]->(already:Concept)
WHERE already.concept_id IN mastered
  AND NOT candidate.concept_id IN mastered
  AND ALL(p IN [(candidate)<-[:PREREQUISITE_OF]-(prereq) | prereq.concept_id]
          WHERE prereq.concept_id IN mastered)
RETURN candidate.concept_name, candidate.key_stage
```

**Lesson sequence for a domain (concept clusters)**
```cypher
MATCH (d:Domain {domain_id: 'MA-Y3-D001'})-[:HAS_CLUSTER]->(cc:ConceptCluster)
OPTIONAL MATCH (cc)-[:SEQUENCED_AFTER]->(prev:ConceptCluster)
OPTIONAL MATCH (cc)-[:APPLIES_LENS {rank: 1}]->(lens:ThinkingLens)
RETURN cc.name, cc.cluster_type, prev.name AS after, lens.name AS thinking_lens
ORDER BY cc.cluster_id
```

**Content vehicles for a concept**
```cypher
MATCH (cv:ContentVehicle)-[:DELIVERS]->(c:Concept {concept_id: 'HI-KS2-C001'})
RETURN cv.name, cv.vehicle_type, cv.assessment_guidance, cv.definitions
```

**Age-appropriate interaction types for Year 3**
```cypher
MATCH (y:Year {year_id: 'Y3'})-[:SUPPORTS_INTERACTION]->(it:InteractionType)
MATCH (y)-[:HAS_CONTENT_GUIDELINE]->(cg:ContentGuideline)
MATCH (y)-[:HAS_PEDAGOGY_PROFILE]->(pp:PedagogyProfile)
RETURN it.name, it.agent_prompt, cg.reading_level, pp.session_structure
```

**Disciplinary skills a programme develops**
```cypher
MATCH (p:Programme {programme_id: 'PROG-Science-KS2'})-[:DEVELOPS_SKILL]->(s:WorkingScientifically)
RETURN s.skill_name, s.strand, s.complexity_level
ORDER BY s.complexity_level
```

**Cross-subject prerequisite chains (KS1 -> KS3)**
```cypher
MATCH path = (start:Concept)-[:PREREQUISITE_OF*]->(end:Concept)
WHERE start.key_stage = 'KS1' AND end.key_stage = 'KS3'
RETURN path
ORDER BY length(path) DESC
LIMIT 5
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

More CASE comparison queries in `layers/case-standards/docs/CASE_GRAPH_MODEL_v3.5.md`.

## Repository layout

The project is organized into **layers** -- each layer is a self-contained module with its own import scripts, data extractions, and documentation. Layers can be imported independently or removed cleanly.

```
layers/                          Layer-based organization
  uk-curriculum/                 Foundation layer: UK National Curriculum (KS1-KS4)
    scripts/
      import_curriculum.py
      import_thinking_lenses.py
      generate_concept_clusters.py
      enrich_grouping_signals.py
      validate_cluster_definitions.py
    data/
      extractions/primary/       KS1-KS2 JSONs (26 files)
      extractions/secondary/     KS3-KS4 JSONs (29 files)
      cluster_definitions/       ConceptCluster JSON definitions per subject
      thinking_lenses/           ThinkingLens definitions
      cross_domain_links/        Cross-domain CO_TEACHES curations
      concept_skill_links/       Concept-level DEVELOPS_SKILL curations
    README.md

  eyfs/                          Early Years Foundation Stage (Reception)
    scripts/import_eyfs.py
    data/extractions/            7 area-of-learning JSONs
    research/                    EYFS statutory framework reference
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

  content-vehicles/              Teaching packs (Content Vehicles)
    scripts/import_content_vehicles.py
    data/                        Curated JSON files per subject/KS
    README.md

  learner-profiles/              Age-appropriate design constraints
    scripts/import_learner_profiles.py
    data/                        InteractionType, Guideline, Profile JSONs
    README.md

  case-standards/                US/International standards comparison
    scripts/import_case_standards_v2.py
    data/extractions/case/
      packages/                  Cached CASE packages
      mappings/                  Cross-layer alignments
    docs/CASE_GRAPH_MODEL_v3.5.md
    README.md

  oak-content/                   Oak National Academy content (skeleton)
    scripts/import_oak_content.py
    README.md

  visualization/                 Neo4j Bloom perspectives
    scripts/apply_formatting.py
    data/bloom/                  Perspective JSON files
    README.md

core/                            Shared infrastructure
  scripts/
    neo4j_config.py              Shared Neo4j configuration
    create_schema.py             Schema constraints/indexes
    validate_schema.py           Graph integrity checks
    validate_extractions.py      JSON validation
    import_all.py                Import orchestrator
  migrations/
    compute_lesson_grouping_signals.py   Enrichment: teaching_weight, CO_TEACHES
    create_cross_domain_co_teaches.py    Cross-domain CO_TEACHES from curated JSONs
    create_concept_skill_links.py        Concept-level DEVELOPS_SKILL links
  compliance/
    DATA_CLASSIFICATION.md       What data can/cannot be collected
    CONSENT_RULES.md             Consent requirements per purpose
    DPIA.md                      Data Protection Impact Assessment
  docs/
    graph_model_overview.md      Graph model documentation

generated/                       Simulated teacher evaluations
  teachers/                      Query helpers + v1 context/lesson outputs
    graph_query_helper.py        Generates curriculum context from Neo4j
    query_cluster_context.py     Generates cluster-level teaching context
  teachers-v2/                   v3 graph: 5 subjects
  teachers-v3/                   v4 graph: 5 teachers, v4_group_report.md
  teachers-v4/                   v5 graph: 5 teachers, v5_group_report.md
  teachers-v5/                   v6 graph: Y3-Y5 full curriculum, v6_group_report.md

docs/                            Research and documentation
  README.md                      Navigation guide
  design/                        Product thinking and design rationale
  analysis/                      Curriculum analysis and extraction reports
  archive/                       Stale/superseded docs preserved for history
  user-stories/
    child-experience/            Child-facing experience narratives
    technical/                   Numbered system behaviour specs
  research/
    SOURCES.md                   Annotated bibliography (18 sources)
    learning-science/            16 papers: KT, motivation, pedagogy, ITS
    interoperability/            CASE spec, xAPI standard
    case-standards/              US comparative standards research
    content-sources/             UK content provider research
    privacy-compliance/          Regulatory research audit trail

CLAUDE.md                        AI agent navigation guide
```

## Privacy & compliance

This platform serves children (age 4-14). Development is governed by the ICO Children's Code, UK GDPR, and the platform's own ethical framework. The core rule: **the AI learns HOW the child learns, not WHO the child is.**

Key compliance documents:
- `core/compliance/DATA_CLASSIFICATION.md` -- mandatory data tier classification
- `core/compliance/CONSENT_RULES.md` -- consent requirements per processing purpose
- `core/compliance/DPIA.md` -- Data Protection Impact Assessment (skeleton)
- `docs/design/CHILD_PROFILE_CONSENT.md` -- full legal and ethical analysis

See `CLAUDE.md` for full privacy rules and prohibited design patterns.

**NEW**: See `CLAUDE.md` for the complete guide to navigating this project, including common tasks, troubleshooting, and layer architecture.
