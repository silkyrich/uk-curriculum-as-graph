# UK Curriculum Knowledge Graph - AI Agent Guide

**For: Claude, Cursor, GitHub Copilot, or any AI working on this project**

## What This Is

A **multi-layer knowledge graph** comparing UK National Curriculum with US standards (NGSS, Common Core) and content providers (Oak National Academy). Built in Neo4j, designed for curriculum research and adaptive learning systems.

**Main use case**: Understand curriculum structure, compare international standards, map learning progressions.

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
   - 1,032 concepts, 1,193 objectives, 225 domains across 12 subjects
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

6. **`layers/oak-content/`** - Oak National Academy (future)
   - Content provider mapping
   - Script: `import_oak_content.py`

### Shared Infrastructure

- **`core/scripts/`** - Schema, validation, config shared across all layers
- **`core/migrations/`** - Database migrations (add properties, fix data)
- **`viz/`** - Bloom perspectives, styling configs

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

# Visualization properties (recommended)
python3 core/migrations/add_name_properties.py
python3 core/migrations/add_display_properties.py
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

**NO namespace labels** - Each node has ONE semantic label (e.g., `:Objective`, not `:Curriculum:Objective`)

### Provenance Property

All nodes have `display_category` property:
- `"UK Curriculum"`
- `"CASE Standards"`
- `"Epistemic Skills"`
- `"Assessment"`
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
```

---

## Where to Find Things

**Want to work on...**

- UK curriculum extraction? → `layers/uk-curriculum/`
- NGSS structure? → `layers/case-standards/docs/CASE_GRAPH_MODEL_v3.5.md`
- Visualization? → `viz/bloom/`
- User stories? → `research/learner-layer/user-stories/`
- Schema definition? → `core/scripts/create_schema.py`
- Import all data? → `core/scripts/import_all.py` (orchestrator)

**Confused about...**

- Graph model? → `core/docs/graph_model_overview.md`
- Layer architecture? → This file (CLAUDE.md)
- Specific layer? → `layers/{layer-name}/README.md`

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

## Current State (2026-02-20)

✅ **Complete layers:**
- UK National Curriculum (3,252 nodes)
- Assessment (KS2 test frameworks)
- Epistemic Skills
- Topics
- CASE Standards (NGSS + Common Core Math)

✅ **In Aura cloud database:**
- Instance: education-graphs
- All layers imported
- Visualization properties applied

🚧 **In progress:**
- Oak National Academy content (skeleton only)
- Alignment mappings (CASE ↔ UK)

---

## Key Files to Read First

1. This file (CLAUDE.md) - Architecture overview
2. `core/docs/graph_model_overview.md` - Data model
3. `layers/uk-curriculum/README.md` - Core layer
4. `layers/case-standards/docs/CASE_GRAPH_MODEL_v3.5.md` - NGSS structure

---

## Don't Do This

❌ Add namespace labels (`:Curriculum:Objective`) - We removed these for clarity
❌ Hardcode credentials in scripts - Use `neo4j_config.py`
❌ Create generic "CFItem" blobs - Parse structure intelligently
❌ Skip validation - Always run `validate_schema.py`
❌ Mix layer data in scripts - Keep layers self-contained

---

**Questions?** Check layer-specific READMEs or ask the human!
