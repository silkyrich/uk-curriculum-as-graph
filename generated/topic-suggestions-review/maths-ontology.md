# Maths Subject Ontology: Graph Model Design

**Author**: Henderson (Y2-Y6 Maths lead, 11 years primary, White Rose Maths / NCETM Mastery trained)
**Date**: 2026-02-24
**Status**: DRAFT for architect review

---

## 0. Why Maths Needs Its Own Ontology

I said it in my previous review and I will say it louder here: **Maths is not organised by topics.** History teachers choose *which period* to teach. Geography teachers choose *which place* to study. Maths teachers choose *how* to teach a concept that is already mandated by the National Curriculum. The choices are:

1. Which **representation** to use (number line, bar model, array, place value chart)
2. Which **manipulative** to deploy (Dienes blocks, Numicon, Cuisenaire rods, algebra tiles)
3. Which **real-world context** to embed the maths in (money, measurement, cooking, map scales)
4. Where the child currently sits in the **CPA cycle** and where to move them next

These four choices are the core pedagogical decisions in mastery maths teaching. They are not "topics." Forcing them into a `TopicSuggestion` wrapper with a `name` like "Place Value with Dienes Blocks" obscures what is actually happening: the AI is selecting a *teaching approach* for a *mandated concept* at a *specific point in the CPA cycle*.

The flat `MathsTopicSuggestion` schema from the panel review is a reasonable compromise, but now that we have complete freedom, I can design what Maths actually needs.

---

## 1. Node Labels (5 new labels)

### 1.1 `MathsRepresentation`

**What it is**: A named pictorial or structural representation used to make mathematical ideas visible. The NCETM's "Five Big Ideas in Teaching for Mastery" names *Representation and Structure* as a foundational pillar. Choosing the right representation is the single most important pedagogical decision in Maths teaching.

**Why a node, not a property**: Representations have their own progression across year groups. A `number_line` in Y1 (structured, 0-20) is not the same object as a `number_line` in Y6 (empty, extending to fractions and negative numbers). Representations connect to multiple concepts across multiple domains and years. They deserve first-class status.

**Examples**: `number_line`, `bar_model`, `part_whole_model`, `array`, `ten_frame`, `place_value_chart`, `fraction_wall`, `area_model`, `algebra_tile_diagram`, `ratio_table`, `coordinate_grid`, `tree_diagram`, `function_machine`

### 1.2 `MathsManipulative`

**What it is**: A concrete physical (or virtual) resource that children handle to build understanding. In the CPA model, manipulatives are the "Concrete" stage made tangible. Different manipulatives foreground different mathematical structures -- Dienes blocks foreground base-10 place value; Cuisenaire rods foreground proportional relationships; Numicon foregrounds the five-structure and odd/even patterns.

**Why a node, not a property**: Manipulatives have a year-group progression (Numicon dominates Y1, Dienes dominates Y2-3, place value counters take over Y4+). They have pedagogical properties (whether they are proportional or non-proportional, structured or unstructured). And critically, different manipulatives connect to different CPA pathways for the same concept.

**Examples**: `dienes_blocks`, `numicon`, `cuisenaire_rods`, `counters`, `multilink_cubes`, `fraction_tiles`, `algebra_tiles`, `geoboards`, `pattern_blocks`, `bead_strings`, `coins_and_notes`, `clocks_analogue`, `measuring_equipment`

### 1.3 `MathsContext`

**What it is**: A real-world application scenario that embeds mathematical learning in meaning. This is the closest thing Maths has to a "topic" -- the teacher chooses *which context* to wrap the maths in. Where History chooses "The Romans" and Geography chooses "Kenya", Maths chooses "Shopping" or "Cooking" or "Map Reading."

**Why a node, not a property**: Contexts are reusable across year groups and domains. A "shopping" context works for addition (Y1), money (Y2), multiplication (Y3), decimals (Y4), percentages (Y5), and ratio (Y6). Making them nodes lets us trace which contexts appear at each stage and prevents the AI from overusing one context or choosing age-inappropriate ones.

**Examples**: `shopping_and_money`, `cooking_and_recipes`, `measurement_practical`, `time_and_timetables`, `sports_and_games`, `building_and_construction`, `travel_and_distance`, `nature_and_science`, `sharing_and_fairness`, `scaling_recipes`, `map_reading`

### 1.4 `CPAPathway`

**What it is**: A specific concrete-pictorial-abstract route through a concept at a given difficulty level. This is the heart of the redesign.

**Why a node and not an enum**: In the previous schema, `cpa_stage` was a 6-value enum (`concrete`, `pictorial`, `abstract`, `concrete_pictorial`, `pictorial_abstract`, `concrete_pictorial_abstract`). This is inadequate for three reasons:

1. **CPA is cyclical, not linear** (NCETM position). A child working at "expected" level on column addition may need to re-enter concrete (Dienes blocks) when they encounter carrying across a zero in 504 - 268. The enum implies a one-directional progression that does not match how mastery teaching actually works.

2. **CPA interacts with DifficultyLevel**. The `entry` level of a Y3 addition concept uses Dienes blocks (concrete). The `expected` level uses columnar notation (abstract). But a child at `greater_depth` might re-enter pictorial (bar model) to reason about a word problem. The CPA stage is *per difficulty level*, not per concept.

3. **Each CPA stage has different specific content**. "Concrete for Y2 fractions" means fraction tiles and paper folding. "Concrete for Y5 fractions" means Cuisenaire rods and fraction circles for equivalence. A flat enum cannot carry this specificity.

A `CPAPathway` node captures a *specific route* through the CPA cycle for a given concept at a given difficulty level, linking to the exact manipulatives and representations the child should use at each stage.

### 1.5 `ReasoningPromptType`

**What it is**: A named pattern for mathematical reasoning questions. The NCETM, NRICH, and White Rose all use a standard set of reasoning prompt structures. These are not content -- they are *question templates* that the AI should deploy.

**Why a node**: Reasoning prompt types have their own progression (Y1 children can do `odd_one_out`; `always_sometimes_never` is developmentally appropriate from Y3+; `convince_me` requires formal proof skills from Y5+). Making them nodes lets us link them to KeyStages with age-appropriateness metadata.

**Examples**: `always_sometimes_never`, `true_or_false`, `spot_the_mistake`, `odd_one_out`, `convince_me`, `how_many_ways`, `what_if`, `what_comes_next`, `same_and_different`, `would_you_rather`

---

## 2. Property Tables

### 2.1 `MathsRepresentation` Properties

| Property | Type | Required | Rationale |
|---|---|---|---|
| `representation_id` | string | Yes | Unique ID. Format: `MR-{code}` e.g. `MR-NUMLINE`, `MR-BARMOD` |
| `name` | string | Yes | Display name. E.g. "Number Line", "Bar Model" |
| `description` | string | Yes | What this representation is and what mathematical structure it foregrounds |
| `representation_type` | string (enum) | Yes | `diagrammatic` / `tabular` / `notational` / `physical_model` |
| `agent_prompt` | string | Yes | Instruction for AI: how to describe/draw/use this representation when generating content |
| `key_stages` | string[] | Yes | Which key stages this representation is used in. E.g. `["KS1", "KS2", "KS3"]` |
| `variants` | object[] | No | Year-specific variants. E.g. number line: `{year: "Y1", variant: "structured, 0-20"}`, `{year: "Y3", variant: "empty, to 1000"}` |
| `mathematical_structure` | string | No | What mathematical idea this representation makes visible. E.g. "Part-whole relationship", "Proportional comparison", "Positional magnitude" |
| `display_category` | string | Yes | `"Maths Ontology"` |
| `display_color` | string | Yes | `"#2563EB"` (Blue-600) |
| `display_icon` | string | Yes | `"analytics"` |

### 2.2 `MathsManipulative` Properties

| Property | Type | Required | Rationale |
|---|---|---|---|
| `manipulative_id` | string | Yes | Unique ID. Format: `MM-{code}` e.g. `MM-DIENES`, `MM-NUMICON` |
| `name` | string | Yes | Display name. E.g. "Dienes Blocks (Base-10 Apparatus)" |
| `description` | string | Yes | What this manipulative is, physically |
| `manipulative_type` | string (enum) | Yes | `proportional` (size encodes value -- Dienes, Cuisenaire) / `non_proportional` (tokens -- counters, coins) / `structural` (pattern/structure -- Numicon, ten frames) |
| `is_virtual_available` | boolean | Yes | Whether a digital/virtual version exists for screen-based learning |
| `virtual_interaction_notes` | string | No | How to simulate this manipulative digitally. E.g. "Drag-and-drop Dienes blocks with automatic regrouping animation" |
| `agent_prompt` | string | Yes | Instruction for AI: how to describe using this manipulative in a lesson, including for parents who may not have it at home |
| `primary_year_range` | string | Yes | When this manipulative is most commonly used. E.g. "Y1-Y3" for Dienes, "EYFS-Y1" for Numicon |
| `secondary_year_range` | string | No | When this manipulative is still valid but less common. E.g. "Y4-Y6" for Dienes (revisiting for decimals) |
| `key_stages` | string[] | Yes | Broader KS applicability |
| `display_category` | string | Yes | `"Maths Ontology"` |
| `display_color` | string | Yes | `"#D97706"` (Amber-600) |
| `display_icon` | string | Yes | `"extension"` |

### 2.3 `MathsContext` Properties

| Property | Type | Required | Rationale |
|---|---|---|---|
| `context_id` | string | Yes | Unique ID. Format: `MC-{code}` e.g. `MC-SHOP`, `MC-COOK` |
| `name` | string | Yes | Display name. E.g. "Shopping and Money" |
| `description` | string | Yes | What real-world scenario this context covers |
| `context_type` | string (enum) | Yes | `everyday` (shopping, cooking) / `cross_curricular` (science measurement, geography map reading) / `investigative` (open-ended mathematical exploration) / `historical` (ancient number systems, historical measurement) |
| `age_suitability` | string | Yes | Year range. E.g. "Y1-Y6" for shopping, "Y5-KS4" for scaling recipes |
| `cross_curricular_subjects` | string[] | No | Which other subjects this context connects to. E.g. `["Science", "Geography"]` for measurement context |
| `agent_prompt` | string | Yes | How the AI should embed this context in lesson content |
| `example_problems` | string[] | No | 2-3 sample problems in this context to guide AI generation |
| `safeguarding_notes` | string | No | E.g. "Avoid assumptions about pocket money or family financial situations" |
| `display_category` | string | Yes | `"Maths Ontology"` |
| `display_color` | string | Yes | `"#059669"` (Emerald-600) |
| `display_icon` | string | Yes | `"public"` |

### 2.4 `CPAPathway` Properties

| Property | Type | Required | Rationale |
|---|---|---|---|
| `pathway_id` | string | Yes | Unique ID. Format: `CPA-{concept_id}-DL{level}` e.g. `CPA-MA-Y3-C014-DL01` |
| `name` | string | Yes | Human-readable. E.g. "Column Addition (Entry): Concrete with Dienes" |
| `entry_stage` | string (enum) | Yes | `concrete` / `pictorial` / `abstract` -- where this pathway *starts* |
| `target_stage` | string (enum) | Yes | `concrete` / `pictorial` / `abstract` -- where this pathway aims to *reach* |
| `stage_sequence` | string[] | Yes | Ordered CPA stages in this pathway. E.g. `["concrete", "pictorial"]` or `["concrete", "pictorial", "abstract"]` or `["abstract", "pictorial"]` (re-entry) |
| `is_reentry` | boolean | Yes | `true` if this pathway involves returning to a more concrete stage from a more abstract one. This is the cyclical CPA that the NCETM describes. |
| `reentry_trigger` | string | No | When `is_reentry` is true: what triggers the return to concrete. E.g. "Cascading exchange across zero (e.g. 600 - 347) typically causes procedural breakdown requiring concrete support" |
| `concrete_description` | string | No | What the concrete stage looks like for this specific pathway |
| `pictorial_description` | string | No | What the pictorial stage looks like for this specific pathway |
| `abstract_description` | string | No | What the abstract stage looks like for this specific pathway |
| `transition_guidance` | string | Yes | How to move between stages. E.g. "Move from Dienes to place value chart when child can partition without physical regrouping. Move from chart to columnar notation when child can describe the process verbally." |
| `agent_prompt` | string | Yes | Full instruction for AI: how to implement this CPA pathway in a lesson |
| `display_category` | string | Yes | `"Maths Ontology"` |
| `display_color` | string | Yes | `"#7C3AED"` (Violet-600, matching ThinkingLens family) |
| `display_icon` | string | Yes | `"route"` |

### 2.5 `ReasoningPromptType` Properties

| Property | Type | Required | Rationale |
|---|---|---|---|
| `prompt_type_id` | string | Yes | Unique ID. Format: `RPT-{code}` e.g. `RPT-ASN` (Always Sometimes Never) |
| `name` | string | Yes | Display name. E.g. "Always, Sometimes, Never" |
| `description` | string | Yes | What this prompt pattern is and how it develops reasoning |
| `question_template` | string | Yes | The structural template. E.g. "{mathematical statement}. Is this always true, sometimes true, or never true? Prove it." |
| `example_questions` | object[] | Yes | Year-banded examples. E.g. `[{year: "Y3", question: "When you add two odd numbers, the answer is even. Always, sometimes, or never?"}, {year: "Y6", question: "A square number has an odd number of factors. Always, sometimes, or never?"}]` |
| `minimum_year` | string | Yes | Earliest year this prompt type is developmentally appropriate. E.g. "Y1" for `odd_one_out`, "Y3" for `always_sometimes_never`, "Y5" for `convince_me` (formal justification) |
| `nc_aim` | string (enum) | Yes | Which NC aim this primarily serves: `reasoning` / `problem_solving` |
| `agent_prompt` | string | Yes | How the AI should construct questions of this type, including common pitfalls |
| `source` | string | No | Attribution. E.g. "NCETM Mastery PD materials", "NRICH" |
| `display_category` | string | Yes | `"Maths Ontology"` |
| `display_color` | string | Yes | `"#DC2626"` (Red-600) |
| `display_icon` | string | Yes | `"psychology"` |

---

## 3. Relationship Model

### 3.1 Core Relationships (ASCII)

```
                    (:KeyStage)
                        |
               [:HAS_YEAR]
                        |
                     (:Year)
                        |
              [:HAS_PROGRAMME]
                        |
                   (:Programme)
                        |
                  [:HAS_DOMAIN]
                        |
                    (:Domain)
                   /    |    \
        [:HAS_CLUSTER]  |   [:HAS_VEHICLE]
              /         |          \
  (:ConceptCluster)     |    (:ContentVehicle)      <-- existing nodes
              |         |
         [:GROUPS]  [:CONTAINS]
              |         |
              v         v
           (:Concept) <---------[:TEACHES]---------- (:Objective)
            /  |  \
           /   |   \
          /    |    \
         v     v     v
   [:HAS_DIFFICULTY_LEVEL]      [:DEVELOPS_SKILL]
         |                            |
         v                            v
  (:DifficultyLevel)       (:MathematicalReasoning)
         |
   [:HAS_CPA_PATHWAY]        <--- NEW relationship
         |
         v
   (:CPAPathway)
      /   |   \
     /    |    \
    v     v     v
[:USES_MANIPULATIVE]  [:USES_REPRESENTATION]  [:EMBEDDED_IN_CONTEXT]
    |                       |                        |
    v                       v                        v
(:MathsManipulative)  (:MathsRepresentation)  (:MathsContext)
```

### 3.2 Complete Relationship Table

#### Relationships FROM new Maths nodes

| From | Relationship | To | Properties | Cardinality | Description |
|---|---|---|---|---|---|
| `CPAPathway` | `USES_MANIPULATIVE` | `MathsManipulative` | `{role: str, notes: str}` | Many-to-many | Which concrete manipulatives this pathway uses. `role`: `primary` (main manipulative) or `support` (backup/extension). `notes`: specific usage guidance. |
| `CPAPathway` | `USES_REPRESENTATION` | `MathsRepresentation` | `{role: str, stage: str, notes: str}` | Many-to-many | Which representations this pathway uses. `stage`: which CPA stage this representation belongs to (`concrete`, `pictorial`, `abstract`). `role`: `primary` or `alternative`. |
| `CPAPathway` | `EMBEDDED_IN_CONTEXT` | `MathsContext` | `{suitability: str}` | Many-to-many | Which real-world contexts work for this pathway. `suitability`: `strong` / `adequate` / `stretch`. |
| `MathsManipulative` | `PROGRESSES_TO` | `MathsManipulative` | `{domain: str, rationale: str}` | Many-to-many | Manipulative progression within a domain. E.g. Numicon PROGRESSES_TO Dienes for place value. Domain-specific because progression differs by topic. |
| `MathsRepresentation` | `PROGRESSES_TO` | `MathsRepresentation` | `{domain: str, rationale: str}` | Many-to-many | Representation progression. E.g. ten_frame PROGRESSES_TO place_value_chart for place value work. |
| `ReasoningPromptType` | `APPROPRIATE_FOR` | `KeyStage` | `{agent_prompt: str, example_questions: str[]}` | Many-to-many | Age-banded prompt guidance, following the ThinkingLens PROMPT_FOR pattern. |

#### Relationships TO new Maths nodes (from existing nodes)

| From | Relationship | To | Properties | Cardinality | Description |
|---|---|---|---|---|---|
| `DifficultyLevel` | `HAS_CPA_PATHWAY` | `CPAPathway` | `{}` | One-to-one (or one-to-few) | Each difficulty level of each concept has a primary CPA pathway. This is THE key structural relationship -- it binds CPA to difficulty. |
| `Concept` | `USES_REPRESENTATION` | `MathsRepresentation` | `{rank: int}` | Many-to-many | Which representations are used for this concept overall (aggregated across all DLs). `rank=1` is the primary representation. |
| `Concept` | `USES_MANIPULATIVE` | `MathsManipulative` | `{rank: int}` | Many-to-many | Which manipulatives are used for this concept overall. |
| `ConceptCluster` | `USES_PROMPT_TYPE` | `ReasoningPromptType` | `{rank: int, example: str}` | Many-to-many | Which reasoning prompt types work for this cluster's concepts. |
| `ConceptCluster` | `SUGGESTED_CONTEXT` | `MathsContext` | `{rank: int, rationale: str}` | Many-to-many | Which real-world contexts work for embedding this cluster's learning. |
| `MathsManipulative` | `SUPPORTS_LEARNING_OF` | `Subject` | `{}` | Many-to-many | Cross-layer link, following InteractionType pattern. Mostly Mathematics, but e.g. measuring_equipment also supports Science. |

#### Relationships BETWEEN new Maths nodes

| From | Relationship | To | Properties | Cardinality | Description |
|---|---|---|---|---|---|
| `MathsManipulative` | `BRIDGES_TO` | `MathsRepresentation` | `{transition_notes: str}` | Many-to-many | How a concrete manipulative transitions to a pictorial representation. E.g. Dienes blocks BRIDGES_TO place_value_chart ("Draw the Dienes you have used, recording tens as sticks and ones as dots"). This is the C-to-P transition in CPA. |
| `MathsRepresentation` | `FORMALISES_AS` | `MathsRepresentation` | `{transition_notes: str}` | Many-to-many | How a pictorial representation transitions to abstract notation. E.g. place_value_chart FORMALISES_AS expanded_notation ("Write the number shown in the chart as 300 + 40 + 7"). This is the P-to-A transition in CPA. |

---

## 4. How CPA Cycles Work in the Graph

### 4.1 The Core Insight: CPA is Per-Difficulty-Level, Not Per-Concept

The existing DifficultyLevel nodes already capture the progression from `entry` through `developing` to `expected` and `greater_depth`. Look at the existing data for MA-Y3-C014 (Column Addition):

- **Entry** (DL01): "Adding two three-digit numbers using **Dienes blocks**, physically regrouping" -- this is CONCRETE
- **Developing** (DL02): "Setting out columnar addition on paper with correct alignment, carrying between columns, with a **place value grid** for support" -- this is PICTORIAL bridging to ABSTRACT
- **Expected** (DL03): "Fluent columnar addition of any two three-digit numbers, including multiple carries, **without support**" -- this is ABSTRACT
- **Greater depth** (DL04): "Adding where the result exceeds 1000, and **checking with estimation**" -- this is ABSTRACT with metacognitive overlay

The CPA progression is ALREADY ENCODED in the DifficultyLevel descriptions. What is missing is the *structure* that makes this explicit and machine-queryable. The `CPAPathway` node provides that structure.

### 4.2 The Cyclical CPA Model

Here is how a re-entry cycle works in the graph:

```
Concept: MA-Y3-C015 (Column Subtraction)

DifficultyLevel 1 (entry):
  CPAPathway: CPA-MA-Y3-C015-DL01
    entry_stage: concrete
    target_stage: pictorial
    stage_sequence: ["concrete", "pictorial"]
    is_reentry: false
    USES_MANIPULATIVE -> Dienes blocks (role: primary)
    USES_REPRESENTATION -> place_value_chart (stage: pictorial)

DifficultyLevel 2 (developing):
  CPAPathway: CPA-MA-Y3-C015-DL02
    entry_stage: pictorial
    target_stage: abstract
    stage_sequence: ["pictorial", "abstract"]
    is_reentry: false
    USES_REPRESENTATION -> place_value_grid (stage: pictorial)
    USES_REPRESENTATION -> columnar_notation (stage: abstract)

DifficultyLevel 3 (expected):
  CPAPathway: CPA-MA-Y3-C015-DL03
    entry_stage: abstract
    target_stage: abstract
    stage_sequence: ["abstract"]
    is_reentry: false
    USES_REPRESENTATION -> columnar_notation (stage: abstract)

DifficultyLevel 4 (greater_depth):
  CPAPathway: CPA-MA-Y3-C015-DL04
    entry_stage: abstract
    target_stage: abstract
    stage_sequence: ["abstract", "pictorial", "abstract"]   <-- RE-ENTRY
    is_reentry: true
    reentry_trigger: "Cascading exchange across zero (e.g. 600-347).
      Child may need to return to pictorial place value chart to
      visualise the exchange chain: 6 hundreds -> 5 hundreds + 10 tens
      -> 5 hundreds + 9 tens + 10 ones."
    USES_REPRESENTATION -> columnar_notation (stage: abstract, role: primary)
    USES_REPRESENTATION -> place_value_chart (stage: pictorial, role: support)
    USES_MANIPULATIVE -> Dienes blocks (role: support, notes: "For children
      who cannot visualise the cascading exchange, return to physical Dienes
      briefly to rebuild understanding before returning to written method")
```

This captures exactly what happens in a real Y3 classroom: most children work abstractly at greater_depth, but some hit a wall at cascading exchanges and need to cycle back through concrete/pictorial before returning to abstract. The `is_reentry: true` flag and `reentry_trigger` tell the AI when and why to offer concrete support even at a higher difficulty level.

### 4.3 Querying the CPA Model

**"What manipulatives does a Y3 child at entry level need for column addition?"**
```cypher
MATCH (c:Concept {concept_id: 'MA-Y3-C014'})
      -[:HAS_DIFFICULTY_LEVEL]->(dl:DifficultyLevel {label: 'entry'})
      -[:HAS_CPA_PATHWAY]->(cpa:CPAPathway)
      -[:USES_MANIPULATIVE]->(m:MathsManipulative)
RETURN c.name, dl.description, cpa.entry_stage, cpa.target_stage,
       m.name, cpa.transition_guidance
```

**"Show me the full CPA cycle for a concept, across all difficulty levels"**
```cypher
MATCH (c:Concept {concept_id: 'MA-Y3-C014'})
      -[:HAS_DIFFICULTY_LEVEL]->(dl:DifficultyLevel)
      -[:HAS_CPA_PATHWAY]->(cpa:CPAPathway)
OPTIONAL MATCH (cpa)-[:USES_MANIPULATIVE]->(m:MathsManipulative)
OPTIONAL MATCH (cpa)-[ur:USES_REPRESENTATION]->(r:MathsRepresentation)
RETURN dl.level_number, dl.label, dl.description,
       cpa.entry_stage, cpa.target_stage, cpa.stage_sequence,
       cpa.is_reentry, cpa.reentry_trigger,
       collect(DISTINCT m.name) AS manipulatives,
       collect(DISTINCT {rep: r.name, stage: ur.stage}) AS representations
ORDER BY dl.level_number
```

**"Which manipulatives progress from Numicon across year groups?"**
```cypher
MATCH path = (start:MathsManipulative {name: 'Numicon'})
              -[:PROGRESSES_TO*1..3]->(next:MathsManipulative)
RETURN [n IN nodes(path) | n.name] AS progression,
       [r IN relationships(path) | r.domain] AS domains
```

**"Find all CPA re-entry points across Y3 Maths"**
```cypher
MATCH (c:Concept)-[:HAS_DIFFICULTY_LEVEL]->(dl:DifficultyLevel)
      -[:HAS_CPA_PATHWAY]->(cpa:CPAPathway {is_reentry: true})
WHERE c.concept_id STARTS WITH 'MA-Y3'
RETURN c.name, dl.label, cpa.reentry_trigger, cpa.stage_sequence
```

---

## 5. Example Instances: Real Maths Teaching Scenarios

### 5.1 Scenario: Y2 Fractions -- Finding 1/3 of a Quantity

**Child profile**: Year 2, developing level, learning to find unit fractions of quantities.

**Graph traversal**:

```
Concept: MA-Y2-C012 "Recognise, find, name and write fractions 1/3, 1/4, 2/4 and 3/4"

DifficultyLevel: DL02 (developing)
  "Find fractions of quantities (1/3 of 12)"

  CPAPathway: CPA-MA-Y2-C012-DL02
    entry_stage: concrete
    target_stage: pictorial
    stage_sequence: ["concrete", "pictorial"]
    is_reentry: false
    transition_guidance: "Start with physical sharing of counters into
      equal groups. Once child can explain 'I shared 12 into 3 equal
      groups so 1/3 of 12 is 4', bridge to bar model showing the same
      sharing as a diagram. Do NOT move to pictorial until child can
      verbalise the concrete step."

    USES_MANIPULATIVE -> MM-COUNTERS (role: primary, notes: "12 counters,
      shared into 3 groups of 4")
    USES_MANIPULATIVE -> MM-FRAC-TILES (role: support, notes: "Fraction
      wall to show 1/3 as a proportion of the whole")

    USES_REPRESENTATION -> MR-BARMOD (stage: pictorial, role: primary,
      notes: "Bar divided into 3 equal parts, total labelled 12,
      each part labelled ?")
    USES_REPRESENTATION -> MR-PARTWHOL (stage: pictorial, role: alternative,
      notes: "Part-whole model with 12 at top, three equal parts below")

    EMBEDDED_IN_CONTEXT -> MC-SHARE (suitability: strong)
      "Sharing 12 sweets equally between 3 children"
    EMBEDDED_IN_CONTEXT -> MC-COOK (suitability: adequate)
      "Cutting a pizza into 3 equal slices"

ConceptCluster: MA-Y2-CL-xxx "Fractions of shapes and quantities"
  USES_PROMPT_TYPE -> RPT-STM {rank: 1}
    "Spot the mistake: Sam says 1/3 of 12 is 3 because 12 divided by 4
    is 3. What is wrong with Sam's thinking?"
  SUGGESTED_CONTEXT -> MC-SHARE {rank: 1}
  SUGGESTED_CONTEXT -> MC-COOK {rank: 2}
```

**What the AI generates from this**: A lesson that starts with physical counters being shared into groups (concrete), transitions to drawing bar models (pictorial) once the child demonstrates understanding, uses a "sharing sweets" context for engagement, and includes a "Spot the Mistake" reasoning question. The DifficultyLevel provides the expected task ("Find 1/3 of 12") and common errors ("Thinking 1/3 > 1/2 because 3 > 2").

### 5.2 Scenario: Y3 Column Addition -- Greater Depth Re-Entry

**Child profile**: Year 3, greater depth, encountering addition that crosses 1000.

**Graph traversal**:

```
Concept: MA-Y3-C014 "Add numbers with up to three digits using columnar addition"

DifficultyLevel: DL04 (greater_depth)
  "Adding three-digit numbers where the result exceeds 1000,
   and checking with estimation"

  CPAPathway: CPA-MA-Y3-C014-DL04
    entry_stage: abstract
    target_stage: abstract
    stage_sequence: ["abstract"]
    is_reentry: false
    transition_guidance: "Child should be working abstractly. If they
      struggle with the four-digit answer, use estimation as the
      metacognitive scaffold (not concrete materials at this level)."

    USES_REPRESENTATION -> MR-COLUMNAR (stage: abstract, role: primary)
    USES_REPRESENTATION -> MR-NUMLINE (stage: abstract, role: support,
      notes: "Empty number line for estimation/rounding, not for calculation")

    EMBEDDED_IN_CONTEXT -> MC-TRAVEL (suitability: strong)
      "Combining journey distances that total more than 1000m"
    EMBEDDED_IN_CONTEXT -> MC-SHOP (suitability: strong)
      "Adding up prices in a catalogue that total more than 1000p"

ConceptCluster: MA-Y3-CL-xxx "Columnar addition"
  USES_PROMPT_TYPE -> RPT-STM {rank: 1}
    "A pupil says 587 + 468 = 955. Without calculating, explain
     why this must be wrong."
  USES_PROMPT_TYPE -> RPT-ASN {rank: 2}
    "When you add two three-digit numbers, the answer is always
     a four-digit number. Always, sometimes, or never?"
```

**What the AI generates**: A lesson working entirely in abstract columnar notation, with estimation as a checking strategy. The AI uses a travel or shopping context for word problems. The reasoning prompts develop the child's number sense (Can you spot an impossible answer? Can you generalise about when addition does/doesn't cross 1000?).

### 5.3 Scenario: Y7 Algebra -- First Encounter, Full CPA Cycle

**Child profile**: Year 7, emerging level, first encounter with expanding single brackets.

**Graph traversal**:

```
Concept: MA-KS3-Cxxx "Expand single brackets"

DifficultyLevel: DL01 (emerging)
  "Expand single brackets with positive terms using algebra tiles"

  CPAPathway: CPA-MA-KS3-Cxxx-DL01
    entry_stage: concrete
    target_stage: abstract
    stage_sequence: ["concrete", "pictorial", "abstract"]
    is_reentry: false
    transition_guidance: "This is a FIRST ENCOUNTER. Even at secondary,
      the NCETM recommends starting with concrete manipulatives for new
      concepts. Use algebra tiles to build the area model physically.
      Bridge to a drawn area model diagram. Then connect to the formal
      algebraic notation. The transition from pictorial to abstract is
      the critical step -- the child must see that 3(x + 2) = 3x + 6
      IS the area model written in symbols."

    USES_MANIPULATIVE -> MM-ALGTILE (role: primary, notes: "Use x-tiles
      and unit tiles. Build 3 rows of (x + 2). Total area = 3x + 6")
    USES_MANIPULATIVE -> MM-COUNTERS (role: support, notes: "Double-sided
      counters for negative terms in later lessons, not needed at emerging")

    USES_REPRESENTATION -> MR-ALGTILE-DIAG (stage: pictorial, role: primary,
      notes: "Drawn area model: rectangle with width 3, length (x + 2)")
    USES_REPRESENTATION -> MR-AREA-MODEL (stage: pictorial, role: alternative)
    USES_REPRESENTATION -> MR-NOTATION (stage: abstract, notes:
      "3(x + 2) = 3 x x + 3 x 2 = 3x + 6")

    EMBEDDED_IN_CONTEXT -> MC-BUILD (suitability: strong)
      "Area of rectangles with algebraic sides"

ConceptCluster: MA-KS3-CL-xxx "Expanding brackets"
  USES_PROMPT_TYPE -> RPT-CONVINCE {rank: 1}
    "Convince me that 3(x + 2) and 3x + 6 are the same thing.
     What if x = 5? What if x = 10? Does it always work?"
  USES_PROMPT_TYPE -> RPT-WHATIF {rank: 2}
    "What if the bracket had a subtraction? What would 3(x - 2) look like
     with algebra tiles?"
```

**What the AI generates**: A lesson that starts with physical algebra tiles (even at KS3), bridges to drawn area models, then formalises into algebraic notation. This is exactly how White Rose Secondary and the NCETM recommend introducing algebra -- concrete first, regardless of the child's age.

### 5.4 Scenario: Y4 Times Tables Fluency (No CPA -- Pure Abstract)

**Child profile**: Year 4, developing level, building fluency with 6, 7, 8 times tables.

**Graph traversal**:

```
Concept: MA-Y4-C0xx "Recall multiplication and division facts for
  multiplication tables up to 12 x 12"

DifficultyLevel: DL02 (developing)
  "Recall 6x, 7x, 8x tables within 10 seconds per fact"

  CPAPathway: CPA-MA-Y4-C0xx-DL02
    entry_stage: abstract
    target_stage: abstract
    stage_sequence: ["abstract"]
    is_reentry: false
    transition_guidance: "By Y4 developing level, times table fluency
      should be practised abstractly. If the child cannot recall facts,
      do NOT revert to arrays -- instead use derived fact strategies
      (e.g. 8x = double 4x, 6x = 5x + 1x). Concrete materials are
      for UNDERSTANDING multiplication, not for FLUENCY practice."

    USES_REPRESENTATION -> MR-MULTGRID (stage: abstract, role: primary,
      notes: "Multiplication grid for pattern-spotting and self-checking")
    USES_REPRESENTATION -> MR-ARRAY (stage: pictorial, role: support,
      notes: "ONLY if child has a fundamental misconception about what
      multiplication means -- not for routine fluency work")

    EMBEDDED_IN_CONTEXT -> MC-SPORT (suitability: adequate)
      "Team games: 6 teams of 7 players, 8 rows of 6 seats"

ConceptCluster: MA-Y4-CL-xxx "Multiplication facts to 12x12"
  USES_PROMPT_TYPE -> RPT-HMW {rank: 1}
    "How many ways can you make 24 using multiplication?"
  USES_PROMPT_TYPE -> RPT-OOO {rank: 2}
    "48, 54, 63, 72 -- which is the odd one out? Why?"
```

**What the AI generates**: A pure fluency session -- no manipulatives, rapid recall practice, derived fact strategies, pattern-spotting in multiplication grids. The key insight: `CPAPathway` with `stage_sequence: ["abstract"]` tells the AI that this is NOT a conceptual introduction -- this is drill. The `transition_guidance` explicitly warns against reverting to concrete for fluency work. This distinction is impossible with a flat `cpa_stage` enum.

---

## 6. How CPA Interacts with DifficultyLevel

### 6.1 The General Pattern

For most primary concepts, the CPA-DifficultyLevel interaction follows this pattern:

| DifficultyLevel | Typical CPA entry_stage | Typical CPA target_stage | Notes |
|---|---|---|---|
| Entry (DL01) | `concrete` | `concrete` or `pictorial` | Manipulatives dominate. The child is building first understanding. |
| Developing (DL02) | `concrete` or `pictorial` | `pictorial` or `abstract` | Bridging phase. Manipulatives available as backup. Pictorial representations (bar model, number line, place value chart) are the main tool. |
| Expected (DL03) | `pictorial` or `abstract` | `abstract` | Working towards NC expectation. Pictorial representations still available but child should be moving to standard notation. |
| Greater Depth (DL04) | `abstract` | `abstract` | Fluent abstract work, with reasoning and proof. May re-enter pictorial/concrete for novel problem types (is_reentry: true). |

This is NOT a rigid rule. Some concepts (like Y4 fluency) are abstract from DL01. Some concepts (like EYFS counting) remain concrete through all levels. The `CPAPathway` node captures the *actual* progression for each specific concept at each specific level, rather than imposing a template.

### 6.2 The Re-Entry Pattern (KS2-KS4)

As children encounter more complex instances of a concept, they may need to cycle back. Examples:

| Concept | DifficultyLevel | Re-entry trigger | Re-entry stage |
|---|---|---|---|
| Column subtraction (Y3) | Greater depth | Exchange across zero (600 - 347) | Pictorial (place value chart) |
| Fraction equivalence (Y4) | Expected | Non-obvious equivalences (3/5 = 6/10) | Concrete (fraction tiles) |
| Long division (Y5) | Developing | Division by 2-digit divisor | Pictorial (chunking diagram) |
| Expanding double brackets (KS3) | Secure | Brackets with negative terms | Concrete (algebra tiles) |
| Trigonometry (KS4) | Secure | Non-right-angled triangles | Pictorial (unit circle diagram) |

The `is_reentry: true` flag on a CPAPathway is a powerful signal to the AI: "This child may need concrete/pictorial support even though they are working at a high difficulty level." Without this, the AI would assume that a Y5 child at "expected" level should be working abstractly on everything, which is pedagogically wrong.

### 6.3 EYFS Special Case

EYFS Maths concepts are almost entirely concrete and pictorial. CPAPathway nodes for EYFS would typically have:
- `entry_stage: "concrete"`, `target_stage: "concrete"` (DL01)
- `entry_stage: "concrete"`, `target_stage: "pictorial"` (DL02)
- `entry_stage: "pictorial"`, `target_stage: "pictorial"` (DL03 -- expected for EYFS)

There is no "abstract" stage for most EYFS concepts. Number recognition and early counting are concrete/pictorial activities. The CPAPathway model handles this naturally because `stage_sequence` is flexible.

---

## 7. What This Enables That the Flat Enum Could Not

### 7.1 Problem: "What manipulative should the AI use?"

**Flat enum**: `cpa_stage: "concrete_pictorial_abstract"` -- tells the AI nothing about *which* concrete manipulative. The AI must guess, and may pick Numicon for a Y5 child (too young) or algebra tiles for a Y2 child (too old).

**Graph model**: `CPAPathway -[:USES_MANIPULATIVE]-> MathsManipulative` -- tells the AI *exactly* which manipulative, with role (primary/support) and usage notes. The AI cannot pick an inappropriate manipulative because the data constrains its choices.

### 7.2 Problem: "When should the AI offer concrete support to an advanced child?"

**Flat enum**: Cannot represent this. A child working at `greater_depth` would have `cpa_stage: "abstract"`, and the AI would never offer concrete support.

**Graph model**: `CPAPathway {is_reentry: true, reentry_trigger: "..."}` -- the AI knows that for THIS specific concept at THIS difficulty level, a return to concrete is expected and appropriate. It can proactively offer Dienes blocks when the child struggles with cascading exchanges, instead of just repeating the abstract explanation.

### 7.3 Problem: "How do representations progress across year groups?"

**Flat enum**: No progression information. The AI treats "number_line" as the same thing in Y1 and Y6.

**Graph model**: `MathsRepresentation.variants` captures year-specific forms. `MathsRepresentation -[:PROGRESSES_TO]-> MathsRepresentation` captures the progression chain (ten_frame -> place_value_chart -> expanded_notation -> standard_notation). The AI can show the child where they are in the representation progression and what comes next.

### 7.4 Problem: "How does the AI know when to move from concrete to pictorial?"

**Flat enum**: No transition guidance. The AI must improvise.

**Graph model**: `CPAPathway.transition_guidance` provides explicit criteria for stage transitions. E.g. "Move from Dienes to place value chart when child can partition without physical regrouping." The AI can use this to set assessment checkpoints in the lesson.

### 7.5 Problem: "Which reasoning prompts are age-appropriate?"

**Flat enum / property**: `reasoning_prompts: ["always_sometimes_never", "convince_me"]` -- no age-appropriateness information.

**Graph model**: `ReasoningPromptType {minimum_year: "Y3"}` + `APPROPRIATE_FOR` relationship to KeyStage with `agent_prompt` -- the AI knows not to use "Always, Sometimes, Never" with Y1 children and gets age-specific question examples.

### 7.6 Problem: "The AI generates the same context for every lesson"

**Flat property**: `application_contexts: ["money", "measurement"]` -- a static list that the AI reads once and may fixate on.

**Graph model**: `ConceptCluster -[:SUGGESTED_CONTEXT]-> MathsContext` with `rank` -- the AI can rotate through contexts, prioritise the best fit, and ensure variety across a sequence of lessons. The `MathsContext.safeguarding_notes` property prevents the AI from using culturally insensitive or financially assumptive contexts.

---

## 8. Integration with NC Three Aims

The National Curriculum's three aims for Mathematics are Fluency, Reasoning, and Problem-Solving. These are not node labels -- they are lenses that cut across the entire graph. Here is how they map:

### 8.1 Fluency

**Where it lives**: Primarily in `DifficultyLevel` descriptions (what facts and procedures should be automatic at each level) and `CPAPathway` (fluency practice pathways typically have `stage_sequence: ["abstract"]` with no manipulatives).

**Signal to the AI**: When `CPAPathway.entry_stage == "abstract"` AND `CPAPathway.target_stage == "abstract"` AND no `USES_MANIPULATIVE` relationships exist, the AI knows this is a fluency-focused pathway. Generate drill, rapid recall, and speed challenges.

**Fluency targets** become a property on `ConceptCluster`:

| Property | Type | Required | Rationale |
|---|---|---|---|
| `fluency_targets` | string[] | Yes (for Maths clusters) | What must be practised to automaticity. E.g. `["Recall addition/subtraction facts to 20", "Number bonds to 10"]` |
| `prerequisite_fluency` | string[] | No | What must ALREADY be automatic before starting this cluster. E.g. `["Number bonds to 10", "Counting in 2s, 5s, 10s"]` |
| `nc_aim_emphasis` | string (enum) | Yes | `fluency` / `reasoning` / `problem_solving` / `mixed` |

### 8.2 Reasoning

**Where it lives**: In `ReasoningPromptType` nodes linked to `ConceptCluster` via `USES_PROMPT_TYPE`, and in the `MathematicalReasoning` epistemic skills already in the graph.

**Signal to the AI**: When `ConceptCluster.nc_aim_emphasis == "reasoning"` or the cluster has `USES_PROMPT_TYPE` relationships, include structured reasoning questions in the lesson. The `ReasoningPromptType.question_template` provides the structure; the `APPROPRIATE_FOR` relationship ensures age-appropriateness.

### 8.3 Problem-Solving

**Where it lives**: In `MathsContext` nodes (real-world problems require context) and in `VehicleTemplate` (the `problem_solving_task` template structures the session).

**Signal to the AI**: When `ConceptCluster.nc_aim_emphasis == "problem_solving"` or the cluster has `SUGGESTED_CONTEXT` relationships, generate multi-step problems embedded in real-world contexts. The `MathsContext.example_problems` provide models; the `VehicleTemplate.session_structure` provides the lesson flow.

---

## 9. Relationship to Existing Graph Nodes

### 9.1 What Changes in Existing Nodes

**`ConceptCluster`** gains three new properties:
- `fluency_targets` (string[], required for Maths)
- `prerequisite_fluency` (string[], optional)
- `nc_aim_emphasis` (string enum, required for Maths)

**`ContentVehicle`** (existing Maths vehicles): These remain as-is. The new Maths ontology nodes complement, not replace, ContentVehicles. ContentVehicles are *authored teaching packs* with specific worked examples. The new nodes are *structural metadata* that helps the AI generate content dynamically. A ContentVehicle might reference specific manipulatives and representations in its free-text properties; the new nodes make those references machine-queryable.

**`DifficultyLevel`**: Gains the `HAS_CPA_PATHWAY` relationship. No property changes needed -- the existing `description`, `example_task`, `example_response`, and `common_errors` are sufficient. The CPAPathway node adds the *how* (which manipulatives, which representations, which CPA stage) to the DifficultyLevel's *what* (what the child should be able to do).

### 9.2 What Does NOT Change

- `Concept`, `Objective`, `Domain`, `Programme` nodes -- unchanged
- `ThinkingLens` and `APPLIES_LENS` -- unchanged (ThinkingLens is cognitive framing; CPA is pedagogical delivery -- they are orthogonal)
- `MathematicalReasoning` skills -- unchanged (the new `ReasoningPromptType` nodes are prompt patterns; `MathematicalReasoning` nodes are skills. A `DEVELOPS_SKILL` relationship from Concept to MathematicalReasoning is already curated)
- `KeyStage`, `Year`, `Subject` hierarchy -- unchanged

### 9.3 Node Counts (Estimated)

| Node Label | Estimated Count | Rationale |
|---|---|---|
| `MathsRepresentation` | ~30-35 | Core representations across KS1-KS4 (see controlled vocabulary in Section 1) |
| `MathsManipulative` | ~25-30 | Core manipulatives across KS1-KS4 (see controlled vocabulary in Section 1) |
| `MathsContext` | ~15-20 | Reusable real-world contexts |
| `CPAPathway` | ~500-600 | One per DifficultyLevel for ~150 Maths concepts x ~3.5 DLs average. Some DLs may share a pathway. |
| `ReasoningPromptType` | ~10-12 | Small fixed set of prompt patterns |
| **Total new nodes** | **~580-700** | |

---

## 10. Display Properties

Following the project's conventions (all nodes need `display_category`, `display_color`, `display_icon`, `name`):

| Node Label | display_category | display_color | display_icon | Rationale |
|---|---|---|---|---|
| `MathsRepresentation` | `"Maths Ontology"` | `"#2563EB"` (Blue-600) | `"analytics"` | Blue for structural/analytical -- representations are structural tools |
| `MathsManipulative` | `"Maths Ontology"` | `"#D97706"` (Amber-600) | `"extension"` | Amber for physical/concrete -- manipulatives are hands-on objects |
| `MathsContext` | `"Maths Ontology"` | `"#059669"` (Emerald-600) | `"public"` | Green for real-world -- contexts connect maths to the world |
| `CPAPathway` | `"Maths Ontology"` | `"#7C3AED"` (Violet-600) | `"route"` | Violet to match ThinkingLens family -- both are pedagogical overlay nodes |
| `ReasoningPromptType` | `"Maths Ontology"` | `"#DC2626"` (Red-600) | `"psychology"` | Red for cognitive challenge -- reasoning prompts push thinking |

---

## 11. VehicleTemplate Requirements

The new ontology does not replace VehicleTemplates -- it informs which template the AI selects. Maths needs these templates (some exist, some are new):

| Template | Exists? | NC Aim | Session Structure | Notes |
|---|---|---|---|---|
| `worked_example_set` | Yes | Mixed | activate_prior -> concrete -> pictorial -> abstract -> apply -> fluency -> reason | Modified: add activation and reasoning bookends |
| `fluency_practice` | **NEW** | Fluency | warm_up -> retrieval -> focused_drill -> speed_challenge -> self_check | For times tables, number bonds, mental arithmetic. No CPA progression -- pure abstract. |
| `reasoning_task` | **NEW** | Reasoning | stimulus -> conjecture -> test -> justify -> generalise | For ASN, Spot the Mistake, Convince Me. Uses `ReasoningPromptType` nodes. |
| `problem_solving_task` | **NEW** | Problem-solving | problem -> represent -> work -> check -> extend | Multi-step real-world problems. Uses `MathsContext` nodes. |
| `mathematical_investigation` | **NEW** | Reasoning + PS | question -> explore -> collect -> pattern -> conjecture -> test -> prove | Open-ended. E.g. "Investigate the digit sums of multiples of 9." |
| `pre_teaching_diagnostic` | **NEW** | N/A | anchor_q -> probe -> misconception_check -> classify | Pre-unit assessment. Uses `DifficultyLevel` entry criteria. |
| `pattern_seeking` | Yes | Reasoning | observe -> describe -> predict -> test -> generalise | Existing template, good fit for Maths. |
| `practical_application` | Yes | Problem-solving | context -> measure/calculate -> record -> interpret | For measurement, statistics, money. |

---

## 12. Open Questions

### 12.1 CPAPathway Granularity

Should every DifficultyLevel have its own CPAPathway, or should some DLs share a pathway? For example, if DL02 (developing) and DL03 (expected) for a concept both involve `["pictorial", "abstract"]` with the same manipulatives and representations, should they share one CPAPathway node or have two?

**My lean**: Separate nodes, even if similar. The `transition_guidance` and `agent_prompt` will differ because the expectations at "developing" and "expected" are different. Shared nodes would force shared guidance, which is pedagogically wrong.

### 12.2 Secondary Maths Coverage

My expertise is Y2-Y6. The KS3-KS4 manipulatives (algebra tiles, protractors, compasses) and representations (coordinate grid, unit circle, tree diagram) need review by a secondary specialist. The CPA model still applies at secondary -- the NCETM is explicit about this -- but the specific pathways need domain expertise I do not have.

### 12.3 Virtual Manipulatives

The `is_virtual_available` flag on `MathsManipulative` is important for a digital-first platform. Some manipulatives (Dienes blocks, fraction tiles, algebra tiles) have excellent virtual versions. Others (Cuisenaire rods, geoboards) work less well on screen. For a home-learning context where parents may not have physical manipulatives, the AI needs to know which manipulatives can be simulated and which need alternatives.

### 12.4 Relationship Between MathsContext and ContentVehicle

The existing `ContentVehicle` nodes for Maths already contain `application_contexts` as free-text properties. Should `MathsContext` nodes replace these, or complement them? My recommendation: `MathsContext` nodes are the canonical source; ContentVehicle free-text contexts are for backward compatibility and human-authored specificity.

### 12.5 Reasoning Prompt Types vs. Thinking Lenses

`ReasoningPromptType` and `ThinkingLens` are both cognitive-framing tools. The difference: ThinkingLens says "frame this cluster through the lens of Patterns" (conceptual framing), while ReasoningPromptType says "ask an Always-Sometimes-Never question" (task structure). They are orthogonal and should both be used. But the AI needs clear guidance on when to use which.

### 12.6 Data Volume

~500-600 CPAPathway nodes is significant. Each needs `transition_guidance` and `agent_prompt` which are non-trivial to author. This is a large data generation task. I recommend:
1. Start with Y1-Y3 (where CPA is most critical and varies most by DL)
2. KS3-KS4 pathways can be simpler (many are `["abstract"]` with one or two representations)
3. Use existing DifficultyLevel descriptions as the seed -- they already encode CPA information implicitly

### 12.7 NC Aim Emphasis at Cluster vs. Concept Level

Should `nc_aim_emphasis` live on `ConceptCluster` or `Concept`? I put it on `ConceptCluster` because a single concept might be taught with a fluency focus in one lesson and a reasoning focus in another. The cluster is the lesson-level unit, so the emphasis belongs there. But a concept like "Recall multiplication facts to 12x12" is inherently fluency-focused regardless of which cluster it sits in. This needs discussion.

---

## 13. Summary: What the Maths Ontology Provides

For an AI tutor generating a Maths lesson, the graph now answers:

1. **What to teach** -- Concept + DifficultyLevel (existing)
2. **How to frame it** -- ThinkingLens (existing) + nc_aim_emphasis (new property)
3. **Where to start on the CPA cycle** -- CPAPathway.entry_stage (new)
4. **Which manipulatives to use** -- CPAPathway -> USES_MANIPULATIVE -> MathsManipulative (new)
5. **Which representations to use** -- CPAPathway -> USES_REPRESENTATION -> MathsRepresentation (new)
6. **When to transition between CPA stages** -- CPAPathway.transition_guidance (new)
7. **When to cycle back to concrete** -- CPAPathway.is_reentry + reentry_trigger (new)
8. **What real-world context to embed it in** -- ConceptCluster -> SUGGESTED_CONTEXT -> MathsContext (new)
9. **What reasoning questions to ask** -- ConceptCluster -> USES_PROMPT_TYPE -> ReasoningPromptType (new)
10. **What fluency targets to set** -- ConceptCluster.fluency_targets (new property)
11. **What common errors to anticipate** -- DifficultyLevel.common_errors (existing)
12. **What session structure to follow** -- VehicleTemplate (existing, with new Maths templates)

This is what a mastery Maths lesson looks like in graph form. Every pedagogical decision that a Y2-Y6 Maths lead makes when planning a lesson is now captured as queryable, structured data.
