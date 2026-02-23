# UK Curriculum Knowledge Graph - AI Agent Guide

**For: Claude, Cursor, GitHub Copilot, or any AI working on this project**

## What This Is

A **multi-layer knowledge graph** comparing UK National Curriculum with US standards (NGSS, Common Core) and content providers (Oak National Academy). Built in Neo4j, designed for curriculum research and adaptive learning systems.

**Main use case**: Understand curriculum structure, compare international standards, map learning progressions, and generate age-appropriate AI lessons via graph queries.

**Regulatory context**: This platform serves children (age 5-14). All development is governed by the ICO Children's Code (Age Appropriate Design Code), UK GDPR, and the platform's own ethical framework. See **Privacy & Compliance** section below.

---

## Project Architecture (Layer-Based)

Each **layer** is self-contained with its own:
- `extractions/` - Source data (JSON)
- `scripts/` - Import scripts
- `docs/` - Documentation
- `research/` - Background research

### Core Layers (in dependency order)

0. **`layers/eyfs/`** - Early Years Foundation Stage (Reception, age 4-5)
   - Pre-KS1 layer — must be imported *after* UK curriculum so EYFS→KS1 prerequisites can resolve
   - 7 Areas of Learning, 17 Early Learning Goals, 53 concepts, 69 prerequisites (34 cross-stage EYFS→KS1)
   - EYFS Year node (year_id: `'EYFS'`, year_number: 0) linked to KS1 via `PRECEDES`
   - Script: `layers/eyfs/scripts/import_eyfs.py`

1. **`layers/uk-curriculum/`** - UK National Curriculum (2014)
   - Foundation layer - everything else builds on this
   - 1,278+ concepts, 1,559+ objectives, 316 domains across 55 subjects (KS1–KS4)
   - 1,354 prerequisite relationships (cross-KS aware via two-pass import)
   - Script: `import_curriculum.py`

2. **`layers/assessment/`** - KS2 Test Frameworks
   - Links to UK curriculum concepts
   - 268 content domain codes
   - Script: `import_test_frameworks.py`

3. **`layers/epistemic-skills/`** - Disciplinary thinking skills
   - Working Scientifically, Mathematical Reasoning, etc.
   - 105 skills across 6 types
   - Script: `import_epistemic_skills.py`

4. **`layers/topics/`** - Topic layer (History, Geography)
   - 55 topics
   - Script: `import_topics.py`

5. **`layers/content-vehicles/`** - Teaching packs (Content Vehicles)
   - Choosable teaching packs that deliver curriculum concepts with rich metadata
   - ~60 pilot vehicles across 7 subject/KS combinations (History, Geography, Science, English, Maths)
   - Vehicle types: `topic_study`, `case_study`, `investigation`, `text_study`, `worked_example_set`
   - Many-to-many: vehicles deliver concepts, teachers choose between packs
   - Script: `import_content_vehicles.py`

6. **`layers/case-standards/`** - US CASE standards (NGSS, Common Core)
   - **Independent layer** - can be removed without affecting UK layers
   - NGSS 3D model: 8 practices, 41 core ideas, 208 performance expectations
   - Script: `import_case_standards_v2.py`

7. **`layers/learner-profiles/`** - Age-appropriate design constraints
   - Depends on UK curriculum (links from Year nodes)
   - 33 InteractionTypes + 11 each of ContentGuideline, PedagogyProfile, FeedbackProfile + 5 PedagogyTechniques
   - Each node has an `agent_prompt` or `how_to_implement` property for direct LLM instruction
   - InteractionType PRECEDES chain encodes the interface curriculum (voice → text → analysis)
   - PedagogyTechnique REQUIRES chain encodes the pedagogy curriculum (spacing → interleaving → ...)
   - Cross-layer: InteractionType -[:SUPPORTS_LEARNING_OF]-> Subject
   - Script: `import_learner_profiles.py`

8. **Concept Grouping** (derived layer, lives within `layers/uk-curriculum/`)
   - Depends on UK curriculum (enrichment signals on Concept nodes + generated ConceptCluster nodes)
   - Enrichment: `teaching_weight` (1-6), `co_teach_hints`, `is_keystone`, `prerequisite_fan_out` on Concept nodes
   - `CO_TEACHES` relationships between co-teachable concepts (extracted + inferred inverse pairs)
   - 626 `ConceptCluster` nodes: sits between Domain and Concept, following the CC Math Cluster pattern
   - Cluster types: `introduction` (first exposure) and `practice` (fluency/application)
   - `SEQUENCED_AFTER` chains encode lesson ordering within each domain
   - `thinking_lens_primary` convenience property on each cluster; full lens options via `APPLIES_LENS` rels
   - Scripts: `enrich_grouping_signals.py` (JSONs), `compute_lesson_grouping_signals.py` (migration), `generate_concept_clusters.py` (cluster generation), `validate_cluster_definitions.py`

8. **ThinkingLens** (derived layer, lives within `layers/uk-curriculum/`)
   - 10 cross-subject cognitive lenses adapted from NGSS CCCs + UK-specific frames
   - Each lens has `description`, `key_question`, and `agent_prompt` for direct LLM instruction
   - `APPLIES_LENS {rank, rationale}` relationships from every ConceptCluster (1,222 total, ~2 per cluster)
   - `rank=1` = primary recommendation; higher ranks = valid alternative framings
   - The rationale on each rel explains *why* the lens fits *this specific cluster* — not just the topic name
   - `PROMPT_FOR {agent_prompt, question_stems}` relationships to KeyStage (40 total: 10 lenses × 4 KS)
   - Age-banded prompts: query scripts use `coalesce(pf.agent_prompt, tl.agent_prompt)` for backward-compatible fallback
   - Definitions: `layers/uk-curriculum/data/thinking_lenses/thinking_lenses.json`
   - Age-banded prompts: `layers/uk-curriculum/data/thinking_lenses/thinking_lens_ks_prompts.json`
   - Import: `layers/uk-curriculum/scripts/import_thinking_lenses.py`
   - Surfaced by `query_cluster_context.py` in the `## Thinking lenses` section

9. **`layers/oak-content/`** - Oak National Academy (future)
   - Content provider mapping
   - Script: `import_oak_content.py`

### Shared Infrastructure

- **`core/scripts/`** - Schema, validation, config shared across all layers
- **`core/migrations/`** - Database migrations (add properties, fix data)
- **`core/compliance/`** - Data classification, consent rules, DPIA (see Privacy & Compliance below)
- **`layers/visualization/`** - Bloom perspectives, display property formatting

---

## Quick Start

### 1. Set up Neo4j connection
```bash
# For local Neo4j:
export NEO4J_URI='neo4j://127.0.0.1:7687'
export NEO4J_USERNAME='neo4j'
export NEO4J_PASSWORD='password123'

# For Aura (cloud):
export NEO4J_URI='neo4j+s://xxxxx.databases.neo4j.io'
export NEO4J_USERNAME='your-username'
export NEO4J_PASSWORD='your-password'
```

### 2. Create schema
```bash
python3 core/scripts/create_schema.py
```

### 3. Import layers (order matters!)
```bash
# Core UK curriculum (required)
python3 layers/uk-curriculum/scripts/import_curriculum.py

# Concept grouping signals (run after curriculum import)
python3 core/migrations/compute_lesson_grouping_signals.py

# ThinkingLens nodes + PROMPT_FOR age-banded prompts (must run before cluster generation)
python3 layers/uk-curriculum/scripts/import_thinking_lenses.py
python3 layers/uk-curriculum/scripts/generate_concept_clusters.py

# DifficultyLevel nodes (run after curriculum import — pilot: Y3 Maths)
python3 layers/uk-curriculum/scripts/import_difficulty_levels.py

# Cross-domain CO_TEACHES (run after concept grouping)
python3 core/migrations/create_cross_domain_co_teaches.py

# Concept-level skill integration (run after epistemic skills import)
python3 core/migrations/create_concept_skill_links.py

# Assessment layer (optional, depends on UK)
python3 layers/assessment/scripts/import_test_frameworks.py

# Epistemic skills (optional, depends on UK)
python3 layers/epistemic-skills/scripts/import_epistemic_skills.py

# Topics (optional, depends on UK)
python3 layers/topics/scripts/import_topics.py

# Content vehicles (optional, depends on UK + Topics)
python3 layers/content-vehicles/scripts/import_content_vehicles.py

# CASE standards (optional, independent)
python3 layers/case-standards/scripts/import_case_standards_v2.py --import

# Learner profiles (optional, depends on UK)
python3 layers/learner-profiles/scripts/import_learner_profiles.py

# EYFS (optional, depends on UK — run after curriculum so EYFS→KS1 prereqs resolve)
python3 layers/eyfs/scripts/import_eyfs.py

# Visualization properties (recommended, run last)
python3 layers/visualization/scripts/apply_formatting.py
```

### 4. Validate
```bash
python3 core/scripts/validate_schema.py
```

---

## Common Tasks

### Remove a layer entirely
```bash
# Example: Remove CASE standards
rm -rf layers/case-standards/

# Remove from schema (edit core/scripts/create_schema.py)
# Comment out CASE constraints and indexes

# Reimport without CASE
python3 core/scripts/create_schema.py
# (skip import_case_standards_v2.py)
```

### Add a new layer
1. Create `layers/new-layer/` directory
2. Add `extractions/`, `scripts/`, `docs/`, `research/`
3. Create import script following pattern
4. Add constraints to `core/scripts/create_schema.py`
5. Add validation checks to `core/scripts/validate_schema.py`
6. **Compliance check**: Classify any new data against `core/compliance/DATA_CLASSIFICATION.md` — if it touches learner data, update the DPIA

### Update data for one layer
```bash
# Example: Re-extract UK curriculum
# 1. Update JSONs in layers/uk-curriculum/extractions/
# 2. Clear only UK data in Neo4j:
MATCH (n) WHERE n.display_category = 'UK Curriculum' DETACH DELETE n
# 3. Re-import:
python3 layers/uk-curriculum/scripts/import_curriculum.py
```

---

## Graph Model Overview

### Node Labels (Clean, Single-Type)

**UK Curriculum:**
- `:Curriculum` (root node only)
- `:KeyStage`, `:Year`, `:Subject`, `:Programme`
- `:Domain`, `:Objective`, `:Concept`, `:ConceptCluster`
- `:ThinkingLens` — 10 cross-subject cognitive lenses (Patterns, Cause and Effect, …)
- `:DifficultyLevel` — grounded difficulty tiers per Concept (entry → developing → expected → greater_depth)
- `:Topic`, `:SourceDocument`

**Epistemic Skills:**
- `:WorkingScientifically`, `:ReadingSkill`, `:MathematicalReasoning`
- `:GeographicalSkill`, `:HistoricalThinking`, `:ComputationalThinking`

**Assessment:**
- `:TestFramework`, `:TestPaper`, `:ContentDomainCode`

**CASE Standards:**
- `:Framework`, `:Dimension`, `:Practice`, `:CoreIdea`
- `:CrosscuttingConcept`, `:PerformanceExpectation`, `:GradeBand`

**Content Vehicles:**
- `:ContentVehicle` — teaching packs with resources, definitions, assessment (topic_study, case_study, investigation, text_study, worked_example_set)

**Learner Profiles:**
- `:InteractionType` — 33 UI/pedagogical patterns (phoneme splitter, bus stop division, concept mapper, etc.)
- `:ContentGuideline` — reading level, TTS, vocabulary constraints per Year
- `:PedagogyProfile` — session structure, productive failure, scaffolding per Year
- `:FeedbackProfile` — tone, gamification safety, metacognitive prompts per Year
- `:PedagogyTechnique` — 5 desirable difficulty techniques with evidence base and implementation notes

**NO namespace labels** - Each node has ONE semantic label (e.g., `:Objective`, not `:Curriculum:Objective`)

### Provenance Property

All nodes have `display_category` property:
- `"UK Curriculum"`
- `"CASE Standards"`
- `"Epistemic Skills"`
- `"Assessment"`
- `"Learner Profile"`
- `"Content Vehicle"`
- `"Structure"`

### Key Relationships

```cypher
// UK Curriculum structure (KS1–KS4)
(:Curriculum)-[:HAS_KEY_STAGE]->(:KeyStage)-[:HAS_YEAR]->(:Year)-[:HAS_PROGRAMME]->(:Programme)
(:Programme)-[:HAS_DOMAIN]->(:Domain)-[:CONTAINS]->(:Objective)-[:TEACHES]->(:Concept)
(:Concept)-[:PREREQUISITE_OF]->(:Concept)  // Learning progressions (incl. EYFS→KS1 cross-stage)

// EYFS
(:KeyStage {key_stage_id: 'EYFS'})-[:HAS_YEAR]->(:Year {year_id: 'EYFS', year_number: 0})
(:Year {year_id: 'EYFS'})-[:PRECEDES]->(:Year {year_id: 'Y1'})
// EYFS follows the same Programme→Domain→Objective→Concept hierarchy

// Concept Grouping + ThinkingLens
(:Domain)-[:HAS_CLUSTER]->(:ConceptCluster)-[:GROUPS]->(:Concept)
(:ConceptCluster)-[:SEQUENCED_AFTER]->(:ConceptCluster)               // within-domain lesson ordering
(:Concept)-[:CO_TEACHES]->(:Concept)                                  // co-teachability signal
(:ConceptCluster)-[:APPLIES_LENS {rank: int, rationale: str}]->(:ThinkingLens)  // ordered, 1=primary
(:ThinkingLens)-[:PROMPT_FOR {agent_prompt: str, question_stems: [str]}]->(:KeyStage)  // age-banded prompts

// DifficultyLevel (v3.9) — grounded difficulty tiers replacing complexity_level
(:Concept)-[:HAS_DIFFICULTY_LEVEL]->(:DifficultyLevel)  // 3-4 levels per concept (pilot: Y3 Maths)

// Content Vehicles (v3.8)
(:Domain)-[:HAS_VEHICLE]->(:ContentVehicle)-[:DELIVERS]->(:Concept)
(:ContentVehicle)-[:IMPLEMENTS]->(:Topic)  // optional link to Topics layer

// NGSS 3D model
(:Framework)-[:HAS_DIMENSION]->(:Dimension)-[:HAS_PRACTICE]->(:Practice)
(:Dimension)-[:HAS_CORE_IDEA]->(:CoreIdea)
(:PerformanceExpectation)-[:USES_PRACTICE]->(:Practice)
(:PerformanceExpectation)-[:USES_CORE_IDEA]->(:CoreIdea)

// Cross-layer alignments
(:Practice)-[:ALIGNS_TO]->(:Concept)  // NGSS ↔ UK
(:Programme)-[:DEVELOPS_SKILL]->(:WorkingScientifically)  // UK ↔ Skills (programme level)
(:Concept)-[:DEVELOPS_SKILL]->(:WorkingScientifically)    // UK ↔ Skills (concept level, curated)

// Learner profiles (linked from Year)
(:Year)-[:PRECEDES]->(:Year)                                      // Y1→Y2→...→Y11
(:Year)-[:HAS_CONTENT_GUIDELINE]->(:ContentGuideline)
(:Year)-[:HAS_PEDAGOGY_PROFILE]->(:PedagogyProfile)
(:Year)-[:HAS_FEEDBACK_PROFILE]->(:FeedbackProfile)
(:Year)-[:SUPPORTS_INTERACTION {primary: bool}]->(:InteractionType)
(:InteractionType)-[:PRECEDES]->(:InteractionType)                // interface curriculum
(:InteractionType)-[:SUPPORTS_LEARNING_OF]->(:Subject)           // cross-layer
(:PedagogyProfile)-[:USES_TECHNIQUE]->(:PedagogyTechnique)
(:PedagogyProfile)-[:INTRODUCES_TECHNIQUE]->(:PedagogyTechnique) // first year of introduction
(:PedagogyTechnique)-[:REQUIRES]->(:PedagogyTechnique)           // pedagogy curriculum
```

---

## Privacy & Compliance (Children's Data)

**This section is mandatory reading for anyone building features that touch learner data, session data, parent accounts, or AI interactions.**

### Regulatory Position

We are a **commercial edtech controller** offering a direct-to-parent/child service. We are **in scope** of the ICO Children's Code (all 15 standards). The education exemption does **not** apply to us — it only applies to schools acting as processors.

### The Core Rule

**The AI learns HOW the child learns, not WHO the child is.**

Every data element must pass this test: "Is this necessary to make a better pedagogical decision?" If no, don't collect it.

### Data Tiers (Mandatory Classification)

Any new data element introduced anywhere in the platform must be classified into one of these tiers. See `core/compliance/DATA_CLASSIFICATION.md` for the full specification.

| Tier | What | Where Stored | Example |
|---|---|---|---|
| **0: Identity** | Account data | Separate identity service, NEVER in event log | Parent email, child first name, year group |
| **1: Learning Events** | Pseudonymous interaction data | Event store (UUID, no names) | Attempt result, response time, error pattern, concept ID |
| **2: Derived Model** | Computed from Tier 1 (not stored independently) | Runtime projection | Mastery probability, spacing interval, scaffold preference |
| **3: Aggregated** | Anonymised population data (1000+ minimum) | Analytics store | Common misconceptions per concept |
| **PROHIBITED** | Never collected under any circumstances | Nowhere | Emotional state, interests, personal disclosures, device fingerprints |

### Consent Architecture

Consent must be **specific** and **unbundled** (separate toggles per purpose):

| Purpose | Required for service? | Default | Lawful Basis |
|---|---|---|---|
| Core adaptive learning | Yes | Off until consented | Parental consent (Art. 6(1)(a) + Art. 8) |
| Teacher sharing | No | Off | Parental consent |
| Anonymised analytics | No | Off | Parental consent |
| Camera/microphone | No | Off, per activity | Parental consent |
| Anomaly detection (safety) | Active while service is active | On | Legitimate interests (Art. 6(1)(f)) |

### Profiling Justification

Adaptive learning **is** profiling under the Children's Code. Standard 12 says profiling must be off by default. Our compelling reason: knowledge tracing is core to the service, personalised instruction is in the child's best interests (evidence-based), all content is curriculum-grounded (no harmful content risk), and full parent transparency/control is provided.

### Key Compliance Documents

| Document | Purpose | Status |
|---|---|---|
| `core/compliance/DATA_CLASSIFICATION.md` | What data can/cannot be collected — the developer reference | Active |
| `core/compliance/CONSENT_RULES.md` | Consent requirements per processing purpose | Active |
| `core/compliance/DPIA.md` | Data Protection Impact Assessment (ICO Annex D) | Skeleton — needs completion before launch |
| `docs/design/CHILD_PROFILE_CONSENT.md` | Full legal and ethical analysis | Reference |
| `docs/research/privacy-compliance/` | Source audit trail for all regulatory research | Reference |

### Compliance in Development Workflow

Every feature that introduces or modifies data processing must:
1. Classify all data elements against `DATA_CLASSIFICATION.md`
2. Confirm consent basis against `CONSENT_RULES.md`
3. Update the DPIA if processing changes
4. Include a privacy boundary section in any user story

---

## Where to Find Things

**Want to work on...**

- EYFS / Reception / nursery content? → `layers/eyfs/` (extraction + import), `docs/design/PLAN_EYFS_INTEGRATION.md` (design)
- UK curriculum extraction? → `layers/uk-curriculum/`
- NGSS structure? → `layers/case-standards/docs/CASE_GRAPH_MODEL_v3.5.md`
- Visualization / Bloom perspectives? → `layers/visualization/`
- Age-appropriate design / learner profiles? → `layers/learner-profiles/`
- Content vehicles / teaching packs? → `layers/content-vehicles/`
- Teacher review findings / lesson plans? → `generated/teachers-v4/` (V5 review), `generated/teachers-v3/` (V4 review)
  - **`generated/` is TEST output, not canon** — do not treat its contents as authoritative for graph model or data decisions
- Concept grouping / lesson clusters? → `layers/uk-curriculum/scripts/generate_concept_clusters.py`
- Thinking lenses (cognitive framing for clusters)? → `layers/uk-curriculum/data/thinking_lenses/` + `import_thinking_lenses.py`
- Difficulty levels (grounded difficulty tiers)? → `layers/uk-curriculum/data/difficulty_levels/` + `import_difficulty_levels.py`
- User stories? → `docs/user-stories/`
- Schema definition? → `core/scripts/create_schema.py`
- Import all data? → `core/scripts/import_all.py` (orchestrator)
- **Privacy & data rules?** → `core/compliance/` (start here for any learner data question)
- **Consent architecture?** → `docs/design/CHILD_PROFILE_CONSENT.md`

**Confused about...**

- Graph model? → This file (see Graph Model Overview section above)
- Layer architecture? → This file (CLAUDE.md)
- Specific layer? → `layers/{layer-name}/README.md`
- Learner profile queries? → `layers/learner-profiles/README.md`
- **What data you can collect?** → `core/compliance/DATA_CLASSIFICATION.md`
- **What needs consent?** → `core/compliance/CONSENT_RULES.md`

---

## Important Conventions

### File Naming
- Extractions: `{subject}_{key_stage}.json`
- Scripts: `import_{layer}.py`
- Docs: `{TOPIC}.md` (uppercase for main docs)

### Node IDs
- UK: `EN-Y5-O021` (Subject-Year-Type-Number)
- Clusters: `MA-Y3-CL001` (Subject-Year-CL-Number)
- CASE: `ngss-sep-1` (framework-type-number)
- Always unique, never reused

### Properties ALL nodes must have
- `name` (for visualization)
- `display_category` (for provenance)
- `display_color`, `display_icon` (for Bloom styling)

### Import Script Pattern
```python
from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

class LayerImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def import_data(self):
        # Load JSON
        # Create nodes (NO namespace labels!)
        # Create relationships
        # Track stats
```

---

## Troubleshooting

**Import fails with constraint violation**
- Run `core/scripts/create_schema.py` first
- Check for duplicate IDs in JSON files

**Nodes show blank in Neo4j Browser**
- All nodes require a `name` property — check the import script set it during MERGE/SET
- Re-run the relevant import script; `name` is set on all nodes by current import scripts

**Can't find a script**
- Check `layers/{layer}/scripts/` not root `scripts/`
- Use layer-based organization

**CASE queries don't work**
- Read `layers/case-standards/docs/CASE_GRAPH_MODEL_v3.5.md`
- CASE uses different node types than UK curriculum

**Learner profile relationships missing**
- Run `python3 layers/learner-profiles/scripts/import_learner_profiles.py`
- Year nodes link via `year_id` property (e.g. `"Y3"`), not `year_code`

---

## Development Workflow

### Graph Layer Development
1. **Research** → `layers/{layer}/research/`
2. **Extract** → Create JSONs in `layers/{layer}/extractions/`
3. **Validate** → Run `core/scripts/validate_extractions.py`
4. **Import** → Run `layers/{layer}/scripts/import_{layer}.py`
5. **Verify** → Run `core/scripts/validate_schema.py`
6. **Document** → Update `layers/{layer}/README.md`
7. **Commit** → Git commit with clear message

### Feature / Application Development (Touches Learner Data)
1. **Classify data** → Check every new data element against `core/compliance/DATA_CLASSIFICATION.md`
2. **Check consent** → Confirm lawful basis in `core/compliance/CONSENT_RULES.md`
3. **Design** → Include privacy boundary section (what is/isn't stored, retention, deletion)
4. **Build** → Enforce Tier 0/1 separation (identity never in event log)
5. **Test** → Verify no PII leaks into event log, LLM prompts, or analytics
6. **Update DPIA** → If processing has changed, update `core/compliance/DPIA.md`
7. **Document** → User story with compliance checklist completed
8. **Commit** → Git commit with clear message

---

## Current State (2026-02-23)

✅ **Documentation reorganised:**
- 61 docs sorted into semantic subdirectories (`design/`, `analysis/`, `archive/`, `user-stories/`, `research/learning-science/`, `research/interoperability/`)
- `docs/README.md` added as navigation guide
- CASE graph model moved to its layer (`layers/case-standards/docs/`)
- `STATUS.md` archived; `migrations/legacy_scripts_README.md` archived

✅ **KS4 fully extracted and imported:**
- 17 new KS4 JSON extraction files in `layers/uk-curriculum/data/extractions/secondary/`
- Subjects: English Language, English Literature, Mathematics, Biology, Chemistry, Physics, History, Geography, Art & Design, Music, Drama, Design & Technology, Languages (MFL), Religious Studies, Business, Food Preparation & Nutrition, Media Studies
- Plus 3 existing KS3-4 combined programmes: Citizenship, Computing, Physical Education

✅ **Complete layers:**
- UK National Curriculum (55 subjects, 316 domains, 1,559+ objectives, 1,278+ concepts — KS1–KS4, 1,354+ prerequisites)
  - Two-pass import: nodes in pass 1, all PREREQUISITE_OF in pass 2 (cross-KS links resolve correctly)
  - Enriched: D&T KS1-KS4 concepts added; History disciplinary objectives filled; Y6 Maths/English concepts added for KS3 prerequisite links
  - Quality fixes: concept_type normalisation, Art KS4 prefix (AD- not ART-), Languages KS4 subject name consistency
- Assessment (KS2 test frameworks)
- Epistemic Skills
- Topics
- CASE Standards (NGSS + Common Core Math)
- Learner Profiles (71 nodes — 33 InteractionType, 11 ContentGuideline, 11 PedagogyProfile, 11 FeedbackProfile, 5 PedagogyTechnique)
- Visualization (5 Bloom perspectives with icons, styleRules, and search templates)

✅ **Concept Grouping layer (v3.7, 2026-02-22):**
- Enrichment signals: `teaching_weight` (1-6) and `co_teach_hints` added to all 55 extraction JSONs via `enrich_grouping_signals.py`
- Import: `import_curriculum.py` now imports `teaching_weight` + `co_teach_hints` into Concept nodes
- Migration: `compute_lesson_grouping_signals.py` computes `is_keystone`, `prerequisite_fan_out`, and creates `CO_TEACHES` relationships (extracted + inferred inverse pairs)
- Cluster generation: `generate_concept_clusters.py` creates `ConceptCluster` nodes (two types: introduction, practice)
- Schema: ConceptCluster uniqueness constraint + indexes on `cluster_type`, `is_keystone`, `teaching_weight` (v3.7)
- Validation: 6 new schema checks + extraction checks for new fields; `validate_cluster_definitions.py` validates all cluster definition JSONs
- Visualization: ConceptCluster styled (Indigo-500, view_module icon) + name mapping
- No learner data — all nodes are curriculum design metadata

✅ **ThinkingLens layer (2026-02-23):**
- 10 cross-subject cognitive lenses in `layers/uk-curriculum/data/thinking_lenses/thinking_lenses.json`
- Adapted from NGSS CCCs + UK-specific frames: Patterns, Cause & Effect, Scale/Proportion/Quantity, Systems & System Models, Energy & Matter, Structure & Function, Stability & Change, Continuity & Change, Perspective & Interpretation, Evidence & Argument
- Each lens has `description`, `key_question`, `agent_prompt` for direct LLM instruction; `display_color = '#7C3AED'`
- All 626 cluster definition clusters enriched with `thinking_lenses` arrays (1-3 lenses each, ordered by fit, with per-lens rationale)
- `validate_cluster_definitions.py` enforces `VALID_THINKING_LENSES` set and requires non-empty rationale on each lens entry
- `generate_concept_clusters.py` writes `thinking_lens_primary` property + `APPLIES_LENS {rank, rationale}` relationships
- **40 PROMPT_FOR relationships** (10 lenses × 4 KS) with age-banded `agent_prompt` and `question_stems`
- `thinking_lens_ks_prompts.json`: KS1 uses concrete/observable language, KS4 uses formal analytical vocabulary
- `query_cluster_context.py` and `graph_query_helper.py` use `coalesce(pf.agent_prompt, tl.agent_prompt)` — backward-compatible fallback
- `validate_schema.py`: 2 new checks — PROMPT_FOR coverage (4 per lens) and PROMPT_FOR completeness (non-empty properties)
- No learner data — pure curriculum metadata

✅ **EYFS layer (2026-02-23):**
- 7 Areas of Learning as Subjects: Communication and Language, PSED, Physical Development, Literacy, Mathematics, Understanding the World, Expressive Arts and Design
- 1 KeyStage (EYFS), 1 Year node (year_id: `'EYFS'`, year_number: 0, age_range: `'4-5'`)
- 17 domains (one per ELG), 51 objectives, 53 concepts
- 69 PREREQUISITE_OF relationships: 35 within-EYFS + 34 cross-stage EYFS→KS1 (English, Maths, Science, History, Geography, Art, Music, DT)
- EYFS Year -[:PRECEDES]-> Y1 — completes the progression chain from Reception to Year 11
- Import script: `layers/eyfs/scripts/import_eyfs.py`

✅ **In Aura cloud database — all layers active (2026-02-23):**
- Instance: education-graphs (6981841e)
- **~4,900+ total nodes** including ConceptClusters, ThinkingLens, EYFS, and ContentVehicle nodes
- 61 ContentVehicle nodes; 217 DELIVERS + 92 HAS_VEHICLE + 24 IMPLEMENTS relationships
- 10 ThinkingLens nodes; 1,222 APPLIES_LENS relationships (~2 per cluster on average); 40 PROMPT_FOR relationships (age-banded prompts)
- 626 ConceptCluster nodes (167 introduction, 459 practice) — all with `thinking_lens_primary`
- 1,351 Concept nodes enriched with `teaching_weight` + `co_teach_hints`
- 53 EYFS Concept nodes; 34 EYFS→KS1 cross-stage prerequisites
- 1,827 CO_TEACHES relationships (extracted + inferred inverse-operation pairs)
- Visualization properties applied (display_color, display_icon, name) — Year nodes labelled "Year 1"…"Year 11"
- 5 Bloom perspectives uploaded and active

✅ **Dead migration scripts removed (2026-02-22):**
- `core/migrations/fix_ks4_programme_metadata.py` — one-time KS4 metadata fix, already applied
- `core/migrations/remove_flat_year_metadata.py` — one-time cleanup of superseded Year properties, already applied
- `layers/uk-curriculum/scripts/add_year_metadata.py` — original flat-metadata script, superseded by learner-profiles layer
- `core/migrations/` now contains only the 3 active rerunnable migrations: `compute_lesson_grouping_signals.py`, `create_cross_domain_co_teaches.py`, `create_concept_skill_links.py`

✅ **All extraction gaps filled (2026-02-22):**
- **0 domains with no concepts** across all 315 domains, KS1–KS4
- Geography place knowledge KS1-KS3, Languages reading/writing/listening KS2-KS4 filled
- MA-Y5 addition/subtraction + statistics domains fixed (missing domain_id assignments)
- GE-KS3 geographical skills, Chemistry analysis, Business operations, Media contexts, RS practices filled

✅ **Compliance framework (2026-02-20):**
- Data classification spec (`core/compliance/DATA_CLASSIFICATION.md`)
- Consent rules spec (`core/compliance/CONSENT_RULES.md`)
- DPIA skeleton (`core/compliance/DPIA.md`) — needs completion before launch
- Full legal/ethical analysis (`docs/design/CHILD_PROFILE_CONSENT.md`)
- Regulatory research audit trail (`docs/research/privacy-compliance/`)
- CLAUDE.md updated with compliance as first-class development concern

✅ **Cross-domain CO_TEACHES (2026-02-22):**
- 48 curated within-subject cross-domain links (maths, english, science, humanities, arts, applied)
- 18 curated cross-subject links (Science↔Maths, Science↔English, Geography↔History, English↔History)
- Migration: `create_cross_domain_co_teaches.py` loads from `layers/uk-curriculum/data/cross_domain_links/*.json`
- Validator: curated cross-domain = PASS, extracted cross-domain = WARN

✅ **Concept-level DEVELOPS_SKILL integration (2026-02-22):**
- 34 Science concept→WorkingScientifically links (KS2 + KS3, with enquiry_type tags)
- 18 Geography concept→GeographicalSkill links (KS2 + KS3)
- 18 History concept→HistoricalThinking links (KS2 + KS3)
- Migration: `create_concept_skill_links.py` loads from `layers/uk-curriculum/data/concept_skill_links/*.json`
- Complements existing Programme→Skill links with concept granularity
- Validator: check_concept_skill_links_completeness added

✅ **Content Vehicles layer (v3.8, 2026-02-23):**
- 61 ContentVehicle nodes across 7 subject/KS combinations, 217 DELIVERS rels, 92 HAS_VEHICLE, 24 IMPLEMENTS
- Vehicle types: `topic_study` (History), `case_study` (Geography), `investigation` (Science), `text_study` (English), `worked_example_set` (Maths)
- Subject-specific properties: sources/perspectives (History), data_points/themes (Geography), equipment/enquiry_type (Science), genre/grammar_focus (English), manipulatives/CPA stage (Maths)
- DELIVERS relationship (many-to-many): vehicles deliver concepts, concepts can be delivered by multiple vehicles
- HAS_VEHICLE from Domain (inferred), IMPLEMENTS to Topic (optional)
- Schema: ContentVehicle uniqueness constraint + indexes on vehicle_type, subject, key_stage (v3.8)
- Validation: 4 new checks (completeness, DELIVERS coverage, assessment_guidance, definitions)
- Query helpers: `graph_query_helper.py` surfaces vehicles + ThinkingLens per domain; `query_cluster_context.py` surfaces lenses per cluster
- V5 teacher review (2026-02-23): content readiness nearly doubled (avg 3.7→6.6/10); data errors found and fixed
- No learner data — all nodes are curriculum design metadata

✅ **V5 teacher review (2026-02-23):**
- 5 simulated teacher personas reviewed the graph with Content Vehicles + Thinking Lenses
- Team: Henderson (Y2 Maths), Okonkwo (Y4 English), Kapoor (Y5 Science), Osei (KS3 Biology), Adeyemi (KS3 Geography/History)
- Average content generation readiness: **6.6/10** (up from 3.7/10 in V4)
- Average structure rating: **7.8/10** (up from 6.7/10 in V4)
- Data errors found and fixed: 6 KS3 Science vehicles had wrong concept IDs (systematic domain offset), 3 KS2 Science vehicles mixed WS concepts into delivers, EN-Y4-CV004 had wrong book recommendation (baby book for Y4)
- Remaining consensus gaps: no worked examples, no difficulty sub-levels, incomplete vehicle coverage (~40% Geography statutory content missing), thin safety notes, Thinking Lens rationales age-inappropriate for KS1 and duplicated across clusters
- Reports: `generated/teachers-v4/` (lesson plans, teaching logs, v5 findings, group report)
- Path to 9/10: add worked examples, fix data quality, add difficulty sub-levels

✅ **DifficultyLevel layer (v3.9, 2026-02-23):**
- Replaces ungrounded `complexity_level` integer with structured sub-nodes per Concept
- `(:Concept)-[:HAS_DIFFICULTY_LEVEL]->(:DifficultyLevel)` — 3-4 levels per concept
- Standard labels aligned with KS2 statutory assessment: `entry` (1), `developing` (2), `expected` (3), `greater_depth` (4)
- Each node has `description`, `example_task`, `example_response`, `common_errors` — grounding abstract difficulty into concrete, assessable tasks
- Pilot: Y3 Mathematics (41 concepts, ~150 DifficultyLevel nodes)
- Data: `layers/uk-curriculum/data/difficulty_levels/mathematics_y3.json`
- Import: `layers/uk-curriculum/scripts/import_difficulty_levels.py`
- Schema: DifficultyLevel uniqueness constraint + indexes on `level_number`, `label` (v3.9)
- Validation: 5 new checks (completeness, level_number range, label values, HAS_DIFFICULTY_LEVEL integrity, no duplicate levels)
- `complexity_level` property removed from Concept import; `complexity_range` removed from ConceptCluster generation
- Query helpers: `query_cluster_context.py` and `graph_query_helper.py` surface difficulty levels under each concept
- Backward-compatible: non-pilot concepts show no difficulty levels (no errors)
- No learner data — pure curriculum design metadata

🚧 **In progress:**
- Oak National Academy content (skeleton only)
- Alignment mappings (CASE ↔ UK)
- DPIA completion (skeleton exists, needs human review and sign-off)

---

## Key Files to Read First

1. This file (CLAUDE.md) - Architecture overview **including compliance rules**
2. `core/compliance/DATA_CLASSIFICATION.md` - **What data you can and cannot collect**
3. `docs/README.md` - Documentation navigation guide
4. `core/docs/graph_model_overview.md` - Data model
5. `layers/uk-curriculum/README.md` - Core layer
6. `layers/case-standards/docs/CASE_GRAPH_MODEL_v3.5.md` - NGSS structure
7. `layers/learner-profiles/README.md` - Age-appropriate design layer + agent query patterns
8. `docs/design/RESEARCH_BRIEFING.md` - Research briefing and rationale for the learner layer
9. `docs/design/CHILD_PROFILE_CONSENT.md` - Full consent and compliance analysis

---

## Don't Do This

### Architecture
❌ Add namespace labels (`:Curriculum:Objective`) - We removed these for clarity
❌ Hardcode credentials in scripts - Use `neo4j_config.py`
❌ Create generic "CFItem" blobs - Parse structure intelligently
❌ Skip validation - Always run `validate_schema.py`
❌ Mix layer data in scripts - Keep layers self-contained
❌ Add flat age/interaction properties to Year nodes - Use the learner-profiles layer instead
❌ Match Year nodes on `year_code` - the property is `year_id`
❌ Manually create ConceptCluster nodes - Use `generate_concept_clusters.py` (they are derived from graph topology)
❌ Edit `teaching_weight` or `co_teach_hints` directly in the graph - Edit the extraction JSONs, then reimport
❌ Manually create APPLIES_LENS relationships - Edit `thinking_lenses` arrays in the cluster definition JSONs, then re-run `generate_concept_clusters.py`
❌ Import ThinkingLens nodes after cluster generation - ThinkingLens nodes must exist *before* `generate_concept_clusters.py` runs (MATCH fails silently if the node isn't there)

### Privacy & Compliance (Non-Negotiable)
❌ Store child's name, school, or any PII in the learning event log - Identity and events are architecturally separated
❌ Store emotional states, interests, or personal disclosures - Prompt classifier must flag and discard these
❌ Send PII to LLM without processor agreement - Check `CONSENT_RULES.md` before adding anything to prompts
❌ Add engagement-maximising metrics (scroll depth, tap heatmaps, streak counts) - We optimise learning, not engagement
❌ Add gamification that creates extrinsic pressure (badges, leaderboards, progress bars, streaks, loss aversion) - Meta-analyses show net negative effect, especially for introverted learners
❌ Build AI that claims emotional reciprocity ("I missed you", "We're friends", "I was thinking about you") - Creates parasocial dependency; not in child's best interests
❌ Use time-of-day patterns for behavioural profiling or push notifications - Session timestamps for spacing are fine; engagement scheduling is not
❌ Profile for anything other than curriculum-aligned pedagogy - Commercial profiling is prohibited
❌ Collect data without classifying it against `DATA_CLASSIFICATION.md` - Every new data element must be classified
❌ Bundle consent purposes together - Each processing purpose needs its own toggle
❌ Share child data with third parties without explicit per-recipient parent consent
❌ Retain session transcripts beyond 30 days or learning events beyond 12 months
❌ Present mastery predictions to children in ways that could label or stigmatise them

### Permitted Design Choices (Not Prohibited)
✅ Warm, encouraging educational character with personality — a friendly avatar that says "Let's explore fractions!" is fine
✅ Session timestamps, response times, event timestamps — essential for spacing algorithms and session limits
✅ Surprise/delight moments tied to genuine learning milestones — not engagement metrics
✅ Session duration visible to parents — informational, not competitive
✅ Age-appropriate celebratory feedback ("You figured it out!") — not contingent on streaks or return visits

---

**Questions?** Check layer-specific READMEs or ask the human!
