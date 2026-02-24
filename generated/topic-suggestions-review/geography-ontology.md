# Geography Ontology Design: Subject-Specific Graph Model

**Author**: KS2 + KS3 Geography Specialist
**Date**: 2026-02-24
**Status**: DESIGN PROPOSAL
**Scope**: Complete replacement of `GeographyTopicSuggestion` with a Geography-native graph model

---

## 0. Design Rationale: Why Geography Needs Its Own Ontology

The universal `TopicSuggestion` wrapper failed Geography for three structural reasons:

1. **Geography studies places, not topics.** History studies events, English studies texts, Science studies phenomena. Geography studies *places* — and a place is not a property of a topic, it IS the topic. Cramming "Lagos, Nigeria and London, UK" into a `locations: string[]` property on a topic node is like cramming "Pride and Prejudice" into a `texts: string[]` property on an English topic node. The place deserves to be a first-class node.

2. **Contrasting localities are a structural relationship, not a string cross-reference.** The National Curriculum mandates comparing places at every key stage. A `contrasting_with: "TS-GE-KS1-004"` property captures that two topics are paired, but it does not capture *why* they contrast (development level, climate, scale, governance) or *what dimensions* of contrast are pedagogically productive. The contrast is a rich relationship, not a pointer.

3. **Geography has three fundamentally different study types that require different data structures.** A place study (build layered understanding of Lagos), a thematic study (rivers and the water cycle), and a fieldwork investigation (measure river velocity at five points) need different properties, different session structures, and different AI tutor prompts. A single flat node with optional properties does not capture these distinctions — it just accumulates nulls.

The design below addresses all three failures by separating **places** from **studies**, making **contrasts** first-class relationships with properties, and using **study type** as a structural organiser rather than an enum.

---

## 1. Node Labels

Geography needs **three** node labels, not one.

### 1.1 `:GeoPlace`

A discrete geographical location that can be studied, mapped, and compared. This is the fundamental unit of Geography — everything in the subject is *about* places.

**Why a separate node?** Because:
- The same place appears in multiple studies across key stages (the UK is studied at KS1, KS2, and KS3 in completely different ways)
- Places have inherent properties (coordinates, scale, continent, climate zone) that are facts about the place, not about any study that uses the place
- Contrasting locality pairs are relationships BETWEEN places, not between studies
- An AI tutor generating a map needs to geocode a place, regardless of which study it appears in
- A place can be shared across subjects (Nigeria appears in Geography KS3 development AND History KS3 colonial Africa)

### 1.2 `:GeoStudy`

A specific unit of geographical study that uses one or more places to teach curriculum concepts. This is the "what do we teach?" node — it connects places to curriculum, specifies the pedagogical approach, and carries the AI-generation metadata.

**Why not just use `GeographyTopicSuggestion`?** Because the word "topic" is overloaded. In Geography, a "topic" could mean rivers (a physical process), Nigeria (a place), or fieldwork (a skill). `GeoStudy` is precise: it is a planned unit of geographical study with a defined approach, places, and curriculum targets.

### 1.3 `:GeoContrast`

A curated pairing of two `GeoPlace` nodes (or two `GeoStudy` nodes) that captures the National Curriculum's contrasting locality requirement. This is a relationship-with-properties pattern, but the richness of contrast data (dimensions of contrast, pedagogical purpose, stimulus questions) justifies a first-class node rather than a property-laden relationship.

**Why a node instead of a relationship?** Because:
- A contrast has multiple dimensions (e.g. Haiti vs Japan contrasts on development level, preparedness, governance, AND casualty toll — these are not a single string)
- Contrasts have their own pedagogical rationale and stimulus questions
- A contrast can link two places (generic: "UK locality vs Kenyan village") or two studies (specific: "Haiti earthquake case study vs Japan earthquake case study")
- The AI tutor needs the contrast framing as a discrete queryable entity to generate comparison tasks

---

## 2. Property Tables

### 2.1 `:GeoPlace` Properties

| Property | Type | Required | Rationale |
|---|---|---|---|
| `place_id` | string | Yes | Unique identifier. Format: `GP-{CONTINENT_CODE}-{sequence}` (e.g. `GP-AF-001` for Nigeria, `GP-EU-001` for UK, `GP-LOCAL` for school locality) |
| `name` | string | Yes | Display name (e.g. "Nigeria", "Lake District", "Port-au-Prince") |
| `formal_name` | string | No | Full formal name if different from display name (e.g. "Federal Republic of Nigeria") |
| `place_type` | string | Yes | Controlled vocabulary: `country`, `region`, `city`, `locality`, `continent`, `global`, `physical_feature` |
| `continent` | string | Yes | Controlled: `Africa`, `Antarctica`, `Asia`, `Australasia`, `Europe`, `North_America`, `South_America`, `Global`, `Multiple` |
| `country` | string | No | ISO country name if applicable (null for continents and global) |
| `lat` | float | No | Latitude for geocoding/map generation (null for "school locality" adaptive places) |
| `lon` | float | No | Longitude for geocoding/map generation |
| `scale` | string | Yes | Controlled: `local`, `regional`, `national`, `continental`, `global` |
| `climate_zone` | string | No | Controlled: `tropical`, `arid`, `temperate`, `continental`, `polar`, `multiple` |
| `development_classification` | string | No | Controlled: `HIC`, `LIC`, `NEE`, `not_applicable` (for physical features, global) |
| `is_adaptive` | boolean | Yes | `true` if the place is determined by the school (e.g. "our local area", "a European region"). Signals to AI: do not hardcode, prompt for specifics |
| `exemplar_choices` | string[] | No | For adaptive places: common school choices (e.g. `["Kenya village", "Indian city", "Chinese village"]` for the KS1 non-European slot) |
| `key_physical_features` | string[] | No | Notable physical geography (e.g. `["River Niger", "Sahel", "Jos Plateau"]`) |
| `key_human_features` | string[] | No | Notable human geography (e.g. `["Lagos", "oil industry", "Nollywood"]`) |
| `display_category` | string | Yes | Always `"Geography"` |
| `display_color` | string | Yes | `"#059669"` (Emerald-600, matching Geography's existing colour) |
| `display_icon` | string | Yes | `"place"` (Material icon) |

**Design notes:**
- `is_adaptive` is critical. Geography has many "open slot" studies where the school picks the place. The AI cannot hardcode "Kenya" when some schools study "Ghana" or "India". The `is_adaptive: true` flag tells the AI to ask the learner (or use the school's configuration) to resolve the place.
- `exemplar_choices` provides common defaults for adaptive places, which an AI can offer as suggestions.
- `lat`/`lon` are optional because adaptive places have no fixed coordinates. When present, they enable map generation and spatial queries ("show me all GeoPlaces in Africa").

### 2.2 `:GeoStudy` Properties

| Property | Type | Required | Rationale |
|---|---|---|---|
| `study_id` | string | Yes | Unique identifier. Format: `GS-GE-{KS}-{sequence}` (e.g. `GS-GE-KS1-001`) |
| `name` | string | Yes | Display name (e.g. "Rivers and the Water Cycle", "Haiti 2010 Earthquake") |
| `study_type` | string | Yes | Controlled vocabulary: `place_study`, `thematic_study`, `case_study`, `fieldwork_investigation`, `decision_making_exercise` (see section 3 for rationale) |
| `subject` | string | Yes | Always `"Geography"` |
| `key_stage` | string | Yes | `KS1`, `KS2`, `KS3` |
| `year_groups` | string[] | No | Specific years if narrower than full KS (e.g. `["Y5", "Y6"]`) |
| `curriculum_status` | string | Yes | Controlled: `mandatory`, `exemplar`, `convention` |
| `suggestion_type` | string | Yes | Controlled: `prescribed_topic`, `exemplar_topic`, `open_slot`, `teacher_convention` (retained for compatibility) |
| `choice_group` | string | No | Groups mutually exclusive alternatives (e.g. `"tectonic_hazards_case_study"`) |
| `curriculum_reference` | string[] | No | Direct NC quotations this study addresses |
| `theme_category` | string | Yes | Controlled: `physical`, `human`, `environmental`, `economic`, `social`, `political`, `integrated` |
| `themes` | string[] | Yes | Specific thematic concepts (e.g. `["vulnerability", "development", "governance"]`) |
| `scale` | string | Yes | Dominant spatial scale: `local`, `regional`, `national`, `continental`, `global` |
| `map_types` | string[] | Yes | Controlled vocabulary of map/visual types appropriate to this study (see section 4) |
| `data_sources` | string[] | Yes | Named data sources appropriate to key stage (e.g. `["USGS", "World Bank"]` at KS3, `["classroom globe", "photographs"]` at KS1) |
| `definitions` | string[] | Yes | Specialist vocabulary for this study, in teaching order |
| `pedagogical_rationale` | string | Yes | Why this study matters and how it builds geographical understanding |
| `common_pitfalls` | string[] | No | Common teaching/learning errors |
| `cross_curricular_hooks` | string[] | No | Format: `"[Subject] specific connection"` |
| `sensitive_content_notes` | string[] | No | Content requiring careful handling |
| `fieldwork_potential` | string | No | Description of possible fieldwork activities, or null if not applicable |
| `duration_lessons` | int | No | Suggested number of lessons |
| `enquiry_question` | string | No | The driving geographical question (e.g. "Why did so many people die in the Haiti earthquake?") |
| `data_points` | string[] | No | Key statistics and factual data for the AI to use (e.g. `["Magnitude 7.0", "230,000+ deaths"]`) |
| `assessment_guidance` | string | No | What pupils should be able to do/explain by the end |
| `success_criteria` | string[] | No | Observable success indicators |
| `display_category` | string | Yes | Always `"Geography"` |
| `display_color` | string | Yes | `"#059669"` |
| `display_icon` | string | Yes | Icon varies by `study_type` (see section 3) |

### 2.3 `:GeoContrast` Properties

| Property | Type | Required | Rationale |
|---|---|---|---|
| `contrast_id` | string | Yes | Unique identifier. Format: `GC-{KS}-{sequence}` (e.g. `GC-KS1-001`) |
| `name` | string | Yes | Display name (e.g. "Our Locality vs Non-European Locality", "Haiti vs Japan") |
| `contrast_type` | string | Yes | Controlled: `contrasting_locality` (NC statutory), `development_contrast` (HIC vs LIC), `hazard_contrast`, `scale_contrast`, `thematic_contrast` |
| `dimensions` | string[] | Yes | What dimensions of contrast are pedagogically productive (e.g. `["development level", "governance", "preparedness", "casualty toll"]`) |
| `stimulus_questions` | string[] | No | Questions that drive the comparison (e.g. `["Why did 230,000 people die in Haiti but only 20,000 in Japan, despite Japan's earthquake being far more powerful?"]`) |
| `nc_requirement` | string | No | Which NC requirement this contrast fulfils (e.g. "KS1: contrasting non-European locality") |
| `pedagogical_rationale` | string | Yes | Why this contrast is pedagogically valuable |
| `display_category` | string | Yes | Always `"Geography"` |
| `display_color` | string | Yes | `"#10B981"` (Emerald-500, slightly lighter than GeoPlace/GeoStudy) |
| `display_icon` | string | Yes | `"compare_arrows"` (Material icon) |

---

## 3. Study Types and Their Significance

The `study_type` property on `:GeoStudy` is not just an enum — it determines the pedagogical structure of the unit. Each type implies a different session flow, different AI tutor behaviour, and different assessment patterns.

| study_type | Description | Session structure | Display icon | KS prevalence |
|---|---|---|---|---|
| `place_study` | Build layered understanding of a specific place through physical, human, economic, and cultural lenses | `locate -> describe_physical -> describe_human -> explain_interactions -> compare -> evaluate_change` | `travel_explore` | KS1 (dominant), KS2, KS3 |
| `thematic_study` | Study a geographical theme or process using exemplar places | `define_process -> observe_patterns -> explain_causes -> explore_impacts -> evaluate_responses` | `category` | KS2 (dominant), KS3 |
| `case_study` | In-depth analysis of a specific geographical event or situation using evidence | `locate_and_describe -> data_collection -> analysis -> comparison -> evaluation` | `case_study` (custom) | KS3 (dominant) |
| `fieldwork_investigation` | Design and carry out a geographical enquiry collecting primary data | `question -> methodology -> data_collection -> presentation -> analysis -> evaluation` | `explore` | All KS (statutory) |
| `decision_making_exercise` | Evaluate evidence from multiple stakeholder perspectives to reach a justified geographical decision | `context -> stakeholder_identification -> evidence_gathering -> perspective_analysis -> decision -> justification` | `gavel` | KS3 |

**Why these five and not fewer?** Because the AI tutor needs to know the pedagogical shape of the lesson, not just the content. A `place_study` of Lagos starts with "Where is Lagos? What does it look like?" (locate and describe). A `case_study` of the Lagos urbanisation crisis starts with "Lagos has grown from 1 million to 16 million in 50 years — why?" (evidence and analysis). Same place, completely different pedagogy.

**Why these five and not more?** The `mystery` template from my earlier review could be a sixth, but it is better modelled as a variant of `case_study` with a specific `enquiry_question` format ("Why did...?") rather than a separate type. The template system (VehicleTemplate) can handle the mystery structure without a new study type.

---

## 4. Map Types Controlled Vocabulary

Maps are the language of Geography. The `map_types` property on `:GeoStudy` uses a controlled vocabulary that progresses with key stage:

### KS1 Map Types
`globe`, `picture_map`, `aerial_photo`, `simple_plan`, `world_political_map`, `uk_political_map`, `labelling_map`

### KS2 Map Types
All KS1 types plus: `os_map`, `atlas_map`, `satellite_image`, `thematic_map`, `weather_map`, `climate_graph`, `cross_section`, `river_basin_map`, `land_use_map`, `trade_flow_map`, `resource_distribution_map`

### KS3 Map Types
All KS2 types plus: `gis`, `choropleth`, `isoline`, `flow_map`, `dot_map`, `proportional_symbol`, `topographic`, `hazard_overlay`, `population_density`, `vulnerability_index`, `time_series_satellite`

The AI tutor uses `map_types` to determine what visual resources to reference, generate, or prompt the learner to interpret. A KS1 lesson must never reference a choropleth; a KS3 lesson should expect GIS interpretation.

---

## 5. Relationship Model

### 5.1 Relationships TO/FROM Other Graph Nodes

```
(:GeoStudy)-[:DELIVERS_VIA {primary: bool}]->(:Concept)
(:GeoStudy)-[:USES_TEMPLATE]->(:VehicleTemplate)
(:Domain)-[:HAS_STUDY]->(:GeoStudy)
(:ConceptCluster)-[:SUGGESTED_STUDY {rank: int}]->(:GeoStudy)
(:GeoStudy)-[:STUDIES]->(:GeoPlace)
(:GeoPlace)-[:IN_CONTINENT]->(:GeoPlace)  // e.g. Nigeria -[:IN_CONTINENT]-> Africa
```

### 5.2 Relationships BETWEEN Geography Nodes

```
// Place-to-place: structural geography
(:GeoPlace)-[:LOCATED_IN]->(:GeoPlace)          // city in country, region in continent
(:GeoPlace)-[:SHARES_BORDER_WITH]->(:GeoPlace)  // adjacency (optional, for KS3 geopolitics)

// Contrast: the NC's contrasting locality requirement
(:GeoContrast)-[:CONTRASTS_PLACE {role: str}]->(:GeoPlace)     // role = 'place_a' or 'place_b'
(:GeoContrast)-[:CONTRASTS_STUDY {role: str}]->(:GeoStudy)     // role = 'study_a' or 'study_b'
(:GeoStudy)-[:PART_OF_CONTRAST]->(:GeoContrast)                // convenience traversal

// Study-to-study: sequencing and progression
(:GeoStudy)-[:BUILDS_ON]->(:GeoStudy)           // prerequisite study (e.g. KS1 weather -> KS2 climate zones)
(:GeoStudy)-[:COMPLEMENTS]->(:GeoStudy)         // studies that benefit from being taught alongside

// Place-to-study: the core teaching relationship
(:GeoStudy)-[:STUDIES {role: str}]->(:GeoPlace)  // role = 'primary' or 'comparison' or 'case_study'
```

### 5.3 Relationship Diagram (ASCII)

```
                                        (:Domain)
                                            |
                                       [:HAS_STUDY]
                                            |
                                            v
(:VehicleTemplate) <--[:USES_TEMPLATE]-- (:GeoStudy) --[:DELIVERS_VIA {primary}]--> (:Concept)
                                            |    |
                                   [:STUDIES |    | [:PART_OF_CONTRAST]
                                   {role}]  |    |
                                            v    v
                                     (:GeoPlace)  (:GeoContrast)
                                        |    ^         |
                                        |    |         |[:CONTRASTS_PLACE {role}]
                               [:IN_    |    |         |
                              CONTINENT]|    +---------+
                                        v
                                     (:GeoPlace)  // continent node

(:ConceptCluster) --[:SUGGESTED_STUDY {rank}]--> (:GeoStudy)
(:GeoStudy) --[:BUILDS_ON]--> (:GeoStudy)     // cross-KS progression
```

---

## 6. Example Instances

### 6.1 KS1: "Our Local Area" + "Kenyan Village" Contrasting Locality Study

**GeoPlace nodes:**

```json
{
  "place_id": "GP-EU-001",
  "name": "School Locality",
  "place_type": "locality",
  "continent": "Europe",
  "country": "United Kingdom",
  "scale": "local",
  "is_adaptive": true,
  "exemplar_choices": ["Village in Hampshire", "Estate in Manchester", "Town in Yorkshire"],
  "key_physical_features": ["Determined by school location"],
  "key_human_features": ["Determined by school location"]
}
```

```json
{
  "place_id": "GP-AF-001",
  "name": "Kenyan Village",
  "place_type": "locality",
  "continent": "Africa",
  "country": "Kenya",
  "lat": -1.286,
  "lon": 36.817,
  "scale": "local",
  "climate_zone": "tropical",
  "development_classification": "LIC",
  "is_adaptive": false,
  "key_physical_features": ["savanna grassland", "seasonal rainfall", "red soil"],
  "key_human_features": ["farming village", "market", "school", "community well"]
}
```

**GeoStudy nodes:**

```json
{
  "study_id": "GS-GE-KS1-001",
  "name": "Our Local Area",
  "study_type": "place_study",
  "key_stage": "KS1",
  "curriculum_status": "mandatory",
  "suggestion_type": "open_slot",
  "theme_category": "integrated",
  "themes": ["local geography", "observation", "human and physical features"],
  "scale": "local",
  "map_types": ["simple_plan", "picture_map", "aerial_photo"],
  "data_sources": ["Pupil observation", "Local photographs", "Google Earth"],
  "definitions": ["local area", "physical feature", "human feature", "map", "compare"],
  "pedagogical_rationale": "The local area study grounds abstract concepts in direct experience...",
  "fieldwork_potential": "Walking survey of school grounds observing human and physical features",
  "enquiry_question": "What is our local area like?"
}
```

```json
{
  "study_id": "GS-GE-KS1-004",
  "name": "Contrasting Non-European Locality Study",
  "study_type": "place_study",
  "key_stage": "KS1",
  "curriculum_status": "mandatory",
  "suggestion_type": "open_slot",
  "theme_category": "human",
  "themes": ["place comparison", "cultural diversity", "similarities and differences"],
  "scale": "local",
  "map_types": ["world_political_map", "simple_plan", "aerial_photo"],
  "data_sources": ["Photographs", "Video resources", "Google Earth"],
  "definitions": ["locality", "compare", "contrast", "similarities", "differences"],
  "pedagogical_rationale": "Ensures pupils' earliest geography extends beyond Europe...",
  "sensitive_content_notes": ["Avoid charity tourism framing", "Pupils of heritage culture may have personal connections"]
}
```

**GeoContrast node:**

```json
{
  "contrast_id": "GC-KS1-001",
  "name": "UK Locality vs Non-European Locality",
  "contrast_type": "contrasting_locality",
  "dimensions": ["climate", "settlement type", "daily life", "physical features", "economic activity"],
  "stimulus_questions": [
    "How is the Kenyan village the same as our area? How is it different?",
    "What do children in the Kenyan village do that is the same as what you do?"
  ],
  "nc_requirement": "KS1: study a small area in a contrasting non-European country",
  "pedagogical_rationale": "The NC mandates that KS1 pupils compare a UK locality with a non-European locality to develop early comparative geographical thinking and openness to diverse human geographies."
}
```

**Relationships:**
```
(GS-GE-KS1-001)-[:STUDIES {role: 'primary'}]->(GP-EU-001)
(GS-GE-KS1-004)-[:STUDIES {role: 'primary'}]->(GP-AF-001)
(GC-KS1-001)-[:CONTRASTS_STUDY {role: 'study_a'}]->(GS-GE-KS1-001)
(GC-KS1-001)-[:CONTRASTS_STUDY {role: 'study_b'}]->(GS-GE-KS1-004)
(GC-KS1-001)-[:CONTRASTS_PLACE {role: 'place_a'}]->(GP-EU-001)
(GC-KS1-001)-[:CONTRASTS_PLACE {role: 'place_b'}]->(GP-AF-001)
(GS-GE-KS1-001)-[:PART_OF_CONTRAST]->(GC-KS1-001)
(GS-GE-KS1-004)-[:PART_OF_CONTRAST]->(GC-KS1-001)
(GP-AF-001)-[:IN_CONTINENT]->(GP-AF-CONTINENT)  // Kenya -> Africa
```

### 6.2 KS2: "Rivers and the Water Cycle" Thematic Study

**GeoPlace node:**

```json
{
  "place_id": "GP-EU-010",
  "name": "River Thames",
  "place_type": "physical_feature",
  "continent": "Europe",
  "country": "United Kingdom",
  "lat": 51.508,
  "lon": -0.076,
  "scale": "regional",
  "climate_zone": "temperate",
  "is_adaptive": false,
  "key_physical_features": ["source in Cotswolds", "meanders at Oxford", "tidal estuary at London", "215 miles long"],
  "key_human_features": ["London", "flood barrier", "historic trade route", "tourism"]
}
```

**GeoStudy node:**

```json
{
  "study_id": "GS-GE-KS2-004",
  "name": "Rivers and the Water Cycle",
  "study_type": "thematic_study",
  "key_stage": "KS2",
  "curriculum_status": "mandatory",
  "suggestion_type": "prescribed_topic",
  "theme_category": "physical",
  "themes": ["river processes", "water cycle", "erosion and deposition", "landscape formation"],
  "scale": "regional",
  "map_types": ["river_basin_map", "os_map", "cross_section", "satellite_image"],
  "data_sources": ["Environment Agency", "Ordnance Survey", "Met Office rainfall data", "Google Earth"],
  "definitions": ["river", "source", "mouth", "tributary", "drainage basin", "meander", "flood plain", "erosion", "deposition", "water cycle", "evaporation", "condensation", "precipitation"],
  "pedagogical_rationale": "Connects observable local features to global-scale processes...",
  "fieldwork_potential": "Local river study measuring width, depth, and flow velocity at different points",
  "enquiry_question": "How does water shape the landscape?",
  "cross_curricular_hooks": [
    "[Science] States of matter — evaporation, condensation, precipitation",
    "[Maths] Measuring rainfall, calculating river flow rates",
    "[History] Historical importance of rivers for settlement and trade"
  ]
}
```

**Relationships:**
```
(GS-GE-KS2-004)-[:STUDIES {role: 'primary'}]->(GP-EU-010)    // River Thames as exemplar
(GS-GE-KS2-004)-[:DELIVERS_VIA {primary: true}]->(GE-KS2-C003)  // river processes concept
(GS-GE-KS2-004)-[:BUILDS_ON]->(GS-GE-KS1-005)               // builds on KS1 weather/water
(GE-KS2-D003)-[:HAS_STUDY]->(GS-GE-KS2-004)                  // domain: Physical Geography
```

### 6.3 KS3: "Haiti vs Japan" Hazard Contrast

**GeoPlace nodes:**

```json
{
  "place_id": "GP-NA-001",
  "name": "Port-au-Prince",
  "place_type": "city",
  "continent": "North_America",
  "country": "Haiti",
  "lat": 18.541,
  "lon": -72.336,
  "scale": "national",
  "climate_zone": "tropical",
  "development_classification": "LIC",
  "is_adaptive": false,
  "key_physical_features": ["Caribbean plate boundary", "deforested hillsides", "coastal plain"],
  "key_human_features": ["2 million population", "informal settlements", "limited infrastructure", "NGO presence"]
}
```

```json
{
  "place_id": "GP-AS-001",
  "name": "Tohoku Region",
  "place_type": "region",
  "continent": "Asia",
  "country": "Japan",
  "lat": 38.268,
  "lon": 140.872,
  "scale": "national",
  "climate_zone": "temperate",
  "development_classification": "HIC",
  "is_adaptive": false,
  "key_physical_features": ["Pacific Ring of Fire", "subduction zone", "coastal plain", "mountainous interior"],
  "key_human_features": ["Sendai (1 million)", "Fukushima nuclear plant", "tsunami walls", "early warning systems"]
}
```

**GeoStudy nodes:**

```json
{
  "study_id": "GS-GE-KS3-001",
  "name": "Haiti 2010 Earthquake",
  "study_type": "case_study",
  "key_stage": "KS3",
  "curriculum_status": "exemplar",
  "suggestion_type": "exemplar_topic",
  "choice_group": "tectonic_hazards_case_study",
  "theme_category": "physical",
  "themes": ["vulnerability", "development", "governance", "international aid effectiveness"],
  "scale": "national",
  "map_types": ["hazard_overlay", "gis", "population_density", "choropleth"],
  "data_sources": ["USGS", "World Bank", "UN OCHA", "Red Cross"],
  "definitions": ["epicentre", "magnitude", "tectonic plate", "conservative boundary", "vulnerability", "resilience", "HDI", "aid dependency"],
  "data_points": ["Magnitude 7.0", "230,000+ deaths", "1.5 million displaced", "GDP $7 billion", "HDI rank 168/189"],
  "enquiry_question": "Why did so many people die in the Haiti earthquake?",
  "sensitive_content_notes": ["Significant loss of life — handle with sensitivity", "Avoid deficit framing of Haitian people"]
}
```

```json
{
  "study_id": "GS-GE-KS3-002",
  "name": "Japan 2011 Earthquake and Tsunami",
  "study_type": "case_study",
  "key_stage": "KS3",
  "curriculum_status": "exemplar",
  "suggestion_type": "exemplar_topic",
  "choice_group": "tectonic_hazards_case_study",
  "theme_category": "physical",
  "themes": ["preparedness", "resilience", "technology", "cascading hazards"],
  "scale": "national",
  "map_types": ["hazard_overlay", "gis", "population_density", "topographic"],
  "data_sources": ["USGS", "Japan Meteorological Agency", "IAEA", "World Bank"],
  "definitions": ["subduction zone", "tsunami", "seismometer", "early warning system", "resilience", "Richter scale", "nuclear meltdown"],
  "data_points": ["Magnitude 9.1", "c.20,000 deaths", "Tsunami wave height up to 40m", "Fukushima nuclear meltdown"],
  "enquiry_question": "Can technology make a country safe from tectonic hazards?"
}
```

**GeoContrast node:**

```json
{
  "contrast_id": "GC-KS3-001",
  "name": "Haiti vs Japan: Development and Disaster",
  "contrast_type": "hazard_contrast",
  "dimensions": ["development level", "governance quality", "preparedness infrastructure", "casualty toll relative to magnitude", "cascading effects", "international response"],
  "stimulus_questions": [
    "Japan's earthquake was 100x more powerful than Haiti's. Why did Haiti lose 10x more people?",
    "Does money make you safe from earthquakes?",
    "What does the Fukushima meltdown tell us about the limits of preparedness?"
  ],
  "nc_requirement": "KS3: detailed place-based exemplars for plate tectonics",
  "pedagogical_rationale": "The Haiti-Japan pairing is the most widely used tectonic hazard contrast in English secondary schools because the two events occurred within 14 months of each other, enabling clean comparison while exposing the critical role of development and governance in disaster outcomes."
}
```

**Relationships:**
```
(GS-GE-KS3-001)-[:STUDIES {role: 'primary'}]->(GP-NA-001)    // Haiti study -> Port-au-Prince
(GS-GE-KS3-002)-[:STUDIES {role: 'primary'}]->(GP-AS-001)    // Japan study -> Tohoku
(GC-KS3-001)-[:CONTRASTS_STUDY {role: 'study_a'}]->(GS-GE-KS3-001)
(GC-KS3-001)-[:CONTRASTS_STUDY {role: 'study_b'}]->(GS-GE-KS3-002)
(GC-KS3-001)-[:CONTRASTS_PLACE {role: 'place_a'}]->(GP-NA-001)
(GC-KS3-001)-[:CONTRASTS_PLACE {role: 'place_b'}]->(GP-AS-001)
(GS-GE-KS3-001)-[:PART_OF_CONTRAST]->(GC-KS3-001)
(GS-GE-KS3-002)-[:PART_OF_CONTRAST]->(GC-KS3-001)
(GS-GE-KS3-001)-[:DELIVERS_VIA {primary: true}]->(GE-KS3-C001)
(GS-GE-KS3-002)-[:DELIVERS_VIA {primary: true}]->(GE-KS3-C001)
```

### 6.4 KS3: "Africa Depth Study" Multi-Place Study

**GeoPlace nodes:** (illustrative subset)

```json
{"place_id": "GP-AF-CONTINENT", "name": "Africa", "place_type": "continent", "continent": "Africa", "scale": "continental", "is_adaptive": false}
{"place_id": "GP-AF-002", "name": "Kenya", "place_type": "country", "continent": "Africa", "country": "Kenya", "lat": -1.286, "lon": 36.817, "scale": "national", "climate_zone": "tropical", "development_classification": "LIC", "is_adaptive": false}
{"place_id": "GP-AF-003", "name": "Morocco", "place_type": "country", "continent": "Africa", "country": "Morocco", "lat": 33.972, "lon": -6.850, "scale": "national", "climate_zone": "arid", "development_classification": "LIC", "is_adaptive": false}
{"place_id": "GP-AF-004", "name": "South Africa", "place_type": "country", "continent": "Africa", "country": "South Africa", "lat": -33.925, "lon": 18.424, "scale": "national", "climate_zone": "temperate", "development_classification": "NEE", "is_adaptive": false}
```

**GeoStudy node:**

```json
{
  "study_id": "GS-GE-KS3-007",
  "name": "Africa: Place Depth Study",
  "study_type": "place_study",
  "key_stage": "KS3",
  "curriculum_status": "mandatory",
  "suggestion_type": "prescribed_topic",
  "theme_category": "integrated",
  "themes": ["diversity", "stereotypes", "development", "physical geography"],
  "scale": "continental",
  "map_types": ["choropleth", "climate_zones", "population_density", "thematic_map"],
  "data_sources": ["African Development Bank", "World Bank", "UN Population Division"],
  "definitions": ["stereotype", "diversity", "Sahel", "savanna", "Great Rift Valley", "desertification", "neo-colonialism"],
  "enquiry_question": "Is Africa really what the media says it is?",
  "sensitive_content_notes": ["Colonial legacy — discuss factually", "Avoid white saviour narratives", "Pupils of African heritage may have strong connections"]
}
```

**Relationships:**
```
(GS-GE-KS3-007)-[:STUDIES {role: 'primary'}]->(GP-AF-CONTINENT)
(GS-GE-KS3-007)-[:STUDIES {role: 'case_study'}]->(GP-AF-002)   // Kenya
(GS-GE-KS3-007)-[:STUDIES {role: 'case_study'}]->(GP-AF-003)   // Morocco
(GS-GE-KS3-007)-[:STUDIES {role: 'case_study'}]->(GP-AF-004)   // South Africa
(GP-AF-002)-[:IN_CONTINENT]->(GP-AF-CONTINENT)
(GP-AF-003)-[:IN_CONTINENT]->(GP-AF-CONTINENT)
(GP-AF-004)-[:IN_CONTINENT]->(GP-AF-CONTINENT)
```

This demonstrates a key advantage: a single `GeoStudy` can reference multiple `GeoPlace` nodes with different roles. The Africa depth study has Africa as its primary place, with Kenya, Morocco, and South Africa as case study sub-places. The old flat model crammed all of these into `locations: ["Africa", "Kenya", "Morocco", "South Africa", "Ethiopia"]` with no indication of which was primary and which were illustrative.

---

## 7. What This Enables That the Universal TopicSuggestion Could Not

### 7.1 Spatial queries across studies

```cypher
// "Show me all KS3 studies that use places in Africa"
MATCH (gs:GeoStudy)-[:STUDIES]->(gp:GeoPlace)-[:IN_CONTINENT]->(c:GeoPlace {name: 'Africa'})
WHERE gs.key_stage = 'KS3'
RETURN gs.name, collect(gp.name)
```

The old model could not do this because locations were strings, not nodes.

### 7.2 Contrast-aware lesson generation

```cypher
// "Give me the contrast framing for the Haiti-Japan unit"
MATCH (gc:GeoContrast)-[:CONTRASTS_STUDY]->(gs:GeoStudy)
WHERE gc.contrast_id = 'GC-KS3-001'
RETURN gc.dimensions, gc.stimulus_questions, collect(gs.name)
```

The old model stored `contrasting_with: "TS-GE-KS3-002"` as a string pointer with no dimensions or stimulus questions.

### 7.3 Place reuse across studies and key stages

```cypher
// "How is Kenya studied differently at KS1 vs KS3?"
MATCH (gs:GeoStudy)-[:STUDIES]->(gp:GeoPlace {country: 'Kenya'})
RETURN gs.key_stage, gs.study_type, gs.themes
```

The old model created duplicate location data on every TopicSuggestion that mentioned Kenya. Now Kenya is one node referenced by many studies.

### 7.4 Adaptive place resolution

```cypher
// "Which studies need the school to choose a place?"
MATCH (gs:GeoStudy)-[:STUDIES]->(gp:GeoPlace {is_adaptive: true})
RETURN gs.name, gp.exemplar_choices
```

This tells the AI tutor: "Before generating this lesson, you need to ask the user which specific place their school has chosen for this open slot."

### 7.5 Map-appropriate content generation

```cypher
// "What map types should the AI use for a KS1 place study?"
MATCH (gs:GeoStudy {key_stage: 'KS1', study_type: 'place_study'})
RETURN gs.name, gs.map_types
```

The controlled `map_types` vocabulary prevents the AI from generating a choropleth for Year 1 or a picture map for Year 9.

### 7.6 Cross-KS progression queries

```cypher
// "What does the pupil need to have studied before the KS2 rivers unit?"
MATCH (gs:GeoStudy {study_id: 'GS-GE-KS2-004'})-[:BUILDS_ON]->(prerequisite:GeoStudy)
RETURN prerequisite.name, prerequisite.key_stage
```

The old model had no `BUILDS_ON` between topic suggestions.

### 7.7 Fieldwork-ready study identification

```cypher
// "Which studies have fieldwork potential?"
MATCH (gs:GeoStudy)
WHERE gs.fieldwork_potential IS NOT NULL
RETURN gs.name, gs.key_stage, gs.fieldwork_potential
```

---

## 8. Relationship to Existing Graph Nodes

### 8.1 Replacing ContentVehicle for Geography

The existing `ContentVehicle` nodes for Geography (GE-KS3-CV001 through GE-KS3-CV010) are effectively prototype `GeoStudy` nodes. The migration path is:

- Each existing `ContentVehicle` becomes a `GeoStudy` node
- The `location` string property is replaced by `[:STUDIES]->(:GeoPlace)` relationships
- The `contrasting_with` string property is replaced by `[:PART_OF_CONTRAST]->(:GeoContrast)` relationships
- The `vehicle_type` property maps to `study_type` (most KS3 CVs are `case_study`)
- All other properties (`themes`, `map_types`, `data_sources`, `definitions`, `data_points`, `assessment_guidance`, `success_criteria`) transfer directly

### 8.2 Coexistence with VehicleTemplate

`GeoStudy` nodes still use `[:USES_TEMPLATE]->(:VehicleTemplate)` for the session structure scaffolding. The `study_type` determines which templates are valid:

| study_type | Valid VehicleTemplates |
|---|---|
| `place_study` | `VT-19` (place_study), `VT-14` (comparison_study) |
| `thematic_study` | `VT-01` (topic_study), `VT-05` (pattern_seeking), `VT-16` (modelling_enquiry) |
| `case_study` | `VT-02` (case_study), `VT-18` (secondary_data_analysis) |
| `fieldwork_investigation` | `VT-10` (fieldwork), `VT-09` (open_investigation) |
| `decision_making_exercise` | *Needs new VehicleTemplate* (see open questions) |

### 8.3 Relationship to Concept and Domain

The existing relationship pattern is preserved:
```
(:Domain)-[:HAS_STUDY]->(:GeoStudy)-[:DELIVERS_VIA {primary: bool}]->(:Concept)
```

This is identical to the current `HAS_SUGGESTION` / `DELIVERS_VIA` pattern but with a Geography-specific node label.

### 8.4 Relationship to ConceptCluster and ThinkingLens

```
(:ConceptCluster)-[:SUGGESTED_STUDY {rank: int}]->(:GeoStudy)
```

This replaces `SUGGESTED_TOPIC`. The rank indicates recommendation priority (1 = best fit, 2 = alternative).

The ThinkingLens relationship remains on ConceptCluster, not on GeoStudy. The lens frames *how to think about a cluster of concepts*; the study frames *what place and pedagogy to use to teach them*. These are complementary, not redundant.

---

## 9. Node Counts (Estimated)

| Label | Estimated count | Rationale |
|---|---|---|
| `:GeoPlace` | 40-60 | ~15 KS1 (UK countries, continents, exemplar localities), ~15 KS2 (rivers, regions, global features), ~25 KS3 (countries, cities, physical features) plus ~5 continent nodes. Many reused across key stages. |
| `:GeoStudy` | 30-40 | ~5 KS1, ~7 KS2, ~15-20 KS3 (matching current topic suggestion inventory) |
| `:GeoContrast` | 8-12 | ~2 KS1 (UK vs non-European), ~2 KS2 (UK vs Europe, UK vs Americas), ~5-8 KS3 (Haiti/Japan, Lagos/London, development contrasts, etc.) |

Total new nodes: **78-112** (comparable to the 33 current TopicSuggestion nodes plus the 10 ContentVehicle nodes, with the addition of ~40-60 reusable GeoPlace nodes).

---

## 10. Open Questions

### 10.1 Decision Making Exercise VehicleTemplate

My earlier review recommended a `decision_making_exercise` VehicleTemplate. This is not in the current 24-template list. If it is added, its session structure would be:

`context -> stakeholder_identification -> evidence_gathering -> perspective_analysis -> decision -> justification`

This is a genuinely distinctive Geography pedagogy (also used in Citizenship and GCSE Geography). Should it be added to the template list, or should `case_study` be stretched to cover it?

**My recommendation**: Add it. The session structure is fundamentally different from a case study. In a case study, the student analyses what happened. In a decision-making exercise, the student decides what SHOULD happen. The AI tutor needs different prompting for each.

### 10.2 GeoPlace granularity

How granular should GeoPlace nodes be? Options:
- **Country-level only** (simple, fewer nodes, but misses city-level case studies like Lagos)
- **Mixed: countries + cities + regions + physical features** (current proposal — richer, but more nodes)
- **Very granular: individual streets, school postcodes** (too much — the `is_adaptive` pattern handles this)

**My recommendation**: Mixed granularity as proposed. The AI needs to know that the Haiti study focuses on Port-au-Prince (a city), not rural Haiti. But we should not create GeoPlace nodes for every possible school locality — those are adaptive.

### 10.3 GeoPlace sharing across subjects

Nigeria appears in Geography KS3 (development study) AND in History KS3 (colonial Africa). Should `GeoPlace` be a cross-subject node, or should Geography and History each maintain their own place inventories?

**My recommendation**: Keep Geography-specific for now (`GP-` prefix). If a cross-subject Place layer is needed later, it can absorb GeoPlace nodes with a label migration. Premature cross-subject sharing creates coupling that is hard to undo. Geography's `GeoPlace` has Geography-specific properties (`climate_zone`, `development_classification`) that History does not need.

### 10.4 Relationship between GeoStudy and the existing TopicSuggestion data

The migrated data in `layers/topic-suggestions/data/topic_suggestions/geography_ks*.json` currently follows the `GeographyTopicSuggestion` flat schema. If this ontology is adopted, those files need restructuring into three separate files:
- `geo_places.json` (all GeoPlace nodes)
- `geo_studies_ks1.json`, `geo_studies_ks2.json`, `geo_studies_ks3.json` (GeoStudy nodes per KS)
- `geo_contrasts.json` (all GeoContrast nodes)

The import script would need a two-pass approach (similar to `import_curriculum.py`): create GeoPlace nodes first, then GeoStudy nodes with STUDIES relationships, then GeoContrast nodes with CONTRASTS relationships.

### 10.5 Should `data_points` be on GeoPlace or GeoStudy?

Currently proposed on GeoStudy (e.g. "Magnitude 7.0" is about the Haiti earthquake study, not about Port-au-Prince as a place). But some data is place-intrinsic (e.g. "Population 220 million" is about Nigeria regardless of which study uses it).

**My recommendation**: Keep on GeoStudy. The "population 220 million" statistic is only relevant because the development study uses it. A different study of Nigeria (e.g. Nollywood cultural study) would use different data points. Data points are study-contextual, not place-intrinsic. Place-intrinsic facts go in `key_physical_features` and `key_human_features`.

### 10.6 Mystery template

The "Thinking Through Geography" mystery activity is widely used in Geography departments. Should it be:
- A separate `study_type` value?
- A VehicleTemplate variant?
- An `enquiry_question` format convention?

**My recommendation**: VehicleTemplate variant. The mystery is a pedagogical *method*, not a fundamentally different type of geographical study. A mystery about Haiti is still a case study — it just uses a clue-sorting activity structure. The VehicleTemplate captures this without inflating the study_type enum.

---

## 11. Schema Summary

### Labels
| Label | Count | Purpose |
|---|---|---|
| `:GeoPlace` | 40-60 | Geographical locations: countries, cities, regions, physical features |
| `:GeoStudy` | 30-40 | Units of geographical study connecting places to curriculum |
| `:GeoContrast` | 8-12 | Curated place/study pairings for comparative geography |

### Relationships
| Relationship | From | To | Properties |
|---|---|---|---|
| `STUDIES` | GeoStudy | GeoPlace | `role`: primary, comparison, case_study |
| `DELIVERS_VIA` | GeoStudy | Concept | `primary`: bool |
| `USES_TEMPLATE` | GeoStudy | VehicleTemplate | |
| `HAS_STUDY` | Domain | GeoStudy | |
| `SUGGESTED_STUDY` | ConceptCluster | GeoStudy | `rank`: int |
| `PART_OF_CONTRAST` | GeoStudy | GeoContrast | |
| `CONTRASTS_PLACE` | GeoContrast | GeoPlace | `role`: place_a, place_b |
| `CONTRASTS_STUDY` | GeoContrast | GeoStudy | `role`: study_a, study_b |
| `IN_CONTINENT` | GeoPlace | GeoPlace | |
| `LOCATED_IN` | GeoPlace | GeoPlace | |
| `BUILDS_ON` | GeoStudy | GeoStudy | |
| `COMPLEMENTS` | GeoStudy | GeoStudy | |

### Key design decisions
1. **Places are nodes, not properties.** This enables reuse, spatial queries, and cross-KS progression.
2. **Contrasts are nodes, not string pointers.** This captures the richness of comparative geography.
3. **Study types determine pedagogy.** Five types, each with a distinct session structure.
4. **Adaptive places are flagged, not faked.** `is_adaptive: true` tells the AI to ask, not guess.
5. **Map types are controlled vocabulary.** Prevents age-inappropriate cartography in AI generation.
6. **Data sources are required at all key stages.** "Classroom globe" is a data source at KS1; "World Bank" is a data source at KS3.

---

*This ontology was designed from Geography's disciplinary needs, not from a universal template. It reflects how Geography is actually taught: through places, through comparison, through maps, and through fieldwork. The three-node model (Place, Study, Contrast) captures the subject's fundamental structure in a way that a single flat node with optional properties cannot.*
