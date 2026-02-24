# Geography Teacher Review: GeographyTopicSuggestion Schema

**Reviewer**: KS2 + KS3 Geography Specialist
**Date**: 2026-02-24
**Focus**: GeographyTopicSuggestion schema, VehicleTemplates, and topic inventory for KS1-KS3 Geography

---

## 1. Subject-Specific Property Review

### `location` (string, required) — MODIFY to `locations` (string[], required)

**Rationale**: A single string is fundamentally insufficient for Geography. The existing CV data already exposes this problem:

- GE-KS3-CV005 ("Urbanisation: Lagos and London") stores `"Lagos, Nigeria and London, UK"` as a single string — this is two distinct places being crammed into one field
- GE-KS3-CV007 ("Africa: Place Depth Study") stores `"Africa (multiple countries: Kenya, Morocco, South Africa, Ethiopia)"` — that's four countries in parenthetical notation
- GE-KS3-CV003 ("Climate Change") stores `"Global (with regional case studies: Arctic, Bangladesh, Sahel)"` — a global topic with three sub-locations

An AI tutor generating a lesson about Lagos vs London needs to know these are *two separate places*. A map generator needs individual locations to geocode. The current single-string approach forces the AI to parse natural language to extract locations, which is fragile and unnecessary.

**Proposed change**:
```json
"locations": ["Lagos, Nigeria", "London, UK"]
```

Each entry is a discrete, geocodable place name. For KS1 "Our Local Area", the array would contain `["School locality"]` (a single item). For KS2 Amazon Rainforest: `["Amazon Basin, Brazil"]`. For KS3 Haiti/Japan comparison: the *suggestion* for Haiti has `["Port-au-Prince, Haiti"]` and the Japan suggestion has `["Tohoku, Japan"]` — the *contrasting pair* is captured by the `CONTRASTS_WITH` relationship, not by stuffing two locations into one node.

### `themes` (string[], required) — MODIFY: use controlled vocabulary with extensibility

**Rationale**: Free-text themes create inconsistency. The existing CV data already shows drift:
- GE-KS3-CV001 uses `"vulnerability"`, `"governance"`
- GE-KS3-CV004 uses `"inequality"`, `"resource curse"`
- GE-KS3-CV005 uses `"push-pull factors"`, `"informal settlements"`

These are a mix of geographical concepts, processes, and specific topic vocabulary. An AI tutor needs to know whether a topic is primarily physical, human, or environmental to select the right framing — but it also needs the specific thematic vocabulary.

**Proposed change**: Split into two properties:

| Property | Type | Required | Description |
|---|---|---|---|
| `theme_category` | string | Yes | Controlled vocabulary: `physical`, `human`, `environmental`, `economic`, `social`, `political`, `integrated` |
| `themes` | string[] | Yes | Specific thematic concepts (free text, but curated per suggestion) |

This lets the AI quickly filter by geography strand while retaining granular topic vocabulary.

### `contrasting_with` (string, optional) — KEEP but clarify semantics

**Rationale**: This is correct for Geography where contrasting studies are statutory (KS1: UK vs non-European; KS2: UK vs European vs Americas). But the current CV data is inconsistent — some contrasts are explicit (Haiti↔Japan), some are implicit (Nigeria has `"with comparisons to UK"`), and some are null.

**Recommendation**: Keep the property *and* the `CONTRASTS_WITH` relationship (they serve different audiences — property for quick lookup, relationship for graph traversal). Clarify that `contrasting_with` stores the `suggestion_id` of the paired topic, not a free-text description. For open-slot contrasts where the teacher hasn't picked a specific pair, use `null`.

### `data_sources` (string[], optional) — MODIFY to required

**Rationale**: Data literacy is a statutory requirement at every key stage:
- KS1: "use simple fieldwork and observational skills"
- KS2: "use fieldwork to observe, measure, record and present... using a range of methods"
- KS3: "collect, analyse and draw conclusions from geographical data, using multiple sources of increasingly complex information"

Every Geography topic must engage with data of some kind. At KS1 this might be `["weather chart", "picture postcard comparison"]`. At KS3 it's `["USGS", "World Bank", "UN OCHA"]`. Making `data_sources` optional signals it's a nice-to-have, when in reality data engagement is non-negotiable.

**Proposed change**: Required, with age-appropriate expectations. KS1 data sources are observational/primary. KS2 introduces secondary data. KS3 requires named authoritative sources.

### ADD: `map_types` (string[], required)

**Rationale**: Maps are the *language* of Geography. The existing CV data already includes `map_types` on every single vehicle — this property was clearly needed. Geography without maps is like English without texts.

The AI tutor needs to know what kinds of maps to reference, generate, or link to. A Year 2 "Our Locality" lesson needs a simple sketch map or aerial photo. A Year 9 Nigeria development lesson needs a choropleth HDI map.

**Proposed controlled vocabulary** (extensible):
- KS1: `sketch_map`, `aerial_photo`, `globe`, `simple_plan`, `picture_map`
- KS2: `OS_map`, `atlas_map`, `sketch_map`, `satellite_image`, `thematic_map`, `weather_map`
- KS3: `OS_map`, `GIS`, `satellite_image`, `choropleth`, `isoline`, `flow_map`, `dot_map`, `proportional_symbol`, `topographic`

### ADD: `scale` (string, required)

**Rationale**: Geographical scale is a core disciplinary concept. The NC explicitly progresses from local → regional → national → continental → global across key stages. An AI tutor generating a lesson needs to know the spatial scale to calibrate language, examples, and map zoom level.

| Value | Description | Typical KS |
|---|---|---|
| `local` | School grounds, village, neighbourhood | KS1, KS2 |
| `regional` | County, river catchment, climate zone | KS2, KS3 |
| `national` | UK-wide patterns, country study | KS2, KS3 |
| `continental` | Europe, Africa, Asia, Americas | KS2, KS3 |
| `global` | Worldwide patterns and processes | KS2 (intro), KS3 |

A topic can operate at multiple scales (e.g. climate change is global but studied through regional case studies), so this could be `string[]` — but a primary scale is most useful. Use `string` for the dominant scale, and let `themes` capture the multi-scale nature.

### ADD: `fieldwork_potential` (string | null, optional)

**Rationale**: Fieldwork is statutory at all key stages. Some topics are inherently fieldwork-rich (rivers, local area, microclimate investigation) while others are primarily desk-based (plate tectonics, distant place studies). An AI tutor or teacher planning tool needs to flag fieldwork-suitable topics and suggest what data collection is possible.

This should be a **descriptive string** (not boolean), because the value is in explaining *what kind* of fieldwork is possible:
- `"River study: measure width, depth, velocity, bedload at multiple points along river course"` (KS2 rivers)
- `"Local area survey: land use mapping, environmental quality assessment, pedestrian counts"` (KS1/KS2 local)
- `"Weather data collection: daily temperature, rainfall, wind direction over 2 weeks"` (KS1 weather)
- `null` for topics where fieldwork is not directly applicable (e.g. plate tectonics — though you *could* study volcanic rocks locally)

### REMOVE: No properties need removing

The proposed schema is lean. All four proposed properties are relevant; they just need the modifications above.

---

## 2. Universal Property Review

### `suggestion_type` — ADD `place_study` value

The current values (`prescribed_topic`, `exemplar_topic`, `open_slot`, `exemplar_figure`, `exemplar_event`, `exemplar_text`, `teacher_convention`) are History/English-biased. Geography's primary unit of study is the **place**, not the event or figure.

Add `place_study` to the controlled vocabulary. This is the dominant Geography pattern — "Study a region of Europe", "Study a contrasting non-European country", "In-depth study of Africa".

### `definitions` (string[], required) — KEEP, but add Geography-specific note

Definitions are essential. Geography has heavy specialist vocabulary (choropleth, isoline, epicentre, megacity, HDI, GNI). The existing CV data shows excellent definition lists. Keep as required.

**Note**: Geography definitions often need to be visualised (you can't define "choropleth map" without showing one). The AI tutor should be prompted to generate visual examples alongside text definitions. This is a generation prompt concern, not a schema concern.

### `common_pitfalls` — Geography-specific examples needed

Common Geography pitfalls include:
- Treating countries as homogeneous ("Africa is poor") rather than exploring internal diversity
- Confusing weather and climate
- Teaching place knowledge as facts-to-memorise rather than as evidence for geographical processes
- Neglecting the "so what?" — describing without explaining or evaluating
- Using outdated data (population figures, GDP) — Geography data ages faster than History data

These should be curated for each topic suggestion, not generic.

### `cross_curricular_hooks` — Geography has strong cross-curricular links

Geography naturally connects to:
- **Science**: weather/climate, water cycle, rocks/soil, ecosystems, habitats
- **Maths**: data handling, coordinates, scale, ratio (map scales), graph interpretation
- **History**: changing landscapes, migration, trade routes, empire (shared content in many schools)
- **English**: travel writing, persuasive writing (environmental arguments), report writing
- **Computing**: GIS, data visualisation, satellite imagery analysis
- **Art**: landscape art, aerial photography, observational drawing in fieldwork
- **PSHE/Citizenship**: sustainability, global citizenship, inequality

This property is well-suited to Geography. Keep as optional but encourage population for every topic.

---

## 3. VehicleTemplate Critique

### Templates that work well for Geography

| # | Template | Geography fit | Notes |
|---|---|---|---|
| 1 | `topic_study` | Good | Works for KS1 place studies, KS2 regional studies |
| 2 | `case_study` | Excellent | The dominant KS3 Geography pattern. All existing CVs use this |
| 5 | `pattern_seeking` | Good | Weather patterns, population distribution, economic patterns |
| 9 | `investigation_design` | Good | Geographical enquiry |
| 10 | `fieldwork` | Excellent | Statutory Geography requirement — glad to see it here |
| 14 | `comparison_study` | Excellent | Contrasting localities (KS1), contrasting regions (KS2/3) |

### Missing templates for Geography

#### `place_study` — MUST ADD

This is the most fundamental Geography template and it's absent. A place study is NOT the same as a `topic_study` or `case_study`:
- A **topic study** is structured around a theme (e.g. "Trade and Fairtrade")
- A **case study** is structured around evidence and analysis of a specific situation (e.g. "Haiti earthquake")
- A **place study** is structured around building a rich, layered understanding of a specific place through multiple lenses (physical, human, economic, cultural)

**Proposed session structure**: `locate -> describe_physical -> describe_human -> explain_interactions -> compare -> evaluate_change`

This is the pedagogical backbone of Geography at every key stage:
- KS1: "Our school and its grounds" → "Our local area" → "Kenya"
- KS2: "A region of the UK" → "A region of Europe" → "A region of the Americas"
- KS3: "Africa depth study" → "Asia depth study" → "Middle East depth study"

#### `decision_making_exercise` — STRONGLY RECOMMEND

Decision-making exercises are a distinctively geographical pedagogy. Students are given a real-world geographical decision and must weigh evidence from multiple perspectives:
- "Should the new bypass go through the green belt or the town centre?"
- "Should the UK build more reservoirs or reduce demand?"
- "Should Lagos invest in public transport or housing?"

**Proposed session structure**: `context -> stakeholder_identification -> evidence_gathering -> perspective_analysis -> decision -> justification`

This is widely used in KS3 and is the basis of GCSE geography "decision making" exam questions (both AQA and Edexcel).

#### `mystery` — RECOMMEND

The Thinking Through Geography "mystery" activity is a distinctive Geography teaching strategy. Students receive a set of clue cards and must construct an explanation for a geographical puzzle:
- "Why did so many people die in the Haiti earthquake?"
- "Why is the Sahel getting drier?"

**Proposed session structure**: `stimulus_question -> clue_distribution -> sorting_and_grouping -> hypothesis_building -> explanation -> reflection`

This could be a variant of `investigation_design` rather than a standalone template, but it's so widely used in Geography departments that it deserves its own template.

### Template modifications

**`case_study` session structure**: The proposed structure (`introduction -> data_collection -> analysis -> comparison -> evaluation`) is good but Geography case studies specifically need an explicit **location** phase. Proposed modification:

`introduction -> locate_and_describe -> data_collection -> analysis -> comparison -> evaluation`

The "locate and describe" phase is where students establish *where* they're studying and *what* the physical/human characteristics are — this is Geography's distinctive contribution compared to a generic case study.

### Summary of template recommendations

| Action | Template | Rationale |
|---|---|---|
| ADD | `place_study` | Core Geography pedagogy missing from the list |
| ADD | `decision_making_exercise` | Distinctively geographical; used in GCSE assessment |
| ADD | `mystery` | Widely used Geography teaching strategy |
| MODIFY | `case_study` | Add "locate and describe" as explicit phase |

---

## 4. TopicSuggestion Inventory

### KS1 Geography Topics

| suggestion_id | Name | Type | Curriculum status | Notes |
|---|---|---|---|---|
| TS-GE-KS1-001 | Our School and Grounds | `prescribed_topic` | `mandatory` | Statutory: local area study |
| TS-GE-KS1-002 | Our Local Area | `prescribed_topic` | `mandatory` | Statutory: UK small area |
| TS-GE-KS1-003 | UK Countries, Capitals and Seas | `prescribed_topic` | `mandatory` | Statutory locational knowledge |
| TS-GE-KS1-004 | Seven Continents and Five Oceans | `prescribed_topic` | `mandatory` | Statutory locational knowledge |
| TS-GE-KS1-005 | Hot and Cold Places | `prescribed_topic` | `mandatory` | Statutory: weather, Equator, Poles |
| TS-GE-KS1-006 | A Village in Kenya | `teacher_convention` | `convention` | ~60-70% of schools use Kenya for contrasting non-European locality |
| TS-GE-KS1-007 | A City in India | `exemplar_topic` | `exemplar` | NC non-statutory guidance mentions India |
| TS-GE-KS1-008 | Contrasting Non-European Locality | `open_slot` | `mandatory` | School picks: Kenya, India, China, Brazil, etc. |
| TS-GE-KS1-009 | Seasonal Weather Patterns | `prescribed_topic` | `mandatory` | Statutory: daily/seasonal weather in UK |

### KS2 Geography Topics

| suggestion_id | Name | Type | Curriculum status | Notes |
|---|---|---|---|---|
| TS-GE-KS2-001 | UK Regional Study | `open_slot` | `mandatory` | School picks: Lake District, Yorkshire, Scottish Highlands, etc. |
| TS-GE-KS2-002 | European Regional Study | `open_slot` | `mandatory` | School picks: Alps, Italy, Rhine Valley, Catalonia, etc. |
| TS-GE-KS2-003 | Americas Regional Study | `open_slot` | `mandatory` | School picks region in N or S America |
| TS-GE-KS2-004 | Amazon Rainforest | `teacher_convention` | `convention` | Most common Americas choice (~50%+ of schools) |
| TS-GE-KS2-005 | The Alps | `teacher_convention` | `convention` | Very common European choice |
| TS-GE-KS2-006 | Rivers and the Water Cycle | `prescribed_topic` | `mandatory` | Statutory physical geography |
| TS-GE-KS2-007 | Mountains, Volcanoes and Earthquakes | `prescribed_topic` | `mandatory` | Statutory physical geography |
| TS-GE-KS2-008 | Climate Zones, Biomes and Vegetation | `prescribed_topic` | `mandatory` | Statutory physical geography |
| TS-GE-KS2-009 | Trade and Economic Activity | `prescribed_topic` | `mandatory` | Statutory human geography |
| TS-GE-KS2-010 | Settlements and Land Use | `prescribed_topic` | `mandatory` | Statutory human geography |
| TS-GE-KS2-011 | Fairtrade | `teacher_convention` | `convention` | Extremely common vehicle for trade/economics |
| TS-GE-KS2-012 | Distribution of Natural Resources | `prescribed_topic` | `mandatory` | Energy, food, minerals, water |
| TS-GE-KS2-013 | Latitude, Longitude and Time Zones | `prescribed_topic` | `mandatory` | Statutory locational knowledge |
| TS-GE-KS2-014 | Map Skills and Fieldwork | `prescribed_topic` | `mandatory` | Statutory skills requirement |
| TS-GE-KS2-015 | The River Thames | `teacher_convention` | `convention` | Common river case study choice |

### KS3 Geography Topics

| suggestion_id | Name | Type | Curriculum status | Notes |
|---|---|---|---|---|
| TS-GE-KS3-001 | Tectonic Hazards | `prescribed_topic` | `mandatory` | Statutory: plate tectonics |
| TS-GE-KS3-002 | Haiti 2010 Earthquake | `teacher_convention` | `convention` | Near-universal LIC earthquake case study |
| TS-GE-KS3-003 | Japan 2011 Earthquake/Tsunami | `teacher_convention` | `convention` | Near-universal HIC earthquake case study |
| TS-GE-KS3-004 | Climate Change | `prescribed_topic` | `mandatory` | Statutory: weather and climate |
| TS-GE-KS3-005 | Development and Global Inequality | `prescribed_topic` | `mandatory` | Statutory: human geography |
| TS-GE-KS3-006 | Nigeria Development Study | `teacher_convention` | `convention` | Dominant development case study (AQA GCSE influence) |
| TS-GE-KS3-007 | Urbanisation: Lagos | `teacher_convention` | `convention` | Dominant urbanisation LIC case study |
| TS-GE-KS3-008 | Urbanisation: London | `teacher_convention` | `convention` | Dominant urbanisation HIC case study |
| TS-GE-KS3-009 | Resource Management: UK Water | `teacher_convention` | `convention` | Very common resource management choice |
| TS-GE-KS3-010 | Africa Depth Study | `prescribed_topic` | `mandatory` | Statutory place knowledge (Africa, Asia, M. East) |
| TS-GE-KS3-011 | Asia Depth Study | `prescribed_topic` | `mandatory` | Statutory place knowledge |
| TS-GE-KS3-012 | Middle East Depth Study | `teacher_convention` | `convention` | Common but not all schools cover Middle East separately |
| TS-GE-KS3-013 | Population and Migration | `prescribed_topic` | `mandatory` | Statutory: human geography |
| TS-GE-KS3-014 | Geographical Fieldwork Investigation | `prescribed_topic` | `mandatory` | Statutory skills requirement |
| TS-GE-KS3-015 | Weather and Climate Systems | `prescribed_topic` | `mandatory` | Statutory physical geography |
| TS-GE-KS3-016 | Coasts | `teacher_convention` | `convention` | Very commonly taught physical topic (GCSE prep) |
| TS-GE-KS3-017 | Ecosystems and Tropical Rainforests | `teacher_convention` | `convention` | Common biome case study |
| TS-GE-KS3-018 | UK Physical Landscapes | `prescribed_topic` | `mandatory` | Statutory locational knowledge |
| TS-GE-KS3-019 | Flooding: Bangladesh or Somerset | `teacher_convention` | `convention` | Common weather hazard case study |

---

## 5. Content Generation Requirements

### What an AI tutor needs to generate a good Geography lesson

**Scenario 1: Year 2 "Our Locality" lesson**

The AI needs:
- `locations`: `["School locality"]` — but crucially needs to know this is *adaptable* to the child's actual school location
- `scale`: `local`
- `map_types`: `["aerial_photo", "simple_plan", "picture_map"]` — the AI must generate/reference age-appropriate map types, not OS maps
- `themes`: `["our school", "local features", "human and physical"]`
- `fieldwork_potential`: `"Walk around school grounds: identify human features (playground, car park, shops) and physical features (trees, hills, river). Create a simple sketch map."`
- `definitions`: `["human feature", "physical feature", "map", "aerial photograph"]`
- `pedagogical_rationale`: Why locality matters — children learn geography from the known to the unknown, from concrete to abstract

The AI does NOT need GIS, data_sources like "World Bank", or choropleth maps. The schema must work at this very simple level.

**Scenario 2: Year 9 "Nigeria Development" assessment task**

The AI needs:
- `locations`: `["Nigeria"]` with comparisons to UK, other African nations
- `scale`: `national` (with `continental` context)
- `map_types`: `["choropleth", "proportional_symbol", "dot_map", "flow_map"]`
- `data_sources`: `["World Bank", "UNDP", "Nigerian National Bureau of Statistics"]` — required for data response questions
- `themes`: `["development indicators", "inequality", "resource curse", "urbanisation"]`
- `theme_category`: `economic`
- `definitions`: `["GDP", "GNI", "HDI", "resource curse", "informal economy"]`
- DifficultyLevel data to calibrate the assessment (emerging → mastery)
- `common_pitfalls`: `["Treating Nigeria as uniformly poor — Lagos vs rural north", "Using only GDP as a development measure", "Ignoring positive development trends"]`

**Scenario 3: Video script for "Rivers and the Water Cycle" (Year 5)**

The AI needs:
- `locations`: `["River Thames, UK"]` or whatever exemplar river is chosen
- `map_types`: `["OS_map", "satellite_image"]` — to generate map-based visual sequences
- `definitions`: clear, ordered vocabulary (`source`, `tributary`, `meander`, `floodplain`, `estuary`, `mouth`)
- `fieldwork_potential`: to suggest "you could investigate this at your local river" segments
- `cross_curricular_hooks`: `["Science: water cycle and states of matter"]` — for connecting to the child's other learning

### Key insight: the schema must support KS1 simplicity AND KS3 complexity

The biggest risk is designing for KS3 and leaving KS1 behind. A Year 1 "Hot and Cold Places" topic has:
- `locations`: `["North Pole", "South Pole", "Equator"]`
- `scale`: `global`
- `map_types`: `["globe", "simple_plan"]`
- `data_sources`: `["classroom globe", "simple temperature comparison"]`
- `fieldwork_potential`: `"Measure temperature in sun vs shade in school grounds"`
- No complex vocabulary, no data manipulation, no GIS

If `data_sources` is required (as I recommend), it needs to accept simple observational sources at KS1, not just formal institutions.

---

## 6. Cross-Curricular Hooks

### Geography's natural cross-curricular connections

| Geography topic | Connected subject | Specific hook |
|---|---|---|
| Weather and climate | Science KS1-2 | Seasonal changes, states of matter (water cycle) |
| Rivers and water cycle | Science KS2 | States of matter, evaporation, condensation |
| Volcanoes and earthquakes | Science KS2-3 | Rocks, earth structure, forces |
| Rainforest/biomes | Science KS2-3 | Habitats, adaptation, food chains, ecosystems |
| Trade and Fairtrade | Maths KS2 | Data handling, percentages, graph interpretation |
| Map skills | Maths KS1-3 | Coordinates, scale, ratio, compass directions (angles) |
| Population data | Maths KS3 | Statistical analysis, percentage change, graph types |
| Local area study | English KS1-2 | Descriptive writing, report writing, directions |
| Climate change | English KS3 | Persuasive writing, balanced argument |
| Development and inequality | PSHE/Citizenship | Global citizenship, fairness, sustainability |
| GIS and data visualisation | Computing KS2-3 | Data handling, digital literacy, spatial analysis |
| Place depth studies | History | Colonial legacies, migration, empire, trade routes |
| Landscapes | Art KS1-3 | Landscape painting, observational drawing, photography |

### Most important hooks to capture

For an AI tutor, the most valuable cross-curricular hooks are:
1. **Geography ↔ Science** (physical processes overlap heavily)
2. **Geography ↔ Maths** (data literacy, coordinates, graph skills)
3. **Geography ↔ History** (many KS3 topics share context: Nigeria → colonial history, urbanisation → industrial revolution)

---

## 7. Stress Test Scenarios

### Scenario 1: Year 1 — "Kenya vs Our Village" contrasting locality study

**What the teacher does**: Children compare their school/village with a Kenyan village. They look at houses, weather, food, animals, clothing. They use picture maps and aerial photos. They do a "walk around school" to map features.

**What the schema needs to capture**:
- Two locations: the child's locality (adaptable) and Kenya — `locations: ["School locality", "Kenyan village"]` works
- Very simple map types: `["picture_map", "aerial_photo", "globe"]` — no OS maps, no GIS
- Simple data sources: `["photographs", "video clips", "classroom globe"]`
- Fieldwork: `"Walk around school: identify and photograph human and physical features"`
- Scale: `local` (both localities are studied at local scale, even though Kenya is far away)

**Schema verdict**: Works if `locations` is an array, `map_types` is included, and `data_sources` accepts simple observational sources. Currently fails because `location` is singular and `data_sources` is optional.

### Scenario 2: Year 5 — "The Amazon Rainforest" Americas regional study

**What the teacher does**: Children locate the Amazon on a world map and South American map. They study physical geography (climate, vegetation layers, animals), human geography (indigenous peoples, deforestation, rubber tappers), and make links to climate change and trade. They handle climate graphs, population data, and satellite deforestation images.

**What the schema needs to capture**:
- Location: `["Amazon Basin, Brazil"]` (may reference Manaus specifically)
- Scale: `regional` (within continental context)
- Map types: `["atlas_map", "satellite_image", "thematic_map"]` — crucial for deforestation time-series
- Data sources: `["WWF", "Brazilian Space Agency (INPE)", "climate data"]`
- Themes: `["deforestation", "biodiversity", "indigenous peoples", "climate"]`
- Theme category: `environmental`
- Cross-curricular: Science (habitats, food chains, adaptation), English (persuasive writing about deforestation)
- Fieldwork: `null` (distant place study — fieldwork not directly applicable)

**Schema verdict**: Works well. The `theme_category` addition helps the AI understand this is primarily an environmental topic with human geography dimensions.

### Scenario 3: Year 8 — "Should the UK build a new reservoir in the Severn Valley?"  Decision-making exercise

**What the teacher does**: Students receive a resource booklet with OS maps, rainfall data, population projections, stakeholder viewpoints (farmer, wildlife trust, water company, local residents, Environment Agency). They must weigh evidence, consider different perspectives, and justify a decision.

**What the schema needs to capture**:
- Location: `["Severn Valley, UK"]`
- Scale: `regional`
- Map types: `["OS_map", "GIS", "choropleth"]` — OS map essential for the site analysis
- Data sources: `["Environment Agency", "Met Office", "Ofwat", "ONS population projections"]`
- Themes: `["water supply", "sustainability", "stakeholder conflict", "environmental impact"]`
- VehicleTemplate: `decision_making_exercise` — this is NOT a case study. The pedagogical structure is fundamentally different (stakeholder analysis, evidence weighing, justified decision)
- Fieldwork potential: `"River flow measurement, water quality testing, land use survey of proposed site"`

**Schema verdict**: Fails without `decision_making_exercise` template. The `case_study` template doesn't capture the stakeholder-perspective-decision structure. Also needs `map_types` to specify OS maps are required.

### Scenario 4: Year 3 — "What is it like in the Lake District?" UK regional study

**What the teacher does**: Children use maps, photos, and videos to explore the Lake District. They identify physical features (mountains, lakes, rivers), human features (farming, tourism, Windermere), compare with their local area, and begin using simple OS map symbols and grid references.

**What the schema needs to capture**:
- Location: `["Lake District, UK"]`
- Scale: `regional`
- Map types: `["OS_map", "aerial_photo", "simple_plan"]` — first introduction to OS maps
- Data sources: `["Visit Cumbria tourism data", "OS maps", "Met Office rainfall data"]`
- Theme category: `integrated` (both physical and human — tourism links them)
- Fieldwork potential: `null` for distant study, but could be `"If local: fell walking, river study, tourism survey"` if school is near
- Definitions: `["mountain", "lake", "valley", "tourism", "national park", "grid reference", "symbol"]`

**Schema verdict**: Works well if `map_types` is present. The progression from picture maps (KS1) to OS maps (KS2) is critical and only capturable if the schema includes map type data.

---

## 8. Summary: Top 3 Recommendations

### 1. Change `location` to `locations` (string[], required) — CRITICAL

**Impact**: Fixes data modelling for 40%+ of Geography topics that inherently involve multiple places (contrasting studies, depth studies, comparison studies). Without this, the AI tutor must parse natural language to extract locations — fragile, lossy, and unnecessary.

**Effort**: Low — property rename and type change.

### 2. Add `map_types` (string[], required) and `scale` (string, required) — CRITICAL

**Impact**: Maps and scale are the two most distinctively geographical concepts. Without `map_types`, the AI tutor has no guidance on what visual/cartographic resources to reference or generate. Without `scale`, it can't calibrate the spatial scope of the lesson. The existing CV data already includes `map_types` on every vehicle — this was clearly needed and should be promoted to the formal schema.

**Effort**: Low — two new required properties with controlled vocabularies.

### 3. Add `place_study` and `decision_making_exercise` VehicleTemplates — HIGH IMPACT

**Impact**: The current template list has a Geography-shaped hole. `case_study` is the right pattern for hazard events (earthquakes, floods), but Geography's two other dominant pedagogies — building layered place knowledge (`place_study`) and evaluating evidence to make geographical decisions (`decision_making_exercise`) — are absent. Without `place_study`, the AI has no template for the most common Geography lesson type at KS1-KS2 (locality studies, regional studies). Without `decision_making_exercise`, it can't generate the stakeholder-analysis-and-justify-your-decision tasks that are central to KS3 Geography and GCSE preparation.

**Effort**: Medium — two new templates with session structures, agent prompts, and age-banded guidance.

### Bonus: Make `data_sources` required

**Impact**: Data literacy is statutory at all key stages. Making this required forces every topic suggestion to specify what data the AI should use or prompt the student to engage with — even if at KS1 that's just "photographs and a classroom globe". This prevents the AI from generating data-free Geography lessons, which would be pedagogically unsound.

---

## Appendix: Revised GeographyTopicSuggestion Property Summary

| Property | Type | Required | Status | Notes |
|---|---|---|---|---|
| `locations` | string[] | Yes | MODIFIED (was `location`: string) | Array of geocodable place names |
| `theme_category` | string | Yes | NEW | Controlled: physical, human, environmental, economic, social, political, integrated |
| `themes` | string[] | Yes | KEEP | Specific thematic concepts per topic |
| `scale` | string | Yes | NEW | Controlled: local, regional, national, continental, global |
| `map_types` | string[] | Yes | NEW | Age-appropriate map/visual types |
| `data_sources` | string[] | Yes | MODIFIED (was optional) | Observational at KS1, institutional at KS3 |
| `contrasting_with` | string | No | KEEP | suggestion_id of contrasting topic |
| `fieldwork_potential` | string | No | NEW | Description of possible fieldwork activities |
| *Plus all universal properties* | | | | |

---

*Review complete. The schema has a solid foundation but needs Geography's three distinctive disciplinary pillars — place, map, and scale — to be first-class properties rather than afterthoughts. The VehicleTemplate inventory needs place_study and decision_making_exercise to cover Geography's most common and most distinctive teaching patterns.*
