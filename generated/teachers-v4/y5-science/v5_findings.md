# V5 Findings -- Mrs Priya Kapoor, Y5 Science

**Date:** 23 February 2026
**Teacher:** Mrs Priya Kapoor, 10 years' experience, Science Coordinator
**School:** Primary, Leicester
**Domains evaluated:** Light (SC-KS2-D005), Forces and Magnets (SC-KS2-D006)
**New layers evaluated:** Content Vehicles (SC-KS2-CV007, SC-KS2-CV001), Thinking Lenses
**Previous review:** v4 findings (22 February 2026, under Mr Raj Kapoor -- same school, shared review)
**Method:** Planned and taught a 2-week, 10-lesson unit using Content Vehicles and Thinking Lenses. Teaching log covers Week 1 (Light, 5 lessons).

---

## 1. What Has Improved Since V4

The v4 review concluded: "The graph is a strong conceptual framework that does not yet understand practical science." The v4 overall verdict was 7.5/10 for content generation, **4/10 for investigation generation**, 5/10 for assessment generation, 6/10 for teaching resource generation.

Two new layers have been added since v4:

### 1a. Content Vehicles -- addressing the investigation gap

The v4 review's most critical finding was: "KS2 science is built around five enquiry types. The graph does not model these." The v4 report listed 10 things an AI would need to generate a fair test investigation and noted the graph could provide only 3 of them (#1 scientific question, #9 expected pattern, fragments of #5 equipment).

**Content Vehicles now provide 9 of those 10:**

| V4 requirement | V4 status | V5 status (Content Vehicles) |
|----------------|-----------|------------------------------|
| 1. Scientific question | Partial (from concept description) | Yes -- vehicle description frames the question |
| 2. Independent variable | Missing | **Yes** -- `variables_independent` field |
| 3. Dependent variable | Missing | **Yes** -- `variables_dependent` field |
| 4. Control variables | Missing | **Yes** -- `variables_controlled` array |
| 5. Equipment list | Fragments in prose | **Yes** -- `equipment` array (structured) |
| 6. Method steps | Missing | Partial -- implied by vehicle description, not step-by-step |
| 7. Recording format | Missing | **Yes** -- `recording_format` field |
| 8. Graph type | Missing | Implicit in recording format (line graph, bar chart) |
| 9. Expected pattern/outcome | Partial (in teaching guidance) | **Yes** -- `expected_outcome` field |
| 10. Risk assessment | Missing | **Partial** -- `safety_notes` field, but minimal |

This is a major improvement. The v4 complaint that "the graph can generate steps 1, 2, 8 of a lesson (the conceptual bookends) but not steps 3-7, 9 (the actual science)" is substantially addressed. An AI using CV007 can now generate a structured investigation with variables, equipment, recording format, and expected outcome.

### 1b. Thinking Lenses -- addressing the crosscutting concept gap

The v4 review specifically recommended: "Even without formal NGSS alignment, adding a 'crosscutting concept' tag to UK concepts would be transformative." The v4 report mapped NGSS crosscutting concepts to UK KS2 science and noted this was "the third question the graph doesn't answer at all."

Thinking Lenses now provide this. The 10 lenses are adapted from NGSS CCCs plus UK-specific frames:
- Patterns, Cause and Effect, Scale/Proportion/Quantity, Systems and System Models, Energy and Matter, Structure and Function, Stability and Change (NGSS CCCs)
- Continuity and Change, Perspective and Interpretation, Evidence and Argument (UK-adapted additions)

Each cluster has a primary and secondary lens with:
- A key question (displayed to pupils)
- An AI instruction (for content generation)
- A per-cluster rationale explaining why this lens fits this cluster

In practice, the Cause and Effect lens was highly effective as a lesson-framing tool. Pupils internalised the "what caused this?" question within 2 days. The Patterns lens worked well for consolidation and reflection. The lens key questions gave me a ready-made pedagogical language that transferred consistently across lessons.

### 1c. Other v4 recommendations -- status

| V4 recommendation | Priority | V5 status |
|-------------------|----------|-----------|
| Add `nc_year` to all concepts | Must-have | **Not addressed** -- still "KS2, Age 7-11" without year group |
| Fix context to include D013 (Forces Y5) | Must-have (bug) | **Not addressed** -- D013 still absent from my context |
| Add investigation/enquiry metadata | Must-have | **Addressed via Content Vehicles** |
| Link WS skills to concepts/clusters | Should-have | **Partially addressed** -- Disciplinary Skills per Concept section now in context (C022 -> WS-KS2-002, C067 -> WS-KS2-003, C027 -> WS-KS2-003/005). Only 5 concepts across Light and Forces have links. |
| Add CO_TEACHES strength | Should-have | **Not addressed** |
| Add crosscutting concept tags | Should-have | **Addressed via Thinking Lenses** |
| Add science assessment framework | Should-have | **Not addressed** |
| Add equipment lists as structured data | Nice-to-have | **Addressed via Content Vehicles** |
| Add risk assessment references | Nice-to-have | **Partially addressed** -- safety_notes field exists but minimal |
| Add cross-subject links | Nice-to-have | **Addressed** -- Cross-Domain CO_TEACHES now present (C067 <-> MA-Y5-C015, C027 <-> MA-Y3-C015) |

**5 of 10 v4 recommendations addressed. 2 partially addressed. 3 not addressed.**

The 3 unaddressed recommendations include the two marked "must-have" in v4: `nc_year` and D013 context inclusion. These remain critical.

---

## 2. Updated Rating

| Category | V4 rating | V5 rating | Change |
|----------|-----------|-----------|--------|
| Content generation (explanations, vocabulary, misconceptions) | 7.5/10 | 8/10 | +0.5 -- Thinking Lenses add coherent framing; cross-domain links improve context |
| Investigation generation | 4/10 | **7/10** | **+3** -- Content Vehicles provide variables, equipment, recording format, expected outcomes |
| Assessment generation | 5/10 | 6.5/10 | +1.5 -- CV success criteria provide assessment checklist; misconceptions still the strongest feature |
| Teaching resource generation | 6/10 | 7/10 | +1 -- structured equipment lists, Thinking Lens display questions, and vocabulary definitions |

**Overall: 7/10 (up from 5.75/10 weighted average in v4)**

The investigation generation improvement from 4/10 to 7/10 is the headline change. Content Vehicles transform the graph from "a conceptual framework that does not understand practical science" to "a practical science planning tool with some gaps." It is no longer accurate to say the graph cannot generate a science investigation. It can -- with caveats.

---

## 3. Remaining Gaps

### 3a. Critical gaps (block quality for AI-generated content)

**1. `nc_year` still missing.**
This was the #1 must-have in v4. Every concept is still "KS2, Age 7-11." For my Light unit:
- C022, C023, C024 are Y3 content. For Y5, these are retrieval.
- C067 is Y6 content. For Y5, this is preview/new learning.

Without `nc_year`, an AI would give equal teaching weight to all four concepts. In practice, I compressed C022/C023/C024 into starter activities (5-10 min each) and gave C067 two full lessons. This professional judgement cannot be replicated by an AI without year-group attribution.

**The data already exists.** Every concept description says "In Year 3, this is..." or "In Year 6, it is explained using..." The extraction JSON has `"year": [5]` on every concept. This property is present in the source data but not surfaced in the graph or in the context output.

**2. D013 (Forces Y5) still missing from context.**
The graph contains SC-KS2-D013 (Forces) with 3 concepts (C055 Gravity, C056 Resistance Forces, C057 Mechanisms), 3 objectives (O068-O070), 2 clusters, and cluster definitions with Thinking Lenses. This is genuine Y5 content. My context included D006 (Forces and Magnets, Y3) but not D013. When I teach Y5 Forces next half-term, I will need D013. An AI planning "Y5 Science: Forces" would miss the entire Y5 forces domain.

Furthermore, D013 has no Content Vehicle. There are 10 vehicles in science_ks2.json and none delivers C055, C056, or C057. This means even if D013 were in the context, there would be no investigation structure for the most investigation-rich Y5 science domain (gravity drop tests, parachute investigations, lever/pulley practicals).

**3. Step-by-step method not in Content Vehicles.**
CV007 and CV001 provide variables, equipment, and recording format -- but not the method steps. For the shadow investigation (CV007), the method is implied: set up torch, place object at distances, measure shadow, record, repeat. An experienced teacher fills this in. But the v4 complaint was specifically about AI and NQT support. Method steps (numbered, sequential, actionable) would close this gap.

### 3b. Significant gaps (degrade quality)

**4. Safety notes are minimal and sometimes missing critical hazards.**

From my teaching log, specific safety issues encountered that are NOT in CV007:
- Darkened room trip hazards
- Battery compartment security on torches
- Reflected sunlight from mirrors into eyes
- Laser pointer safety (laser pointer not listed in CV007 at all despite being in C067 teaching guidance)
- Iron filings handling (mentioned in C026 teaching guidance but not in any Content Vehicle)

CV001 safety notes: "Low risk. Ensure ramp is stable and surfaces are secured flat." -- this is adequate for the friction investigation (genuinely low risk). But CV007's safety notes are inadequate for the range of activities the investigation involves.

**Recommendation:** Safety notes should be hazard-specific, not generic. Minimum per vehicle:
- Specific hazards identified (light in eyes, broken torch, trip hazard in dark, mirror reflection)
- Control measures for each hazard
- CLEAPSS reference where applicable (e.g., CLEAPSS L195 for laser use in schools)

**5. Thinking Lens rationales are duplicated across clusters.**

Both Light clusters (CL001 and CL002) have identical rationale text for the Cause and Effect lens: "Fair testing and investigations are designed to isolate variables and establish causal relationships -- the cognitive demand is reasoning from controlled evidence to causal claims."

This rationale fits CL001 (which is an investigation cluster) but not CL002 (which is an explanation/modelling cluster about straight-line light and reflection). CL002 should have a rationale like: "Understanding how light travels and reflects requires tracing causal chains -- light from source causes illumination, reflection causes us to see objects, blocking causes shadows."

The same duplication appears for the Patterns lens rationale across both clusters. Checking the context, this identical-rationale pattern appears in several domains: D006-CL001/CL002, D007-CL002/CL003, D012-CL001/CL002 all share identical text for their respective lenses. The per-cluster rationale was one of the claimed features of the Thinking Lens layer ("The rationale on each rel explains why the lens fits this specific cluster -- not just the topic name"). In practice, many rationales are topic-generic, not cluster-specific.

**6. Only 1 Content Vehicle per domain.**

Light has 1 vehicle (CV007). Forces and Magnets has 1 vehicle (CV001). The Content Vehicle layer documentation says "teachers choose between packs" (DELIVERS is many-to-many, vehicles deliver concepts, teachers choose). But there is no choice -- each domain has exactly one vehicle. For Light, you could reasonably offer:
- CV007a: Shadow investigation (fair test -- as currently)
- CV007b: Mirror and periscope challenge (pattern seeking)
- CV007c: How we see -- model building (research/secondary sources)

For Forces:
- CV001: Friction investigation (fair test -- as currently)
- A magnets investigation vehicle (identifying/classifying -- currently absent)

The architecture supports multiple vehicles per domain. The data does not yet populate this.

**7. Content Vehicle delivers concepts outside the domain.**

CV001 (Friction Investigation) delivers: SC-KS2-C002, SC-KS2-C003, SC-KS2-C005, SC-KS2-C025, SC-KS2-C027.

C002, C003, and C005 are from domain SC-KS2-D002 (Animals including Humans) and SC-KS2-D003 (Plants). These are not Forces concepts. This appears to be a data error -- the friction investigation does not deliver animal or plant concepts. It should deliver only C025 and C027 (and possibly C055/C056 from D013 if extended to Y5 forces).

### 3c. Minor gaps

**8. Recording format could specify graph type explicitly.**
CV007 says "results table -> line graph -> ray diagram." This is correct. CV001 says "table of results -> bar chart -> written conclusion." This is also correct. But the REASON for choosing line graph vs. bar chart (continuous vs. categorical independent variable) is not stated. For an AI or NQT, this reasoning matters.

**9. No time estimates on Content Vehicles.**
The v4 review noted that time allocations were correctly removed from clusters (teacher professional judgement is better). But Content Vehicles are different from clusters -- they describe practical activities with real-world time constraints. "Set up and test 5 surfaces x 3 repeats" takes 25 minutes minimum. "Results table -> line graph -> ray diagram" takes 2 lessons. A rough time estimate per vehicle would help AI planning.

**10. Thinking Lens key questions are not age-differentiated.**
The Cause and Effect key question is: "What caused this to happen, and how do we know?" This works for Y5. Would it work for Y2? Possibly, but the phrasing might need simplification. The lenses are described as "cross-subject cognitive lenses" without age adaptation. For a platform serving ages 5-14, the key questions should have age-appropriate variants.

---

## 4. Recommendations

### Must-have (blocks AI content generation quality)

1. **Surface `nc_year` from extraction data to the graph and context output.** The extraction JSON already contains `"year": [5]` on every concept. Import this as a property. Surface it in context output. This is a data pipeline fix, not new extraction work. Without it, no AI can distinguish Y3 retrieval from Y6 new learning.

2. **Include D013 (Forces Y5) in Y5 Science context.** This is the same bug flagged in v4. The domain exists in the graph with full cluster definitions and Thinking Lenses. It is not pulled into the Y5 context.

3. **Create a Content Vehicle for D013 (Forces Y5).** This is the most investigation-rich Y5 science domain: gravity drop tests (fair test), parachute investigations (fair test), lever/pulley practicals (pattern seeking). Currently zero vehicles. Suggested:
   - SC-KS2-CV011: Gravity and Air Resistance Investigation (fair test -- dropping objects with different parachute sizes)
   - SC-KS2-CV012: Levers and Pulleys (pattern seeking -- how does distance from fulcrum affect effort?)

4. **Fix CV001 delivers list.** Remove SC-KS2-C002, C003, C005 (Animals/Plants concepts). Replace with SC-KS2-C025, SC-KS2-C027 only. Verify all other Content Vehicles for similar cross-domain deliver errors.

### Should-have (significantly improves quality)

5. **Add method steps to Content Vehicles.** Numbered, sequential, actionable steps for each vehicle. Example for CV007:
   1. Set up torch at one end of table. Secure with Blu-Tack.
   2. Place white screen at other end (60cm from torch).
   3. Place opaque object 10cm from torch.
   4. Turn off lights. Measure shadow height on screen. Record.
   5. Move object to 20cm, 30cm, 40cm, 50cm. Repeat measurement.
   6. Repeat each distance 3 times. Calculate mean.

6. **Expand safety notes to hazard-specific format.** For each vehicle:
   - List specific hazards (not "low risk" generically)
   - List control measures
   - Flag any CLEAPSS references
   - Include teacher demonstration notes where applicable (e.g., laser pointer, boiling water)

7. **De-duplicate Thinking Lens rationales.** Write cluster-specific rationales that explain why the lens fits THAT cluster, not the topic generically. CL001 and CL002 within the same domain should never have identical rationale text.

8. **Add more Content Vehicles per domain.** Target: 2-3 vehicles per domain to give teachers genuine choice. Different enquiry types per vehicle (one fair test, one observation, one research) would demonstrate the breadth of Working Scientifically.

### Nice-to-have (improves teacher and AI resource generation)

9. **Add graph type reasoning to recording format.** "Line graph (independent variable is continuous)" or "Bar chart (independent variable is categorical)."

10. **Add rough time estimate to Content Vehicles.** Not per-lesson (that is teacher judgement) but per-vehicle: "This investigation typically takes 2-3 one-hour lessons including planning, practical, and recording."

11. **Add age-differentiated Thinking Lens key questions.** Y1-2 version: "What made this happen?" Y3-4 version: "What caused this to happen?" Y5-6 version: "What caused this to happen, and how do we know?" Y7-9 version: "What caused this to happen, how do we know, and what would falsify our explanation?"

---

## 5. Content Vehicle Quality Audit

I evaluated both science Content Vehicles used in my teaching (CV007 and CV001) against practical classroom reality. I also reviewed the remaining 8 KS2 science vehicles from the JSON data.

### SC-KS2-CV007 -- Light and Shadows

| Element | Accurate? | Notes |
|---------|-----------|-------|
| Equipment list | Mostly | Missing: cards with holes (for straight-line demo), laser pointer (class 2), blackout materials, protractor (extension). Listed equipment (torches, objects, screen, mirrors, ruler, metre stick) is correct and sufficient for the shadow investigation specifically. |
| Variables (independent) | Yes | "Distance between light source and object" -- correct and clearly stated. |
| Variables (dependent) | Yes | "Size of shadow (cm height)" -- correct. Could add "(cm height on screen)" for clarity. |
| Variables (controlled) | Yes | "Same light source, same object, same screen distance, darkened room" -- all correct and complete. |
| Recording format | Yes | "Results table -> line graph -> ray diagram" -- correct sequence. Line graph is the right choice for continuous independent variable. |
| Safety notes | Inadequate | "Do not shine torches directly into eyes. Supervise mirror use." Missing: darkened room trip hazards, torch battery security, reflected sunlight from mirrors, laser pointer safety, glass mirror risk. See Section 3b.4 for full list. |
| Expected outcome | Correct | "Shadows form when opaque objects block light. Shadow size increases as the object moves closer to the light source. Light travels in straight lines. We see objects because light reflects off them into our eyes." -- all four statements are scientifically accurate and age-appropriate. |
| Definitions | Good | 8 key terms listed. All scientifically accurate. Missing: "ray" and "luminous/non-luminous" which are essential Y5/Y6 Light vocabulary. |
| Assessment guidance | Good | Three assessment questions that map directly to statutory objectives. Could be more specific about expected depth of ray diagram. |
| Success criteria | Excellent | Four criteria that directly map to O079-O082. Usable as a teacher checklist without modification. |
| Enquiry type | Correct | "fair_test" -- the shadow distance investigation is a genuine fair test. |

**Overall CV007 quality: 7/10.** The investigation structure is sound. Equipment and safety are the weak points. The vehicle covers the investigation well but does not cover the full teaching sequence (introductory lessons, the straight-line demo, mirror work). This is a design question: should a Content Vehicle cover just the investigation or the full unit? Currently it is ambiguous.

### SC-KS2-CV001 -- Friction Investigation

| Element | Accurate? | Notes |
|---------|-----------|-------|
| Equipment list | Correct | "Ramp, toy car, metre stick, surface samples (carpet, wood, sandpaper, tile, fabric), masking tape" -- all standard primary science equipment, all necessary and sufficient. |
| Variables (independent) | Correct | "Surface type (carpet, wood, sandpaper, tile, fabric)" -- 5 surfaces is a good number for KS2. |
| Variables (dependent) | Correct | "Distance travelled by toy car (cm)" -- clear, measurable, appropriate. |
| Variables (controlled) | Correct | "Ramp angle, car mass, release point, same car" -- complete and correct. |
| Recording format | Correct | "Table of results -> bar chart -> written conclusion" -- bar chart is correct for categorical independent variable. |
| Safety notes | Adequate | "Low risk. Ensure ramp is stable and surfaces are secured flat." -- this is genuinely a low-risk investigation. The safety note is proportionate. |
| Expected outcome | Correct | "Rougher surfaces produce more friction, so the car travels a shorter distance. Smooth surfaces produce less friction." -- scientifically accurate and testable. |
| Definitions | Good | 7 key terms. "Fair test" and "variable" are particularly useful for WS development. |
| Assessment guidance | Good | Three questions covering variables, measurement, and explanation. |
| Success criteria | Excellent | Four criteria mapping to WS skills and content knowledge. |
| Enquiry type | Correct | "fair_test" -- this is the canonical KS2 fair test investigation. |
| **Delivers concept IDs** | **ERROR** | Lists SC-KS2-C002, C003, C005, C025, C027. C002, C003, C005 are from Animals/Plants domains, NOT Forces. This is a data error. Should be C025 and C027 only. |

**Overall CV001 quality: 7.5/10.** The investigation structure is excellent -- this is a textbook KS2 fair test. The delivers list error is the only significant problem but it is a data integrity issue that would cause incorrect concept coverage reporting.

### Remaining KS2 Science Vehicles (spot checks)

**CV002 (Plant Growth Enquiry):** Equipment correct (cress, pots, ruler). Variables well-structured. Safety note "Wash hands after handling soil. No allergenic plants" -- appropriate. Expected outcome correct. **7/10.**

**CV003 (Rocks and Fossils):** Enquiry type "identifying_and_classifying" -- correct, this is not a fair test. Variables correctly marked N/A. Equipment includes "vinegar (acid test for chalk)" -- useful and practical. Safety: "Supervise scratch tests. Vinegar is mild acid -- avoid eyes" -- adequate. NHM resource link is a positive addition. **8/10.**

**CV005 (Electrical Circuits):** Equipment correct and comprehensive. Safety: "Use only low-voltage cells (1.5V). Never connect directly across battery terminals (short circuit). Do not use mains electricity." -- this is the most complete safety note in the set, and appropriately so (electrical safety matters). **8/10.** The best safety note of all 10 vehicles.

**CV006 (States of Matter):** Safety: "Teacher demonstrates boiling water. Pupils do not handle hot water. Thermometers should be non-mercury." -- good, specific, hazard-appropriate. **7.5/10.**

**CV009 (Evolution and Adaptation):** Enquiry type "research" -- correct for this domain. Equipment includes "bird beak models (tweezers, pegs, chopsticks), seeds of different sizes" -- this is the classic bird beak simulation. Excellent. Safety: "No specific hazards. Ensure sensitivity around evolution/creation discussions." -- the sensitivity note is appropriate and unusual; it shows awareness of the classroom context. **8/10.** Best overall vehicle.

**CV010 (Separating Mixtures):** Equipment comprehensive. Safety: "Wear safety goggles during evaporation. Teacher supervises heating. Do not taste solutions." -- adequate but should add iron filings handling safety (iron filings are listed in equipment). **7/10.**

### Cross-Vehicle Patterns

| Pattern | Observation |
|---------|-------------|
| Safety quality | Ranges from minimal (CV007: 2 sentences) to thorough (CV005: 3 specific hazards). No consistency standard. |
| Equipment accuracy | Generally correct. No equipment listed that is unavailable to a typical primary school. |
| Variable structure | Well-structured for fair tests. Correctly marked N/A for non-fair-test enquiries. |
| Expected outcomes | All scientifically accurate. All age-appropriate. |
| Definitions | Generally good. Typically 7-9 terms per vehicle. |
| Assessment guidance | Consistently framed as 3 "Can pupils..." questions. Useful but could be more specific about expected depth. |
| Success criteria | Consistently 4 criteria per vehicle. All actionable. All assessable. This is the strongest element across all vehicles. |

**Errors found across all 10 vehicles:**
1. CV001 delivers wrong concept IDs (C002, C003, C005 from wrong domains)
2. CV007 missing equipment for core demonstration activities
3. CV007 safety notes inadequate for the range of activities involved
4. No vehicle references CLEAPSS guidelines (standard UK safety resource for school science)

---

## 6. Final Verdict

**The Content Vehicle layer is the single most important addition to the graph since its creation.**

My v4 review said: "A Science lesson without a practical is not a Science lesson." The graph now has practicals. They are structured, they have variables, equipment, recording formats, expected outcomes, and assessment criteria. An AI using CV007 can generate a shadow investigation that a Y5 class could actually do. An NQT could follow the vehicle without prior experience of the investigation. This was not possible before.

**The Thinking Lens layer is the second most important addition.**

It answers the v4 criticism that the graph had no crosscutting conceptual framework. The lenses give every lesson a cognitive frame -- not just "what are we learning?" but "what kind of thinking are we doing?" In practice, the Cause and Effect lens was powerful for investigation lessons and the Patterns lens was effective for consolidation. The lenses will be even more powerful for AI content generation, where consistent cognitive framing across sessions builds cumulative understanding.

**The graph is now 80% of what primary science needs (up from 70% in v4).**

The remaining 20% is:
- Year group attribution (5% -- the single most impactful missing property)
- D013 Forces Y5 inclusion in context + vehicle creation (5%)
- Safety notes expansion to hazard-specific format (3%)
- Method steps in Content Vehicles (3%)
- De-duplicated, cluster-specific Thinking Lens rationales (2%)
- Multiple vehicles per domain for teacher choice (2%)

**I would now trust an AI to generate a structured science investigation from this graph**, with the caveat that a teacher must review equipment availability, safety considerations, and time allocation. Before Content Vehicles, I would not trust an AI to generate any practical science content. That is a fundamental change.

**I would not yet trust an AI to plan a full Y5 science unit from the graph**, because the year-group problem means it cannot distinguish retrieval from new learning, and the missing D013 domain means it cannot plan the most important Y5 forces content.

**Comparison with v4:**
- V4: "The graph is 70% of what primary science needs. The missing 30% is the practical, procedural, cross-curricular layer."
- V5: "The graph is 80% of what primary science needs. The practical layer exists. The missing 20% is year-group attribution, domain coverage gaps, and safety/method detail."

The nature of the gap has shifted from structural (no investigation architecture) to data quality (incomplete safety, missing year groups, incomplete domain coverage). This is progress -- data quality problems are solvable without architectural change.

---

*V5 findings complete. Mrs Priya Kapoor, February 2026.*
