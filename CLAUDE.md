# UK Curriculum Knowledge Graph - AI Agent Guide

**For: Claude, Cursor, GitHub Copilot, or any AI working on this project**

## What This Is

A **multi-layer knowledge graph** comparing UK National Curriculum with US standards (NGSS, Common Core) and content providers (Oak National Academy). Built in Neo4j, designed for curriculum research and adaptive learning systems.

**Main use case**: Understand curriculum structure, compare international standards, map learning progressions, and generate age-appropriate AI lessons via graph queries.

---

## Project Architecture (Layer-Based)

Each **layer** is self-contained with its own:
- `extractions/` - Source data (JSON)
- `scripts/` - Import scripts
- `docs/` - Documentation
- `research/` - Background research

### Core Layers (in dependency order)

1. **`layers/uk-curriculum/`** - UK National Curriculum (2014)
   - Foundation layer - everything else builds on this
   - 1,219 concepts, 1,551 objectives, 316 domains across 55 subjects (KS1–KS4)
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

7. **`layers/oak-content/`** - Oak National Academy (future)
   - Content provider mapping
   - Script: `import_oak_content.py`

### Shared Infrastructure

- **`core/scripts/`** - Schema, validation, config shared across all layers
- **`core/migrations/`** - Database migrations (add properties, fix data)
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

# Assessment layer (optional, depends on UK)
python3 layers/assessment/scripts/import_test_frameworks.py

# Epistemic skills (optional, depends on UK)
python3 layers/epistemic-skills/scripts/import_epistemic_skills.py

# Topics (optional, depends on UK)
python3 layers/topics/scripts/import_topics.py

# CASE standards (optional, independent)
python3 layers/case-standards/scripts/import_case_standards_v2.py --import

# Learner profiles (optional, depends on UK)
python3 layers/learner-profiles/scripts/import_learner_profiles.py

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
- `:Domain`, `:Objective`, `:Concept`
- `:Topic`, `:SourceDocument`

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

**NO namespace labels** - Each node has ONE semantic label (e.g., `:Objective`, not `:Curriculum:Objective`)

### Provenance Property

All nodes have `display_category` property:
- `"UK Curriculum"`
- `"CASE Standards"`
- `"Epistemic Skills"`
- `"Assessment"`
- `"Learner Profile"`
- `"Structure"`

### Key Relationships

```cypher
// UK Curriculum structure
(:Curriculum)-[:HAS_KEY_STAGE]->(:KeyStage)-[:HAS_YEAR]->(:Year)-[:HAS_PROGRAMME]->(:Programme)
(:Programme)-[:HAS_DOMAIN]->(:Domain)-[:CONTAINS]->(:Objective)-[:TEACHES]->(:Concept)
(:Concept)-[:PREREQUISITE_OF]->(:Concept)  // Learning progressions

// NGSS 3D model
(:Framework)-[:HAS_DIMENSION]->(:Dimension)-[:HAS_PRACTICE]->(:Practice)
(:Dimension)-[:HAS_CORE_IDEA]->(:CoreIdea)
(:PerformanceExpectation)-[:USES_PRACTICE]->(:Practice)
(:PerformanceExpectation)-[:USES_CORE_IDEA]->(:CoreIdea)

// Cross-layer alignments
(:Practice)-[:ALIGNS_TO]->(:Concept)  // NGSS ↔ UK
(:Programme)-[:DEVELOPS_SKILL]->(:WorkingScientifically)  // UK ↔ Skills

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

## Where to Find Things

**Want to work on...**

- UK curriculum extraction? → `layers/uk-curriculum/`
- NGSS structure? → `layers/case-standards/docs/CASE_GRAPH_MODEL_v3.5.md`
- Visualization / Bloom perspectives? → `layers/visualization/`
- Age-appropriate design / learner profiles? → `layers/learner-profiles/`
- User stories? → `docs/user-stories/`
- Schema definition? → `core/scripts/create_schema.py`
- Import all data? → `core/scripts/import_all.py` (orchestrator)

**Confused about...**

- Graph model? → `core/docs/graph_model_overview.md`
- Layer architecture? → This file (CLAUDE.md)
- Specific layer? → `layers/{layer-name}/README.md`
- Learner profile queries? → `layers/learner-profiles/README.md`

---

## Important Conventions

### File Naming
- Extractions: `{subject}_{key_stage}.json`
- Scripts: `import_{layer}.py`
- Docs: `{TOPIC}.md` (uppercase for main docs)

### Node IDs
- UK: `EN-Y5-O021` (Subject-Year-Type-Number)
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
- Run `core/migrations/add_name_properties.py`
- All nodes need `name` property

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

1. **Research** → `layers/{layer}/research/`
2. **Extract** → Create JSONs in `layers/{layer}/extractions/`
3. **Validate** → Run `core/scripts/validate_extractions.py`
4. **Import** → Run `layers/{layer}/scripts/import_{layer}.py`
5. **Verify** → Run `core/scripts/validate_schema.py`
6. **Document** → Update `layers/{layer}/README.md`
7. **Commit** → Git commit with clear message

---

## Current State (2026-02-21)

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
- UK National Curriculum (55 subjects, 316 domains, 1,551 objectives, 1,219 concepts — KS1–KS4)
- Assessment (KS2 test frameworks)
- Epistemic Skills
- Topics
- CASE Standards (NGSS + Common Core Math)
- Learner Profiles (71 nodes — 33 InteractionType, 11 ContentGuideline, 11 PedagogyProfile, 11 FeedbackProfile, 5 PedagogyTechnique)
- Visualization (5 Bloom perspectives with icons, styleRules, and search templates)

✅ **In Aura cloud database — clean full import (2026-02-21):**
- Instance: education-graphs (6981841e)
- **3,995 total nodes**
- Visualization properties applied (display_color, display_icon, name) — Year nodes labelled "Year 1"…"Year 11"
- 5 Bloom perspectives uploaded and active

🚧 **In progress:**
- Oak National Academy content (skeleton only)
- Alignment mappings (CASE ↔ UK)

---

## Key Files to Read First

1. This file (CLAUDE.md) - Architecture overview
2. `core/docs/graph_model_overview.md` - Data model
3. `layers/uk-curriculum/README.md` - Core layer
4. `layers/case-standards/docs/CASE_GRAPH_MODEL_v3.5.md` - NGSS structure
5. `layers/learner-profiles/README.md` - Age-appropriate design layer + agent query patterns
6. `docs/design/RESEARCH_BRIEFING.md` - Research briefing and rationale for the learner layer

---

## Don't Do This

❌ Add namespace labels (`:Curriculum:Objective`) - We removed these for clarity
❌ Hardcode credentials in scripts - Use `neo4j_config.py`
❌ Create generic "CFItem" blobs - Parse structure intelligently
❌ Skip validation - Always run `validate_schema.py`
❌ Mix layer data in scripts - Keep layers self-contained
❌ Add flat age/interaction properties to Year nodes - Use the learner-profiles layer instead
❌ Match Year nodes on `year_code` - the property is `year_id`

---

**Questions?** Check layer-specific READMEs or ask the human!
