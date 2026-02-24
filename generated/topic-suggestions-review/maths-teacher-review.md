# KS2 Maths Specialist Review: MathsTopicSuggestion Schema

**Reviewer**: Henderson (Y2–Y6 Maths lead, 11 years primary, White Rose / NCETM Mastery trained)
**Date**: 2026-02-24

---

## 0. The Fundamental Naming Problem

Before addressing individual properties, I need to flag a structural issue that affects the whole Maths design.

**Maths is not organised by "topics" the way History and Geography are.** In History, a teacher chooses *which period to teach* (Roman Britain vs Anglo-Saxons). In Geography, they choose *which place to study* (Kenya vs India). These are genuine topic choices. In Maths, you don't "choose" place value — you teach it because it's in the programme of study. The progression is fixed: place value → addition/subtraction → multiplication/division → fractions → measurement → geometry → statistics (broadly).

What teachers *do* choose in Maths is:

1. **Which REPRESENTATION to use** (number line vs bar model vs array)
2. **Which CONTEXT to embed it in** (money, measurement, real-world scenarios)
3. **Which MANIPULATIVE to deploy** (Dienes vs Numicon vs Cuisenaire)
4. **Which PEDAGOGICAL APPROACH to structure the session around** (fluency drill, reasoning task, problem-solving challenge, investigation)

A `MathsTopicSuggestion` called "Place Value with Dienes Blocks" is really a **representation/manipulative recommendation**, not a topic suggestion. The name is misleading and will confuse AI content generation — the AI needs to understand it's choosing *how* to teach a concept, not *what* to teach.

**Recommendation**: Either rename to `MathsApproachSuggestion` or accept that `MathsTopicSuggestion` nodes represent something fundamentally different from `HistoryTopicSuggestion` nodes — and document this distinction explicitly in the schema. I lean towards keeping the unified `MathsTopicSuggestion` label for schema simplicity but adding a `suggestion_nature` property: `context_choice` | `representation_choice` | `application_context`.

---

## 1. Subject-Specific Property Review

### `cpa_stage` — MODIFY (critical)

**Current**: string (free text)
**Existing CV data**: `"concrete -> pictorial -> abstract"`, `"concrete (counting objects) -> pictorial (number line jumps) -> abstract (column method introduction)"`

The free-text approach is problematic. The CPA model (derived from Jerome Bruner's enactive–iconic–symbolic modes) is the backbone of UK mastery teaching, used by White Rose Maths, Maths No Problem, and endorsed by the NCETM. But CPA isn't always a linear progression — as the NCETM emphasises, it's often **cyclical**, with pupils moving back and forth between representations.

**Recommendation**: Change to a **controlled enum** plus a freetext elaboration:

| Property | Type | Required | Values |
|---|---|---|---|
| `cpa_stage` | string (enum) | Yes | `concrete`, `pictorial`, `abstract`, `concrete_pictorial`, `pictorial_abstract`, `concrete_pictorial_abstract` |
| `cpa_notes` | string | No | Freetext elaboration, e.g. "Concrete: Dienes blocks on place value mat. Pictorial: place value chart with drawn tens and ones. Abstract: partitioning notation 47 = 40 + 7" |

The enum tells the AI the dominant stage. The notes give specific guidance for generation. At KS3/KS4, `abstract` becomes the most common value, but `concrete_pictorial_abstract` remains valid for introducing new concepts (e.g. algebra tiles for expanding brackets).

### `manipulatives` — MODIFY (make required, add controlled vocabulary)

**Current**: string[] (optional)
**Existing CV data**: `["Dienes blocks (units and tens)", "place value charts", "arrow cards"]`

Manipulatives are not optional in mastery Maths. Every lesson should specify what concrete resources support the learning. The existing data already demonstrates this — every single Y2 CV has manipulatives listed.

**Recommendation**: Make **required**. Add a controlled core vocabulary (extensible):

**Primary (KS1-KS2) standard manipulatives**:
- `dienes_blocks` (base-10 apparatus — units, tens, hundreds, thousands)
- `numicon` (structured number shapes)
- `cuisenaire_rods` (proportional lengths for number relationships)
- `counters` (single-colour and two-sided)
- `multilink_cubes` (interlocking cubes)
- `place_value_charts` (place value mats/charts)
- `arrow_cards` (expanded notation)
- `hundred_square` (number grid to 100)
- `bead_strings` (10-bead and 100-bead)
- `fraction_tiles` (fraction wall pieces)
- `fraction_circles` (pizza/pie slices)
- `number_lines` (structured and empty)
- `geoboards` (for geometry)
- `pattern_blocks` (tessellation/shape)
- `measuring_equipment` (rulers, scales, jugs, thermometers)
- `coins_and_notes` (real or plastic currency)
- `dice` (standard and polyhedral)
- `dominoes`
- `clocks` (analogue, geared)

**Secondary (KS3-KS4) additions**:
- `algebra_tiles` (for expressions and equations)
- `double_sided_counters` (for directed number)
- `protractors`
- `compasses` (geometrical)
- `scientific_calculators`
- `graph_paper` (coordinate geometry)

The property should accept both controlled vocabulary terms AND freetext (for novel/context-specific resources like "egg boxes for arrays"). Storage: `manipulatives: ["dienes_blocks", "place_value_charts", "arrow_cards"]`.

### `representations` — MODIFY (make required, add controlled vocabulary)

**Current**: string[] (optional)
**Existing CV data**: `["place value chart", "part-whole model", "number line to 100"]`

This is arguably **THE most important property** in the entire Maths schema. Choosing the right representation is the core pedagogical decision in mastery Maths. The NCETM's "Five Big Ideas" names "Representation and Structure" as one of the five pillars. At secondary level, the move between representations (concrete manipulative → pictorial diagram → algebraic notation) *is* the mathematical thinking.

**Recommendation**: Make **required**. Controlled core vocabulary:

**KS1-KS2 representations**:
- `number_line` (structured/empty/vertical)
- `bar_model` (comparison and part-whole)
- `part_whole_model` (cherry/part-part-whole diagrams)
- `array` (dots/counters in rows and columns)
- `ten_frame` (5×2 grid)
- `hundred_square` (number grid)
- `place_value_chart` (columns)
- `fraction_wall` (proportional strips)
- `fraction_bar` (shaded bars)
- `pie_chart_fraction` (divided circles)
- `number_line_fractions` (0 to 1 or beyond)
- `pictogram` / `block_diagram` / `bar_chart` (statistics)
- `tally_chart`
- `sorting_diagram` (Venn/Carroll)
- `coin_images`

**KS3-KS4 additions**:
- `area_model` (for multiplication, algebra)
- `algebra_tile_diagram` (for expressions)
- `coordinate_grid` (four quadrants)
- `ratio_table` (multiplicative reasoning)
- `box_plot` / `scatter_graph` / `cumulative_frequency`
- `tree_diagram` (probability)
- `unit_circle` (trigonometry)
- `function_machine` (input-output)

### NEW: `fluency_targets` — ADD (required)

**Rationale**: The NC Maths aims are explicitly three-fold: **fluency**, **reasoning**, and **problem-solving**. Fluency (facts and procedures that need to be automatic) is unique to Maths — no other subject has an equivalent concept. DifficultyLevel nodes capture *what* children should be able to do at each level, but they don't specify *what needs to be practised to automaticity*.

| Property | Type | Required | Example |
|---|---|---|---|
| `fluency_targets` | string[] | Yes | `["Recall addition/subtraction facts to 20", "Add/subtract 2-digit and 1-digit numbers mentally"]` |

An AI tutor generating a Y2 addition lesson MUST know which facts the child should already be fluent with (prerequisites) and which are the target for this session. Without this, the AI cannot calibrate its expectations — it might accept finger-counting for facts that should be automatic by this point.

### NEW: `reasoning_prompts` — ADD (recommended)

**Rationale**: Reasoning is a NC aim and a distinct activity type. UK schools universally use structured reasoning prompt types, drawn from the NCETM and NRICH. These are not content — they're **prompt patterns** that the AI should use.

| Property | Type | Required | Example |
|---|---|---|---|
| `reasoning_prompts` | string[] | No | `["always_sometimes_never", "true_or_false", "spot_the_mistake", "what_comes_next", "odd_one_out", "convince_me"]` |

Controlled vocabulary for prompt types:
- `always_sometimes_never` — "A square is always/sometimes/never a rectangle"
- `true_or_false` — "23 + 15 = 37. True or false? Prove it."
- `spot_the_mistake` — "Sam says 1/3 > 1/2 because 3 > 2. What is wrong?"
- `what_comes_next` — "2, 6, 18, __ — what's the pattern?"
- `odd_one_out` — "12, 15, 20, 25 — which doesn't belong and why?"
- `convince_me` — "Can a triangle have two right angles? Convince me."
- `how_many_ways` — "How many ways can you make 50p?"
- `what_if` — "What if the number line went backwards?"

These prompt types are subject-specific to Maths and belong in `MathsTopicSuggestion`, not in VehicleTemplate.

### NEW: `application_contexts` — ADD (recommended)

**Rationale**: This is the actual "topic choice" in Maths. For addition and subtraction, a teacher might embed the learning in a money context, a measurement context, or a story problem context. The AI needs these options.

| Property | Type | Required | Example |
|---|---|---|---|
| `application_contexts` | string[] | No | `["money (adding prices, calculating change)", "measurement (comparing lengths)", "time (calculating durations)"]` |

This bridges the gap between "Maths doesn't have topics" and the TopicSuggestion architecture. The context IS the generative hook for making personalised content.

### NOT NEEDED: `common_errors` (as a separate property)

The existing CVs have `common_errors` and it's excellent data. However, the DifficultyLevel nodes already have `common_errors` at each level (entry, developing, expected, greater_depth). Adding it again on TopicSuggestion would create **data duplication** and drift risk. The AI should pull common errors from DifficultyLevel nodes via the graph relationship.

**Exception**: If there are representation-specific errors that don't map to difficulty levels (e.g. "When using a number line, children count the marks instead of the jumps"), these could go in `cpa_notes`.

---

## 2. Universal Property Review

### KEEP (no changes):
- `suggestion_id`, `name`, `subject`, `key_stage`, `display_*` — all fine
- `pedagogical_rationale` — critical for Maths ("WHY use a bar model for this concept?")
- `definitions` — essential, Maths vocabulary is precise and must be correct
- `cross_curricular_hooks` — useful (money → PSHE; measurement → Science; statistics → Geography)

### MODIFY:

**`suggestion_type`**: The proposed enum values (`prescribed_topic`, `exemplar_topic`, `open_slot`, `teacher_convention`) don't map well to Maths.

- There are no "open slots" in Maths (you don't choose WHICH fractions to teach)
- There are no "exemplar topics" (the NC doesn't say "e.g. fractions" — it says "fractions")
- Every Maths domain is prescribed

For Maths, the values should be:
- `prescribed_domain` — the NC content is mandatory (place value, addition, fractions...)
- `representation_choice` — teacher picks the representation approach (Dienes vs Numicon for place value)
- `context_choice` — teacher picks the application context (money vs measurement for addition)
- `enrichment_extension` — optional deepening (investigations, cross-curricular projects)

**Recommendation**: Either expand the enum to include these Maths-specific values, or accept that for Maths, `suggestion_type` will mostly be `prescribed_topic` and the real variability is captured by `cpa_stage`, `manipulatives`, `representations`, and `application_contexts`.

**`curriculum_status`**: Similarly, nearly everything in Maths is `mandatory`. The only real choices are about *how* to teach it, not *what* to teach. `menu_choice` and `exemplar` barely apply.

**`common_pitfalls`**: Rename to `teaching_pitfalls` to distinguish from pupil `common_errors`. Pitfalls are things the TEACHER gets wrong in delivery ("Introducing column method before children have secure understanding of partitioning", "Jumping to abstract notation before sufficient concrete experience").

### ADD:

**`nc_aim_emphasis`**: Which of the three NC aims does this suggestion primarily serve?

| Property | Type | Required | Values |
|---|---|---|---|
| `nc_aim_emphasis` | string | Yes | `fluency` / `reasoning` / `problem_solving` / `mixed` |

This is the single most important organising principle in Maths teaching and is absent from the schema.

---

## 3. VehicleTemplate Critique

### Templates that work for Maths:

| # | Template | Maths fit | Notes |
|---|---|---|---|
| 8 | `worked_example_set` | Strong | The existing CV type. Good for introducing procedures. Session structure (concrete → pictorial → abstract → application → fluency) is sound. |
| 5 | `pattern_seeking` | Strong | Maths is fundamentally about pattern. Good for sequences, number properties, algebra. |
| 13 | `practical_application` | Adequate | Works for measurement, money, data handling. |

### Templates MISSING for Maths:

**`fluency_practice`** — CRITICAL gap. Maths lessons frequently include a dedicated fluency phase (rapid recall, timed challenges, games). This is distinct from worked examples. Structure: `warm_up → retrieval_practice → focused_drill → speed_challenge → self_check`.

**`reasoning_task`** — CRITICAL gap. An "Always, Sometimes, Never" investigation or "Spot the Mistake" activity has a completely different pedagogical structure from a worked example set. Structure: `stimulus → conjecture → testing → justification → generalisation`.

**`problem_solving_task`** — Important gap. Multi-step problems that require selecting and combining operations. Different from worked examples because the method isn't given. Structure: `problem_presentation → representation_choice → working → checking → extension`.

**`mathematical_investigation`** — A more open-ended exploration where children generate and test their own conjectures. Structure: `question_posing → systematic_exploration → data_collection → pattern_identification → conjecture → testing → proof_attempt`.

**`pre_teaching_diagnostic`** — Maths benefits from diagnostic assessment at the start of a unit, not just formative assessment during. The AI should be able to generate a short diagnostic. Structure: `anchor_question → probing_questions → misconception_check → readiness_classification`.

### Template modifications:

**`worked_example_set`** (template 8): The session structure `concrete -> pictorial -> abstract -> application -> fluency` should be updated to reflect the cyclical nature of CPA. Better: `activate_prior_knowledge → concrete_exploration → pictorial_bridging → abstract_recording → application → fluency_consolidation → reasoning_extension`. Note the bookends: starting with prior knowledge activation and ending with reasoning, not just fluency.

---

## 4. TopicSuggestion Inventory for Maths

Maths "topics" are really **domain-representation pairings**. Here is what should exist for KS1-KS2 Mathematics:

### Year 2 (sample — extrapolate pattern to all year groups)

| suggestion_id | name | suggestion_type | cpa_stage | Key representations |
|---|---|---|---|---|
| TS-MA-KS1-001 | Place Value with Dienes Blocks | prescribed_topic | concrete_pictorial_abstract | place_value_chart, part_whole_model |
| TS-MA-KS1-002 | Place Value with Numicon | prescribed_topic | concrete_pictorial | numicon shapes, number line |
| TS-MA-KS1-003 | Addition on a Number Line | prescribed_topic | pictorial_abstract | number_line, hundred_square |
| TS-MA-KS1-004 | Subtraction with Bar Models | prescribed_topic | pictorial_abstract | bar_model, part_whole_model |
| TS-MA-KS1-005 | Times Tables with Arrays | prescribed_topic | concrete_pictorial_abstract | array, bar_model |
| TS-MA-KS1-006 | Fractions with Fraction Tiles | prescribed_topic | concrete_pictorial | fraction_wall, fraction_bar |
| TS-MA-KS1-007 | Fractions on a Number Line | prescribed_topic | pictorial_abstract | number_line_fractions, fraction_bar |
| TS-MA-KS1-008 | Money as Addition/Subtraction Context | prescribed_topic | concrete_pictorial_abstract | coin_images, bar_model |
| TS-MA-KS1-009 | Measurement: Practical Weighing | prescribed_topic | concrete | balance scales, comparison |
| TS-MA-KS1-010 | Shape Properties with 3-D Models | prescribed_topic | concrete_pictorial | sorting_diagram, shape property table |
| TS-MA-KS1-011 | Statistics: Collecting and Representing Data | prescribed_topic | concrete_pictorial_abstract | pictogram, tally_chart, block_diagram |

### KS3-KS4 examples (to test schema scalability)

| suggestion_id | name | cpa_stage | Key representations |
|---|---|---|---|
| TS-MA-KS3-001 | Expanding Brackets with Algebra Tiles | concrete_pictorial_abstract | algebra_tile_diagram, area_model |
| TS-MA-KS3-002 | Ratio with Bar Models | pictorial_abstract | bar_model, ratio_table |
| TS-MA-KS4-001 | Trigonometry with Unit Circle | pictorial_abstract | unit_circle, coordinate_grid |
| TS-MA-KS4-002 | Quadratic Graphs from Tables | pictorial_abstract | coordinate_grid, function_machine |
| TS-MA-KS4-003 | Probability with Tree Diagrams | pictorial_abstract | tree_diagram |

**Observation**: At KS3-KS4, the `concrete` stage becomes rarer but doesn't disappear (algebra tiles ARE concrete). The schema handles this fine via the enum. Most KS4 suggestions will be `pictorial_abstract` or `abstract`.

**Note on `curriculum_status`**: Every single Maths suggestion above is `mandatory` — there are no "choose one ancient civilisation" equivalents in Maths. The variability is in *how* you teach it (which representation, which manipulative, which context), not *what* you teach.

---

## 5. Content Generation Requirements

### What the AI needs to generate a good Maths lesson:

1. **Concept + DifficultyLevel** (from graph): What to teach, at what level of challenge
2. **CPA stage** (from TopicSuggestion): Whether to start with physical objects, diagrams, or notation
3. **Specific manipulatives** (from TopicSuggestion): "Use Dienes blocks" — the AI can then describe how to use them, even in a digital context (virtual Dienes, or instructions for parents to use physical ones)
4. **Specific representations** (from TopicSuggestion): "Use a bar model" — the AI structures the worked example around this representation
5. **Fluency targets** (from TopicSuggestion): What the child should already know automatically, and what this lesson aims to make automatic
6. **Reasoning prompts** (from TopicSuggestion): What types of higher-order questions to include
7. **Application contexts** (from TopicSuggestion): "Use a shopping scenario" for addition, "Use a cooking scenario" for fractions
8. **VehicleTemplate** (from graph): The session structure to follow
9. **Common errors** (from DifficultyLevel nodes): What mistakes to anticipate and address

### What the AI needs for a video script:

All of the above, PLUS the video must model the CPA progression visually. A video about "Fractions with Fraction Tiles" needs to show:
- **Concrete**: Hands manipulating physical fraction tiles (or animation of same)
- **Pictorial**: Transition to fraction wall diagram on screen
- **Abstract**: Writing fraction notation

The `cpa_notes` property provides this script guidance.

### What the AI needs for assessment:

- DifficultyLevel nodes (already in graph) provide the primary assessment framework
- `fluency_targets` tell the AI what to assess for automaticity (speed + accuracy)
- `reasoning_prompts` tell the AI what types of reasoning questions to include
- The VehicleTemplate's `assessment_approach` provides the overall approach

### What's MISSING for content generation:

**`prerequisite_fluency`**: What must the child already be fluent with BEFORE this lesson? Different from `fluency_targets` (which is what this lesson aims for). Example: Before "Addition of 2-digit numbers", the child must be fluent with number bonds to 10 and place value partitioning. The PREREQUISITE_OF relationships in the graph capture concept dependencies but not fluency dependencies specifically.

---

## 6. Cross-Curricular Hooks

Maths has strong cross-curricular connections that are well-defined by the NC:

| Maths domain | Connected subject | Hook |
|---|---|---|
| Measurement | Science | Measuring in experiments, reading scales, recording data |
| Statistics | Geography | Collecting weather data, population comparisons |
| Statistics | Science | Recording experiment results, interpreting graphs |
| Money | PSHE | Financial literacy, budgeting |
| Time | History | Timelines, chronology, duration |
| Shape & space | Art | Tessellation, symmetry, pattern |
| Shape & space | DT | Measuring for construction, 3-D nets |
| Fractions/decimals/% | Food/Cooking | Scaling recipes, measuring ingredients |
| Ratio/proportion | Science | Concentration, dilution, scaling |
| Coordinates | Geography | Grid references, map reading |
| Data handling | Computing | Spreadsheets, data collection, algorithms |

These should be captured as `cross_curricular_hooks` on the relevant TopicSuggestion nodes.

---

## 7. Stress Test Scenarios

### Scenario 1: AI generates a Y2 "Fractions with Fraction Tiles" lesson

**Child profile**: Y2, developing level, learning 1/3 of quantities.

What the AI needs from the schema:
- `cpa_stage`: `concrete_pictorial` (start with tiles, move to diagrams)
- `manipulatives`: `["fraction_tiles", "counters"]` — fold paper, share counters
- `representations`: `["fraction_wall", "fraction_bar", "number_line_fractions"]`
- `fluency_targets`: `["Equal sharing into 2, 3, 4 groups"]`
- `reasoning_prompts`: `["spot_the_mistake"]` — "Sam says 1/3 of this shape is shaded. Is Sam right?"
- `application_contexts`: `["sharing food equally (pizza, cake)", "dividing objects into groups"]`
- DifficultyLevel (from graph): developing — "Find fractions of quantities (1/3 of 12)"
- VehicleTemplate: `worked_example_set` — concrete → pictorial → abstract → application → fluency
- Common errors (from DL node): "Thinking 1/3 is bigger than 1/2 because 3 > 2"

**Verdict**: Schema captures this well IF `fluency_targets`, `reasoning_prompts`, and `application_contexts` are added. Without them, the AI has the *what* (fractions) and the *with* (fraction tiles) but not the *how deeply* or *in what context*.

### Scenario 2: AI generates a Y6 "Ratio and Proportion" assessment

**Child profile**: Y6, expected level, end-of-unit assessment.

What the AI needs:
- `cpa_stage`: `pictorial_abstract` (bar models transitioning to notation)
- `manipulatives`: `["cuisenaire_rods"]` (for concrete backup if needed)
- `representations`: `["bar_model", "ratio_table", "number_line"]`
- `fluency_targets`: `["Times tables to 12×12", "Simplifying fractions"]`
- `reasoning_prompts`: `["always_sometimes_never", "true_or_false"]` — "The ratio 2:3 is always the same as 4:6. True or false?"
- `application_contexts`: `["scaling recipes", "map scales", "mixing paint colours"]`
- DifficultyLevel: expected — structured assessment tasks
- VehicleTemplate: Could be `worked_example_set` OR `problem_solving_task` (this is where multiple templates matter)

**Verdict**: Works. The `application_contexts` are crucial here — without them, ratio problems are dry and abstract. With them, the AI can generate "Scale this cake recipe for 8 people instead of 4" which is meaningful.

### Scenario 3: AI generates a KS3 "Expanding Brackets with Algebra Tiles" lesson

**Child profile**: Y7, emerging level, first encounter with algebra.

What the AI needs:
- `cpa_stage`: `concrete_pictorial_abstract` (MUST start concrete for first encounter)
- `manipulatives`: `["algebra_tiles", "double_sided_counters"]`
- `representations`: `["algebra_tile_diagram", "area_model"]`
- `fluency_targets`: `["Times tables", "Area of rectangles"]` (prerequisite fluency)
- `reasoning_prompts`: `["convince_me", "what_if"]` — "What if x was 3? Does your expansion still work?"
- `application_contexts`: `["area of rectangles with algebraic sides"]`
- DifficultyLevel: emerging — "Expand single brackets with positive terms"
- VehicleTemplate: `worked_example_set`

**Verdict**: The schema scales to KS3. The controlled vocabulary for manipulatives includes `algebra_tiles`. The `cpa_stage` enum handles the transition from primary to secondary well — Y7 algebra SHOULD still use concrete manipulatives, and the schema supports this.

### Scenario 4: AI generates a Y4 "Times Tables Fluency" session

**Child profile**: Y4, developing level, needs fluency with 6, 7, 8 times tables.

What the AI needs:
- `cpa_stage`: `abstract` (by Y4, fluency practice should be mostly abstract)
- `manipulatives`: `["counters"]` (for concrete backup if misconceptions arise)
- `representations`: `["multiplication_grid", "array"]`
- `fluency_targets`: `["Recall 6×, 7×, 8× tables within 5 seconds"]` — this is the KEY data
- `reasoning_prompts`: `["how_many_ways", "what_comes_next"]`
- `application_contexts`: `["real-world multiplication problems"]`
- VehicleTemplate: **`fluency_practice`** (NOT `worked_example_set`)

**Verdict**: This scenario BREAKS if `fluency_practice` template doesn't exist. A fluency session has a completely different structure from a worked example session. The AI needs speed challenges, retrieval practice grids, and self-check activities — none of which appear in the `worked_example_set` structure.

---

## 8. Summary: Top 3 Recommendations

### 1. Add `fluency_targets` (required) and `reasoning_prompts` (recommended)

**Impact**: HIGH — these capture the two unique pillars of Maths teaching (alongside problem-solving, which is served by VehicleTemplates). Without `fluency_targets`, the AI cannot distinguish between "practise this until automatic" and "understand this conceptually." Without `reasoning_prompts`, the AI generates procedural-only lessons, which is the opposite of mastery.

### 2. Make `manipulatives` and `representations` required with controlled vocabulary

**Impact**: HIGH — representation choice is THE key pedagogical decision in Maths. The current schema makes both optional, which means an AI could generate a Maths lesson with no representation guidance — pedagogical malpractice in mastery teaching. The controlled vocabulary ensures the AI generates valid resources (not "use a histogram" for Y2 data handling).

### 3. Add `fluency_practice` and `reasoning_task` VehicleTemplates

**Impact**: HIGH — the current templates are biased towards instruction/explanation (`worked_example_set`). Maths lessons are balanced across fluency, reasoning, and problem-solving. A `fluency_practice` template (for times tables drills, number bond speed challenges) and a `reasoning_task` template (for "Always, Sometimes, Never" investigations) are structurally different session types that the AI must be able to generate.

### Honourable mentions:

4. **Add `application_contexts`** — the actual "topic choice" in Maths (money vs measurement vs real-world). Without this, the AI generates context-free abstract Maths, which is poor pedagogy.
5. **Add `nc_aim_emphasis`** (`fluency` / `reasoning` / `problem_solving` / `mixed`) — the organising principle the NC itself uses.
6. **Change `cpa_stage` to a controlled enum** — stops the free-text drift visible in existing CVs.
7. **Accept that Maths `TopicSuggestion` represents something different** — document that Maths suggestions are representation/approach recommendations, not topic choices. Add `suggestion_nature` or at minimum note this in schema documentation.

---

## Appendix: Proposed MathsTopicSuggestion Schema (Revised)

| Property | Type | Required | Notes |
|---|---|---|---|
| `cpa_stage` | string (enum) | Yes | `concrete` / `pictorial` / `abstract` / `concrete_pictorial` / `pictorial_abstract` / `concrete_pictorial_abstract` |
| `cpa_notes` | string | No | Specific CPA progression guidance for this suggestion |
| `manipulatives` | string[] | **Yes** | Controlled vocabulary (see Section 1), extensible |
| `representations` | string[] | **Yes** | Controlled vocabulary (see Section 1), extensible |
| `fluency_targets` | string[] | **Yes** | What should be practised to automaticity |
| `reasoning_prompts` | string[] | No | Controlled prompt types: `always_sometimes_never`, `true_or_false`, `spot_the_mistake`, `odd_one_out`, `convince_me`, `how_many_ways`, `what_if`, `what_comes_next` |
| `application_contexts` | string[] | No | Real-world contexts for embedding the maths |
| `nc_aim_emphasis` | string (enum) | Yes | `fluency` / `reasoning` / `problem_solving` / `mixed` |

Plus all universal properties from the briefing.

**Removed from original proposal**: Nothing removed — all three original properties kept (with modifications).
**Added**: 5 new properties (`cpa_notes`, `fluency_targets`, `reasoning_prompts`, `application_contexts`, `nc_aim_emphasis`).
