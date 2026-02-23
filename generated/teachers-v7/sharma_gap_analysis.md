# Gap Analysis: Y5 Mathematics — Factors, Multiples, Primes, Squares and Cubes

**Teacher:** Mr. Sharma (Y5, Birmingham)
**Cluster:** MA-Y5-D003-CL001
**Date:** 2026-02-23
**Graph version:** v3.9 (DifficultyLevel pilot — Y3 Maths only)

---

## Section-by-Section Analysis

### 1. Learning Objectives — ✅ (10/10)

| Available | Missing | Invented |
|---|---|---|
| 4 statutory objectives with full text (MA-Y5-O011, O012, O013, O020) | Nothing | Nothing |
| Objective-to-concept mapping clear | | |
| Assessment content domain codes aligned | | |

**Commentary:** This is the strongest section. The graph's statutory objective data is complete, well-structured, and directly usable. The concept-to-objective mapping means I can trace every learning objective back to its assessed content domain code. No teacher input needed.

---

### 2. Success Criteria — ⚠️ (6/10)

| Available | Missing | Invented |
|---|---|---|
| Concept mastery descriptions (what "mastery" looks like) | Graded success criteria at entry/developing/expected/greater_depth | All/most/some thresholds |
| Assessment content domain codes | Exemplar pupil responses at each level | Boundary between tiers |
| | DifficultyLevel descriptions | |

**Commentary:** The concept mastery descriptions are good ("mastery means pupils can...") but they describe only the EXPECTED standard. I had no graph data to distinguish what "working towards" looks like versus "greater depth." With DifficultyLevel data, each tier would have had a description I could directly convert into success criteria.

---

### 3. Prior Knowledge Required — ✅ (9/10)

| Available | Missing | Invented |
|---|---|---|
| PREREQUISITE_OF relationships with concept names | Diagnostic questions for prerequisite checking | Entry ticket questions |
| Cross-year prerequisite chain (Y4→Y5) | | |
| Prerequisite concept descriptions | | |

**Commentary:** The prerequisite chain is excellent. I can see exactly which Y4 concepts feed into this cluster. The only gap is diagnostic items — but that's reasonable, as diagnostic questions are teacher-facing content, not curriculum structure.

---

### 4. Lesson Structure with Timings — ⚠️ (6/10)

| Available | Missing | Invented |
|---|---|---|
| PedagogyProfile (session length, scaffolding, productive failure) | Lesson structure template | Timing splits (10/35/15) |
| PedagogyTechniques (generation effect, interleaving, spacing, variation) | Activity sequencing | Phase transitions |
| InteractionTypes (16 types, 8 primary) | Suggested activity-to-concept mapping | Activity selection |
| Hint tiers (4 levels with examples) | | |

**Commentary:** The graph gives me excellent building blocks (techniques, interaction types, hint tiers) but no blueprint for assembling them into a lesson. This is perhaps appropriate — lesson structure is a teacher decision. But a suggested sequence (e.g., "for introduction clusters, use: productive failure → direct instruction → faded worked example → interleaved practice") would save significant planning time.

---

### 5. Key Vocabulary with Definitions — ✅ (10/10)

| Available | Missing | Invented |
|---|---|---|
| 14 terms with definitions from key_vocabulary fields | Nothing | Nothing |
| Vocabulary mapped to specific concepts | | |
| Content guideline: "academic vocabulary OK with scaffolding" | | |

**Commentary:** Excellent. Every term comes directly from the graph. The content guideline confirms Y5 pupils can handle academic vocabulary with scaffolding, which means I don't need to simplify the terminology.

---

### 6. Resources and Materials — ⚠️ (4/10)

| Available | Missing | Invented |
|---|---|---|
| Teaching guidance implies resources (cubes, grids, Venn diagrams) | Explicit resources list | Mini whiteboards |
| InteractionType descriptions imply materials | Quantities needed | Coloured pencils |
| | Digital resource links | Category sorting cards |
| | Printable templates | |

**Commentary:** The graph doesn't have a resources/materials property on any node. I had to infer from teaching guidance ("use physical square arrays" → need multilink cubes). A `resources_needed` array on ConceptCluster or ContentVehicle would be straightforward to add and highly useful.

**No Content Vehicles:** There are zero Mathematics KS2 ContentVehicle nodes. History, Geography, Science, and English all have vehicles but Maths does not. A `worked_example_set` vehicle type already exists in the schema — it just hasn't been populated for Maths. This is a significant gap for lesson planning.

---

### 7. Differentiation — ⚠️→❌ (2/10)

| Available | Missing | Invented |
|---|---|---|
| Concept mastery descriptions (expected standard only) | DifficultyLevel nodes (entry/developing/expected/greater_depth) | ALL support tasks |
| Misconceptions (useful for identifying struggle points) | example_task per level | ALL extension tasks |
| Teaching guidance (one approach, not differentiated) | example_response per level | ALL scaffolding decisions |
| | common_errors per level | Difficulty boundaries |
| | Scaffold descriptions | Number range reductions |

**Commentary:** This is the most critical gap. Without DifficultyLevel data, differentiation is entirely my invention. I have 12 years of experience — a newly qualified teacher or an AI agent would be guessing. The graph tells me WHAT to teach but not HOW to adjust it for different attainment levels within the same classroom.

**Specific impact:**
- I cannot confidently set "working towards" tasks because I don't know the lower boundary
- I cannot confidently set "greater depth" tasks because I don't know the upper boundary
- I cannot identify level-specific misconceptions (a child working at "entry" has different errors than one at "expected")
- I cannot create a faded worked example with grounded difficulty steps — I'm choosing the numbers myself

---

### 8. Assessment Opportunities — ✅ (9/10)

| Available | Missing | Invented |
|---|---|---|
| 7 content domain codes mapped to concepts | Sample assessment questions | Exit ticket questions |
| Mastery threshold (5 correct in 7 days, 80%) | Level-specific assessment criteria | |
| Spacing interval (3-14 days) | | |

**Commentary:** Strong assessment alignment. The content domain codes tell me exactly what's formally assessed. The mastery threshold and spacing data are directly usable for adaptive systems. Only gap: no sample questions at each assessed level.

---

### 9. Common Misconceptions — ✅ (10/10)

| Available | Missing | Invented |
|---|---|---|
| 8 specific misconceptions with pedagogical counters | Level-specific misconception prevalence | Nothing |
| Misconceptions mapped to specific concepts | | |
| Counter-strategies included in teaching guidance | | |

**Commentary:** The strongest qualitative data in the graph. Every misconception is specific ("pupils think 1 is prime"), tied to a concept, and comes with a pedagogical counter-strategy. This is genuinely useful, experienced-teacher-quality data. The only enhancement would be prevalence data (how common is each misconception?) and level-specific variants.

---

### 10. Worked Examples — ⚠️ (5/10)

| Available | Missing | Invented |
|---|---|---|
| Method descriptions (systematic factor pair listing, sieve) | Grounded example_task per difficulty level | Specific numbers chosen |
| PedagogyProfile: "faded worked examples required" | example_response per level | Difficulty graduation |
| Teaching guidance: step-by-step method | common_errors per worked example | Fading structure |

**Commentary:** The graph gives me the METHOD (how to find factors systematically) but not GRADED EXAMPLES. With DifficultyLevel data, I'd have had pre-validated tasks like "Find factor pairs of 12" (entry), "Find factor pairs of 48" (expected), "Find HCF of 48 and 72" (greater_depth) — each with an expected response and common errors. Instead I'm choosing numbers from experience.

---

### 11. Practice Questions — ⚠️→❌ (2/10)

| Available | Missing | Invented |
|---|---|---|
| PedagogyTechnique: interleaved practice, varied practice | ALL specific practice questions | Every question |
| Teaching guidance: method descriptions | Difficulty-graded question sets | Every difficulty label |
| | example_task / example_response | Number choices |
| | DifficultyLevel data | Intended difficulty |

**Commentary:** The graph tells me to interleave and vary, but gives me zero actual questions. Every practice question in the lesson plan is my invention. With DifficultyLevel data providing example_tasks at each tier, I could have directly used those as practice questions and been confident they're correctly graded.

---

### 12. Cross-Curricular Links — ⚠️ (6/10)

| Available | Missing | Invented |
|---|---|---|
| 2 cross-domain CO_TEACHES links (fractions, volume) | Cross-subject links (Maths→Science, Maths→Computing) | Science/computing connections |
| 2 ThinkingLens connections with prompts and stems | Real-world application contexts | |
| PROMPT_FOR age-banded prompts (KS2 specific) | | |

**Commentary:** Within-maths connections are excellent — the cross-domain CO_TEACHES data directly tells me "factors connect to fractions because LCM = common denominator." The ThinkingLens provides a cognitive framing ("Scale, Proportion and Quantity") with KS2-appropriate question stems. Cross-subject connections are absent — the DEVELOPS_SKILL relationships exist for Science but there's no Maths→Science conceptual bridge in the graph.

---

## Overall Scores

### Overall Readiness Score: 6/10

**Breakdown:**
- Curriculum structure and objectives: 10/10 (complete)
- Pedagogical framework: 8/10 (techniques, interaction types, learner profile — all strong)
- Qualitative teaching data: 9/10 (misconceptions, vocabulary, teaching guidance — excellent)
- Differentiation and difficulty: 2/10 (no DifficultyLevel data — critical gap)
- Practice content: 2/10 (no questions, no worked examples at graded levels)
- Resources and vehicles: 3/10 (no explicit resources, no Maths content vehicles)

The graph is excellent at telling me WHAT to teach, to WHOM, and with WHAT pedagogical techniques. It is weak at telling me HOW to differentiate within a concept and WHAT specific tasks to use at each difficulty level.

---

### Missing DifficultyLevels Impact: 8/10

**How much harder was planning without DifficultyLevel data?**

This is an 8/10 impact — the absence of DifficultyLevel data was the single most significant barrier to producing a genuinely teach-ready lesson plan.

**Specific difficulties:**

1. **Differentiation (sections 2, 7):** I had to invent all support and extension tasks. A Y3 Maths planner (brennan) with DifficultyLevel data gets entry/developing/expected/greater_depth descriptions with example_tasks and example_responses. I got nothing. This meant I was relying entirely on professional experience for the most important part of the plan — the part that determines whether every child in my class can access the lesson.

2. **Worked examples (section 10):** DifficultyLevel nodes include `example_task` and `example_response`. These would have given me concrete, pre-validated worked examples at each tier. Instead I chose my own numbers and hoped they were appropriate.

3. **Practice questions (section 11):** DifficultyLevel nodes include `common_errors` per level. This would have let me design distractors and anticipated-error feedback at each tier. Instead I used concept-level misconceptions (which are good, but not graded).

4. **Success criteria (section 2):** The four tiers (entry/developing/expected/greater_depth) align directly to all/most/some success criteria banding. Without them, my banding is professional guesswork.

5. **Assessment (section 8):** DifficultyLevel `example_response` data would have told me what a correct answer LOOKS LIKE at each tier — essential for marking and moderation.

**Estimate:** With DifficultyLevel data, my overall readiness score would rise from **6/10 to 8/10**. The remaining 2 points would require content vehicles (worked example sets) and explicit resource lists.

---

### Top 5 Data Additions That Would Most Improve Lesson Planning

| Rank | Addition | Impact | Effort |
|---|---|---|---|
| 1 | **DifficultyLevel nodes for Y5 Maths** (and all year groups) | Transforms differentiation from guesswork to evidence. Each concept gets 3-4 grounded tiers with example_task, example_response, common_errors. | High — requires subject-expert curation per concept per year |
| 2 | **ContentVehicle nodes for Mathematics KS2** (`worked_example_set` type) | Provides ready-to-use teaching packs with graduated examples, manipulatives lists, and assessment tasks. | Medium — vehicle structure exists, needs Maths content |
| 3 | **`resources_needed` property on ConceptCluster** | Explicit list of physical and digital resources. Saves teacher inference from teaching guidance. | Low — straightforward enrichment of existing clusters |
| 4 | **Cross-subject conceptual links for Mathematics** | Maths→Science, Maths→Computing connections at concept level (not just programme level). | Medium — requires cross-subject expert review |
| 5 | **Practice question bank per concept** | Even 5 questions per concept, graded by DifficultyLevel, would transform the practice sections. | High — requires question authoring and validation |

---

### Specific New Entities/Properties Requested

#### New Nodes
- **DifficultyLevel for Y5 Maths** (extends existing pilot) — ~150 nodes (41 concepts x 3-4 levels)
- **ContentVehicle for Mathematics KS2** — ~15-20 worked_example_set vehicles across Y3-Y6

#### New Properties
- `resources_needed: [str]` on ConceptCluster — list of physical/digital resources
- `suggested_lesson_sequence: str` on ConceptCluster — brief recommended phase structure for introduction vs. practice clusters
- `diagnostic_questions: [str]` on the PREREQUISITE_OF relationship — 2-3 quick checks per prerequisite link
- `cross_subject_links: [{subject, concept_id, rationale}]` on Concept — explicit cross-subject bridges

#### New Relationships
- `(:Concept)-[:APPLIED_IN]->(:Subject)` — cross-subject conceptual application (e.g., prime numbers in computing)
- `(:ContentVehicle)-[:PROVIDES_WORKED_EXAMPLE]->(:DifficultyLevel)` — linking vehicles to specific difficulty tiers

---

## Comparison Note: Y5 vs. Y3 (DifficultyLevel Impact)

The Y3 Maths pilot (brennan's assignment) has DifficultyLevel data; Y5 does not. This creates a natural comparison:

| Dimension | Y3 (with DifficultyLevels) | Y5 (without DifficultyLevels) |
|---|---|---|
| Differentiation confidence | High — grounded in entry/developing/expected/greater_depth | Low — teacher professional judgement only |
| Worked examples | Pre-validated example_task + example_response per level | Teacher-invented, unvalidated |
| Practice questions | Can be sourced from example_tasks across levels | Entirely invented |
| Common errors | Level-specific (entry pupils make different errors to expected) | Concept-level only (not graded) |
| Success criteria | Directly mapped to DL descriptions | Approximated from concept mastery description |
| Time to plan | Significantly reduced for differentiation sections | Full planning burden on teacher |

**Verdict:** DifficultyLevel data is not a "nice to have" — it is the single most impactful addition for lesson planning. Rolling it out from the Y3 pilot to all year groups should be a priority.

---

## Teaching Artefacts Needed

**The question:** What do I actually need to walk from "lesson plan on screen" to "ready to teach 30 children at 9am"? Here are my top 5 for Y5 Mathematics, in strict priority order.

### 1. Differentiated Practice Worksheets (print) — CRITICAL

**Why this is #1:** In a mastery classroom of 30 Y5 pupils, I have at least 3-4 attainment groups working on the same concept at different depths. I need a printed worksheet for each group — not a single sheet with "easy/medium/hard" rows, but genuinely different tasks at each DifficultyLevel tier.

**What I need generated:**
- **Sheet A (Entry/Support):** Factor pairs of numbers up to 30, primes identification up to 20 only, square numbers with physical array diagrams to count. Larger font, fewer questions (6-8), visual scaffolds (number line, multiplication square border).
- **Sheet B (Developing):** Factor pairs up to 50, primes up to 50, square and cube number calculations. Standard layout, 10-12 questions.
- **Sheet C (Expected):** Factor pairs up to 100, common factors and HCF, primes up to 100, full square/cube notation. 12-15 questions including word problems.
- **Sheet D (Greater Depth):** HCF of larger numbers, LCM problems, "always/sometimes/never" reasoning tasks, multi-step problems connecting factors to fractions. 8-10 questions requiring extended reasoning.

**What the graph provides today:** Nothing. Zero practice questions at any level. This is the artefact I spend the most time creating manually — typically 45-60 minutes per lesson to write, format, and differentiate four sheets. An AI system that could generate these from DifficultyLevel data + concept descriptions would save me more time than any other single feature.

**Graph data needed:** DifficultyLevel nodes (example_task, example_response, common_errors per tier). Without these, even an AI generator would be guessing at calibration.

### 2. Faded Worked Example Sheets (print) — HIGH

**Why this is #2:** The graph's PedagogyProfile explicitly says "faded worked examples required" for Y5. In a mastery lesson, I model a worked example on the board, then pupils complete partially-worked examples at their tables. This is the bridge between "I do" and "you do."

**What I need generated:**
- **Worked Example 1 (fully worked):** Factor pairs of 36 — every step shown with annotation ("Start at 1 × 36. Work up. Stop when factors meet.")
- **Worked Example 2 (partially faded):** Factor pairs of 48 — first 3 pairs given, pupil completes the rest
- **Worked Example 3 (mostly faded):** Factor pairs of 60 — only "1 × 60" given, pupil does all remaining pairs
- **Same pattern for:** Sieve of Eratosthenes (partially completed grid), square/cube notation (partially completed table)

**What the graph provides today:** The METHOD is well-described in teaching guidance ("start from 1 × n, work upward until factors meet"). The fading pedagogy is specified. But no actual worked example sheets exist. I have to create these from scratch every time.

**Graph data needed:** A `worked_example_steps` property on Concept or DifficultyLevel — structured step-by-step procedures that a generator could fade progressively.

### 3. 1-100 Number Grid (Sieve of Eratosthenes) (print) — HIGH

**Why this is #3:** The Sieve of Eratosthenes is the centrepiece activity for teaching primes. Every child needs a clean 1-100 grid to cross out multiples. This is mentioned explicitly in the graph's teaching guidance for MA-Y5-C003.

**What I need generated:**
- Clean 10×10 grid, numbers 1-100, large enough for children to cross out with coloured pencils
- Ideally with a step-by-step instruction strip at the top ("Step 1: Cross out 1. Step 2: Circle 2, then cross out all multiples of 2...")
- Differentiated version for support group: grid pre-started with multiples of 2 already crossed out

**What the graph provides today:** The teaching guidance describes the activity perfectly. But no printable grid exists. This is a 5-minute design task — trivial for a generator, but it's 5 minutes I shouldn't need to spend.

**Graph data needed:** Minimal — the concept description is sufficient. A `printable_template_type: 'number_grid_100'` property on the concept would let a generator know to produce this automatically.

### 4. Vocabulary Word Mat (print/display) — MEDIUM

**Why this is #4:** I keep a vocabulary mat on every table during maths lessons. For this cluster, there are 14 terms (factor, multiple, prime, composite, HCF, LCM, square number, cube number, etc.). Children refer to it constantly. I also want a large display version for the working wall.

**What I need generated:**
- **Table mat (A4 landscape):** All 14 terms with child-friendly definitions, an example for each, and a visual where possible (e.g., square array for "square number", factor pair tree for "factor")
- **Working wall cards (A4 portrait, one per term):** Large font, bold term, definition, visual example. For sticking on the classroom display wall during the unit.

**What the graph provides today:** All 14 vocabulary terms with definitions — this is one of the graph's strongest data sets. The definitions are accurate and curriculum-aligned. What's missing is the visual/layout formatting and child-friendly simplification (the graph definitions are teacher-facing, slightly too formal for a pupil word mat).

**Graph data needed:** A `child_friendly_definition` property (shorter, simpler phrasing) and `visual_hint` (description of an appropriate diagram) on each vocabulary term. The current definitions are good for teacher reference but need simplification for pupil-facing artefacts.

### 5. Exit Ticket / Mini-Assessment (print) — MEDIUM

**Why this is #5:** Every mastery lesson ends with an exit ticket — 3-5 questions that tell me whether each child has met the learning objective. I collect these at the door. They directly inform tomorrow's lesson (who needs same-day intervention, who's ready to move on).

**What I need generated:**
- **3-question exit ticket** aligned to the lesson's learning objectives:
  1. "Is 43 prime or composite? Explain how you know." (tests MA-Y5-O013 — primality)
  2. "What is 7²?" (tests MA-Y5-O020 — square number notation)
  3. "Name a common factor of 20 and 30." (tests MA-Y5-O011 — common factors)
- **Differentiated version:** Same 3 questions but with number scaffolds for support group (e.g., "Is 7 prime or composite?" instead of 43)
- **Marking guide:** Expected answers at each DifficultyLevel tier, common errors to watch for

**What the graph provides today:** Content domain codes (5C5a-d) tell me WHAT to assess. Misconceptions tell me what errors to anticipate. But no actual assessment items exist. The mastery threshold (5 correct in 7 days, 80%) is useful for adaptive systems but doesn't help me write a paper exit ticket.

**Graph data needed:** `assessment_items` on ContentDomainCode or DifficultyLevel — 3-5 validated questions per content domain code, graded by difficulty.

---

### Artefacts I Considered But Ranked Lower

| Artefact | Why it's lower priority for Y5 Maths |
|---|---|
| **Presentation slides / PowerPoint** | I teach from the board with live modelling, not slides. Maths mastery pedagogy is built around the "I do / we do / you do" cycle with real-time board work. Slides are too static for the Sieve of Eratosthenes or factor pair exploration. |
| **Knowledge organiser** | Useful for a whole unit (the full multiplication & division domain), but I don't use one for a single lesson. Would be valuable as a domain-level artefact, not a cluster-level one. |
| **Manipulative templates (fraction strips, place value cards)** | Not needed for THIS cluster — multilink cubes for square/cube arrays are physical objects I already have. Fraction strips would matter for MA-Y5-D004 (fractions cluster). |
| **Marking rubric / assessment grid** | The graph's content domain codes already give me the assessment framework. A formal rubric adds bureaucratic overhead without improving my teaching. The exit ticket + misconception data is more useful. |
| **Homework sheet** | I set homework from the school's scheme (White Rose), not bespoke sheets. A spacing-algorithm-driven homework generator would be interesting but that's a system feature, not a per-lesson artefact. |
| **Parent-facing summary** | Useful at unit level ("This half-term in Maths, we're learning about...") but not per-lesson. Would be a good automated output from the domain description. |
| **Interactive whiteboard resources** | I use a physical whiteboard and visualiser. IWB resources are useful but secondary to printed materials for a mastery classroom. |
| **Images / diagrams / illustrations** | The square array and cube diagrams would be useful projected, but I can draw these live. Lower priority than worksheets. |
| **Videos / animations** | Maths mastery is built on teacher modelling, not video. An animation of the Sieve of Eratosthenes would be nice but not essential. |

---

### The "Plan to Teach" Gap — Summary

| What I have from the graph | What I still need to create manually | Time cost |
|---|---|---|
| Learning objectives (complete) | Differentiated worksheets (4 versions) | 45-60 min |
| Vocabulary (complete, 14 terms) | Faded worked example sheets | 20-30 min |
| Misconceptions (complete, 8 items) | 1-100 number grid with instructions | 10-15 min |
| Teaching methods (complete) | Vocabulary word mat (reformatted for pupils) | 15-20 min |
| Assessment codes (complete) | Exit ticket with marking guide | 10-15 min |
| Pedagogy techniques (complete) | | |
| ThinkingLens framing (complete) | | |

**Total manual creation time: ~100-140 minutes** to go from lesson plan to classroom-ready.

The lesson plan itself took about 30 minutes to write using graph data. But the ARTEFACTS take 3-4x longer than the plan. This is where generation would have the highest impact.

**The key insight:** The graph is excellent at the INTELLECTUAL work of lesson planning (what to teach, how to teach it, what to assess, what misconceptions to address). But the PRODUCTION work — turning that intellectual plan into physical classroom materials — is entirely manual. A generation layer that converts graph data into printable artefacts would close the biggest remaining gap between "plan" and "teach."

---

*Generated by Mr. Sharma (simulated Y5 teacher persona) from knowledge graph data, 2026-02-23*
