# Senior Curriculum Leader Review: Cross-Subject Schema Arbitration

**Reviewer**: Senior Curriculum Leader (cross-curricular, whole-school perspective)
**Date**: 2026-02-24
**Inputs reviewed**: All 6 specialist reviews (History, Geography, Science, English, Maths, Foundation), BRIEFING.md, SPECIALIST-SUMMARY.md, CLAUDE.md (graph model)

---

## 1. Final Label Count Recommendation

### Verdict: 9 labels (8 typed + 1 generic)

| Label | Subjects Covered | Rationale |
|---|---|---|
| `HistoryTopicSuggestion` | History | Period + sources + disciplinary concepts = unique structure |
| `GeographyTopicSuggestion` | Geography | Location + scale + maps = unique structure |
| `ScienceTopicSuggestion` | Science, Biology, Chemistry, Physics | Enquiry type + safety + equipment = unique structure |
| `EnglishTopicSuggestion` | English, English Language, English Literature | Genre + text + writing outcome = unique structure |
| `MathsTopicSuggestion` | Mathematics | CPA + manipulatives + representations = unique structure |
| `ArtTopicSuggestion` | Art & Design | Artist + medium + technique = unique structure |
| `MusicTopicSuggestion` | Music | Piece + activity focus + musical elements = unique structure |
| `DTTopicSuggestion` | Design & Technology | Design brief + strand + materials = unique structure |
| `TopicSuggestion` | Computing, RS, Citizenship, Drama, PE, Business, Food, Media Studies | Extended optional properties on generic label |

### Rationale

**Why 9, not 6?** The foundation teacher's case is compelling: Art topics are artist+medium+technique triples, Music topics are piece+activity+element triples, DT topics are design_brief+strand+material triples. None of these can be expressed as `themes: [string]`. Without typed labels, the AI tutor receives `themes: ["Mondrian"]` and has no idea whether to generate a painting lesson, a printing lesson, or an art history discussion. The NC Art curriculum explicitly requires teaching specific media, techniques, and formal elements — these are structural properties, not optional enrichment.

**Why not 17 (one per subject)?** The remaining foundation subjects (Computing, RS, Citizenship, Drama, PE, Business, Food, Media Studies) do not have sufficiently distinct topic structures to justify dedicated labels. Their variability is captured by 2-3 optional properties on the generic label (e.g. `religion` for RS, `computational_concept` for Computing). If any of these grows beyond ~30 TopicSuggestion nodes, reassess.

**Query concern resolved.** "Find all topic suggestions" does NOT require a 9-way UNION. All nodes share `display_category: "Topic Suggestion"`, so `MATCH (n) WHERE n.display_category = 'Topic Suggestion'` returns everything. Typed labels are for subject-specific queries only. This matches the existing graph convention.

**Property count impact.** This adds ~25 total properties across 3 new labels. The graph already manages 10+ node types per layer with comparable property counts. The complexity is bounded and justified by the content generation quality gain for subjects covering ~40% of curriculum time.

---

## 2. Consolidated VehicleTemplate List

### Final count: 24 templates (14 retained/renamed + 10 new)

#### Retained from original 14 (some renamed)

| # | template_type | Subjects | Change |
|---|---|---|---|
| 1 | `topic_study` | History, Geography, RS, Citizenship | No change |
| 2 | `case_study` | Geography, Business, Science | MODIFY: add `locate_and_describe` phase for Geography |
| 3 | `fair_test` | Science | No change |
| 4 | `observation_over_time` | Science, Art | RENAME from `observation_enquiry` to match NC terminology |
| 5 | `pattern_seeking` | Science, Maths, Geography | No change |
| 6 | `research_enquiry` | Science, History, RS | No change |
| 7 | `text_study` | English (KS1-KS3) | CLARIFY: this is the "reading into writing" model |
| 8 | `worked_example_set` | Maths | MODIFY: extend session structure with prior knowledge activation and reasoning extension |
| 9 | `open_investigation` | Science, Geography | RENAME from `investigation_design`; emphasise pupil method autonomy |
| 10 | `fieldwork` | Geography, Science | No change |
| 11 | `discussion_and_debate` | English, RS, Citizenship, History | No change |
| 12 | `creative_response` | Art, English | CLARIFY: primarily for visual art and creative writing |
| 13 | `practical_application` | Maths, DT, Computing, Food | No change |
| 14 | `comparison_study` | Geography, History, RS | No change |

#### New additions (10)

| # | template_type | Subjects | Session Structure | Justification |
|---|---|---|---|---|
| 15 | `source_enquiry` | History | source_presentation -> observation -> questioning -> contextualisation -> inference -> evaluation | History's signature activity. Analysing Bayeux Tapestry, Vindolanda tablets, propaganda posters. Distinct from `research_enquiry` because the source itself is the focus, not a question answered by sources. |
| 16 | `modelling_enquiry` | Science, Geography | stimulus -> model_building -> prediction_from_model -> testing_against_reality -> model_refinement -> evaluation | Core KS3 enquiry type. Particle model, food web models, Earth/Sun/Moon. Neither fair_test nor observation captures "build a model, make predictions from it, test against reality." Both Science and Geography specialists independently requested this. |
| 17 | `identifying_and_classifying` | Science | question -> observation -> property_identification -> grouping_criteria -> classification -> key_construction | One of the 5 NC statutory enquiry types with no template. Y3 rocks, Y4 living things, Y6 microorganisms, KS3 biological classification. |
| 18 | `secondary_data_analysis` | Science, Geography, Maths | question -> dataset_selection -> data_exploration -> pattern_identification -> analysis -> conclusion -> limitations | Working with existing datasets (climate records, population data, public health statistics). Distinct from `research_enquiry` (source-based) and `pattern_seeking` (collecting new data). Both Science and Geography specialists independently requested this. |
| 19 | `place_study` | Geography | locate -> describe_physical -> describe_human -> explain_interactions -> compare -> evaluate_change | Geography's most fundamental template, absent from the original list. Building layered understanding of a place through multiple lenses. KS1 locality, KS2 regional, KS3 depth study — this is the backbone of Geography at every key stage. |
| 20 | `performance` | Music, Drama, PE | warm_up -> skill_building -> rehearsal -> performance -> evaluation | Fundamentally different from `creative_response` (which is a making/creating cycle). Performance subjects follow a warm-up -> practise -> perform -> evaluate cycle. Music performing, Drama, PE all use this pattern. |
| 21 | `design_make_evaluate` | DT | explore -> design -> plan -> make -> test -> evaluate -> improve | The mandated DT process, explicitly required by the NC ("design, make, evaluate"). Distinct from `practical_application` (which lacks the design, test, and iterative improvement phases central to DT). |
| 22 | `ethical_enquiry` | RS, Citizenship | stimulus -> identify_issue -> explore_perspectives -> construct_argument -> evaluate_positions -> personal_response | GCSE RS requires structured ethical reasoning, not just discussion. "Evaluate the significance and coherence of different beliefs from both insider and outsider perspectives" — this needs a more rigorous structure than `discussion_and_debate`. |
| 23 | `text_study_literature` | English (KS4) | introduction -> close_reading -> analysis -> contextualisation -> essay_planning -> essay_writing -> peer_review | KS4 Literature is analytical, not "reading into writing." Students write ABOUT texts, not creatively inspired BY them. Closed-book exam means quotation memorisation is part of the process. Conflating this with KS1-3 `text_study` would produce Y10 Macbeth lessons ending with "Now write your own tragedy!" |
| 24 | `writers_workshop` | English | mini_lesson -> independent_writing -> conferencing -> sharing -> revision | The dominant primary writing pedagogy (Calkins/Graves model). Starting point is the child's own writing, not a model text. Covers the 40-50% of English lessons that `text_study` cannot serve. |

#### Rejected proposals (13 of 23)

| Proposed template | Verdict | Reasoning |
|---|---|---|
| `significance_enquiry` (History) | **MERGE** into `topic_study` | The `disciplinary_concepts` property (with `significance` as a value) plus the age-banded `TEMPLATE_FOR` agent_prompt on `topic_study` can generate significance-focused lessons without a dedicated template. |
| `local_history_enquiry` (History) | **MERGE** into `fieldwork` + `place_study` | Local history enquiry = fieldwork (data collection in locality) + place study (layered understanding of a place). Use the existing templates with a History-specific agent_prompt. |
| `decision_making_exercise` (Geography) | **MERGE** into `case_study` | Distinctive but structurally similar to case_study with a decision/justification phase. Handle via age-banded agent_prompt variant: "This case study requires a stakeholder analysis and justified decision." Revisit if Geography specialists find this insufficient after testing. |
| `mystery` (Geography) | **REJECT** — too niche | A valid Geography teaching strategy but better handled as a task type within `open_investigation` rather than a standalone template. |
| `fluency_practice` (Maths) | **REJECT** — session type, not template | Fluency practice is a session *phase* that appears within `worked_example_set` and `practical_application`, not a standalone lesson structure. Use `nc_aim_emphasis: "fluency"` on the TopicSuggestion to signal fluency-focused sessions. |
| `reasoning_task` (Maths) | **REJECT** — session type, not template | Same reasoning. Use `nc_aim_emphasis: "reasoning"` + `reasoning_prompts` property to signal reasoning-focused sessions. The `pattern_seeking` template already covers investigation-style reasoning. |
| `problem_solving_task` (Maths) | **REJECT** — covered by existing | Multi-step problems fit `practical_application` (context -> skill -> solve -> evaluate) or `open_investigation`. |
| `mathematical_investigation` (Maths) | **MERGE** into `pattern_seeking` | The session structure (explore -> find patterns -> conjecture -> test) maps directly onto `pattern_seeking`. |
| `pre_teaching_diagnostic` (Maths) | **REJECT** — assessment mode, not template | This is a diagnostic assessment, not a lesson template. Better handled by an `assessment_mode` property on the TopicSuggestion. |
| `grammar_in_context` (English) | **REJECT** — pedagogical principle | "Grammar in context" is a delivery principle that applies within `text_study` and `writers_workshop`, not a standalone session structure. |
| `reading_for_pleasure` (English) | **REJECT** — classroom culture, not template | Reading for pleasure is a reading culture practice, not a structured lesson template. |
| `spoken_language_performance` (English) | **MERGE** into `performance` | Performance template (#20) already covers this. English spoken language performance uses the same warm_up -> skill_building -> rehearsal -> performance -> evaluation structure. |
| `unseen_analysis` (English) | **MERGE** into `text_study_literature` | Unseen analysis is a variant of literary analytical study. Handle via `assessment_mode: "exam_practice"` on the TopicSuggestion + age-banded agent_prompt. |

### Notes for Maths specialists

I recognise the Maths concern that `fluency_practice` and `reasoning_task` represent genuinely different lesson types. My reasoning for rejection is not that these differences don't exist — they do — but that they are better captured by properties on the TopicSuggestion (`nc_aim_emphasis`, `reasoning_prompts`, `fluency_targets`) than by dedicated VehicleTemplates. The VehicleTemplate defines the *session structure*; the TopicSuggestion defines the *pedagogical intent*. A fluency-focused `worked_example_set` with `nc_aim_emphasis: "fluency"` is structurally valid. If testing reveals that generated content quality drops because the AI conflates fluency drills with conceptual worked examples, revisit this decision and promote `fluency_practice` to a dedicated template.

---

## 3. Required vs Optional Arbitration

### Principle

**Required means: if this property is empty, the AI tutor cannot generate a safe, pedagogically sound lesson for this subject.** Required does NOT mean "nice to have for data quality." It means "absence causes generation failure."

This platform serves children aged 5-14. Safety properties are non-negotiable. Pedagogically critical properties are required. Everything else is recommended-but-optional with validation warnings.

### Universal required properties (all 9 labels)

| Property | Type | Required | Notes |
|---|---|---|---|
| `suggestion_id` | string | Yes | Unique identifier |
| `name` | string | Yes | Display name |
| `suggestion_type` | string | Yes | Controlled enum (see Section 4) |
| `subject` | string | Yes | Subject name |
| `key_stage` | string | Yes | KS1/KS2/KS3/KS4/EYFS |
| `curriculum_status` | string | Yes | mandatory/menu_choice/exemplar/convention |
| `pedagogical_rationale` | string | Yes | WHY this topic/approach works. Brief (1-3 sentences) is acceptable. |
| `definitions` | string[] | Yes | Key vocabulary the AI must scaffold |
| `display_category` | string | Yes | `"Topic Suggestion"` |
| `display_color` | string | Yes | `#059669` |
| `display_icon` | string | Yes | `lightbulb` |

### Universal optional properties (all 9 labels)

| Property | Type | Required | Notes |
|---|---|---|---|
| `choice_group` | string | No | For menu items: grouping label |
| `curriculum_reference` | string[] | No | NC text references (changed to array per specialist consensus) |
| `common_pitfalls` | string[] | No | What goes wrong teaching this |
| `cross_curricular_hooks` | object[] | No | Structured: `{subject, hook, strength}`. Changed from string[] per 5/6 consensus |
| `sensitive_content_notes` | string[] | No | Safeguarding guidance. Promoted to universal per History + Science consensus |
| `year_groups` | string[] | No | Useful for foundation subjects where NC gives KS-level but practice is year-specific |
| `duration_lessons` | int | No | Typical lesson count. Useful for planning but varies by school |

### Per-label required properties

| Label | Required subject-specific | Count |
|---|---|---|
| **HistoryTopicSuggestion** | `period`, `source_types`, `perspectives`, `disciplinary_concepts`, `significance_claim` | 5 |
| **GeographyTopicSuggestion** | `locations`, `theme_category`, `themes`, `scale`, `map_types`, `data_sources` | 6 |
| **ScienceTopicSuggestion** | `enquiry_type`, `science_discipline`, `equipment`, `safety_notes`, `hazard_level`, `expected_outcome`, `misconceptions` | 7 |
| **EnglishTopicSuggestion** | `text_type`, `genre`, `text_features`, `writing_outcome`, `reading_level` | 5 |
| **MathsTopicSuggestion** | `cpa_stage`, `manipulatives`, `representations`, `fluency_targets`, `nc_aim_emphasis` | 5 |
| **ArtTopicSuggestion** | `medium`, `techniques` | 2 |
| **MusicTopicSuggestion** | `musical_elements`, `activity_focus` | 2 |
| **DTTopicSuggestion** | `dt_strand`, `design_brief`, `materials`, `techniques` | 4 |
| **TopicSuggestion** (generic) | `themes` | 1 |

**Total required per node: 11 universal + 1-7 subject-specific = 12-18 properties.** This is manageable and comparable to existing graph nodes (ConceptCluster has ~15 properties, DifficultyLevel has ~8).

### Arbitration notes

**Science has the highest required count (7).** This is justified because:
- `safety_notes` and `hazard_level` are child safeguarding requirements, not data quality preferences
- `misconceptions` is the single highest-leverage AI generation property in Science (PSTT research consensus)
- `equipment` prevents the AI suggesting resources schools don't have
- The Science teacher's case that all 7 are "minimum viable for safe, effective lesson generation" is accepted

**English `grammar_focus` is deliberately NOT in the required set.** The specialist wants it required for KS1-3 and optional for KS4. Schema constraints cannot express "required at some key stages." Solution: make it optional with a validation rule that warns when empty for KS1-3 EnglishTopicSuggestions. Same pattern for Science `variables` (required for fair_test only) and History `interpretations` (required for KS3 only).

**Science `recording_format` is deliberately NOT in the required set.** The specialist makes a strong case but 8 required properties is excessive. Make it recommended-optional with a validation warning when empty.

---

## 4. Universal Property Changes

### ACCEPTED

| Change | Proposed by | Verdict | Rationale |
|---|---|---|---|
| `curriculum_reference`: string -> string[] | Foundation, History | **ACCEPT** | DT projects reference multiple NC statements; English references span multiple appendices. Array is more flexible with no downside. |
| `cross_curricular_hooks`: string[] -> object[] | History, 5/6 consensus | **ACCEPT** | Structure: `{subject: string, hook: string, strength: "strong"/"moderate"/"light"}`. The `strength` field lets the AI prioritise substantial cross-curricular links over tenuous ones. "Greek democracy and Citizenship" is a strong link; "Roman numerals" is light. |
| `sensitive_content_notes`: ADD as universal optional | History, Science | **ACCEPT** | Multiple subjects need this: History (Holocaust, slavery, empire), Science (evolution sensitivity, hazardous materials), RS (religious persecution), DT (tool safety). Making it universal avoids duplicating the concept per label. |
| `year_groups`: ADD as universal optional | Foundation | **ACCEPT** | Valuable for foundation subjects where NC gives KS-level guidance but school practice is year-specific (Art, Music). Also useful for History/Geography where KS2 topics are typically taught in specific years by convention. |
| `duration_lessons`: ADD as universal optional | Foundation | **ACCEPT** | DT projects run 4-6 lessons, Art 4-6, History 6-12. This varies by school so cannot be required, but it's useful planning metadata. |

### REJECTED

| Change | Proposed by | Verdict | Rationale |
|---|---|---|---|
| `pedagogical_rationale` -> optional | (Implicit in "hard to write for 200+ suggestions") | **REJECT** | This is the single most important property for AI generation quality. Without it, the AI has no "why" — it generates generic lessons. Brief rationales (1-3 sentences) are acceptable. "This topic works for these concepts because..." is not onerous. |
| `suggestion_type` expansion to 15+ values | Multiple specialists | **PARTIALLY ACCEPT** | Each specialist proposed subject-specific values. The expanded enum should be: `prescribed_topic`, `exemplar_topic`, `open_slot`, `exemplar_figure`, `exemplar_event`, `exemplar_text`, `set_text` (English KS4), `genre_requirement` (English), `teacher_convention`. That's 9 values — manageable. Rejected: `paired_figure_study` (use `comparison_pairs` property on exemplar_figure), `enquiry_topic` (use enquiry_type property on prescribed_topic), `place_study` (use suggestion_type=prescribed_topic with theme_category=integrated), `prescribed_domain`/`representation_choice`/`context_choice` (Maths-specific semantics captured by properties, not suggestion_type). |
| `common_pitfalls` rename to `teaching_pitfalls` | Maths | **REJECT** | The current name is clear enough. Teaching pitfalls vs student errors is a valid distinction, but renaming creates inconsistency with the existing ContentVehicle data pattern. Document in schema notes that `common_pitfalls` refers to teacher delivery errors, while student errors live in DifficultyLevel `common_errors`. |

### `suggestion_type` final controlled vocabulary

```
prescribed_topic     — NC explicitly names this content as mandatory
exemplar_topic       — NC names this as one option among several
open_slot            — NC requires a study but school picks the specific content
exemplar_figure      — NC names this person as an example
exemplar_event       — NC names this event as an example
exemplar_text        — NC names this text/genre as an example
set_text             — Exam board set text (KS4 only)
genre_requirement    — NC requires this genre/text type but not a specific text
teacher_convention   — Most schools teach this even though NC doesn't mandate it
```

---

## 5. Naming Convention Guidelines

### The problem

Six specialists have proposed ~60 new properties with no coordination on naming. The same concept appears under different names:

| Concept | History | Science | Geography | English | Art | Music |
|---|---|---|---|---|---|---|
| "What kind of subject thinking?" | `disciplinary_concepts` | — | — | — | — | — |
| "Which branch/strand?" | — | `science_discipline` | `theme_category` | `text_type` | — | — |
| "Which formal elements?" | — | — | — | — | `visual_elements` | `musical_elements` |
| "Which NC aim?" | — | — | — | — | — | — |

### Are these the same concept?

**No.** On careful analysis, these properties answer genuinely different questions:

1. **Disciplinary thinking** (what cognitive skills does this develop?): History's `disciplinary_concepts` is unique — no other subject has a direct equivalent. Closest: Maths' `nc_aim_emphasis` (fluency/reasoning/problem-solving) and Science's `enquiry_type` (fair_test/observation/etc.), but these are operationally distinct.

2. **Organisational classifier** (which sub-domain/branch?): Science's `science_discipline`, Geography's `theme_category`, English's `text_type`, DT's `dt_strand`. These all answer "what kind of [subject] is this?" but with subject-specific vocabularies. Forcing a universal `subject_strand` would lose semantic precision.

3. **Formal elements** (which disciplinary elements are the focus?): Art's `visual_elements`, Music's `musical_elements`. Both are arrays of NC-defined formal dimensions. These COULD be merged into a universal `formal_elements` — but the controlled vocabularies are entirely different (colour/line/shape vs pulse/rhythm/pitch) and merging them would reduce type safety.

### Recommendation: Don't force a universal property. Document naming patterns.

Each subject's properties should use the **NC's own terminology** for that subject. The NC calls them "second-order concepts" in History, "enquiry types" in Science, "inter-related dimensions" in Music, "visual elements" in Art. Renaming these to a universal abstraction would confuse teachers and diverge from the source framework.

### Naming conventions to enforce

| Convention | Rule | Examples |
|---|---|---|
| **Plurals for arrays** | If the property is `string[]`, the name should be plural | `locations` (not `location`), `techniques` (not `technique`) |
| **Controlled vocabulary documentation** | Every property with a controlled vocabulary must have its valid values listed in the schema docs | `enquiry_type`: fair_test, observation_over_time, ... |
| **No abbreviations in property names** | Write out fully | `disciplinary_concepts` (not `disc_concepts`) |
| **Snake_case consistently** | Match existing graph convention | `theme_category`, `source_types`, `nc_aim_emphasis` |
| **Subject prefix only when ambiguous** | Only prefix with subject name if the property could collide | `science_discipline` (could collide with History disciplinary concepts), but `medium` not `art_medium` (unambiguous on ArtTopicSuggestion) |
| **No property name collisions across labels** | Each typed label's properties must be unique names | `themes` can appear on multiple labels because it means the same thing everywhere; `discipline` cannot because it means different things |

### Cross-label property reuse

These property names appear on multiple labels with the same semantics — this is intentional and should be preserved:

| Property | Labels | Meaning |
|---|---|---|
| `themes` | Geography, Art, Music, DT, generic | Thematic concepts (free text, curated) |
| `techniques` | Art, DT | Making/doing techniques |
| `safety_notes` | Science, DT | Safety guidance for practical work |

---

## 6. Scalability Assessment

### KS4 GCSE (immediate next expansion)

**Verdict: Schema scales well.**

- **English KS4**: `exam_board_status` property handles set texts cleanly. `text_study_literature` template is purpose-built for analytical study. `set_text` suggestion_type captures the board-mandated nature.
- **Science KS4**: `science_discipline` (biology/chemistry/physics) already handles the split. Equipment, safety, and misconceptions remain equally critical at GCSE. No schema changes needed.
- **Maths KS4**: CPA model still applies (algebra tiles are concrete). `representations` vocabulary extends to `unit_circle`, `cumulative_frequency`, etc. No schema changes needed.
- **History KS4**: Same properties work. `interpretations` becomes more prominent. No schema changes needed.
- **Geography KS4**: Same properties work. Data sources become more formal. No schema changes needed.
- **Foundation KS4**: Music, Art, DT at GCSE use the same typed labels with richer content. Computing at GCSE stays under generic with `programming_paradigm: "text_based"`. Drama at GCSE uses generic + `performance_style`/`practitioner` properties.

### A-Level (future expansion)

**Verdict: Schema scales with minor additions.**

- A-Level subjects are deeper specialisations, not structurally different. A-Level Chemistry TopicSuggestion uses the same `ScienceTopicSuggestion` label with `science_discipline: "chemistry"` and more advanced content.
- **New subjects**: Psychology, Sociology, Economics, Government & Politics — all fit generic `TopicSuggestion` with `themes`.
- **Potential issue**: A-Level Further Maths has a split into Pure/Applied/Statistics/Mechanics that the current `nc_aim_emphasis` property doesn't capture. Add a `maths_strand` property if needed.
- **No new labels needed.** The 9-label model covers A-Level without structural changes.

### Vocational qualifications (BTEC, T-Levels)

**Verdict: Schema needs extension but doesn't break.**

- Vocational qualifications are organised by **units** and **learning outcomes**, not topics and concepts. The TopicSuggestion concept extends if we add a `qualification_framework: "BTEC"/"T-Level"` property to distinguish vocational from academic suggestions.
- VehicleTemplates remain valid: vocational courses use investigations, case studies, practical applications, and projects — all covered by existing templates.
- **Risk area**: Vocational assessment is often portfolio-based, not exam-based. The `assessment_mode` property would need `portfolio` as an additional value.
- **Decision**: Do not over-engineer for vocational now. Flag as a future extension point.

### International curricula

**Verdict: Schema is UK-specific but extensible.**

- The typed labels are subject-archetypes, not UK-specific. `ScienceTopicSuggestion` would work for US NGSS or Australian curriculum with different controlled vocabularies.
- `curriculum_status` values (`mandatory`, `menu_choice`, `exemplar`, `convention`) are generic enough for any curriculum framework.
- The graph already has CASE standards as an independent layer. International TopicSuggestions could follow the same pattern: a separate layer with `ALIGNS_TO` relationships to UK suggestions.

---

## 7. Top 5 Concerns

### 1. Population cost: 200+ nodes each needing 12-18 populated properties

The specialists have designed a rich schema. Rich schemas produce excellent AI output — IF they're populated. A half-populated TopicSuggestion with empty `disciplinary_concepts`, null `misconceptions`, and missing `cross_curricular_hooks` is worse than a simpler schema that's fully populated.

**Mitigation**: Implement in phases. Phase 1: populate the 5 core subjects (History, Geography, Science, English, Maths) at KS2 only (~80-100 nodes). Phase 2: extend to KS1 and KS3. Phase 3: KS4 and foundation subjects. Validate AI generation quality at each phase before expanding.

### 2. VehicleTemplate-to-TopicSuggestion mapping ambiguity

Some topics genuinely suit multiple templates. A Roman Britain lesson could be `topic_study`, `source_enquiry`, or `comparison_study` depending on the lesson's focus. The schema says `USES_TEMPLATE` with `primary: bool`, but who decides which is primary?

**Mitigation**: Allow `USES_TEMPLATE` to be a ranked list (1 = default, 2 = alternative). The AI selects based on the learning objective and DifficultyLevel. Document that `USES_TEMPLATE` rank 1 is the recommended starting template, not the only valid choice.

### 3. Controlled vocabulary governance

The specialists have proposed ~15 controlled vocabularies (enquiry types, genres, map types, manipulatives, CPA stages, etc.). These must be maintained. If a new manipulative enters the market (like algebra tiles did), who adds it to the vocabulary?

**Mitigation**: Store controlled vocabularies as reference data in JSON files (pattern: `layers/uk-curriculum/data/controlled_vocabularies/`). Validation scripts check TopicSuggestion properties against these files. Adding a new value = updating the JSON + revalidating.

### 4. Subject-specific "required" properties blocking cross-subject queries

If a curriculum overview tool queries all TopicSuggestions for a year group, it will receive nodes with completely different property shapes. A HistoryTopicSuggestion has `disciplinary_concepts`; a MathsTopicSuggestion has `representations`. Dashboard and reporting tools must handle this gracefully.

**Mitigation**: All nodes share the universal property set (name, subject, key_stage, pedagogical_rationale, definitions, etc.). Cross-subject queries should use only universal properties. Subject-specific properties are for subject-specific content generation, not cross-subject reporting.

### 5. Exam board dependency (English KS4)

The `exam_board_status` property ties TopicSuggestions to specific exam boards (AQA, Edexcel, OCR, Eduqas). Exam boards update their set text lists periodically (AQA added new texts for 2025). This creates a maintenance burden.

**Mitigation**: Store exam board set text lists as separate reference data, not hard-coded in TopicSuggestion nodes. `exam_board_status` on the node captures the fact of being a set text; the specific board information comes from a join with the reference data. When boards change their lists, update the reference data, not the graph nodes.

---

## 8. Final Schema Recommendation

### Implement in this order

**Phase 0 (this review)**: Finalise schema decisions. This document is the arbitration.

**Phase 1: Core schema + VehicleTemplates**
- Create 9 uniqueness constraints (one per label) + indexes
- Import 24 VehicleTemplate nodes with session structures and agent_prompts
- Create `TEMPLATE_FOR` relationships to KeyStage (24 templates x 4 KS = up to 96 age-banded prompts)
- Validate with `validate_schema.py`

**Phase 2: Populate KS2 core subjects first (~80-100 TopicSuggestions)**
- History KS2: ~18 nodes (prescribed + exemplar + convention)
- Geography KS2: ~15 nodes
- Science KS2: ~24 nodes (Y3-Y6, ~6 per year)
- English KS2: ~16 nodes (genre requirements + exemplar texts)
- Maths KS2: ~11 nodes per year group
- Test AI generation quality with these nodes before expanding

**Phase 3: Extend to KS1, KS3, KS4, and foundation subjects**
- KS1 has fewer topics but distinctive patterns (KS1 History paired figures, KS1 Geography simple localities)
- KS3 adds volume but not structural complexity
- KS4 adds exam_board_status for English; science_discipline split for Science
- Foundation subjects (Art, Music, DT) add ~30-50 nodes across 3 new labels
- Generic TopicSuggestion for Computing, RS, Citizenship, Drama add ~30-40 nodes

**Phase 4: Migrate from ContentVehicle + Topic**
- Map existing 61 ContentVehicle nodes to new TopicSuggestion nodes (many will split: one CV "Roman Britain" becomes multiple TopicSuggestions with different templates)
- Map existing 55 Topic nodes to TopicSuggestion nodes (most become `prescribed_topic` or `teacher_convention`)
- Deprecate ContentVehicle and Topic labels
- Update `query_cluster_context.py` and `graph_query_helper.py` to query TopicSuggestions

### Key design principles (for implementers)

1. **One label per node.** No namespace labels. All TopicSuggestion nodes share `display_category: "Topic Suggestion"` for cross-label queries.

2. **Controlled vocabularies in JSON files.** Every enum property has a corresponding JSON file in `layers/uk-curriculum/data/controlled_vocabularies/`. Validation scripts enforce these at import time.

3. **Properties, not labels, capture subject variability.** The 9 typed labels capture structural differences (different required properties). Within a label, variability is captured by properties (e.g. `nc_aim_emphasis: "fluency"` vs `"reasoning"` on MathsTopicSuggestion).

4. **VehicleTemplates are pedagogical patterns, not lesson plans.** The template says "fair test follows: question -> hypothesis -> method -> data -> analysis -> conclusion." The AI tutor fills in the content at runtime. The TopicSuggestion says WHAT to teach; the VehicleTemplate says HOW to structure the session.

5. **Required means "absence causes generation failure."** Not "nice for data quality." If the AI can produce a pedagogically sound lesson without a property, that property is optional.

6. **Age-banded prompts on VehicleTemplates.** Each VehicleTemplate has `TEMPLATE_FOR {agent_prompt}` relationships to KeyStage nodes, following the ThinkingLens `PROMPT_FOR` pattern. This means the same `fair_test` template generates age-appropriate content for Y3 (concrete, supported, simple variables) and Y9 (abstract, independent, controlled variables) without needing separate templates.

7. **Sensitive content notes are a safeguarding requirement.** The platform serves children aged 5-14. Topics involving the Holocaust, slavery, colonialism, religious persecution, hazardous materials, or tool use MUST have `sensitive_content_notes` populated. This is not optional enrichment; it is a compliance obligation under the ICO Children's Code.

---

## Appendix A: Consolidated Property Tables

### Universal Properties (all 9 labels)

| Property | Type | Required | Status |
|---|---|---|---|
| `suggestion_id` | string | Yes | Original |
| `name` | string | Yes | Original |
| `suggestion_type` | string (9-value enum) | Yes | Modified (expanded enum) |
| `subject` | string | Yes | Original |
| `key_stage` | string | Yes | Original |
| `curriculum_status` | string | Yes | Original |
| `choice_group` | string | No | Original |
| `curriculum_reference` | string[] | No | Modified (was string) |
| `pedagogical_rationale` | string | Yes | Original |
| `common_pitfalls` | string[] | No | Original |
| `cross_curricular_hooks` | object[] | No | Modified (was string[]) |
| `sensitive_content_notes` | string[] | No | New (promoted to universal) |
| `year_groups` | string[] | No | New |
| `duration_lessons` | int | No | New |
| `definitions` | string[] | Yes | Original |
| `display_category` | string | Yes | Original |
| `display_color` | string | Yes | Original |
| `display_icon` | string | Yes | Original |

### HistoryTopicSuggestion

| Property | Type | Required | Status |
|---|---|---|---|
| `period` | string | Yes | Original |
| `period_start_year` | integer | No | New |
| `period_end_year` | integer | No | New |
| `key_figures` | string[] | No | Original |
| `comparison_pairs` | object[] | No | New (KS1) |
| `key_events` | string[] | No | Original |
| `sources` | string[] | No | Original |
| `source_types` | string[] | Yes | Modified (was optional) |
| `perspectives` | string[] | Yes | Original |
| `interpretations` | string[] | No | New (recommended for KS3+) |
| `disciplinary_concepts` | string[] | Yes | New |
| `significance_claim` | string | Yes | New |
| `enquiry_questions` | string[] | No | New |

### GeographyTopicSuggestion

| Property | Type | Required | Status |
|---|---|---|---|
| `locations` | string[] | Yes | Modified (was `location`: string) |
| `theme_category` | string | Yes | New |
| `themes` | string[] | Yes | Original |
| `scale` | string | Yes | New |
| `map_types` | string[] | Yes | New |
| `data_sources` | string[] | Yes | Modified (was optional) |
| `contrasting_with` | string | No | Original |
| `fieldwork_potential` | string | No | New |

### ScienceTopicSuggestion

| Property | Type | Required | Status |
|---|---|---|---|
| `enquiry_type` | string (7-value enum) | Yes | Modified (controlled vocab) |
| `secondary_enquiry_types` | string[] | No | New |
| `science_discipline` | string | Yes | New |
| `equipment` | string[] | Yes | Modified (was optional) |
| `safety_notes` | string | Yes | Modified (was optional) |
| `hazard_level` | string | Yes | New |
| `expected_outcome` | string | Yes | Modified (was optional) |
| `recording_format` | string[] | No | New (recommended) |
| `misconceptions` | string[] | Yes | New |
| `variables` | object | No | New (for fair_test/pattern_seeking) |

### EnglishTopicSuggestion

| Property | Type | Required | Status |
|---|---|---|---|
| `text_type` | string | Yes | New |
| `genre` | string[] | Yes | Modified (was string) |
| `text_features` | string[] | Yes | Original |
| `suggested_texts` | object[] | No | Modified (structured objects) |
| `reading_level` | string | Yes | New |
| `writing_outcome` | string | Yes | New |
| `grammar_focus` | string[] | No | New (recommended for KS1-3) |
| `spoken_language_focus` | string | No | New |
| `exam_board_status` | object[] | No | New (KS4 only) |
| `assessment_mode` | string | No | New |
| `literary_terms` | string[] | No | New |

### MathsTopicSuggestion

| Property | Type | Required | Status |
|---|---|---|---|
| `cpa_stage` | string (6-value enum) | Yes | Modified (controlled enum) |
| `cpa_notes` | string | No | New |
| `manipulatives` | string[] | Yes | Modified (was optional) |
| `representations` | string[] | Yes | Modified (was optional) |
| `fluency_targets` | string[] | Yes | New |
| `reasoning_prompts` | string[] | No | New |
| `application_contexts` | string[] | No | New |
| `nc_aim_emphasis` | string (4-value enum) | Yes | New |

### ArtTopicSuggestion

| Property | Type | Required | Status |
|---|---|---|---|
| `artist` | string | No | New |
| `art_movement` | string | No | New |
| `medium` | string[] | Yes | New |
| `techniques` | string[] | Yes | New |
| `visual_elements` | string[] | No | New |
| `themes` | string[] | No | New |

### MusicTopicSuggestion

| Property | Type | Required | Status |
|---|---|---|---|
| `composer` | string | No | New |
| `piece` | string | No | New |
| `genre` | string | No | New |
| `musical_elements` | string[] | Yes | New |
| `activity_focus` | string[] | Yes | New |
| `instrument` | string[] | No | New |
| `themes` | string[] | No | New |

### DTTopicSuggestion

| Property | Type | Required | Status |
|---|---|---|---|
| `dt_strand` | string | Yes | New |
| `design_brief` | string | Yes | New |
| `materials` | string[] | Yes | New |
| `tools` | string[] | No | New |
| `techniques` | string[] | Yes | New |
| `evaluation_criteria` | string[] | No | New |
| `safety_notes` | string | No | New |
| `themes` | string[] | No | New |

### TopicSuggestion (generic)

| Property | Type | Required | Status |
|---|---|---|---|
| `themes` | string[] | Yes | Original |
| *Extended optional per subject:* | | | |
| `computational_concept` | string[] | No | New (Computing) |
| `programming_paradigm` | string | No | New (Computing) |
| `software_tool` | string | No | New (Computing) |
| `religion` | string[] | No | New (RS) |
| `ethical_issue` | string | No | New (RS) |
| `civic_domain` | string | No | New (Citizenship) |
| `activity_type` | string | No | New (Citizenship) |
| `performance_style` | string | No | New (Drama) |
| `practitioner` | string | No | New (Drama) |

---

## Appendix B: VehicleTemplate Count Comparison

| Category | Original | Final | Change |
|---|---|---|---|
| Original retained | 14 | 14 | 0 (some renamed) |
| New additions | 0 | 10 | +10 |
| Proposals rejected/merged | — | 13 | -13 (from 23 proposed) |
| **Total** | **14** | **24** | **+10** |

This is a 71% increase in template count but a 57% reduction from what the specialists proposed (37 -> 24). Each addition serves a genuine pedagogical gap validated by 2+ specialist reviews or fills an NC statutory requirement that no existing template covers.
