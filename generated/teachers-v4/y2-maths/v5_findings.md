# Year 2 Mathematics -- Teacher Evaluation (v5)

**Evaluator:** James Henderson, Year 2 class teacher (Maths lead), 15 years' experience
**Date:** 2026-02-23
**Scope:** All 8 Year 2 Maths domains (23 concepts, 34 objectives, 16 concept clusters, 8 content vehicles, 10 thinking lenses)
**Previous evaluation:** v4 (2026-02-22) -- rated Structure 7/10, Content Generation Readiness 4/10

---

## 1. What Has Improved Since v4

### 1.1 Content Vehicles -- The Big Addition

Content Vehicles are the single most significant improvement since v4. They directly address three of my top five complaints from the previous review:

**Complaint #3 (v4): "No concrete-pictorial-abstract progression as structured data."**
**Status: SUBSTANTIALLY ADDRESSED.**

Every Content Vehicle now has a structured `CPA stage` field. For example, CV001 specifies:
> `concrete (Dienes blocks) -> pictorial (place value chart, part-whole model, number line) -> abstract (numeral representation)`

And CV002:
> `concrete (counting objects) -> pictorial (number line jumps) -> abstract (column method introduction)`

This is exactly what I asked for. An AI generating a lesson can now follow a structured CPA trajectory rather than extracting it from prose. The manipulatives list is also structured: CV001 lists "Dienes blocks (units and tens), place value charts, arrow cards" -- queryable, specific, and correct.

**Complaint #5 (v4): "No question specifications for assessment."**
**Status: PARTIALLY ADDRESSED.**

Each Content Vehicle has `Assessment` and `Success criteria` fields. CV001's assessment asks: "Can pupils partition any 2-digit number into tens and ones using Dienes and without? Can they compare pairs of numbers using < > = symbols? Can they order a set of 2-digit numbers and explain their reasoning?"

This is progress. However, these are assessment QUESTIONS, not assessment SPECIFICATIONS. There is still no difficulty grading within the assessment, no diagnostic question templates linked to specific misconceptions, and no distinction between formative and summative items. More on this in the gaps section.

**Complaint #4 (v4): "No worked examples."**
**Status: NOT ADDRESSED.**

Content Vehicles are typed as `worked_example_set` but contain no actual worked examples. The vehicle describes what to teach and assesses, but does not contain a single step-by-step worked problem. CV001 does not say: "Step 1: Show 37 with 3 ten-sticks and 7 unit cubes. Step 2: Ask -- what does the 3 represent? Step 3: Record 37 = 30 + 7." This remains the most significant gap for content generation.

### 1.2 Thinking Lenses -- New Layer

Thinking Lenses are a genuinely new addition that addresses something I did not explicitly ask for in v4 but recognise as valuable: cognitive framing.

Every cluster now has a primary and secondary lens with:
- A key question (e.g., "What patterns can I notice here, and what do they allow me to predict?")
- A rationale explaining why this lens fits this cluster
- An AI instruction describing how to implement the lens

In practice (see teaching log), the Patterns lens was the right choice for D001-CL001 and worked well as a questioning framework. The key question drove genuine mathematical reasoning in Lessons 1, 3, and 4.

**However, the lenses have problems.** See Section 5 for detail.

### 1.3 Learner Profile -- Fixed

The v4 context file had the Y1 learner profile attached to Y2 content. This has been fixed. The v5 context correctly shows Y2 data:
- Number range: 0-100 (not 1-20)
- Sentence length: max 10 words (not 8)
- FK grade max: 1 (not 0)
- Session length: 8-15 min, 3 activities (not 5-12 min, 2 activities)

This was the #1 critical bug in v4 and fixing it removes the risk of age-inappropriate content generation.

### 1.4 Cross-Domain CO_TEACHES -- Enriched

The cross-domain connections now have rationales and reason types (`prerequisite_gap`, `feeds_into`, `parallel_concept`, `shared_context`). The Henderson annotations from my earlier review appear in the rationale text. This is useful for an AI deciding how to connect concepts across domains.

### 1.5 Summary Table: v4 Complaints Status

| v4 Priority | Complaint | Status in v5 | Notes |
|---|---|---|---|
| 1 (CRITICAL) | Wrong learner profile year | FIXED | Correct Y2 data now present |
| 2 (HIGH) | No worked examples | NOT FIXED | CVs typed as worked_example_set but contain no actual worked examples |
| 3 (HIGH) | No difficulty sub-levels | PARTIALLY | CVs have common errors but no graduated difficulty within concepts |
| 4 (HIGH) | Missing maths interaction types | NOT FIXED | Still no array builder, part-whole model, coin manipulative, clock face |
| 5 (MEDIUM) | CPA not structured data | FIXED | CPA field on every CV |
| 6 (MEDIUM) | No diagnostic question templates | NOT FIXED | Assessment questions exist but not diagnostic specifications |
| 7 (MEDIUM) | No lesson count per cluster | NOT FIXED | Still no timing guidance |
| 8 (LOW) | CC Math content not populated | NOT FIXED | Dangling references remain |
| 9 (LOW) | No domain-specific epistemic skill instantiations | NOT FIXED | |

---

## 2. Updated Ratings

### Structure: 8/10 (was 7/10, +1)

The additional layers (Content Vehicles, Thinking Lenses) add genuine structural depth. The graph now has:
- Curriculum structure (domains, objectives, concepts) -- unchanged, still excellent
- Prerequisite chains -- unchanged, still excellent
- Concept grouping (clusters with sequencing) -- unchanged, still sound
- **NEW:** Teaching packs with CPA, manipulatives, assessment -- good addition
- **NEW:** Cognitive framing per cluster -- useful addition
- Cross-domain connections with rationales -- improved

The +1 is earned by the Content Vehicles, which add a teaching-level structural layer that was entirely absent before. The Thinking Lenses contribute a smaller increment.

**Why not 9?** The structure still does not include:
- Difficulty progression within concepts (introductory/developing/secure sub-levels)
- Lesson-level granularity (no lesson count, no timing)
- Assessment gates between clusters
- Companion resource references (images, worksheets, concrete resource packs)

### Content Generation Readiness: 6/10 (was 4/10, +2)

This is the bigger shift. An AI can now generate:
- A **lesson with correct CPA progression**: The CV tells it to start with Dienes blocks, move to place value charts, then to abstract notation. This was impossible at v4.
- A **lesson with correct manipulatives**: CV001 lists exactly which concrete resources to use. No guessing.
- A **lesson that identifies common errors**: CVs list 2-3 common errors per pack. The AI can pre-emptively address these.
- A **formative assessment activity**: CV assessment questions are specific enough to generate assessment items.
- A **cognitively framed activity**: The Thinking Lens gives the AI a question stem and instructional approach.

An AI STILL cannot generate:
- A **worked example** with step-by-step narration (no worked examples in the data)
- A **differentiated lesson** with below/at/above pathways (no difficulty sub-levels)
- A **diagnostic assessment** that targets specific misconceptions with structured distractors
- A **full lesson** with timing (5 min review, 15 min input, 15 min practice, 5 min plenary)
- An **interactive activity** for half the domains (no array builder, clock face, coin manipulative, fraction wall)

The +2 reflects that the AI can now produce a structurally correct lesson with appropriate resources and CPA progression, whereas before it could only produce a narrative description. The gap from 6 to 10 is the difference between "structurally correct" and "actually usable without teacher modification."

---

## 3. Remaining Gaps

### 3.1 No Worked Examples (STILL HIGH PRIORITY)

This is my strongest recommendation from v4 and it remains unaddressed. The Content Vehicles are typed `worked_example_set` but do not contain worked examples. The Pedagogy Profile says "Worked examples: Required (Narrated with text displayed. Character models the thinking. Pause points for child to predict next step.)" but there is nothing in the data to fulfil this requirement.

A worked example for MA-Y2-C002 (place value) should look like:

> **Problem:** Show that 37 has 3 tens and 7 ones.
> **Step 1:** Place 3 ten-sticks on the place value mat, in the tens column. *"Three tens -- that is thirty."*
> **Step 2:** Place 7 unit cubes in the ones column. *"Seven ones -- that is seven."*
> **Step 3:** Record: 37 = 30 + 7. *"So 37 is the same as 30 and 7."*
> **Pause and predict:** *"Now show me 52. How many ten-sticks do you need?"*

This is not prose guidance -- it is a structured sequence with narration, actions, and a predict-point. An AI needs this to generate actual teaching content.

### 3.2 Content Vehicle Coverage Gaps

Only 5 of 8 domains have Content Vehicles:
- D001 (Number & Place Value): CV001 -- covers C002, C003 only. **C001 (counting) and C011 (odd/even) have no CV.**
- D002 (Addition & Subtraction): CV002 -- covers C004, C005, C006, C007. Complete.
- D003 (Multiplication & Division): CV003 -- covers C008, C009, C010. Complete.
- D004 (Fractions): CV004 -- covers C012, C013. Complete.
- D005 (Measurement): CV005 + CV006 -- covers C014, C015. **C016 (time) has no CV.**
- D006 (Shapes): CV007 -- covers C017, C018, C019. Complete.
- D007 (Position & Direction): **No CV at all.** C020 has no vehicle.
- D008 (Statistics): CV008 -- covers C022, C023. Complete.

**3 concepts have no Content Vehicle:** C001 (counting in steps), C011 (odd/even), C016 (time), C020 (position/direction). These are significant omissions:
- Counting in steps is the very first thing taught in Y2 Maths (Week 1, Lesson 1). An AI starting from the graph would hit a CV gap immediately.
- Telling the time is one of the most resource-intensive topics in Y2 (needs clock faces, geared clocks, clock stamps). A CV for time would be especially useful.

### 3.3 No Difficulty Sub-Levels Within Concepts

The keystone concept MA-Y2-C005 (Adding and subtracting two-digit numbers) covers an enormous range:
- 34 + 5 (TU + O, no bridging) -- straightforward
- 37 + 6 (TU + O, with bridging) -- harder
- 43 + 25 (TU + TU, no bridging) -- harder still
- 37 + 26 (TU + TU, with bridging) -- most challenging
- 42 - 17 (TU - TU, with exchange) -- the hardest subtraction

The graph treats all of this as one concept (weight 3, complexity 3). A teacher knows to teach these as 4-5 separate lessons with increasing difficulty. An AI does not know this unless told. Need: sub-levels within C005 specifying calculation types and their relative difficulty.

### 3.4 No Lesson Count or Timing Estimates

The teaching_weight property (1-6) hints at relative importance but does not translate to lesson count. In my plan, D002-CL001 (weight includes a keystone concept) took 10 lessons. D001-CL003 (single concept, weight 2) took 2 lessons. There is no heuristic in the graph to guide this allocation.

### 3.5 No Differentiation Data

My class of 30 has children working at Y1, Y2, and Y3 levels simultaneously. The graph provides a single path. Each lesson in my plan has differentiation notes that I created from experience, not from the data. Need: within-concept scaffolding (below expected) and extension (above expected) guidance, even if just a sentence each.

### 3.6 Missing Interaction Types (from v4, still missing)

Still no:
- **Array builder** -- essential for MA-Y2-C008/C009/C010 (multiplication)
- **Part-whole model / bar model** -- the most important visual model in primary maths, used in every domain
- **Coin manipulative** -- needed for MA-Y2-C015 (money)
- **Clock face** -- needed for MA-Y2-C016 (time)
- **Fraction strips/wall** -- needed for MA-Y2-C012/C013

The interaction types remain top-down (generic drag-and-drop, multiple choice) rather than concept-driven.

---

## 4. Recommendations (Prioritised)

| Priority | Recommendation | Effort | Impact | Addresses |
|---|---|---|---|---|
| 1 | **Add worked examples to Content Vehicles** (2-3 per CV, structured with steps, narration, and predict-points) | Medium | Transforms content generation from structural to instructional | Gap 3.1 |
| 2 | **Add difficulty sub-levels within C005 and other multi-type concepts** (specify calculation types as ordered difficulty tiers) | Medium | Enables differentiation and adaptive progression | Gap 3.3 |
| 3 | **Create missing Content Vehicles** for C001/C011, C016, C020 | Medium | Fills the Day 1 gap and the time topic | Gap 3.2 |
| 4 | **Add lesson count estimates** per cluster (or a formula: base count + weight multiplier) | Small | Enables automated scheme-of-work generation | Gap 3.4 |
| 5 | **Add within-concept differentiation** (one sentence each for below/at/above expected) | Medium | Enables personalised teaching paths | Gap 3.5 |
| 6 | **Add concept-driven interaction types** (array builder, bar model, coin, clock, fraction wall) | Large | Enables appropriate interactive activities for all domains | Gap 3.6 |
| 7 | **Add diagnostic question templates** per concept linking misconceptions to distractors | Medium | Enables truly diagnostic assessment generation | v4 gap, still open |
| 8 | **Differentiate lens AI instructions by age/KS** | Small | Makes lens instructions usable for actual Y2 teaching | Section 5 issue |
| 9 | **Add actual worked examples as structured data** (not just in CVs but as a reusable node type) | Large | Enables cross-vehicle, cross-domain worked example generation | Gap 3.1 extension |
| 10 | **Populate CC Math content** or remove dangling references | Small | Cleans up dead links | v4 gap, still open |

---

## 5. Content Vehicle Quality Assessment -- Y2 Maths

### 5.1 MA-Y2-CV001 -- Place Value with Dienes Blocks

**CPA stages:** Correct. Concrete (Dienes) -> pictorial (place value chart, part-whole model, number line) -> abstract is exactly the progression I used in Lessons 6-10.

**Manipulatives:** Correct and complete. Dienes blocks, place value charts, and arrow cards are the standard resources for this topic. I would add "straws bundled in tens" as an alternative concrete -- mentioned in the concept teaching guidance but not in the CV.

**Common errors:** All three are accurate:
1. "Thinking the digits represent their face value (e.g. 34 = 3 and 4, not 30 and 4)" -- the single most common Y2 place value error. Correct.
2. "Confusing tens and ones columns" -- yes, particularly when recording.
3. "Writing numbers in reverse order (e.g. writing 41 for fourteen)" -- yes, common with teen numbers specifically.

**Missing common error:** Flexible partitioning errors. Many children can partition 34 into 30 + 4 but cannot partition as 20 + 14. This is in the concept guidance but not in the CV error list. It is a significant omission because flexible partitioning is the direct prerequisite for subtraction with exchange.

**Assessment:** Good but not diagnostic. "Can pupils partition any 2-digit number into tens and ones using Dienes and without?" is a clear assessment question but does not specify what a diagnostic version would look like (e.g., asking "What does the 3 in 34 represent?" with 3 as a misconception distractor).

**Success criteria:** All four are appropriate and assessable. They progress from concrete to abstract, which mirrors the CPA stages.

**Key vocabulary:** Complete and accurate for this concept level.

**Overall:** 7/10. Structurally sound, manipulatives correct, CPA progression right. Missing flexible partitioning errors and any form of worked example.

### 5.2 MA-Y2-CV002 -- Addition and Subtraction with Number Lines

**CPA stages:** Correct. Concrete (counting objects) -> pictorial (number line jumps) -> abstract (column method introduction) is the right progression.

**Manipulatives:** Good. Dienes blocks, hundred square, bead strings (100 beads). The bead string is an excellent addition -- it is particularly good for bridging through 10 (slide beads across the ten-boundary). I would add ten frames for number bonds to 20 fluency.

**Common errors:** All three are accurate:
1. "Counting from 1 instead of counting on from the larger number" -- yes, very common.
2. "Not bridging through 10 correctly" -- yes, the key difficulty.
3. "Subtracting the smaller digit from the larger regardless of position" -- yes, the most persistent subtraction error.

**Assessment:** Good coverage. Tests number line use, commutativity understanding, and inverse checking.

**Success criteria:** Complete. All four criteria map to the concepts delivered.

**Representations:** Comprehensive. Number line, hundred square, part-whole model, bar model -- all the right pictorial representations.

**Missing:** No mention of the "counting up" strategy for subtraction (complementary addition), which is how I teach subtraction to most Y2 children before column methods. Also missing: the specific number line strategy of "bridge through 10" (e.g., 37 + 6: jump 3 to 40, then jump 3 more to 43) as a structured technique.

**Overall:** 8/10. The strongest CV in the Y2 set. Accurate manipulatives, good error coverage, comprehensive representations. Missing specific strategies.

### 5.3 MA-Y2-CV003 -- Times Tables: 2, 5 and 10

**CPA stages:** Correct. Concrete (arrays with counters) -> pictorial (array diagrams, bar models) -> abstract (multiplication/division sentences).

**Manipulatives:** Good. Counters, Numicon, Cuisenaire rods, arrays on pegboards. I would query the inclusion of Cuisenaire rods here -- they are more commonly used for fractions and number bonds than for times tables. Pegboard arrays are excellent. I would add: squared paper (for drawing arrays) and the counting stick (for rapid recall).

**Common errors:** Accurate:
1. "Confusing multiplication and addition (2 x 5 vs 2 + 5)" -- very common in early multiplication.
2. "Not understanding that division is the inverse of multiplication" -- yes.
3. "Thinking division is commutative (10 / 2 = 2 / 10)" -- yes, though this is more of a later error once children have encountered commutativity of multiplication.

**Overall:** 7/10. Sound CPA, some manipulative choices questionable. Missing link to counting in steps (the prerequisite connection to C001 that would make Autumn -> Spring progression explicit).

### 5.4 MA-Y2-CV004 -- Fractions of Shapes and Quantities

**CPA stages:** Correct. Concrete (folding paper, sharing objects) -> pictorial (shaded fraction diagrams) -> abstract (fraction notation). Paper folding is the right concrete start for fractions.

**Manipulatives:** Good. Fraction wall, paper circles/rectangles, counters, fraction tiles. I would add: fraction strips (which are different from tiles -- strips show continuous quantity, tiles show discrete).

**Common errors:** All three are real:
1. "Not making equal parts" -- fundamental fraction error.
2. "Thinking 1/3 is bigger than 1/2 because 3 > 2" -- very common; the "bigger denominator means bigger fraction" misconception.
3. "Not connecting fraction of a shape to fraction of a quantity" -- yes, this transfer is harder than expected.

**Overall:** 7/10. Solid. The equivalence work (2/4 = 1/2) is correctly flagged.

### 5.5 MA-Y2-CV005 -- Measuring Length, Mass and Capacity

**CPA stages:** Correct.

**Manipulatives:** Comprehensive and appropriate. Rulers, metre sticks, balance scales, weights, measuring jugs, thermometers -- all the standard Y2 measurement equipment.

**Common errors:** All accurate. "Reading scales incorrectly when divisions are not labelled" is the single biggest measurement error across KS1-2.

**Overall:** 7/10. Practical and usable. Missing: estimation activities, which the NC emphasises ("estimate and measure").

### 5.6 MA-Y2-CV006 -- Money: Coins, Notes and Change

**CPA stages:** Correct. Real/plastic coins -> coin images and price tags -> written calculations with symbols.

**Manipulatives:** Good. Plastic coins, price tags, shop role-play resources.

**Common errors:** Accurate. "Confusing the value of coins with their size" is correct (the 5p coin is physically larger than the 10p coin, which confuses children).

**Success criteria note:** The success criterion "Use symbols correctly (not together: 1.50 or 150p, not 1.50p)" contains a formatting issue -- it should clarify that children at this stage write "one pound and 50p" or "150p" but NOT the decimal notation "1.50" which uses decimal points not yet taught. The current wording could confuse an AI into generating decimal notation questions.

**Overall:** 7/10. Good real-world application. The success criterion formatting needs attention.

### 5.7 MA-Y2-CV007 -- 2-D and 3-D Shapes

**CPA stages:** Correct. Handling shapes -> sorting diagrams -> describing with vocabulary.

**Common errors:** The error "Thinking a square is not a rectangle" is important to flag -- this is a common teacher misconception as well as a pupil one. (A square IS a special case of a rectangle.) Good that this is included.

**Overall:** 7/10. Sound.

### 5.8 MA-Y2-CV008 -- Statistics: Pictograms and Tally Charts

**CPA stages:** Correct. Sorting real objects -> pictograms/block diagrams -> answering questions from data.

**Common errors:** All accurate. "Pictogram symbols not equal size or spacing" is the construction error I see most often.

**Overall:** 7/10. Practical and usable.

---

## 6. Thinking Lens Quality Assessment -- Y2 Maths

### 6.1 Lens Assignments (Are the right lenses assigned to the right clusters?)

| Cluster | Primary Lens | Correct? | Secondary Lens | Correct? |
|---|---|---|---|---|
| D001-CL001 (Counting/Odd-Even) | Patterns | YES | Cause and Effect | DEBATABLE |
| D001-CL002 (Place Value) | Patterns | YES | Scale/Proportion/Quantity | YES |
| D001-CL003 (Patterns) | Patterns | YES | Evidence and Argument | YES |
| D002-CL001 (Add/Sub Facts) | Patterns | YES | Scale/Proportion/Quantity | YES |
| D002-CL002 (Properties) | Patterns | YES | Cause and Effect | YES |
| D003-CL001 (Times Tables) | Scale/Prop/Qty | DEBATABLE | Patterns | YES |
| D003-CL002 (Commutativity) | Scale/Prop/Qty | DEBATABLE | Patterns | YES |
| D005-CL001 (Measurement) | Scale/Prop/Qty | YES | Structure and Function | DEBATABLE |
| D005-CL002 (Money) | Patterns | DEBATABLE | Cause and Effect | NO |
| D005-CL003 (Time) | Scale/Prop/Qty | DEBATABLE | Structure and Function | YES |
| D006-CL001 (Shape Properties) | Structure and Function | YES | Scale/Prop/Qty | NO |
| D006-CL002 (2-D on 3-D) | Structure and Function | YES | Scale/Prop/Qty | NO |
| D007-CL001 (Position/Direction) | Structure and Function | YES | Scale/Prop/Qty | DEBATABLE |
| D008-CL001 (Statistics - Construct) | Patterns | YES | Evidence and Argument | YES |
| D008-CL002 (Statistics - Question) | Patterns | YES | Evidence and Argument | YES |

**Primary lens assignments are mostly correct.** Patterns is right for number work. Structure and Function is right for geometry. Scale/Proportion/Quantity is right for measurement.

**Issues:**
- D003-CL001 (Times Tables): Primary lens is Scale/Proportion/Quantity, but for Y2 the tables are about PATTERN recognition (2, 4, 6, 8... / 5, 10, 15, 20...) not proportional reasoning. Patterns should be primary here. Scale/Prop/Qty makes sense for Y4+ multiplication where proportional reasoning is explicit.
- D005-CL002 (Money): Patterns as primary lens is weak. Money problems at Y2 are about practical calculation, not pattern recognition. Structure and Function (how coins combine to make amounts) or even no lens would be better than forcing Patterns.
- D006 secondary lens Scale/Prop/Qty: "Similarity, enlargement and trigonometry" in the rationale is clearly a KS3/4 rationale, not a Y2 one. This has been copy-pasted from the wrong key stage.

### 6.2 Lens Rationale Quality

The rationales on the APPLIES_LENS relationships are **mixed quality.** Some are genuinely cluster-specific:

> D001-CL002 Patterns: "Place value is the positional pattern in our base-10 number system -- pupils recognise how each digit's value follows a regular, predictable rule they can extend indefinitely."

This is a good rationale. It explains WHY Patterns fits THIS cluster, not just patterns in general.

Others are clearly templated and not cluster-specific:

> D005-CL001 Scale/Prop/Qty: "Area, volume and perimeter formulae encode how measurements scale -- doubling a dimension does not double all quantities, making proportional reasoning essential."

This is a KS3 rationale applied to a Y2 measurement cluster about reading rulers and thermometers. Year 2 children are not working with area formulae. The rationale has been generated from the lens description, not from the cluster content.

> D005-CL002 Patterns: "Algebraic manipulation relies on recognising structural patterns -- equivalent forms, factorisation rules, and the symmetry of operations -- that apply consistently."

This is a KS4 algebra rationale applied to a Y2 money cluster. It is completely wrong for the context.

**This is a significant quality issue.** The rationales appear to have been generated at the subject level (Mathematics) and then applied uniformly to all clusters without age differentiation. For Y2, about half the rationales are age-inappropriate.

### 6.3 AI Instructions

The AI instructions are **functional but not age-differentiated.** Every instance of the Patterns lens has the same instruction regardless of whether it is applied to Y2 counting or Y9 algebra:

> "Use the PATTERNS lens: prompt pupils to notice what repeats or follows a rule, classify examples by shared features, identify exceptions, and predict what comes next."

"Classify examples by shared features" is reasonable language for KS3. It is not how a Y2 teacher speaks. The instruction should say: "Ask: What do you notice? Can you see a pattern? What will come next? Can you explain the pattern to your partner?"

### 6.4 Summary

Thinking Lenses are a genuinely useful structural addition. The primary lens assignments are mostly correct. The secondary assignments and the rationales have quality problems due to insufficient age differentiation. The AI instructions are functional but generic.

**Rating: 6/10 for concept; 4/10 for execution at Y2 level.**

---

## 7. Overall Verdict

### What is genuinely better

1. **Content Vehicles give an AI structured teaching resources for the first time.** CPA progressions, manipulative lists, common errors, and success criteria are all queryable data. This transforms content generation from "describe the topic" to "design a lesson with appropriate resources."
2. **The learner profile bug is fixed.** Y2 children now get Y2-appropriate content parameters.
3. **Thinking Lenses give cognitive framing.** The Patterns lens key question is a usable teaching tool.
4. **Cross-domain links have rationales.** An AI can now explain WHY it is connecting place value to addition.

### What is not good enough yet

1. **No worked examples anywhere.** The pedagogy profile demands them; the data does not contain them. This is the biggest remaining gap.
2. **Content Vehicles have inconsistent coverage.** 3 concepts have no CV at all, including the first topic of the year.
3. **Thinking Lens rationales are often age-inappropriate.** KS3/4 language applied to KS1 clusters.
4. **No difficulty progression within concepts.** C005 covers 5 distinct calculation types of increasing difficulty, but the graph treats it as one concept.
5. **No differentiation data.** Single path, no scaffolding or extension guidance.
6. **Still missing concept-driven interaction types** for multiplication, money, time, and fractions.

### The score in context

| Aspect | v4 | v5 | Change | Notes |
|---|---|---|---|---|
| Structure | 7/10 | 8/10 | +1 | CVs and lenses add genuine depth |
| Content generation readiness | 4/10 | 6/10 | +2 | CVs transform resource specification; still no worked examples |

**The 70% problem from v4 is now closer to 80%.** The Content Vehicles add the CPA and resource layer that was missing. But the final 20% -- worked examples, difficulty progression, differentiation, diagnostic assessment -- is the 20% that makes the difference between "an AI that can describe a structurally correct lesson" and "an AI that can TEACH a structurally correct lesson."

### Can an AI generate content from this data today?

- **A quiz?** Better than v4. CVs provide common errors that can inform distractors. Still no diagnostic question templates, but an AI could construct plausible items from the CV error list. **5/10.**
- **A lesson?** Significantly better. The CPA progression, manipulatives, and success criteria give structure. The Thinking Lens gives cognitive framing. But without worked examples, the AI can say "start with Dienes blocks" but cannot model the actual teaching sequence. **6/10.**
- **A slide deck?** Still limited. No images, no worked examples, no specific visual resources. The CPA field tells you WHAT to show but not HOW to show it. **4/10.**
- **A scheme of work?** The cluster structure, CVs, and lens assignments get you to about 80%. Still no lesson counts, no differentiation, and 3 concepts have no CV. **7/10.**
- **An adaptive AI session?** The learner profile is now correct, which is essential. The pedagogy profile demands worked examples and spacing. The CV success criteria define mastery targets. But no difficulty sub-levels means the AI cannot adapt within a concept. **5/10.**

---

## 8. Closing Statement

The graph has made genuine progress. Content Vehicles are the right architectural choice -- teaching packs with structured CPA, manipulatives, and assessment criteria are exactly what was needed. Thinking Lenses add a cognitive dimension that enriches the teaching model. The learner profile fix removes a critical bug.

The remaining work is not architectural -- the architecture is sound. It is content quality work: filling in worked examples, grading difficulty within concepts, differentiating lens rationales by age, adding missing vehicles, and building concept-driven interaction types. This is the kind of work that requires subject specialist input, not more graph engineering.

If I were advising the team on next steps: **hire a Y2 maths specialist for two weeks to write worked examples and difficulty progressions for CV001-CV008.** That single intervention would move content generation readiness from 6/10 to 8/10. Everything else is incremental.

---

*James Henderson, Maths Lead*
*"The architecture is right. The content needs filling in. Get a teacher to do it."*
