# Gap Analysis: Mr. Adebayo -- Geography KS4 (Tectonic Hazards)

**Planner:** Tectonic Hazards: Earthquakes and Volcanoes
**Date:** February 2026 (V8 review)
**V7 score:** 5.0/10 (KS2 Climate & Water Cycle cluster) -> **V8 score:** 7.0/10

---

## Top 5 Data Additions That Would Improve This Planner

### 1. Case Study Data -- Named Examples With Specific Facts

This is the single highest-impact gap for GCSE Geography. The planner names Haiti 2010 and Japan 2011 as locations but provides no case study detail. GCSE mark schemes explicitly reward "specific, located, factual detail." A student who writes "the earthquake in Haiti killed many people" gets 1 mark. A student who writes "the Haiti earthquake on 12 January 2010, magnitude 7.0, killed over 316,000 people and displaced 1.5 million, partly because 80% of buildings in Port-au-Prince were not built to withstand earthquakes" gets 4 marks. The difference is specific data.

What the GeoStudy node needs:

```
case_studies:
  - name: "Haiti Earthquake 2010"
    date: "12 January 2010"
    type: "earthquake"
    magnitude: 7.0
    focus_depth: "13km (shallow)"
    location: "Port-au-Prince, Haiti"
    development_context: "LIC"
    key_facts:
      - "316,000 deaths, 300,000 injured, 1.5 million displaced"
      - "$8 billion economic damage (120% of GDP)"
      - "80% of buildings not earthquake-resistant; no enforced building codes"
      - "No earthquake early warning system"
      - "International aid response: $13.5 billion pledged"
    primary_effects:
      - "Building collapse -- 80% of buildings in Port-au-Prince damaged or destroyed"
      - "Infrastructure destruction -- roads, bridges, port, airport all damaged"
    secondary_effects:
      - "Cholera outbreak (introduced by UN peacekeepers) -- 10,000+ deaths"
      - "Displacement camps with inadequate sanitation for 18+ months"
    management_evaluation:
      - "No earthquake monitoring system was in place before the event"
      - "Immediate international response was hampered by damage to the port and airport"
      - "Long-term reconstruction was slow -- political instability and corruption"

  - name: "Japan Earthquake and Tsunami 2011"
    date: "11 March 2011"
    type: "earthquake + tsunami"
    magnitude: 9.0
    focus_depth: "32km"
    location: "Tohoku Region, Japan"
    development_context: "HIC"
    key_facts:
      - "15,899 deaths (most from the 40m tsunami, not the earthquake shaking)"
      - "$235 billion economic damage (most expensive natural disaster in history)"
      - "Fukushima Daiichi nuclear disaster triggered by the tsunami"
      - "Japan's earthquake early warning system gave 8-30 seconds advance notice"
    primary_effects:
      - "Tsunami destroyed entire coastal communities"
      - "Fukushima nuclear plant cooling failure led to meltdown and 160,000 evacuations"
    secondary_effects:
      - "Nuclear contamination zone -- some areas still uninhabitable"
      - "Economic disruption to global supply chains (Japan manufactures car parts, electronics)"
    management_evaluation:
      - "Earthquake-resistant buildings saved millions of lives -- most structures survived the shaking"
      - "Tsunami seawalls at Tohoku were designed for 10m waves; the tsunami reached 40m"
      - "Evacuation procedures worked in most areas but not all -- some communities ignored warnings"
      - "Fukushima showed that even HIC preparation has limits -- the nuclear plant was not designed for a 9.0+ event"
```

This data structure already exists in the per-subject ontology architecture -- HistoryStudy nodes have `primary_sources` and GeoStudy nodes have `data_sources`. Adding a `case_studies` array with structured data would be the natural extension.

### 2. Lesson Structure -- A 10-Lesson Sequence With Exam Focus

For GCSE, lesson sequencing is not optional. The content builds cumulatively and the exam board expects knowledge to be applied in specific ways. A 10-lesson structure needs to be surfaced either from a VehicleTemplate or as a `lesson_sequence` property on the GeoStudy node:

| Lesson | Focus | Key Concept | Exam Skill |
|--------|-------|-------------|------------|
| 1 | Plate tectonics theory | Convection, boundary types | AO1: Describe processes |
| 2 | Constructive and conservative boundaries | Plate movement mechanisms | AO1: Explain with detail |
| 3 | Destructive boundaries and subduction | Volcanic and seismic processes | AO1: Use specialist vocabulary |
| 4 | Haiti 2010 -- LIC earthquake case study | Primary/secondary effects, vulnerability | AO2: Apply to named example |
| 5 | Japan 2011 -- HIC earthquake + tsunami | Effects, response, Fukushima | AO2: Apply to named example |
| 6 | Comparative analysis: Haiti vs Japan | Differential impacts, development | AO3: Compare and evaluate |
| 7 | Volcanic hazards: Montserrat or Eyjafjallajokull | Volcanic processes, impacts | AO2: Apply to named example |
| 8 | Management: monitoring, prediction, protection | Warning systems, building design | AO1/AO2: Describe and apply |
| 9 | Evaluation of management strategies | Assess effectiveness in HIC vs LIC | AO3: Evaluate with evidence |
| 10 | Exam technique and timed practice | Command words, mark scheme | All AOs: Exam practice |

This level of planning guidance does not need to be prescriptive -- a teacher should be free to reorder or adapt. But a suggested sequence demonstrates curricular logic and saves planning time.

### 3. Command Word and Mark Scheme Alignment

GCSE Geography assessment is structured around command words that students must understand and respond to correctly. Each command word implies a specific response structure:

| Command Word | Meaning | Marks | Required Response Structure |
|---|---|---|---|
| Describe | Say what you see / state facts | 2-4 | Factual statements with specific detail |
| Explain | Give reasons why | 4-6 | Because... this leads to... which means... |
| Compare | Identify similarities AND differences | 4-6 | Both... however... whereas... |
| Assess | Weigh up and make a judgement | 6-9 | Evidence for... evidence against... on balance... |
| Evaluate | Judge the success/effectiveness | 6-9 | To what extent... strengths... limitations... overall... |
| "To what extent" | Evaluate with a final judgement | 9 | Multiple perspectives + weighing + concluding judgement |

This data could sit on the GeoStudy node as an `exam_skills` property or on a separate ExamFramework node linked to KS4 subjects. The planner already uses correct mark allocations in its differentiation tables (4 marks, 9 marks), but without the command word framework, a teacher would not know how to teach students to structure their responses.

### 4. Vocabulary Definitions -- Precise GCSE Terminology

The 10 vocabulary terms are well-chosen but have empty definitions. For GCSE, precision matters. Here are the definitions the planner should provide:

| Term | GCSE-precise definition |
|---|---|
| plate boundary | The point where two tectonic plates meet; classified as constructive (diverging), destructive (converging), or conservative (sliding past) |
| subduction | The process where a denser oceanic plate is forced beneath a less dense continental plate at a destructive boundary, creating deep ocean trenches and volcanic arcs |
| convection current | Circular movements of semi-molten rock in the mantle, driven by heat from the core; the driving force behind plate movement |
| focus | The point within the Earth's crust where an earthquake originates; the deeper the focus, the wider the area affected but generally the less intense the shaking at the surface |
| epicentre | The point on the Earth's surface directly above the focus; the place where shaking is usually most intense |
| magnitude | The measure of energy released by an earthquake, measured on the moment magnitude scale (MMS); each whole number increase represents approximately 32 times more energy |
| seismometer | An instrument that detects and records seismic waves; used for earthquake monitoring and as part of early warning systems |
| pyroclastic flow | A fast-moving current of hot gas and volcanic matter (up to 700 degrees C, moving at up to 200 km/h) that flows down the side of a volcano; the most dangerous volcanic hazard |
| lahar | A destructive mudflow of volcanic debris and water, often triggered by rainfall mixing with ash deposits; can occur during or long after an eruption |
| primary vs secondary hazard | Primary hazards are caused directly by the tectonic event (ground shaking, lava flow). Secondary hazards are triggered as a consequence (tsunami, landslide, fire, disease) |

These definitions need to be stored as a `vocabulary_definitions` property or populated in the vocabulary word mat. For GCSE revision, students memorise key term definitions -- an empty word mat is a missed opportunity.

### 5. Data Removal: Arctic Location and Climate Change Concept

The planner includes "Arctic" as a location and "Climate Change" as a secondary concept. Both should be removed or replaced.

**Arctic** is not a tectonic hazard location. There is some seismic activity along the Mid-Atlantic Ridge near Iceland, but "Arctic" does not feature in any GCSE tectonic hazards specification. It appears to have been pulled from a different GeoStudy node (possibly a climate change or polar environments topic). Replace with a volcanic hazard location: Montserrat (Soufriere Hills, 1997 -- excellent for management evaluation) or Eyjafjallajokull (2010 -- excellent for secondary effects on air travel and global systems).

**Climate Change** as a secondary concept is misleading. Climate change does not cause earthquakes or volcanic eruptions. Including it risks reinforcing a common student misconception. The Development Gap concept is correctly included because differential vulnerability is central to the topic. Climate Change should be replaced with a more relevant secondary concept -- either UK Physical Landscapes (for context on plate boundaries affecting the UK, e.g., why the UK has minimal seismic risk) or Global Atmospheric Circulation (which helps explain why some tectonic regions also experience secondary hazards from weather systems).

---

## What the Auto-Generator Does Well

### 1. GCSE-Calibrated Differentiation
The four-level differentiation with exam-style tasks and correct mark allocations is the standout feature. "Explain why the Haiti earthquake caused more deaths than the Japan earthquake (4 marks)" is a question I could put directly on a mock exam paper. The common errors at each level ("Attributing the difference in deaths solely to magnitude") are the exact errors I mark in student work. This is DifficultyLevel-quality data generated from the GeoStudy node.

### 2. Teaching Guidance Aligned to Exam Requirements
"The key analytical skill at GCSE is explaining differential impacts" -- this single sentence tells a teacher where to focus their teaching. The hazard management cycle framework (prevention, preparation, response, recovery) structures teaching around the exam mark scheme. This is not generic curriculum guidance; it is exam-board-aware pedagogical advice.

### 3. Pitfalls as Exam Error Prevention
All three pitfalls target specific mark-losing behaviours: describing without explaining, listing without analysing, conflating earthquake and volcanic management. These are based on examiner report patterns. They are the most useful section for an NQT who has not yet seen enough student work to identify common errors.

### 4. Sensitive Content Awareness
"Avoid sensationalising death tolls -- analyse them as data points that reveal vulnerability patterns" is sophisticated pedagogical advice that many experienced teachers still need to hear. Treating disaster statistics with analytical respect, not emotional manipulation, is both ethically correct and better exam preparation (students who describe emotionally rather than analytically lose marks).

### 5. Assessment Guidance
"Can pupils explain plate boundary processes? Can they compare impacts in HIC and LIC/NEE? Can they evaluate management strategies?" Three questions that map directly to AO1, AO2, and AO3. This is a usable mid-unit assessment framework.

---

## What the Auto-Generator Gets Wrong

### 1. Empty Case Study Locations
Listing "Port-au-Prince" and "Tohoku Region" with no data is worse than not listing them at all. It implies the system knows these are the right case studies but has nothing to say about them. For GCSE, case study detail IS the content. A tectonic hazards planner without case study facts is like a recipe without ingredients.

### 2. Arctic as a Tectonic Hazard Location
This is a factual error. The Arctic is not on any exam specification for tectonic hazards. Including it undermines confidence in the rest of the planner's content accuracy. Data quality checks on GeoStudy location lists should flag locations that do not match the study theme.

### 3. Climate Change as a Secondary Concept
Including Climate Change risks reinforcing the misconception that climate change causes tectonic hazards. The secondary concepts should be limited to those that are genuinely integrated with the primary topic (Development Gap -- yes; Map Skills -- yes; Statistical Skills -- yes; Climate Change -- no).

### 4. Source Document Error
"Citizenship (KS3/KS4) - National Curriculum Programme of Study" as the source for a GCSE Geography tectonic hazards planner is a data join error. The correct source is the DfE GCSE Geography subject content (2014) and/or the relevant exam board specification.

### 5. No Lesson Structure for a 10-Lesson Unit
Ten lessons is substantial. Without a suggested sequence, a teacher must construct the entire scheme of work from the concept descriptions. For experienced teachers, this is manageable. For NQTs or teachers new to the specification, it is a significant planning burden that the system should reduce.

---

## Comparison: Hand-Written vs Auto-Generated Planner

Planning a 10-lesson GCSE tectonic hazards unit from scratch:
1. Review exam board specification and past papers for topic boundaries (30 minutes)
2. Research and compile case study data -- Haiti, Japan, volcanic case study (45 minutes)
3. Design 10-lesson sequence with progressive skill development (45 minutes)
4. Create differentiated resources for each lesson (60 minutes)
5. Write assessment tasks aligned to command words and mark allocations (30 minutes)
6. Source maps, data, photographs, and video resources (30 minutes)
7. Create vocabulary resources and revision materials (20 minutes)
8. Write the scheme of work document (30 minutes)

Total: approximately 4 hours 50 minutes.

With the auto-generated planner, I save the specification review (step 1 -- the statutory reference and assessment guidance cover this), the differentiation design (step 4 -- the four-level tables are directly usable), the command word alignment (step 5 partially -- the example tasks already use correct mark allocations), and the pitfall identification (already done). I still need case study research (step 2), lesson sequencing (step 3), resource sourcing (step 6), and vocabulary definitions (step 7).

Time saving: approximately 2 hours. The planner reduces preparation from about 5 hours to about 3 hours, a saving of roughly 40%.

This is a better time saving than the KS2 Geography experience in V7 (where the saving was perhaps 20-25%) because the GCSE planner provides exam-calibrated differentiation and teaching guidance that would otherwise require significant exam board research. The differentiation tables alone save 45-60 minutes of planning because they provide assessment-aligned task descriptors at four levels.

---

## Verdict

This is the most complete of the three V8 planners I am aware of being reviewed. The per-subject ontology demonstrates its value most clearly here: the GeoStudy node provides GCSE-specific content (scale, themes, map types, data sources, locations, contrasting localities, assessment guidance) that the generic ConceptCluster layer could never provide.

The score of 7.0/10 represents a 2-point improvement over my V7 KS2 experience (5.0/10). The improvement comes from:
- GCSE-calibrated differentiation (+1.0) -- four levels with exam-style tasks and mark allocations
- Exam-focused teaching guidance (+0.5) -- differential impacts framing, management cycle structure
- Practical pitfalls and sensitive content (+0.5) -- directly address common exam errors

The remaining 3 points are lost to:
- Empty case study data (-1.0) -- the most critical gap for GCSE
- No lesson structure (-0.5) -- a 10-lesson unit needs sequencing
- Empty vocabulary definitions (-0.5) -- precise terminology is assessed at GCSE
- Data quality errors (-0.5) -- Arctic location, Climate Change concept, source document bug
- Missing exam technique framework (-0.5) -- command words, mark scheme structure

The path to 9/10:
1. Populate case study data with specific facts, dates, figures (+1.0)
2. Add a suggested 10-lesson sequence (+0.5)
3. Add command word and mark scheme framework (+0.5)
4. Populate vocabulary definitions (+0.5)
5. Fix data errors (remove Arctic, reconsider Climate Change, fix source document) (+0.5)

Items 1-2 require new data authoring on GeoStudy nodes. Item 3 could be a shared KS4 Geography resource linked to all GeoStudy nodes. Items 4-5 are data quality fixes.

The fundamental architecture is right. The per-subject ontology provides the right kind of subject-specific data for GCSE planning. The gap is in depth and accuracy of content, not in structure. Fill the empty fields, fix the data errors, and add lesson sequencing, and these planners become genuinely exam-ready.
