# Science Ontology Design: Graph Model for KS2-KS3 Science Topics

**Author**: KS2 + KS3 Science Specialist
**Date**: 2026-02-24
**Scope**: Complete graph ontology for Science topics, designed with full subject freedom after the universal `TopicSuggestion` wrapper was rejected by the teacher panel

---

## 0. Design Rationale: Why Science Needs Its Own Ontology

Science is not organised around "topics" in the way History or Geography are. A History teacher thinks in topics: "The Romans", "The Tudors", "The Industrial Revolution". A Science teacher thinks in **enquiries**: "How does the surface affect friction?", "What factors affect the rate of photosynthesis?", "How can we classify these rocks?".

The universal `TopicSuggestion` model tried to bolt Science enquiry properties onto a topic-shaped wrapper. The result was a node that carried 10 universal properties Science does not need (like `suggestion_type`, which is `prescribed_topic` for 95% of Science entries because the NC specifies content, not topic choice) and forced the most important Science properties -- safety, misconceptions, variables, enquiry type -- into optional fields.

The fundamental problem: **Science's organising principle is the enquiry type, not the topic**. A "Friction Investigation" and a "Plant Growth Enquiry" look superficially similar (both are KS2 Science), but they demand completely different pedagogical structures because one is a `fair_test` and the other is an `observation_over_time`. The enquiry type determines the session structure, the recording format, the variables scaffold, the Working Scientifically skills developed, and the assessment approach. This is not a property -- it is the structural backbone of the node.

This ontology separates what the universal model conflated:
- **What** to investigate (the Science Enquiry, linked to curriculum concepts)
- **How** to investigate it (the enquiry type, with its specific pedagogical structure)
- **What could go wrong** (misconceptions, as first-class linked nodes)
- **What to be careful of** (safety, modelled with CLEAPSS-level rigour)

---

## 1. Node Labels

### 1.1 `:ScienceEnquiry` (Primary node -- replaces `ScienceTopicSuggestion`)

The central node for Science. Renamed from "TopicSuggestion" because Science teachers do not think in "topic suggestions" -- they think in enquiries. Every Science lesson at KS2-KS3 is structured around an enquiry question, even research-based lessons. The NC Working Scientifically strand makes this explicit: "pupils should use different types of scientific enquiries to answer their own questions".

**Why not keep "Topic"?** Because the word "topic" in a Science staffroom means "the next unit" (Forces, Sound, Cells), not "a choosable teaching context". The node name should match what it models. A `ScienceEnquiry` is a complete, teachable investigation context: it has an enquiry question, an enquiry type, equipment, safety notes, variables, misconceptions, and expected outcomes.

### 1.2 `:Misconception` (Separate node -- NOT a property array)

In my original review, I asked for `misconceptions: string[]` as a required property. I was wrong. Having now seen the full data, I am convinced misconceptions should be **separate nodes** for three reasons:

1. **Misconceptions span multiple enquiries**. "Plants get their food from the soil" appears in Plant Growth (Y3), Photosynthesis (KS3), and Ecosystems (KS3). As a property array, this misconception is duplicated three times with slightly different wording. As a node, it is authored once and linked to all three enquiries. When the AI tutor encounters it in one context, it can check whether the child has met -- and overcome -- this misconception in an earlier enquiry.

2. **Misconceptions have their own properties**. Each misconception has: a pupil-language statement, a correct scientific explanation, diagnostic questions that surface it, and a persistence rating (some misconceptions persist into adulthood; others are resolved quickly). None of this fits in a `string[]`.

3. **Misconceptions form chains**. "Particles expand when heated" is a prerequisite misconception for "Gas has no particles" -- if you do not address the first, the second becomes harder to correct. These chains are relationships, not properties.

### 1.3 `:EnquiryType` (Structural node -- the 7 canonical enquiry types)

The 7 enquiry types are NOT just string values in a controlled vocabulary. They are first-class nodes because:

- Each enquiry type has its own **pedagogical structure** (session phases). A `fair_test` follows: question -> hypothesis -> method -> data collection -> analysis -> conclusion. An `identifying_and_classifying` enquiry follows: question -> observation -> property identification -> grouping criteria -> classification -> key construction. These are fundamentally different pedagogical patterns.
- Each enquiry type maps to specific **Working Scientifically skills**. A `fair_test` develops WS-KS2-003 (controlling variables); `identifying_and_classifying` develops WS-KS2-004 (classifying). The AI tutor needs these links to scaffold the right skills.
- Each enquiry type has **age-banded expectations**. A Y3 fair test is qualitative ("which surface was best?"); a Y8 fair test is quantitative with repeat readings and statistical analysis. The `EnquiryType` node carries age-banded `agent_prompt` properties via `PROMPT_FOR` relationships to KeyStage, exactly like ThinkingLens.
- There are exactly 7 of them. They are stable, curriculum-defined, and shared across all Science enquiries. This is a lookup table, not a free-text field.

### 1.4 Considered and Rejected: `:SafetyNote` as a separate node

I considered making safety notes into separate, reusable nodes (e.g. "Wear goggles when using acids" could be shared across all chemistry practicals). I rejected this because:

- Safety notes are highly context-specific. "Wear goggles" in an acids practical is different from "wear goggles" in a rock scratch test (different hazard, different severity, different emergency action).
- CLEAPSS model risk assessments are per-activity, not per-hazard. The safety note needs to be read as a complete instruction for THAT specific enquiry.
- The `hazard_level` triage flag (`low`, `standard`, `elevated`) is sufficient for cross-enquiry safety queries ("show me all elevated-hazard enquiries").

Safety stays as properties on `ScienceEnquiry`, not as a separate node.

---

## 2. Property Tables

### 2.1 `:ScienceEnquiry` Properties

| Property | Type | Required | Rationale |
|---|---|---|---|
| `enquiry_id` | string | Yes | Unique identifier. Format: `SE-{KS}-{NNN}` (e.g. `SE-KS2-001`). Distinct from ContentVehicle IDs to avoid confusion with the existing CV layer. |
| `name` | string | Yes | Human-readable name (e.g. "Friction Investigation", "Photosynthesis Rate Investigation"). |
| `enquiry_question` | string | Yes | The actual question the enquiry answers, in pupil language. E.g. "How does the surface affect how far a toy car travels?" This is what the AI tutor presents to the child. Every Science enquiry starts with a question -- this is the NC Working Scientifically requirement. |
| `science_discipline` | string | Yes | Controlled vocabulary: `general_science` (KS1-KS2), `biology`, `chemistry`, `physics`. Determines which KS3 programme of study the enquiry maps to, which discipline-specific safety protocols apply, and which vocabulary register the AI uses. |
| `key_stage` | string | Yes | `KS1`, `KS2`, `KS3`, or `KS4`. |
| `year_groups` | string[] | Yes | Which year groups this enquiry is suitable for. E.g. `["Y5", "Y6"]` for a forces enquiry that spans the upper KS2 programme. Required because the NC assigns content to specific years within KS2. |
| `curriculum_status` | string | Yes | `mandatory` (NC statutory content), `non_statutory` (NC non-statutory guidance), `extension` (beyond NC, teacher convention). Almost all KS2-KS3 Science is mandatory -- this field exists for the rare extensions. |
| `curriculum_reference` | string[] | Yes | Verbatim NC programme of study references. Required because the AI must be able to cite exactly which statutory requirement this enquiry addresses. Teachers check this. Ofsted checks this. |
| `equipment` | string[] | Yes | Realistic school equipment only. The AI must not suggest equipment schools do not have. At KS2, "oscilloscope" is wrong; "ruler" is right. Each item should be specific enough to order (e.g. "dilute hydrochloric acid (1M)" not just "acid"). |
| `safety_notes` | string | Yes | CLEAPSS-aligned safety instructions for this specific enquiry. Must be present even for low-risk enquiries (stating "Low risk. No specific hazards" is itself a safety assessment). For elevated-hazard enquiries, this should reference the CLEAPSS model risk assessment number where applicable. |
| `hazard_level` | string | Yes | Controlled vocabulary: `low` (no specific hazards -- observation, research, classification), `standard` (normal lab procedures -- goggles, careful handling, hot water), `elevated` (CLEAPSS model risk assessment required -- acids, heating chemicals, biological material, Bunsen burners, flammable gases). This is a triage flag for the AI: `elevated` triggers mandatory safety language in any generated content. |
| `expected_outcome` | string | Yes | What correct scientific understanding looks like after this enquiry. The AI needs this to assess pupil responses, generate marking guidance, and avoid reinforcing misconceptions. Should include the key scientific explanation, not just "pupils will understand forces". |
| `recording_format` | string[] | Yes | Age-appropriate data presentation formats for this enquiry. E.g. `["results table", "bar chart", "written conclusion"]` for KS2, `["results table", "line graph with line of best fit", "conclusion referencing equation"]` for KS3. The AI uses this to generate data recording scaffolds. |
| `variables` | object | No | For `fair_test` and `pattern_seeking` enquiries only. Structure: `{ "independent": string, "dependent": string, "controlled": string[] }`. Null/absent for other enquiry types. The AI needs this to generate the "What will you change? / What will you measure? / What will you keep the same?" scaffold that is the foundation of fair testing at KS2-KS3. |
| `definitions` | string[] | Yes | Technical vocabulary introduced or required by this enquiry. Science has the highest vocabulary density of any primary subject. The AI uses these to scaffold age-appropriate definitions rather than using informal language that creates later misconceptions. |
| `pedagogical_rationale` | string | Yes | Why this enquiry is the right pedagogical vehicle for these concepts. Not just "teaches forces" but "this is the most accessible fair test in the curriculum because pupils can see and feel friction, the variables are tangible, and the measurement (distance) is straightforward". The AI surfaces this for parent-facing content. |
| `common_pitfalls` | string[] | Yes | Teaching pitfalls for this specific enquiry (distinct from pupil misconceptions). E.g. "Pupils water plants inconsistently across conditions, undermining the fair test" is a pitfall; "Plants get food from soil" is a misconception. Pitfalls guide the AI in generating teacher notes and anticipating procedural errors. |
| `cross_curricular_hooks` | string[] | No | Links to other subjects. E.g. `["[Maths] Measuring in cm, drawing bar charts", "[English] Writing a scientific conclusion"]`. Optional because not every enquiry has strong cross-curricular links, though most Science enquiries do. |
| `sensitive_content_notes` | string[] | No | Pedagogical sensitivity notes beyond physical safety. E.g. "Evolution can conflict with some religious beliefs -- present as scientific explanation supported by evidence". "Be sensitive to pupils with hearing impairments -- adapt sound activities". |
| `duration_lessons` | int | No | Estimated number of lessons. Varies by school and depth of coverage. |
| `display_category` | string | Yes | Always `"Science Enquiry"`. For cross-label queries with other topic types. |
| `display_color` | string | Yes | `"#059669"` (Emerald-600, same as existing Science ContentVehicles for visual consistency). |
| `display_icon` | string | Yes | `"science"` (Material icon). |

### 2.2 `:Misconception` Properties

| Property | Type | Required | Rationale |
|---|---|---|---|
| `misconception_id` | string | Yes | Unique identifier. Format: `MC-{NNN}` (e.g. `MC-001`). Global across all Science, not per-enquiry. |
| `name` | string | Yes | Short label for display (e.g. "Food from soil"). |
| `pupil_statement` | string | Yes | The misconception stated in pupil language, as a complete sentence. E.g. "Plants get their food from the soil." Not jargon, not abbreviated. This is what the AI uses in diagnostic questions: "Some children think that plants get their food from the soil. What do you think?" |
| `correct_explanation` | string | Yes | The correct scientific explanation, at the appropriate age level. E.g. "Plants make their own food (glucose) through photosynthesis using light energy, carbon dioxide from the air, and water from the soil. The soil provides water and minerals, but not food." |
| `diagnostic_questions` | string[] | Yes | 2-3 questions that reliably surface this misconception. E.g. `["Where does a plant get its food from?", "If you put a plant in very good soil but no light, would it grow well? Why?"]`. These are the highest-leverage questions an AI tutor can ask. |
| `persistence` | string | Yes | Controlled vocabulary: `transient` (typically resolved within the unit), `persistent` (often survives to the next key stage), `lifelong` (commonly held by adults). Based on science education research (PSTT, ECLIPSE, Rosalind Driver's "Making Sense of Secondary Science"). This tells the AI how much emphasis to give to addressing this misconception. |
| `evidence_base` | string | No | Source reference for this misconception being common. E.g. "Driver et al., 'Making Sense of Secondary Science' (1994), Chapter 7". Optional because not all misconceptions have published research, but many do. |
| `science_discipline` | string | Yes | `general_science`, `biology`, `chemistry`, `physics`. Allows discipline-filtered queries. |
| `key_stages` | string[] | Yes | Which key stages this misconception is relevant to. Many span multiple key stages. E.g. "Plants get food from soil" is relevant at KS2 AND KS3. |
| `display_category` | string | Yes | `"Science Misconception"`. |
| `display_color` | string | Yes | `"#DC2626"` (Red-600 -- misconceptions should visually stand out as "things to watch for"). |
| `display_icon` | string | Yes | `"warning"` (Material icon). |

### 2.3 `:EnquiryType` Properties

| Property | Type | Required | Rationale |
|---|---|---|---|
| `enquiry_type_id` | string | Yes | Unique identifier. Format: `ET-{NNN}` (e.g. `ET-001`). |
| `name` | string | Yes | Human-readable name using NC terminology. E.g. "Fair Test", "Observation Over Time". |
| `code` | string | Yes | Machine-readable code matching the controlled vocabulary: `fair_test`, `observation_over_time`, `pattern_seeking`, `identifying_and_classifying`, `research`, `modelling`, `secondary_data_analysis`. |
| `description` | string | Yes | What this enquiry type IS, in teacher language. |
| `nc_basis` | string | Yes | Where this enquiry type comes from in the NC. E.g. "NC KS2 statutory: Working Scientifically" or "NC KS3 WS: extended from NGSS practices". |
| `session_structure` | string[] | Yes | The canonical pedagogical phases for this enquiry type. E.g. for `fair_test`: `["question", "hypothesis", "method_design", "data_collection", "analysis", "conclusion"]`. For `identifying_and_classifying`: `["question", "observation", "property_identification", "grouping_criteria", "classification", "key_construction"]`. This is what the VehicleTemplate tried to capture, but it belongs here -- the enquiry type IS the session structure. |
| `key_question_scaffold` | string[] | Yes | The guiding questions for this enquiry type. For `fair_test`: `["What will you change?", "What will you measure?", "What will you keep the same?", "What do you predict will happen?"]`. For `pattern_seeking`: `["Is there a pattern between...?", "What do you notice when...?"]`. The AI uses these as the backbone of its questioning. |
| `agent_prompt` | string | Yes | Default prompt instruction for the AI tutor when running this enquiry type. E.g. "Guide the pupil through a fair test. Ensure they identify the independent, dependent, and controlled variables before collecting data. Challenge them to predict the outcome and explain their prediction using scientific knowledge." |
| `key_stages` | string[] | Yes | Which key stages this enquiry type is used at. E.g. `["KS1", "KS2", "KS3", "KS4"]` for fair test; `["KS2", "KS3", "KS4"]` for modelling. |
| `display_category` | string | Yes | `"Science Enquiry Type"`. |
| `display_color` | string | Yes | `"#7C3AED"` (Violet-600 -- same family as ThinkingLens, since enquiry types serve an analogous "how to think about this" role). |
| `display_icon` | string | Yes | `"category"` (Material icon). |

---

## 3. Relationship Model

```
                                                    (:KeyStage)
                                                        ^
                                                        |
                                                  [:PROMPT_FOR]
                                                  {agent_prompt, question_stems}
                                                        |
(:Domain)--[:HAS_ENQUIRY]-->(:ScienceEnquiry)--[:USES_ENQUIRY_TYPE]-->(:EnquiryType)
                                |        |                                   |
                                |        |                             [:DEVELOPS_SKILL]
                                |        |                                   |
                                |        |                                   v
                                |        |                        (:WorkingScientifically)
                                |        |
                                |        +--[:DELIVERS]-->(:Concept)
                                |        |    {primary: bool}
                                |        |
                                |        +--[:SURFACES_MISCONCEPTION]-->(:Misconception)
                                |        |    {likelihood: str}
                                |        |
                                |        +--[:SUPERSEDES]-->(:ContentVehicle)
                                |             (backward compatibility)
                                |
                                +--[:PROGRESSES_TO]-->(:ScienceEnquiry)
                                     {rationale: str}
```

### 3.1 Relationships FROM `:ScienceEnquiry`

| Relationship | Target | Properties | Cardinality | Rationale |
|---|---|---|---|---|
| `DELIVERS` | `:Concept` | `primary: bool` | Many-to-many | Which curriculum concepts this enquiry teaches. `primary=true` for the main concept; `false` for secondary concepts. Identical semantics to ContentVehicle DELIVERS -- this is the core curriculum alignment link. |
| `USES_ENQUIRY_TYPE` | `:EnquiryType` | `rank: int` | One-to-many (1 primary, 0-2 secondary) | The primary enquiry type (`rank=1`) plus optional secondary types. E.g. Evolution uses `research` (rank 1) + `pattern_seeking` (rank 2). The primary type determines the session structure; secondary types indicate blended approaches. |
| `SURFACES_MISCONCEPTION` | `:Misconception` | `likelihood: string` | Many-to-many | Which misconceptions are likely to surface during this enquiry. `likelihood` is controlled: `high` (almost always surfaces), `moderate` (surfaces if probed), `low` (occasionally surfaces). The AI uses this to decide which misconceptions to proactively address. |
| `PROGRESSES_TO` | `:ScienceEnquiry` | `rationale: string` | Many-to-many | Enquiry progression chains. E.g. "States of Matter" (Y4, observation) PROGRESSES_TO "Particle Model" (KS3, modelling). The rationale explains what conceptual development connects them. This is NOT the same as concept PREREQUISITE_OF -- concept prerequisites are already in the graph. This is about enquiry pedagogy: "you need to have done an observation-based exploration of states before you can build a particle model". |
| `SUPERSEDES` | `:ContentVehicle` | none | One-to-one | Backward compatibility link to the existing ContentVehicle for this enquiry. Allows queries to traverse both the old and new models during migration. Optional -- only present where a CV exists. |

### 3.2 Relationships TO `:ScienceEnquiry`

| Relationship | Source | Properties | Rationale |
|---|---|---|---|
| `HAS_ENQUIRY` | `:Domain` | none | Inferred from the domains of delivered concepts, exactly as HAS_VEHICLE is inferred for ContentVehicles. Every enquiry belongs to one or more curriculum domains. |
| `SUGGESTED_ENQUIRY` | `:ConceptCluster` | `rank: int` | Which ConceptCluster suggests this enquiry for teaching. Replaces `SUGGESTED_TOPIC`. Rank indicates preference order when multiple enquiries cover the same cluster. |

### 3.3 Relationships FROM `:EnquiryType`

| Relationship | Target | Properties | Rationale |
|---|---|---|---|
| `DEVELOPS_SKILL` | `:WorkingScientifically` | `strength: string` | Which Working Scientifically skills this enquiry type inherently develops. `strength` is `core` (the defining skill -- fair test develops "controlling variables") or `supporting` (also developed -- fair test also develops "recording data"). This is structural: ALL fair tests develop variable control. Concept-level DEVELOPS_SKILL links are already in the graph; these are type-level links. |
| `PROMPT_FOR` | `:KeyStage` | `agent_prompt: string, question_stems: string[]` | Age-banded AI prompts for this enquiry type. A KS1 fair test prompt uses concrete, simple language; a KS3 fair test prompt expects statistical analysis. Follows the same pattern as ThinkingLens PROMPT_FOR. |

### 3.4 Relationships BETWEEN `:Misconception` Nodes

| Relationship | Properties | Rationale |
|---|---|---|
| `PREREQUISITE_MISCONCEPTION` | `rationale: string` | Misconception chains. "Particles expand when heated" often leads to "There is air between particles". If the AI does not address the first, the second becomes harder to correct. The rationale explains the dependency. Direction: the prerequisite misconception points to the one it enables. |

### 3.5 Relationship Diagram (ASCII)

```
    (:KeyStage)
       ^ ^
       | |
       | +--- [:PROMPT_FOR {agent_prompt, question_stems}] --- (:EnquiryType)
       |                                                            |
       |                                                      [:DEVELOPS_SKILL]
       |                                                            |
       |                                                            v
       |                                                 (:WorkingScientifically)
       |
  [:HAS_KEY_STAGE]
       |
  (:Curriculum)

                     (:ConceptCluster)
                           |
                  [:SUGGESTED_ENQUIRY {rank}]
                           |
                           v
  (:Domain)---[:HAS_ENQUIRY]--->(:ScienceEnquiry)---[:USES_ENQUIRY_TYPE {rank}]--->(:EnquiryType)
                                     |     |
                                     |     +---[:DELIVERS {primary}]--->(:Concept)
                                     |     |
                                     |     +---[:SURFACES_MISCONCEPTION {likelihood}]--->(:Misconception)
                                     |     |                                                |
                                     |     +---[:PROGRESSES_TO {rationale}]--->(:ScienceEnquiry)  |
                                     |     |                                                |
                                     |     +---[:SUPERSEDES]--->(:ContentVehicle)           |
                                     |                                              [:PREREQUISITE_
                                     |                                               MISCONCEPTION]
                                     |                                                      |
                                     |                                                      v
                                     |                                              (:Misconception)
```

---

## 4. The 7 Enquiry Types (Structural Nodes)

These are seeded as structural data, not generated per enquiry. They are the Science equivalent of ThinkingLens nodes -- stable, cross-curricular, and shared.

| `code` | `name` | NC Basis | Session Structure | Core WS Skill | Key Stages |
|---|---|---|---|---|---|
| `fair_test` | Fair Test | NC KS2 statutory | question -> hypothesis -> method_design -> data_collection -> analysis -> conclusion | WS-KS2-003 (controlling variables) | KS1-KS4 |
| `observation_over_time` | Observation Over Time | NC KS2 statutory | question -> prediction -> observation_schedule -> systematic_recording -> pattern_identification -> conclusion | WS-KS2-002 (systematic observations) | KS1-KS4 |
| `pattern_seeking` | Pattern Seeking | NC KS2 statutory | question -> prediction -> data_gathering -> pattern_identification -> explanation -> evaluation | WS-KS2-004 (classifying/patterns) | KS2-KS4 |
| `identifying_and_classifying` | Identifying and Classifying | NC KS2 statutory | question -> observation -> property_identification -> grouping_criteria -> classification -> key_construction | WS-KS2-004 (classifying) | KS1-KS4 |
| `research` | Research Using Secondary Sources | NC KS2 statutory | question -> source_identification -> information_gathering -> note_taking -> synthesis -> conclusion | WS-KS2-008 (evidence evaluation) | KS1-KS4 |
| `modelling` | Modelling | NC KS3 WS | stimulus -> model_building -> prediction_from_model -> testing_against_reality -> model_refinement -> evaluation | WS-KS3-007 (reasoned explanations) | KS2-KS4 |
| `secondary_data_analysis` | Secondary Data Analysis | NC KS3 WS | question -> dataset_selection -> data_exploration -> pattern_identification -> analysis -> conclusion_with_limitations | WS-KS3-011 (statistical analysis) | KS2-KS4 |

---

## 5. Handling the KS2 to KS3 Transition

The KS2-to-KS3 transition is the hardest structural problem in Science because:

- At KS2, Science is a single subject (`general_science`). One teacher teaches it all.
- At KS3, Science splits into Biology, Chemistry, and Physics. Often three different teachers.
- Many concepts span the transition: "forces" at KS2 becomes "forces and motion" in KS3 Physics; "living things and habitats" at KS2 becomes "ecology" in KS3 Biology.

### How the ontology handles this:

1. **`science_discipline` property on ScienceEnquiry**. KS2 enquiries are tagged `general_science` (or occasionally `biology`/`chemistry`/`physics` when the content clearly maps -- e.g. Rocks is `chemistry`, Evolution is `biology`). KS3 enquiries are always tagged with a specific discipline. This allows the AI to surface "you covered this in KS2 general science; now we are studying it in KS3 Biology" transitions.

2. **`PROGRESSES_TO` relationships across key stages**. "States of Matter" (SE-KS2-006, `general_science`, observation) PROGRESSES_TO "Particle Model and Changes of State" (SE-KS3-005, `chemistry`, observation/modelling). The relationship carries a rationale: "Y4 explores states of matter through observation and classification; KS3 builds the particle model to EXPLAIN those observations. The particle model is the explanatory framework that was missing at KS2."

3. **Concept-level PREREQUISITE_OF already in the graph**. The existing `(:Concept)-[:PREREQUISITE_OF]->(:Concept)` relationships already encode the cross-KS learning progressions (e.g. SC-KS2-C034 "states of matter" is PREREQUISITE_OF SC-KS3-C068 "particle model"). The ScienceEnquiry layer does not duplicate this -- it adds the ENQUIRY progression on top. The concept prerequisite says "you need to know X before Y"; the enquiry progression says "you need to have INVESTIGATED X before you can MODEL Y".

4. **Misconception chains cross the boundary**. "Particles expand when heated" (KS2 misconception from States of Matter) often persists into KS3 Particle Model. Making it a shared `Misconception` node linked to both enquiries means the AI can check whether this was addressed at KS2 before teaching the KS3 content.

---

## 6. Safety Model

Safety in Science is non-negotiable. This is a children's platform. The ontology models safety at three levels:

### Level 1: Triage (`hazard_level` property)

Every `ScienceEnquiry` has a `hazard_level`:

- **`low`**: No specific hazards. Observation, research, classification of safe materials. Generated content includes a brief "low risk" acknowledgement.
- **`standard`**: Normal lab procedures. Goggles, careful handling, hot water (teacher-supervised), glass equipment. Generated content includes specific safety reminders.
- **`elevated`**: CLEAPSS model risk assessment required. Acids, heating chemicals, Bunsen burners, biological material, flammable gases. Generated content includes detailed safety instructions, equipment list with safety equipment, and a warning that teacher/parent supervision is essential.

### Level 2: Specific Instructions (`safety_notes` property)

Every enquiry has a `safety_notes` string with context-specific safety instructions. Not generic "be careful" but specific: "Wear safety goggles and gloves. Use only dilute acids (max 1M). Wash splashes immediately with plenty of water. Know the location of the eyewash station."

### Level 3: AI Generation Rules

The `hazard_level` triggers specific AI behaviour:
- `elevated` enquiries: the AI MUST include safety notes in any generated content (lesson plans, video scripts, parent guides). The `agent_prompt` on the EnquiryType PROMPT_FOR relationship includes safety language.
- Home-learning context: `elevated` enquiries are flagged to parents as requiring adult supervision. Some may be marked as school-only.
- The AI never suggests improvised alternatives to safety equipment ("you could use sunglasses instead of safety goggles").

---

## 7. Example Instances

### 7.1 Fair Test: Friction Investigation (KS2)

```
(:ScienceEnquiry {
  enquiry_id: "SE-KS2-001",
  name: "Friction Investigation",
  enquiry_question: "How does the surface affect how far a toy car travels?",
  science_discipline: "physics",
  key_stage: "KS2",
  year_groups: ["Y5"],
  curriculum_status: "mandatory",
  curriculum_reference: [
    "Y5 Forces: identify the effects of air resistance, water resistance and friction, that act between moving surfaces"
  ],
  equipment: ["ramp", "toy car", "metre stick", "surface samples (carpet, wood, sandpaper, tile, fabric)", "masking tape"],
  safety_notes: "Low risk. Ensure ramp is stable and surfaces are secured flat. Keep floor area clear to prevent tripping.",
  hazard_level: "low",
  expected_outcome: "Rougher surfaces produce more friction, so the car travels a shorter distance. Smooth surfaces produce less friction.",
  recording_format: ["results table", "bar chart", "written conclusion"],
  variables: {
    independent: "surface type (carpet, wood, sandpaper, tile, fabric)",
    dependent: "distance travelled by toy car (cm)",
    controlled: ["ramp angle", "car mass", "release point", "same car"]
  },
  definitions: ["friction", "force", "contact force", "surface", "fair test", "variable", "conclusion"],
  pedagogical_rationale: "This is the most accessible fair test in the KS2 curriculum...",
  common_pitfalls: ["Inconsistent release of the car on the ramp leads to unreliable data..."],
  cross_curricular_hooks: ["[Maths] Measuring in cm, drawing bar charts", "[English] Writing a conclusion using causal connectives"],
  display_category: "Science Enquiry",
  display_color: "#059669",
  display_icon: "science"
})

-- relationships -->
-[:USES_ENQUIRY_TYPE {rank: 1}]-> (:EnquiryType {code: "fair_test"})
-[:DELIVERS {primary: true}]-> (:Concept {concept_id: "SC-KS2-C025"})   // friction
-[:DELIVERS {primary: false}]-> (:Concept {concept_id: "SC-KS2-C027"})  // friction investigation
-[:SURFACES_MISCONCEPTION {likelihood: "high"}]-> (:Misconception {misconception_id: "MC-021", pupil_statement: "Smooth surfaces have no friction"})
-[:SURFACES_MISCONCEPTION {likelihood: "moderate"}]-> (:Misconception {misconception_id: "MC-022", pupil_statement: "Friction is always unhelpful"})
-[:PROGRESSES_TO {rationale: "KS3 forces extends friction to quantitative measurement with Newton meters"}]-> (:ScienceEnquiry {enquiry_id: "SE-KS3-003"})
```

### 7.2 Modelling Enquiry: Particle Model (KS3)

```
(:ScienceEnquiry {
  enquiry_id: "SE-KS3-005",
  name: "Particle Model and Changes of State",
  enquiry_question: "How can we use the particle model to explain the properties of solids, liquids, and gases?",
  science_discipline: "chemistry",
  key_stage: "KS3",
  year_groups: ["Y7", "Y8"],
  curriculum_status: "mandatory",
  curriculum_reference: [
    "KS3 Chemistry: the properties of the different states of matter in terms of the particle model",
    "KS3 Chemistry: changes of state in terms of the particle model"
  ],
  equipment: ["thermometers", "beakers", "ice", "Bunsen burner or water bath", "stearic acid", "stopwatch", "heatproof mat"],
  safety_notes: "Use water baths rather than direct heating where possible. Stearic acid is hot when melted -- use tongs. Wear safety goggles. Tie back long hair near Bunsen burners. Heatproof mats in place.",
  hazard_level: "elevated",
  expected_outcome: "Temperature stays constant during changes of state. Particles in solids vibrate in fixed positions; in liquids move freely; in gases move rapidly. Energy is needed to change state.",
  recording_format: ["temperature-time data table", "heating/cooling curve graph", "particle diagrams for each state"],
  variables: {
    independent: "time (continuous heating or cooling)",
    dependent: "temperature",
    controlled: ["same substance", "same volume", "same heating rate"]
  },
  definitions: ["particle", "solid", "liquid", "gas", "melting point", "boiling point", "evaporation", "condensation", "sublimation", "energy"],
  pedagogical_rationale: "The heating/cooling curve is pedagogically powerful because it reveals a counter-intuitive result: temperature stays constant during a change of state. This drives deeper questioning about what is happening at the particle level.",
  common_pitfalls: [
    "Pupils draw particles as being larger in a gas -- particles are the same size",
    "Difficulty explaining constant temperature during state change"
  ],
  display_category: "Science Enquiry",
  display_color: "#059669",
  display_icon: "science"
})

-- relationships -->
-[:USES_ENQUIRY_TYPE {rank: 1}]-> (:EnquiryType {code: "observation_over_time"})
-[:USES_ENQUIRY_TYPE {rank: 2}]-> (:EnquiryType {code: "modelling"})
-[:DELIVERS {primary: true}]-> (:Concept {concept_id: "SC-KS3-C068"})
-[:DELIVERS {primary: false}]-> (:Concept {concept_id: "SC-KS3-C069"})
-[:DELIVERS {primary: false}]-> (:Concept {concept_id: "SC-KS3-C070"})
-[:DELIVERS {primary: false}]-> (:Concept {concept_id: "SC-KS3-C071"})
-[:SURFACES_MISCONCEPTION {likelihood: "high"}]-> (:Misconception {
  misconception_id: "MC-045",
  pupil_statement: "Particles expand when heated",
  correct_explanation: "Particles do not change size. They gain kinetic energy and move further apart.",
  diagnostic_questions: [
    "When you heat ice and it melts, what happens to the water particles? Do they get bigger?",
    "Draw what you think happens to the particles when a solid is heated."
  ],
  persistence: "persistent"
})
-[:SURFACES_MISCONCEPTION {likelihood: "moderate"}]-> (:Misconception {
  misconception_id: "MC-046",
  pupil_statement: "There are no particles in a gas because you cannot see it"
})
```

### 7.3 Research Enquiry: Evolution and Adaptation (KS2)

```
(:ScienceEnquiry {
  enquiry_id: "SE-KS2-009",
  name: "Evolution and Adaptation",
  enquiry_question: "How have living things changed over time, and how are they adapted to their environments?",
  science_discipline: "biology",
  key_stage: "KS2",
  year_groups: ["Y6"],
  curriculum_status: "mandatory",
  curriculum_reference: [
    "Y6 Evolution and inheritance: recognise that living things have changed over time",
    "Y6 Evolution and inheritance: identify how animals and plants are adapted to suit their environment"
  ],
  equipment: ["fossil samples or images", "bird beak models (tweezers, pegs, chopsticks)", "seeds of different sizes", "images of adapted organisms"],
  safety_notes: "No specific physical hazards. Handle fossil samples with care. Ensure sensitivity around evolution/creation discussions -- follow school RE policy.",
  hazard_level: "low",
  expected_outcome: "Fossils show how organisms changed over time. Offspring vary. Organisms are adapted. Natural selection means better-adapted organisms survive and reproduce.",
  recording_format: ["timeline of life on Earth", "beak adaptation results table", "explanation text"],
  definitions: ["fossil", "evolution", "adaptation", "variation", "natural selection", "inherited", "species", "extinct"],
  pedagogical_rationale: "The bird beak simulation transforms natural selection from an abstract concept into a physical investigation where pupils experience variation, competition, and differential survival first-hand.",
  common_pitfalls: [
    "Pupils think individual organisms evolve during their lifetime",
    "Confusing adaptation with acclimatisation"
  ],
  sensitive_content_notes: [
    "Evolution can conflict with some religious beliefs -- present as scientific explanation supported by evidence, while being respectful of faith backgrounds"
  ],
  display_category: "Science Enquiry",
  display_color: "#059669",
  display_icon: "science"
})

-- relationships -->
-[:USES_ENQUIRY_TYPE {rank: 1}]-> (:EnquiryType {code: "research"})
-[:USES_ENQUIRY_TYPE {rank: 2}]-> (:EnquiryType {code: "pattern_seeking"})
-[:DELIVERS {primary: true}]-> (:Concept {concept_id: "SC-KS2-C063"})
-[:DELIVERS {primary: false}]-> (:Concept {concept_id: "SC-KS2-C064"})
-[:DELIVERS {primary: false}]-> (:Concept {concept_id: "SC-KS2-C065"})
-[:DELIVERS {primary: false}]-> (:Concept {concept_id: "SC-KS2-C066"})
-[:SURFACES_MISCONCEPTION {likelihood: "high"}]-> (:Misconception {
  misconception_id: "MC-031",
  pupil_statement: "Evolution means an animal chose to change",
  persistence: "persistent"
})
-[:SURFACES_MISCONCEPTION {likelihood: "high"}]-> (:Misconception {
  misconception_id: "MC-032",
  pupil_statement: "Humans evolved from modern monkeys",
  persistence: "lifelong"
})
```

### 7.4 Pattern Seeking: Chemical Reactions -- Metals and Acids (KS3)

```
(:ScienceEnquiry {
  enquiry_id: "SE-KS3-008",
  name: "Chemical Reactions: Metals and Acids",
  enquiry_question: "How can we use the reactions of metals with acids to put them in order of reactivity?",
  science_discipline: "chemistry",
  key_stage: "KS3",
  year_groups: ["Y8", "Y9"],
  curriculum_status: "mandatory",
  curriculum_reference: [
    "KS3 Chemistry: the order of metals and carbon in the reactivity series",
    "KS3 Chemistry: reactions of acids with metals to produce a salt plus hydrogen"
  ],
  equipment: ["dilute hydrochloric acid (1M)", "metal samples (Mg, Zn, Fe, Cu)", "test tubes", "test tube rack", "splints", "safety goggles", "gloves", "thermometer"],
  safety_notes: "Wear safety goggles and gloves throughout. Magnesium reacts vigorously -- use small pieces only (1-2cm ribbon). Test for hydrogen with a lighted splint held away from the acid. Good ventilation required. Dilute acid only (max 1M HCl). Dispose of waste according to school policy.",
  hazard_level: "elevated",
  expected_outcome: "Metals react with acids to produce a salt and hydrogen. More reactive metals react more vigorously. Reactivity series: Mg > Zn > Fe > Cu.",
  recording_format: ["observations table (metal, observations, temperature change)", "reactivity series ranking", "word equations"],
  variables: {
    independent: "type of metal (magnesium, zinc, iron, copper)",
    dependent: "vigour of reaction (fizzing, temperature change, gas production)",
    controlled: ["same volume and concentration of acid", "same size of metal piece"]
  },
  definitions: ["reactivity", "reactivity series", "displacement", "salt", "hydrogen", "acid", "oxidation", "corrosion"],
  pedagogical_rationale: "Building the reactivity series from first-hand observations develops genuine scientific reasoning. The gradient from vigorous (Mg) to no reaction (Cu) is dramatic and demands explanation.",
  common_pitfalls: [
    "Pupils memorise the reactivity series without understanding what it means",
    "Difficulty writing word equations -- practise the pattern: metal + acid -> metal salt + hydrogen"
  ],
  display_category: "Science Enquiry",
  display_color: "#059669",
  display_icon: "science"
})

-- relationships -->
-[:USES_ENQUIRY_TYPE {rank: 1}]-> (:EnquiryType {code: "pattern_seeking"})
-[:DELIVERS {primary: true}]-> (:Concept {concept_id: "SC-KS3-C086"})
-[:DELIVERS {primary: false}]-> (:Concept {concept_id: "SC-KS3-C094"})
-[:DELIVERS {primary: false}]-> (:Concept {concept_id: "SC-KS3-C097"})
-[:SURFACES_MISCONCEPTION {likelihood: "high"}]-> (:Misconception {
  misconception_id: "MC-061",
  pupil_statement: "All metals react with acids",
  correct_explanation: "Some metals like copper and gold are too unreactive to react with dilute acids.",
  diagnostic_questions: [
    "If you put a gold ring in acid, would it dissolve? Why or why not?",
    "What would you observe if you put copper in dilute hydrochloric acid?"
  ],
  persistence: "transient"
})
-[:SURFACES_MISCONCEPTION {likelihood: "moderate"}]-> (:Misconception {
  misconception_id: "MC-062",
  pupil_statement: "The bubbles in the reaction are air",
  persistence: "transient"
})
```

---

## 8. What This Enables That the Universal Model Could Not

### 8.1 Misconception-Aware Tutoring

**Universal model**: `misconceptions: string[]` on ScienceTopicSuggestion. The AI reads a list of strings. It cannot track whether a child has met this misconception before, whether it was addressed, or whether it connects to other misconceptions.

**This ontology**: The AI queries:
```cypher
MATCH (se:ScienceEnquiry {enquiry_id: $current_enquiry})-[:SURFACES_MISCONCEPTION]->(m:Misconception)
OPTIONAL MATCH (m)<-[:SURFACES_MISCONCEPTION]-(prev:ScienceEnquiry)-[:DELIVERS]->(c:Concept)
WHERE c.concept_id IN $previously_taught_concepts
RETURN m, prev, m.diagnostic_questions, m.persistence
```
This tells the AI: "This misconception might surface. The child may have encountered it before in [previous enquiry]. Here are diagnostic questions to check. Its persistence rating is [lifelong/persistent/transient]."

### 8.2 Enquiry Type Progression

**Universal model**: `enquiry_type: string` as a property. No progression, no structure.

**This ontology**: The AI queries:
```cypher
MATCH (et:EnquiryType {code: "fair_test"})-[:PROMPT_FOR]->(ks:KeyStage {key_stage_id: "KS2"})
RETURN et.session_structure, et.key_question_scaffold, pf.agent_prompt
```
The AI receives the complete pedagogical structure for a KS2 fair test: the session phases, the guiding questions, and an age-appropriate agent prompt. At KS3, the same query returns a more sophisticated structure with statistical analysis expectations.

### 8.3 Safety-Driven Content Generation

**Universal model**: `safety_notes: string`, `hazard_level: string` as properties. The AI reads them. That is all.

**This ontology**: The `hazard_level` triggers AI behaviour rules. The `EnquiryType` PROMPT_FOR relationship includes safety language calibrated to the key stage. The AI can query all elevated-hazard enquiries for a year group:
```cypher
MATCH (se:ScienceEnquiry {hazard_level: "elevated"})
WHERE "Y8" IN se.year_groups
RETURN se.name, se.safety_notes, se.equipment
```
For home-learning contexts, this query identifies which enquiries need parental supervision warnings.

### 8.4 Cross-KS Enquiry Progression

**Universal model**: No relationships between TopicSuggestions.

**This ontology**: The AI can trace enquiry progressions across key stages:
```cypher
MATCH path = (se1:ScienceEnquiry)-[:PROGRESSES_TO*1..3]->(se2:ScienceEnquiry)
WHERE se1.key_stage = "KS2" AND se2.key_stage = "KS3"
RETURN se1.name, se2.name, [r IN relationships(path) | r.rationale]
```
This enables "bridge" lessons at the KS2-KS3 transition: "Last year you observed that ice melts when heated. This year we are going to build a model to explain WHY."

### 8.5 Working Scientifically Integration

**Universal model**: No link between topic suggestions and Working Scientifically skills.

**This ontology**: The EnquiryType nodes link to WS skills structurally. The AI can determine which WS skills a child has practised:
```cypher
MATCH (se:ScienceEnquiry)-[:USES_ENQUIRY_TYPE]->(et:EnquiryType)-[:DEVELOPS_SKILL]->(ws:WorkingScientifically)
WHERE se.enquiry_id IN $completed_enquiries
RETURN ws.skill_name, count(se) AS times_practised
```
This enables the AI to identify under-practised skills: "This child has done five fair tests but no classification enquiries. Suggest a classification enquiry next."

---

## 9. Migration Path from ContentVehicle

The existing ContentVehicle data for Science (10 KS2 + 8 KS3 vehicles) and the migrated TopicSuggestion data (10 KS2 + 8 KS3 suggestions) should be migrated to ScienceEnquiry nodes. The migration is straightforward because:

1. Every existing ContentVehicle maps 1:1 to a ScienceEnquiry.
2. The ScienceEnquiry carries all ContentVehicle properties plus additional ones (misconceptions, hazard_level, enquiry_question, etc.).
3. The `SUPERSEDES` relationship preserves backward compatibility.
4. The `DELIVERS` relationship semantics are identical.

New properties that need to be authored for the migration:
- `enquiry_question` (new -- can be derived from the enquiry name + concept)
- `misconceptions` (partially new -- some exist in TopicSuggestion data, need Misconception node authoring)
- `hazard_level` (exists in TopicSuggestion data, needs migration)

The Misconception nodes require dedicated authoring. I estimate approximately 60-80 unique misconceptions across KS2-KS3 Science, based on the PSTT misconception database, Driver et al., and the existing data in the TopicSuggestion JSONs. Many are well-documented in the science education literature.

---

## 10. Open Questions

### 10.1 Should `:EnquiryType` replace VehicleTemplates for Science?

The FINAL-SCHEMA defines VehicleTemplates (fair_test, observation_over_time, etc.) that overlap almost exactly with EnquiryType nodes. For Science, the enquiry type IS the template -- there is no meaningful distinction between "the type of enquiry" and "the session structure for that type of enquiry". I propose that for Science, `EnquiryType` nodes replace VehicleTemplates entirely, and the `PROMPT_FOR` relationship on EnquiryType serves the same role as `TEMPLATE_FOR` on VehicleTemplate. Other subjects can keep VehicleTemplates where they make sense (History's `source_enquiry` vs `topic_study` is a genuine template distinction, not an enquiry type distinction).

**My recommendation**: Yes, replace. The EnquiryType node carries everything VehicleTemplate carried (session_structure, agent_prompt, assessment_approach via PROMPT_FOR) plus the WS skill links that VehicleTemplate lacked. Keeping both creates confusion about which one the AI should query.

### 10.2 How granular should Misconception nodes be?

"Plants get food from soil" and "Plants only need water and sunlight to grow" are related but distinct misconceptions. Should they be separate nodes (more precise) or merged into a single "photosynthesis misconceptions" cluster (simpler graph)? I lean towards separate nodes with `PREREQUISITE_MISCONCEPTION` relationships between them, because the diagnostic questions and correct explanations are different. But this increases the node count significantly.

### 10.3 Should `variables` be a nested object or flattened?

The existing ContentVehicles store variables as three flat properties (`variables_independent`, `variables_dependent`, `variables_controlled`). The TopicSuggestion data stores them as a nested object `{ independent, dependent, controlled }`. Neo4j supports nested maps only as node properties (not as relationship properties). I propose keeping the nested object format for clarity, but this means the import script must handle serialisation. The flat format is safer for Neo4j compatibility but less readable.

**My recommendation**: Store as a nested object in the JSON data files; flatten to three properties on import (`variables_independent`, `variables_dependent`, `variables_controlled`) for Neo4j compatibility. The query helper recombines them for the AI prompt.

### 10.4 Should EnquiryType nodes have PRECEDES chains?

Similar to how InteractionType nodes form a PRECEDES chain (the "interface curriculum"), EnquiryType nodes could form a progression: `identifying_and_classifying` PRECEDES `pattern_seeking` PRECEDES `fair_test` PRECEDES `modelling`. This reflects the pedagogical reality: children learn to classify before they can seek patterns, and they can seek patterns before they can design fair tests. However, this is a simplification -- all enquiry types are used at all key stages, just with increasing sophistication. I am not sure the PRECEDES chain adds value beyond the age-banded PROMPT_FOR relationships.

**My recommendation**: Do not add PRECEDES chains between EnquiryType nodes. The sophistication progression is better captured by the age-banded PROMPT_FOR prompts (which already distinguish KS1/KS2/KS3 expectations for each enquiry type). A PRECEDES chain implies a linear ordering that does not reflect classroom reality.

### 10.5 PE KS3-KS4 Science practicals

55 PE KS3-KS4 concepts are excluded from DifficultyLevels because they need a sport-specific assessment framework. Similarly, some PE-adjacent Science content (human body, exercise physiology) blurs the boundary between Science and PE. These enquiries should be tagged `biology` but may need a `cross_subject_link` to PE concepts. This is a data authoring question, not an ontology question.
