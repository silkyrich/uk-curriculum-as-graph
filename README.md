# UK Curriculum as a Knowledge Graph

A Neo4j knowledge graph of the England National Curriculum (EYFS through KS4, ages 4-16), with every statutory subject structured as concepts, objectives, domains, prerequisite relationships, disciplinary skills, concept clusters, thinking lenses, difficulty levels, representation stages, delivery readiness classification, and per-subject teaching ontologies. Built as the curriculum ontology layer for an adaptive learning platform.

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
| CO_TEACHES | 1,892 rels | Co-teachability signal between concepts |
| **ThinkingLens** | | **Cross-subject cognitive framing** |
| ThinkingLens nodes | 10 | Patterns, Cause & Effect, Scale, Systems, etc. |
| APPLIES_LENS | 1,222 rels | Ranked lens assignments (~2 per cluster) |
| PROMPT_FOR | 40 rels | Age-banded prompts (10 lenses x 4 KS) |
| **DifficultyLevel** | | **Grounded difficulty tiers** |
| DifficultyLevel nodes | 4,952 | 3-4 levels per concept (entry -> greater_depth / emerging -> mastery) |
| **RepresentationStage** | | **CPA framework (primary maths)** |
| RepresentationStage nodes | ~462 | Concrete-Pictorial-Abstract, 3 stages per concept (Y1-Y6) |
| **Delivery Readiness** | | **AI teachability classification** |
| DeliveryMode nodes | 4 | AI Direct, AI Facilitated, Guided Materials, Specialist Teacher |
| TeachingRequirement nodes | 15 | Atomic pedagogical requirements driving classification |
| DELIVERABLE_VIA | 1,351 rels | Every concept classified (79% AI-addressable) |
| **Per-Subject Ontology** | | **Typed study/unit nodes (v4.2)** |
| Study/unit nodes | 326 | HistoryStudy, GeoStudy, ScienceEnquiry, EnglishUnit, etc. |
| Reference nodes | 255 | GeoPlace, Misconception, Genre, MathsManipulative, etc. |
| VehicleTemplate nodes | 24 | Pedagogical pattern templates with age-banded prompts |
| DELIVERS_VIA | 1,076 rels | Many-to-many concept delivery |
| **Epistemic Skills** | | **Disciplinary skills layer** |
| Epistemic skills | 105 | Across 6 subject types (Working Scientifically, etc.) |
| **Assessment** | | **KS2 test framework layer** |
| Content Domain Codes | 268 | KS2 STA test framework codes (Maths, Reading, GPS) |
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
| Bloom perspectives | 6 | With icons, styleRules, and search templates |

**Total: ~10,675 nodes, ~23,740+ relationships** in Neo4j Aura cloud database.

**Subjects covered (KS1-KS2):** Art & Design, Computing, Design & Technology, English (KS1 + Y3-Y6), Geography, History, Languages, Mathematics (Y1-Y6), Music, Physical Education, Science

**Subjects covered (KS3):** Art & Design, Citizenship, Computing, Design & Technology, English, Geography, History, Languages, Mathematics, Music, Physical Education, Science

**Subjects covered (KS4):** Art & Design, Biology, Business, Chemistry, Citizenship, Computing, Design & Technology, Drama, English Language, English Literature, Food Preparation & Nutrition, Geography, History, Languages (MFL), Mathematics, Media Studies, Music, Physical Education, Physics, Religious Studies

**EYFS (Reception):** Communication & Language, Personal Social & Emotional Development, Physical Development, Literacy, Mathematics, Understanding the World, Expressive Arts & Design

## Graph model (v4.3)

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
                  |     +--[HAS_SUGGESTION]--> HistoryStudy / GeoStudy / ScienceEnquiry / ...
                  |           +--[DELIVERS_VIA {primary}]--> Concept
                  +--[HAS_CONCEPT]--> Concept
                  |                    <--> [PREREQUISITE_OF]
                  |                    <--> [CO_TEACHES]
                  |                    +--[HAS_DIFFICULTY_LEVEL]--> DifficultyLevel
                  |                    +--[HAS_REPRESENTATION_STAGE]--> RepresentationStage
                  |                    +--[DELIVERABLE_VIA {primary, confidence, rationale}]--> DeliveryMode
                  |                    +--[HAS_TEACHING_REQUIREMENT]--> TeachingRequirement
                  +--[DEVELOPS_SKILL]--> WorkingScientifically / ReadingSkill /
                                         HistoricalThinking / GeographicalSkill /
                                         MathematicalReasoning / ComputationalThinking
                                             <--> [PROGRESSION_OF]

ThinkingLens --[PROMPT_FOR {agent_prompt, question_stems}]--> KeyStage
VehicleTemplate --[TEMPLATE_FOR {agent_prompt}]--> KeyStage
TeachingRequirement --[IMPLIES_MINIMUM_MODE]--> DeliveryMode
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

**ThinkingLens** nodes provide cross-subject cognitive framing. 10 lenses adapted from NGSS Crosscutting Concepts + UK-specific frames: Patterns, Cause & Effect, Scale/Proportion/Quantity, Systems & System Models, Energy & Matter, Structure & Function, Stability & Change, Continuity & Change, Perspective & Interpretation, Evidence & Argument. Each lens has a `key_question` and `agent_prompt` for direct LLM instruction. Age-banded prompts via `PROMPT_FOR` relationships to KeyStage.

Every cluster has 1-3 `APPLIES_LENS` relationships with `rank` (1 = primary) and `rationale` explaining why that lens fits that specific cluster.

### Per-subject ontology (v4.2)

Typed study/unit nodes deliver curriculum concepts with rich, subject-specific metadata. Each subject has its own node label and property schema:

- **HistoryStudy** -- sources, key figures, perspectives, chronological sequencing
- **GeoStudy** -- places, contrasting localities, data points, fieldwork
- **ScienceEnquiry** -- enquiry type, variables, equipment, misconceptions
- **EnglishUnit** -- genre, set texts, grammar focus, writing outcome
- **ArtTopicSuggestion / MusicTopicSuggestion / DTTopicSuggestion / ComputingTopicSuggestion** -- foundation subjects
- **TopicSuggestion** -- generic (RE, Citizenship, etc.)

Many-to-many via `DELIVERS_VIA`: one study delivers multiple concepts, one concept can be delivered by multiple studies. **VehicleTemplate** nodes provide 24 reusable pedagogical patterns with age-banded `agent_prompt` per KeyStage.

### Difficulty levels and representation stages

**DifficultyLevel** nodes provide grounded difficulty tiers per concept. Primary uses entry/developing/expected/greater_depth (4 levels); secondary uses emerging/developing/secure/mastery (4 levels); EYFS uses 3 levels. Each node has `description`, `example_task`, `example_response`, `common_errors`.

**RepresentationStage** nodes model the CPA (Concrete-Pictorial-Abstract) progression for primary maths (Y1-Y6). Each node has `description`, `resources`, `example_activity`, and `transition_cue` describing observable readiness behaviour.

### Delivery readiness

Every concept is classified by what combination of AI, human facilitation, and specialist expertise is needed to teach it. 4 delivery modes: AI Direct (59.5%), AI Facilitated (19.5%), Guided Materials (10.4%), Specialist Teacher (10.7%). **79% of concepts are AI-addressable** (AI Direct + AI Facilitated).

### Node properties (key fields)

**Concept**
- `concept_id`, `concept_name`, `concept_type` (`knowledge` | `skill` | `process` | `attitude` | `content`)
- `teaching_weight` (1-6), `is_keystone`, `prerequisite_fan_out`
- `description`, `teaching_guidance`, `common_misconceptions`, `key_vocabulary`

**ConceptCluster**
- `cluster_id`, `name`, `cluster_type` (`introduction` | `practice`)
- `is_keystone`, `teaching_weight`, `thinking_lens_primary`
- `teaching_guidance`, `common_misconceptions`

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

### US Academic Standards (CASE layer)
CASE (IMS Global Competencies and Academic Standards Exchange) packages from:

- [OpenSALT](https://opensalt.net) -- public CASE server (NGSS, Common Core Math)
- NGSS: Next Generation Science Standards (Achieve Inc, 2013)
- Common Core State Standards for Mathematics (CCSSO, 2010)

## Prerequisites

- Python 3.10+
- Neo4j 5.x (local or cloud -- Neo4j Aura Free works perfectly)
- Python dependencies: `pip install -r requirements.txt`

## Setup and import

### 1. Configure Neo4j connection

Set environment variables (use your Neo4j Aura credentials or local instance):

```bash
export NEO4J_URI="neo4j+s://xxxxx.databases.neo4j.io"  # or neo4j://127.0.0.1:7687 for local
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your-password-here"
```

### 2. Create schema and import all layers

```bash
python3 core/scripts/create_schema.py
python3 core/scripts/import_all.py
```

The orchestrator (`import_all.py`) handles dependency order automatically. Use `--skip-case` or `--skip-oak` to exclude optional layers. See `CLAUDE.md` for the full manual import sequence.

### 3. Validate the graph

```bash
python3 core/scripts/validate_schema.py
```

### 4. Generate teacher planners (optional)

```bash
python3 scripts/generate_all_planners.py --all
```

Generates markdown, PPTX, and DOCX planners for all study nodes. See `justfile` for convenience recipes (`just generate`, `just generate-md`, etc.).

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

**Lesson sequence for a domain (concept clusters + thinking lenses)**
```cypher
MATCH (d:Domain {domain_id: 'MA-Y3-D001'})-[:HAS_CLUSTER]->(cc:ConceptCluster)
OPTIONAL MATCH (cc)-[:SEQUENCED_AFTER]->(prev:ConceptCluster)
OPTIONAL MATCH (cc)-[:APPLIES_LENS {rank: 1}]->(lens:ThinkingLens)
RETURN cc.name, cc.cluster_type, prev.name AS after, lens.name AS thinking_lens
ORDER BY cc.cluster_id
```

**Study nodes for a domain (per-subject ontology)**
```cypher
MATCH (d:Domain {domain_id: 'HI-KS2-D001'})-[:HAS_SUGGESTION]->(s:HistoryStudy)
OPTIONAL MATCH (s)-[:DELIVERS_VIA]->(c:Concept)
RETURN s.name, s.period, s.key_question, collect(c.concept_name) AS concepts
```

**Difficulty levels for a concept**
```cypher
MATCH (c:Concept {concept_id: 'MA-Y3-C014'})-[:HAS_DIFFICULTY_LEVEL]->(dl:DifficultyLevel)
RETURN dl.label, dl.description, dl.example_task, dl.example_response
ORDER BY dl.level_number
```

**Delivery mode classification for a subject**
```cypher
MATCH (p:Programme {programme_id: 'PROG-Mathematics-Y3'})-[:HAS_DOMAIN]->(d:Domain)
      -[:HAS_CONCEPT]->(c:Concept)-[dv:DELIVERABLE_VIA {primary: true}]->(dm:DeliveryMode)
RETURN dm.name, count(c) AS concept_count
ORDER BY concept_count DESC
```

**Age-appropriate interaction types for Year 3**
```cypher
MATCH (y:Year {year_id: 'Y3'})-[:SUPPORTS_INTERACTION]->(it:InteractionType)
MATCH (y)-[:HAS_CONTENT_GUIDELINE]->(cg:ContentGuideline)
MATCH (y)-[:HAS_PEDAGOGY_PROFILE]->(pp:PedagogyProfile)
RETURN it.name, it.agent_prompt, cg.reading_level, pp.session_structure
```

More CASE comparison queries in `layers/case-standards/docs/CASE_GRAPH_MODEL_v3.5.md`.

## Repository layout

The project is organized into **layers** -- each layer is a self-contained module with its own import scripts, data, and documentation.

```
layers/                          Layer-based organization
  uk-curriculum/                 Foundation layer: UK National Curriculum (KS1-KS4)
    scripts/                     Import, enrichment, generation, and validation scripts
    data/
      extractions/primary/       KS1-KS2 JSONs (26 files)
      extractions/secondary/     KS3-KS4 JSONs (29 files)
      cluster_definitions/       ConceptCluster JSON definitions per subject
      thinking_lenses/           ThinkingLens + age-banded prompt definitions
      difficulty_levels/         DifficultyLevel JSONs (148 files, per domain)
      representation_stages/     RepresentationStage JSONs (12 files, primary maths)
      delivery_modes/            DeliveryMode classification JSONs (62 files)
      cross_domain_links/        Cross-domain CO_TEACHES curations
      concept_skill_links/       Concept-level DEVELOPS_SKILL curations

  eyfs/                          Early Years Foundation Stage (Reception)
  assessment/                    KS2 Test Frameworks
  epistemic-skills/              Disciplinary skills (6 subject types)
  topic-suggestions/             Per-subject ontology: typed study nodes + vehicle templates
  learner-profiles/              Age-appropriate design constraints
  case-standards/                US/International standards comparison (NGSS, Common Core)
  visualization/                 Neo4j Bloom perspectives
  oak-content/                   Oak National Academy content (skeleton)

core/                            Shared infrastructure
  scripts/                       Schema, validation, config, import orchestrator
  migrations/                    Rerunnable enrichment scripts
  compliance/                    Data classification, consent rules, DPIA

scripts/                         Output generation (teacher planners)
generated/                       Generated output (teacher-planners/, teacher reviews)
docs/                            Research and documentation
```

## Layer documentation

Each layer has its own detailed README:
- `layers/uk-curriculum/README.md` -- UK National Curriculum foundation
- `layers/eyfs/README.md` -- Early Years Foundation Stage (Reception)
- `layers/assessment/README.md` -- KS2 test frameworks
- `layers/epistemic-skills/README.md` -- Disciplinary thinking skills
- `layers/topic-suggestions/README.md` -- Per-subject ontology (typed study nodes + vehicle templates)
- `layers/learner-profiles/README.md` -- Age-appropriate design layer + agent query patterns
- `layers/case-standards/README.md` -- US/international standards comparison
- `layers/visualization/README.md` -- Neo4j Bloom perspectives

**Quick reference**: See `CLAUDE.md` for the complete guide to project architecture, import pipeline, and common tasks.

## Privacy & compliance

This platform serves children (age 4-14). Development is governed by the ICO Children's Code, UK GDPR, and the platform's own ethical framework. The core rule: **the AI learns HOW the child learns, not WHO the child is.**

Key compliance documents:
- `core/compliance/DATA_CLASSIFICATION.md` -- mandatory data tier classification
- `core/compliance/CONSENT_RULES.md` -- consent requirements per processing purpose
- `core/compliance/DPIA.md` -- Data Protection Impact Assessment (skeleton)
- `docs/design/CHILD_PROFILE_CONSENT.md` -- full legal and ethical analysis

See `CLAUDE.md` for full privacy rules and prohibited design patterns.
