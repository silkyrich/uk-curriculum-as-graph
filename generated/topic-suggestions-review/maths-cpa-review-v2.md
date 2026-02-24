# CPA Model Implementation Review -- Revised Assessment

**Reviewer**: Henderson (Y2-Y6 Maths Lead, White Rose Maths / NCETM Mastery trained)
**Date**: 2026-02-24
**What changed**: Project lead clarified that this graph is a **curriculum intelligence graph** -- it encodes how experienced teachers teach, not where individual children are. A separate runtime graph (not yet built) will map a specific child's position.

---

## Revised Overall Assessment: 8.5/10 (up from 7/10)

I was wrong about what this graph is for, and that error inflated the gap between what was built and what I thought was needed. Let me explain.

My original review scored 7/10 largely because:
- RepresentationStage is bound to Concept rather than DifficultyLevel (-1.5)
- No cyclical CPA re-entry model (-1.0)
- Missing manipulative/representation nodes as first-class entities (-0.5)

The project lead's clarification forces me to reconsider all three. This graph is not deciding what a child should do next. It is encoding what a well-trained teacher knows about how to teach each concept. The question is not "where is child A on the CPA cycle?" but "what does the CPA teaching approach look like for this concept?"

With that framing, the current `RepresentationStage` implementation is significantly closer to the right design than I originally assessed.

---

## 1. The DifficultyLevel Binding (Reconsidered)

### What I originally said

"This is the most significant structural divergence. CPA should be per-difficulty-level, not per-concept." I proposed `(:DifficultyLevel)-[:HAS_CPA_PATHWAY]->(:CPAPathway)` -- one CPA pathway per difficulty level per concept, yielding ~500-600 CPAPathway nodes.

### What I now think

The DifficultyLevel binding is **mostly already solved by the existing data, and the explicit link I proposed belongs in the runtime graph, not here.**

Look at what the curriculum graph already encodes for MA-Y3-C014 (column addition):

**RepresentationStage data** (per concept):
- Concrete: Dienes blocks, exchanging physically
- Pictorial: Drawn place value counters, expanded column method
- Abstract: Compact columnar notation with carried digits

**DifficultyLevel data** (per concept):
- Entry: "Adding two three-digit numbers using Dienes blocks, physically regrouping"
- Developing: "Setting out columnar addition on paper... with a place value grid for support"
- Expected: "Fluent columnar addition... without support"
- Greater depth: "Adding where the result exceeds 1000, checking with estimation"

The DifficultyLevel descriptions already encode the CPA stage implicitly. Entry says "Dienes blocks" (concrete). Developing says "on paper with a place value grid" (pictorial). Expected says "without support" (abstract). An AI reading both RepresentationStage and DifficultyLevel for the same concept has all the information it needs to match difficulty level to CPA stage.

**My original proposal would have created ~500 CPAPathway nodes that explicitly state what is already inferable from the intersection of two existing datasets.** That is redundant in a curriculum intelligence graph.

The explicit binding ("child A is at entry, therefore use concrete") is a runtime decision. It belongs in the adaptive engine that maps a child's current position to the curriculum graph's teaching guidance. This graph says "here is what concrete looks like for column addition, here is what pictorial looks like, here is what abstract looks like, and here are the difficulty levels that describe the progression." The runtime system decides which combination to deploy for a specific child.

### What still matters

There is one piece of curriculum intelligence that the current model does not capture: the **typical CPA-DifficultyLevel correspondence**. The graph says "entry means X" and "concrete means Y" but it does not say "entry typically corresponds to concrete for this concept." An experienced teacher knows this mapping. The AI must infer it from the text of both nodes.

**Revised recommendation**: Add a lightweight `typical_cpa_emphasis` property to each DifficultyLevel node for Maths concepts. Values: `concrete`, `pictorial`, `abstract`, `mixed`. This is curriculum intelligence (it encodes what experienced teachers know about where the CPA emphasis falls at each difficulty level). It is not child tracking. It costs one property per DifficultyLevel, not 500 new nodes.

This is now **Priority 2** rather than Priority 1, because the DifficultyLevel descriptions already encode this implicitly and a well-prompted AI can infer the mapping.

---

## 2. The Cyclical CPA Re-Entry Model (Reconsidered)

### What I originally said

"The current model enforces the linear misconception. No mechanism for re-entry, stage skipping, or reverse pathways." I proposed `is_reentry: true` and `reentry_trigger` properties on CPAPathway nodes bound to DifficultyLevel.

### What I now think

**The cyclical CPA model absolutely matters as curriculum intelligence, but the granularity I proposed was wrong.**

Re-entry is a fact about how experienced teachers teach certain concepts. It is not a fact about an individual child. "When children encounter cascading exchange across zero in column subtraction, they typically need to return to concrete Dienes blocks even if they have been working abstractly" -- this is curriculum intelligence. It describes what happens in classrooms, not what should happen to child A.

But my proposal encoded this at the wrong level. I proposed per-DifficultyLevel CPAPathway nodes with `is_reentry: true` and specific `reentry_trigger` values. This is too granular for a curriculum graph. It is really saying "when this specific child hits this specific difficulty level and encounters this specific obstacle, cycle them back to concrete." That is an adaptive runtime decision.

What the curriculum graph should encode is the **general teaching knowledge** about re-entry points:

- "Column subtraction: cascading exchange across zero is a known re-entry point. Expect children to need pictorial or concrete support at this stage, regardless of their general difficulty level."
- "Fraction equivalence: non-obvious equivalences (e.g. 3/5 = 6/10) commonly trigger a return to fraction tiles."
- "Times table fluency: this is an abstract-only concept. Do not default to concrete for fluency practice."

This is teacher knowledge. It belongs in the curriculum graph. But it belongs as **teaching notes on the RepresentationStage or on the Concept**, not as routing logic on a per-DifficultyLevel pathway node.

### Revised recommendation

Add optional `teaching_notes` to the RepresentationStage JSON (or as a property on the Concept node). These would include:

- `reentry_points`: Known points where children commonly need to cycle back to a more concrete stage. Free text describing what triggers this and what to do. E.g. "Cascading exchange across zero (e.g. 600 - 347) commonly causes procedural breakdown. Return to Dienes blocks briefly to rebuild the exchange chain visually, then move back to written method."
- `fluency_note`: Whether this concept has a fluency-focused CPA pattern. E.g. "Times table recall should be practised abstractly. Concrete resources are for understanding multiplication, not for fluency drill."
- `stage_exceptions`: Any concept-specific deviations from the standard C-P-A linear progression. E.g. "Y6 mathematical reasoning/proof: the three 'stages' here represent maturity levels (pattern-spotting, diagrammatic justification, algebraic proof) rather than literal CPA stages."

This is **Priority 2**. It is genuine curriculum intelligence that the AI cannot easily infer from the existing data. But it is free-text teaching notes on existing nodes, not a new node type with routing logic.

---

## 3. RepresentationStage vs CPAPathway: Which Is the Right Design?

### What I originally proposed

`CPAPathway` -- a node per concept per difficulty level, representing a specific route through CPA with direction, re-entry capability, and links to manipulatives and representations as first-class nodes.

### What I now think

**RepresentationStage at the Concept level is the right design for a curriculum intelligence graph.**

Here is why. The curriculum graph answers: "For column addition, what does concrete teaching look like? What does pictorial teaching look like? What does abstract teaching look like? What resources does each stage use? What signals readiness to move between stages?"

These are concept-level questions. They do not change based on which child is being taught. The concrete stage for column addition uses Dienes blocks and place value mats regardless of whether the child is at entry or greater depth. What changes is which stage the child is working in -- and that is a runtime question, not a curriculum question.

`RepresentationStage` answers the curriculum question correctly:
- Stage 1 (concrete): here is what concrete looks like for this concept, with these resources and this transition cue
- Stage 2 (pictorial): here is what pictorial looks like, with these resources and this transition cue
- Stage 3 (abstract): here is what abstract looks like

`CPAPathway` was designed to answer a mixed question: "For this concept, at this difficulty level, which CPA stages should be traversed in which order?" That mixes curriculum intelligence (what concrete looks like) with runtime routing (which stages this child should traverse). The routing belongs in the adaptive engine.

### The naming question

I said in my original review "keep RepresentationStage, it accurately names what exists." I still stand by this. The node IS a representation stage. It is not a pathway. The name is correct.

### What RepresentationStage could still gain

Two properties would make it a more complete encoding of curriculum teaching knowledge:

1. `is_default_entry`: boolean. For most concepts, stage 1 (concrete) is the default entry point. But for fluency concepts (times tables recall), stage 3 (abstract) is the default. This flag tells the AI which stage an experienced teacher would typically start with. This is curriculum intelligence, not child tracking.

2. `teaching_notes`: free text. Per-stage notes that encode experienced teacher knowledge. E.g. on the concrete stage for column subtraction: "When the child encounters cascading exchange across zero, expect them to need extended time at this stage. This is not regression -- it is the normal learning curve for this sub-skill."

---

## 4. MathsManipulative and MathsRepresentation as First-Class Nodes (Reconsidered)

### What I originally proposed

~25-30 MathsManipulative nodes and ~30-35 MathsRepresentation nodes as first-class entities in the graph, with progression chains (PROGRESSES_TO) and concept links.

### What I now think

**This is the one part of my original proposal that I still fully endorse, and it is even more important under the curriculum-intelligence framing.**

Manipulatives and representations are curriculum knowledge, not child-level data. The question "which manipulatives does a Y3 teacher need for addition and subtraction?" is a curriculum question. "How does the number line representation change from Y1 to Y6?" is a curriculum question. "Is Numicon available as a virtual manipulative?" is a curriculum question.

These questions cannot be answered from the current data because manipulatives and representations are embedded as string arrays in RepresentationStage resources. The strings are human-readable but not machine-queryable. You cannot run "MATCH (m:MathsManipulative) WHERE m.primary_year_range = 'Y1-Y3' RETURN m" because there are no MathsManipulative nodes.

Moreover, under the curriculum-intelligence framing, these nodes become MORE valuable, not less. They are pure curriculum metadata:

- **MathsManipulative**: "Dienes blocks are a proportional base-10 manipulative, primarily used Y1-Y3 with secondary use Y4-Y6 for decimals. They are available as a virtual manipulative. The agent prompt for describing Dienes in lessons is [X]."
- **MathsRepresentation**: "The bar model is a diagrammatic representation that foregrounds part-whole relationships. In Y1 it is used with known totals; by Y5 it supports ratio and proportion. Variants by year: [structured list]."

None of this is child data. It is pure teacher knowledge.

### Revised recommendation

**Priority 1** (moved up from Priority 2): Extract MathsManipulative and MathsRepresentation as first-class nodes.

The data already exists in the RepresentationStage resources arrays. The extraction is:
1. Compile a controlled vocabulary from all 154 concepts' resources lists (~25-30 unique manipulatives, ~30-35 unique representations)
2. Create node definitions with properties: `name`, `description`, `manipulative_type` / `representation_type`, `primary_year_range`, `is_virtual_available`, `agent_prompt`
3. Create `(:RepresentationStage)-[:USES_RESOURCE]->(:MathsManipulative|MathsRepresentation)` relationships
4. Add `PROGRESSES_TO` chains where progression is clear (Numicon -> Dienes -> place value counters)

This adds ~60 nodes and ~400 relationships. It makes the curriculum graph answer questions it currently cannot.

---

## 5. My "What I Would Use in a Lesson Tomorrow" Section (Reconsidered)

This is the most important reconsideration. In my original review, Section 10 listed four things "the AI cannot tell me." Let me re-examine each one through the curriculum-intelligence lens.

### 5.1 "This child is at developing level, so they should be bridging from concrete to pictorial"

**Original**: Listed as something the AI cannot tell me.

**Revised**: This is a **runtime decision**, not curriculum intelligence. The curriculum graph says "here is what concrete looks like, here is what pictorial looks like, here is the transition cue." The runtime system knows "this child is at developing level" and can match that to the appropriate stage. The graph does not need to make this link explicit -- the adaptive engine does.

**Verdict**: Correctly absent from the curriculum graph. No change needed.

### 5.2 "The primary manipulative is counters; fraction circles are support. If you do not have fraction circles at home, use folded paper strips instead."

**Original**: Listed as something the AI cannot tell me.

**Revised**: This IS curriculum intelligence. "Counters are the primary manipulative for this stage; fraction circles are supplementary" is experienced teacher knowledge, not child data. "If you don't have fraction circles, folded paper strips are a substitute" is a curriculum planning fact. Both belong in the graph.

The current RepresentationStage lists resources as a flat array with no primary/secondary distinction. With MathsManipulative as first-class nodes, you could have `USES_RESOURCE` with `{role: 'primary'}` and `{role: 'support'}`, plus `alternative_for` relationships between manipulatives.

**Verdict**: Genuine gap in the curriculum graph. Addressed by MathsManipulative nodes (Priority 1 above).

### 5.3 "This is a conceptual introduction, not a fluency lesson -- do not drill, explore."

**Original**: Listed as something the AI cannot tell me.

**Revised**: This is curriculum intelligence. Whether a concept is best taught as conceptual introduction or fluency practice is a curriculum design decision. It does not depend on the child. Column addition is always a conceptual introduction (it requires understanding of exchange). Times table recall is always a fluency concept (it requires automaticity, not new understanding).

This could be a property on Concept or ConceptCluster: `nc_aim_emphasis` (fluency / reasoning / problem_solving / mixed). It is a fixed curriculum fact.

**Verdict**: Genuine gap. Lightweight fix: add `nc_aim_emphasis` property to ConceptCluster. Priority 2.

### 5.4 "If the child gets stuck on non-obvious equivalences at expected level, return to concrete with fraction tiles. This is expected, not a regression."

**Original**: Listed as something the AI cannot tell me.

**Revised**: This requires splitting in two:

The **curriculum intelligence** part is: "Non-obvious equivalences commonly trigger a return to concrete. This is a known re-entry point, not a regression." This is teacher knowledge. It belongs in the graph as a teaching note on the RepresentationStage or Concept.

The **runtime** part is: "This specific child got stuck on non-obvious equivalences." That is an event in the adaptive system, not a fact in the curriculum graph.

**Verdict**: Half curriculum intelligence (the re-entry point knowledge), half runtime (the child's specific difficulty). The curriculum half belongs as a `teaching_notes` property on RepresentationStage. Priority 2.

---

## 6. The ~500 CPAPathway Nodes Question

### What I originally proposed

~500-600 CPAPathway nodes, one per concept per difficulty level. Each encoding entry_stage, target_stage, stage_sequence, is_reentry, reentry_trigger, transition_guidance.

### What I now think

**These belong in the runtime child graph, not in the curriculum intelligence graph.**

A CPAPathway that says "for MA-Y3-C014 at entry level, start at concrete and target pictorial" is encoding a routing decision. It presupposes a child at entry level and prescribes their route. That is the adaptive engine's job.

The curriculum graph should encode:
1. What concrete teaching looks like for this concept (RepresentationStage -- DONE)
2. What pictorial teaching looks like (RepresentationStage -- DONE)
3. What abstract teaching looks like (RepresentationStage -- DONE)
4. What signals readiness to move between stages (transition cues -- DONE)
5. What known re-entry points exist (teaching notes -- Priority 2, not done)
6. Which manipulatives and representations are used (MathsManipulative/MathsRepresentation nodes -- Priority 1, not done)
7. Whether this concept is fluency-focused or conceptual (nc_aim_emphasis -- Priority 2, not done)

Items 1-4 are already built. Items 5-7 are lightweight additions (properties and ~60 reference nodes). The ~500 CPAPathway nodes were trying to do item 1-4 AND make routing decisions simultaneously. Under the curriculum-intelligence framing, they are unnecessary.

**The runtime child graph** would contain nodes like:
- `(:ChildConceptState {child_id, concept_id, current_difficulty_level, current_cpa_stage, last_updated})`
- `(:CpaRoute {entry_stage, target_stage, stage_sequence})` -- THIS is where the CPAPathway logic lives

But that graph does not exist yet. When it is built, it will query the curriculum graph for "what does concrete look like for column addition?" and combine that with the child's state to create a personalised route. The curriculum graph provides the teaching knowledge. The runtime graph provides the child-specific routing.

---

## 7. MathsContext and ReasoningPromptType (Reconsidered)

### MathsContext

**Original assessment**: Priority 3.

**Revised assessment**: Still Priority 3, but the framing is cleaner. MathsContext nodes ("shopping", "cooking", "map reading") are curriculum intelligence -- they encode which real-world contexts work for which mathematical concepts, with safeguarding notes and age-suitability. None of this is child data. It is teacher planning knowledge.

The ContentVehicle layer already provides some of this via `worked_example_set` vehicles. MathsContext nodes would complement rather than replace these.

### ReasoningPromptType

**Original assessment**: Priority 3.

**Revised assessment**: Elevated to **Priority 2**. Under the curriculum-intelligence framing, ReasoningPromptType nodes are pure curriculum metadata. They encode "Always-Sometimes-Never is developmentally appropriate from Y3, and here is the question template." This is exactly the kind of experienced teacher knowledge that the curriculum graph should capture. It does not reference individual children.

The ThinkingLens layer already provides cognitive framing. ReasoningPromptType adds question-level structure. They are complementary: ThinkingLens says "frame this through Patterns," ReasoningPromptType says "ask an Always-Sometimes-Never question about this pattern."

~10-12 nodes with `APPROPRIATE_FOR` links to KeyStage. Lightweight, high value.

---

## 8. Revised Scoring

| Dimension | Original Score | Revised Score | Change | Rationale |
|---|---|---|---|---|
| Coverage | 10/10 | 10/10 | -- | 154/154 primary Maths concepts. Still perfect. |
| Data quality | 9/10 | 9/10 | -- | Still excellent. Minor issues noted in v1 still apply. |
| Schema design | 6/10 | 8/10 | +2 | The Concept-level binding is correct for a curriculum intelligence graph. The DifficultyLevel binding I wanted is a runtime concern. |
| Integration | 8/10 | 8/10 | -- | Query helpers still surface CPA data correctly. |
| Ontology completeness | 4/10 | 6/10 | +2 | Reframed: the missing CPAPathway nodes are runtime concerns, not curriculum gaps. The genuine curriculum gaps are MathsManipulative/MathsRepresentation nodes and teaching notes. |
| Pedagogical fidelity to CPA model | 5/10 | 8/10 | +3 | The linear 1-2-3 model is correct for a curriculum graph. The curriculum describes what each stage looks like. The cyclical routing is a runtime concern. Re-entry knowledge can be added as teaching notes without restructuring. |
| **Overall** | **7/10** | **8.5/10** | **+1.5** | **The implementation is closer to the right design than I originally assessed. The main genuine gap is MathsManipulative/MathsRepresentation as first-class nodes.** |

### Why +1.5, not +3

The reframing solves the DifficultyLevel binding question (+2 in schema, +3 in pedagogical fidelity) but reveals that I was looking at the right problem from the wrong angle. The genuine curriculum intelligence gaps remain:

1. Manipulatives and representations are strings, not queryable nodes (-0.5 from perfect)
2. No teaching notes for re-entry points, fluency flags, or stage exceptions (-0.5)
3. No nc_aim_emphasis signal (-0.25)
4. No ReasoningPromptType nodes (-0.25)

These are real gaps in curriculum intelligence. They are just smaller and simpler to fix than what I originally proposed.

---

## 9. Revised Recommendations (Prioritised)

### Priority 1: MathsManipulative and MathsRepresentation as first-class nodes
**What**: Extract ~25-30 MathsManipulative nodes and ~30-35 MathsRepresentation nodes from existing RepresentationStage resource arrays.
**Why**: This is the single largest gap in the curriculum intelligence graph for Maths. The data exists but is trapped in string arrays. First-class nodes make it queryable: "which manipulatives does a Y3 teacher need?", "is this manipulative available virtually?", "what progresses from Numicon?"
**Effort**: Moderate. Controlled vocabulary extraction, node definitions, import script, relationship creation.
**This is curriculum intelligence**: Yes. Manipulatives and representations are curriculum planning entities, not child data.

### Priority 2: Teaching notes on RepresentationStage
**What**: Add optional `teaching_notes` to RepresentationStage JSON. Include: `reentry_points` (known re-entry triggers), `fluency_note` (whether abstract-only), `stage_exceptions` (deviations from standard CPA).
**Why**: Encodes experienced teacher knowledge about non-linear CPA patterns. The AI currently has no signal for "times tables should be drilled abstractly" or "cascading exchange is a known re-entry point."
**Effort**: Low. Property additions to existing JSON files, no schema changes.
**This is curriculum intelligence**: Yes. These are facts about how concepts are taught, not about how individual children learn.

### Priority 2 (tied): ReasoningPromptType nodes
**What**: ~10-12 nodes encoding reasoning question patterns with age-appropriateness, question templates, and examples.
**Why**: Pure curriculum metadata. Complements ThinkingLens (cognitive framing) with question-level structure (task format).
**Effort**: Low. Small fixed node set, APPROPRIATE_FOR links to KeyStage.
**This is curriculum intelligence**: Yes. "Always-Sometimes-Never is appropriate from Y3" is a curriculum fact.

### Priority 2 (tied): nc_aim_emphasis on ConceptCluster
**What**: A single enum property (`fluency` / `reasoning` / `problem_solving` / `mixed`) on each Maths ConceptCluster.
**Why**: Tells the AI whether to drill, explore, or problem-solve. This is a curriculum design decision, not a child-level decision.
**Effort**: Low. One property per Maths cluster (~60 values to set).
**This is curriculum intelligence**: Yes. "Column addition is a conceptual introduction" is a curriculum fact.

### Priority 3: MathsContext nodes
**What**: ~15-20 reusable real-world context nodes with safeguarding notes and age-suitability.
**Why**: Curriculum planning knowledge. Prevents the AI from overusing one context or choosing age-inappropriate ones.
**Effort**: Low-moderate.
**This is curriculum intelligence**: Yes.

### Priority 3: typical_cpa_emphasis on DifficultyLevel
**What**: A single property (`concrete` / `pictorial` / `abstract` / `mixed`) on each DifficultyLevel for Maths concepts.
**Why**: Makes the implicit CPA-DifficultyLevel mapping explicit. Currently inferable from DL descriptions but not machine-readable.
**Effort**: Low.
**This is curriculum intelligence**: Yes, borderline. It is a heuristic about typical teaching emphasis, not a child-level decision.

### Removed from curriculum graph recommendations

The following items from my original proposal should be built in the **runtime child graph**, not here:

| Original Proposal | Why It Belongs in Runtime |
|---|---|
| CPAPathway node (~500 nodes) | Routes a child through CPA stages -- that is adaptive, not curriculum |
| `(:DifficultyLevel)-[:HAS_CPA_PATHWAY]->(:CPAPathway)` | Binds a child's difficulty level to a CPA route -- adaptive |
| `is_reentry` flag on CPAPathway | Decides whether a specific child should re-enter concrete -- adaptive |
| `reentry_trigger` on CPAPathway | Triggers a specific child's re-entry -- adaptive |
| `entry_stage` / `target_stage` on CPAPathway | Defines a child's start and end point in CPA -- adaptive |
| `stage_sequence` on CPAPathway | Orders a child's CPA traversal -- adaptive |

The curriculum intelligence versions of these concepts (general re-entry knowledge, fluency patterns) are captured by the teaching_notes property in Priority 2 above.

---

## 10. What I Would Use in a Lesson Tomorrow (Revised)

The original version of this section mixed curriculum questions with child-tracking questions. Here is the clean split:

### What the curriculum graph tells me now (and should continue to tell me)

- "For column addition (MA-Y3-C014), concrete means Dienes blocks on a place value mat, exchanging 10 ones for 1 ten physically. Pictorial means drawn place value counters with the expanded column method. Abstract means compact columnar notation."
- "The transition from concrete to pictorial is signalled when the child completes 3 additions with exchange without prompting, articulating the exchange verbally each time."
- "At entry difficulty, the teaching emphasis is on physical regrouping with Dienes. At expected difficulty, the teaching emphasis is on fluent columnar addition without support."

### What the curriculum graph should also tell me (Priority 1-2 additions)

- "The primary manipulative for the concrete stage is Dienes blocks. Multilink cubes are a secondary option for children who struggle with the proportional representation." (MathsManipulative nodes)
- "The bar model is the primary pictorial representation for this cluster. Number lines are an alternative." (MathsRepresentation nodes)
- "Cascading exchange across zero is a known re-entry point. Expect children working abstractly to need pictorial support when they first encounter 600 - 347." (teaching_notes)
- "This is a conceptual introduction cluster, not a fluency cluster. Explore and discuss, do not drill." (nc_aim_emphasis)
- "Ask an Always-Sometimes-Never question: 'When you add two three-digit numbers, the answer is always a four-digit number.' Y3 appropriate." (ReasoningPromptType)

### What the curriculum graph should NOT tell me (runtime concerns)

- "This child is at developing level, so start at pictorial." -- Runtime.
- "This child got stuck on cascading exchange, so cycle back to concrete." -- Runtime.
- "This child has been at the concrete stage for 3 sessions, so push towards pictorial." -- Runtime.
- "This child mastered the transition cue, so advance to the next stage." -- Runtime.

The curriculum graph provides the **teaching playbook**. The runtime graph decides which page to open for which child.

---

## 11. Final Reflection

I came into this review thinking about individual children because that is what I think about every day in my classroom. When I plan a lesson, I think "Maisie needs concrete, Jayden is ready for abstract, and the middle table should be bridging pictorial." My ontology was designed to encode those per-child decisions.

The project lead is right: those decisions are runtime. The curriculum graph should encode what I KNOW about teaching column addition that lets me make those decisions. It should encode:

- What Dienes blocks are and how to use them for this concept
- What the place value chart looks like and when to introduce it
- What the compact method looks like and what readiness signals to watch for
- That cascading exchange is a known stumbling block
- That this is an understanding concept, not a fluency concept
- That "Spot the Mistake" and "Always-Sometimes-Never" are good reasoning prompt formats for this cluster

The current RepresentationStage implementation captures the first four of these. With the additions I have proposed (MathsManipulative/MathsRepresentation nodes, teaching notes, nc_aim_emphasis, ReasoningPromptType), it would capture all six.

The per-child routing -- CPAPathway with entry_stage, target_stage, stage_sequence, and is_reentry -- will be important. But it will be important in the runtime graph that does not exist yet. When that graph is built, it should consume the curriculum graph's teaching knowledge and combine it with each child's state. The curriculum graph provides the what-and-how. The runtime graph provides the who-and-when.

This is a cleaner separation of concerns than what I originally proposed, and the implementation is closer to right than I gave it credit for.

**Revised overall: 8.5/10. The right first step is actually a good step, not just a first one.**
