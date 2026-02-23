# V6 Teacher Review: Year 4 Curriculum Context Evaluation

**Reviewer:** Mr David Okafor, Year 4 Class Teacher (12 years' experience, inner-city London)
**Date:** 2026-02-23
**File evaluated:** `generated/teachers-v5/y4/context.md` (763KB, ~6500 lines)
**Central question:** If an AI — Claude — had ONLY this graph data, could it sit with a Year 4 child and actually TEACH them?

---

## 1. Subject-by-Subject Ratings

Each subject is rated 1-10 across five dimensions:

| Dimension | What it means |
|---|---|
| **MODEL** | Can Claude show step-by-step thinking? Demonstrate a procedure? Think aloud? |
| **SCAFFOLD** | Can Claude start easy and get harder? Simplify when a child is stuck? |
| **HAND OVER** | Can Claude tell when the child is ready to work independently? |
| **RESPOND** | Can Claude diagnose what went wrong when a child makes an error? |
| **CONNECT** | Can Claude link this to what the child already knows and to other subjects? |

### Core Subjects

| Subject | MODEL | SCAFFOLD | HAND OVER | RESPOND | CONNECT | Avg | Notes |
|---|---|---|---|---|---|---|---|
| **English** | 6 | 5 | 5 | 7 | 7 | **6.0** | Grammar/VGP modelling possible; no actual text passages to read |
| **Mathematics** | 3 | 4 | 4 | 6 | 7 | **4.8** | Critical gap: no worked examples, no step-by-step procedures |
| **Science** | 7 | 6 | 5 | 8 | 8 | **6.8** | Strongest misconception data; investigation vehicles structure well |
| **History** | 7 | 6 | 6 | 7 | 8 | **6.8** | Content vehicles are excellent; rich source material |
| **Geography** | 5 | 4 | 3 | 6 | 7 | **5.0** | No content vehicles; ~40% statutory content missing |

### Foundation Subjects

| Subject | MODEL | SCAFFOLD | HAND OVER | RESPOND | CONNECT | Avg | Notes |
|---|---|---|---|---|---|---|---|
| **Art & Design** | 4 | 4 | 3 | 5 | 6 | **4.4** | Concepts rich but Claude cannot demonstrate physical techniques |
| **Music** | 4 | 4 | 3 | 5 | 6 | **4.4** | Cannot model performance; composition/notation partially possible |
| **Design & Tech** | 5 | 4 | 4 | 5 | 7 | **5.0** | Can support design/evaluate; cannot support hands-on making |
| **Computing** | 6 | 5 | 5 | 6 | 6 | **5.6** | Best foundation fit for AI — algorithms are textual/logical |
| **Languages** | 4 | 4 | 3 | 5 | 6 | **4.4** | Generic "target language" — no French/Spanish-specific data |
| **Physical Education** | 2 | 2 | 2 | 3 | 4 | **2.6** | Almost entirely physical; Claude cannot teach movement |

### Summary Statistics

| Metric | Value |
|---|---|
| **Overall average** | **5.1/10** |
| **Core subjects average** | **5.9/10** |
| **Foundation subjects average** | **4.4/10** |
| **Highest rated** | Science (6.8), History (6.8) |
| **Lowest rated** | PE (2.6), Art (4.4), Music (4.4), Languages (4.4) |
| **Weakest dimension across all** | HAND OVER (avg 3.9) |
| **Strongest dimension across all** | CONNECT (avg 6.5) |

---

## 2. Cross-Subject Patterns

### What the graph does well (and why it matters for teaching)

**Pattern 1: Misconception data is genuinely excellent.**
Every concept has specific, actionable misconceptions. These are not generic ("children find fractions hard") — they are precise ("children may think 1/4 > 1/3 because 4 > 3"; "pupils think plants get food from the soil"; "pupils conflate significance with fame"). In 12 years of teaching, the quality of these misconceptions is better than most published schemes. A teacher reading them would nod and say "yes, that exact thing happens in my class every year." Claude could use these to anticipate common errors and prepare responses. **Rating: 8/10 as a resource.**

**Pattern 2: Prerequisites and connections are the graph's superpower.**
The PREREQUISITE_OF chains are comprehensive: 1,354+ relationships spanning EYFS through KS4, including 34 cross-stage EYFS→KS1 links. CO_TEACHES relationships (1,827) map where concepts reinforce each other. Cross-subject links (Science↔Maths through measurement, History↔English through source reading, Geography↔Science through climate) are well-curated. This means Claude always knows where a concept sits in the learning journey and what it connects to. No published scheme I've used has prerequisite mapping this thorough. **Rating: 9/10.**

**Pattern 3: Content Vehicles transform History from "nice graph" to "usable teaching data."**
The 12 History vehicles are outstanding: specific historical sources (Vindolanda tablets, Sutton Hoo helmet, Benin Bronzes), named key figures, multiple perspectives (Roman coloniser, Briton, enslaved person), period dates, assessment questions, and success criteria. Claude could plausibly lead a Year 4 child through a historical enquiry using these vehicles. By contrast, subjects without vehicles (Geography, Art, Music, D&T, Computing, Languages, PE) drop sharply in teachability. **The vehicles are the difference between a curriculum map and a teaching resource.**

**Pattern 4: ThinkingLens provides good cognitive framing but is age-agnostic.**
Every ConceptCluster has 1-2 ThinkingLens assignments with AI instruction prompts. The rationale for each lens choice is thoughtful (e.g., "the water cycle is an archetypal system" → Systems lens). But the AI instruction text is identical whether applied to a KS1 concept or a KS4 concept. A prompt that says "prompt pupils to map the parts of a system and their connections, identify inputs and outputs, trace feedback loops" is appropriate for a Year 9 pupil but too abstract for a Year 4 child who needs "What are all the bits? What happens if we take one bit away?" **This needs age-banding.**

**Pattern 5: The graph is KS-level, not Year-level, for most foundation subjects.**
History is KS2 (ages 7-11). Geography is KS2. D&T is KS2. PE concepts are KS1. Languages are KS2. This means the graph cannot differentiate between what a Year 3 child and a Year 6 child should be learning within the same Key Stage. For English and Maths, the year-level precision is good (domains like EN-Y4-D001, MA-Y4-D001). For Science, some domains are year-specific (Plants = KS1/Y3), others span KS2. **This KS-level granularity makes it impossible for Claude to pitch teaching at exactly the right level for an 8-9 year old in History, Geography, D&T, Music, Art, Languages, or PE.**

### What the graph is missing (and why it kills teaching)

**Missing 1: No worked examples — and for Maths, this is fatal.**
The `worked_example_set` vehicle type exists in the schema but the V5 review already flagged this: there are no actual worked examples in any vehicle. Maths concept descriptions say things like "Teach column addition, progressing from no-exchange to exchange" but never show:
```
  347
+ 256
-----
Step 1: 7 + 6 = 13. Write 3, carry 1.
Step 2: 4 + 5 + 1 = 10. Write 0, carry 1.
Step 3: 3 + 2 + 1 = 6.
Answer: 603
```
Teaching Maths IS modelling worked examples. Without them, Claude is a textbook that describes fractions but never does one. This single gap drops Maths MODEL from what could be 7/10 to 3/10.

**Missing 2: No difficulty sub-levels within concepts.**
Every Year 4 concept has `complexity: 2` and `teaching_weight: 2`. There is no way for Claude to start easy and get harder. A real teacher teaching column addition starts with 2-digit + 2-digit (no exchange), then 2-digit + 2-digit (with exchange), then 3-digit + 3-digit (no exchange), then 3-digit + 3-digit (with exchange), then 4-digit. The graph has none of this progression. Similarly, a reading comprehension question about a simple text and a reading comprehension question about a complex text are both just "EN-Y4-C006 — Inference and Prediction" at complexity 2.

**Missing 3: No formative handover indicators.**
Success criteria on vehicles are summative: "Can pupils place the three ages (Stone, Bronze, Iron) in chronological order and explain what changed between them?" These tell you what mastery looks like at the END. They don't tell Claude WHEN to step back mid-lesson. A teacher knows to hand over when a child starts self-correcting, when they can explain their thinking back to you, when they attempt the next problem without asking. The graph has no "readiness for independence" signals.

**Missing 4: No concrete examples, texts, or problems.**
The concepts describe skills but provide no material to practise them on:
- Reading Comprehension says "teach inference" but provides no text passage to infer from
- Fractions says "compare fractions with different denominators" but provides no problems
- Spelling says "learn the common exception words" but doesn't list which words
- Science says "investigate light" but provides no experimental instructions
- Geography says "study climate zones" but provides no maps or data

Content Vehicles partially fill this for History and Science, but even they describe resources (Vindolanda tablets) rather than providing them.

**Missing 5: No structured diagnostic pathways.**
Misconceptions are listed but not structured for real-time diagnosis. A teacher doesn't just know that "children may subtract the smaller digit from the larger regardless of position" — they know that if a child writes 326 - 158 = 232, the child is doing this exact thing, and the intervention is to model exchange explicitly with Dienes blocks. The graph has the misconception but not the diagnosis-to-intervention chain.

**Missing 6: Foundation subjects have zero Content Vehicles.**
Art, Music, D&T, Computing, Languages, and PE all have detailed concept descriptions and teaching guidance but zero vehicles. This means zero assessment guidance, zero success criteria, zero teaching pack resources for these subjects. Combined with the inherent limitation that Claude cannot physically demonstrate Art, Music, D&T, and PE, this means the foundation subjects are essentially unteachable from this data alone.

---

## 3. The Expressive Framework: Concrete Schema Proposals

The graph is an outstanding curriculum MAP — probably the best machine-readable curriculum map I've seen. But it is not yet a teaching RESOURCE. To close the gap, the schema needs additions that transform it from "what to teach" to "how to teach." Here are six concrete proposals.

### Proposal 1: `WorkedExample` nodes

**The single highest-impact addition to the graph.**

```
(:Concept)-[:HAS_WORKED_EXAMPLE]->(:WorkedExample)
```

| Property | Type | Description |
|---|---|---|
| `example_id` | string | e.g. `MA-Y4-WE001` |
| `concept_id` | string | Parent concept |
| `difficulty` | int (1-5) | Within-concept difficulty level |
| `problem_statement` | string | The question or task |
| `solution_steps` | string[] | Ordered array of thinking steps |
| `teacher_narration` | string[] | Parallel array: what the teacher SAYS at each step |
| `common_error_at_step` | string[] | Parallel array: what could go wrong here |
| `manipulative` | string | Optional: concrete resource used (Dienes blocks, fraction wall) |
| `representation` | string | Optional: pictorial representation (bar model, number line) |
| `year_group` | string | Y4, Y5, etc. |

**Example for column addition:**
```json
{
  "example_id": "MA-Y4-WE003",
  "concept_id": "MA-Y4-C002",
  "difficulty": 3,
  "problem_statement": "347 + 256",
  "solution_steps": [
    "Start with the ones column: 7 + 6 = 13",
    "13 is more than 9, so write 3 in the ones column and carry 1 to the tens",
    "Now the tens: 4 + 5 = 9, plus the carried 1 = 10",
    "10 tens = 1 hundred, so write 0 in tens and carry 1 to hundreds",
    "Now hundreds: 3 + 2 = 5, plus carried 1 = 6",
    "Answer: 603"
  ],
  "teacher_narration": [
    "Let's start with the ones. What's 7 add 6?",
    "13! That's too many for one column. What do we do?",
    "Good — write the 3, carry the 1. Now look at the tens.",
    "Careful — don't forget the little 1 we carried!",
    "And the hundreds. Nearly there.",
    "603. Let's check — is that reasonable? 347 is close to 350, 256 is close to 250, so about 600. Yes!"
  ],
  "common_error_at_step": [
    null,
    "Writes 13 in the ones column instead of exchanging",
    "Forgets the carried 1 (gets 593 instead of 603)",
    "Carries 10 instead of 1",
    null,
    null
  ],
  "manipulative": "Dienes blocks (ones, tens, hundreds)",
  "representation": "Place value columns with carry row"
}
```

**Why this matters:** This is the difference between a textbook and a teacher. Claude can currently say "column addition involves exchanging when the total exceeds 9." With this node, Claude can say "Let's start with the ones. What's 7 add 6? ... 13! That's too many for one column. What do we do?"

**Estimated scope:** 5-8 worked examples per Y4 Maths concept (8 concepts = ~50 examples), 3-5 per English grammar/spelling concept (~30), 2-3 per Science investigation (~30). Total: ~110 worked examples for Y4. This is achievable by LLM generation with teacher review.

### Proposal 2: `DifficultyLevel` sub-nodes within concepts

```
(:Concept)-[:HAS_DIFFICULTY_LEVEL]->(:DifficultyLevel)
```

| Property | Type | Description |
|---|---|---|
| `level` | int (1-5) | 1=foundational, 5=extension |
| `description` | string | What this level looks like |
| `entry_criteria` | string | Child should attempt this level when... |
| `exit_criteria` | string | Child is ready for the next level when... |
| `example_task` | string | A representative task at this level |

**Example for Fractions — Equivalent Fractions (MA-Y4-C004):**
```
Level 1: Recognise equivalent fractions using fraction walls (1/2 = 2/4)
Level 2: Generate equivalent fractions by multiplying numerator and denominator (2/3 = 4/6)
Level 3: Simplify fractions by dividing (4/8 = 1/2)
Level 4: Compare fractions with different denominators by finding common denominators
Level 5: Order a set of 4+ fractions including mixed numbers
```

**Why this matters:** This gives Claude the scaffolding ladder. Currently, all Y4 concepts are complexity 2 — Claude has no way to differentiate between a child who needs Level 1 and a child ready for Level 5.

### Proposal 3: `DiagnosticQuestion` nodes

```
(:Concept)-[:HAS_DIAGNOSTIC]->(:DiagnosticQuestion)
```

| Property | Type | Description |
|---|---|---|
| `question_id` | string | e.g. `MA-Y4-DQ003` |
| `question_text` | string | The question posed to the child |
| `correct_answer` | string | Expected correct response |
| `distractor_answers` | object[] | Array of {answer, misconception, intervention} |
| `difficulty` | int (1-5) | Maps to DifficultyLevel |
| `question_type` | string | `multiple_choice`, `open_response`, `true_false`, `sort` |

**Example:**
```json
{
  "question_id": "MA-Y4-DQ007",
  "question_text": "Which is bigger: 1/3 or 1/4?",
  "correct_answer": "1/3",
  "distractor_answers": [
    {
      "answer": "1/4",
      "misconception": "Bigger denominator = bigger fraction",
      "intervention": "Use a fraction wall. Show that when you cut something into MORE pieces, each piece is SMALLER. 1/3 means 1 piece out of 3 — that's bigger than 1 piece out of 4."
    },
    {
      "answer": "They are the same",
      "misconception": "Both have numerator 1, so they must be equal",
      "intervention": "Draw two identical rectangles. Cut one into 3 equal parts and one into 4 equal parts. Shade 1 part of each. Which shaded part is bigger?"
    }
  ],
  "difficulty": 2,
  "question_type": "multiple_choice"
}
```

**Why this matters:** This closes the gap between "Claude knows the misconception exists" and "Claude can diagnose it in real time and respond with a targeted intervention." Currently, the graph says children confuse fraction size. This node tells Claude: if the child says 1/4, they think bigger denominator = bigger fraction, and here's what to do about it.

### Proposal 4: `HandoverIndicator` property on ConceptCluster

Add to existing ConceptCluster nodes:

| Property | Type | Description |
|---|---|---|
| `readiness_signals` | string[] | Observable signs the child is ready for independence |
| `independence_task` | string | A task to confirm readiness (child does it alone) |
| `common_false_readiness` | string | What looks like readiness but isn't |

**Example for HI-KS2-D004-CL001 (Analyse causes/consequences/significance):**
```json
{
  "readiness_signals": [
    "Child offers multiple causes without prompting",
    "Child uses 'because' and 'therefore' unprompted in historical argument",
    "Child challenges a single-cause explanation ('but there was also...')",
    "Child distinguishes short-term and long-term consequences"
  ],
  "independence_task": "Give the child a new historical event they haven't studied. Can they identify at least 2 causes and 2 consequences without scaffolding?",
  "common_false_readiness": "Child can list causes from the taught example but cannot transfer the skill to a new event — this is recall, not analytical competence"
}
```

**Why this matters:** This tells Claude when to step back. Currently, Claude has no signal for "this child is ready to try alone." The common_false_readiness is critical — it prevents Claude from handing over too early when a child can parrot an answer but hasn't internalised the skill.

### Proposal 5: Age-banded ThinkingLens `agent_prompt` variants

Add to existing APPLIES_LENS relationship:

| Property | Type | Description |
|---|---|---|
| `agent_prompt_ks1` | string | AI instruction calibrated for 5-7 year olds |
| `agent_prompt_ks2` | string | AI instruction calibrated for 7-11 year olds |
| `agent_prompt_ks3` | string | AI instruction calibrated for 11-14 year olds |

**Example for "Systems and System Models" lens:**

Current (all ages): "prompt pupils to map the parts of a system and their connections, identify inputs and outputs, trace feedback loops, and predict what happens when one component changes"

**KS1 variant:** "Help the child name all the parts. Ask: What are the bits? What does each bit do? What happens if we take this bit away? Use a physical object (a bicycle, a sandwich) they can see or imagine."

**KS2 variant:** "Guide the child to draw a simple diagram showing the parts and how they connect. Ask: What goes IN and what comes OUT? If we change THIS part, what happens to THAT part? Use concrete systems they know — the water cycle, a food chain, a school timetable."

**KS3 variant:** "Challenge pupils to map interactions formally. Identify feedback loops, unintended consequences, and boundary decisions. Ask: Where does this system end and another begin? What assumptions are we making? Use abstract systems — economic models, ecosystems, political structures."

**Why this matters:** "Trace feedback loops" is meaningless to a Year 1 child and insultingly simple for a Year 9 pupil. The current one-size-fits-all prompt limits the ThinkingLens from being a genuinely useful teaching tool.

### Proposal 6: `ConcreteResource` nodes for text-based subjects

```
(:ContentVehicle)-[:USES_RESOURCE]->(:ConcreteResource)
(:Concept)-[:HAS_RESOURCE]->(:ConcreteResource)
```

| Property | Type | Description |
|---|---|---|
| `resource_id` | string | e.g. `EN-Y4-RES001` |
| `resource_type` | string | `text_passage`, `image_description`, `data_set`, `word_list`, `map_description` |
| `content` | string | The actual text, data, or description |
| `source` | string | Attribution |
| `reading_level` | string | e.g. `Y4`, `Y4-stretch` |
| `curriculum_links` | string[] | Concept IDs this resource supports |

**Why this matters:** Claude cannot teach reading comprehension without a text to read, cannot teach data interpretation without data to interpret, and cannot teach map skills without a map to read. Currently the graph names resources (Vindolanda tablets) but provides nothing Claude can actually present to a child.

---

## 4. Three Worked Examples: What Teaching Looks Like

### Example A: Mathematics — Equivalent Fractions (MA-Y4-C004)

**What Claude has from the graph:**
- Concept description: "Equivalent fractions are fractions that have the same value but are expressed using different numerators and denominators"
- Teaching guidance: "Use visual models — fraction walls, number lines, bar models — to demonstrate that fractions such as 1/2, 2/4 and 4/8 all name the same proportion"
- Common misconception: "Pupils may believe that multiplying the numerator and denominator by the same number is 'cheating' or that the fraction must change"
- CO_TEACHES: Links to MA-Y4-C005 (Decimal Equivalents)
- Vehicle success criteria: "Find equivalent fractions using multiplication and division; Simplify fractions to their lowest terms"
- ThinkingLens: Patterns — "prompt pupils to notice what repeats or follows a rule"

**What Claude is MISSING:**
- No worked example showing HOW to find equivalent fractions step by step
- No difficulty levels (start with halves? quarters? thirds?)
- No problems for the child to attempt
- No diagnostic questions to check understanding
- No fraction wall or visual representation to show
- No "ready to try alone" indicator

**What a real lesson looks like (what Claude CANNOT do from this data):**

> **Teacher:** Look at this fraction wall. Can you see that 1/2 takes up the same space as 2/4? *(Claude has no fraction wall to show)*
>
> **Child:** Yes.
>
> **Teacher:** What about 3/6 — does that look the same size? *(Claude has no representation to point to)*
>
> **Child:** Yes... they're all the same!
>
> **Teacher:** Brilliant. Now watch what I do. I'm going to take 1/2, and multiply the top AND the bottom by 2. What do I get? *(This is the worked example Claude cannot provide)*
>
> **Child:** 2/4!
>
> **Teacher:** And if I multiply 1/2 top and bottom by 3?
>
> **Child:** 3/6!
>
> **Teacher:** You've spotted the pattern. Now you try: make 3 fractions equivalent to 1/3. *(Claude has no problems to set)*

**Verdict:** Claude could explain WHAT equivalent fractions are and name the misconceptions. It CANNOT model the step-by-step thinking, provide visual representations, set graduated problems, or diagnose specific errors in the child's working. **Teaching readiness: 3/10.**

### Example B: English — Fronted Adverbials (EN-Y4-C015, VGP domain)

**What Claude has from the graph:**
- Concept description: "Using fronted adverbials to vary sentence openings and control how information is presented. Fronted adverbials — words, phrases or clauses that add information about time, place, manner or frequency — are placed at the front of the sentence and followed by a comma."
- Teaching guidance: "Teach fronted adverbials as a deliberate writer's choice that controls the reader's attention. Start with time adverbials (After lunch, Later that day), then place (Behind the door, In the distance), then manner (Carefully, With great effort)."
- Common misconception: "Pupils may place the adverbial at the end of the sentence rather than fronting it, or forget the comma after it"
- CO_TEACHES: Links to EN-Y4-C016 (Noun Phrases), EN-Y4-C014 (Punctuation)
- Vehicle (EN-Y4-CV002 Adventure Narrative): "grammar_focus: fronted adverbials, expanded noun phrases"
- ThinkingLens: Structure and Function

**What Claude is MISSING:**
- No example sentences showing fronted adverbials in context
- No graded practice sentences (easy → hard)
- No model text containing fronted adverbials for children to find
- No sentence transformation exercises
- No diagnostic questions (can the child identify vs. use fronted adverbials?)

**What a real lesson looks like:**

> **Teacher:** "The fox crept through the garden." That's a fine sentence. But watch this — I'm going to move one bit to the front: "Through the garden, the fox crept." *(Claude could generate this — the grammar rule is explicit enough)*
>
> **Teacher:** Notice the comma after "Through the garden" — that's the rule: fronted adverbial, comma, rest of the sentence. *(Claude could teach this — the punctuation rule is stated)*
>
> **Teacher:** Now try this one: "The children played happily in the park after school." Can you move something to the front? *(Claude would need to generate practice sentences — possible from its own language model, but not from the graph data)*

**Verdict:** This is one of the more teachable concepts because the grammar rule is explicit, the common error is identified, and Claude's own language capabilities can generate example sentences. The graph provides the WHAT and the WHY; Claude's language model can supply the HOW. **Teaching readiness: 6/10** — but this is because Claude is supplementing graph data with its own linguistic knowledge, not because the graph is sufficient.

### Example C: Science — States of Matter (SC-KS2-C014)

**What Claude has from the graph:**
- Concept description: "Materials exist in three states — solid, liquid and gas — each with distinctive properties relating to shape, volume and particle arrangement"
- Teaching guidance: "Use everyday examples to establish the observable properties of each state... introduce the particle model as a way of explaining observable differences"
- Common misconceptions: "Pupils may confuse melting and dissolving"; "Pupils may think gases have no mass or do not take up space"
- Vehicle (SC-KS2-CV015 States of Matter Investigation): enquiry_type: classifying_and_grouping, equipment: thermometer, ice, water, kettle, chocolate, butter, wax; variables and expected outcomes
- ThinkingLens: Patterns — "prompt pupils to notice what repeats or follows a rule"
- DEVELOPS_SKILL: WS-003 (Fair Testing and Variables)
- CO_TEACHES: Links to SC-KS2-C015 (Evaporation and Condensation)

**What Claude is MISSING:**
- No particle model diagrams (the concept describes the model but Claude cannot show it)
- No step-by-step experimental procedure (vehicle lists equipment but not method)
- No data table template for recording observations
- No difficulty levels (identifying states → explaining WHY → predicting changes)

**What a real lesson looks like:**

> **Teacher:** I've got ice, water, and steam. They're all the same thing — what? *(Claude can ask this — the concept is clear)*
>
> **Child:** Water!
>
> **Teacher:** Right. So why does ice feel hard and water flows? Let's draw the particles. In ice, they're packed tight, barely moving. In water, they slide past each other. In steam, they fly apart. *(Claude cannot draw but could describe this vividly — the concept description supports it)*
>
> **Teacher:** Now — is melting the same as dissolving? *(Claude knows this is a key misconception and could probe it)*
>
> **Child:** Um... yes?
>
> **Teacher:** Let's test it. If I melt chocolate, can I get the chocolate back by cooling it? *(Vehicle lists chocolate as equipment — Claude could reference this)*
>
> **Child:** Yes!
>
> **Teacher:** And if I dissolve sugar in water, can I get it back by cooling it? *(Claude could extend this — the misconception data supports the pedagogical move)*

**Verdict:** Science is the most teachable subject from this data because the concept descriptions are rich enough to support explanatory teaching, the misconceptions enable diagnostic questioning, the vehicles provide equipment context, and the ThinkingLens frames the cognitive approach. The gap is still in concrete procedures and visual representations, but Claude's general knowledge of science can partially fill this. **Teaching readiness: 7/10.**

---

## 5. Overall Verdict

### The Bottom Line

**Can Claude TEACH a Year 4 child from this graph data alone? Not yet — but it's closer than I expected, and the path to "yes" is clear.**

The graph is an exceptional curriculum map: 5.1/10 as a teaching resource, but 8.5/10 as a curriculum reference. The distinction matters. As a reference, it tells Claude everything about WHAT Year 4 children should learn, WHY concepts are sequenced as they are, WHERE each concept connects to others, and WHAT misconceptions to watch for. As a teaching resource, it lacks the HOW: how to model thinking, how to scaffold difficulty, how to diagnose errors in real time, and how to know when the child is ready to fly solo.

### The Gap is Smaller Than It Looks

Here's the key insight: **Claude already knows how to teach.** It has deep knowledge of mathematics, English grammar, science, and history. What the graph provides — and what Claude CANNOT supply on its own — is:

1. **Curriculum-specific sequencing** (what comes before and after each concept)
2. **Age-appropriate calibration** (what a Y4 child should know vs. a Y6 child)
3. **UK-specific content** (National Curriculum statutory requirements, KS2 test frameworks)
4. **Misconception libraries** (specific to British classrooms and UK curriculum sequencing)
5. **Assessment alignment** (what will actually be tested)

These are exactly the things the graph does well. The things the graph does badly — worked examples, difficulty levels, diagnostic questions — are things Claude could partially generate from its own training. **The optimal architecture is graph data + Claude's general knowledge, not graph data alone.**

### Three Changes That Would Transform the Score

1. **Add WorkedExample nodes for Maths and English grammar** (~80-110 examples for Y4). This single addition would raise Maths from 4.8/10 to approximately 7/10. It is the highest-impact, most achievable improvement. Estimated effort: LLM-generated with teacher review, 2-3 days of curation per subject.

2. **Add DifficultyLevel sub-nodes to every Y4 concept** (5 levels per concept, ~80 concepts = ~400 entries). This gives Claude the scaffolding ladder and raises SCAFFOLD scores across all subjects by 2-3 points. Estimated effort: teacher-authored, 1 week for core subjects.

3. **Add DiagnosticQuestion nodes for the top 20 misconceptions** (3-5 questions per misconception = ~80 questions). This closes the diagnosis-to-intervention gap and raises RESPOND scores. Estimated effort: teacher-authored, 3-4 days.

These three additions would raise the overall average from 5.1/10 to approximately 7.0/10 — which is the threshold where I'd say "yes, Claude could genuinely teach from this."

### What This Means for the Project

The graph is NOT trying to replace a teacher. It's trying to give an AI the curriculum knowledge that a teacher has. On that measure, it's already doing a remarkable job for the structural/relational dimension. The missing dimension is the PROCEDURAL knowledge — the step-by-step "this is how you actually do a column addition" that teachers carry in their heads from 12 years of practice.

The good news: procedural knowledge is the most generatable layer. Claude can produce worked examples. Teachers can validate them. The graph provides the scaffold (which concept, what difficulty, what misconceptions to embed), and the generation can be automated.

**My recommendation:** Don't try to make the graph do everything. Make it do what only a graph CAN do — structure, sequencing, connections, prerequisites, misconceptions — and let Claude supply the procedural narration from its own capabilities. The schema proposals above (WorkedExamples, DifficultyLevels, DiagnosticQuestions) fill exactly the gap between what the graph knows and what Claude needs to teach.

### Final Score Card

| What | Rating | Trajectory |
|---|---|---|
| Graph as curriculum map | 8.5/10 | Excellent — best machine-readable curriculum map I've seen |
| Graph as teaching resource (current) | 5.1/10 | Usable for explanation, weak for active teaching |
| Graph as teaching resource (with 3 additions) | ~7.0/10 | Viable for AI-led tutoring in core subjects |
| Graph as teaching resource (ceiling) | ~8.5/10 | With vehicles + worked examples + diagnostics across all subjects |

---

*Mr David Okafor, Year 4 Class Teacher*
*"The graph knows what I know about curriculum. It doesn't yet know what I know about the child in front of me. The three proposals above start to close that gap."*
