# Science Teacher Review: ScienceTopicSuggestion Schema

**Reviewer**: KS2 + KS3 Science Specialist
**Date**: 2026-02-24
**Scope**: ScienceTopicSuggestion schema, VehicleTemplates for Science, and content generation requirements

---

## 1. Subject-Specific Property Review

### Proposed Properties

| Property | Type | Required | Verdict | Rationale |
|---|---|---|---|---|
| `enquiry_type` | string | Yes | **MODIFY** | Must use a controlled vocabulary — see detailed analysis below |
| `equipment` | string[] | No | **MODIFY** — make Required | Every practical topic needs equipment. Even research enquiries need "books, tablets, or teacher-prepared information sheets". Without this, the AI tutor will hallucinate equipment that schools don't have |
| `safety_notes` | string | No | **MODIFY** — make Required | Non-negotiable for a children's platform. CLEAPSS provides model risk assessments for nearly all school practicals. An AI generating a lesson about acids without safety notes is a safeguarding failure, not just a gap. Even "low risk" topics should state that explicitly |
| `expected_outcome` | string | No | **MODIFY** — make Required | The AI tutor must know what correct understanding looks like. Without this, it cannot assess whether a child's response is on track, nor generate valid assessment tasks |

### Properties to ADD

| Property | Type | Required | Rationale |
|---|---|---|---|
| `recording_format` | string[] | Yes | How data should be recorded and presented is curriculum-specific and age-dependent. At KS2 a sound investigation uses "observations table -> pattern statement"; at KS3 a photosynthesis investigation uses "results table -> line graph with line of best fit -> conclusion referencing equation". The AI needs this to generate appropriate data recording scaffolds. The existing CVs already have this and teachers rely on it |
| `misconceptions` | string[] | Yes | This is the single highest-leverage property for AI lesson generation. The Primary Science Teaching Trust identifies misconceptions as the #1 barrier to learning in Science. If the AI doesn't know that children think "heavier objects fall faster" when teaching forces, it will fail to address the most common errors. The DifficultyLevel `common_errors` property captures per-concept errors, but topic-level misconceptions capture the broader conceptual misunderstandings that span multiple concepts (e.g. "plants get their food from the soil" spans photosynthesis, nutrition, and ecology concepts) |
| `science_discipline` | string | Yes | At KS3, Science splits into Biology, Chemistry, Physics. The schema lists `ScienceTopicSuggestion` covering "Science, Biology, Chemistry, Physics" — but the AI needs to know which discipline a topic belongs to. This matters for: (a) matching to the correct KS3 programme of study, (b) applying discipline-specific safety protocols (Chemistry has COSHH requirements that Biology doesn't), (c) surfacing the right Working Scientifically skills. Controlled vocabulary: `general_science`, `biology`, `chemistry`, `physics` |
| `hazard_level` | string | Yes | A simple triage flag: `low` (no specific hazards — observation, research), `standard` (normal lab procedures — gloves, goggles), `elevated` (CLEAPSS model risk assessment required — acids, heating, chemicals, biological material). This lets the AI tutor (a) flag safety to parents in home-learning contexts, (b) adjust language around safety in generated content, (c) indicate when teacher supervision is essential vs desirable |
| `variables` | object | No | For `fair_test` and `pattern_seeking` enquiry types only. Structure: `{ independent: string, dependent: string, controlled: string[] }`. The existing CVs already have this as three separate flat properties — it should be formalised as a typed sub-object. For non-fair-test enquiries, this is null/absent. The AI needs this to generate valid experimental design scaffolds — "What will you change? What will you measure? What will you keep the same?" is the foundational structure of fair testing at KS2-KS3 |

### Properties NOT needed (considered and rejected)

| Property | Rationale for exclusion |
|---|---|
| `reaction_type` (Chemistry-specific) | Over-engineers the schema. The `enquiry_type` + `expected_outcome` + `definitions` combination captures enough for the AI to generate Chemistry-appropriate content. Reaction types (combustion, neutralisation, displacement) are already encoded in concept data |
| `practical_tier` (Biology-specific) | Biology practicals don't have a meaningful tiering system distinct from `hazard_level`. The distinction between microscopy, dissection, and fieldwork is already captured by `enquiry_type` and `equipment` |
| `maths_skills_required` | Tempting (Science relies heavily on Maths), but this is better handled via the graph's existing `cross_curricular_hooks` universal property + the `DEVELOPS_SKILL` relationships to `MathematicalReasoning` nodes. Adding it as a property would duplicate graph structure |

### `enquiry_type` Controlled Vocabulary

The UK National Curriculum identifies five canonical types of scientific enquiry at KS2 (Working Scientifically). The ASE and various curriculum guidance documents extend this to seven types that are used across KS2-KS3. The proposed schema should use the following controlled vocabulary:

| Value | NC Basis | Description | Key Age Range |
|---|---|---|---|
| `fair_test` | NC KS2 statutory | Controlled investigation: change one variable, measure another, keep others the same | Y3-Y11 |
| `observation_over_time` | NC KS2 statutory | Systematic observation and recording at intervals (e.g. plant growth over 3 weeks, moon phases) | Y1-Y9 |
| `pattern_seeking` | NC KS2 statutory | Looking for correlations between variables without necessarily controlling them (e.g. "Do people with longer legs jump further?") | Y2-Y11 |
| `identifying_and_classifying` | NC KS2 statutory | Sorting, grouping, and using classification keys based on observable properties | Y1-Y9 |
| `research` | NC KS2 statutory | Finding answers from secondary sources (books, websites, databases, expert testimony) | Y1-Y11 |
| `modelling` | NC KS3 WS | Using physical or mathematical models to explain phenomena (e.g. particle model, food web models, circuit simulations) | Y5-Y11 |
| `secondary_data_analysis` | NC KS3 WS | Analysing existing datasets to identify trends (e.g. public health data, climate data, astronomical observations) | Y5-Y11 |

**Important**: The existing CVs use `observation` (not `observation_over_time`). I recommend the full NC term because "observation" is ambiguous — all Science involves observation. The `_over_time` qualifier is what makes it a distinct enquiry type (systematic repeated measurement).

The existing CVs also omit `modelling` and `secondary_data_analysis`, which are critical at KS3. A Y8 lesson on the particle model of matter is fundamentally a modelling enquiry, not a fair test or observation. If the controlled vocabulary doesn't include it, the AI will be forced to shoehorn it into an ill-fitting type.

---

## 2. Universal Property Review

### Changes to shared universal properties

| Property | Verdict | Rationale |
|---|---|---|
| `suggestion_type` | **ADD VALUE** | Add `enquiry_topic` to the enumeration. Science "topics" are often structured around an enquiry ("Friction Fair Test", "Photosynthesis Rate Investigation") rather than a content topic ("Roman Britain"). The distinction matters: `exemplar_topic` implies content flexibility; `enquiry_topic` implies the enquiry design IS the topic |
| `pedagogical_rationale` | **KEEP** | Essential for Science. The rationale for "Friction Investigation" isn't just "teaches forces" — it's "this is the most accessible fair test in the curriculum: pupils can see and feel friction, the variables are tangible, and the measurement (distance) is straightforward" |
| `definitions` | **KEEP** | Critical for Science vocabulary load. Science has the highest vocabulary density of any primary subject. A single Y4 unit can introduce 8-12 new technical terms |
| `common_pitfalls` | **MODIFY** | For Science, this should be **Required**, not optional. Every Science topic has well-documented pitfalls (e.g. "pupils confuse mass and weight", "pupils think electricity is used up in a circuit"). Unlike History where pitfalls are pedagogical (not enough time on sources), Science pitfalls are conceptual and directly affect what the AI generates |
| `cross_curricular_hooks` | **KEEP** | Science has the strongest cross-curricular links of any subject: Maths (measurement, graphs, calculation), English (report writing, scientific vocabulary), Geography (ecosystems, rocks, water cycle), DT (materials, structures, food) |
| `curriculum_reference` | **KEEP but STRENGTHEN** | For Science, this should include the specific NC programme of study reference (e.g. "Year 4 Sound: identify how sounds are made, associating some of them with something vibrating"). This is what teachers use to check alignment |

### Properties that should stay universal (not subject-specific)

- `choice_group` — works for Science. Some topics genuinely are interchangeable: at Y5 you could investigate friction OR air resistance to teach forces. The `choice_group` captures this.
- `display_*` properties — fine as universal.

---

## 3. VehicleTemplate Critique

### Existing Science templates — assessment

| # | Template | Verdict | Notes |
|---|---|---|---|
| 3 | `fair_test` | **KEEP** | Session structure is correct: question -> hypothesis -> method -> data_collection -> analysis -> conclusion. This is the gold standard for UK primary and secondary Science |
| 4 | `observation_enquiry` | **MODIFY** | Rename to `observation_over_time` to match the NC terminology. Session structure should be: question -> prediction -> observation_schedule -> systematic_recording -> pattern_identification -> conclusion. The current structure omits `prediction` (critical at KS2+) and `observation_schedule` (what/when/how often to observe) |
| 5 | `pattern_seeking` | **KEEP** | Structure is sound. Add `prediction` step between `question` and `data_gathering` |
| 6 | `research_enquiry` | **KEEP** | Works well for Science research topics (evolution, human body, space). Note: at KS3, "research" increasingly means "secondary data analysis" rather than "look it up in a book" |
| 9 | `investigation_design` | **MODIFY** | This overlaps heavily with `fair_test`. In practice, "investigation design" at KS3 means pupils design their OWN method (not follow a given one). Rename to `open_investigation` and restructure: question_framing -> hypothesis -> pupil_method_design -> peer_method_review -> data_collection -> analysis -> method_evaluation. The key difference from `fair_test` is pupil autonomy over method |
| 10 | `fieldwork` | **KEEP** | Essential for ecology (KS2 habitats, KS3 ecosystems). Structure is correct |
| 2 | `case_study` | **KEEP for Science** | Works for environmental topics (pollution case studies, disease outbreaks, climate change impacts) |

### Templates to ADD for Science

| Template | Subjects | Session Structure | Rationale |
|---|---|---|---|
| `modelling_enquiry` | Science, Geography | stimulus -> model_building -> prediction_from_model -> testing_against_reality -> model_refinement -> evaluation | The particle model, food web models, circuit models, Earth/Sun/Moon models — modelling is a core KS3 enquiry type and increasingly important at upper KS2. The AI needs a distinct pedagogical pattern for "build a model and test it" vs "do a fair test" |
| `identifying_and_classifying` | Science | question -> observation -> property_identification -> grouping_criteria -> classification -> key_construction | Classification is one of the 5 NC enquiry types but has no template. Y3 rocks, Y4 living things, Y6 microorganisms, KS3 biological classification — all use this pattern. The existing `observation_enquiry` doesn't capture the sorting/grouping/key-building structure |
| `secondary_data_analysis` | Science, Geography, Maths | question -> dataset_selection -> data_exploration -> pattern_identification -> analysis -> conclusion -> limitations | At KS3, pupils increasingly work with existing datasets (population data, climate records, public health statistics). This is distinct from `research_enquiry` (which is source-based) and from `pattern_seeking` (which involves collecting new data) |

### Templates that need Science-specific session notes

The `case_study` template has a generic session structure. For Science, case studies follow: context_introduction -> evidence_gathering -> scientific_explanation -> evaluation -> implications. The AI should receive a Science-specific `agent_prompt` via `TEMPLATE_FOR` -> KeyStage.

---

## 4. TopicSuggestion Inventory

### KS2 Science — proposed topics

#### Year 3

| Name | Type | Enquiry Type | Rationale |
|---|---|---|---|
| Plant Growth Investigation | `prescribed_topic` | `fair_test` | NC Y3 statutory: "explore the requirements of plants for life and growth" |
| Rocks and Fossils Classification | `prescribed_topic` | `identifying_and_classifying` | NC Y3 statutory: "compare and group together different kinds of rocks" |
| Light and Shadow Investigation | `prescribed_topic` | `fair_test` | NC Y3 statutory: "recognise that light from the sun can be dangerous" + shadow formation |
| Magnet Investigation | `prescribed_topic` | `fair_test` | NC Y3 statutory: "compare how things move on different surfaces" + magnetic materials |
| Skeleton and Muscles | `prescribed_topic` | `research` | NC Y3 statutory: "identify that humans and some animals have skeletons and muscles" |

#### Year 4

| Name | Type | Enquiry Type | Rationale |
|---|---|---|---|
| Sound Investigation | `prescribed_topic` | `pattern_seeking` | NC Y4 statutory: "identify how sounds are made" + pitch/volume patterns |
| States of Matter | `prescribed_topic` | `observation_over_time` | NC Y4 statutory: "compare and group materials" + evaporation investigation |
| Electrical Circuits | `prescribed_topic` | `fair_test` | NC Y4 statutory: "construct a simple series electrical circuit" |
| Digestive System | `prescribed_topic` | `research` | NC Y4 statutory: "describe the simple functions of the basic parts of the digestive system" |
| Living Things and Habitats Classification | `prescribed_topic` | `identifying_and_classifying` | NC Y4 statutory: "recognise that living things can be grouped in a variety of ways" + classification keys |
| Teeth and Food Chains | `prescribed_topic` | `identifying_and_classifying` | NC Y4 statutory: "identify the different types of teeth" + "construct and interpret food chains" |

#### Year 5

| Name | Type | Enquiry Type | Rationale |
|---|---|---|---|
| Friction Investigation | `prescribed_topic` | `fair_test` | NC Y5 statutory: "identify the effects of... friction, that act between moving surfaces" |
| Dissolving and Separating Mixtures | `prescribed_topic` | `fair_test` | NC Y5 statutory: "know that some materials will dissolve in liquid" + separation methods |
| Earth and Space | `prescribed_topic` | `modelling` | NC Y5 statutory: "describe the movement of the Earth, and other planets, relative to the Sun" — fundamentally a modelling/research topic, not a fair test |
| Life Cycles | `prescribed_topic` | `observation_over_time` | NC Y5 statutory: "describe the life process of reproduction in some plants and animals" |
| Forces: Air and Water Resistance | `prescribed_topic` | `fair_test` | NC Y5 statutory: "identify the effects of air resistance, water resistance" |
| Reversible and Irreversible Changes | `prescribed_topic` | `observation_over_time` | NC Y5 statutory: "demonstrate that dissolving, mixing and changes of state are reversible" |

#### Year 6

| Name | Type | Enquiry Type | Rationale |
|---|---|---|---|
| Evolution and Adaptation | `prescribed_topic` | `research` | NC Y6 statutory: "recognise that living things have changed over time" + natural selection |
| Electrical Circuits (Y6) | `prescribed_topic` | `fair_test` | NC Y6 statutory: "associate the brightness of a lamp or the volume of a buzzer with the number and voltage of cells" |
| Light: How We See | `prescribed_topic` | `fair_test` | NC Y6 statutory: "recognise that light appears to travel in straight lines" |
| Heart and Circulation | `prescribed_topic` | `research` | NC Y6 statutory: "identify and name the main parts of the human circulatory system" |
| Classification of Living Things (Y6) | `prescribed_topic` | `identifying_and_classifying` | NC Y6 statutory: "describe how living things are classified into broad groups" + Linnaeus system introduction |
| Healthy Living | `prescribed_topic` | `research` | NC Y6 statutory: "recognise the impact of diet, exercise, drugs and lifestyle on the way their bodies function" |

### KS3 Science — proposed topics (sample per discipline)

#### Biology

| Name | Type | Enquiry Type | Discipline |
|---|---|---|---|
| Cell Structure and Microscopy | `prescribed_topic` | `observation_over_time` | biology |
| Photosynthesis Rate Investigation | `prescribed_topic` | `fair_test` | biology |
| Ecosystem Sampling and Food Webs | `prescribed_topic` | `fieldwork` (via template) | biology |
| Respiration Investigation | `prescribed_topic` | `fair_test` | biology |
| Human Reproduction | `prescribed_topic` | `research` | biology |
| Biological Classification | `prescribed_topic` | `identifying_and_classifying` | biology |
| Inheritance and Variation | `prescribed_topic` | `secondary_data_analysis` | biology |

#### Chemistry

| Name | Type | Enquiry Type | Discipline |
|---|---|---|---|
| Acids, Alkalis and Neutralisation | `prescribed_topic` | `fair_test` | chemistry |
| Particle Model and Changes of State | `prescribed_topic` | `modelling` | chemistry |
| Chemical Reactions: Metals and Acids | `prescribed_topic` | `pattern_seeking` | chemistry |
| Elements, Compounds and Mixtures | `prescribed_topic` | `identifying_and_classifying` | chemistry |
| Combustion and Oxidation | `prescribed_topic` | `observation_over_time` | chemistry |
| The Periodic Table | `prescribed_topic` | `pattern_seeking` | chemistry |
| Exothermic and Endothermic Reactions | `prescribed_topic` | `fair_test` | chemistry |

#### Physics

| Name | Type | Enquiry Type | Discipline |
|---|---|---|---|
| Forces and Motion | `prescribed_topic` | `fair_test` | physics |
| Energy Transfers and Efficiency | `prescribed_topic` | `fair_test` | physics |
| Waves: Sound and Light | `prescribed_topic` | `pattern_seeking` | physics |
| Electricity and Magnetism | `prescribed_topic` | `fair_test` | physics |
| Pressure in Fluids | `prescribed_topic` | `fair_test` | physics |
| Speed and Distance-Time Graphs | `prescribed_topic` | `secondary_data_analysis` | physics |
| Space: The Solar System | `prescribed_topic` | `modelling` | physics |

**Note on Science `suggestion_type`**: Almost all Science topics at KS2-KS3 are `prescribed_topic` because the NC specifies content. Unlike History (where "Ancient Egypt" is one of several options), Science doesn't offer menu choices between topics. The flexibility in Science is in *how* you teach it (enquiry type, context, depth) rather than *what* you teach. This is a key difference the schema should acknowledge — Science has fewer `open_slot` and `exemplar_topic` entries than humanities subjects.

---

## 5. Content Generation Requirements

### What the AI needs to generate a good KS2 lesson (e.g. Y4 Sound Investigation)

1. **Enquiry type** (`pattern_seeking`) — tells the AI the pedagogical structure isn't "change one variable" but "look for a pattern across multiple observations"
2. **Equipment list** — the AI must only suggest equipment that a primary school plausibly has. "Tuning forks, rulers, elastic bands, shoe boxes" is realistic; "oscilloscope" is not
3. **Safety notes** — even for "low risk" topics. "Keep volume levels reasonable. Tuning forks can be sharp." The AI must include these in any generated lesson plan
4. **Variables** (when applicable) — for a fair test, the AI needs to scaffold: "What will you change? What will you measure? What will you keep the same?"
5. **Recording format** — tells the AI what data presentation to scaffold. Y4 should get "observations table -> pattern statement"; Y8 should get "results table -> scatter graph with line of best fit -> statistical analysis"
6. **Expected outcome** — the AI needs to know the correct scientific explanation to assess pupil responses and generate marking guidance
7. **Misconceptions** — the AI needs to know "pupils often think sound can only travel through air" to generate diagnostic questions that surface this error
8. **Definitions** — the AI needs the precise technical vocabulary to scaffold (with age-appropriate definitions) rather than using informal language that creates later misconceptions

### What the AI needs for a KS3 assessment task (e.g. Y8 Photosynthesis)

All of the above, plus:
- **Science discipline** (`biology`) — to select appropriate vocabulary register and assessment format
- **Hazard level** (`standard`) — to include safety reminders in any practical assessment component
- **Variables** — for the classic pondweed experiment: independent (light intensity/distance), dependent (bubble count), controlled (temperature, CO2, pondweed size)
- **Recording format** — the AI needs to know that Y8 assessment expects "graph with labelled axes, units, line of best fit" not just "draw a bar chart"
- **Misconceptions** — "pupils think plants get their food from the soil" is the most persistent misconception in biology; the AI must probe for this

### What the AI needs for a video script

- **Expected outcome** — the video must explain the correct science
- **Misconceptions** — the video should explicitly address common errors ("You might think that... but actually...")
- **Equipment** — the video should show realistic equipment
- **Safety notes** — the video must model safe practice

### What the AI needs for parent-facing content

- **Pedagogical rationale** — parents need to understand WHY their child is doing a fair test, not just what a fair test is
- **Definitions** — parents need the same vocabulary their child is learning
- **Expected outcome** — parents need to know what "understanding" looks like at this age

---

## 6. Cross-Curricular Hooks

Science has the richest cross-curricular connections of any NC subject. These should be captured in `cross_curricular_hooks`:

### Science <-> Mathematics (strongest link)

| Science Topic | Maths Connection |
|---|---|
| Fair tests (all) | Measurement in standard units, tables, bar charts (KS2), line graphs, scatter graphs, mean/range (KS3) |
| Forces and motion | Speed = distance / time, reading scales, plotting distance-time graphs |
| Electricity | Series/parallel calculations, Ohm's law at KS4 |
| Photosynthesis rate | Continuous data, line graphs, rates of change |
| Classification | Venn diagrams, Carroll diagrams, sorting by criteria |
| States of matter | Temperature measurement, reading thermometers, negative numbers |

### Science <-> English

| Science Topic | English Connection |
|---|---|
| All enquiries | Report writing (Y3+ non-fiction), using conjunctions to explain cause and effect |
| Evolution | Narrative of change over time, persuasive writing (endangered species) |
| Research enquiries | Note-taking from secondary sources, synthesising information |
| All | Technical vocabulary (etymology: Latin/Greek roots — "photo" = light, "synthesis" = putting together) |

### Science <-> Geography

| Science Topic | Geography Connection |
|---|---|
| Rocks and fossils | Rock cycle, landscape formation, geological time |
| Ecosystems/habitats | Biomes, climate zones, human impact on environment |
| Water cycle | Weather and climate, rivers, erosion |
| Earth and Space | Time zones, seasons, day length |

### Science <-> Design Technology

| Science Topic | DT Connection |
|---|---|
| Electrical circuits | DT circuits unit (KS2), control systems |
| Forces | Structures, mechanisms (levers, pulleys, gears) |
| Materials | Properties of materials, material selection for purpose |
| Food and nutrition | DT Food (cooking, food hygiene, nutrition) |

### Science <-> History

| Science Topic | History Connection |
|---|---|
| Evolution | Darwin, Victorian scientific debate |
| Medicine/health | History of medicine (KS3) |
| Electricity | History of invention (Faraday, Edison) |
| Earth and Space | Copernicus, Galileo, history of astronomy |

---

## 7. Stress Test Scenarios

### Scenario 1: Y4 Sound Investigation (KS2, pattern seeking)

**The lesson**: Pupils explore how pitch changes when you change the length of a vibrating object (ruler over table edge, elastic bands on shoe box).

**Does the schema capture everything?**

- `enquiry_type: "pattern_seeking"` — Yes, correct
- `equipment: ["rulers", "elastic bands", "shoe boxes", "tuning forks", "rice", "drum skin"]` — Yes
- `safety_notes: "Keep volume reasonable. Demonstrate correct use of tuning forks."` — Yes
- `expected_outcome: "Shorter/tighter = higher pitch; bigger vibrations = louder"` — Yes
- `recording_format: ["observations table", "pattern statement", "vibration diagram"]` — Yes
- `variables: null` — Correct, pattern seeking doesn't use controlled variables in the same way
- `misconceptions: ["Sound can only travel through air", "Louder sounds travel faster", "Pitch and volume are the same thing"]` — **CRITICAL: without this the AI won't probe these errors**
- `hazard_level: "low"` — Yes
- `science_discipline: "general_science"` — Yes (KS2 is not split)

**Verdict**: Schema works well. The `misconceptions` and `recording_format` additions are essential for this scenario.

### Scenario 2: Y8 Photosynthesis Rate Investigation (KS3, fair test)

**The lesson**: Pupils investigate how light intensity affects the rate of photosynthesis using pondweed (Elodea) and counting oxygen bubbles.

**Does the schema capture everything?**

- `enquiry_type: "fair_test"` — Yes
- `equipment: ["Elodea pondweed", "beaker", "lamp", "ruler", "stopwatch", "sodium bicarbonate", "thermometer"]` — Yes
- `safety_notes: "Lamp gets hot. Ensure water does not contact electrical equipment."` — Yes
- `expected_outcome: "Rate increases with light intensity, then plateaus (limiting factor: CO2 or temperature)"` — Yes
- `recording_format: ["results table", "line graph (light intensity vs bubble rate)", "conclusion referencing equation"]` — Yes
- `variables: { independent: "distance of lamp from pondweed", dependent: "oxygen bubbles per minute", controlled: ["same pondweed", "same temperature", "same volume", "same NaHCO3 concentration"] }` — Yes
- `misconceptions: ["Plants only respire at night", "Plants get food from soil", "Photosynthesis and respiration are opposites that cancel out"]` — Essential
- `hazard_level: "standard"` — Yes (hot lamp, water near electrics)
- `science_discipline: "biology"` — Yes

**Verdict**: Schema works. The `variables` object and `science_discipline` are both essential for KS3 fair tests.

### Scenario 3: KS3 Particle Model (Y7-8, modelling enquiry)

**The lesson**: Pupils use the particle model to explain properties of solids, liquids, and gases, and to predict behaviour during changes of state.

**Does the schema capture everything?**

- `enquiry_type: "modelling"` — **ONLY if we add this to the controlled vocabulary**. Without it, this topic would be forced into `observation` or `research`, neither of which captures the core pedagogy (build a model -> make predictions from it -> test against reality -> refine)
- `equipment: ["marbles or ball bearings (particle model)", "tray", "Bunsen burner", "ice", "stearic acid", "thermometers"]` — Yes
- `safety_notes: "Use water baths for heating. Stearic acid is hot — use tongs. Goggles. Hair tied back near Bunsen burners."` — Yes
- `expected_outcome` — Yes
- `recording_format: ["particle diagrams for each state", "heating/cooling curve graph", "annotated model diagram"]` — Yes
- `variables` — Partially applicable (the heating curve part is observation over time, not a controlled fair test)
- `misconceptions: ["Particles expand when heated", "There is air between particles", "Particles in a liquid are further apart than in a solid (they're roughly the same distance)", "Ice molecules are colder than water molecules"]` — Essential
- `hazard_level: "standard"` — Yes

**Verdict**: Schema works IF `modelling` is in the enquiry type vocabulary. This scenario is the strongest argument for adding it.

### Scenario 4: Y6 Evolution and Adaptation (KS2, research + classification)

**The lesson**: Pupils explore how living things have changed over time using fossil evidence, investigate variation using real data, and explain adaptation with specific examples.

**Does the schema capture everything?**

- `enquiry_type: "research"` — Partially correct. This topic blends research (fossil evidence, Darwin) with classification (grouping adaptations) and secondary data analysis (variation data). **This reveals a limitation**: some topics genuinely span multiple enquiry types. The schema should allow either a primary + secondary enquiry type, or an array.
- **Proposed solution**: Change `enquiry_type` from `string` to `string` (primary) + add `secondary_enquiry_types: string[]` (optional). This keeps the primary type clean for template matching while acknowledging multi-method topics.
- `safety_notes: "No specific hazards. Sensitivity required around evolution/creation."` — Yes, and this illustrates that `safety_notes` covers more than physical safety — it includes pedagogical sensitivity notes
- `misconceptions: ["Evolution is a ladder of progress", "Individuals evolve (no — populations evolve)", "Adaptation is a deliberate choice by the organism", "Humans evolved from monkeys"]` — Essential

**Verdict**: Schema mostly works but reveals the need for `secondary_enquiry_types` or a similar mechanism.

---

## 8. Summary: Top 3 Recommendations

### 1. Add `misconceptions` as a REQUIRED property (Impact: Critical)

**Why**: Misconceptions are the single most important piece of curriculum intelligence for Science. Research from the Primary Science Teaching Trust, Cambridge ECLIPSE project, and decades of science education research consistently shows that unaddressed misconceptions persist into adulthood. An AI tutor generating a forces lesson without knowing "pupils think heavier objects fall faster" will fail to diagnose the most common error.

**What**: `misconceptions: string[]` — Required, minimum 2 entries per topic. Each entry should be a complete sentence stating the misconception in pupil language (e.g. "Heavier objects fall faster than lighter objects" not just "mass/weight confusion").

**Risk of not doing this**: The AI generates lessons that test surface recall rather than probing for deep understanding. Children pass the lesson but retain the misconception. This is the #1 failure mode in Science education.

### 2. Add `modelling` and `secondary_data_analysis` to the enquiry type vocabulary, and add 3 missing VehicleTemplates (Impact: High)

**Why**: The current 5-type vocabulary reflects KS2 only. At KS3, modelling and secondary data analysis are core enquiry types that don't map onto any existing template. Without them, topics like the particle model, Earth and Space, inheritance, and the periodic table have no appropriate pedagogical pattern.

**What**:
- Extend `enquiry_type` controlled vocabulary to 7 types (add `modelling`, `secondary_data_analysis`)
- Rename `observation` to `observation_over_time` (NC terminology)
- Add 3 VehicleTemplates: `modelling_enquiry`, `identifying_and_classifying`, `secondary_data_analysis`
- Consider `secondary_enquiry_types: string[]` for multi-method topics

**Risk of not doing this**: The AI shoehorns modelling lessons into fair test templates, producing pedagogically incoherent content. Teachers would immediately spot that a "particle model" lesson structured as "hypothesis -> method -> data collection" makes no sense.

### 3. Make `equipment`, `safety_notes`, `recording_format`, and `expected_outcome` all REQUIRED (Impact: High)

**Why**: These four properties are the minimum viable set for safe, effective Science lesson generation.

- **Equipment**: Without it, the AI suggests equipment schools don't have (oscilloscopes in primary, or chemicals not CLEAPSS-approved for student use)
- **Safety notes**: This is a children's platform. CLEAPSS provides model risk assessments for a reason. An AI generating an acids lesson without "wear goggles and gloves" is a safeguarding risk. Even "low risk" must be stated explicitly
- **Recording format**: The expected data presentation format is age-dependent and curriculum-linked. Y3 draws pictures; Y6 draws bar charts; Y8 plots scatter graphs with lines of best fit. The AI cannot infer this without being told
- **Expected outcome**: The AI needs to know what correct understanding looks like to generate valid assessment, provide accurate feedback, and avoid reinforcing misconceptions in its explanations

**Risk of not doing this**: Optional properties will be left blank in some topics, forcing the AI to guess. For safety_notes, guessing is unacceptable. For the others, guessing produces generic content that doesn't match the specific topic or age group.

---

## Appendix: Complete Proposed Schema for ScienceTopicSuggestion

| Property | Type | Required | Notes |
|---|---|---|---|
| `enquiry_type` | string (controlled vocab) | Yes | One of: `fair_test`, `observation_over_time`, `pattern_seeking`, `identifying_and_classifying`, `research`, `modelling`, `secondary_data_analysis` |
| `secondary_enquiry_types` | string[] | No | For multi-method topics (e.g. Evolution uses research + classification + secondary data) |
| `science_discipline` | string | Yes | `general_science` (KS1-KS2), `biology`, `chemistry`, `physics` |
| `equipment` | string[] | Yes | Realistic school equipment only |
| `safety_notes` | string | Yes | CLEAPSS-aligned. Must be present even for "low risk" topics |
| `hazard_level` | string | Yes | `low`, `standard`, `elevated` |
| `expected_outcome` | string | Yes | What correct understanding looks like |
| `recording_format` | string[] | Yes | Age-appropriate data presentation formats |
| `misconceptions` | string[] | Yes | Common student errors, stated in pupil language. Minimum 2 |
| `variables` | object | No | For `fair_test` and `pattern_seeking` only: `{ independent: string, dependent: string, controlled: string[] }` |

Plus all universal properties from the briefing.
