# KS3 Biology — Graph v5 Evaluation

**Reviewer:** Kwame Osei
**Role:** KS3 Science Teacher (Biology specialist), 8 years' experience, Birmingham secondary school
**Previous review:** v4 (2026-02-22) — rated content 7/10, practical lesson generation 4/10, assessment 6/10
**Scope:** KS3 Biology domains (D002-D005) + Content Vehicles (CV001, CV004, CV006) + Thinking Lenses + Concept-Skill Links
**Date:** 2026-02-23

---

## 1. What Has Improved Since v4

### 1.1 Content Vehicles: Science Investigations as Structured Data

This was my single biggest criticism in v4: "No Practical Work Layer... The graph cannot generate practical lessons in any usable form." The Content Vehicle layer directly addresses this.

**What now exists:** 8 KS3 Science Content Vehicles with structured properties:
- `enquiry_type` (observation, fair_test, pattern_seeking)
- `variables_independent`, `variables_dependent`, `variables_controlled`
- `equipment` (specific lists)
- `recording_format` (step-by-step data recording progression)
- `safety_notes`
- `expected_outcome`
- `assessment_guidance` and `success_criteria`
- `definitions` (key vocabulary)

This is a fundamental improvement. For the first time, the graph contains enough structured data to generate a practical lesson that a teacher could walk into a lab and deliver. The equipment lists mean I can write a technician request. The safety notes mean I have a starting point for a risk assessment. The variables mean I can scaffold pupil investigation planning. The success criteria mean I can assess the practical.

**Impact on my v4 ratings:**
- Practical lesson generation: **4/10 -> 7/10**
- The improvement is substantial but not yet 8/10 or above because of the issues detailed in section 4.

### 1.2 Thinking Lenses: Crosscutting Concepts Realised

In v4, I wrote: "Adding Crosscutting Concepts — borrow from NGSS: Pattern, Cause/Effect, Scale, Systems, Energy/Matter, Structure/Function, Stability/Change — would dramatically improve the graph's ability to generate higher-order thinking questions."

The Thinking Lenses layer does exactly this. The 10 lenses are:
1. Patterns
2. Cause and Effect
3. Scale, Proportion and Quantity
4. Systems and System Models
5. Energy and Matter
6. Structure and Function
7. Stability and Change
8. Continuity and Change Over Time
9. Perspective and Interpretation
10. Evidence and Argument

The first seven map directly to the NGSS Crosscutting Concepts. Lenses 8-10 are UK-specific additions for humanities. This is well-designed — they took the NGSS frame and extended it for the UK context.

**What makes this useful in practice:**
- Each cluster has a primary lens and a secondary lens. When I planned the Cells unit, the primary lens "Structure and Function" gave every lesson a cognitive through-line. Pupils were not just learning facts about cells — they were repeatedly asking "How does the structure of this thing enable what it does?"
- The `agent_prompt` on each lens is directly usable. I could see an AI tutor using "Why is it shaped like that? What would happen if this part were different?" as prompts during a cell structure activity.
- The `rationale` on each APPLIES_LENS relationship explains WHY the lens fits the cluster. This is not a generic tagging — it is cluster-specific reasoning.

**My one criticism:** The lens assignments for the later Biology clusters (CL004-CL008 in D002) become somewhat repetitive. CL004 through CL008 all get "Cause and Effect" as primary or "Systems and System Models" as primary. This is not wrong — both are valid for organ systems and ecology. But the dominance of two lenses across five clusters suggests either that the lens set needs more biology-specific options or that the assignment algorithm is defaulting to safe choices. I would expect CL005 (nutrition) to get "Energy and Matter" as a strong candidate, not just Structure and Function.

### 1.3 Concept-Level DEVELOPS_SKILL Links

In v4, I wrote: "Working Scientifically Is Listed but Not Integrated... Create DEVELOPS_SKILL relationships from specific Concept nodes to WorkingScientifically nodes."

This has been done. The science concept-skill links file contains 34 curated links, including:

| Concept | Skill | Enquiry Type | My Assessment |
|---------|-------|-------------|---------------|
| SC-KS3-C040 (Enzymes) | WS-KS3-003 (Controlled experiments) | fair_test | Correct. Classic enzyme temperature investigation. |
| SC-KS3-C040 (Enzymes) | WS-KS3-005 (Tables and graphs) | fair_test | Correct. Continuous IV requires line graph. |
| SC-KS3-C064 (Variation) | WS-KS3-006 (Interpreting data) | pattern_seeking | Correct. Histogram analysis of continuous variation. |
| SC-KS3-C064 (Variation) | WS-KS3-011 (Statistical analysis) | pattern_seeking | Correct. Mean, range, frequency diagrams. |
| SC-KS3-C063 (DNA history) | WS-KS3-009 (Evaluating evidence) | secondary_research | Correct. Watson/Crick/Franklin — evaluating scientific evidence. |
| SC-KS3-C078 (Diffusion in chem) | WS-KS3-003 (Controlled experiments) | fair_test | Correct. Diffusion rate vs temperature. |
| SC-KS3-C075 (Conservation of mass) | WS-KS3-003 (Controlled experiments) | fair_test | Correct. Sealed vs open container. |
| SC-KS3-C075 (Conservation of mass) | WS-KS3-004 (Accurate measurement) | fair_test | Correct. Precise mass measurement, systematic error. |
| SC-KS3-C084 (Acids) | WS-KS3-012 (Risk assessment) | fair_test | Correct. Corrosive substances, eye protection. |

Every link I checked is accurate. The rationale on each link explains the specific practical and why the skill applies. The enquiry_type tags (fair_test, observation, pattern_seeking, secondary_research, classifying) are correctly assigned. This is exactly what I asked for.

**Coverage:** 34 links total (16 KS2, 18 KS3). For KS3, the links cover enzymes, diffusion, forces (Hooke's Law), motion (distance-time graphs), heating curves, climate data, variation, DNA history, conservation of mass, acids, forces, and catalysts. This is a solid initial set. It does not cover every concept that develops a WS skill, but it covers the most important ones.

**What is still missing:** No concept-skill links for KS3 Biology topics that I specifically highlighted:
- SC-KS3-C030 (Diffusion) should link to WS-KS3-003 and WS-KS3-005 — the potassium permanganate / agar cube investigation is a controlled experiment with graphable results
- SC-KS3-C051 (Photosynthesis) should link to WS-KS3-003 — the pondweed investigation is one of the most important fair tests in KS3 Biology
- SC-KS3-C065 (Natural selection) should link to WS-KS3-009 — evaluating evidence from fossils, comparative anatomy, antibiotic resistance
- SC-KS3-C057/C058 (Ecosystems/Food webs) should link to WS-KS3-002 and WS-KS3-005 — quadrat sampling and data presentation

These are biology-specific gaps. The 18 KS3 links are skewed towards Chemistry and Physics. I count 2 Biology-specific links (C040 enzymes and C063/C064 genetics), versus 7 Chemistry and 5 Physics. The remaining 4 are WS-general. Biology needs at least 8-10 more concept-skill links to reach parity.

---

## 2. Updated Ratings

| Aspect | v4 Rating | v5 Rating | Change | Notes |
|--------|-----------|-----------|--------|-------|
| Content accuracy | 9/10 | 9/10 | -- | Unchanged. Still excellent. |
| Teaching guidance | 8/10 | 8/10 | -- | Unchanged. Still reads like an experienced teacher. |
| Cross-domain connections | 8/10 | 8/10 | -- | Unchanged. CO_TEACHES still the standout feature. |
| Cluster sequencing | 7/10 | 7/10 | -- | Within domains: good. Between domains: still implicit. |
| Working Scientifically integration | 3/10 | 6/10 | +3 | Concept-skill links created. Coverage incomplete for Biology. |
| Practical work support | 2/10 | 7/10 | +5 | Content Vehicles with equipment, safety, variables, outcomes. Major improvement. |
| Assessment scaffolding | 4/10 | 5/10 | +1 | CV success criteria + assessment guidance help. Still no mark scheme templates. |
| NGSS comparison | 2/10 | 5/10 | +3 | Thinking Lenses implement crosscutting concepts. Alignment layer still empty. |
| KS2-KS3 transition | 3/10 | 3/10 | -- | No change. Still too few cross-KS prerequisite links. |
| Lesson generation potential | 7/10 | 8/10 | +1 | Thinking Lenses add cognitive framing to every cluster. |
| Test generation potential | 6/10 | 6/10 | -- | Misconceptions still the best diagnostic source. No new scaffolding. |
| Resource generation potential | 4/10 | 7/10 | +3 | Content Vehicles enable practical resource generation. |
| **Thinking Lenses (NEW)** | N/A | 8/10 | N/A | Strong implementation of crosscutting concepts. Minor repetition issues. |
| **Content Vehicle quality (NEW)** | N/A | 6/10 | N/A | Good structure. Several data errors. See section 4. |

**Overall: 6.5/10 -> 7.5/10**

The graph has made meaningful progress on the two areas I identified as critical: practical work and WS integration. The Thinking Lenses are a bonus I did not specifically request but which turned out to be the most pedagogically useful addition for planning. The graph is now usable for planning a biology unit with practicals, structured data recording, and cognitive framing. It is not yet usable for generating ready-to-deliver practical lessons (safety data needs more detail, equipment lists need validation), but it is much closer.

---

## 3. Remaining Gaps

### 3.1 No Risk Assessment Data

The Content Vehicles have `safety_notes` but these are brief single sentences. A real risk assessment for a KS3 microscopy practical needs:

| Hazard | Risk | Who is at risk | Control measure | CLEAPSS ref |
|--------|------|----------------|-----------------|-------------|
| Broken glass (slides, cover slips) | Cuts to skin | Pupils | Sharps bin on every bench. Report breakages. Do not pick up fragments. | GL058 |
| Iodine solution | Staining, minor irritation | Pupils | Wear lab coat. Wash spills immediately. | HC054a |
| Methylene blue | Staining | Pupils | Low hazard. Wash spills. | HC059 |
| Mounted needles | Puncture wounds | Pupils | Point away from body. Demonstrate safe handling. | n/a |
| Electrical equipment (microscope) | Electrical shock | Pupils | Dry hands. Do not touch plug with wet hands. | n/a |

The CV001 safety notes ("Handle glass slides carefully. Iodine stains skin and clothing. Cheek cell collection requires hygiene protocol. Do not taste stains.") cover the first two rows but miss the last three entirely. This is not good enough for a platform claiming to support practical science. CLEAPSS references are the industry standard and should be included.

**Recommendation:** Add `cleapss_references` property to Content Vehicles. Add `hazards` as a structured array with `hazard`, `risk_level`, `control_measure` properties. This is the minimum viable safety data for science practicals.

### 3.2 Biology Concept-Skill Links Are Thin

As detailed in section 1.3, the concept-skill links are heavily skewed towards Chemistry and Physics. KS3 Biology needs at minimum:
- C030 (Diffusion) -> WS-KS3-003 (fair test), WS-KS3-005 (tables/graphs)
- C051 (Photosynthesis) -> WS-KS3-003 (fair test, pondweed investigation)
- C057 (Ecosystems) -> WS-KS3-002 (observation, quadrat sampling), WS-KS3-005 (data presentation)
- C065 (Natural selection) -> WS-KS3-009 (evaluating evidence)
- C047 (Reproduction) -> WS-KS3-001 (scientific attitudes, sensitive topics)
- C054 (Respiration) -> WS-KS3-003 (fair test, germinating seeds in limewater)

### 3.3 KS2-KS3 Transition Still Weak

The only KS2->KS3 Biology prerequisite is SC-KS2-C012 (Plant Requirements) -> SC-KS3-C026 (Cell structure). In reality, pupils arrive at KS3 Biology with knowledge from:
- KS2 animals including humans (digestion, circulation, skeleton, teeth)
- KS2 living things and habitats (classification, food chains)
- KS2 evolution and inheritance (adaptation, fossils, Darwin)

None of these are captured as formal prerequisites. This means a Y7 Biology unit cannot automatically check what prior knowledge to expect.

### 3.4 No "Practical Type" Classification

CV001 is classified as "investigation" with enquiry_type "observation." But a cells practical is not one type of activity. It involves:
- Teacher demonstration (microscope setup)
- Guided practical (following a method)
- Independent practical (making own slides)
- Observation and recording
- Calculation

The Content Vehicle type system (investigation, topic_study, case_study, text_study, worked_example_set) is designed for History/Geography/English/Maths. Science needs finer granularity. A single Science investigation contains multiple practical activity types.

### 3.5 No Inter-Domain Teaching Sequence

The cluster SEQUENCED_AFTER chains work within each domain. But a KS3 Biology scheme of work teaches across domains. What order should a Biology teacher teach D002 (Structure and Function), D003 (Material Cycles), D004 (Interactions), and D005 (Genetics)?

The graph has no inter-domain sequencing. My v4 lesson plan handled this by following the biological narrative (cells -> organisms -> ecosystems -> evolution), but this was my professional knowledge, not data from the graph. An AI lesson planner would need this metadata to generate a full-year scheme of work.

---

## 4. Content Vehicle Quality Audit

### 4.1 SC-KS3-CV001 — Cell Structure and Microscopy

**Equipment list accuracy:**

| Equipment Item | Accurate? | Notes |
|----------------|-----------|-------|
| Light microscopes | Yes | Standard school equipment |
| Prepared slides (cheek cells, onion epidermis) | Partially | Onion epidermis: fine. Cheek cells: supplier-prepared slides are often poor quality. Fresh cells stained by pupils are better but require hygiene protocol. |
| Iodine stain | Yes | Standard. Stains starch/nuclei. |
| Methylene blue stain | Yes | Standard for animal cells. |
| Cover slips | Yes | Standard. |
| Glass slides | Yes | Standard. |
| Mounted needles | Yes | Standard for peeling epidermis. |

**Missing equipment:**
- Forceps/tweezers (for handling epidermis)
- Filter paper / paper towels (for blotting excess stain)
- Lens paper (for cleaning microscope lenses)
- Sharps bin (for broken glass — mandatory safety equipment)
- Lab coats or eye protection (for staining work)

**Verdict:** Equipment list is a reasonable starting point but incomplete. A teacher using ONLY this list would arrive in the lab missing at least three items needed for the practical to run smoothly.

**Safety notes accuracy:**
- "Handle glass slides carefully" — correct but vague. What does "carefully" mean to an 11-year-old? Specify: do not pick up broken glass, report breakages, use the sharps bin.
- "Iodine stains skin and clothing" — correct.
- "Cheek cell collection requires hygiene protocol" — correct to flag but provides no detail on what the protocol is. This should specify: do not share scrapers, use antiseptic mouthwash, dispose of swabs in biohazard bag.
- "Do not taste stains" — correct.
- **Missing:** mounted needle safety, hair near microscope, electrical safety (wet hands near power supply), broken glass protocol.

**Variables:**
- Listed as "N/A (observation enquiry)" — this is technically correct for a pure observation investigation. But the magnification calculation work and the comparison of plant vs animal cells introduce a structured comparison element that could be considered a categorical independent variable (cell type). This is a minor point.

**Expected outcome:** "Pupils observe cell structures under the microscope, distinguish plant and animal cells, and calculate magnification. Plant cells have cell wall, chloroplasts, and permanent vacuole; animal cells do not." — Correct and well-stated.

**Assessment/success criteria:** Well-written and directly assessable. These mapped precisely to what I assessed in L5.

**Overall CV001 rating: 7/10** — The structure is excellent. The content is accurate. The equipment list and safety notes need expanding to be genuinely classroom-ready.

### 4.2 SC-KS3-CV004 — Photosynthesis Investigation

**Equipment list accuracy:**

| Equipment Item | Accurate? | Notes |
|----------------|-----------|-------|
| Elodea (pondweed) | Yes | Standard. Must be fresh and actively photosynthesising. |
| Beaker | Yes | 250ml or larger. |
| Lamp | Yes | Desk lamp or bench lamp. Must be able to vary distance. |
| Ruler | Yes | For measuring lamp distance. |
| Stopwatch | Yes | Standard. |
| Sodium bicarbonate solution | Yes | Important — provides CO2 source, prevents CO2 becoming limiting factor. |
| Thermometer | Yes | For monitoring temperature (heat from lamp). |

**Missing equipment:**
- Scissors (to cut pondweed to equal lengths)
- Boiling tube or test tube (to hold pondweed upright in water — a beaker alone makes it hard to count bubbles)
- Funnel (inverted over pondweed to collect gas)
- Measuring cylinder (if collecting gas by displacement rather than counting bubbles)

**Variables accuracy:**
- Independent: "distance of lamp from pondweed (light intensity)" — correct, though note that light intensity is inversely proportional to distance squared, not distance. A common pupil error.
- Dependent: "number of oxygen bubbles per minute" — correct for a basic version. More advanced: volume of gas collected.
- Controlled: "same piece of pondweed, same temperature, same volume of water, same concentration of sodium bicarbonate" — correct and comprehensive.

**Safety notes:** "Lamp gets hot — do not touch. Ensure water does not contact electrical equipment. Wash hands after handling pondweed." — Correct. I would add: "Do not look directly at the lamp at close range."

**Expected outcome:** "As light intensity increases (lamp closer), rate of photosynthesis increases (more bubbles). At high light intensities, the rate levels off (limited by CO2 or temperature)." — Correct. The limiting factor plateau is an important teaching point and it is captured here.

**Overall CV004 rating: 7/10** — Accurate and well-structured. Equipment list needs boiling tube/funnel for standard setup.

### 4.3 SC-KS3-CV006 — Ecosystem Relationships

**Critical data error:** The `delivers_concept_ids` are wrong.

The vehicle is described as: "Fieldwork and research enquiry exploring food webs, interdependence, and the impact of environmental change on populations. Includes quadrat sampling."

But the concept IDs it claims to deliver are:
- SC-KS3-C053 (Leaf adaptations) — this is a photosynthesis concept from D003, NOT an ecology concept
- SC-KS3-C054 (Aerobic respiration) — D003 concept, NOT ecology
- SC-KS3-C055 (Anaerobic respiration) — D003 concept, NOT ecology
- SC-KS3-C056 (Comparing respiration types) — D003 concept, NOT ecology

**These are wrong.** A quadrat-sampling, food-web-building fieldwork investigation delivers ECOLOGY concepts from D004:
- SC-KS3-C057 (Ecosystem interdependence) — the core concept this vehicle teaches
- SC-KS3-C058 (Food webs) — constructed from fieldwork data
- SC-KS3-C059 (Pollination and food security) — could be addressed through pollinator observations
- SC-KS3-C060 (Environmental interactions) — comparing habitats is exactly this

The equipment, expected outcome, assessment guidance, and success criteria all describe an ecology investigation. The concept IDs are simply misassigned. This looks like an error in the JSON generation — perhaps the concept IDs for D003 and D004 were swapped during authoring.

**This must be fixed.** An AI system using the `delivers_concept_ids` to plan lessons would generate a fieldwork-based investigation on aerobic respiration, which makes no sense.

**Equipment list accuracy:**

| Equipment Item | Accurate? | Notes |
|----------------|-----------|-------|
| Quadrats | Yes | 0.5m x 0.5m standard. |
| Identification keys | Yes | Must be appropriate for school grounds species. |
| Tally counters | Yes | Or tally sheets. |
| Tape measures | Yes | For transect lines. |
| Light meters | Yes | Good for comparing abiotic factors. |
| Soil thermometers | Yes | Good for comparing abiotic factors. |

**Missing equipment:**
- Clipboards (essential for outdoor recording)
- Pooters or collection pots (for invertebrate sampling)
- Hand lenses (for field identification)
- Random number table or calculator (for random quadrat placement)
- Antibacterial gel/wipes (mandatory after outdoor work with soil)

**Safety notes:** "Outdoor fieldwork risk assessment required. Check for allergies. Wash hands after handling soil/organisms. Stay in designated areas." — These are correct and cover the main points. I would add: check the site for broken glass or other hazards before pupils arrive; ensure a first aid kit is accessible outdoors; pupils with asthma should carry inhalers.

**Overall CV006 rating: 4/10** — The vehicle structure is good, but the concept ID error is a fundamental data integrity problem. Fix the delivers_concept_ids and this becomes a 7/10.

### 4.4 SC-KS3-CV005 — Particle Model and Changes of State

**Same concept ID error pattern.** This vehicle describes a particle model investigation (heating/cooling curves, particle diagrams) but delivers:
- SC-KS3-C058 (Food webs) — D004 ecology concept
- SC-KS3-C059 (Pollination and food security) — D004 ecology concept
- SC-KS3-C060 (Environmental interactions) — D004 ecology concept
- SC-KS3-C061 (Heredity) — D005 genetics concept

**These are obviously wrong.** A particle model investigation delivers D006 concepts:
- SC-KS3-C068 (Particle model of matter)
- SC-KS3-C069 (States of matter)
- SC-KS3-C071 (Changes of state)

And the equipment (thermometers, beakers, ice, Bunsen burner, stearic acid) is clearly for a chemistry states-of-matter investigation, not an ecology investigation.

**This confirms a systematic concept ID mapping error** in the science_ks3.json file. The concept IDs appear to be shifted — CV005 has D004 concepts that should belong to CV006, and CV006 has D003 concepts that should belong elsewhere. An AI system consuming this data would produce nonsensical results.

### 4.5 SC-KS3-CV002 — Acids, Alkalis and Neutralisation

**Concept ID error again.** The vehicle describes an acids/alkalis investigation but delivers:
- SC-KS3-C065 (Natural selection) — D005 genetics
- SC-KS3-C066 (Adaptation and extinction) — D005 genetics
- SC-KS3-C067 (Biodiversity) — D005 genetics
- SC-KS3-C068 (Particle model of matter) — D006 chemistry particle model

The correct concept IDs for an acids vehicle should be:
- SC-KS3-C084 (Acids and alkalis)
- SC-KS3-C085 (pH scale)
- SC-KS3-C086 (Acid-metal reactions)
- SC-KS3-C087 (Neutralisation)

### 4.6 Summary of Concept ID Errors

| Vehicle | Description | Current concept IDs | Correct concept IDs |
|---------|------------|--------------------|--------------------|
| CV001 | Cell Structure and Microscopy | C026, C027, C028, C029 | **CORRECT** |
| CV002 | Acids, Alkalis, Neutralisation | C065, C066, C067, C068 | C084, C085, C086, C087 |
| CV003 | Forces and Motion | C088, C089, C090, C091 | Needs checking (C088=catalysts, not forces). Likely C119-C124 range. |
| CV004 | Photosynthesis Investigation | C042, C046 | **CORRECT** |
| CV005 | Particle Model | C058, C059, C060, C061 | C068, C069, C071 (and possibly C070) |
| CV006 | Ecosystem Relationships | C053, C054, C055, C056 | C057, C058, C059, C060 |
| CV007 | Energy Transfers | C083, C084, C085, C086 | Needs checking. C083=types of reactions, not energy. Likely C107-C114 range. |
| CV008 | Chemical Reactions: Metals | C069, C070, C071 | Needs checking. C069=states of matter, not metals. Likely C086, C093-C096 range. |

**Only CV001 and CV004 have correct concept IDs.** 6 of 8 vehicles have misassigned concept IDs. This is a serious data quality issue. The descriptions, equipment, safety notes, expected outcomes, and assessment criteria are all correct for the named investigation — but they are linked to the wrong concepts.

**Root cause hypothesis:** The concept IDs were assigned sequentially or by offset rather than by matching the vehicle description to the correct concepts in each domain. CV001 (cells) and CV004 (photosynthesis) are correct because they were probably authored first and checked. The remaining 6 appear to have ID ranges shifted by one or two domains.

---

## 5. Recommendations (Priority Order)

### 5.1 CRITICAL: Fix Content Vehicle Concept ID Mappings

Six of eight KS3 Science Content Vehicles have wrong `delivers_concept_ids`. This is a data integrity error that would cause any AI system consuming the graph to generate nonsensical lesson plans. Fix the JSON source file (`layers/content-vehicles/data/science_ks3.json`) and re-import.

### 5.2 HIGH: Add CLEAPSS References and Structured Hazard Data

Add a `hazards` array to each Science Content Vehicle with structured properties: `hazard`, `risk_level` (low/medium/high), `control_measure`, `cleapss_ref`. This is the minimum viable safety data for UK school science. Without CLEAPSS references, the platform cannot claim to support practical science teaching to the standard expected by UK school leadership and inspectors.

### 5.3 HIGH: Expand Biology Concept-Skill Links

Add at least 8 more Biology-specific DEVELOPS_SKILL links covering diffusion (C030), photosynthesis (C051), ecosystems (C057/C058), natural selection (C065), reproduction (C047), and respiration (C054). The current 34 links are heavily skewed towards Chemistry and Physics.

### 5.4 MEDIUM: Complete Equipment Lists

Every Content Vehicle equipment list should include ALL items needed to run the practical, including support items (filter paper, sharps bins, hand lenses, clipboards, antibacterial gel) that are often forgotten. A teacher printing the equipment list for a technician request should not need to add items from memory.

### 5.5 MEDIUM: Add Inter-Domain Sequencing Metadata

Add explicit sequencing between Biology domains: D002 (Structure and Function) -> D003 (Material Cycles) -> D004 (Interactions) -> D005 (Genetics and Evolution). This mirrors the biological narrative (cells -> organisms -> ecosystems -> evolution) and would enable a full-year scheme-of-work generator.

### 5.6 MEDIUM: Expand KS2-KS3 Prerequisites for Biology

Add prerequisites from KS2 animals including humans, KS2 living things and habitats, and KS2 evolution and inheritance into the relevant KS3 Biology domains. Y7 teachers need this data to plan transition units and diagnostic assessments.

### 5.7 LOW: Add "Practical Type" Sub-Classification for Science

Science Content Vehicles need a finer classification than "investigation." A cells investigation includes teacher demonstrations, guided practicals, independent practicals, observations, and calculations. Consider a `practical_components` array listing the activity types within each vehicle.

### 5.8 LOW: Improve Thinking Lens Variety in Biology Clusters

Review the lens assignments for Biology D002 CL004-CL008 to reduce over-reliance on "Cause and Effect" and "Systems and System Models." Consider "Energy and Matter" for nutrition/respiration clusters and "Scale, Proportion and Quantity" for cell size/magnification clusters.

---

## 6. What I Would Tell the Development Team

The Content Vehicle layer and the Thinking Lenses together represent the most significant improvement to Science support since the graph was first built. For the first time, I can plan a unit with structured practical data AND a cognitive framework, rather than filling in both from my own experience.

The concept ID errors in the Content Vehicles are a significant problem, but they are a DATA error, not a DESIGN error. The design is right — vehicles with enquiry types, variables, equipment, safety, outcomes, and success criteria is exactly what Science teachers need. Fix the data and the system becomes genuinely useful.

If I had to prioritise one thing: fix the concept IDs in science_ks3.json. Everything else is incremental improvement. Wrong concept mappings fundamentally break any downstream system that uses them.

If I had two priorities: fix the concept IDs and add CLEAPSS references. In UK schools, if an AI system generates a practical lesson that omits a standard safety control, the platform owner is liable. CLEAPSS is the accepted authority. Reference it.

---

## 7. Comparison to v4 Findings

| v4 Recommendation | Status in v5 | Assessment |
|-------------------|-------------|------------|
| 1. Integrate Working Scientifically | Done (34 concept-skill links) | Addressed. Biology coverage needs expansion. |
| 2. Add a Practical Work layer | Done (Content Vehicles) | Addressed. Data quality issues (concept IDs, safety detail). |
| 3. Add Crosscutting Concepts | Done (Thinking Lenses) | Exceeds expectations. 10 lenses with AI prompts. |
| 4. Complete NGSS alignment | Not done | Alignment layer still empty. Lenses are a workaround, not a fix. |
| 5. Add assessment scaffolding | Partially done (CV success criteria) | Success criteria and assessment guidance in CVs. No mark scheme templates. |
| 6. Strengthen KS2-KS3 links | Not done | Still only one Biology prerequisite link across key stages. |
| 7. Resolve D006/D015 overlap | Not done | Still two domains covering particle model. No explicit guidance. |
| 8. Add narrative arc metadata | Not done | No BigIdea or Narrative node type. Inter-domain sequencing still missing. |

**Score: 3 of 8 recommendations fully addressed, 1 partially addressed, 4 not addressed.**

The three that were addressed (WS integration, practicals, crosscutting concepts) were the three I rated as highest priority. The development team read the feedback and acted on the right things. The remaining 4 are lower priority and can wait for the next iteration.

---

## 8. Final Verdict

**v4 verdict:** "The graph knows WHAT to teach in KS3 Science. It does not yet know HOW to teach it as science."

**v5 verdict:** The graph now knows what to teach AND has the structural scaffolding for how to teach it practically. Content Vehicles provide the practical framework. Thinking Lenses provide the cognitive framework. Concept-skill links begin (but do not complete) the Working Scientifically integration. The gap between "content knowledge graph" and "teaching resource platform" has narrowed significantly. The remaining barriers are data quality (concept ID errors, incomplete safety data, thin Biology skill links) rather than structural design problems. Fix the data and this becomes a 8/10 platform for KS3 Science.
