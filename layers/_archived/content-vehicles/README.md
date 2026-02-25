# Content Vehicles Layer

**Teaching packs that deliver curriculum concepts — the HOW behind the WHAT.**

## Purpose

The graph tells teachers WHAT to teach (concepts, objectives, domains) but not HOW to deliver it or WHAT materials to use. Content vehicles are structured bundles of resources, activities, definitions, and assessment guidance tied to curriculum concepts.

Teachers choose between multiple packs for the same concept — "Roman Britain" and "Anglo-Saxon England" are different vehicles that both deliver the same History concepts (cause and consequence, significance, evidence).

## Architecture

```
(:Domain)-[:HAS_VEHICLE]->(:ContentVehicle)-[:DELIVERS]->(:Concept)
(:ContentVehicle)-[:IMPLEMENTS]->(:Topic)  // optional link to Topics layer
```

**Many-to-many**: One vehicle delivers multiple concepts. One concept can be delivered by multiple vehicles.

### Relationship to Other Layers

| Layer | Role | Example |
|---|---|---|
| **Topics** (existing) | Thin curriculum-prescribed content groupings from the NC | "The Roman Empire and its Impact on Britain" |
| **ContentVehicle** (new) | Rich teaching packs with resources, definitions, assessment | Roman Britain pack with sources, figures, assessment criteria |
| **Oak Content** (future) | External provider content | Oak Academy lesson on Roman Britain |

## Vehicle Types

| Type | Subject | Example |
|---|---|---|
| `topic_study` | History | Roman Britain, Ancient Egypt |
| `case_study` | Geography | Haiti 2010 Earthquake, UK Urbanisation |
| `investigation` | Science | Friction Fair Test, Plant Growth Enquiry |
| `text_study` | English | Adventure Narrative, Persuasive Writing |
| `worked_example_set` | Maths | Place Value with Dienes, Bus Stop Division |

## Node Properties

### Universal (all vehicle types)

| Property | Type | Required | Description |
|---|---|---|---|
| `vehicle_id` | string | Yes | Unique ID (e.g. `HI-KS2-CV001`) |
| `name` | string | Yes | Human-readable name |
| `vehicle_type` | string | Yes | One of the vehicle types above |
| `subject` | string | Yes | Subject name |
| `key_stage` | string | Yes | Key stage (e.g. `KS2`) |
| `description` | string | Yes | What this pack covers and why |
| `definitions` | string[] | Yes | Key vocabulary specific to this pack |
| `assessment_guidance` | string | Yes | How to test understanding through this vehicle |
| `success_criteria` | string[] | Yes | What mastery looks like |
| `resources` | string[] | No | References/URLs to images, assets, video |
| `resource_types` | string[] | No | Parallel array: `image`, `video`, `document`, etc. |
| `display_category` | string | Yes | Always `"Content Vehicle"` |

### Subject-Specific Properties

**History** (`topic_study`): `period`, `key_figures`, `key_events`, `sources`, `source_types`, `perspectives`

**Geography** (`case_study`): `location`, `data_points`, `themes`, `contrasting_with`, `map_types`, `data_sources`

**Science** (`investigation`): `enquiry_type`, `variables_independent`, `variables_dependent`, `variables_controlled`, `equipment`, `recording_format`, `safety_notes`, `expected_outcome`

**English** (`text_study`): `genre`, `text_features`, `suggested_texts`, `reading_level`, `writing_outcome`, `grammar_focus`

**Maths** (`worked_example_set`): `cpa_stage`, `manipulatives`, `representations`, `difficulty_levels`, `common_errors`

## Data Files

JSON files in `layers/content-vehicles/data/`, one per subject/key-stage:

```
data/
  history_ks2.json
  history_ks3.json
  geography_ks3.json
  science_ks2.json
  science_ks3.json
  english_y4.json
  mathematics_y2.json
```

## Scripts

| Script | Purpose |
|---|---|
| `import_content_vehicles.py` | Import JSONs into Neo4j (MERGE-based, idempotent) |
| `generate_content_vehicles.py` | LLM-assisted generation of vehicle JSONs from graph data |

## Import

```bash
# After UK curriculum is imported
python3 layers/content-vehicles/scripts/import_content_vehicles.py
```

## V5 Teacher Review (2026-02-23)

Five simulated teacher personas reviewed the vehicles in context. Key findings:

- **Content readiness nearly doubled** — average 3.7/10 → 6.6/10
- **Data errors found and fixed:** 6/8 KS3 Science vehicles had wrong `delivers_concept_ids` (systematic domain offset); 3 KS2 Science vehicles mixed Working Scientifically process concepts into delivers; EN-Y4-CV004 recommended a baby book for Y4 poetry (replaced with age-appropriate Rosen collection)
- **Consensus remaining gaps:** no worked examples (despite `worked_example_set` type), no difficulty sub-levels, ~40% Geography statutory content not yet covered, thin safety notes on some Science vehicles, Thinking Lens rationales age-inappropriate for KS1

Full reports in `generated/teachers-v4/` (gitignored — lesson plans, teaching logs, v5 findings, group synthesis).

## Queries

```cypher
// All vehicles for a domain
MATCH (d:Domain {domain_id: 'HI-KS2-D002'})-[:HAS_VEHICLE]->(cv:ContentVehicle)
RETURN cv.name, cv.vehicle_type, cv.description

// Vehicles that deliver a specific concept
MATCH (cv:ContentVehicle)-[:DELIVERS]->(c:Concept {concept_id: 'HI-KS2-C001'})
RETURN cv.name, cv.vehicle_type, cv.assessment_guidance

// Vehicles implementing a topic
MATCH (cv:ContentVehicle)-[:IMPLEMENTS]->(t:Topic {topic_id: 'HI-KS2-TOPIC-002'})
RETURN cv.name, cv.definitions, cv.success_criteria

// Teacher choice: multiple vehicles for same concept
MATCH (cv:ContentVehicle)-[:DELIVERS]->(c:Concept {concept_id: 'HI-KS2-C001'})
RETURN cv.name, cv.description, cv.vehicle_type
ORDER BY cv.name
```
