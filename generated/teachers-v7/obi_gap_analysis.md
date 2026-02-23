# Gap Analysis: KS2 Geography (Y4) — Mr. Obi

**Cluster reviewed:** `GE-KS2-D003-CL001` — Understand climate zones, biomes and the water cycle
**All 5 KS2 Geography clusters queried** for context
**Date:** February 2026

---

## Overall Readiness Score: 4/10

Geography is the least well-served subject I reviewed in the graph. The curriculum skeleton is sound — the concepts, domains, prerequisites, thinking lenses and geographical skills links give me a solid *what to teach* framework. But Geography is a resource-intensive, data-driven, visually dependent subject, and the graph provides almost none of the *with what* that makes a Geography lesson teachable.

For comparison: the V5 teacher review scored the graph at 6.6/10 average after ContentVehicles and ThinkingLenses were added. But KS2 Geography received **zero ContentVehicles**. It has no case studies, no investigations, no data packs, no fieldwork plans. The thinking lenses help with cognitive framing, but they cannot compensate for the absence of geographical resources.

---

## Section-by-Section Assessment

| Section | Rating | Notes |
|---|---|---|
| Learning objectives | ✅ | Concept descriptions + geographical skills links = strong objectives |
| Success criteria | ⚠️ | No DifficultyLevel nodes; I built tiers from professional judgement |
| Prior knowledge | ✅ | Prerequisite chains explicit and useful |
| Lesson structure | ⚠️ | Pedagogy profile + interaction types helpful; no estimated teaching time |
| Key vocabulary | ✅ | Comprehensive word lists from concepts; no child-friendly definitions |
| Resources and materials | ❌ | Zero resource specifications; Geography is resource-dependent |
| Differentiation | ⚠️ | Learner profile parameters useful; no DifficultyLevel tiers |
| Assessment | ⚠️ | Interaction types suggest formats; no criteria or exemplars |
| Misconceptions | ✅ | Specific, accurate, directly teachable |
| Worked examples | ❌ | No model geographical analysis or exemplar responses |
| Practice activities | ⚠️ | Interaction types give format; no specific data/maps/resources |
| Cross-curricular links | ⚠️ | Some CO_TEACHES; critical Science↔Geography link missing |

**Strong sections (4/12):** Learning objectives, prior knowledge, vocabulary, misconceptions
**Partial sections (6/12):** Success criteria, lesson structure, differentiation, assessment, practice activities, cross-curricular links
**Missing sections (2/12):** Resources and materials, worked examples

---

## Geography-Specific Gaps

### 1. Zero ContentVehicles for KS2 Geography

This is the single most impactful gap. History has case studies, Science has investigations, English has text studies, Maths has worked example sets. Geography has nothing.

**What Geography vehicles should look like:**

| Vehicle type | Example | Delivers |
|---|---|---|
| `case_study` | "The Amazon Rainforest: A Tropical Biome Under Pressure" | GE-KS2-C002 (Climate Zones and Biomes) |
| `case_study` | "Nottingham and the River Trent: A Local River Study" | GE-KS2-C003 (River Systems and Water Cycle) |
| `case_study` | "Comparing Nottingham with Toulouse: A UK-European Region Study" | GE-KS2-C006 (Regional Place Study) |
| `investigation` | "Where Does Nottingham's Food Come From? A Trade Investigation" | GE-KS2-C004 (Settlement and Economic Geography) |
| `data_pack` | "Climate Data for Six World Locations" | GE-KS2-C002, GE-KS2-C001 |
| `fieldwork_plan` | "Mapping Our School Grounds: An OS Map Skills Fieldwork" | GE-KS2-C005 (OS Maps and Grid References) |

Geography-specific vehicle properties should include:
- `map_resources`: list of required map types (world outline, OS extract, atlas pages)
- `data_sources`: specific datasets with values (temperature, rainfall, population)
- `photograph_set`: list of required photographs with descriptions
- `fieldwork_requirements`: equipment, risk assessment, data collection method
- `contrasting_localities`: the specific places being compared
- `perspectives`: list of viewpoints for enquiry (borrowed from History vehicles — see below)

**Learning from History's ContentVehicles (via Ms. Farah, Y4 History):** History vehicles include a `perspectives` property — e.g., Roman Britain has [Roman coloniser, Briton, Roman soldier, enslaved person]. Geography should adopt this. A climate zones case study could have: [climate scientist, local farmer in the Amazon, Inuit community member, conservation worker]. A settlement vehicle: [medieval merchant, river fisherman, modern town planner, commuter]. Perspectives are what move Geography from "learn facts about a place" to genuine geographical enquiry with multiple viewpoints — which is what the National Curriculum actually requires.

### 2. No Map Resources

Geography without maps is not geography. The teaching guidance mentions "Use world climate and biome maps," "Use a globe," "Use OS maps" — but the graph cannot provide, reference, or link to any of these.

**What is needed:**
- `MapResource` nodes or properties on ContentVehicles specifying: map type (world political, world physical, OS 1:50000, OS 1:25000, thematic), coverage area, key features visible, recommended atlas pages
- Links between Concepts and the specific map types needed to teach them
- For the platform: an embeddable map viewer (even a static image pipeline) that can display the right map at the right moment

### 3. No Real-World Data

Geography is a data-literate subject. KS2 pupils should be interpreting climate data, population statistics, trade figures, and land use data. The graph holds none of this.

**What is needed:**
- `DataSet` nodes or properties on ContentVehicles with: actual data values (not just descriptions), source attribution, year of data, units
- For climate: monthly temperature and rainfall for at least 6 contrasting locations
- For population: settlement size data for local area and contrasting localities
- For trade: import/export data for a familiar product (e.g., bananas, chocolate)

### 4. No Fieldwork Scaffolds

The DEVELOPS_SKILL links from `GE-KS2-C002` to "Fieldwork: data collection and presentation" are a start, but they lead nowhere practical.

**What is needed:**
- `FieldworkPlan` nodes or properties on ContentVehicles with: learning objectives, equipment list, risk assessment template, data collection sheet, location guidance (school grounds / local area / urban / rural)
- Links from Concepts to the fieldwork activities that develop them
- For the platform: safety and safeguarding notes for out-of-classroom learning

### 5. No Place-Specific Knowledge

The concept `GE-KS2-C006` (Regional Place Study) says "study three contrasting regions" but does not name them, provide case study material, or link to any place-specific content. This is the most characteristic gap for Geography — the subject requires deep knowledge of specific places, not just conceptual frameworks.

**What is needed:**
- Place-specific ContentVehicles for at least: one UK region, one European region, one Americas region
- Each vehicle should include: location data (coordinates, continent, country), physical geography summary, human geography summary, photographs, statistical data, and comparison framework
- The Geographical Association's "Geography Champion" model could inform the structure

---

## Top 5 Data Additions (Priority Order)

### 1. ContentVehicle nodes for KS2 Geography (CRITICAL)
- 8-10 case studies covering all 4 domains (locational knowledge, place knowledge, human/physical geography, skills/fieldwork)
- Geography-specific properties: `map_resources`, `data_sources`, `photograph_set`, `fieldwork_requirements`, `contrasting_localities`
- DELIVERS relationships to concepts; IMPLEMENTS to Topics
- **Impact:** Would transform readiness from 4/10 to ~7/10

### 2. DifficultyLevel nodes for Geography concepts
- Entry / developing / expected / greater_depth tiers for each KS2 Geography concept
- With `example_task`, `example_response`, `common_errors` (as per Y3 Maths pilot)
- **Impact:** Would enable generated success criteria, differentiation, and assessment criteria
- Estimated: ~30 concepts x 3-4 levels = ~100-120 DifficultyLevel nodes

### 3. Cross-subject CO_TEACHES / PREREQUISITE_OF links
- Geography water cycle ↔ Science states of matter (Y4)
- Geography data handling ↔ Maths statistics (Y4)
- Geography settlement ↔ History local history (Y3/Y4)
- Geography map scale ↔ Maths measurement and scale (Y4)
- **Impact:** Would enable genuine cross-curricular planning from the graph

### 4. Estimated teaching time on ConceptCluster nodes
- Currently all KS2 Geography clusters show "None lessons (~None weeks)"
- Need: `estimated_lessons` and `estimated_weeks` properties
- Geography concepts vary hugely: OS map skills might be 2 lessons; a regional place study could be 6-8
- **Impact:** Would enable medium-term planning and curriculum coverage checks

### 5. Child-friendly vocabulary definitions
- Current `key_vocabulary` lists provide terms but not definitions
- Need: `vocabulary_definitions` property (or linked VocabularyTerm nodes) with age-appropriate definitions matching the content guidelines (Lexile 300-500L, max 18 words)
- **Impact:** Would enable automated vocabulary support and glossary generation

---

## Specific New Entities/Properties Requested

### New node type: `MapResource`
```
(:MapResource {
  map_id: 'MAP-WORLD-CLIMATE-001',
  name: 'World Climate Zones Map',
  map_type: 'thematic',        // thematic | political | physical | topographic | OS
  scale: 'world',              // world | continental | national | regional | local
  coverage: 'Global',
  key_features: ['climate zone boundaries', 'latitude lines', 'ocean labels'],
  source: 'Philip\'s Primary School Atlas p.12',
  digital_equivalent: 'Google Earth climate overlay',
  display_category: 'Content Vehicle'
})

(:Concept)-[:REQUIRES_MAP]->(:MapResource)
(:ContentVehicle)-[:USES_MAP]->(:MapResource)
```

### New properties on ContentVehicle (Geography-specific)
```
cv.data_sources = ['Monthly temp/rainfall for 6 locations']
cv.photograph_set = ['Amazon canopy aerial', 'Sahara sand dunes', 'UK deciduous woodland autumn']
cv.fieldwork_type = 'data_collection'          // observation | data_collection | sketch_mapping | survey
cv.fieldwork_equipment = ['clipboards', 'thermometers', 'rain gauges', 'tally charts']
cv.fieldwork_location = 'school_grounds'       // school_grounds | local_area | urban | rural | residential
cv.contrasting_localities = ['Nottingham, UK', 'Toulouse, France']
cv.risk_assessment_notes = 'Outdoor learning: standard school trip protocols apply'
```

### New property on ConceptCluster
```
cc.estimated_lessons = 3
cc.estimated_weeks = 1.5
```

### New property on Concept (vocabulary)
```
c.vocabulary_definitions = {
  'climate zone': 'A large area of the Earth with a similar pattern of temperature and rainfall.',
  'biome': 'A large natural area defined by its climate and the type of plants that grow there.'
}
```

---

## Comparison with Other Subjects

| Feature | Geography | History | Science | Maths | English |
|---|---|---|---|---|---|
| ContentVehicles | ❌ None | ✅ Case studies | ✅ Investigations | ✅ Worked examples | ✅ Text studies |
| DifficultyLevels | ❌ None | ❌ None | ❌ None | ✅ Y3 pilot | ❌ None |
| Disciplinary skills links | ✅ 18 concept-level | ✅ 18 concept-level | ✅ 34 concept-level | ✅ Programme-level | ✅ Programme-level |
| Thinking lenses | ✅ 2 per cluster | ✅ 2 per cluster | ✅ 2 per cluster | ✅ 2 per cluster | ✅ 2 per cluster |
| Subject-specific needs | Maps, data, fieldwork | Primary sources | Equipment, safety | Manipulatives, CPA | Texts, genre models |
| Estimated teaching time | ❌ None | ❌ None | ❌ None | ❌ None | ❌ None |

Geography is uniquely disadvantaged by the absence of ContentVehicles because it is the most resource-dependent humanities subject. History can be taught with a good source pack and narrative skill. Geography requires maps, data, photographs, and (ideally) fieldwork — all of which need to be explicitly specified and provided.

---

## Summary

The knowledge graph gives me a solid curriculum skeleton for Geography: I know *what* to teach (concepts, objectives, domains), *in what order* (prerequisites, domain progression), *with what cognitive framing* (thinking lenses), and *using what geographical skills* (DEVELOPS_SKILL links). The learner profile tells me *how* to teach (interaction types, scaffolding level, feedback tone).

What it cannot tell me is *with what resources*. And for Geography, the resources *are* the lesson. A lesson on climate zones without a world map, a lesson on rivers without OS map extracts, a lesson on regional comparison without data from real places — these are not Geography lessons. They are Geography talks.

**Path to 8/10:**
1. Add 8-10 ContentVehicles for KS2 Geography with geography-specific properties
2. Add DifficultyLevel nodes for all KS2 Geography concepts
3. Add cross-subject CO_TEACHES links (Geography↔Science, Geography↔Maths)
4. Add estimated teaching time to all ConceptCluster nodes
5. Add child-friendly vocabulary definitions

**Current readiness: 4/10** — strong conceptual framework, but not yet teach-ready without significant teacher resource creation.

---

## Teaching Artefacts Needed

The lesson plan gets me from "no plan" to "plan on paper." But to walk into my Y4 classroom on Monday morning and actually teach this climate zones lesson, I still need to create or source a stack of physical and digital artefacts. Here are my top 5, in the order I'd reach for them.

### 1. Knowledge Organiser (CRITICAL — print, project, stick on wall)

**What it is:** A single A4 sheet containing: the 6 climate zones with definitions, a small world map showing zone distribution, the water cycle diagram with labels, key vocabulary with child-friendly definitions, and one worked example of a geographical comparison.

**Why it matters for Geography:** Geography has a uniquely heavy vocabulary and spatial knowledge load. My Y4s need to hold climate zone names, biome characteristics, water cycle processes, and map conventions in working memory simultaneously. A knowledge organiser externalises that load — it goes on the desk during the lesson, on the working wall for the half-term, and into the homework folder for retrieval practice at home. It is the single artefact that ties the whole unit together.

**What the graph could provide:** The concept descriptions, key vocabulary lists, misconceptions, and thinking lens key questions are all present in the graph. A knowledge organiser generator could pull vocabulary from `key_vocabulary`, the core explanation from the concept `description`, the thinking lens key question, and the prerequisite links to show "what you already know." The missing piece is the visual content — the world map, the water cycle diagram, the biome photographs. The graph could specify *what* visuals are needed even if it cannot generate them.

**Could the graph generate this today?** Partially. ~60% of the text content is there. The visual layout and images would need a template engine and image assets.

### 2. Differentiated Map Worksheets (print, hand out)

**What it is:** Three versions of a world outline map worksheet:
- **Support:** Climate zone boundaries pre-drawn, pupils colour and label from a word bank
- **Expected:** Latitude lines marked, pupils draw zone boundaries and label independently
- **Greater depth:** Blank outline, pupils draw latitude lines, zone boundaries, and annotate with biome names and characteristics

**Why it matters for Geography:** Map work is the defining practical activity of the subject — it is to Geography what calculation is to Maths or close reading is to English. Every Geography lesson I teach involves pupils working on a map in some form. Differentiated map worksheets are the single most-used physical resource in my classroom. I currently spend more time creating and adapting map worksheets than any other planning activity.

**What the graph could provide:** The DifficultyLevel nodes (if they existed for Geography) would directly map to the three worksheet tiers: entry = support, expected = standard, greater_depth = extension. The concept teaching guidance specifies what map features to include. The content guidelines (Lexile, sentence length) would constrain the text on each sheet.

**Could the graph generate this today?** No. No DifficultyLevel nodes for Geography, no map templates, no visual generation capability. This is a hard gap — it requires both structured data (difficulty tiers) and visual assets (base maps).

### 3. Climate Data Cards / Enquiry Pack (print, hand out)

**What it is:** A set of 6 laminated cards, each showing: location name, coordinates, a small location map, monthly temperature data (table + bar chart), monthly rainfall data (table + bar chart), and 2-3 photographs of the landscape. Pupils use these as evidence to identify climate zones and compare locations.

**Why it matters for Geography:** Geographical enquiry — asking questions and using evidence to answer them — is the core disciplinary skill. My Y4s cannot do genuine enquiry without real data to analyse. Climate data cards are the geography equivalent of a science experiment: they make the abstract concrete. I use data packs in almost every Geography unit. Currently I build them by hand from Met Office and World Bank data, which takes hours.

**What the graph could provide:** If ContentVehicles existed for Geography with `data_sources` properties containing actual numerical data (monthly temperatures, rainfall totals, coordinates), a data card generator could format this into print-ready cards. The graph already links concepts to geographical skills ("data collection and presentation"), so it knows *that* data is needed — it just does not hold *what* data.

**Could the graph generate this today?** No. Zero ContentVehicles, zero data. This is the gap that most directly reduces my readiness score.

### 4. Vocabulary Word Mat (print, laminate, desk resource)

**What it is:** An A4 landscape sheet with 15-20 key terms organised by concept (climate zone terms on the left, water cycle terms on the right), each with: the word in bold, a simple definition (max 15 words), a small illustration or diagram, and a sentence starter showing how to use the word in geographical writing ("The tropical zone is located near the Equator because...").

**Why it matters for Geography:** Geography has a dual vocabulary challenge: technical terms (evaporation, precipitation, infiltration) AND place-specific proper nouns (Equator, Tropics of Cancer, Arctic Circle, Amazon, Sahara). My Y4s need both types available during writing tasks. The word mat sits on the desk during independent work and is the first thing a struggling pupil reaches for. It directly supports the content guidelines (academic vocabulary OK with brief inline definition on first use).

**What the graph could provide:** The `key_vocabulary` fields on concepts give me a comprehensive term list. The content guidelines specify the language level (Lexile 300-500L, max 18 words). What is missing is: child-friendly definitions, sentence starters, and illustrations. If the graph added `vocabulary_definitions` (as I proposed), a word mat generator could produce these automatically with a template.

**Could the graph generate this today?** Partially. The term lists are there (~60%). Definitions and sentence starters are not. No illustration capability.

### 5. Assessment Grid / Success Criteria Rubric (print for teacher, project for pupils)

**What it is:** A 4-column rubric aligned to the success criteria:

| Criterion | Working towards | Expected | Greater depth |
|---|---|---|---|
| Name climate zones | Names 2-3 zones | Names all 6 zones and locates on map | Explains relationship between latitude and zone |
| Describe biomes | Matches 1-2 biomes to photos | Describes characteristics of 3+ biomes | Explains how climate determines biome type |
| Water cycle | Sequences 3+ stages | Labels all stages and explains as system | Predicts effects of changing one component |
| Geographical vocabulary | Uses 3-4 key terms | Uses 8+ key terms accurately | Uses vocabulary in extended geographical writing |

**Why it matters for Geography:** Without a rubric, my formative assessment during the lesson is impressionistic. With one, I can quickly categorise each pupil's response against the criteria, identify who needs intervention, and have evidence for my assessment records. The rubric also goes on the board so pupils can self-assess — "Am I at expected? What do I need to do to reach greater depth?"

**What the graph could provide:** The DifficultyLevel nodes (entry/developing/expected/greater_depth) with `example_task`, `example_response`, and `common_errors` would directly generate each cell of this grid. The concept descriptions provide the content. The interaction types suggest the assessment format. If DifficultyLevels existed for Geography, this artefact could be almost entirely auto-generated.

**Could the graph generate this today?** No. No DifficultyLevel nodes for Geography. I built the rubric above from professional judgement.

---

### Artefacts I Considered But Ranked Lower

| Artefact | Why it ranked lower for Geography Y4 |
|---|---|
| **Presentation slides** | I project maps and diagrams, but the knowledge organiser + map worksheets matter more than a slide deck. I can teach from the board. |
| **Homework sheet** | Useful but secondary — a retrieval quiz pulling from the knowledge organiser is my standard homework, and I can write 5 questions faster than I can design a worksheet. |
| **Working wall display** | Important for the half-term, but it is built *from* the knowledge organiser, vocabulary mat, and pupil work — not a separate generated artefact. |
| **Parent-facing summary** | Nice to have for the curriculum newsletter. Low priority compared to in-classroom resources. |
| **Interactive whiteboard resource** | Would be valuable for a digital map explorer, but is a platform feature rather than a generated artefact. |
| **Marking rubric (detailed)** | The assessment grid above covers formative use. A more detailed rubric with exemplar pupil work would be helpful for summative assessment, but Geography at KS2 is not formally assessed, so this is lower priority than for Maths or English. |

### What I'd Add That's Not on Your List

**Fieldwork data collection sheet** — A structured recording sheet for outdoor geographical enquiry: what to observe, where to record measurements, how to sketch a field map, what to count or measure. This is unique to Geography (and Science) and is the artefact most likely to be forgotten when planning from a desk. The graph's DEVELOPS_SKILL links to "Fieldwork: data collection and presentation" should generate these, but currently cannot.

---

### Summary: Teaching Artefact Generation Readiness

| Artefact | Could generate today? | What's missing? |
|---|---|---|
| Knowledge organiser | ~60% of text content | Vocabulary definitions, visual assets (maps, diagrams) |
| Differentiated map worksheets | No | DifficultyLevel nodes, map templates, visual generation |
| Climate data cards | No | ContentVehicles with actual data, photograph references |
| Vocabulary word mat | ~40% (terms only) | Definitions, sentence starters, illustrations |
| Assessment grid | No | DifficultyLevel nodes with example tasks/responses |
| Fieldwork data collection sheet | No | Fieldwork plan data in ContentVehicles |

**The pattern:** The graph holds the *curriculum intelligence* (what to teach, in what order, at what level) but not the *resource intelligence* (with what materials, what data, what visuals). For Geography, the resource intelligence is 70% of the planning workload. The system can tell me I need a world climate zone map — but it cannot give me one, describe one precisely enough to source one, or generate one.

---

*Gap analysis by Mr. Obi, Y4 class teacher and humanities subject lead, Nottingham.*
*Based on graph queries of all 5 KS2 Geography clusters + Y4 learner profile.*
