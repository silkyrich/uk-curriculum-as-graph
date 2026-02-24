# CPA Model Implementation Review

**Reviewer**: Henderson (Y2-Y6 Maths Lead, White Rose Maths / NCETM Mastery trained)
**Date**: 2026-02-24
**What I reviewed**: The `RepresentationStage` layer vs my proposed Maths ontology

---

## Overall Assessment: 7/10

This is a solid first iteration that gets the most important thing right: **every primary Maths concept now has concrete, pictorial and abstract stage data that an AI tutor can actually use**. The data quality is excellent -- I read files across Y1, Y2, Y3, Y4, Y5 and Y6, and the descriptions are pedagogically accurate, the resources are age-appropriate, and the transition cues reflect genuine mastery assessment criteria. The query integration is clean: both `query_cluster_context.py` and `graph_query_helper.py` surface CPA stages directly under each concept in the lesson generation context.

However, this implementation captures approximately 30% of what I proposed. It delivers the **most urgent** 30% -- the per-concept CPA descriptions -- but it does not deliver the structural model I designed. The naming, the relationship to DifficultyLevel, the cyclical CPA model, and four of my five proposed node types are absent. These are not cosmetic gaps; they are pedagogical gaps that will limit what the AI can do.

I would characterise this as: **"CPA descriptions delivered; CPA ontology deferred."**

---

## 1. What Is Good and Should Be Kept

### 1.1 Complete Y1-Y6 coverage (154/154 concepts) -- Excellent

Every primary Maths concept has CPA data. The coverage is 100%. This is the single most important metric. A partially covered CPA layer would be worse than no CPA layer at all, because the AI would have CPA guidance for some concepts and not others, leading to inconsistent lesson quality. Full coverage was the right call.

### 1.2 Data quality is high

I read files covering Y1 (counting, place value, addition, fractions, measurement, geometry, time, money), Y2 (place value, operations, fractions, measurement, shape, statistics), Y3 (all 7 domains), Y4, Y5 and Y6. Specific quality observations:

- **Resources are age-appropriate**: Y1 correctly uses bead strings, ten frames, Numicon, counters. Y3 correctly transitions to Dienes blocks and fraction strips. Y5 correctly uses place value counters (including 0.001, 0.01, 0.1 denominations for decimals). Y6 correctly uses algebra tiles and protractors. There are no instances of inappropriately advanced or immature resources.

- **Transition cues are assessment criteria, not vague aspirations**: The transition cue for MA-Y1-C008 (number bonds) reads "Child builds any bond to 10 on a ten frame without counting the empty spaces one by one -- they see the complement as a known fact and announce it immediately." This is a specific, observable behaviour a teacher (or AI) can check. Not "child understands number bonds" -- which is meaningless as a transition signal.

- **Concrete stages describe what children DO, not what they KNOW**: The concrete stage for MA-Y2-C002 (place value) reads "Children build two-digit numbers using Dienes blocks on a place value mat divided into Tens and Ones columns. They physically exchange 10 unit cubes for 1 ten-stick to understand the grouping principle." This describes the physical action. An AI tutor can translate this into a lesson instruction.

- **Abstract stages correctly include "no resources" or minimal resources**: When the abstract stage is genuine abstraction, the resources list is empty. When a concrete reference remains useful even at abstract level (e.g. whiteboards for quick-write practice), it is included. This distinction is correct.

- **Y3 is split by domain**: The Y3 data is split into 7 files (number_place_value, addition_subtraction, multiplication_division, fractions, measurement, geometry, statistics). This is the right granularity -- it follows the CLAUDE.md convention for DifficultyLevel files and keeps files maintainable.

### 1.3 Import script is clean and idempotent

The import script follows the project pattern correctly: MERGE on `stage_id`, `--clear` flag, stats tracking, concept existence checking with warnings. The `display_color` is `#06B6D4` (Cyan-500) and `display_icon` is `view_carousel` -- these are reasonable choices that distinguish RepresentationStage from other node types in the graph visualisation.

### 1.4 Query integration is complete

Both query helpers surface CPA data under each concept. The `query_cluster_context.py` renders:

```
**CPA stages (Concrete -> Pictorial -> Abstract):**
1. **Concrete**: [description]
   Resources: [list]
   *Transition cue:* [criteria]
```

This gives the AI tutor a clear, structured briefing on how to teach each concept at each CPA stage. The transition cues tell the AI when to move between stages.

### 1.5 Validation is thorough

Five validation checks: completeness, stage_number range (1-3), stage values (concrete/pictorial/abstract), relationship integrity, no duplicate stages. This matches the DifficultyLevel validation pattern.

---

## 2. Gap Analysis: What I Proposed vs What Was Built

### 2.1 Naming: `RepresentationStage` vs `CPAPathway`

**What I proposed**: `CPAPathway` -- a node representing a specific route through the CPA cycle for a concept at a given difficulty level.

**What was built**: `RepresentationStage` -- a node representing a single CPA stage (concrete OR pictorial OR abstract) for a concept.

**My assessment**: The naming is defensible but different in meaning. `RepresentationStage` accurately describes what the node IS: a single stage. `CPAPathway` described what I wanted the node to BE: a route through multiple stages with direction, re-entry capability, and links to manipulatives and representations.

**Recommendation**: Keep `RepresentationStage` for now. It accurately names what exists. If we later add the full pathway model (see Section 3), we can add `CPAPathway` as a higher-level node that aggregates `RepresentationStage` nodes. Renaming mid-implementation would cause churn for no gain.

### 2.2 Relationship anchor: Concept vs DifficultyLevel

**What I proposed**: `(:DifficultyLevel)-[:HAS_CPA_PATHWAY]->(:CPAPathway)` -- CPA bound to difficulty level.

**What was built**: `(:Concept)-[:HAS_REPRESENTATION_STAGE]->(:RepresentationStage)` -- CPA bound to concept.

**My assessment**: This is the most significant structural divergence. I was explicit in my ontology that CPA is per-difficulty-level, not per-concept. The current model gives the AI one set of CPA stages per concept regardless of whether the child is at entry, developing, expected or greater depth.

Consider MA-Y3-C014 (column addition). The current model says:
- Stage 1 (concrete): Dienes blocks
- Stage 2 (pictorial): Place value chart
- Stage 3 (abstract): Columnar notation

But in reality:
- A child at **entry** level should be working entirely in concrete (Dienes) and maybe bridging to pictorial
- A child at **expected** level should be working abstractly with columnar notation
- A child at **greater depth** who hits cascading exchange across zero may need to **re-enter** pictorial

The current model cannot express this. It provides one-size-fits-all CPA stages regardless of the child's difficulty level.

**Impact**: Medium-high. The AI will still get useful CPA information -- it knows concrete means Dienes blocks, pictorial means place value charts. But it cannot differentiate its CPA approach by difficulty level. A child at greater depth gets the same "start with Dienes blocks" instruction as a child at entry, which is wrong.

**Recommendation (Priority 1)**: In a future iteration, add a `difficulty_level_guidance` object to each RepresentationStage or (better) create DifficultyLevel-specific CPA pathway nodes as I originally proposed. For now, the AI can cross-reference DifficultyLevel descriptions with RepresentationStage data to infer the right approach -- the DL descriptions already encode CPA information implicitly.

### 2.3 Missing node types

| My proposed node | Built? | Assessment |
|---|---|---|
| `CPAPathway` | Partially (as `RepresentationStage`) | Core CPA data exists. Pathway routing, re-entry, and direction are missing. |
| `MathsRepresentation` | No | Resources listed as string arrays, not first-class nodes. Cannot query "which concepts use bar models?" or trace representation progressions across year groups. |
| `MathsManipulative` | No | Same as above. Resources listed as strings. Cannot query "which manipulatives does a Y3 child need?" or track manipulative progressions. |
| `MathsContext` | No | Not present at all. No real-world context data in RepresentationStage. |
| `ReasoningPromptType` | No | Not present at all. No reasoning prompt patterns. |

**My assessment**: The absence of `MathsRepresentation` and `MathsManipulative` as nodes is the second most significant gap (after the DifficultyLevel binding). The resources are embedded as string arrays, which means they are human-readable but not machine-queryable.

Example: The Y3 fractions concrete stage lists `["counters", "sorting trays (3, 4, 5, 6, 8 compartments)", "fraction circles", "fraction strips"]`. An AI can read this text and mention these resources. But it CANNOT:
- Query "across all Y3 concepts, which manipulatives appear most frequently?" (for classroom preparation lists)
- Know whether fraction strips have a virtual equivalent (for home learning)
- Know that Numicon is typically EYFS-Y1 and should not be suggested for Y5
- Trace the progression from concrete objects to pictorial representations (the C-to-P bridge)

**Recommendation (Priority 2)**: Extract `MathsManipulative` and `MathsRepresentation` as first-class nodes in a future iteration. The data already exists in the resources arrays -- it needs to be normalised into a controlled vocabulary and promoted to nodes.

`MathsContext` and `ReasoningPromptType` are lower priority (Priority 3) and could be deferred to a later phase.

---

## 3. The Cyclical CPA Question

### 3.1 Does the current model enforce the linear misconception?

**Yes, partially.**

The current model has `stage_number` 1, 2, 3 mapping to concrete, pictorial, abstract. This is always linear: 1 -> 2 -> 3. There is no mechanism for:

- **Re-entry**: A child at greater depth who needs to return to concrete for a specific sub-skill
- **Stage skipping**: Fluency concepts (like Y4 times tables recall) that should start and stay abstract
- **Reverse pathways**: A child who grasps the abstract method but cannot draw it pictorially (which does happen with procedurally strong but conceptually weak children)

The transition cues partially mitigate this by describing what "ready to move on" looks like. An AI reading the transition cue for the concrete stage knows when to move to pictorial. But there is no signal for "when should you move BACK to concrete?"

### 3.2 Does this matter in practice?

For the current use case (AI lesson generation for a child whose difficulty level is already known), the impact is moderate. The AI has both RepresentationStage data and DifficultyLevel data for each concept. A well-prompted AI can infer that a child at entry level should focus on the concrete stage, and a child at expected level should focus on the abstract stage. The transition cues help it know when to bridge.

The gap becomes significant when:
1. **The child struggles mid-lesson**: The AI needs to know that returning to concrete is appropriate, not a regression. Without `is_reentry: true` and `reentry_trigger`, the AI may not offer concrete support to an advanced child.
2. **The concept is inherently abstract**: Some concepts (times table fluency, BODMAS) should start at abstract. The current model always starts at concrete (stage 1), which could mislead the AI.
3. **KS3-KS4 extension**: Secondary concepts often start with a full C-P-A cycle for first encounter, then move to pure abstract for practice. The current model cannot distinguish first encounter from practice.

### 3.3 Recommendation

**Short-term (no schema change needed)**: Add an optional `cpa_notes` property to RepresentationStage or to the concept-level entry in the JSON, with flags like:
- `"fluency_focus": true` -- tells the AI this concept should primarily be practised abstractly
- `"reentry_likely": true` -- tells the AI that returning to concrete is expected at higher difficulty levels
- `"reentry_trigger": "cascading exchange across zero"` -- tells the AI when to offer concrete support

**Medium-term**: Implement the `CPAPathway` model I proposed, with `entry_stage`, `target_stage`, `stage_sequence`, `is_reentry`, and `reentry_trigger`. Bind it to DifficultyLevel.

---

## 4. Data Quality Issues Found

### 4.1 No errors found in curriculum accuracy

I checked 50+ stage descriptions across Y1-Y6 and found no factual errors in the mathematical content. The resources are appropriate, the progression from concrete to abstract is pedagogically sound, and the transition cues describe observable behaviours.

### 4.2 Minor quality observations (not errors)

**Y1-C004 (number words)**: The concrete stage uses "word cards" for number words, which is appropriate. But the abstract stage says children write number words "from memory" -- at Y1, this is a stretch goal. Many Y1 children will still need the word wall. The transition cue correctly gates this ("Child writes all number words from 'one' to 'twenty' from dictation with correct spelling, including the irregular forms"), so the gate is set high enough. Not an error, but worth noting that this is greater-depth-level for Y1.

**Y5-C003 (prime numbers)**: The pictorial stage mentions "sqrt(37) approximately 6, so only need to check up to 6." The square root method is not in the Y5 National Curriculum programme of study. It is a valid mathematical shortcut, but it may confuse an AI that is trying to stay within curriculum scope. Consider adding a note: "The square root test is an extension; curriculum only requires systematic factor checking."

**Y6-C030 (mathematical reasoning / proof)**: The pictorial stage introduces algebraic proof: "odd + odd = (2a+1)+(2b+1) = 2a+2b+2 = 2(a+b+1)". This is a Y6 greater-depth extension and is mathematically correct. However, the transition from concrete pattern-spotting to formal algebraic proof is a very large step. The CPA stages here are more like "stages of mathematical maturity" than the literal concrete-pictorial-abstract of the CPA model. This is not wrong -- it is a valid interpretation -- but it stretches the CPA framework beyond its original meaning.

**Y3 fractions (MA-Y3-C027, equivalent fractions)**: The abstract stage says "Simplify 6/8" -- simplifying fractions is a Y4 objective, not Y3. The Y3 curriculum says "recognise and show, using diagrams, equivalent fractions." This is a minor curriculum placement issue; the concept is covered but the abstract example pushes into Y4 territory. Not a blocking issue for the AI.

### 4.3 Consistency observations

- Y1 and Y2 files use longer, more descriptive entries (697 and 668 lines respectively). Y4-Y6 files use shorter, more compressed entries. The Y1/Y2 style is better for AI consumption because it provides more specific guidance. Consider bringing Y4-Y6 entries closer to the Y1/Y2 level of detail in a future pass.

- Y3 is the only year group split into domain-level files. Y1, Y2, Y4, Y5, Y6 are each a single file. The Y3 split is better (follows the DifficultyLevel convention). Consider splitting Y4-Y6 by domain in a future iteration for maintainability.

---

## 5. Integration with DifficultyLevel

### 5.1 Current state

DifficultyLevel and RepresentationStage are siblings on Concept:
```
(:Concept)-[:HAS_DIFFICULTY_LEVEL]->(:DifficultyLevel)
(:Concept)-[:HAS_REPRESENTATION_STAGE]->(:RepresentationStage)
```

They are surfaced together in the query helpers -- under each concept, the AI sees both the difficulty levels and the CPA stages. This is functional. The AI can mentally cross-reference "entry level means using Dienes blocks" with "the concrete stage uses Dienes blocks."

### 5.2 What is missing

There is no formal link between the two. The AI has to infer the mapping:
- Entry -> likely concrete
- Developing -> likely concrete-to-pictorial bridge
- Expected -> likely pictorial-to-abstract bridge
- Greater depth -> likely abstract (but may re-enter concrete)

This inference is usually correct but not always. Some concepts are abstract from entry (fluency concepts). Some are concrete through expected (EYFS and early Y1 concepts). The AI has no machine-readable signal for these exceptions.

### 5.3 Recommendation

**Priority 1**: Add a `typical_cpa_stage` property to each DifficultyLevel node for Maths concepts. Values: `concrete`, `pictorial`, `abstract`, `mixed`. This is a lightweight change that gives the AI an explicit mapping without requiring a new node type or relationship.

**Priority 2 (longer term)**: Implement the full `(:DifficultyLevel)-[:HAS_CPA_PATHWAY]->(:CPAPathway)` model from my ontology.

---

## 6. What the AI Tutor Gets (and What It Lacks)

### 6.1 What it gets now

For any Maths concept, the AI receives:
1. **What to teach**: Concept name, description, objectives (existing)
2. **Difficulty levels**: Entry, developing, expected, greater depth with descriptions, example tasks, example responses, common errors (DifficultyLevel layer)
3. **CPA stages**: Concrete description + resources, pictorial description + resources, abstract description + resources, transition cues (RepresentationStage layer)
4. **Thinking lens**: Cognitive framing for the cluster (ThinkingLens layer)
5. **Content vehicle**: Teaching pack structure (ContentVehicle layer)

This is a significant improvement over the pre-CPA state. The AI now knows **how** to teach, not just **what** to teach.

### 6.2 What it lacks

1. **Which manipulative to choose for THIS child at THIS level**: The resources are a flat list. The AI must guess which manipulative is primary vs supplementary, which is for entry vs greater depth.
2. **When to offer concrete support to an advanced child**: No re-entry signals.
3. **Which representations progress from which**: No representation progression chain.
4. **What real-world context to embed the maths in**: No MathsContext data.
5. **What reasoning questions to ask**: No ReasoningPromptType data.
6. **Whether this is a fluency or conceptual introduction lesson**: No NC aim emphasis signal.
7. **Whether a manipulative is available virtually**: No virtual availability flag.

### 6.3 Can the AI infer what it lacks?

Partially. A well-prompted AI (with the full lesson context from the query helpers) can:
- Infer the primary manipulative from the concrete description (the first-mentioned resource is usually primary)
- Infer the CPA stage from the DifficultyLevel label (entry = concrete, expected = abstract)
- Choose real-world contexts from general knowledge (but without safeguarding notes)
- Generate reasoning questions using the ThinkingLens prompts (but without maths-specific question structures)

It cannot infer re-entry triggers, manipulative progressions, virtual availability, or NC aim emphasis. These require structured data.

---

## 7. Recommendations (Prioritised)

### Priority 1 (Next iteration -- high impact, moderate effort)

1. **Add `typical_cpa_stage` to DifficultyLevel for Maths concepts**: A single string property (`concrete`, `pictorial`, `abstract`, `mixed`) on each DL node. Can be derived from existing data -- the DL descriptions already encode this.

2. **Add `cpa_notes` or `teaching_notes` to RepresentationStage JSON**: Optional properties for `fluency_focus`, `reentry_likely`, `reentry_trigger`. These are free-text hints the AI can use without requiring schema changes.

3. **Split Y4-Y6 files by domain**: Align with Y3 and DifficultyLevel file conventions. Improves maintainability and allows targeted updates.

### Priority 2 (Future iteration -- high impact, high effort)

4. **Extract `MathsManipulative` as first-class nodes**: ~25-30 nodes. Build a controlled vocabulary from the existing resources arrays. Add `is_virtual_available`, `primary_year_range`, `manipulative_type` properties. Create `(:RepresentationStage)-[:USES_MANIPULATIVE]->(:MathsManipulative)` relationships.

5. **Extract `MathsRepresentation` as first-class nodes**: ~30-35 nodes. Same approach. Representations are the pictorial tools (bar model, number line, place value chart, fraction wall).

6. **Bind CPA to DifficultyLevel**: Either add DL-specific guidance to RepresentationStage or implement the full CPAPathway model.

### Priority 3 (Later -- moderate impact, moderate effort)

7. **Add `MathsContext` nodes**: ~15-20 real-world context nodes with safeguarding notes.

8. **Add `ReasoningPromptType` nodes**: ~10-12 reasoning question pattern nodes with age-appropriateness.

9. **Add KS3-KS4 RepresentationStage data**: The current layer covers Y1-Y6 only. Secondary Maths also uses CPA (the NCETM is explicit about this for KS3-KS4 first encounters).

### Priority 4 (Nice-to-have)

10. **Manipulative and representation progression chains**: `PROGRESSES_TO` relationships between manipulatives (Numicon -> Dienes -> place value counters) and representations (ten frame -> place value chart -> columnar notation).

11. **NC aim emphasis**: `fluency` / `reasoning` / `problem_solving` signal on ConceptCluster or Concept.

12. **Fluency targets**: Explicit "what must be automatic" lists on ConceptCluster.

---

## 8. Should `RepresentationStage` Be Renamed?

**No, not now.**

`RepresentationStage` accurately describes what the node IS: a stage in the CPA representation progression for a concept. Renaming it to `CPAPathway` would be misleading because the current node is a single stage, not a pathway.

If the full pathway model is implemented later, I would recommend:
- Keep `RepresentationStage` as is
- Add `CPAPathway` as a new node that groups RepresentationStages into directed routes per DifficultyLevel
- Relationship: `(:DifficultyLevel)-[:HAS_CPA_PATHWAY]->(:CPAPathway)-[:INCLUDES_STAGE {order: int}]->(:RepresentationStage)`

This would preserve the current working layer while adding the routing, re-entry, and difficulty-level binding I originally proposed.

---

## 9. Summary

| Dimension | Score | Notes |
|---|---|---|
| Coverage | 10/10 | 154/154 primary Maths concepts. 100%. |
| Data quality | 9/10 | Excellent descriptions, resources, transition cues. Minor curriculum placement issues in Y3 fractions and Y5 primes. |
| Schema design | 6/10 | Clean and functional, but missing the DifficultyLevel binding and the cyclical CPA model. |
| Integration | 8/10 | Both query helpers surface CPA data. AI gets a useful briefing. |
| Ontology completeness | 4/10 | 1 of 5 proposed node types built. No manipulative/representation nodes, no contexts, no reasoning prompts. |
| Pedagogical fidelity to CPA model | 5/10 | Linear 1-2-3 model. No re-entry, no stage skipping, no direction. |
| **Overall** | **7/10** | **The right first step. The data is excellent. The structure needs the second iteration.** |

The team delivered the hardest part: 154 concepts worth of accurate, detailed CPA stage data. The structural model I proposed is a superset of what was built, and the data already contains the raw material to evolve towards it. This is a solid foundation.

---

## 10. What I Would Use in a Lesson Tomorrow

If I were teaching a Y3 fractions lesson tomorrow and asked the AI for help, here is what the current model gives me versus what I still need:

**What the AI can tell me (with current data)**:
- "For unit fractions of quantities (MA-Y3-C025), start concrete with counters and sorting trays. Share 12 counters between 3 trays. The child should be able to say 'bigger denominator means smaller pieces' before moving to pictorial."
- "The pictorial stage uses fraction walls and number lines. The abstract stage is mental division."

**What the AI cannot tell me (missing data)**:
- "This child is at developing level, so they should be bridging from concrete to pictorial -- not starting from scratch with counters."
- "The primary manipulative is counters; fraction circles are support. If you do not have fraction circles at home, use folded paper strips instead."
- "This is a conceptual introduction, not a fluency lesson -- do not drill, explore."
- "If the child gets stuck on non-obvious equivalences at expected level, return to concrete with fraction tiles. This is expected, not a regression."

The first set is valuable and usable today. The second set is what the full ontology would provide. The path from here to there is clear.
