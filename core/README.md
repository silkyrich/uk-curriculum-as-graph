# Core Infrastructure

Shared infrastructure for building and validating the knowledge graph. Schema management, import orchestration, validation, and Neo4j configuration used by all layers.

## Scripts

| Script | Purpose |
|---|---|
| `neo4j_config.py` | Neo4j connection config (reads environment variables) |
| `create_schema.py` | Create uniqueness constraints and indexes (run before any import) |
| `import_all.py` | Orchestrate import of all layers in dependency order |
| `validate_schema.py` | 40+ integrity checks: node completeness, relationship integrity, property completeness |
| `validate_extractions.py` | Validate JSON extraction files before import |

### Import orchestrator

`import_all.py` handles the full import pipeline in the correct order:

1. UK Curriculum (foundation -- structure, concepts, prerequisites)
2. EYFS (depends on UK Curriculum for cross-stage prerequisite links)
3. Concept grouping signals + CO_TEACHES relationships
4. ThinkingLens nodes + age-banded prompts
5. ConceptCluster generation (depends on ThinkingLens)
6. DifficultyLevel import
7. RepresentationStage import (primary maths CPA)
8. Cross-domain CO_TEACHES curations
9. Concept-level DEVELOPS_SKILL links
10. Delivery mode classification + import
11. Assessment (KS2 test frameworks)
12. Epistemic skills
13. Per-subject ontology (VehicleTemplates + typed study nodes)
14. CASE standards (optional, `--skip-case`)
15. Learner profiles
16. Visualization properties (display_color, display_icon, display_category)

Use `--skip-case` or `--skip-oak` to exclude optional layers.

## Migrations

`core/migrations/` contains three rerunnable enrichment scripts (not one-time fixes):

| Script | Purpose |
|---|---|
| `compute_lesson_grouping_signals.py` | Compute `is_keystone`, `prerequisite_fan_out`, create `CO_TEACHES` rels |
| `create_cross_domain_co_teaches.py` | Load curated cross-domain/cross-subject CO_TEACHES links |
| `create_concept_skill_links.py` | Load curated concept-level DEVELOPS_SKILL links |

These are idempotent -- safe to re-run after data changes.

## Compliance

`core/compliance/` contains the data governance framework:

| Document | Purpose |
|---|---|
| `DATA_CLASSIFICATION.md` | Mandatory tier classification for any data element |
| `CONSENT_RULES.md` | Consent requirements per processing purpose |
| `DPIA.md` | Data Protection Impact Assessment (skeleton, needs completion) |

No learner data exists in this repository. These documents define rules for any future system that processes learner data.

## Configuration

All scripts use `neo4j_config.py`, which reads:

```python
NEO4J_URI = os.getenv('NEO4J_URI', 'neo4j://127.0.0.1:7687')
NEO4J_USER = os.getenv('NEO4J_USERNAME', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password123')
```

## Schema constraints

Uniqueness constraints on ID properties for all node types:

- **UK Curriculum:** Curriculum, KeyStage, Year, Subject, Programme, Domain, Objective, Concept, SourceDocument
- **Derived layers:** ConceptCluster, ThinkingLens, DifficultyLevel, RepresentationStage, DeliveryMode, TeachingRequirement
- **Per-subject ontology:** HistoryStudy, GeoStudy, ScienceEnquiry, EnglishUnit, ArtTopicSuggestion, MusicTopicSuggestion, DTTopicSuggestion, ComputingTopicSuggestion, TopicSuggestion, VehicleTemplate + 12 reference node types
- **Assessment:** TestFramework, TestPaper, ContentDomainCode
- **Epistemic skills:** WorkingScientifically, ReadingSkill, HistoricalThinking, GeographicalSkill, MathematicalReasoning, ComputationalThinking
- **CASE standards:** Framework, Dimension, Practice, CoreIdea, PerformanceExpectation
- **Learner profiles:** InteractionType, ContentGuideline, PedagogyProfile, FeedbackProfile, PedagogyTechnique

## Validation

`validate_schema.py` runs checks in three categories:

- **Category I (Schema completeness):** All expected node types exist
- **Category II (Relationship integrity):** No dangling references, all relationship endpoints valid
- **Category III (Property completeness):** Required fields present on all nodes

All checks should PASS. The CI pipeline runs validation on every push to main.
