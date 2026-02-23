# V6 Group Report: Can Claude Teach From This Graph?

**Synthesis of three full-curriculum evaluations (Years 3, 4, 5)**
**Date:** 2026-02-23

| Reviewer | Year | Experience | School Context |
|---|---|---|---|
| Ms Rachel Chen | Year 3 | 9 years | Two-form entry primary, Bristol |
| Mr David Okafor | Year 4 | 12 years | Inner-city London |
| Ms Sarah Brennan | Year 5 | 11 years | (not specified) |

**Central question:** If Claude had ONLY this graph data, could it sit with a child and actually TEACH them?

**Bottom-line answer:** Not yet for most subjects. The graph is an exceptional curriculum map (~8.5/10) but an incomplete teaching system (~5.2/10). The path to 8/10 is clear and achievable.

---

## 1. Cross-Year Rating Table

### Subject Ratings by Year Group

| Subject | Y3 (Chen) | Y4 (Okafor) | Y5 (Brennan) | **Average** |
|---|---|---|---|---|
| **English** | 4.6 | 6.0 | 7.8 | **6.1** |
| **Mathematics** | 5.6 | 4.8 | 6.2 | **5.5** |
| **Science** | 4.7 | 6.8 | 7.2 | **6.2** |
| **History** | 4.1 | 6.8 | 6.8 | **5.9** |
| **Geography** | 3.4 | 5.0 | 5.8 | **4.7** |
| Computing | 3.6 | 5.6 | 6.8 | **5.3** |
| D&T | 2.0 | 5.0 | 5.8 | **4.3** |
| Languages | 3.0 | 4.4 | 5.2 | **4.2** |
| Art & Design | 2.0 | 4.4 | 4.8 | **3.7** |
| Music | 2.0 | 4.4 | 4.6 | **3.7** |
| PE | 1.2 | 2.6 | 3.6 | **2.5** |
| **OVERALL** | **4.1** | **5.1** | **6.3** | **5.2** |

### Dimension Ratings Across All Subjects

| Dimension | Y3 (Chen) | Y4 (Okafor) | Y5 (Brennan) | **Average** |
|---|---|---|---|---|
| **Connect** | 5.6 | 6.5 | 7.0 | **6.4** |
| **Respond to Error** | 4.7 | 5.7 | 6.2 | **5.5** |
| **Model** | 4.3 | 4.8 | 5.8 | **5.0** |
| **Scaffold** | 3.6 | 4.4 | 5.4 | **4.5** |
| **Hand Over** | 2.5 | 3.9 | 5.0 | **3.8** |

### Key Findings

**Strongest subject: Science (6.2 avg).** Rich misconception data, Content Vehicle investigation structures, and Working Scientifically skill links give Claude the closest thing to a complete lesson plan.

**Weakest core subject: Geography (4.7 avg).** ~40% statutory content missing from vehicles. Sparse scaffolding within concepts. Needs maps and data that the graph cannot currently provide.

**Strongest dimension: Connect (6.4 avg).** The graph's prerequisites, CO_TEACHES, and cross-domain links are unanimously praised as the best feature. All three teachers said the prerequisite mapping is more thorough than any published scheme they've used.

**Weakest dimension: Hand Over (3.8 avg).** The graph tells Claude WHAT to teach and WHAT errors to look for, but almost never tells Claude WHEN THE CHILD IS READY TO TRY ALONE. This is the single biggest consensus gap.

**Notable pattern:** Scores increase from Y3 to Y5. This likely reflects two factors: (1) Y5 English benefits from year-level precision and assessment domain codes; (2) Brennan may rate more generously than Chen. The trend is consistent across subjects, so it may also reflect that Y5 content is more naturally text-teachable (more abstract, less concrete-manipulative).

---

## 2. Consensus: What Claude CAN Teach Today

All three teachers agree Claude could deliver meaningful teaching in these areas **right now**:

### A. Error Diagnosis and Misconception Response (All Subjects)

Unanimous verdict: the `common_misconceptions` property is the graph's single most valuable teaching asset.

- Chen: "The misconceptions data is teacher-quality... what I see in my marking every single day"
- Okafor: "Better than most published schemes... in 12 years of teaching"
- Brennan: "Specific, actionable, evidence-based"

Claude can already diagnose common errors in real time. If a Y3 child writes 355 for 352 - 7, the graph tells Claude exactly what happened (subtracted smaller from larger regardless of position) and implies the correction. This works across Maths, Science, English, and History.

### B. Concept Connection and Navigation (All Subjects)

The prerequisite chains, CO_TEACHES relationships, and cross-domain links let Claude say things like:
- "Remember when we learned about place value? Columnar addition uses those same columns..."
- "You've been reading fairy stories — now let's use those story structures in your own writing"
- "The variables in your science investigation use the same measuring skills as in maths"

All three teachers rated Connect as the strongest dimension by a clear margin.

### C. Science Investigation Lessons (Y4-Y5)

Brennan rated Science forces at 8/10 — the highest single-lesson score across all three reviews. The combination of Content Vehicle (equipment, variables, expected outcomes) + misconceptions ("heavier objects fall faster") + ThinkingLens ("If... then... because...") + Working Scientifically skills gives Claude a near-complete investigation lesson. Okafor concurred, rating Science 6.8/10 overall and calling it "the most teachable subject from this data."

### D. English Grammar and VGP (Y4-Y5)

Okafor rated fronted adverbials at 6/10 as a concept Claude could teach using the explicit grammar rules + misconception data + Claude's own linguistic capability. Brennan rated English overall at 7.8/10 — the highest subject score across all three reviews — because the combination of fine-grained concept descriptions, assessment domain codes, and Content Vehicles gives Claude a solid foundation.

### E. History Through Content Vehicles (Y4-Y5)

Where Content Vehicles exist, History transforms. Okafor: "The 12 History vehicles are outstanding: specific historical sources, named key figures, multiple perspectives... Claude could plausibly lead a Year 4 child through a historical enquiry using these vehicles."

### F. Revision, Quizzing, and Explanation

All three agree Claude could serve as an excellent revision partner and explanation engine TODAY — quizzing children, correcting errors using misconception data, and making connections between topics. The gap is in primary teaching (modelling, scaffolding, handover), not in supporting learning.

---

## 3. Consensus: Where Claude CANNOT Teach

All three teachers agree on five critical gaps, mapped to the five teaching dimensions:

### Gap 1: No Worked Examples (kills MODEL)

**All three teachers independently identified this as the single most impactful missing element.**

- Chen: "The graph says 'teach columnar addition using CPA progression' but never shows one being worked through step by step"
- Okafor: "Teaching Maths IS modelling worked examples. This single gap drops Maths MODEL from what could be 7/10 to 3/10"
- Brennan: "The absence of worked examples is like sending a teacher into a lesson without a whiteboard"

The `worked_example_set` vehicle type exists in the schema but contains no actual worked examples. Claude has to generate ALL step-by-step procedures from concept descriptions alone.

### Gap 2: No Difficulty Sub-Levels Within Concepts (kills SCAFFOLD)

Every concept has a single complexity rating (1-4) but no internal gradient.

- Chen: "Without this progression, Claude can't START EASY when a child is struggling. It has one undifferentiated blob of 'columnar addition'"
- Okafor: "All Y4 concepts are complexity 2 — Claude has no way to differentiate between a child who needs Level 1 and a child ready for Level 5"
- Brennan: "Claude cannot distinguish 'multiply 2-digit by 1-digit' from 'multiply 4-digit by 2-digit' within the same concept"

### Gap 3: No Handover Criteria (kills HAND OVER)

The weakest dimension across all three reviews (avg 3.8/10).

- Chen: "There is no concept of 'success at this level looks like...' expressed as observable child behaviour"
- Okafor: "Success criteria are summative endpoints, not formative handover signals"
- Brennan: "No rubric or exemplar responses showing what a 'good enough' answer looks like at Y5 level"

The graph tells Claude what mastery is but not what readiness-for-independence looks like mid-lesson.

### Gap 4: No Content to Teach WITH (limits all dimensions)

- No text passages for English (the graph says "use fairy stories" but doesn't provide any)
- No problem sets for Maths (describes methods but provides no numbers to practise with)
- No images, diagrams, or visual models for Science
- No primary source materials for History (names "Vindolanda tablets" but doesn't provide them)
- No vocabulary lists for Languages (describes "the target language" without specifying which)

Content Vehicles partially fill this for History and Science, but even they describe resources rather than providing them.

### Gap 5: ThinkingLens Prompts Are Age-Agnostic (limits MODEL for younger years)

- Okafor: "'Trace feedback loops' is meaningless to a Year 1 child and insultingly simple for a Year 9 pupil"
- Brennan: "Some lens rationale text is written at adult academic level... 'Decomposition requires pupils to model a complex problem as a system of smaller interacting parts'"

The AI instruction prompts are identical whether applied to KS1 or KS4. All three teachers' data shows this — Chen's Y3 ratings are systematically lower partly because the ThinkingLens framing is pitched too high.

---

## 4. The Expressive Framework Proposal

Synthesising all three teachers' schema proposals into a single coherent design. Where two teachers proposed the same concept differently, the reconciled version takes the strongest elements of each.

### Priority 1: `WorkedExample` Nodes

**All three teachers' #1 recommendation. Highest impact, most achievable.**

```
(:Concept)-[:HAS_WORKED_EXAMPLE]->(:WorkedExample)
(:WorkedExample)-[:NEXT_DIFFICULTY]->(:WorkedExample)
```

| Property | Type | Source | Description |
|---|---|---|---|
| `example_id` | string | All three | e.g. `MA-Y4-WE003` |
| `difficulty` | int (1-5) | All three | Within-concept difficulty level |
| `problem_statement` | string | All three | The question or task |
| `solution_steps` | object[] | Chen + Brennan | `{step, action, display, say}` — what to do and what to say at each step |
| `common_error_at_step` | object | Okafor + Brennan | `{step_number: error_description}` — what could go wrong here |
| `pupil_input_point` | int | Brennan | Which step to pause and ask "What would you do next?" |
| `variation_prompts` | string[] | Chen | "Now you try: {similar problem}" |
| `error_trap` | string | Chen | "If child says X, go to ErrorPattern Y" |
| `manipulative` | string | Okafor | Concrete resource (Dienes blocks, fraction wall) |
| `representation` | string | Okafor | Pictorial representation (bar model, number line) |
| `cpa_stage` | string | Brennan | `concrete`, `pictorial`, or `abstract` |

**Reconciliation notes:**
- Chen attached worked examples to DifficultyLevel nodes; Okafor and Brennan attached them directly to Concepts. **Decision: attach to Concept**, with the `difficulty` property and `NEXT_DIFFICULTY` chain providing the internal progression. Simpler graph, same expressiveness.
- Chen's `dialogue_template` with variables and Okafor's `teacher_narration[]` serve the same purpose. **Decision: use `solution_steps` as object array** with both `action` (what happens) and `say` (what Claude says), per Chen's schema.

**Scope estimate:** 5-8 examples per Maths concept, 3-5 per English grammar concept, 2-3 per Science investigation. ~100-150 for each year group. LLM-generatable with teacher review.

### Priority 2: `DifficultyLevel` Sub-Nodes

**All three teachers' #2 recommendation. Gives Claude the scaffolding ladder.**

```
(:Concept)-[:HAS_DIFFICULTY_LEVEL]->(:DifficultyLevel)
```

| Property | Type | Source | Description |
|---|---|---|---|
| `level_id` | string | Chen | e.g. `MA-Y3-C014-DL003` |
| `level_number` | int (1-5) | All three | 1 = entry, 5 = mastery/extension |
| `description` | string | All three | What this level looks like |
| `example_task` | string | Okafor + Brennan | A representative task at this level |
| `entry_check` | string | Chen | "Can the child do Level N-1?" |
| `handover_signal` | string | Chen | "Child completes 3 consecutive at this level without error" |
| `common_errors_at_level` | string[] | Chen | Level-specific errors |

**Reconciliation notes:**
- Brennan proposed this as a JSON array property on Concept nodes rather than separate nodes. **Decision: separate nodes.** The `handover_signal` and `common_errors_at_level` make these rich enough to warrant their own nodes, and WorkedExample nodes can link to specific difficulty levels.
- Chen's `scaffold_if_stuck` property merges well with the entry_check — if a child fails the entry check, drop to the previous level.

**Scope estimate:** 3-5 levels per concept. For core subjects (~40 concepts per year), that's ~150-200 DifficultyLevel nodes per year group.

### Priority 3: Diagnostic Items (Reconciled from Chen's ErrorPattern + Okafor's DiagnosticQuestion)

**Chen and Okafor proposed overlapping but complementary structures. Reconciled into a single `DiagnosticItem` node type.**

```
(:Concept)-[:HAS_DIAGNOSTIC]->(:DiagnosticItem)
```

| Property | Type | Source | Description |
|---|---|---|---|
| `diagnostic_id` | string | Both | e.g. `MA-Y4-DQ007` |
| `diagnostic_type` | string | Reconciled | `proactive` (question to test for misconception) or `reactive` (triggered by observed error) |
| `trigger` | string | Chen | What the child does/says that activates this (for reactive type) |
| `question_text` | string | Okafor | The diagnostic question (for proactive type) |
| `correct_response` | string | Okafor | Expected correct answer |
| `distractor_responses` | object[] | Okafor | `{answer, misconception, intervention}` |
| `diagnosis` | string | Chen | What the error means pedagogically |
| `correction_move` | string | Chen | What Claude should say/do in response |
| `severity` | string | Chen | `conceptual`, `procedural`, or `careless` |
| `follow_up` | string | Chen | What to give the child next |
| `difficulty` | int (1-5) | Okafor | Maps to DifficultyLevel |

**Reconciliation notes:**
- Chen's ErrorPattern is reactive ("if child does X, respond with Y"). Okafor's DiagnosticQuestion is proactive ("ask X to check for misconception Y"). Both are needed. The `diagnostic_type` property distinguishes them within a single node type.
- The existing `common_misconceptions` text property on Concepts is the RAW MATERIAL for generating these nodes. Each misconception could spawn 2-3 DiagnosticItems.

**Scope estimate:** 2-4 items per key misconception. Top 20 misconceptions per year × 3 items each = ~60 nodes per year group.

### Priority 4: Handover Criteria on ConceptCluster

**Chen proposed a separate node; Okafor proposed properties on ConceptCluster. Decision: properties on ConceptCluster** (simpler, and clusters already group the teaching sequence).

Add to existing `ConceptCluster` nodes:

| Property | Type | Source | Description |
|---|---|---|---|
| `readiness_signals` | string[] | Chen + Okafor | Observable signs the child is ready for independence |
| `not_ready_indicators` | string[] | Chen | What looks like readiness but isn't |
| `independence_task` | string | Okafor | A task to confirm readiness |
| `common_false_readiness` | string | Okafor | What to watch for (e.g. "recall without understanding") |
| `success_threshold` | string | Chen | e.g. "3 consecutive correct with verbal explanation" |

**Scope estimate:** One set of properties per ConceptCluster. 626 existing clusters, but properties could be added incrementally starting with core Maths and English.

### Priority 5: `ModelResponse` Exemplar Nodes (Brennan)

**Unique to Brennan, but addresses a gap all three identified: Claude doesn't know what a "good enough" Y-level answer looks like.**

```
(:Concept)-[:HAS_MODEL_RESPONSE]->(:ModelResponse)
```

| Property | Type | Description |
|---|---|---|
| `response_id` | string | e.g. `EN-Y5-MR001` |
| `question` | string | The question or prompt |
| `exemplar_response` | string | What a good Y-level answer looks like |
| `response_level` | string | `below_expected`, `expected`, `exceeding` |
| `assessment_domain` | string | Links to ContentDomainCode |
| `features_demonstrated` | string[] | What makes this answer good |

**Scope estimate:** 2-3 exemplars per English/Science concept (expected + exceeding). ~50-80 per year group.

### Priority 6: Age-Banded ThinkingLens Prompts (Okafor, confirmed by Brennan)

Add key-stage-specific AI instruction variants to the `APPLIES_LENS` relationship or the `ThinkingLens` node:

| Property | Type | Description |
|---|---|---|
| `agent_prompt_ks1` | string | AI instruction calibrated for ages 5-7 |
| `agent_prompt_ks2` | string | AI instruction calibrated for ages 7-11 |
| `agent_prompt_ks3` | string | AI instruction calibrated for ages 11-14 |

**Scope estimate:** 3 variants × 10 lenses = 30 text entries. Small effort, significant impact on younger year groups.

### Priority 7: `ConcreteResource` Nodes (Okafor)

```
(:ContentVehicle)-[:USES_RESOURCE]->(:ConcreteResource)
(:Concept)-[:HAS_RESOURCE]->(:ConcreteResource)
```

| Property | Type | Description |
|---|---|---|
| `resource_id` | string | e.g. `EN-Y4-RES001` |
| `resource_type` | string | `text_passage`, `data_set`, `word_list`, `map_description`, `image_description` |
| `content` | string | The actual text, data, or description |
| `reading_level` | string | Year-group calibrated |
| `source` | string | Attribution |

**Scope estimate:** This is the largest effort. 3-5 resources per Content Vehicle × ~60 vehicles = ~200-300 nodes. But even 20-30 high-quality text passages for English would be transformative.

### Summary: Effort vs Impact

| Priority | Addition | Impact | Effort | Changes Score By |
|---|---|---|---|---|
| 1 | WorkedExample nodes | Transforms Maths MODEL | Medium (LLM-generatable) | +1.5-2.0 on Maths |
| 2 | DifficultyLevel sub-nodes | Transforms SCAFFOLD across all | Medium-High | +1.0-1.5 on all subjects |
| 3 | DiagnosticItem nodes | Makes misconceptions actionable | Medium | +0.5-1.0 on RESPOND |
| 4 | Handover criteria on clusters | Gives Claude independence signals | Low | +1.0-1.5 on HAND OVER |
| 5 | ModelResponse exemplars | Calibrates Claude's expectations | Low-Medium | +0.5-1.0 on HAND OVER |
| 6 | Age-banded ThinkingLens | Fixes KS1-KS2 age gap | Low | +0.5 on Y3-Y4 MODEL |
| 7 | ConcreteResource nodes | Gives Claude content to teach WITH | High | +1.0 on English, Geography |

---

## 5. The Two-Tier Model

Brennan identified a clear split between subjects Claude can primary-teach (Tier A) and subjects where it should serve as a knowledge companion (Tier B). **All three teachers' data strongly support this split.**

### Tier A: Claude as Primary Instructor

Subjects where Claude can lead learning with the current graph + proposed additions.

| Subject | Y3 | Y4 | Y5 | Avg | Why Tier A |
|---|---|---|---|---|---|
| English | 4.6 | 6.0 | 7.8 | 6.1 | Rich concept descriptions, assessment domain codes, misconceptions. Claude's own linguistic capability supplements the graph. |
| Science | 4.7 | 6.8 | 7.2 | 6.2 | Content Vehicle investigations, misconception data, ThinkingLens framing, Working Scientifically skills. Strongest teaching readiness. |
| Mathematics | 5.6 | 4.8 | 6.2 | 5.5 | Excellent prerequisites and misconceptions. Currently limited by missing worked examples, but this is the most fixable gap. |
| History | 4.1 | 6.8 | 6.8 | 5.9 | Content Vehicles with sources, perspectives, and key figures transform this subject. Where vehicles exist, teaching readiness is high. |
| Computing | 3.6 | 5.6 | 6.8 | 5.3 | Inherently suited to text-based AI teaching. Content is digital, assessment can be interactive, Claude can reason about code. |

**Tier A threshold:** With the Priority 1-4 additions (worked examples, difficulty levels, diagnostic items, handover criteria), all five subjects would score **7.0+ / 10** — the point where all three teachers said "yes, Claude could genuinely teach from this."

### Tier B: Claude as Knowledge Companion

Subjects where Claude should support learning but not attempt to be the primary instructor.

| Subject | Y3 | Y4 | Y5 | Avg | What Claude CAN Do | What Claude CANNOT Do |
|---|---|---|---|---|---|---|
| Geography | 3.4 | 5.0 | 5.8 | 4.7 | Teach locational knowledge, explain physical processes, discuss human geography | Show maps, conduct fieldwork, teach grid references interactively |
| D&T | 2.0 | 5.0 | 5.8 | 4.3 | Support design briefs, teach evaluation skills, explain materials science, teach computing control | Demonstrate cutting/joining, guide physical making, assess products |
| Languages | 3.0 | 4.4 | 5.2 | 4.2 | Teach grammar concepts, vocabulary practice, language awareness | The graph is language-agnostic — no French/Spanish/German content |
| Art & Design | 2.0 | 4.4 | 4.8 | 3.7 | Teach art history, critical appreciation, design principles | Demonstrate technique, evaluate visual work, guide physical practice |
| Music | 2.0 | 4.4 | 4.6 | 3.7 | Teach music theory, notation reading, music history, composition concepts | Play instruments, demonstrate rhythm, assess performance, produce sound |
| PE | 1.2 | 2.6 | 3.6 | 2.5 | Teach sports science, tactical theory, health knowledge, growth mindset | Demonstrate movement, correct physical technique, assess performance |

**Key insight from all three teachers:** Tier B limitations are NOT data quality problems. The Art and Music concept descriptions are well-written; the DT teaching guidance is thorough. The limitation is fundamental: these subjects require sensory modalities (visual demonstration, auditory feedback, physical manipulation) that a text-based AI cannot deliver.

**Design implication:** For Tier B subjects, the graph should focus on encoding the KNOWLEDGE dimension (art history, music theory, design principles, sports science) and explicitly flag the PRACTICAL dimensions as requiring human instruction or specialist tools (video, audio, physical materials).

---

## 6. Three Before-and-After Examples

### Example 1: Where the Gap is Widest — Maths Columnar Addition (Y3)

**TODAY (from Chen, Y3, 347 + 286):**

> "Today we're going to learn about formal columnar addition. This means adding numbers by writing them in columns — ones under ones, tens under tens, hundreds under hundreds. When a column adds up to more than 9, we carry the extra into the next column. Let's try 347 + 286. Can you set up the columns?"

This is a DESCRIPTION of the method. It's telling, not teaching. Claude knows the concept, the misconception, and the vocabulary — but it doesn't know how to walk a child through the actual doing of it.

**WITH the Expressive Framework:**

> I'm going to show you how I add these big numbers. Watch what I do.
>
> *[Shows: 347 + 286]*
>
> I always start on the right — the ones column. 7 and 6... I know 7 + 6 = 13. But 13 is too big for one column! 13 is the same as 1 ten and 3 ones. So I write 3 in the ones answer... and carry this little 1 up to the tens column. Can you see it?
>
> Now the tens. 4 tens and 8 tens makes 12 tens. But wait — I need to add the 1 I carried! 12 + 1 = 13 tens. Same thing — too big. 13 tens = 1 hundred and 3 tens. Write 3, carry 1.
>
> Last one: hundreds. 3 + 2 = 5, plus my carried 1 = 6. Write 6.
>
> My answer is 633. Quick check: 350 + 300 is about 650. 633 is close. That makes sense.
>
> Now — your turn. Try 258 + 374. Talk me through each step the way I just did.

Then, when the child writes 522 (forgetting the carried ten), Claude matches to DiagnosticItem and responds:

> Hmm, let me look at your tens column. You wrote 5 + 7 = 12, so you wrote 2 and carried 1. But did you add the 1 you carried from the ones column? Let's look at that step again together.

**The difference:** The graph currently provides the *what* (columnar addition), the *why* (place value), and the *watch-out* (forgetting to carry). The framework additions provide the *how* (step-by-step narration), the *respond* (specific error → specific correction), and the *hand over* (3 consecutive correct with verbal explanation).

### Example 2: Where the Graph is Already Strong — Science Forces (Y5)

**TODAY (from Brennan, Y5, gravity and friction):**

> Here's a puzzle: I drop a feather and a marble at the same time from the same height. Which hits the ground first? What do you think, and why?
>
> *[Child: "The marble because it's heavier!"]*
>
> That's what a lot of people think. Let me tell you something surprising — if there were no air, they'd hit at exactly the same time. Gravity pulls on everything equally. The feather is slower because of something else — air resistance pushes against it.
>
> *[ThinkingLens: Cause and Effect]* Let's think about cause and effect: IF we removed the air, THEN what would happen? BECAUSE...
>
> Now, we're going to investigate friction. Here's what we need: a toy car, a ramp, and three different surfaces. To make it a fair test, what do we need to keep the same?

This ALREADY WORKS because the graph provides: misconception data ("heavier objects fall faster"), Content Vehicle investigation structure (variables, equipment, expected outcomes), ThinkingLens framing ("If... then... because..."), and Working Scientifically skill links. Brennan rated this at 8/10 — the highest single-lesson score across all three reviews.

**WITH the Expressive Framework, it would gain:**

- Difficulty sub-levels: start with "identify forces" (Level 1) → "predict force effects" (Level 3) → "explain using particle model" (Level 5)
- Diagnostic items: if child says "friction always slows things down", trigger reactive diagnostic with shoe-grip counter-example
- Handover signal: "Child can plan a fair test identifying all three variable types without scaffolding"

**The difference:** The current graph gets Science to 8/10 for a single concept lesson. The framework additions would make this consistent across ALL science concepts and give Claude the scaffolding ladder to adapt in real time.

### Example 3: Where Content is the Bottleneck — English Reading Inference (Y3)

**TODAY (from Chen, Y3, drawing inferences):**

> Today we're going to practise drawing inferences. An inference is when you read between the lines — you use clues in the text and what you already know to work out something the author hasn't said directly. For example, if the text says a character 'slammed the door and threw their bag on the floor', we can infer they are angry. Let's look at this passage and see what inferences we can draw.

But Claude has no passage. The graph says "use the PEE structure" but provides no text to apply it to.

**WITH the Expressive Framework (including ConcreteResource nodes):**

> *[Presents a short passage, graded for Y3 reading level]*
>
> Listen to this bit: "Maya pushed her cereal around the bowl. She kept glancing at the clock on the wall."
>
> I'm going to show you how I read between the lines. The author doesn't SAY Maya is worried about being late. But look at the clues: she's not eating — she's pushing her cereal around. And she keeps looking at the clock. Why would someone keep looking at a clock?
>
> So my inference is: Maya is worried about being late for something. My evidence is the clock-watching and the not eating.
>
> Now you try: "On the bus, Maya sat at the back and stared out the window. She didn't talk to Anya, even when Anya said hello."
>
> What can you infer about how Maya is feeling? Remember — Point, Evidence, Explain.

Then Claude checks against the ModelResponse exemplar:

> *Expected Y3 response: "I think Maya is feeling upset or worried because the text says she 'stared out the window' and 'didn't talk to Anya.' When someone doesn't talk to their friend, it usually means something is bothering them." (30 words, inference + evidence + explanation)*

**The difference:** The current graph gives Claude the teaching STRATEGY (PEE structure, inference vs retrieval, misconceptions about opinion vs inference). The framework additions give Claude the teaching MATERIALS (passages to read, model answers to benchmark against) and the teaching MOVES (model an inference, then hand over to the child).

---

## 7. The Path to 8/10

Current average across three teachers: **5.2/10**. Target: **8.0/10**.

The gap is 2.8 points. Here is how to close it, in priority order:

### Step 1: Add WorkedExample Nodes for Maths and English (Impact: +1.5 points)

**What:** 5-8 worked examples per Maths concept, 3-5 per English grammar concept, per year group. Each with step-by-step solution, teacher narration, common errors at each step, and variation prompts.

**Why highest priority:** This is the single addition all three teachers named first. Maths scores jump from ~5.5 to ~7.0 when Claude can say "Watch me do this step by step" instead of "The method involves exchanging."

**How:** LLM-generatable from existing concept descriptions + misconception data. Teacher review for accuracy. Estimated: 100-150 examples per year group, ~2 weeks of generation + 1 week of review.

**Score impact:** Maths MODEL +2, English MODEL +1, Science MODEL +0.5. Overall: +1.5.

### Step 2: Add DifficultyLevel Sub-Nodes (Impact: +1.0 points)

**What:** 3-5 difficulty levels per concept with description, example task, entry criteria, and handover signal.

**Why:** Gives Claude the scaffolding ladder. Currently it has a flat landscape — one difficulty level per concept. With sub-levels, Claude can start where the child is and move up or down.

**How:** Teacher-authored for core concepts (Maths has the clearest difficulty gradients), LLM-assisted for others. Estimated: 150-200 per year group, ~1 week per subject.

**Score impact:** SCAFFOLD +1.5 across all subjects. Overall: +1.0.

### Step 3: Add Handover Criteria to ConceptClusters (Impact: +0.5 points)

**What:** `readiness_signals`, `not_ready_indicators`, `independence_task`, and `success_threshold` properties on every ConceptCluster.

**Why:** Addresses the weakest dimension (3.8/10). Low effort — properties on existing nodes, not new node types.

**How:** Teacher-authored, 1-2 sentences per property per cluster. Start with Maths and English clusters. Estimated: 2-3 days for 100 priority clusters.

**Score impact:** HAND OVER +1.5. Overall: +0.5.

### Step 4: Add DiagnosticItem Nodes (Impact: +0.5 points)

**What:** Structured misconception → question → distractor → intervention chains for the top 20 misconceptions per year group.

**Why:** Makes the excellent misconception data machine-actionable. Currently Claude must parse prose to extract what to do; DiagnosticItems give it structured decision trees.

**How:** Derived from existing `common_misconceptions` text. LLM-extractable with teacher validation. Estimated: 60-80 per year group, ~1 week.

**Score impact:** RESPOND +1.0. Overall: +0.5.

### Step 5: Age-Band the ThinkingLens Prompts (Impact: +0.3 points)

**What:** Three variants of `agent_prompt` per ThinkingLens node (KS1, KS2, KS3).

**Why:** Low effort, immediate impact on Y3-Y4 where current prompts are too abstract.

**How:** Rewrite 10 prompts × 3 key stages = 30 text entries. Half a day's work.

**Score impact:** MODEL +0.5 for Y3-Y4. Overall: +0.3.

### Cumulative Impact

| Step | Addition | Effort | Cumulative Score |
|---|---|---|---|
| Baseline | Current graph | — | 5.2 |
| Step 1 | WorkedExample nodes | 3 weeks | 6.7 |
| Step 2 | DifficultyLevel sub-nodes | 2 weeks | 7.7 |
| Step 3 | Handover criteria | 3 days | 8.2 |
| Step 4 | DiagnosticItem nodes | 1 week | 8.7 |
| Step 5 | Age-banded ThinkingLens | 1 day | 9.0 |

**Note on Tier A vs Tier B:** These scores apply to Tier A subjects (English, Maths, Science, History, Computing). Tier B subjects (Art, Music, PE, DT, Geography, Languages) are constrained by medium, not by data. Their ceiling is ~6/10 regardless of graph additions — and that's fine. For Tier B subjects, Claude should be a knowledge companion, not a primary instructor.

### What NOT to Build

Three things that might seem logical but would be wasted effort:

1. **Don't add worked examples for Art, Music, or PE.** The limitation is physical, not informational. A perfectly described brushstroke technique still can't be taught through text.

2. **Don't try to make the graph replace Claude's general knowledge.** Okafor's key insight: "The optimal architecture is graph data + Claude's general knowledge, not graph data alone." The graph should encode what Claude CAN'T know on its own (curriculum sequencing, UK-specific misconceptions, age-appropriate calibration) and let Claude supply what it already knows (how to explain fractions, what a fronted adverbial is, how photosynthesis works).

3. **Don't add ConcreteResource nodes before WorkedExamples and DifficultyLevels.** Text passages and data sets (Priority 7) are valuable but less impactful than the structural additions (Priorities 1-4). A worked example with no text passage is still useful. A text passage with no difficulty gradient wastes half its potential.

---

## Appendix: Data Quality Issues Across All Three Reviews

### Issues Confirmed by Multiple Teachers

| Issue | Reported By | Status |
|---|---|---|
| No worked examples despite `worked_example_set` vehicle type | All three | **Unfixed — highest priority** |
| ThinkingLens rationales age-inappropriate for KS1/KS2 | Okafor + Brennan (Chen's low scores imply same) | **Unfixed — flagged in V5, partially addressed** |
| ~40% Geography statutory content missing from vehicles | Okafor + Brennan | **Unfixed** |
| Science domains are KS-wide, not year-specific | Chen + Brennan | **By design but limits year-specific teaching** |
| History/Geography concepts too coarse-grained | Chen | **Structural — would require extraction rework** |
| Thinking Lens rationales template-duplicated across clusters | Chen (explicit) + Brennan (implicit) | **Partially fixed in V5** |

### Issues Reported by Single Teacher

| Issue | Reported By | Assessment |
|---|---|---|
| EN-Y3 Spoken Language prerequisite anomaly (phonics → spoken language) | Chen | **Valid — prerequisites are pedagogically incorrect** |
| Foundation subjects have zero Content Vehicles | Okafor | **By design for now — Tier B subjects** |
| Learner Profile is "KS2 from Y3" but Y5 metacognition is more developed | Brennan | **Valid — profile could benefit from year-level variants** |
| Languages are language-agnostic (no French/Spanish/German content) | Okafor + Brennan | **By design — but limits teachability** |

---

*Report synthesised 2026-02-23 from three independent teacher evaluations.*
*The graph is an outstanding curriculum map. The path from curriculum map to teaching system requires five concrete additions, prioritised above. Steps 1-3 alone would cross the 8/10 threshold for Tier A subjects.*
