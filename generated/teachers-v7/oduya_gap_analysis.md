# Gap Analysis — Y5 Science (Separating Mixtures)

**Teacher**: Ms. Oduya (Y5 class teacher / Science subject lead)
**Cluster**: `SC-KS2-D011-CL002` — *Investigate dissolving and how to separate mixtures*
**Content Vehicle**: `SC-KS2-CV010` — *Separating Mixtures*
**Date**: 2026-02-23

---

## Section-by-Section Analysis

### 1. Learning Objectives — ✅ Fully supported

| Data Available | Data Missing | What I Invented |
|---------------|-------------|-----------------|
| Concept descriptions (C048, C049) clearly state what pupils should know | No explicit "learning objective" property phrased as "Pupils will..." | Nothing — I used concept descriptions directly |
| DEVELOPS_SKILL links C048 to "Planning enquiries and controlling variables" with `enquiry_type: fair_test` | WS objectives not linked at concept level for C049 (only C048 and C050 have concept-level skill links) | Nothing material |
| ThinkingLens "Cause and Effect" with KS2 agent_prompt and question stems | — | — |

**Verdict**: The concept descriptions are functionally equivalent to learning objectives. The concept-level skill link to WS is excellent where it exists — but only 16 KS2 Science concepts (out of ~70) have these links. C049 (Separating Mixtures) has no concept-level skill link despite being inherently investigative.

---

### 2. Success Criteria — ✅ Mostly supported

| Data Available | Data Missing | What I Invented |
|---------------|-------------|-----------------|
| Vehicle `success_criteria` array: 4 clear, assessable criteria | No WS-focused criteria (e.g., "control variables") | 3 WS-oriented success criteria |
| Vehicle `assessment_guidance` gives 3 key questions | Criteria not levelled (all/most/some) | — |

**Verdict**: Having explicit success criteria on the ContentVehicle is a strong feature. The criteria are content-focused; WS success criteria would need to be generated from the skill links.

---

### 3. Prior Knowledge — ✅ Fully supported

| Data Available | Data Missing | What I Invented |
|---------------|-------------|-----------------|
| PREREQUISITE_OF: C034 (Three States of Matter) → C049 | No diagnostic questions to check prior knowledge | Baseline check sorting activity |
| SEQUENCED_AFTER: CL001 (material properties) → CL002 (this cluster) | — | — |
| Cluster pedagogical_rationale explains the dissolving-melting link | — | — |

**Verdict**: The prerequisite chain is clear and accurate. The domain sequencing is correct. This is one of the graph's strongest structural features.

---

### 4. Lesson Structure with Timings — ⚠️ Partially supported

| Data Available | Data Missing | What I Invented |
|---------------|-------------|-----------------|
| Pedagogy profile session sequence: challenge_problem → guided_exploration → worked_example → independent_practice → retrieval_practice | No lesson plan template or activity descriptions | All specific activities (mystery mixture challenge, demonstrations, etc.) |
| Interaction types with implementation instructions (pattern_discovery, drag_categorise, multi_choice_4) | No timings or pacing guidance | All timing allocations |
| Vehicle recording_format: "method diagram → results table → reversible vs irreversible sorting" | No teaching script or teacher talk points | The flow and linking narrative |
| Vehicle variables (independent, dependent, controlled) | No worked example of how to set up the practical | Setup instructions for activities |
| Teaching guidance for C048 and C049 (detailed, practical) | — | — |

**Verdict**: The graph provides a rich set of *ingredients* — pedagogy sequence, interaction types, recording format, teaching guidance, variables — but no *recipe*. A teacher still needs to design the lesson flow, choose activities, and allocate time. The teaching guidance on concepts is detailed and practical, making it a strong source for activity ideas, but it's not structured as a lesson plan.

---

### 5. Key Vocabulary with Definitions — ✅ Mostly supported

| Data Available | Data Missing | What I Invented |
|---------------|-------------|-----------------|
| Concept `key_vocabulary` arrays: 17 terms on C048, 17 terms on C049 | No pupil-facing definitions (terms listed but not defined) | Child-friendly definitions for all 16 chosen terms |
| Vehicle `definitions` array: 9 key terms | Definitions on the vehicle are term-only, not actual definitions | — |
| Content guideline: FK grade max 2, max sentence length 14 words | No vocabulary progression (which terms are new to Y5 vs. revisited from Y4) | — |

**Verdict**: The vocabulary coverage is strong — both concepts and the vehicle list the key terms. But neither provides child-friendly definitions. The `definitions` property on ContentVehicle is misleadingly named — it's a list of terms, not definitions. Adding actual definitions would be high-value.

---

### 6. Resources and Materials — ⚠️ Partially supported

| Data Available | Data Missing | What I Invented |
|---------------|-------------|-----------------|
| Vehicle `equipment` array: 10 items (salt, sand, water, iron filings, filter paper, funnels, sieves, evaporating dishes, magnets, safety goggles) | Standard lab consumables: beakers, stirring rods, spatulas | 10+ additional items (beakers, scales, heat source, timer, recording sheets, etc.) |
| — | Quantities (how many beakers per group?) | — |
| — | Alternative/budget options | — |
| — | Preparation instructions (e.g., pre-make salt solutions day before) | — |

**Verdict**: The equipment list is a good starting point and covers the investigation-specific materials. But it's incomplete for actual classroom preparation — missing the everyday items that a technician/teacher needs to set out. No quantities, no alternatives, no prep instructions.

---

### 7. Differentiation — ⚠️ Weakly supported

| Data Available | Data Missing | What I Invented |
|---------------|-------------|-----------------|
| Learner profile scaffolding_level: moderate_to_high | No differentiated activities or resources | All support, core, extension, and greater depth activities |
| Learner profile hint_tiers: max 3 | No levelled success criteria (all/most/some) | — |
| — | No DifficultyLevel nodes for Y5 Science (pilot is Y3 Maths only) | — |
| Content guideline: FK grade 2, Lexile 150-350L | No SEN-specific guidance | — |
| — | No EAL/multilingual guidance | — |

**Verdict**: This is a significant gap. The learner profile gives abstract parameters (scaffolding level, hint tiers) but no concrete differentiated activities. The DifficultyLevel layer — which would provide grounded difficulty tiers with example tasks at each level — only covers Y3 Maths. Extending it to Y5 Science would immediately fill this gap.

---

### 8. Assessment Opportunities — ⚠️ Partially supported

| Data Available | Data Missing | What I Invented |
|---------------|-------------|-----------------|
| Vehicle `assessment_guidance`: 3 diagnostic questions | No rubric or marking criteria | Full assessment plan with 7 assessment points |
| Feedback profile: style, tone, example phrases, avoid phrases | No formative assessment checkpoints | — |
| Common misconceptions provide diagnostic content | No summative assessment link (no link to Assessment layer for Y5) | — |

**Verdict**: The assessment_guidance on the vehicle is useful but shallow — 3 questions with no rubric. The feedback profile is excellent for tone and phrasing. The misconceptions are perfect diagnostic content. But there's no structured assessment framework (e.g., emerging/expected/exceeding descriptors).

---

### 9. Common Misconceptions — ✅ Fully supported

| Data Available | Data Missing | What I Invented |
|---------------|-------------|-----------------|
| C048: 3 detailed misconceptions (dissolving=melting, "gone forever", stirring confusion) | No diagnostic questions that target each misconception | Nothing |
| C049: 3 detailed misconceptions (filtering solutions, sieving=filtering, "can never separate") | No "how to address" scripts — only the correct understanding | — |
| Feedback profile says "keep misconception correction implicit" | — | — |

**Verdict**: This is the graph's single strongest feature for science. The misconceptions are specific, curriculum-accurate, and explain both the error and the correct understanding. Any AI or teacher can use these directly. The feedback profile even tells you *how* to correct them (implicitly, not explicitly). Excellent.

---

### 10. Worked Examples / Model Investigations — ❌ Not supported

| Data Available | Data Missing | What I Invented |
|---------------|-------------|-----------------|
| Vehicle `recording_format`: describes WHAT to record | No model method diagrams | Full method diagram template |
| Vehicle `expected_outcome`: describes the answer | No model results tables | Full results table with model entries |
| Teaching guidance describes practical steps | No annotated pupil work examples | — |
| — | No "what good looks like" exemplars | — |
| — | No scientific diagram conventions (labelling, ruler lines, pencil) | — |

**Verdict**: This is the most critical gap for science teaching. Pupils need to see model scientific diagrams before they produce their own — especially in Y5 when they're expected to record formally. The graph has no templates, exemplars, or diagram conventions. The `recording_format` tells me "method diagram for each separation → results table" but not what a method diagram should look like. For a science subject lead, this is non-negotiable: I need model diagrams with correct labelling conventions.

---

### 11. Practice Questions / Follow-up Investigations — ⚠️ Partially supported

| Data Available | Data Missing | What I Invented |
|---------------|-------------|-----------------|
| Teaching guidance on C048 suggests follow-up: "Investigate factors affecting dissolving rate: temperature, stirring, grain size" | No ready-made practice questions | All 5 practice questions |
| Misconceptions provide excellent raw material for diagnostic questions | No question banks at any level | — |
| Thinking lens question stems: "What would happen if we changed just one thing?" | No homework or follow-up activity designs | — |

**Verdict**: The teaching guidance and misconceptions provide good *source material* for writing questions, but no questions exist in the graph. The thinking lens question stems are a nice framing device but not subject-specific questions. A question bank (even 5-10 per cluster) would be transformative.

---

### 12. Cross-Curricular Links — ⚠️ Weakly supported

| Data Available | Data Missing | What I Invented |
|---------------|-------------|-----------------|
| MA-Y5-C017 (Reading and Interpreting Graphs, Tables and Timetables) found via concept search | No explicit cross-curricular relationship type in graph model | English, D&T, Geography, PSHE links |
| WS skills implicitly link to Maths (measurement, data recording) | No LINKS_TO or CROSS_CURRICULAR relationship | — |
| CO_TEACHES relationships exist but none for C048/C049 across subjects | — | — |

**Verdict**: Cross-curricular links are discoverable by searching for related concepts in other subjects, but there's no structural support. A CROSS_CURRICULAR relationship type (or enriching CO_TEACHES to span subjects more broadly) would make this automatic.

---

## Overall Readiness Score

### **6/10** — Good structural foundation, significant practical gaps

The graph provides:
- **Strong** (8/10): Concept content (descriptions, vocabulary, misconceptions), curriculum structure (prerequisites, domain sequencing), pedagogical framing (thinking lenses, learner profiles, interaction types), content vehicle metadata (equipment, variables, assessment guidance, recording format, enquiry type)
- **Moderate** (5/10): Teaching guidance (detailed but unstructured), success criteria, safety notes (basic but incomplete)
- **Weak** (2/10): Worked examples, differentiation activities, practice questions, cross-curricular links, complete equipment lists

For **science specifically**, the investigation support is better than I expected: the ContentVehicle provides equipment, variables, enquiry type, recording format, and expected outcomes. But it's missing the practical detail that makes a lesson actually *work* in a classroom: model diagrams, safety protocols, preparation instructions, and differentiation scaffolds.

---

## Science-Specific Gaps

### 1. No recording templates or model diagrams
Science requires pupils to produce formal scientific diagrams with specific conventions (pencil lines, ruled labels, title, date). The graph describes what to record but never shows what the recording should look like. This is the #1 gap.

### 2. Safety notes are skeletal
The vehicle has 3 bullet points. A real risk assessment for this lesson would have 10-15 hazard/precaution/first-aid entries. Iron filings near eyes, glass breakage, heat source burns, and disposal procedures are all missing.

### 3. No investigation scaffolds
The vehicle identifies variables (independent, dependent, controlled) but provides no planning frame, prediction scaffold, or conclusion frame. Y5 pupils need structured templates for fair test planning — the "I think ___ because ___. I will change ___. I will measure ___. I will keep ___ the same." format.

### 4. Enquiry type not linked to WS progression
The vehicle has `enquiry_type: fair_test` and the concept-level DEVELOPS_SKILL links to "Planning enquiries and controlling variables" — excellent. But only 2 of the 5 concepts delivered by this vehicle have concept-level skill links. The skill coverage is patchy.

### 5. No preparation/technician instructions
No guidance on what to prepare in advance (e.g., make salt solutions the day before, pre-cut filter paper, test sieves for mesh size). This is a real workflow gap — science coordinators need this.

---

## Top 5 Data Additions

### 1. DifficultyLevel nodes for Y5 Science concepts
**Priority: Critical**
Extend the Y3 Maths pilot to Y5 Science. Four levels per concept (entry → developing → expected → greater_depth) with `example_task`, `example_response`, and `common_errors` would immediately fix the differentiation gap. For this cluster: "Entry: Name a separation technique. Expected: Choose the right technique for a given mixture and explain why. Greater depth: Design a multi-step separation for a complex mixture."

### 2. Worked example / model recording templates on ContentVehicle
**Priority: Critical**
Add a `model_recording` property (or sub-node) with structured templates: method diagram SVG/description, model results table, annotated pupil work example. This is especially critical for science where recording conventions matter.

### 3. Structured safety data on ContentVehicle
**Priority: High**
Replace the free-text `safety_notes` with a structured array: `[{hazard, precaution, first_aid, severity}]`. For this lesson: `{hazard: "iron filings near eyes", precaution: "wear goggles; use on trays", first_aid: "flush with water", severity: "medium"}`.

### 4. Practice question bank per cluster
**Priority: High**
Add 5-10 questions per cluster, tagged by type (recall, application, analysis) and difficulty level. Use the existing misconceptions as distractor sources. Could be a new `:PracticeQuestion` node or a JSON property on ConceptCluster.

### 5. Explicit cross-curricular relationships
**Priority: Medium**
Add `(:Concept)-[:CROSS_CURRICULAR {link_type, rationale}]->(:Concept)` for known cross-subject links. E.g., SC-KS2-C048 (dissolving) → MA-Y5-C017 (interpreting graphs/tables) with `{link_type: "data_handling", rationale: "recording dissolving rate data in tables and bar charts"}`.

---

## Specific New Entities/Properties I'd Want

### New Node Types
| Node | Purpose | Example |
|------|---------|---------|
| `:PracticeQuestion` | Ready-made assessment questions per cluster | "Amir tries to filter salt water. Explain why this doesn't work." |
| `:RecordingTemplate` | Model scientific recording formats | Method diagram template for separation techniques |
| `:SafetyHazard` | Structured risk assessment per vehicle | {hazard: "iron filings", precaution: "goggles + tray", severity: "medium"} |

### New Properties on Existing Nodes
| Node | Property | Purpose |
|------|----------|---------|
| `ContentVehicle` | `preparation_instructions` | What to prepare before the lesson (make solutions, cut filter paper, etc.) |
| `ContentVehicle` | `equipment_quantities` | How many of each item per group (e.g., "6 × 250ml beakers") |
| `ContentVehicle` | `safety_hazards` (structured array) | Replace free-text safety_notes with structured hazard/precaution/first_aid |
| `ContentVehicle` | `model_recording` | Template/exemplar of expected pupil recording |
| `ContentVehicle` | `alternative_equipment` | Budget or access-limited alternatives |
| `Concept` | `investigation_scaffold` | Planning frame template for the relevant enquiry type |
| `ConceptCluster` | `cross_curricular_links` | Explicit subject connections with rationale |
| `ConceptCluster` | `practice_questions` (or separate nodes) | 5-10 ready-made questions per cluster |

### New Relationships
| Relationship | Purpose |
|-------------|---------|
| `(:Concept)-[:CROSS_CURRICULAR]->(:Concept)` | Explicit cross-subject links |
| `(:ContentVehicle)-[:HAS_SAFETY_HAZARD]->(:SafetyHazard)` | Structured safety data |
| `(:ConceptCluster)-[:HAS_PRACTICE_QUESTION]->(:PracticeQuestion)` | Assessment questions |
| `(:ContentVehicle)-[:HAS_RECORDING_TEMPLATE]->(:RecordingTemplate)` | Model recordings |

---

## Comparison with V4/V5 Reviews

Compared to the V5 teacher review findings:
- **Content readiness** has improved: the ContentVehicle + ThinkingLens combination gives a much richer foundation than the V4 graph alone
- **Misconceptions and vocabulary** are excellent — these were already strong in V5 and remain so
- **The V5 consensus gaps are confirmed**: no worked examples, no difficulty sub-levels (for Y5), equipment lists incomplete, safety notes thin
- **New finding**: concept-level DEVELOPS_SKILL links are patchy — only ~23% of KS2 Science concepts have them. Completing coverage would significantly improve WS integration

---

## Final Verdict

As a science subject lead, I could build a *good* lesson from this graph — the conceptual backbone is solid, the misconceptions are excellent, and the ContentVehicle provides a meaningful investigation structure. But I'd spend about 40% of my planning time inventing practical detail (model diagrams, differentiation activities, safety protocols, equipment quantities) that the graph doesn't yet provide.

The path to 9/10 for science:
1. DifficultyLevel nodes for Y5 Science (fixes differentiation)
2. Model recording templates (fixes worked examples)
3. Structured safety data (fixes safety)
4. Practice question bank (fixes assessment)
5. Complete concept-level skill links (fixes WS integration)

---

## Teaching Artefacts Needed

*What I'd need to go from "lesson plan on paper" to "ready to teach at 9am Monday" — in priority order for Y5 Science.*

### 1. Investigation Recording Scaffold (print, 1 per pupil) — CRITICAL

A structured A4 sheet that walks pupils through the fair test format:

- **Prediction**: "I think _____ because _____"
- **Variables box**: Change (independent) / Measure (dependent) / Keep the same (controlled) — with sentence starters
- **Method diagram**: blank template with numbered step boxes, space for labelled scientific diagrams (ruler lines, pencil)
- **Results table**: pre-drawn grid with column headers to fill in
- **Conclusion frame**: "I found out that _____. This happened because _____. My evidence is _____."

**Why this matters for science**: Y5 pupils are transitioning from informal to formal recording. Without a scaffold, half the class will write "we mixed stuff and it was cool" instead of a structured investigation. The recording format is as important as the content — it IS the Working Scientifically objective. The graph gives me `recording_format: "method diagram for each separation -> results table -> reversible vs irreversible sorting activity"` — the structure is there, but it needs to be turned into a printable pupil-facing template.

**What the graph provides**: Recording format string, variables (independent/dependent/controlled), expected outcome, success criteria. About 60% of the content exists; it needs layout and pupil-friendly phrasing.

### 2. Differentiated Practice Sheets (print, 3 versions) — CRITICAL

Three levelled worksheets (support / core / greater depth) with:

- **Support**: Scaffolded questions with word banks, sentence starters, diagrams to label (not draw from scratch), matching activities
- **Core**: Application questions requiring explanation ("Explain why filtering won't recover dissolved salt"), predict-and-explain tasks, "design a separation" challenges
- **Greater depth**: Open-ended investigation design ("Plan a fair test to find out if temperature affects dissolving rate"), multi-step separation puzzles, evaluation tasks ("Amir's results were different from Priya's — suggest why")

**Why this matters for science**: In a class of 30, I'll have pupils ranging from "can't spell 'dissolve'" to "already knows about saturated solutions from a YouTube video." Without levelled practice, I'm either pitching too high or too low for two-thirds of the class. The graph's misconceptions are perfect distractor material for questions, but no questions actually exist.

**What the graph provides**: Misconceptions (excellent distractor source), key vocabulary, teaching guidance with suggested activities, assessment guidance questions. Maybe 40% of the raw content; needs structuring into levelled questions with mark schemes.

### 3. Vocabulary Word Mat (print, laminated, 1 per table group) — HIGH

A single A4 landscape sheet with:

- All 14-16 key terms with child-friendly definitions and a small diagram/icon for each
- Organised by concept (dissolving terms on one side, separation techniques on the other)
- Pronunciation guide for tricky words (filtrate, solute, insoluble)
- "Use these words in your writing" reminder

**Why this matters for science**: Scientific vocabulary is the gateway to scientific thinking. If a child can't distinguish "dissolving" from "melting" or "filtering" from "sieving," they can't describe what they observe. A word mat on the table means they USE the vocabulary in real time during the practical, not just hear it once in the introduction. It also supports EAL learners and weaker readers without singling them out.

**What the graph provides**: Complete vocabulary lists (key_vocabulary on both concepts + definitions list on vehicle). The terms are there — about 80% of content exists. Needs child-friendly definitions (not provided), layout, and visual icons.

### 4. Knowledge Organiser (print, A4 landscape, stick in books) — HIGH

A single-page reference combining:

- **Key vocabulary** with definitions (top strip)
- **Separation techniques summary**: technique → what it separates → diagram → real-world example (central grid)
- **Key facts**: "Dissolving is NOT the same as melting", "A dissolved substance has NOT disappeared — it's still there", "The correct technique depends on the properties of the mixture"
- **Working Scientifically reminder**: how to plan a fair test (variables)
- **Links to prior learning**: "In Y4 you learned about solids, liquids and gases..."

**Why this matters for science**: Knowledge organisers are the backbone of retrieval practice. Pupils stick them in books and return to them across the half-term. For science, they need to encode both the content knowledge AND the investigation skills — it's the one artefact that bridges "what I learned" and "how I found out." They're also the single best resource for homework revision and parent communication.

**What the graph provides**: Concept descriptions, key vocabulary, teaching guidance, misconceptions, prerequisite knowledge, thinking lens framing. About 70% of the content exists; needs careful curation and layout. The `curriculum_context` and `pedagogical_rationale` from the cluster context would feed directly into this.

### 5. Safety Cards / Risk Assessment Sheet (print, laminated, 1 per table) — HIGH

A simple traffic-light card per table:

- **Green** (safe to do independently): pouring water, stirring, sieving, using magnets
- **Amber** (do carefully, ask if unsure): filtering with glass funnels, handling iron filings (keep away from eyes)
- **Red** (teacher supervises): anything involving heat (evaporation), carrying hot water, lighting/using Bunsen burners

Plus a one-page risk assessment for the teacher file with hazard/precaution/first-aid columns.

**Why this matters for science**: I cannot run a practical lesson without a risk assessment — it's a legal and professional requirement, not a nice-to-have. The traffic-light card is a classroom management tool: pupils self-regulate ("Is this green, amber, or red?") rather than queuing to ask me. The graph gives me `safety_notes: "Wear safety goggles during evaporation. Teacher supervises heating. Do not taste solutions."` — three sentences. A real risk assessment for this lesson would have 10-15 entries.

**What the graph provides**: 3 safety bullet points on the vehicle. About 15% of what's needed. This is the artefact with the biggest gap between what the graph provides and what the classroom requires.

### Honourable Mentions (would use if available, not top 5)

| Artefact | Why | Graph support |
|----------|-----|---------------|
| **Presentation slides** (5-8 slides for introduction + plenary) | For whole-class teaching phases — vocabulary introduction, demonstration narration, plenary questions | Vocabulary, misconceptions, thinking lens questions — about 50% |
| **Assessment rubric** (1 page, for marking books) | "Emerging / Expected / Exceeding" descriptors for this cluster, aligned to success criteria | Success criteria exist; descriptors don't — about 30% |
| **Homework sheet** (1 page, retrieval practice) | 5-6 spaced retrieval questions mixing this week's learning with prior topics | Misconceptions + teaching guidance give content; no questions exist — about 25% |
| **Working wall display** (A3 poster) | Key vocabulary, method diagram model, "What we found out" summary — stays up for the half-term | Vocabulary + expected outcome — about 50% |
| **Parent summary** (half-page) | "This week in science we learned about... Ask your child: Can they explain the difference between dissolving and melting?" | Concept descriptions + misconceptions — about 60%, very automatable |

### What's Missing from the Team Lead's List

For **primary science specifically**, I'd add:

- **Scientific diagram model sheet**: A printed exemplar showing correct diagram conventions (pencil lines, ruler-drawn labels, title, date, no colouring). This is a subject-specific literacy skill that pupils need to see modelled.
- **Equipment setup diagram**: A labelled illustration showing how to set up the practical (where the funnel goes, what the filter paper looks like in the funnel, where the beaker sits underneath). Half my planning time is drawing these by hand.
- **Sorting/classification cards**: Physical cards for the plenary activity (reversible vs irreversible changes). Printable, cuttable, laminate-able.

### Summary: Artefact Generation Readiness

| Artefact | Content from graph | Layout/design needed | Overall readiness |
|----------|-------------------|---------------------|-------------------|
| Investigation scaffold | 60% | Full template design | Medium |
| Differentiated practice sheets | 40% | Full question writing + levelling | Low |
| Vocabulary word mat | 80% | Definitions + layout | High |
| Knowledge organiser | 70% | Curation + layout | Medium-High |
| Safety cards | 15% | Full risk assessment authoring | Very Low |

**Bottom line**: The graph has the *conceptual content* to populate 3 of my top 5 artefacts (vocabulary mat, knowledge organiser, investigation scaffold) at 60-80% completeness. The other 2 (differentiated practice, safety cards) need substantial new data. The biggest single improvement would be a **practice question bank** per cluster — that alone would unlock both the differentiated worksheets AND the homework sheets AND the assessment rubric.
