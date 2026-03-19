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

4. **`layers/topic-suggestions/`** - Per-subject ontology (Topic Suggestions + VehicleTemplates)
   - Replaces old Topics + Content Vehicles layers with typed per-subject nodes
   - 388 study/unit nodes across 10 typed labels + 255 reference nodes across 12 types + 24 VehicleTemplate nodes
   - **Study nodes** (display_category: `"Topic Suggestion"`): HistoryStudy, GeoStudy, ScienceEnquiry, EnglishUnit, MathsUnit, ArtTopicSuggestion, MusicTopicSuggestion, DTTopicSuggestion, ComputingTopicSuggestion, TopicSuggestion (generic)
   - **Reference nodes** (display_category: `"Subject Reference"`): DisciplinaryConcept, HistoricalSource, GeoPlace, GeoContrast, EnquiryType, Misconception, Genre, SetText, MathsManipulative, MathsRepresentation, MathsContext, ReasoningPromptType
   - **VehicleTemplate** (display_category: `"Vehicle Template"`): 24 pedagogical pattern templates with TEMPLATE_FOR → KeyStage
   - Each subject uses its own property schema (no irrelevant attributes on nodes)
   - Scripts: `import_vehicle_templates.py`, `import_subject_ontologies.py`
   - Data: `layers/topic-suggestions/data/` (per-subject JSON files)

5. **`layers/case-standards/`** - US CASE standards (NGSS, Common Core)
   - **Independent layer** - can be removed without affecting UK layers
   - NGSS 3D model: 8 practices, 41 core ideas, 208 performance expectations
   - Script: `import_case_standards_v2.py`

6. **`layers/learner-profiles/`** - Age-appropriate design constraints
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

9. **DifficultyLevel** (derived layer, lives within `layers/uk-curriculum/`)
   - 4,952 DifficultyLevel nodes across 1,296 concepts (all EYFS + KS1-KS4)
   - `(:Concept)-[:HAS_DIFFICULTY_LEVEL]->(:DifficultyLevel)` — 3-4 levels per concept
   - **Primary labels** (EYFS + KS1-KS2): `entry` (1), `developing` (2), `expected` (3), `greater_depth` (4)
   - **Secondary labels** (KS3-KS4): `emerging` (1), `developing` (2), `secure` (3), `mastery` (4)
   - EYFS uses 3 levels only (entry/developing/expected) — no greater_depth per developmental framework
   - Each node has `description`, `example_task`, `example_response`, `common_errors`
   - Replaces the ungrounded `complexity_level` integer that teachers flagged as meaningless
   - Data: 148 domain-level JSON files in `layers/uk-curriculum/data/difficulty_levels/`
   - File naming: `{subject}_{year}_{domain}.json` (e.g. `english_y4_composition.json`, `science_ks3_physics_waves.json`)
   - Import: `layers/uk-curriculum/scripts/import_difficulty_levels.py` (idempotent, globs `*.json`)
   - ID format: `{concept_id}-DL{zero-padded level_number}` (e.g. `MA-Y3-C014-DL01`)
   - `display_color = '#F59E0B'` (Amber-500), `display_icon = 'signal_cellular_alt'`

10. **RepresentationStage** (derived layer, lives within `layers/uk-curriculum/`)
   - ~462 RepresentationStage nodes across 154 primary maths concepts (Y1-Y6)
   - `(:Concept)-[:HAS_REPRESENTATION_STAGE]->(:RepresentationStage)` — 3 stages per concept
   - CPA framework: `concrete` (1), `pictorial` (2), `abstract` (3)
   - Each node has `description`, `resources` (string array), `example_activity`, `transition_cue`
   - `transition_cue` describes observable child behaviour indicating readiness to progress
   - Complements DifficultyLevel (RS = representation journey, DL = attainment tiers)
   - Data: 12 JSON files in `layers/uk-curriculum/data/representation_stages/`
   - File naming: `mathematics_y{n}.json` or `mathematics_y3_{domain}.json` (Y3 split by domain)
   - Import: `layers/uk-curriculum/scripts/import_representation_stages.py` (idempotent, globs `*.json`)
   - ID format: `{concept_id}-RS{zero-padded stage_number}` (e.g. `MA-Y3-C014-RS01`)
   - `display_color = '#06B6D4'` (Cyan-500), `display_icon = 'view_carousel'`
   - No learner data — pure curriculum design metadata

11. **Delivery Readiness** (derived layer, lives within `layers/uk-curriculum/`)
   - Classifies every concept by delivery suitability: what combination of AI, human facilitation, and specialist expertise is needed
   - 4 `DeliveryMode` nodes: AI Direct, AI Facilitated, Guided Materials, Specialist Teacher
   - 15 `TeachingRequirement` nodes: atomic pedagogical requirements (Objective Assessment, Physical Manipulatives, Creative Assessment, etc.)
   - `(:Concept)-[:DELIVERABLE_VIA {primary, confidence, rationale}]->(:DeliveryMode)` — 1,351 concepts classified
   - `(:Concept)-[:HAS_TEACHING_REQUIREMENT]->(:TeachingRequirement)` — teaching requirements per concept
   - `(:TeachingRequirement)-[:IMPLIES_MINIMUM_MODE]->(:DeliveryMode)` — structural constraint
   - Classification: 59.5% AI Direct, 19.5% AI Facilitated, 10.4% Guided Materials, 10.7% Specialist Teacher
   - **Platform addressable surface: 79% of all concepts** (AI Direct + AI Facilitated)
   - Classification script: `layers/uk-curriculum/scripts/classify_delivery_modes.py` (rule-based, reads all concept metadata)
   - Import script: `layers/uk-curriculum/scripts/import_delivery_modes.py` (idempotent)
   - Data: 62 per-subject JSON files in `layers/uk-curriculum/data/delivery_modes/`
   - Design doc: `docs/design/PLAN_DELIVERY_MODE_CLASSIFICATION.md`
   - `display_color = '#10B981'` (Emerald-500), `display_icon = 'settings_input_antenna'`
   - No learner data — pure curriculum design metadata

12. **`layers/send-support/`** - SEND Support Layer (v4.4)
   - Models barriers to curriculum access and support strategies, NOT diagnoses
   - 4 `NeedArea` nodes (need_area_id; statutory SEND taxonomy -- reporting only, not execution logic)
   - 16 `AccessRequirement` nodes (access_req_id; task-side access barriers: language_load, working_memory_load, etc.)
   - 20 `SupportStrategy` nodes (support_id; universal/targeted/specialist supports)
   - `(:Concept)-[:HAS_ACCESS_REQUIREMENT {level, rationale, source}]->(:AccessRequirement)` -- concept-level barrier tagging
   - `(:SupportStrategy)-[:MITIGATES {strength, notes}]->(:AccessRequirement)` -- what helps what
   - `(:VehicleTemplate)-[:CAN_APPLY {default, notes}]->(:SupportStrategy)` -- template compatibility
   - `(:InteractionType)-[:ENABLES {quality, notes}]->(:SupportStrategy)` -- interaction capability
   - `(:AccessRequirement)-[:TAGGED_AS]->(:NeedArea)`, `(:SupportStrategy)-[:COMMONLY_USED_FOR]->(:NeedArea)` -- reporting links
   - `(:TeachingRequirement)-[:SUPPORTED_BY {notes}]->(:SupportStrategy)` -- teaching req links
   - Construct-protection: strategies with `construct_risk=high` never auto-applied; `conditional` surfaced as warnings
   - Teacher planner renders `## Access and Inclusion` section when data exists
   - Per-type `display_category`: NeedArea = `'SEND Need Area'` (`#E11D48`), AccessRequirement = `'Access Requirement'` (`#F97316`), SupportStrategy = `'Support Strategy'` (`#22C55E`)
   - No learner diagnostic data -- pure curriculum/support metadata
   - Scripts: `import_send_support.py`, `validate_send_support.py`
   - Data: `layers/send-support/data/`

13. **`layers/vocabulary/`** - Vocabulary Layer (v4.5)
   - Promotes `key_vocabulary` strings to first-class graph nodes with definitions
   - ~9,200 `VocabularyTerm` nodes across 62 per-subject/year JSON files
   - `(:Concept)-[:USES_TERM {introduced, importance}]->(:VocabularyTerm)` — concept-vocabulary links
   - `(:VocabularyTerm)-[:REFINES]->(:VocabularyTerm)` — vocabulary progression chains
   - `(:VocabularyTerm)-[:RELATED_TO {relationship}]->(:VocabularyTerm)` — semantic links
   - `(:VocabularyTerm)-[:SAME_SPELLING_AS]->(:VocabularyTerm)` — polysemy disambiguation
   - Beck's tiered model: tier 1 (everyday), 2 (general academic), 3 (domain-specific)
   - ID format: `VOC-{subject_prefix}-{slug}` (e.g. `VOC-MA-fraction`)
   - `display_category = 'Vocabulary Term'`, `display_color = '#0EA5E9'` (Sky-500), `display_icon = 'spellcheck'`
   - Scripts: `extract_vocabulary.py`, `generate_definitions.py`, `import_vocabulary.py`, `validate_vocabulary.py`
   - Data: `layers/vocabulary/data/terms/` (per-subject JSONs), `layers/vocabulary/data/relationships/`
   - No learner data — pure curriculum design metadata

14. **`layers/oak-content/`** - Oak National Academy (future)
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

# DifficultyLevel nodes (run after curriculum + EYFS import)
python3 layers/uk-curriculum/scripts/import_difficulty_levels.py

# RepresentationStage nodes (CPA framework, run after curriculum import)
python3 layers/uk-curriculum/scripts/import_representation_stages.py

# Cross-domain CO_TEACHES (run after concept grouping)
python3 core/migrations/create_cross_domain_co_teaches.py

# Concept-level skill integration (run after epistemic skills import)
python3 core/migrations/create_concept_skill_links.py

# Delivery mode classification (run after all enrichment layers)
python3 layers/uk-curriculum/scripts/classify_delivery_modes.py
python3 layers/uk-curriculum/scripts/import_delivery_modes.py

# Vocabulary (run after curriculum; depends on UK concepts for USES_TERM)
python3 layers/vocabulary/scripts/extract_vocabulary.py
python3 layers/vocabulary/scripts/import_vocabulary.py

# SEND support (run after curriculum + delivery modes; depends on UK + learner-profiles + topic-suggestions)
python3 layers/send-support/scripts/import_send_support.py

# Assessment layer (optional, depends on UK)
python3 layers/assessment/scripts/import_test_frameworks.py

# Epistemic skills (optional, depends on UK)
python3 layers/epistemic-skills/scripts/import_epistemic_skills.py

# Per-subject ontology: VehicleTemplates + typed study/reference nodes (depends on UK)
python3 layers/topic-suggestions/scripts/import_vehicle_templates.py
python3 layers/topic-suggestions/scripts/import_subject_ontologies.py

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
- `:DifficultyLevel` — grounded difficulty tiers per Concept (primary: entry → greater_depth; secondary: emerging → mastery)
- `:RepresentationStage` — CPA (Concrete-Pictorial-Abstract) stages per Concept (primary maths Y1-Y6)
- `:DeliveryMode` — 4 delivery channel nodes (AI Direct, AI Facilitated, Guided Materials, Specialist Teacher)
- `:TeachingRequirement` — 15 atomic pedagogical requirements driving delivery classification
- `:SourceDocument`

**Topic Suggestions (per-subject ontology):**
- `:HistoryStudy`, `:GeoStudy`, `:ScienceEnquiry`, `:EnglishUnit`, `:MathsUnit` — typed study/unit nodes per subject
- `:ArtTopicSuggestion`, `:MusicTopicSuggestion`, `:DTTopicSuggestion`, `:ComputingTopicSuggestion` — foundation subject suggestions
- `:TopicSuggestion` — generic (RE, Citizenship, etc.)
- `:VehicleTemplate` — 24 pedagogical pattern templates with age-banded prompts

**Subject Reference (per-subject ontology):**
- `:DisciplinaryConcept`, `:HistoricalSource` — History reference nodes
- `:GeoPlace`, `:GeoContrast` — Geography reference nodes
- `:EnquiryType`, `:Misconception` — Science reference nodes
- `:Genre`, `:SetText` — English reference nodes
- `:MathsManipulative`, `:MathsRepresentation`, `:MathsContext`, `:ReasoningPromptType` — Maths reference nodes

**Epistemic Skills:**
- `:WorkingScientifically`, `:ReadingSkill`, `:MathematicalReasoning`
- `:GeographicalSkill`, `:HistoricalThinking`, `:ComputationalThinking`

**Assessment:**
- `:TestFramework`, `:TestPaper`, `:ContentDomainCode`

**CASE Standards:**
- `:Framework`, `:Dimension`, `:Practice`, `:CoreIdea`
- `:CrosscuttingConcept`, `:PerformanceExpectation`, `:GradeBand`

**Learner Profiles:**
- `:InteractionType` — 33 UI/pedagogical patterns (phoneme splitter, bus stop division, concept mapper, etc.)
- `:ContentGuideline` — reading level, TTS, vocabulary constraints per Year
- `:PedagogyProfile` — session structure, productive failure, scaffolding per Year
- `:FeedbackProfile` — tone, gamification safety, metacognitive prompts per Year
- `:PedagogyTechnique` — 5 desirable difficulty techniques with evidence base and implementation notes

**Vocabulary:**
- `:VocabularyTerm` — ~9,200 curriculum vocabulary terms with definitions, Beck's tier, etymology

**SEND Support:**
- `:NeedArea` — 4 statutory SEND categories (reporting taxonomy, not execution logic)
- `:AccessRequirement` — 16 task-side access barriers (working_memory_load, decoding_demand, etc.)
- `:SupportStrategy` — 20 support strategies with tier (universal/targeted/specialist) and construct_risk

**NO namespace labels** - Each node has ONE semantic label (e.g., `:Objective`, not `:Curriculum:Objective`)

### Provenance Property

All nodes have `display_category` property:
- `"UK Curriculum"`
- `"CASE Standards"`
- `"Epistemic Skills"`
- `"Assessment"`
- `"Learner Profile"`
- `"Topic Suggestion"` — study/unit nodes (HistoryStudy, GeoStudy, etc.)
- `"Subject Reference"` — reference nodes (GeoPlace, Misconception, Genre, etc.)
- `"Vehicle Template"` — VehicleTemplate nodes
- `"SEND Need Area"` — NeedArea nodes
- `"Access Requirement"` — AccessRequirement nodes
- `"Support Strategy"` — SupportStrategy nodes
- `"Vocabulary Term"` — VocabularyTerm nodes
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
(:Concept)-[:HAS_DIFFICULTY_LEVEL]->(:DifficultyLevel)  // 3-4 levels per concept (1,296/1,351 concepts — all EYFS+KS1-KS4)

// RepresentationStage (v4.1) — CPA (Concrete-Pictorial-Abstract) progression for primary maths
(:Concept)-[:HAS_REPRESENTATION_STAGE]->(:RepresentationStage)  // 3 stages per concept (154 primary maths concepts Y1-Y6)

// Delivery Readiness (v4.3) — delivery mode classification for every concept
(:Concept)-[:DELIVERABLE_VIA {primary: bool, confidence: str, rationale: str}]->(:DeliveryMode)
(:Concept)-[:HAS_TEACHING_REQUIREMENT]->(:TeachingRequirement)
(:TeachingRequirement)-[:IMPLIES_MINIMUM_MODE]->(:DeliveryMode)

// Per-subject ontology (v4.2) — typed study nodes deliver curriculum concepts
(:Domain)-[:HAS_SUGGESTION]->(ts)                     // ts = HistoryStudy | GeoStudy | ScienceEnquiry | EnglishUnit | ...
(ts)-[:DELIVERS_VIA {primary: bool}]->(:Concept)      // many-to-many concept delivery
(:VehicleTemplate)-[:TEMPLATE_FOR {agent_prompt: str}]->(:KeyStage)  // age-banded pedagogical prompts

// Subject-specific relationships (examples)
(:HistoryStudy)-[:FOREGROUNDS]->(:DisciplinaryConcept)       // History disciplinary concepts
(:HistoryStudy)-[:USES_SOURCE]->(:HistoricalSource)          // History source types
(:HistoryStudy)-[:CHRONOLOGICALLY_FOLLOWS]->(:HistoryStudy)  // Timeline sequencing
(:GeoStudy)-[:LOCATED_IN]->(:GeoPlace)                       // Geography places
(:GeoStudy)-[:CONTRASTS_WITH]->(:GeoContrast)                // Contrasting locality pairs
(:ScienceEnquiry)-[:USES_ENQUIRY_TYPE]->(:EnquiryType)       // Science enquiry methodology
(:ScienceEnquiry)-[:ADDRESSES_MISCONCEPTION]->(:Misconception)
(:EnglishUnit)-[:USES_GENRE]->(:Genre)                       // English text types
(:EnglishUnit)-[:USES_SET_TEXT]->(:SetText)                   // KS4 set text links
(:MathsUnit)-[:USES_MANIPULATIVE]->(:MathsManipulative)      // Maths concrete resources
(:MathsUnit)-[:USES_REPRESENTATION]->(:MathsRepresentation)  // Maths pictorial representations
(:MathsUnit)-[:USES_CONTEXT]->(:MathsContext)                // Real-world maths contexts
(:MathsUnit)-[:USES_REASONING_PROMPT]->(:ReasoningPromptType) // Reasoning structures

// Cross-curricular links between study nodes
(ts)-[:CROSS_CURRICULAR {hook: str, strength: str}]->(ts2)  // e.g. HistoryStudy → ScienceEnquiry

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

// Vocabulary (v4.5) — curriculum terms promoted to first-class nodes
(:Concept)-[:USES_TERM {introduced: bool, importance: str}]->(:VocabularyTerm)
(:VocabularyTerm)-[:REFINES]->(:VocabularyTerm)                 // "integer" REFINES "number"
(:VocabularyTerm)-[:RELATED_TO {relationship: str}]->(:VocabularyTerm)  // synonym, antonym, hypernym, etc.
(:VocabularyTerm)-[:SAME_SPELLING_AS]->(:VocabularyTerm)        // polysemy: VOC-SC-cell ↔ VOC-CO-cell

// SEND support (barrier-first model, no diagnostic labels)
(:Concept)-[:HAS_ACCESS_REQUIREMENT {level, rationale, source}]->(:AccessRequirement)  // concept-level barriers
(:SupportStrategy)-[:MITIGATES {strength, notes}]->(:AccessRequirement)                // what helps what
(:VehicleTemplate)-[:CAN_APPLY {default, notes}]->(:SupportStrategy)                   // template compatibility
(:InteractionType)-[:ENABLES {quality, notes}]->(:SupportStrategy)                     // interaction capability
(:AccessRequirement)-[:TAGGED_AS]->(:NeedArea)                                         // reporting taxonomy only
(:SupportStrategy)-[:COMMONLY_USED_FOR]->(:NeedArea)                                   // broad need-area association
(:TeachingRequirement)-[:SUPPORTED_BY {notes}]->(:SupportStrategy)                     // teaching req links
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
- Per-subject ontology / topic suggestions / vehicle templates? → `layers/topic-suggestions/`
- Teacher review findings / lesson plans? → `generated/teachers-v7/` (V7 review + DL QA), `generated/teachers-v4/` (V5 review), `generated/teachers-v3/` (V4 review)
  - **`generated/` is TEST output, not canon** — do not treat its contents as authoritative for graph model or data decisions
- Concept grouping / lesson clusters? → `layers/uk-curriculum/scripts/generate_concept_clusters.py`
- Thinking lenses (cognitive framing for clusters)? → `layers/uk-curriculum/data/thinking_lenses/` + `import_thinking_lenses.py`
- Difficulty levels (grounded difficulty tiers)? → `layers/uk-curriculum/data/difficulty_levels/` + `import_difficulty_levels.py`
- Representation stages (CPA framework for primary maths)? → `layers/uk-curriculum/data/representation_stages/` + `import_representation_stages.py`
- Delivery readiness / teachability classification? → `layers/uk-curriculum/data/delivery_modes/` + `classify_delivery_modes.py` + `import_delivery_modes.py`
- Vocabulary terms / definitions / Beck's tiers? → `layers/vocabulary/data/terms/` + `import_vocabulary.py`
- SEND support / access requirements / support strategies? → `layers/send-support/data/` + `import_send_support.py`
- What can the AI platform teach? → `docs/design/PLAN_DELIVERY_MODE_CLASSIFICATION.md`
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
- DifficultyLevels: `MA-Y3-C014-DL01` (Concept-ID + `-DL` + zero-padded level_number)
- Topic Suggestions: per-label ID property — `study_id` (History/Geo), `enquiry_id` (Science), `unit_id` (English), `suggestion_id` (generic/foundation)
- VehicleTemplates: `VT-001` format
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

## Current State (2026-02-25)

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

✅ **In Aura cloud database — all layers active (2026-02-24):**
- Instance: education-graphs (6981841e)
- **~10,675 total nodes**, **~23,740+ total relationships**
- 581 per-subject ontology nodes (326 study/unit + 255 reference) + 24 VehicleTemplate nodes; 3,383+ ontology relationships + 77 TEMPLATE_FOR
- 4,952 DifficultyLevel nodes; 4,952 HAS_DIFFICULTY_LEVEL relationships (1,296/1,351 concepts covered — all EYFS+KS1-KS4)
- 10 ThinkingLens nodes; 1,222 APPLIES_LENS relationships (~2 per cluster on average); 40 PROMPT_FOR relationships (age-banded prompts)
- 626 ConceptCluster nodes (167 introduction, 459 practice) — all with `thinking_lens_primary`
- 1,351 Concept nodes enriched with `teaching_weight` + `co_teach_hints`
- 53 EYFS Concept nodes; 34 EYFS→KS1 cross-stage prerequisites
- 1,892 CO_TEACHES relationships (extracted + inferred inverse-operation pairs)
- Visualization properties applied (display_color, display_icon, display_category, name) — Year nodes labelled "Year 1"…"Year 11"
- `display_size` property removed from graph and import scripts (was unused by Bloom or custom visualizations)
- `is_cross_cutting` property removed from Domain/Concept imports and indexes (was unreliable LLM-generated flag; kept in extraction JSONs for reference)
- `co_teach_hints` property removed from graph (now read directly from extraction JSONs by `compute_lesson_grouping_signals.py`)
- 6 Bloom perspectives uploaded and active

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

✅ **Per-subject ontology layer (v4.2, 2026-02-24):**
- Replaces old Content Vehicles (v3.8) + Topics layers with typed per-subject nodes
- **581 nodes** across 21 typed labels: 326 study/unit nodes + 255 reference nodes
- **24 VehicleTemplate nodes** with 77 TEMPLATE_FOR relationships (age-banded pedagogical prompts)
- **3,383+ relationships** including DELIVERS_VIA (1,076), HAS_SUGGESTION (460), USES_TEMPLATE (382), FOREGROUNDS, USES_SOURCE, LOCATED_IN, CONTRASTS_WITH, USES_ENQUIRY_TYPE, SURFACES_MISCONCEPTION, IN_GENRE, STUDIES_TEXT, CROSS_CURRICULAR (~246), USED_FOR_CONCEPT (586), etc.
- Subject coverage: History (43 studies, KS1-KS4), Geography (32 studies, KS1-KS4), Science (45 enquiries, KS1-KS4), English (54 units, KS1-KS4), Maths (62 units, KS1-KS4), Art (39, KS1-KS4), Music (35, KS1-KS4), DT (33, KS1-KS4), Computing (22, KS1-KS4), generic/RS/Citizenship (23)
- Each subject uses its own property schema — no irrelevant attributes
- 8-agent teacher panel designed the schema (Phase 0); data migrated from ContentVehicle + Topic nodes (Phase 2)
- Old layers archived to `layers/_archived/content-vehicles/` and `layers/_archived/topics/`
- Scripts: `import_vehicle_templates.py`, `import_subject_ontologies.py`
- Validation: 5 checks (completeness, DELIVERS_VIA coverage, HAS_SUGGESTION coverage, suggestion_type values, curriculum_status values)
- Query helpers: `graph_query_helper.py` surfaces per-subject ontology nodes per domain
- No learner data — all nodes are curriculum design metadata

✅ **DifficultyLevel layer (v3.9 → v3.10, 2026-02-23):**
- Replaces ungrounded `complexity_level` integer with structured sub-nodes per Concept
- `(:Concept)-[:HAS_DIFFICULTY_LEVEL]->(:DifficultyLevel)` — 3-4 levels per concept
- **Primary labels** (EYFS + KS1-KS2): `entry` (1), `developing` (2), `expected` (3), `greater_depth` (4)
- **Secondary labels** (KS3-KS4): `emerging` (1), `developing` (2), `secure` (3), `mastery` (4)
- EYFS uses 3 levels only (entry/developing/expected) — no greater_depth per developmental framework
- Each node has `description`, `example_task`, `example_response`, `common_errors` — grounding abstract difficulty into concrete, assessable tasks
- **Full rollout: 1,296 concepts, 4,952 DifficultyLevel nodes** across 148 domain-level JSON files
- Coverage: all EYFS (53), English KS1-Y6 (294), Mathematics Y1-Y6 (154), Science KS1-KS2 (116), plus History, Geography, DT, Art, Music, PE, Computing, Languages (KS1-KS2) + 595 KS3-KS4 concepts across all secondary subjects
- 55 PE KS3-KS4 concepts excluded (combined programme, may need sport-specific assessment framework)
- Data: 148 files in `layers/uk-curriculum/data/difficulty_levels/` (87 primary + 61 secondary)
- Import: `layers/uk-curriculum/scripts/import_difficulty_levels.py` (idempotent, globs `*.json`)
- Schema: DifficultyLevel uniqueness constraint + indexes on `level_number`, `label` (v3.9)
- Validation: 5 checks (completeness, level_number range, label values, HAS_DIFFICULTY_LEVEL integrity, no duplicate levels)
- `complexity_level` property removed from Concept import; `complexity_range` removed from ConceptCluster generation
- Query helpers: `query_cluster_context.py` and `graph_query_helper.py` surface difficulty levels under each concept
- QA: all 148 files QA-reviewed; KS1-KS2 report in `generated/teachers-v7/dl_qa_report.md`
- No learner data — pure curriculum design metadata

✅ **V7 teacher review (2026-02-23):**
- 9 simulated teacher personas reviewed the graph with DifficultyLevels + per-subject ontology + Thinking Lenses
- Focus: DifficultyLevel quality across Y3-Y5 Maths, English, Science, History, Geography
- Average content generation readiness: **7.2/10** (up from 6.6/10 in V5)
- DifficultyLevels identified as highest-leverage addition (+1.5 score uplift, 9/9 consensus)
- Reports: `generated/teachers-v7/`

✅ **RepresentationStage layer (v4.1, 2026-02-24):**
- CPA (Concrete-Pictorial-Abstract) framework as first-class graph nodes for primary maths
- ~462 RepresentationStage nodes across 154 concepts (Y1-Y6), 3 stages per concept
- Each node: `description`, `resources` (array), `example_activity`, `transition_cue`
- `transition_cue` describes observable child behaviour (not test scores or "when ready")
- Complements DifficultyLevel: RS = representation journey (tools + transition), DL = attainment tiers
- Resources reference UK-standard manipulatives (Dienes blocks, Numicon, Cuisenaire rods, etc.)
- Data: 12 JSON files in `layers/uk-curriculum/data/representation_stages/`
- Import: `layers/uk-curriculum/scripts/import_representation_stages.py` (idempotent)
- Schema: RepresentationStage uniqueness constraint + indexes on `stage_number`, `stage` (v4.1)
- Validation: 5 checks (completeness, stage_number range, stage values, HAS_REPRESENTATION_STAGE integrity, no duplicates)
- Query helpers: `query_cluster_context.py` and `graph_query_helper.py` surface CPA stages per concept
- No learner data — pure curriculum design metadata

✅ **Delivery Readiness layer (v4.3, 2026-02-27):**
- Every concept classified by delivery suitability: what AI/human combination is needed to teach it
- 4 `DeliveryMode` nodes: AI Direct (DM-AI), AI Facilitated (DM-AF), Guided Materials (DM-GM), Specialist Teacher (DM-ST)
- 15 `TeachingRequirement` nodes across 5 categories (assessment, resource, pedagogy, knowledge, safety)
- Each TeachingRequirement has `IMPLIES_MINIMUM_MODE` relationship to a DeliveryMode
- Classification of all 1,351 concepts: 804 AI Direct (59.5%), 263 AI Facilitated (19.5%), 140 Guided Materials (10.4%), 144 Specialist Teacher (10.7%)
- **Platform addressable surface: 1,067 concepts (79%)** can be taught by AI Direct or AI Facilitated
- Subject highlights: Mathematics 100% AI-reachable, Science 99%, Computing 100%, PE 12%, Drama 0%
- Music: theory/notation/listening = AI Direct; composition = AI Facilitated (digital tools); performance = Specialist Teacher
- Classification uses 14 input signals: concept_type, teaching_weight, RepresentationStage resources, concept_skill_links enquiry_type, ThinkingLens, keyword analysis of teaching_guidance/description
- Data: 62 per-subject JSON files + 2 definition files in `layers/uk-curriculum/data/delivery_modes/`
- Scripts: `classify_delivery_modes.py` (generates JSONs), `import_delivery_modes.py` (loads to Neo4j)
- Schema: DeliveryMode + TeachingRequirement uniqueness constraints + indexes (v4.3)
- Validation: 5 checks (completeness, coverage, integrity, distribution)
- No learner data — pure curriculum design metadata

✅ **Vocabulary layer (v4.5, scaffolding complete):**
- ~9,200 VocabularyTerm stubs extracted from all extraction JSONs (62 per-subject/year files)
- ID format: `VOC-{subject_prefix}-{slug}` (e.g. `VOC-MA-fraction`, `VOC-SC-photosynthesis`)
- `(:Concept)-[:USES_TERM {introduced, importance}]->(:VocabularyTerm)` — ~17,000 relationships
- `(:VocabularyTerm)-[:REFINES]->(:VocabularyTerm)` — vocabulary progression chains (skeleton)
- `(:VocabularyTerm)-[:RELATED_TO {relationship}]->(:VocabularyTerm)` — semantic links (skeleton)
- `(:VocabularyTerm)-[:SAME_SPELLING_AS]->(:VocabularyTerm)` — polysemy disambiguation (skeleton)
- Beck's tiered classification: tier 1=everyday, 2=general academic, 3=domain-specific
- Scripts: `extract_vocabulary.py`, `generate_definitions.py` (LLM-assisted), `import_vocabulary.py`, `validate_vocabulary.py`
- Schema: VocabularyTerm uniqueness constraint + 4 indexes (v4.5)
- Validation: 5 checks in validate_schema.py + 8 checks in validate_vocabulary.py
- Site integration: compile_site_data.py, ConceptCard.astro, render_markdown.py word mat, planner_queries.py
- `key_vocabulary` string property preserved on Concept nodes (backward-compatible fallback)
- Definitions pending: Phase 2 will generate definitions using `generate_definitions.py` (Maths Y1-Y6 pilot)
- No learner data — pure curriculum design metadata

🚧 **In progress:**
- Vocabulary definitions: Phase 2 (Maths Y1-Y6 pilot), Phase 3 (remaining subjects)
- Vocabulary relationships: refinements.json, polysemy.json, semantic.json (authoring pending)
- SEND Support Layer (v4.4): data authoring, import scripts, compiler integration
  - 4 NeedArea + 16 AccessRequirement + 20 SupportStrategy nodes designed
  - Teacher planner Access and Inclusion section integrated in compiler
  - Import script + validation script in development
- Per-subject ontology Phase 4: remaining gaps (RS KS4, Citizenship KS4, additional set texts)
- DifficultyLevel: PE KS3-KS4 (55 concepts remaining — sport-specific assessment framework needed)
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
❌ Edit DifficultyLevel data directly in the graph - Edit the JSON files in `data/difficulty_levels/`, then rerun `import_difficulty_levels.py --clear`
❌ Edit RepresentationStage data directly in the graph - Edit the JSON files in `data/representation_stages/`, then rerun `import_representation_stages.py --clear`
❌ Create monolithic DL files for large subjects - Split by curriculum domain (e.g. `english_y4_composition.json`, not `english_y4.json`). Max ~20 concepts per file for maintainability
❌ Edit per-subject ontology data directly in the graph - Edit the JSON files in `layers/topic-suggestions/data/`, then rerun `import_subject_ontologies.py --clear`
❌ Store cross-curricular connections as JSON blobs on nodes — Use `cross_curricular_links` in data files, which creates proper `CROSS_CURRICULAR` relationships via import
❌ Manually assign delivery modes in the graph - Rerun `classify_delivery_modes.py` to regenerate JSONs, then `import_delivery_modes.py --clear`
❌ Change delivery mode classification rules without re-running the full classification - The script is the source of truth; edit the rules in `classify_delivery_modes.py`, then rerun
❌ Use a universal TopicSuggestion label for all subjects - Each subject has its own typed label (HistoryStudy, GeoStudy, etc.) with subject-specific properties
❌ Reference old ContentVehicle or Topic nodes - These have been replaced by the per-subject ontology (v4.2) and archived to `layers/_archived/`
❌ Edit VocabularyTerm data directly in the graph - Edit the JSON files in `layers/vocabulary/data/terms/`, then rerun `import_vocabulary.py --clear`
❌ Store medical diagnoses or EHCP data in the curriculum graph - The SEND layer models barriers to task access, not diagnoses
❌ Create diagnosis-to-action execution logic (e.g. "dyslexia = always use read-aloud") - The system maps access requirements to support strategies, never labels to actions
❌ Auto-apply construct_risk=high strategies in child-facing flows - These must be human-gated
❌ Edit SEND data directly in the graph - Edit JSON files in `layers/send-support/data/`, rerun `import_send_support.py --clear`

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
