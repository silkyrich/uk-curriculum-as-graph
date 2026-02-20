# Core Infrastructure

## Purpose

The **shared infrastructure** for the entire UK curriculum knowledge graph — schema management, validation, visualization configuration, and utility scripts used across all layers.

## Contents

### `/core/scripts/` — Core Scripts

| Script | Purpose | Usage |
|---|---|---|
| `neo4j_config.py` | Neo4j connection configuration (env vars) | Imported by all layer scripts |
| `create_schema.py` | Create constraints and indexes | Run before first import |
| `validate_schema.py` | Validate graph integrity | Run after imports |
| `validate_extractions.py` | Validate JSON extraction files | Run before imports |
| `add_name_properties.py` | Add `name` property to all nodes | Run once after initial import |
| `add_display_properties.py` | Add Bloom visualization properties | Run once after initial import |
| `import_all.py` | Orchestrate import of all layers in correct order | See below |

### `/core/data/` — Core Data

| Directory | Contents |
|---|---|
| `bloom/` | Neo4j Bloom perspectives and configuration |
| `curriculum-documents/` | Source document metadata (PDFs, URLs, references) |

### `/core/docs/` — Core Documentation

| File | Purpose |
|---|---|
| `graph_model_overview.md` | High-level graph model documentation |
| (more to be added) | Architecture decisions, design rationale |

## Usage

### 1. Configure Neo4j connection

Set environment variables:

```bash
export NEO4J_URI="neo4j+s://xxx.databases.neo4j.io"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your-password-here"
```

Or use a local instance (default):

```bash
export NEO4J_URI="neo4j://127.0.0.1:7687"
```

### 2. Create schema constraints and indexes

```bash
cd /Users/richardmorgan/Documents/GitHub/uk-curriculum-as-graph
python3 core/scripts/create_schema.py
```

This creates:
- Uniqueness constraints (28 node types)
- Indexes for common query patterns
- Required before any imports

### 3. Import all layers

```bash
python3 core/scripts/import_all.py
```

This orchestrates the import in the correct order:
1. UK Curriculum (foundation layer)
2. Assessment (depends on UK Curriculum)
3. Epistemic Skills (depends on UK Curriculum + Assessment)
4. Topics (depends on UK Curriculum)
5. CASE Standards (depends on UK Curriculum + Epistemic Skills)
6. Oak Content (depends on UK Curriculum)

### 4. Add visualization properties

```bash
python3 core/scripts/add_name_properties.py
python3 core/scripts/add_display_properties.py
```

These add `name`, `display_color`, `display_icon`, and `display_category` properties to all nodes for Neo4j Browser/Bloom visualization.

### 5. Validate the graph

```bash
python3 core/scripts/validate_schema.py
```

This runs:
- **Category I checks**: Schema completeness (all expected node types exist)
- **Category II checks**: Relationship integrity (no dangling references)
- **Category III checks**: Property completeness (required fields present)

All checks should PASS before considering the import successful.

## Shared Configuration

### `neo4j_config.py`

All layer import scripts use this shared configuration module. It reads environment variables:

```python
import os
NEO4J_URI = os.getenv('NEO4J_URI', 'neo4j://127.0.0.1:7687')
NEO4J_USER = os.getenv('NEO4J_USERNAME', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password123')
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE', None)
```

Layer scripts import this via:

```python
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "core" / "scripts"))
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
```

## Schema Constraints

The graph uses **uniqueness constraints** on ID properties for all node types:

### UK Curriculum Layer
- `Curriculum.curriculum_id`
- `KeyStage.key_stage_id`
- `Year.year_id`
- `Subject.subject_id`
- `Programme.programme_id`
- `Domain.domain_id`
- `Objective.objective_id`
- `Concept.concept_id`
- `SourceDocument.document_id`

### Assessment Layer
- `TestFramework.framework_id`
- `TestPaper.paper_id`
- `ContentDomainCode.code_id`

### Epistemic Skills Layer
- `WorkingScientifically.skill_id`
- `ReadingSkill.skill_id`
- `HistoricalThinking.skill_id`
- `MathematicalReasoning.skill_id`
- `GeographicalSkill.skill_id`
- `ComputationalThinking.skill_id`

### Topics Layer
- `Topic.topic_id`

### CASE Standards Layer
- `Framework.framework_id`
- `Dimension.dimension_id`
- `Practice.practice_id`
- `CoreIdea.core_idea_id`
- `PerformanceExpectation.pe_id`

### Oak Content Layer
- `OakUnit.unit_slug`
- `OakLesson.lesson_slug`

## Visualization Properties

All nodes have these properties for Neo4j Browser/Bloom:

| Property | Type | Example | Purpose |
|---|---|---|---|
| `name` | string | "Fractions" | Display name in Browser |
| `display_color` | string | `#3B82F6` | Node color (Tailwind palette) |
| `display_icon` | string | `lightbulb_outline` | Material icon name |
| `display_category` | string | `"UK Curriculum"` | Grouping for legends |

These are set by `add_display_properties.py` and referenced in Bloom perspectives.

## Validation Strategy

### Category I: Schema Completeness

Check that all expected node types exist in the graph. For example:
- `check_curriculum_layer_completeness()` — KeyStage, Year, Programme, Domain, Objective, Concept
- `check_assessment_layer_completeness()` — TestFramework, TestPaper, ContentDomainCode

### Category II: Relationship Integrity

Check for dangling references. For example:
- `check_has_domain_integrity()` — Programme -[:HAS_DOMAIN]-> Domain (all referenced domains exist)
- `check_assesses_integrity()` — ContentDomainCode -[:ASSESSES]-> Programme (all referenced programmes exist)

### Category III: Property Completeness

Check that required properties are present. For example:
- `check_concept_properties()` — All Concepts have `concept_name`, `source_reference`
- `check_display_properties()` — All nodes have `name`, `display_color`, `display_icon`

## Directory Structure

```
core/
├── README.md                           ← You are here
├── scripts/
│   ├── neo4j_config.py                 ← Shared configuration
│   ├── create_schema.py                ← Schema setup
│   ├── validate_schema.py              ← Validation
│   ├── validate_extractions.py         ← JSON validation
│   ├── add_name_properties.py          ← Visualization setup
│   ├── add_display_properties.py       ← Visualization setup
│   └── import_all.py                   ← Orchestrator
├── data/
│   ├── bloom/                          ← Bloom perspectives
│   │   ├── perspectives/
│   │   │   └── main_perspective.json
│   │   └── README.md
│   └── curriculum-documents/           ← Source metadata
│       ├── metadata.json
│       └── README.md
└── docs/
    ├── graph_model_overview.md         ← Model documentation
    └── (more docs)
```

## Notes

- **Never hardcode credentials** — always use environment variables
- **Run validation after every import** — catch issues early
- **Schema must be created first** — constraints prevent duplicate nodes
- **Display properties are optional** — graph works without them, but visualization is much better with them
- **import_all.py respects dependencies** — layers are imported in the correct order
