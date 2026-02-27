# Per-Subject Ontology Layer

Typed study/unit and reference nodes that describe **how** to teach curriculum concepts -- the pedagogical vehicles that deliver the statutory content. Replaces the earlier generic ContentVehicle and Topic layers (archived in `layers/_archived/`).

See also: [project direction](../../docs/design/PROJECT_DIRECTION.md) | [compilation targets](../../docs/design/OUTPUT_SCHEMAS.md) | [delivery modes](../../docs/design/PLAN_DELIVERY_MODE_CLASSIFICATION.md) | [UK curriculum layer](../uk-curriculum/README.md)

---

## Why typed nodes?

Each subject has fundamentally different pedagogical metadata. A history study needs periods, key figures, sources, and perspectives. A science enquiry needs variables, equipment, and misconceptions. A generic "TopicSuggestion" label with optional fields for everything would be sparse and confusing.

Instead, each subject gets its own node label with its own property schema. No irrelevant attributes on any node.

## Study node types

These are the "compilation units" -- the nodes that [teacher planners](../../docs/design/OUTPUT_SCHEMAS.md#schema-a-teacher-planner) and [session prompts](../../docs/design/OUTPUT_SCHEMAS.md#schema-b-llm-child-session-prompt) query to find the best vehicle for delivering a set of concepts.

| Label | Subject | Count | Key properties |
|---|---|---|---|
| `HistoryStudy` | History | 43 (KS1-KS4) | `period`, `key_figures`, `perspectives`, `key_question`, `chronological_position` |
| `GeoStudy` | Geography | 32 (KS1-KS4) | `study_type` (place/thematic/contrasting), `data_points`, `fieldwork_potential` |
| `ScienceEnquiry` | Science | 45 (KS1-KS4) | `enquiry_type`, `variables`, `equipment`, `safety_notes` |
| `EnglishUnit` | English | 54 (KS1-KS4) | `text_type`, `grammar_focus`, `writing_outcome`, `reading_focus` |
| `ArtTopicSuggestion` | Art & Design | 39 (KS1-KS4) | `medium`, `artists`, `techniques` |
| `MusicTopicSuggestion` | Music | 35 (KS1-KS4) | `musical_elements`, `listening_pieces`, `performance_type` |
| `DTTopicSuggestion` | Design & Technology | 33 (KS1-KS4) | `materials`, `tools`, `design_brief` |
| `ComputingTopicSuggestion` | Computing | 22 (KS1-KS3) | `programming_language`, `computational_concepts` |
| `TopicSuggestion` | RE, Citizenship, etc. | 23 | Generic; `suggestion_type` distinguishes subject |

All study nodes have: `name`, `key_stage`, `curriculum_status` (mandatory/optional/flexible), `duration_lessons`, `success_criteria[]`, `assessment_guidance`, `common_pitfalls[]`, `sensitive_content_notes`.

## Reference node types

Subject-specific reference data that study nodes link to. These enrich the pedagogical context without cluttering the study node properties.

| Label | Subject | Count | Purpose |
|---|---|---|---|
| `DisciplinaryConcept` | History | -- | Second-order concepts (causation, significance, etc.) |
| `HistoricalSource` | History | -- | Source types (written, visual, oral, artefact) |
| `GeoPlace` | Geography | -- | Named places for place studies |
| `GeoContrast` | Geography | -- | Contrasting locality pairs |
| `EnquiryType` | Science | -- | Enquiry methodologies (fair test, pattern seeking, etc.) |
| `Misconception` | Science | -- | Common misconceptions with counter-prompts |
| `Genre` | English | -- | Text types and genres |
| `SetText` | English | -- | KS4 set text specifications |
| `MathsManipulative` | Maths | -- | Physical/virtual manipulatives (Dienes, Numicon, etc.) |
| `MathsRepresentation` | Maths | -- | Visual representations (bar model, number line, etc.) |
| `MathsContext` | Maths | -- | Real-world application contexts |
| `ReasoningPromptType` | Maths | -- | Reasoning prompt patterns (prove it, explain why, etc.) |

## VehicleTemplate nodes

24 reusable pedagogical patterns (e.g. "Topic Study", "Enquiry Investigation", "Design-Make-Evaluate") with age-banded `agent_prompt` per KeyStage via `TEMPLATE_FOR` relationships. Study nodes link to templates via `USES_TEMPLATE`.

Used by [session prompts](../../docs/design/OUTPUT_SCHEMAS.md#output-contract-1) to determine session structure and by [parent guides](../../docs/design/OUTPUT_SCHEMAS.md#schema-c-parent-home-educator-guide) to shape the lesson flow.

## Key relationships

```
(:Domain)-[:HAS_SUGGESTION]->(study)                      # domain delivers via studies
(study)-[:DELIVERS_VIA {primary: bool}]->(:Concept)       # many-to-many concept delivery
(study)-[:USES_TEMPLATE]->(:VehicleTemplate)              # pedagogical pattern
(study)-[:CROSS_CURRICULAR {hook, strength}]->(study2)    # cross-subject connections

# Subject-specific
(:HistoryStudy)-[:FOREGROUNDS]->(:DisciplinaryConcept)
(:HistoryStudy)-[:USES_SOURCE]->(:HistoricalSource)
(:HistoryStudy)-[:CHRONOLOGICALLY_FOLLOWS]->(:HistoryStudy)
(:GeoStudy)-[:LOCATED_IN]->(:GeoPlace)
(:GeoStudy)-[:CONTRASTS_WITH]->(:GeoContrast)
(:ScienceEnquiry)-[:USES_ENQUIRY_TYPE]->(:EnquiryType)
(:ScienceEnquiry)-[:ADDRESSES_MISCONCEPTION]->(:Misconception)
(:EnglishUnit)-[:IN_GENRE]->(:Genre)
(:EnglishUnit)-[:STUDIES_TEXT]->(:SetText)
```

## Import

```bash
# Vehicle templates first (study nodes reference them)
python3 layers/topic-suggestions/scripts/import_vehicle_templates.py

# All subject ontologies
python3 layers/topic-suggestions/scripts/import_subject_ontologies.py

# Re-import after data changes
python3 layers/topic-suggestions/scripts/import_subject_ontologies.py --clear
```

## Data files

Organised by subject in `data/`:

```
data/
  vehicle_templates.json              # 24 template definitions
  vehicle_template_ks_prompts.json    # age-banded prompts
  history_studies/                    # KS1-KS4 HistoryStudy JSONs
  geo_studies/                        # KS1-KS4 GeoStudy JSONs
  science_enquiries/                  # KS1-KS4 ScienceEnquiry JSONs
  english_units/                      # KS1-KS4 EnglishUnit JSONs
  art_studies/                        # KS1-KS4 ArtTopicSuggestion JSONs
  music_studies/                      # KS1-KS4 MusicTopicSuggestion JSONs
  dt_studies/                         # KS1-KS4 DTTopicSuggestion JSONs
  computing_studies/                  # KS1-KS3 ComputingTopicSuggestion JSONs
  generic_studies/                    # RE, Citizenship TopicSuggestion JSONs
  history_disciplinary_concepts/      # DisciplinaryConcept definitions
  history_sources/                    # HistoricalSource definitions
  geo_places/                         # GeoPlace definitions
  geo_contrasts/                      # GeoContrast definitions
  science_enquiry_types/              # EnquiryType definitions
  science_misconceptions/             # Misconception definitions
  english_genres/                     # Genre definitions
  english_set_texts/                  # SetText definitions
  maths_manipulatives/                # MathsManipulative definitions
  maths_representations/              # MathsRepresentation definitions
  maths_contexts/                     # MathsContext definitions
  maths_reasoning/                    # ReasoningPromptType definitions
```

## How compilation targets use this layer

| Target | What it pulls | Details |
|---|---|---|
| [Teacher planner](../../docs/design/OUTPUT_SCHEMAS.md#schema-a-teacher-planner) | Best-fit study node + all subject references + cross-curricular links + vehicle template | [Output contract](../../docs/design/OUTPUT_SCHEMAS.md#output-contract) |
| [LLM session prompt](../../docs/design/OUTPUT_SCHEMAS.md#schema-b-llm-child-session-prompt) | Pre-selected study (enquiry question + pitfalls only) + vehicle template session structure | [Output contract](../../docs/design/OUTPUT_SCHEMAS.md#output-contract-1) |
| [Parent guide](../../docs/design/OUTPUT_SCHEMAS.md#schema-c-parent-home-educator-guide) | Study as lesson shape + vehicle template for step ordering | [Generation prompt](../../docs/design/OUTPUT_SCHEMAS.md#generation-prompt-structure) |
