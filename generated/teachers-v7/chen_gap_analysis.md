# Gap Analysis: Y3 Science — Light and Shadows

**Teacher:** Ms. Chen (NQT+2), Year 3, Sheffield
**Cluster:** SC-KS2-D005-CL001 — *Investigate light sources, vision, and the formation of shadows*
**Date:** 2026-02-23

---

## Section-by-Section Analysis

### 1. Learning Objectives — ✅ Rating: 9/10

**Available from graph:**
- 5 statutory Light objectives (SC-KS2-O025 to SC-KS2-O029) with full NC text
- 4 additional Y6 Light objectives (SC-KS2-O079 to SC-KS2-O082)
- 8 Working Scientifically skills (WS-KS2-001 to WS-KS2-008) with progression chains (builds on / leads to)
- All 9 objectives linked to specific concepts via TEACHES relationships
- WS skills linked to specific concepts via DEVELOPS_SKILL (3 links in Light domain)

**Missing from graph:**
- No year-group tagging on objectives within KS2 — cannot distinguish Y3 objectives from Y6 objectives programmatically
- WS skills are KS2-wide — no Lower/Upper KS2 split despite the NC specifying different expectations

**What I invented:** Selection of which objectives are Y3-appropriate (I know the NC, so this was straightforward — but an AI agent without my curriculum knowledge would struggle to filter correctly).

---

### 2. Success Criteria — ⚠️ Rating: 5/10

**Available from graph:**
- Content vehicle `success_criteria` property: 4 statements
- Content vehicle `expected_outcome` property: summary sentence
- Content vehicle `assessment_guidance` property: 3 assessment questions

**Missing from graph:**
- Success criteria span Y3-Y6 with no year tagging (ray diagrams are Y6, not Y3)
- No child-friendly success criteria ("I can..." statements)
- No differentiated success criteria (working towards / expected / greater depth)
- DifficultyLevel nodes would help here but only exist for Y3 Maths (pilot)

**What I invented:** Rewrote all 5 success criteria in Y3-appropriate "I can..." language, stripped out Y6 content, added age-appropriate expectations.

---

### 3. Prior Knowledge Required — ✅ Rating: 8/10

**Available from graph:**
- Explicit PREREQUISITE_OF chain: SC-KS1-C026 (Material Properties) -> SC-KS2-C022 (Light and Vision)
- Cross-KS prerequisite (KS1 -> KS2) resolved correctly
- Prerequisite concept has full description, teaching guidance, and misconceptions

**Missing from graph:**
- No "prerequisite check" questions or diagnostic assessment to verify children have the prerequisites
- No link to everyday experience prerequisites (e.g., "can name common light sources") which aren't formal concepts but are assumed knowledge
- No indication of *how critical* each prerequisite is — is Material Properties essential or just helpful?

**What I invented:** Nothing significant — the prerequisite data was sufficient.

---

### 4. Lesson Structure with Timings — ⚠️ Rating: 4/10

**Available from graph:**
- Pedagogy profile session sequence: challenge_problem -> guided_exploration -> worked_example -> independent_practice -> retrieval_practice
- Session length: 12-20 minutes (for digital sessions)
- Productive failure: appropriate for Y3
- Scaffolding level: moderate_to_high
- Content vehicle enquiry type: fair_test
- Content vehicle variables (independent, dependent, controlled)
- Content vehicle recording format: results table -> line graph -> ray diagram

**Missing from graph:**
- No classroom lesson timings — only digital session lengths
- No starter/main/plenary structure (the standard primary school format)
- No guidance on grouping (pairs? tables? whole class?)
- No transition guidance between activities
- No dark den / practical setup guidance
- No guidance on how long each phase of a fair test takes with Y3 children
- No awareness that 7-year-olds need more time to set up equipment, need explicit instructions, need physical demonstrations before independent work
- The session sequence is designed for an AI tutor, not a classroom teacher

**What I invented:** Entire lesson structure (10/35/15 split), dark den idea, grouping decisions, transition timings, physical setup logistics, the sequence of activities within the main phase.

---

### 5. Key Vocabulary with Definitions — ✅ but ⚠️ Rating: 7/10

**Available from graph:**
- SC-KS2-C022 key_vocabulary: 16 terms
- SC-KS2-C024 key_vocabulary: 15 terms
- Combined deduplicated: ~22 unique terms
- Content vehicle `definitions` list: 8 terms (light source, opaque, transparent, translucent, shadow, reflection, ray, straight line)

**Missing from graph:**
- No definitions for any vocabulary term — just flat word lists
- The content vehicle `definitions` property is a list of words, not word-definition pairs
- No tier classification (Tier 2 academic vs Tier 3 scientific)
- No indication which words are new to Y3 vs already known from KS1
- No phonetic support or pronunciation guidance for EAL learners
- No visual support suggestions (which words need a picture?)

**What I invented:** Every single definition in the vocabulary table.

---

### 6. Resources and Materials Needed — ⚠️ Rating: 4/10

**Available from graph:**
- Content vehicle `equipment` list: 6 items (torches, opaque objects, white screen/card, mirrors, ruler, metre stick)
- Content vehicle `safety_notes`: "Do not shine torches directly into eyes. Supervise mirror use."

**Missing from graph:**
- Only 6 items listed — a real Y3 science lesson needs 15-20 resource types
- No transparent or translucent example materials (essential for the material sorting activity)
- No preparation materials (bin bags for dark den, tape, picture cards)
- No recording materials (sheets, pencils)
- No display/plenary resources (visualiser, whiteboard)
- No age-specific equipment guidance: standard torches are too large for Y3 hands — need small LED penlights
- No quantities: how many torches per group? How many rulers?
- No "where to get it" notes — can I find these in the school science cupboard or do I need to order?
- Safety notes are minimal: "Don't shine in eyes" is necessary but not sufficient for Y3. What about hot bulb torches? Broken mirror hazard? Children running in darkened rooms?

**What I invented:** Additional 10+ items, dark den materials, quantities, age-appropriate equipment suggestions, extended safety considerations.

---

### 7. Differentiation — ❌ Rating: 1/10

**Available from graph:**
- Learner profile scaffolding level: "moderate_to_high"
- Hint tiers: max 3
- DifficultyLevel nodes: not available for Science (Y3 Maths pilot only)

**Missing from graph:**
- No differentiation strategies for classroom teaching
- No SEN adaptations (visual impairment is particularly relevant for a LIGHT lesson)
- No EAL support strategies
- No greater depth challenges
- No grouping suggestions
- No simplified/extended recording formats
- No alternative evidence-gathering methods for children who struggle with writing
- The DifficultyLevel layer would be transformative here but hasn't been extended to Science yet

**What I invented:** All differentiation — support strategies (pre-teaching, simplified recording, sentence stems, paired work) and extension activities (coloured shadows, two light sources, prediction at longer distances, explanation cards).

---

### 8. Assessment Opportunities — ⚠️ Rating: 4/10

**Available from graph:**
- Content vehicle `assessment_guidance`: 3 questions (but mixed Y3/Y6)
- Learner profile mastery threshold: 5 correct in 7 days (80%)
- Interaction type specifications (MC3, categorise, matching — with Y3-appropriate limits)

**Missing from graph:**
- Assessment guidance mixes Y3 and Y6 without year tags
- No formative assessment prompts for during-lesson use
- No observation checklist for WS skills
- No rubric aligned to success criteria
- No exit ticket / hinge questions
- No guidance on what "working towards", "expected", and "greater depth" look like for this cluster
- No assessment recording sheet template
- Mastery threshold is for digital spaced retrieval, not classroom assessment

**What I invented:** Full assessment table with when/what/how, exit ticket with 3 questions, observation focus areas.

---

### 9. Common Misconceptions — ✅ Rating: 9/10

**Available from graph:**
- SC-KS2-C022: 3 specific misconceptions with explanations
- SC-KS2-C024: 3 specific misconceptions with explanations
- Each misconception names what children actually think/say
- Each provides the correct scientific understanding

**Missing from graph:**
- No indication of how common each misconception is (prevalence data)
- No suggested diagnostic questions to surface each misconception
- No "what to say" scripts for addressing each misconception with Y3 children
- No link between misconceptions and specific activities that surface them

**What I invented:** Timing column (when to address each misconception during the lesson).

---

### 10. Worked Examples / Model Investigations — ⚠️ Rating: 5/10

**Available from graph:**
- Content vehicle: investigation structure (enquiry type, variables, recording format, expected outcome)
- Concept teaching_guidance: step-by-step investigation descriptions
- Thinking lens question stems for framing the investigation

**Missing from graph:**
- No example data / model results
- No model write-up showing what a Y3 conclusion looks like
- No photograph or diagram of the investigation setup
- No step-by-step method written for children (the teaching_guidance is for teachers, not pupils)
- No scaffold for recording (e.g., a pre-drawn table with labelled columns)
- No common mistakes during the investigation process (e.g., "children often measure from the wrong edge of the shadow")

**What I invented:** Model results table with realistic data, model conclusion in Y3 language.

---

### 11. Practice Questions / Follow-Up Tasks — ⚠️ Rating: 3/10

**Available from graph:**
- Interaction type specifications: MC3 (3 options), drag-to-categorise (2-3 categories for Y3), matching pairs (4-5 pairs)
- Thinking lens question stems (4 stems per lens)
- Pedagogy profile: interleaving + spacing requirements

**Missing from graph:**
- Zero actual questions in the graph
- No question bank per concept
- No graduated difficulty within questions
- No answer keys
- No "common wrong answers" for each question (distractor rationale)
- No homework / follow-up investigation suggestions
- No links to next lesson in the sequence

**What I invented:** All 3 MC questions, the categorisation activity, the matching pairs activity, the shadow diary follow-up task.

---

### 12. Cross-Curricular Links — ⚠️ Rating: 3/10

**Available from graph:**
- 1 cross-domain CO_TEACHES link: SC-KS2-C067 ↔ MA-Y5-C015 (Maths reflection/translation)
- Rationale provided: angles of incidence/reflection

**Missing from graph:**
- The one link available is Y5+, irrelevant for Y3
- No Y3 Maths links (measurement, data handling in tables)
- No English links (scientific vocabulary, explanation writing)
- No Art links (shadow puppets, silhouettes — the classic Y3 Light art project)
- No PSHE links (sun safety)
- No links to seasonal change topics from KS1
- Cross-domain CO_TEACHES only tracks within-subject connections, not genuine cross-curricular links

**What I invented:** All 5 cross-curricular links (Maths, English, Art, PSHE, Geography).

---

## Overall Readiness Score

### **6/10 — Good conceptual foundation, weak on classroom practicalities**

**The graph excels at:**
- Curriculum content: objectives, concepts, misconceptions are excellent
- Conceptual structure: prerequisite chains, co-teaches, cluster sequencing work well
- Thinking lenses: provide genuine cognitive framing for investigation design
- Content vehicles: give real investigation structure (variables, equipment, enquiry type)
- Learner profiles: provide age-appropriate interaction and pedagogy guidance (for digital)

**The graph struggles with:**
- Year-group specificity within a Key Stage (KS2 content is not separated into Y3/Y4/Y5/Y6)
- Classroom lesson planning (timings, grouping, transitions, physical logistics)
- Differentiation at any level
- Assessment that maps to NC expectations (working towards / expected / greater depth)
- Vocabulary definitions (words without meanings)
- Resource quantities and specifications for age groups
- Practice content (questions, activities, follow-up tasks)
- Cross-curricular connections beyond subject-internal links

---

## Y3 Science-Specific Gaps

### 1. Practical Safety at Age 7-8
The graph's safety notes are one-liners ("Do not shine torches directly into eyes"). For Y3, I need:
- Safe torch handling (hot bulb warnings for older-style torches, dropping hazards)
- Darkened room management (children stumbling, anxiety about dark)
- Mirror handling (breakage risk with 7-year-olds)
- Water tray management (if using water for transparent material investigation)
- First aid location for specific hazards
- **CLEAPSS references** — the standard safety resource for UK primary science

### 2. Equipment for Small Hands
The equipment list doesn't consider Y3 physicality:
- Standard torches are too big — need small LED penlights (7-year-old hand span is ~14cm)
- Metre sticks are unwieldy — children might need support to read them
- Mirror size matters — small hand mirrors, not large wall mirrors
- Rulers need clear markings — some children still struggle with reading scales at Y3

### 3. Recording Scaffolds
The content vehicle says "results table -> line graph -> ray diagram" but:
- Y3 children are just learning to draw results tables — they need a **pre-drawn template**
- Line graphs are Upper KS2 (Y5/6) — Y3 should use **bar charts** or pictograms
- Ray diagrams are Y6 — Y3 children should **draw and label** their investigation setup
- Many Y3 children still have limited writing stamina — need **sentence stems** and **word banks**

### 4. Year-Group Tagging
Science at KS2 is one programme (SC-KS2) covering Y3-Y6. The graph has no way to distinguish:
- Which objectives are taught in Y3 vs Y6
- Which concepts are introduced in Y3 vs revisited in Y6
- Which recording formats are Y3-appropriate vs Y6-appropriate
- Which success criteria match Y3 expectations vs Y6 expectations

The teaching_guidance property sometimes mentions "In Year 3..." and "In Year 6..." which is helpful but inconsistent — it's prose, not queryable metadata.

### 5. Working Scientifically Progression Within KS2
The NC specifies different WS expectations for Lower KS2 (Y3-4) vs Upper KS2 (Y5-6):
- Lower: observe closely, simple equipment, simple tables, basic patterns
- Upper: control variables, systematic measurement, line graphs, evaluate evidence

The graph has WS-KS2 skills but doesn't split them. An AI agent planning a Y3 lesson might expect children to "control variables" (Y5/6 expectation) when Y3 children should be learning to "observe closely" and "perform simple tests."

---

## Top 5 Data Additions

### 1. Year-Group Tags on KS2 Science Content (Priority: CRITICAL)
**Problem:** All Science KS2 content is tagged KS2 with no year differentiation. A teacher or AI cannot programmatically determine what's Y3 vs Y6.
**Solution:** Add `year_groups: ['Y3']` or `year_groups: ['Y6']` property to Objectives and Concepts within Science KS2. The NC specifies this clearly.
**Impact:** Would fix success criteria, assessment, recording format, and WS progression issues in one change.

### 2. Vocabulary Definitions (Priority: HIGH)
**Problem:** Key vocabulary is word lists only — no definitions, no examples, no pronunciation.
**Solution:** Change `key_vocabulary` from a comma-separated string to a structured array: `[{word: "opaque", definition: "Blocks all light", example: "A wooden door is opaque", tier: 3}]`
**Impact:** Would make vocabulary sections generate-ready. Currently every vocabulary table must be teacher-written.

### 3. DifficultyLevel Nodes for Science (Priority: HIGH)
**Problem:** DifficultyLevel pilot covers Y3 Maths only. Science has no difficulty tiers.
**Solution:** Extend the DifficultyLevel layer to Y3 Science domains (Light, Rocks, Plants, Forces, Animals). Use the same entry/developing/expected/greater_depth structure.
**Impact:** Would enable differentiation, assessment criteria, and graduated success criteria — currently the biggest gap.

### 4. Question Bank per Concept (Priority: HIGH)
**Problem:** Zero practice questions in the graph. Teachers must write all questions from scratch.
**Solution:** Add 5-10 questions per concept, tagged by difficulty level and interaction type. Include distractors with misconception rationale.
**Entity:** New node type `:PracticeQuestion` or property array on Concept nodes.
**Impact:** Would make practice sections generate-ready. Currently rated 3/10.

### 5. Classroom Lesson Template Layer (Priority: MEDIUM)
**Problem:** The pedagogy profile is designed for 12-20 minute digital sessions, not 60-minute classroom lessons.
**Solution:** Add a `:LessonTemplate` node per cluster_type (introduction/practice) with classroom timings, grouping suggestions, and transition notes. Link to content vehicles.
**Properties:** `total_duration`, `starter_minutes`, `main_minutes`, `plenary_minutes`, `grouping_suggestion`, `physical_setup_notes`, `transition_notes`
**Impact:** Would bridge the gap between digital pedagogy profiles and classroom teaching reality.

---

## Specific New Entities/Properties Requested

### New Properties on Existing Nodes

| Node | Property | Type | Example |
|---|---|---|---|
| Concept | `year_groups` | string[] | `['Y3']` or `['Y3', 'Y6']` |
| Concept | `vocabulary_definitions` | JSON[] | `[{word: "opaque", definition: "...", tier: 3}]` |
| Objective | `year_groups` | string[] | `['Y3']` |
| ContentVehicle | `year_groups` | string[] | `['Y3']` |
| ContentVehicle | `equipment_details` | JSON[] | `[{item: "torch", quantity_per_group: 1, specification: "LED penlight", age_notes: "small enough for Y3 hands"}]` |
| ContentVehicle | `safety_notes_detailed` | JSON[] | `[{hazard: "torch in eyes", severity: "medium", mitigation: "...", cleapss_ref: "..."}]` |
| ContentVehicle | `differentiation_support` | string | Strategies for working-towards children |
| ContentVehicle | `differentiation_extension` | string | Greater-depth challenges |
| ConceptCluster | `classroom_duration_minutes` | int | `60` |
| ConceptCluster | `grouping_suggestion` | string | `"pairs"` |

### New Node Types

| Node | Purpose | Properties |
|---|---|---|
| `:PracticeQuestion` | Bank of questions per concept | `question_text`, `answer`, `distractors[]`, `misconception_targeted`, `difficulty_level`, `interaction_type`, `year_group` |
| `:RecordingScaffold` | Age-appropriate recording templates | `template_type` (table, bar chart, labelled diagram), `year_groups`, `description`, `image_url` |
| `:SafetyGuidance` | Detailed practical safety per investigation | `hazard`, `risk_level`, `mitigation`, `cleapss_reference`, `year_group_notes` |

### New Relationships

| From | Rel | To | Properties |
|---|---|---|---|
| Concept | HAS_QUESTION | PracticeQuestion | `difficulty`, `interaction_type` |
| ContentVehicle | HAS_SAFETY | SafetyGuidance | |
| ConceptCluster | HAS_SCAFFOLD | RecordingScaffold | `year_group` |
| Concept | CROSS_CURRICULAR | Concept | `link_type`, `rationale` (spanning subjects) |

---

## Comparison Note: Y3 Science vs Y3 Maths

The DifficultyLevel pilot (Y3 Maths) demonstrates exactly what Y3 Science needs. In Maths, each concept has entry/developing/expected/greater_depth levels with `example_task`, `example_response`, and `common_errors`. If the Light concepts had this:

- **Entry:** "Can name 2 light sources" / example: "The sun and a torch"
- **Developing:** "Can explain we need light to see" / example: "We need light because..."
- **Expected:** "Can explain shadow formation using opaque/transparent" / example: "A shadow forms when..."
- **Greater depth:** "Can predict and explain shadow size changes" / example: "The shadow is bigger because..."

This would give immediate differentiation, assessment criteria, and success criteria — solving three gaps at once.

---

## Teaching Artefacts Needed

What I'd need to go from "lesson plan on paper" to "ready to teach at 9am Monday" — in priority order for Y3 Science practical work.

### Top 5 (Priority Order)

#### 1. Recording Sheets / Investigation Worksheets (CRITICAL)

Y3 children cannot set up their own results tables from scratch. For the Light and Shadows investigation, I need a pre-printed sheet with:
- A results table with columns labelled ("Distance from torch (cm)" / "Shadow height (cm)") and rows pre-drawn
- Sentence stems for the conclusion: "I found that when the object was ______, the shadow was ______. The pattern is ______."
- A labelled diagram space: "Draw your investigation setup and label: torch, object, screen, shadow"
- Differentiated versions: supported (pictorial — draw the shadow, circle bigger/smaller), expected (table + sentence stems), greater depth (blank table, open conclusion)

**Why this matters for Y3 Science specifically:** 7-year-olds have limited writing stamina and are just learning to organise data. Without a scaffold, half my class would spend 20 minutes drawing the table border and run out of time for the actual investigation. The recording sheet IS the differentiation tool — it determines what each child can access.

**What the graph provides:** Content vehicle has `recording_format: "results table -> line graph -> ray diagram"` — this tells me the FORMAT but gives me nothing to print. No template, no scaffold, no differentiated versions. Line graphs and ray diagrams are Y6, not Y3 — further evidence of the year-tagging gap.

#### 2. Vocabulary Cards / Word Mat (HIGH)

A single A4 laminated word mat for each table with:
- Key words: light source, luminous, opaque, translucent, transparent, shadow, reflect
- Each word with: definition in child-friendly language, a small picture/diagram, the word broken into syllables for reading support (o-paque, trans-lu-cent)
- Stays on the table throughout the unit (not just this lesson) — children refer to it during writing

**Why this matters for Y3 Science specifically:** Y3 is where scientific vocabulary load increases sharply. In KS1, children use everyday words ("see-through", "blocks light"). In Y3, they must learn and USE the Tier 3 terms (opaque, translucent, transparent). Without a word mat, half my class will revert to everyday language and never embed the vocabulary. EAL learners (I have 6 in my class) rely on these completely.

**What the graph provides:** Concept `key_vocabulary` gives me the word lists (16 terms for C022, 15 for C024). The content vehicle `definitions` lists 8 key terms. But there are no definitions, no pictures, no syllable breakdowns, no child-friendly explanations. I have the WORDS but nothing printable.

#### 3. Knowledge Organiser (HIGH)

A single-page A4 knowledge organiser for the Light unit (not just this lesson) with:
- Key vocabulary with definitions (top section)
- Key facts: "We need light to see", "Dark is the absence of light", "Shadows form when opaque objects block light"
- A labelled diagram of the investigation setup
- "Did you know?" facts to extend knowledge
- Links to prior learning: "In Year 2, you learned about materials. Now we're learning how materials interact with light."

**Why this matters for Y3 Science specifically:** Knowledge organisers are the standard tool in UK primary schools for retrieval practice. Children take them home, stick them in their books, and use them for self-quizzing. The graph's pedagogy profile specifically recommends spaced retrieval (2-7 day intervals) and interleaving — a knowledge organiser is how you IMPLEMENT those techniques in a classroom without a digital platform. Parents can quiz their children using it.

**What the graph provides:** All the raw content is there — concepts, vocabulary, prerequisites, misconceptions. But it's spread across multiple nodes and properties. A knowledge organiser needs this synthesised into a single printable page. The graph could generate the TEXT content; it cannot generate the LAYOUT.

#### 4. Presentation Slides / IWB Flipchart (MEDIUM-HIGH)

5-8 slides for the interactive whiteboard:
- Slide 1: Challenge question — "What can you see in this picture?" (dark room photo)
- Slide 2: Key vocabulary with images (opaque/translucent/transparent shown with photos)
- Slide 3: Investigation instructions with numbered steps and equipment photo
- Slide 4: Model results table (I fill in first row as demonstration)
- Slide 5: Pattern question — "What pattern can you see?" with class results
- Slide 6: Sorting activity — drag materials into opaque/translucent/transparent categories
- Slide 7: Exit ticket — 3 multiple choice questions
- Slide 8: Plenary — "What did we learn today?" with key facts summary

**Why this matters for Y3 Science specifically:** I do not teach without a flipchart. Y3 children need visual anchoring — when I say "opaque", I need a picture of a brick wall on the board, not just the word. The investigation instructions must be visible throughout the practical so children can check what to do next without asking me (freeing me to circulate and assess). The exit ticket on the board means every child answers simultaneously.

**What the graph provides:** Interaction types (MC3, drag-to-categorise) tell me the FORMAT of activities. Thinking lens question stems give me discussion prompts. Misconceptions tell me what to address. But there are no actual slides, no images, no visual resources. I'd have to build the entire presentation from scratch.

#### 5. Sorting Cards / Practical Resources Templates (MEDIUM)

Printable card sets for the hands-on activities:
- Light source sorting cards: 10 picture cards (sun, torch, candle, lamp, moon, mirror, bicycle reflector, TV screen, star, glow-worm) with the word and image
- Material classification cards: 8 cards showing opaque/translucent/transparent objects
- "Luminous or Non-luminous?" sorting headers

**Why this matters for Y3 Science specifically:** The sorting activity in Part A of my lesson relies on physical cards that children can handle, discuss, and physically place into groups. Y3 children learn through manipulation — the graph's "Drag to Categorise" interaction type is the digital equivalent of what I do with physical cards on a table. I need the physical version. Card sorting also lets me circulate and listen to children's reasoning, which is my primary formative assessment strategy.

**What the graph provides:** The concept teaching guidance mentions sorting activities ("Compare objects that produce their own light (luminous) with those that reflect light (non-luminous)") and the interaction type describes categorisation with 2-3 categories for Y3. But there are no printable cards, no images, no ready-made sorting activities.

### Honourable Mentions (Not Top 5, But I'd Use Them)

- **Marking rubric / assessment grid:** Mapped to the 3 success criteria, with working-towards / expected / greater-depth descriptors. The DifficultyLevel layer would feed this directly if extended to Science.
- **Homework sheet:** A simple "Shadow Diary" template for the follow-up task (draw your shadow at 3 times of day). One side instructions, one side recording space.
- **Parent-facing summary:** A one-paragraph note for the homework folder: "This half term we are learning about Light and Shadows. Your child should be able to explain that we need light to see and that shadows form when light is blocked. You can help by: looking for shadows on a sunny day, talking about light sources at home, asking 'Why can you see that?' about everyday objects."
- **Working wall display:** Key vocabulary, investigation photos, class results — but this is built DURING the unit, not before it.

### What the Graph Could Realistically Generate

The graph has enough structured data to auto-generate the TEXT CONTENT for artefacts 1-3:
- Recording sheets: variable names, sentence stems from teaching guidance, vocabulary from concepts
- Word mats: vocabulary lists (needs definitions added), could generate syllable breakdowns
- Knowledge organisers: key facts from concept descriptions, vocabulary, prerequisite links

It CANNOT generate:
- Visual layout / design (needs a template engine)
- Images / photographs / diagrams (needs an image library or generation)
- Differentiated versions (needs DifficultyLevel data for Science)
- Presentation slides (needs slide generation tooling + images)
- Physical card designs (needs print-ready PDF generation)

### Gap Summary

| Artefact | Graph Can Provide Text? | Graph Can Provide Layout? | Graph Can Provide Images? | Missing Data |
|---|---|---|---|---|
| Recording sheets | Partially (variables, stems) | No | No | Differentiated versions, Y3-appropriate format |
| Word mats | Words only, no definitions | No | No | Definitions, syllable breakdowns, pictures |
| Knowledge organisers | Yes (concepts, facts, vocab) | No | No | Synthesised single-page format |
| Presentation slides | Partially (questions, prompts) | No | No | Images, visual examples, slide structure |
| Sorting cards | Categories from teaching guidance | No | No | Images, print-ready format |

**The gap between "lesson plan" and "ready to teach" is primarily a PRODUCTION gap, not a CONTENT gap.** The graph knows what should be on each artefact. It cannot produce the artefact itself. A template engine that reads graph data and outputs formatted, printable resources would close 70% of this gap. The remaining 30% is images/diagrams, which needs either a curated image library or generative AI.

---

*Ms. Chen, Y3 Science, Sheffield — 2026-02-23*
