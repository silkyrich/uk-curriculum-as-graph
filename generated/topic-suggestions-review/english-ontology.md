# English Ontology Design: Subject-Specific Graph Model

**Author**: KS2 + KS4 English Specialist
**Date**: 2026-02-24
**Status**: DESIGN PROPOSAL (for review)

---

## Executive Summary

English does not have "topics" in the way History, Geography, or Science do. A History teacher teaches "The Romans." A Science teacher teaches "Forces." An English teacher teaches **a genre through a text, producing a written outcome, with embedded grammar**. The organising unit of English teaching is the **text-genre-outcome triad**, not a topic.

The universal `TopicSuggestion` wrapper with ~10 shared properties and subject-specific extras cannot represent this. It forces English into a topic-shaped box when English is fundamentally **text-shaped** (KS1-KS3) and **assessment-objective-shaped** (KS4).

This document proposes a multi-node ontology that models English teaching as it actually works, from Reception through GCSE.

---

## 1. Node Labels and Rationale

### Three node labels, not one

| # | Label | Purpose | Key stages | Why a separate label? |
|---|---|---|---|---|
| 1 | **`EnglishUnit`** | The core teaching unit: a genre + text + writing outcome combination | KS1-KS4 | This is what teachers plan and teach. It replaces `EnglishTopicSuggestion`. The name "Unit" is used because English teachers say "we're doing a unit on adventure narrative" not "we're doing a topic on adventure narrative." |
| 2 | **`Genre`** | A text type/genre node with its own progression chain | KS1-KS4 | Genres are reusable across years and key stages. "Narrative" appears in Y1, Y4, Y7, and Y10. Modelling Genre as a separate node allows genre progression chains (simple recount Y1 -> extended narrative Y4 -> literary fiction Y10) and prevents genre data being duplicated across every unit. |
| 3 | **`SetText`** | A specific GCSE set text with exam board metadata | KS4 only | Set texts are fundamentally different from suggested texts. A suggested text ("The Iron Man is good for Y4 adventure narrative") is a recommendation. A set text ("Macbeth is on the AQA specification") is a curricular fact. Set texts have exam board status, popularity data, text categories, and assessment component mappings that suggested texts do not. Modelling them as a separate node allows schools to select their exam board and have the graph filter accordingly. |

### Why not a single `EnglishTopicSuggestion` node?

Three structural problems with the single-node approach:

1. **Genre duplication**: "Narrative" appears in 8+ units across KS1-KS4 with the same genre features, progressions, and conventions. A single node duplicates this data every time. A separate `Genre` node is referenced by many `EnglishUnit` nodes.

2. **Set text complexity**: A KS4 set text (Macbeth) has exam board status, text category, assessment components, popularity data, and key quotations. This metadata is text-specific, not unit-specific. Multiple units can reference the same set text (a Macbeth character unit, a Macbeth themes unit, a Macbeth context unit). Without a separate node, this data is duplicated or spread across units.

3. **The KS1-KS3 vs KS4 split**: KS1-KS3 English is genre-based (write in a range of genres). KS4 English Literature is text-based (study set texts analytically). KS4 English Language is skills-based (demonstrate reading and writing competencies). A single label forces these three fundamentally different organising principles into one shape.

---

## 2. Node: `Genre`

### Rationale

Genre is the organising principle of English from KS1 to KS3. The National Curriculum says pupils should "write for a range of purposes" and specifies text types (narrative, recount, report, explanation, persuasion, discussion, instruction, poetry). At KS4, genre shifts to literary category (drama, fiction, literary non-fiction, poetry, transactional). Genre is not a property of a unit -- it is a **reusable entity** with its own features, conventions, progression, and pedagogical identity.

### Properties

| Property | Type | Required | Rationale |
|---|---|---|---|
| `genre_id` | string | Yes | Format: `GEN-{code}` e.g. `GEN-NARR`, `GEN-RECOUNT`, `GEN-DRAMA`. Unique identifier. |
| `name` | string | Yes | Display name. E.g. "Narrative", "Recount", "Persuasion", "Drama". |
| `genre_family` | string | Yes | High-level classifier. Enum: `fiction`, `non_fiction`, `poetry`, `drama`, `mixed`. Tells the AI tutor immediately whether it is dealing with a fiction or non-fiction pedagogy. |
| `key_stages` | string[] | Yes | Which key stages this genre appears in. E.g. `["KS1", "KS2", "KS3"]` for narrative; `["KS4"]` for transactional. |
| `conventions` | string[] | Yes | The defining features of this genre that are stable across year groups. E.g. for narrative: `["characters", "setting", "plot", "conflict", "resolution"]`. For report: `["subheadings", "topic sentences", "present tense", "formal register"]`. These are the genre's DNA -- they do not change by year, only the sophistication of how they are deployed. |
| `sub_genres` | string[] | No | Named variants within this genre. E.g. for narrative: `["adventure", "mystery", "historical", "sci-fi", "fantasy"]`. For traditional_tale: `["fairy tale", "myth", "legend", "fable", "folk tale"]`. |
| `primary_writing_purposes` | string[] | Yes | What writing in this genre is FOR. Enum values: `to_entertain`, `to_inform`, `to_persuade`, `to_discuss`, `to_instruct`, `to_explain`, `to_describe`, `to_analyse`, `to_evaluate`. Multiple allowed. |
| `description` | string | Yes | What this genre IS, in plain language. For AI tutor use and parent communication. |
| `display_category` | string | Yes | `"English Ontology"` |
| `display_color` | string | Yes | `"#059669"` (Emerald-600, matching English) |
| `display_icon` | string | Yes | `"menu_book"` |

### Why Genre needs to be a node, not a property

Consider "narrative". At Y1, narrative means "write sentences to form short stories." At Y4, it means "write an extended adventure narrative with problem-resolution structure, vivid description, and dialogue." At Y10, it means "write literary fiction with controlled narrative voice, varied sentence structures for effect, and sophisticated structural choices." The genre is the same; the expectations are different. If genre is a property on the unit, the AI has no way to trace this progression. If genre is a node with relationships, the AI can query "show me all units that use narrative, ordered by key stage" and see the full trajectory.

---

## 3. Node: `EnglishUnit`

### Rationale

The `EnglishUnit` is the core teaching unit. It represents "what an English teacher plans and delivers over 2-4 weeks." In primary, this is typically a genre-based writing unit anchored to a model text. In KS4 Literature, this is a text study unit (one set text, one assessment focus). In KS4 Language, this is a skills practice unit (one paper component, one writing form).

### Properties

| Property | Type | Required | Rationale |
|---|---|---|---|
| **Identity** | | | |
| `unit_id` | string | Yes | Format: `EU-{subject_code}-{KS/Y}-{number}`. E.g. `EU-EN-Y4-001`, `EU-ELT-KS4-001`, `EU-ENL-KS4-001`. |
| `name` | string | Yes | Pattern: "{Genre/Focus}: {Anchor Text or Theme}". E.g. "Adventure Narrative: The Iron Man", "Shakespeare: Macbeth", "Transactional Writing: Speech". |
| `unit_type` | string | Yes | Enum: `genre_study` (KS1-KS3 genre-based writing unit), `text_study_analytical` (KS4 Literature analytical study), `skills_practice` (KS4 Language exam skills), `spelling_and_vocabulary` (standalone word-level unit), `spoken_language` (standalone oracy unit), `poetry_study` (dedicated poetry unit, any KS), `reading_for_pleasure` (statutory non-assessed reading). |
| **Curriculum position** | | | |
| `subject` | string | Yes | `"English"`, `"English Literature"`, or `"English Language"`. |
| `key_stage` | string | Yes | `"KS1"`, `"KS2"`, `"KS3"`, `"KS4"`. |
| `year_groups` | string[] | No | Specific year groups. E.g. `["Y3", "Y4"]` for lower KS2 content. |
| `curriculum_status` | string | Yes | Enum: `mandatory` (NC requires this genre/content), `menu_choice` (NC offers a choice, e.g. Shakespeare play), `exemplar` (good practice, not statutory), `convention` (near-universal teacher practice, not in NC). |
| `curriculum_reference` | string[] | No | NC sections. E.g. `["Writing - Composition (Y3-4)", "English Appendix 2 (Y4 grammar)", "Reading - Comprehension (Y3-4)"]`. |
| `suggestion_type` | string | Yes | Enum: `prescribed_topic`, `exemplar_text`, `genre_requirement`, `set_text`, `teacher_convention`, `open_slot`. Retained from universal schema for cross-subject queryability. |
| **The text-genre-outcome triad** | | | |
| `text_type` | string | Yes | High-level: `fiction`, `non_fiction`, `poetry`, `drama`, `mixed`. Redundant with Genre node's `genre_family` but kept on the unit for fast filtering without joins. |
| `text_features_to_teach` | string[] | Yes | The specific textual/genre features this unit teaches. E.g. `["problem-resolution structure", "vivid description", "dialogue to advance plot", "building suspense"]`. These are the SUCCESS CRITERIA for the unit. Named `text_features_to_teach` (not `text_features`) to clarify these are pedagogical targets, not just descriptions of the text. |
| `writing_outcome` | string | **Yes** | **The single most important property in the entire English ontology.** What the child produces. E.g. "Write an adventure narrative (500-700 words) with clear problem-resolution structure, vivid description, and dialogue." Without this, the AI tutor has no idea what lesson to generate. Every English lesson ends with a piece of writing (or a performance -- see `spoken_language_outcome`). |
| `spoken_language_outcome` | string | No | For units with a primary spoken language outcome. E.g. "Perform a poem to an audience with appropriate expression, pace, and volume." Separate from `writing_outcome` because some units have both, and the NC assesses them differently. |
| **Grammar (statutory, year-specific)** | | | |
| `grammar_focus` | string[] | **Yes (KS1-KS3)** | The statutory grammar to embed in this unit. E.g. `["fronted adverbials", "expanded noun phrases", "direct speech punctuation"]`. REQUIRED for KS1-KS3 because the NC specifies grammar by year group. Optional for KS4 where grammar is embedded in AO6/writing quality. The AI MUST know the grammar focus to generate appropriate teaching and marking. |
| `grammar_year_source` | string | No | Which year's grammar appendix this draws from. E.g. `"Y4"`. Needed because a Y4 class might revise Y3 grammar or preview Y5 grammar. |
| **Suggested texts** | | | |
| `suggested_texts` | object[] | No | Recommended anchor texts for this unit. Structured objects (not strings): `{title: string, author: string, publication_year: int|null, text_type: string, suitability: string, note: string}`. For KS1-KS3 these are SUGGESTIONS. For KS4 Literature, the text is linked via a `SetText` node relationship instead. |
| `reading_level` | string | Yes | Age-appropriateness of the text/content. Values: phonics-based for KS1 (`"Phase 3"`, `"Phase 5"`), year-based for KS2 (`"Y3-Y5"`, `"Y4"`), KS-based for secondary (`"KS3"`, `"KS4"`). This is a CURRICULUM DESIGN property (which texts are appropriate at which age), not a runtime property. |
| **Assessment and pedagogy** | | | |
| `assessment_mode` | string | No | Enum: `formative` (in-lesson checks), `summative` (end-of-unit), `exam_practice` (SATs/GCSE style). Tells the AI whether to generate teaching activities or assessment tasks. |
| `assessment_focus` | string[] | No | For KS4: the assessment objectives being targeted. E.g. `["AO1", "AO2", "AO3"]`. For KS2: the content domain codes. E.g. `["2a", "2b", "2d"]` (SATs reading reference codes). |
| `pedagogical_rationale` | string | Yes | WHY this text/genre combination works at this year group. The AI can use this to explain choices to parents and to make pedagogical decisions. |
| `common_pitfalls` | string[] | No | What goes wrong when this unit is taught badly. |
| **Vocabulary and terminology** | | | |
| `literary_terms` | string[] | No | Subject-specific terminology to introduce: `["protagonist", "antagonist", "climax"]`. These are terms the child learns to USE, not just vocabulary from the text. |
| `definitions` | string[] | Yes | Key vocabulary for this unit, including both literary terminology and content vocabulary. |
| **Cross-curricular** | | | |
| `cross_curricular_hooks` | string[] | No | Specific links to other subjects. Format: `"[Subject] description"`. E.g. `"[History] Ancient Greece - myths as primary sources"`. |
| `spoken_language_focus` | string | No | If this unit has an explicit spoken language component: `"retelling"`, `"performance"`, `"debate"`, `"dramatic_role_play"`, `"formal_presentation"`. |
| **Display** | | | |
| `display_category` | string | Yes | `"English Ontology"` |
| `display_color` | string | Yes | `"#059669"` (Emerald-600) |
| `display_icon` | string | Yes | `"edit_note"` |

### Why `writing_outcome` is the most important property

In my review, I identified `writing_outcome` as the property that makes or breaks English lesson generation. Here is why:

Consider the unit "Greek Myths (Y4)". Without `writing_outcome`, the AI tutor could generate any of these completely different lessons:
- A myth retelling (creative writing, narrative genre)
- An information text about ancient Greece (non-fiction, report genre)
- A diary entry from Theseus's perspective (creative writing, recount genre)
- A comparative analysis of two myths (analytical writing, discussion genre)
- A playscript based on a myth (creative writing, drama genre)

These are five entirely different lessons with different success criteria, different grammar foci, and different assessment approaches. The `writing_outcome` property is the instruction that disambiguates them: "Retell a Greek myth in own words (400-600 words) preserving key features and adding vivid description." Now the AI knows exactly what to generate.

### Why `writing_outcome` is a property, not a separate node

I considered making `WritingOutcome` a separate node. Arguments for: it has its own properties (length, form, features required) and could be reused. Arguments against: writing outcomes are rarely reused across units -- "Write an adventure narrative (500-700 words) with problem-resolution structure" is specific to the Adventure Narrative unit. The overhead of a separate node, relationship, and ID scheme is not justified by the reuse pattern. A string property with a clear format convention (`"Write [form] ([length]) with [features]"`) is simpler and equally queryable via full-text search.

---

## 4. Node: `SetText`

### Rationale

At KS4, English Literature teaching is organised around **set texts** chosen from exam board specifications. These texts are not suggestions -- they are curricular facts. A school that chooses AQA must teach one of six Shakespeare plays, one of nine 19th-century novels, one of eleven modern texts, and one poetry anthology. The choice is the school's, but once made, the text is mandatory.

Set texts have properties that suggested texts do not: exam board status, text category, assessment component mapping, popularity data (which affects resource availability), and key quotations (for closed-book exams). Modelling them as a separate node allows:
- Schools to filter by their exam board
- The AI to know which texts are set vs suggested
- Multiple `EnglishUnit` nodes to reference the same `SetText` (character unit, themes unit, context unit all reference "Macbeth")
- Popularity data to inform resource prioritisation

### Properties

| Property | Type | Required | Rationale |
|---|---|---|---|
| `set_text_id` | string | Yes | Format: `ST-{board_code}-{category_code}-{number}`. E.g. `ST-AQA-SHAK-001` (Macbeth on AQA). A text that appears on multiple boards gets one node per board, because the assessment requirements differ. |
| `name` | string | Yes | Display name. E.g. "Macbeth". |
| `title` | string | Yes | Full title. E.g. "The Tragedy of Macbeth". |
| `author` | string | Yes | E.g. "William Shakespeare". |
| `publication_year` | int | No | Original publication. E.g. 1606. |
| `exam_board` | string | Yes | Enum: `AQA`, `Edexcel`, `OCR`, `Eduqas`, `WJEC`, `CCEA`. |
| `text_category` | string | Yes | Enum: `shakespeare`, `19th_century_novel`, `modern_text`, `poetry_anthology`. Maps to the GCSE assessment component. |
| `assessment_component` | string | Yes | Which exam paper/section. E.g. `"Paper 1 Section A"` (AQA Shakespeare). |
| `genre` | string[] | Yes | Literary genres. E.g. `["drama", "tragedy"]` for Macbeth, `["fiction", "gothic", "novella"]` for Jekyll and Hyde. |
| `period` | string | Yes | Literary period. E.g. `"Jacobean"`, `"Victorian"`, `"Post-war"`. |
| `popularity_estimate` | string | No | Approximate uptake. Enum: `dominant` (>50%), `common` (20-50%), `moderate` (5-20%), `niche` (<5%). Based on exam board entry data and teacher surveys. Informs which texts get the most resource development. |
| `key_themes` | string[] | Yes | The major themes. E.g. for Macbeth: `["ambition", "power", "guilt", "supernatural", "masculinity", "loyalty and betrayal", "appearance vs reality"]`. The AI uses these to generate theme-based revision activities. |
| `key_context_points` | string[] | Yes | Historical/social context the student must know for AO3. E.g. for Macbeth: `["Jacobean attitudes to witchcraft", "the Gunpowder Plot (1605)", "the Great Chain of Being", "divine right of kings", "the real Macbeth"]`. |
| `key_quotations` | object[] | No | Essential quotations for closed-book study. `{act_scene: string, speaker: string, quotation: string, significance: string}`. E.g. `{act_scene: "1.7", speaker: "Macbeth", quotation: "I have no spur / To prick the sides of my intent", significance: "Horse metaphor reveals Macbeth's lack of motivation beyond ambition"}`. |
| `literary_heritage` | boolean | Yes | Whether this text qualifies as part of the "English literary heritage" (statutory requirement: at least 3 of 6 texts must be from the heritage). |
| `closed_book` | boolean | Yes | Whether the exam is closed book (no text in the exam room). Currently all GCSE Lit is closed book, but this may change. |
| `display_category` | string | Yes | `"English Ontology"` |
| `display_color` | string | Yes | `"#7C3AED"` (Violet-600, distinguishing set texts from units) |
| `display_icon` | string | Yes | `"auto_stories"` |

### Why `SetText` needs to be a node, not a property

1. **Multiple units per text**: Macbeth generates at least 4-5 units: character study (Macbeth), character study (Lady Macbeth), themes (ambition and power), themes (supernatural), context (Jacobean England). Each unit references the same SetText node, avoiding duplication of exam board status, key quotations, and context points.

2. **Exam board filtering**: A school using AQA needs to see only AQA set texts. A property on the unit cannot be filtered this cleanly. A `SetText` node with `exam_board: "AQA"` can be.

3. **Cross-board comparison**: Some texts appear on multiple boards (Macbeth is on all four). A separate node per board+text combination allows the graph to represent this without tangling unit data.

4. **Quotation bank**: Key quotations are text-specific, not unit-specific. A Macbeth character unit and a Macbeth themes unit both need the same quotation bank. A `SetText` node holds this once.

---

## 5. Relationship Model

### Relationships TO existing graph nodes

```
(:EnglishUnit)-[:DELIVERS_VIA {primary: bool}]->(:Concept)
    The unit delivers curriculum concepts. Primary = true for the main teaching
    focus; false for secondary/incidental coverage.

(:EnglishUnit)-[:USES_TEMPLATE]->(:VehicleTemplate)
    The unit uses a teaching template (text_study, writers_workshop,
    grammar_in_context, text_study_literature, etc.).

(:Domain)-[:HAS_UNIT]->(:EnglishUnit)
    The curriculum domain contains this unit. Mirrors HAS_SUGGESTION / HAS_VEHICLE.

(:ConceptCluster)-[:SUGGESTED_UNIT {rank: int}]->(:EnglishUnit)
    A concept cluster recommends this unit. Rank 1 = primary recommendation.

(:EnglishUnit)-[:DEVELOPS_SKILL]->(:ReadingSkill)
    The unit develops specific reading skills from the epistemic skills layer.
    E.g. an adventure narrative unit develops RS-KS2-2d (inference) and
    RS-KS2-2g (authorial intent).

(:KeyStage)<-[:AVAILABLE_AT]-(:SetText)
    Set texts are available at a specific key stage (always KS4 currently).
```

### Relationships BETWEEN English nodes

```
(:EnglishUnit)-[:IN_GENRE {role: str}]->(:Genre)
    The unit teaches in this genre. Role = "primary" (the main genre being taught)
    or "secondary" (a genre touched incidentally). E.g. "Greek Myths" is
    IN_GENRE {role: "primary"} -> traditional_tale, and IN_GENRE {role: "secondary"}
    -> narrative (because the retelling IS a narrative).

(:EnglishUnit)-[:STUDIES_TEXT]->(:SetText)
    KS4 Literature units study a specific set text. This is how the graph
    connects "Macbeth Character Study" to "Macbeth (AQA, Shakespeare)".
    Only for KS4 Literature. KS1-KS3 use the `suggested_texts` property
    because those texts are recommendations, not curricular requirements.

(:Genre)-[:PROGRESSES_TO]->(:Genre)
    Genre progression chain. E.g. traditional_tale (KS1) PROGRESSES_TO
    narrative (KS2) PROGRESSES_TO fiction (KS3-4). This encodes the trajectory
    from simple genre forms to complex literary categories.
    Properties: {from_ks: str, to_ks: str, progression_note: str}.

(:Genre)-[:RELATED_GENRE]->(:Genre)
    Genre affinity. E.g. persuasion RELATED_GENRE discussion (they share
    argument structure). Recount RELATED_GENRE report (they share
    organisational features). The AI uses this for "if you liked teaching X,
    try Y" recommendations.

(:EnglishUnit)-[:GRAMMAR_SEQUENCE_AFTER]->(:EnglishUnit)
    Grammar sequencing within a year group. English grammar is statutory and
    year-specific. Direct speech punctuation should be taught BEFORE complex
    dialogue in narrative. Fronted adverbials should be taught BEFORE
    "vary sentence openings for effect." This relationship encodes the
    optimal grammar sequence.
    Properties: {grammar_point: str, rationale: str}.

(:EnglishUnit)-[:TEXT_COMPLEXITY_AFTER]->(:EnglishUnit)
    Text complexity progression within a year or across years. "Traditional
    Tales (Y1)" -> "Fairy Tale Retellings (Y4)" -> "Gothic Fiction (KS3)".
    Encodes the reading-difficulty and analytical-demand trajectory.

(:SetText)-[:SAME_TEXT_DIFFERENT_BOARD]->(:SetText)
    Links the same text across exam boards. E.g. Macbeth (AQA) <->
    Macbeth (Edexcel). Allows the AI to say "this text is also available
    on Edexcel" if a school is considering switching boards.
```

### Full relationship diagram (ASCII)

```
                                    (:KeyStage)
                                        ^
                                        |
                                  [:AVAILABLE_AT]
                                        |
(:ReadingSkill) <--[:DEVELOPS_SKILL]-- (:EnglishUnit) --[:STUDIES_TEXT]--> (:SetText)
                                        |       |                            |
                                   [:IN_GENRE]  [:DELIVERS_VIA]    [:SAME_TEXT_DIFFERENT_BOARD]
                                        |       |
                                        v       v
                                   (:Genre)  (:Concept)
                                     |   |
                        [:PROGRESSES_TO] [:RELATED_GENRE]
                                     |   |
                                     v   v
                                   (:Genre)

(:Domain) --[:HAS_UNIT]--> (:EnglishUnit) --[:USES_TEMPLATE]--> (:VehicleTemplate)
                               |        |
                  [:GRAMMAR_SEQUENCE_AFTER]  [:TEXT_COMPLEXITY_AFTER]
                               |        |
                               v        v
                         (:EnglishUnit)  (:EnglishUnit)

(:ConceptCluster) --[:SUGGESTED_UNIT {rank}]--> (:EnglishUnit)
```

---

## 6. How KS1-KS2 Differs from KS4

### KS1-KS2: Genre-based, text-as-model

```
EnglishUnit: "Adventure Narrative: The Iron Man"
  unit_type: genre_study
  subject: "English"
  text_type: "fiction"
  writing_outcome: "Write an adventure narrative (500-700 words)..."
  grammar_focus: ["fronted adverbials", "expanded noun phrases", "direct speech punctuation"]
  suggested_texts: [{title: "The Iron Man", author: "Ted Hughes", ...}]
  reading_level: "Y3-Y5"
  --[:IN_GENRE {role: "primary"}]--> Genre: "Narrative"
  --[:DELIVERS_VIA {primary: true}]--> Concept: EN-Y4-C016 (composition)
  --[:USES_TEMPLATE]--> VehicleTemplate: "text_study" (shared_reading -> analysis -> planning -> drafting -> editing)
```

The text is a MODEL. Children read it, analyse its features, then write their OWN text in the same genre. The grammar is statutory and year-specific. The writing outcome defines success.

### KS4 Literature: Text-based, analytical writing

```
EnglishUnit: "Macbeth: Character and Ambition"
  unit_type: text_study_analytical
  subject: "English Literature"
  text_type: "drama"
  writing_outcome: "Write an analytical essay (600-800 words) exploring how Shakespeare presents ambition..."
  assessment_focus: ["AO1", "AO2", "AO3"]
  grammar_focus: []  -- not year-specific at KS4
  reading_level: "KS4"
  --[:IN_GENRE {role: "primary"}]--> Genre: "Drama"
  --[:STUDIES_TEXT]--> SetText: "Macbeth" (AQA, shakespeare, Paper 1 Section A)
  --[:DELIVERS_VIA {primary: true}]--> Concept: ELT-KS4-C001 (close reading of Shakespeare)
  --[:USES_TEMPLATE]--> VehicleTemplate: "text_study_literature" (close_reading -> analysis -> contextualisation -> essay_writing)
```

The text is the OBJECT OF STUDY. Students write ABOUT the text analytically, not inspired BY it creatively. The exam board and assessment objectives determine the teaching focus. Grammar is embedded in writing quality (AO4), not taught as separate year-specific items.

### KS4 Language: Skills-based, form-driven writing

```
EnglishUnit: "Transactional Writing: Speech"
  unit_type: skills_practice
  subject: "English Language"
  text_type: "non_fiction"
  writing_outcome: "Write a speech (450-600 words) arguing for or against a proposition, using rhetorical devices..."
  assessment_focus: ["AO5", "AO6"]
  grammar_focus: []
  reading_level: "KS4"
  --[:IN_GENRE {role: "primary"}]--> Genre: "Transactional"
  --[:DELIVERS_VIA {primary: true}]--> Concept: ENL-KS4-C010 (transactional writing)
  --[:USES_TEMPLATE]--> VehicleTemplate: "writers_workshop" (mini_lesson -> independent_writing -> conferencing -> revision)
```

English Language has no set texts. It is a skills subject assessed through unseen texts (reading) and specified forms (writing). The genre and writing form are the organising principles, not a specific text.

### The English Language vs English Literature split

At KS4, English is TWO subjects with TWO GCSEs:
- **English Literature** (`ELT`): Set texts, analytical reading, literary essay writing. Assessment objectives AO1-AO4.
- **English Language** (`ENL`): Unseen texts, creative and transactional writing. Assessment objectives AO1-AO6.

These are modelled through the `subject` property on `EnglishUnit`:
- `subject: "English"` for KS1-KS3 (unified subject)
- `subject: "English Literature"` for KS4 Literature
- `subject: "English Language"` for KS4 Language

The `Genre` nodes are shared across both subjects. "Drama" as a genre is used by both Literature (studying Macbeth) and Language (studying a 20th-century play extract as unseen reading). The `SetText` nodes are Literature-only.

---

## 7. Grammar Focus: Interaction with Text/Genre

Grammar in English is statutory and year-specific (KS1-KS3). The NC Appendix 2 specifies exactly which grammar must be taught in each year. This creates a constraint: the grammar focus of a unit MUST match the year group's statutory grammar.

### The problem

A Y4 teacher wants to teach "Greek Myths" (retelling genre). The statutory Y4 grammar includes fronted adverbials, expanded noun phrases, direct speech punctuation, and present perfect tense. The teacher must embed at least some of these in the unit. The `grammar_focus` property on `EnglishUnit` captures this.

But grammar also has a SEQUENCE. Direct speech punctuation should ideally be introduced through a unit that involves dialogue (narrative, playscript) before being expected in independent writing across all genres. This means the grammar sequence creates dependencies between units.

### The solution

The `GRAMMAR_SEQUENCE_AFTER` relationship encodes these dependencies:

```
EU-EN-Y4-001 (Adventure Narrative) --[:GRAMMAR_SEQUENCE_AFTER {
  grammar_point: "direct speech punctuation",
  rationale: "Dialogue in narrative is the natural context for introducing inverted commas"
}]--> EU-EN-Y4-006 (Fairy Tale Retelling)
```

This means: if you want to teach fairy tale retelling with dialogue, the adventure narrative unit (which introduces direct speech punctuation) should come first.

The AI tutor queries these relationships to suggest unit ordering that respects grammar sequencing. This is something the universal `TopicSuggestion` cannot model because grammar sequence is English-specific.

---

## 8. Example Instances

### Example 1: Y4 Adventure Narrative (KS2, genre study)

**Genre node:**
```json
{
  "genre_id": "GEN-NARR",
  "name": "Narrative",
  "genre_family": "fiction",
  "key_stages": ["KS1", "KS2", "KS3", "KS4"],
  "conventions": ["characters", "setting", "plot", "conflict", "resolution", "narrator", "dialogue"],
  "sub_genres": ["adventure", "mystery", "historical", "sci-fi", "fantasy", "horror", "realistic"],
  "primary_writing_purposes": ["to_entertain"],
  "description": "Extended prose fiction with characters, setting, and a plot driven by conflict and resolution. The dominant literary form across all key stages, progressing from simple retelling (KS1) through structured narrative (KS2) to literary fiction with controlled voice and style (KS3-KS4)."
}
```

**EnglishUnit node:**
```json
{
  "unit_id": "EU-EN-Y4-001",
  "name": "Adventure Narrative: The Iron Man",
  "unit_type": "genre_study",
  "subject": "English",
  "key_stage": "KS2",
  "year_groups": ["Y4"],
  "curriculum_status": "exemplar",
  "suggestion_type": "exemplar_text",
  "curriculum_reference": [
    "Writing - Composition (Y3-4)",
    "Reading - Comprehension (Y3-4)",
    "English Appendix 2 (Y4 grammar)"
  ],
  "text_type": "fiction",
  "text_features_to_teach": [
    "problem-resolution structure",
    "vivid description using expanded noun phrases",
    "dialogue to advance plot",
    "building suspense through sentence variation"
  ],
  "writing_outcome": "Write an adventure narrative (500-700 words) with clear problem-resolution structure, vivid description using expanded noun phrases, and dialogue punctuated with inverted commas",
  "grammar_focus": ["fronted adverbials", "expanded noun phrases", "direct speech punctuation"],
  "grammar_year_source": "Y4",
  "suggested_texts": [
    {"title": "The Iron Man", "author": "Ted Hughes", "publication_year": 1968, "text_type": "novel", "suitability": "Y3-Y5", "note": "Clear three-act structure, rich vocabulary, accessible themes of fear and friendship"},
    {"title": "Stig of the Dump", "author": "Clive King", "publication_year": 1963, "text_type": "novel", "suitability": "Y3-Y5", "note": "Alternative anchor text with adventure + historical elements"}
  ],
  "reading_level": "Y3-Y5",
  "spoken_language_focus": "retelling",
  "literary_terms": ["protagonist", "antagonist", "climax", "resolution", "suspense", "imagery", "personification"],
  "definitions": ["narrative", "protagonist", "antagonist", "setting", "climax", "resolution", "suspense", "dialogue"],
  "pedagogical_rationale": "Ted Hughes' The Iron Man provides a rich model for adventure narrative writing with its clear problem-resolution structure, vivid descriptive language, and dialogue that advances the plot. The text's accessible yet ambitious vocabulary and structural clarity make it an ideal mentor text for Y4 pupils learning to sustain narrative writing across multiple paragraphs with fronted adverbials and expanded noun phrases.",
  "common_pitfalls": [
    "Pupils retell The Iron Man rather than writing their own adventure narrative using its structural features",
    "Dialogue added decoratively rather than used to advance the plot or reveal character",
    "Fronted adverbials used repetitively without varying sentence openings"
  ],
  "cross_curricular_hooks": [
    "[Science] Materials and their properties - the Iron Man's metal body",
    "[PSHE] Themes of fear, friendship, and acceptance of difference",
    "[Art] Illustration and character design inspired by the text"
  ]
}
```

**Relationships:**
```
(EU-EN-Y4-001)-[:IN_GENRE {role: "primary"}]->(GEN-NARR)
(EU-EN-Y4-001)-[:DELIVERS_VIA {primary: true}]->(EN-Y4-C016)   // composition
(EU-EN-Y4-001)-[:DELIVERS_VIA {primary: false}]->(EN-Y4-C017)  // reading comprehension
(EU-EN-Y4-001)-[:DELIVERS_VIA {primary: false}]->(EN-Y4-C019)  // inference
(EU-EN-Y4-001)-[:DELIVERS_VIA {primary: false}]->(EN-Y4-C026)  // fronted adverbials
(EU-EN-Y4-001)-[:DELIVERS_VIA {primary: false}]->(EN-Y4-C027)  // expanded noun phrases
(EU-EN-Y4-001)-[:DELIVERS_VIA {primary: false}]->(EN-Y4-C046)  // direct speech punctuation
(EU-EN-Y4-001)-[:USES_TEMPLATE]->(VT-07)                        // text_study
(EU-EN-Y4-001)-[:DEVELOPS_SKILL]->(RS-KS2-2d)                   // inference
(EU-EN-Y4-001)-[:DEVELOPS_SKILL]->(RS-KS2-2g)                   // authorial intent
(EN-Y4-D006)-[:HAS_UNIT]->(EU-EN-Y4-001)                        // Writing - Composition domain
```

### Example 2: Y10 Macbeth (KS4 Literature, analytical text study)

**SetText node:**
```json
{
  "set_text_id": "ST-AQA-SHAK-001",
  "name": "Macbeth",
  "title": "The Tragedy of Macbeth",
  "author": "William Shakespeare",
  "publication_year": 1606,
  "exam_board": "AQA",
  "text_category": "shakespeare",
  "assessment_component": "Paper 1 Section A",
  "genre": ["drama", "tragedy"],
  "period": "Jacobean",
  "popularity_estimate": "dominant",
  "key_themes": ["ambition", "power", "guilt", "supernatural", "masculinity", "loyalty and betrayal", "appearance vs reality", "fate vs free will"],
  "key_context_points": [
    "Jacobean attitudes to witchcraft and King James I's Daemonologie (1597)",
    "The Gunpowder Plot (1605) and anxiety about regicide",
    "The Great Chain of Being and divine right of kings",
    "The real Macbeth (11th-century Scottish king)",
    "Patriarchal gender roles in Jacobean society",
    "The role of the theatre as moral instruction"
  ],
  "key_quotations": [
    {"act_scene": "1.5", "speaker": "Lady Macbeth", "quotation": "unsex me here", "significance": "Transgression of gender roles, invocation of supernatural power"},
    {"act_scene": "1.7", "speaker": "Macbeth", "quotation": "I have no spur / To prick the sides of my intent, but only / Vaulting ambition", "significance": "Admits ambition is his sole motivation; horse metaphor suggests overreaching"},
    {"act_scene": "2.2", "speaker": "Macbeth", "quotation": "Will all great Neptune's ocean wash this blood / Clean from my hand?", "significance": "Guilt overwhelms immediately; hyperbolic imagery of permanent stain"},
    {"act_scene": "5.5", "speaker": "Macbeth", "quotation": "a tale / Told by an idiot, full of sound and fury, / Signifying nothing", "significance": "Nihilistic despair; meta-theatrical reference to meaninglessness of performance and life"}
  ],
  "literary_heritage": true,
  "closed_book": true
}
```

**EnglishUnit node:**
```json
{
  "unit_id": "EU-ELT-KS4-001",
  "name": "Macbeth: Ambition and Moral Decline",
  "unit_type": "text_study_analytical",
  "subject": "English Literature",
  "key_stage": "KS4",
  "year_groups": ["Y10", "Y11"],
  "curriculum_status": "menu_choice",
  "suggestion_type": "set_text",
  "curriculum_reference": ["GCSE English Literature: Shakespeare (AO1, AO2, AO3, AO4)"],
  "text_type": "drama",
  "text_features_to_teach": [
    "soliloquy as a window into character's internal conflict",
    "blank verse vs prose as indicator of status and mental state",
    "dramatic irony and audience complicity",
    "structural arc of rise and fall (tragic trajectory)"
  ],
  "writing_outcome": "Write an analytical essay (600-800 words) exploring how Shakespeare presents the theme of ambition in Macbeth, using quotations and contextual knowledge to support a sustained critical argument",
  "assessment_focus": ["AO1", "AO2", "AO3"],
  "reading_level": "KS4",
  "literary_terms": ["soliloquy", "blank verse", "iambic pentameter", "dramatic irony", "hamartia", "hubris", "catharsis", "tragic hero", "aside", "motif"],
  "definitions": ["ambition", "regicide", "tyranny", "soliloquy", "dramatic irony", "hamartia"],
  "pedagogical_rationale": "Macbeth is the most widely-taught Shakespeare play at GCSE (70-76% of entries on AQA). Its relatively short length, clear tragic arc, and accessible themes of ambition and guilt make it the most manageable Shakespeare text for mixed-ability classes. The play's focus on power and moral choice resonates with teenage students and provides rich analytical opportunities across all three assessed AOs.",
  "common_pitfalls": [
    "Students retell plot rather than analysing how Shakespeare creates effects",
    "Context (AO3) bolted on as a paragraph rather than integrated into analysis",
    "Quotations presented without analysis of specific word choices (AO2)",
    "Writing about what Macbeth thinks rather than how Shakespeare constructs the character"
  ],
  "cross_curricular_hooks": [
    "[History] Jacobean England, divine right of kings, the Gunpowder Plot",
    "[RS] Morality, guilt, the supernatural, free will vs fate",
    "[Drama] Performance interpretation of key scenes"
  ]
}
```

**Relationships:**
```
(EU-ELT-KS4-001)-[:IN_GENRE {role: "primary"}]->(GEN-DRAMA)
(EU-ELT-KS4-001)-[:STUDIES_TEXT]->(ST-AQA-SHAK-001)
(EU-ELT-KS4-001)-[:DELIVERS_VIA {primary: true}]->(ELT-KS4-C001)  // Shakespeare close reading
(EU-ELT-KS4-001)-[:DELIVERS_VIA {primary: false}]->(ELT-KS4-C003) // thematic analysis
(EU-ELT-KS4-001)-[:DELIVERS_VIA {primary: false}]->(ELT-KS4-C005) // contextualisation
(EU-ELT-KS4-001)-[:USES_TEMPLATE]->(VT-23)                         // text_study_literature
(ELT-KS4-D001)-[:HAS_UNIT]->(EU-ELT-KS4-001)                      // Shakespeare domain
(ST-AQA-SHAK-001)-[:AVAILABLE_AT]->(KS4)
```

### Example 3: Y1 Traditional Tales (KS1, early genre study)

**EnglishUnit node:**
```json
{
  "unit_id": "EU-EN-KS1-001",
  "name": "Traditional Tales: The Three Billy Goats Gruff",
  "unit_type": "genre_study",
  "subject": "English",
  "key_stage": "KS1",
  "year_groups": ["Y1"],
  "curriculum_status": "mandatory",
  "suggestion_type": "exemplar_text",
  "curriculum_reference": [
    "Reading - Comprehension (Y1): listening to and discussing a wide range of poems, stories and non-fiction",
    "Writing - Composition (Y1): write sentences by sequencing sentences to form short narratives"
  ],
  "text_type": "fiction",
  "text_features_to_teach": [
    "repeated refrain (Trip, trap, trip, trap)",
    "rule of three (three goats, three attempts)",
    "good vs evil (goats vs troll)",
    "beginning, middle, end structure"
  ],
  "writing_outcome": "Retell the story in 4-6 sentences using the repeated refrain and sequencing words (first, then, next, finally)",
  "grammar_focus": ["joining words (and)", "sequencing words (first, then, next)", "capital letters and full stops"],
  "grammar_year_source": "Y1",
  "suggested_texts": [
    {"title": "The Three Billy Goats Gruff", "author": "Traditional (various illustrators)", "publication_year": null, "text_type": "picture book", "suitability": "Y1", "note": "Use a version with clear, large illustrations for shared reading"}
  ],
  "reading_level": "Phase 4-5",
  "spoken_language_focus": "retelling",
  "spoken_language_outcome": "Retell the story orally using a story map, with appropriate expression for different characters",
  "literary_terms": ["character", "setting", "beginning", "middle", "end"],
  "definitions": ["troll", "bridge", "refrain", "character", "story"],
  "pedagogical_rationale": "Traditional tales are the entry point to narrative at KS1. The Three Billy Goats Gruff is ideal for Y1 because its repetitive structure, limited cast, and clear conflict support oral retelling before written retelling. The rule of three provides a scaffolding structure that Y1 children can internalise and replicate.",
  "common_pitfalls": [
    "Spending too long on drama/retelling without moving to written output",
    "Not explicitly teaching the story structure (beginning/middle/end) as a transferable pattern",
    "Writing task too ambitious for Y1 - keep to 4-6 sentences"
  ]
}
```

### Example 4: KS4 English Language Transactional Writing (skills practice)

**EnglishUnit node:**
```json
{
  "unit_id": "EU-ENL-KS4-003",
  "name": "Transactional Writing: Speech",
  "unit_type": "skills_practice",
  "subject": "English Language",
  "key_stage": "KS4",
  "year_groups": ["Y10", "Y11"],
  "curriculum_status": "mandatory",
  "suggestion_type": "genre_requirement",
  "curriculum_reference": ["GCSE English Language: Writing (AO5, AO6) - Paper 2 Section B"],
  "text_type": "non_fiction",
  "text_features_to_teach": [
    "direct address (rhetorical questions, imperatives, inclusive pronouns)",
    "tricolon and anaphora for emphasis",
    "structural signposting (opening hook, logical argument, emotive close)",
    "register shift (formal persuasion with controlled informality)",
    "counter-argument and rebuttal"
  ],
  "writing_outcome": "Write a speech (450-600 words) arguing for or against a proposition, using rhetorical devices, structural techniques, and appropriate register for a specific audience",
  "assessment_focus": ["AO5", "AO6"],
  "reading_level": "KS4",
  "assessment_mode": "exam_practice",
  "literary_terms": ["rhetoric", "anaphora", "tricolon", "hyperbole", "direct address", "imperative", "modal verb"],
  "definitions": ["rhetoric", "persuasion", "proposition", "counter-argument", "rebuttal", "register"],
  "pedagogical_rationale": "Speech writing is the most frequently examined transactional form on GCSE English Language Paper 2. It requires students to combine persuasive technique, structural control, and audience awareness in a timed condition. Explicit teaching of rhetorical devices (tricolon, anaphora, direct address) gives students a transferable toolkit they can deploy in articles, letters, and reviews too.",
  "common_pitfalls": [
    "Opening with 'Hello, my name is...' instead of a hook",
    "Rhetorical questions overused as the only persuasive technique",
    "No structural logic - arguments presented as a list rather than a building case",
    "Register too informal for the specified audience"
  ],
  "cross_curricular_hooks": [
    "[History] Famous speeches as models (MLK, Churchill, Pankhurst)",
    "[PSHE/RS] Ethical and social issues as speech topics",
    "[Citizenship] Democratic debate and civic engagement"
  ]
}
```

---

## 9. What This Enables That the Universal TopicSuggestion Could Not

### 1. Genre progression queries

```cypher
// Show the narrative trajectory from KS1 to KS4
MATCH (g:Genre {genre_id: 'GEN-NARR'})<-[:IN_GENRE]-(eu:EnglishUnit)
RETURN eu.key_stage, eu.year_groups, eu.name, eu.writing_outcome
ORDER BY eu.key_stage, eu.year_groups
```

With a universal TopicSuggestion, genre is a string property. You cannot trace how "narrative" evolves from Y1 sentence-level retelling to Y10 literary fiction without full-text search on a property. With a Genre node, it is a single relationship traversal.

### 2. Set text filtering by exam board

```cypher
// Find all AQA Shakespeare units
MATCH (eu:EnglishUnit)-[:STUDIES_TEXT]->(st:SetText {exam_board: 'AQA', text_category: 'shakespeare'})
RETURN eu.name, st.name, st.popularity_estimate
```

Impossible with the universal schema. `exam_board_status` as an object array property on the unit cannot be indexed or efficiently queried.

### 3. Grammar sequencing across units

```cypher
// What is the recommended teaching order for Y4 English units based on grammar dependencies?
MATCH path = (eu1:EnglishUnit)-[:GRAMMAR_SEQUENCE_AFTER*]->(eu2:EnglishUnit)
WHERE eu1.key_stage = 'KS2' AND eu1.year_groups = ['Y4']
RETURN [n IN nodes(path) | n.name] AS sequence,
       [r IN relationships(path) | r.grammar_point] AS grammar_points
```

The universal schema has no mechanism for grammar sequencing because grammar is not relevant to History, Geography, or Science.

### 4. Cross-board text comparison

```cypher
// Which texts are available on both AQA and Edexcel?
MATCH (st1:SetText {exam_board: 'AQA'})-[:SAME_TEXT_DIFFERENT_BOARD]-(st2:SetText {exam_board: 'Edexcel'})
RETURN st1.name, st1.text_category
```

### 5. Writing outcome as the lesson generator

```cypher
// Generate a Y4 fiction writing lesson
MATCH (eu:EnglishUnit {key_stage: 'KS2', text_type: 'fiction'})
WHERE 'Y4' IN eu.year_groups
RETURN eu.name, eu.writing_outcome, eu.grammar_focus, eu.text_features_to_teach,
       eu.suggested_texts, eu.reading_level
```

The `writing_outcome` tells the AI exactly what lesson to generate. The universal schema did not have this property.

### 6. Reading skill development tracking

```cypher
// Which units develop inference skills?
MATCH (eu:EnglishUnit)-[:DEVELOPS_SKILL]->(rs:ReadingSkill {strand: 'inference'})
RETURN eu.name, eu.key_stage, rs.skill_name
ORDER BY eu.key_stage
```

English is the only subject with dedicated ReadingSkill epistemic nodes. The universal schema had no relationship to connect topic suggestions to reading skills.

---

## 10. Open Questions

### 1. Should there be a `GrammarPoint` node?

Grammar points (fronted adverbials, expanded noun phrases, direct speech punctuation, relative clauses, etc.) are currently stored as string arrays on `EnglishUnit`. An argument exists for making them nodes:
- Grammar is year-specific and statutory (NC Appendix 2)
- Grammar has its own progression (coordinating conjunctions Y2 -> subordinating conjunctions Y3 -> relative clauses Y5)
- Grammar points are reused across many units
- The `GRAMMAR_SEQUENCE_AFTER` relationship between units is really encoding a relationship between grammar points that happen to be taught in those units

**Counter-argument**: The graph already has 9,000+ nodes. Adding ~60 grammar point nodes with their own progression chain adds complexity for a feature that could be handled by a controlled vocabulary on the `grammar_focus` property. The grammar sequence is already encoded in NC Appendix 2 -- the graph does not need to re-derive it.

**My recommendation**: Do NOT add GrammarPoint nodes in v1. Keep `grammar_focus` as a string array with a controlled vocabulary. If AI lesson generation reveals that grammar sequencing is a major pain point, upgrade to nodes in v2.

### 2. Should `suggested_texts` be a separate `Text` node for KS1-KS3?

Currently, KS1-KS3 texts are stored as structured objects in the `suggested_texts` property, while KS4 texts are separate `SetText` nodes. The asymmetry is intentional: KS1-KS3 texts are suggestions (there is no "right" text for Y4 adventure narrative), while KS4 texts are curricular requirements.

However, some primary texts (The Iron Man, Charlotte's Web, The BFG) appear across multiple units and year groups. A separate `Text` node would deduplicate this data and allow queries like "show all units that use The Iron Man."

**My recommendation**: Do NOT add a primary `Text` node in v1. The duplication is minor (3-4 popular texts appearing in 2-3 units each) and the query need is not critical. If the corpus grows to hundreds of units, reconsider.

### 3. How should phonics-stage reading levels work at KS1?

I proposed `reading_level: "Phase 4-5"` for KS1 units. But phonics phases are a Letters and Sounds / DfE framework, not part of the NC itself. Some schools use book bands (Red, Yellow, Blue, Green, Orange, Turquoise...) instead. The `reading_level` property needs a flexible format that accommodates both.

**My recommendation**: Allow free-text with a format convention: phonics-based (`"Phase 3"`, `"Phase 5"`), book-band-based (`"Book Band: Orange"`), or year-based (`"Y3-Y5"`). Validate at import time that the format matches one of these three patterns.

### 4. How should poetry anthologies be modelled at KS4?

A poetry anthology (e.g. AQA Power and Conflict) contains 15 individual poems. Each poem has its own themes, techniques, and context. The current design has a `SetText` node for the anthology as a whole. But teachers teach individual poems, not the anthology as a unit. Should each poem be a separate node?

**My recommendation**: Model the anthology as a `SetText` node. Model individual poem units as `EnglishUnit` nodes that `STUDIES_TEXT` the anthology. The poem-specific data (themes, techniques, context) belongs on the `EnglishUnit`, not the `SetText`. This avoids 15+ additional nodes per anthology while still allowing poem-level lesson generation.

### 5. What about drama as a cross-curricular concern?

Drama is listed as a separate NC subject at KS3-KS4, but it is also deeply embedded in English (performing Shakespeare, dramatic role play, spoken language). Should `EnglishUnit` nodes reference Drama concepts?

**My recommendation**: Use `cross_curricular_hooks` for now. E.g. `"[Drama] Performance interpretation of key scenes"`. If a Drama layer is built later, add explicit cross-layer relationships.

### 6. Display properties and cross-label querying

All three English nodes (`EnglishUnit`, `Genre`, `SetText`) share `display_category: "English Ontology"`. This allows:

```cypher
MATCH (n) WHERE n.display_category = 'English Ontology' RETURN labels(n), count(n)
```

Should this be `"Topic Suggestion"` for consistency with other subjects? I think not. English's ontology is structurally different, and forcing a shared display_category hides this. But if cross-subject queries need `display_category = 'Topic Suggestion'` to work, we could add a secondary property `display_category_cross_subject: "Topic Suggestion"` without losing the English-specific one.

---

## Appendix A: Genre Controlled Vocabulary

### Primary genres (KS1-KS3)

| genre_id | name | genre_family | conventions |
|---|---|---|---|
| `GEN-NARR` | Narrative | fiction | characters, setting, plot, conflict, resolution, narrator, dialogue |
| `GEN-TRAD` | Traditional Tale | fiction | archetypal characters, moral, repetition, transformation, rule of three |
| `GEN-POET` | Poetry | poetry | rhythm, rhyme, imagery, figurative language, verse structure, voice |
| `GEN-PLAY` | Playscript | drama | stage directions, dialogue, scenes, cast list, dramatic tension |
| `GEN-RECOUNT` | Recount | non_fiction | chronological order, first/third person, time connectives, detail |
| `GEN-REPORT` | Report | non_fiction | subheadings, topic sentences, present tense, formal register, diagrams |
| `GEN-INSTRUCT` | Instruction | non_fiction | imperative verbs, numbered steps, chronological order, diagrams |
| `GEN-EXPLAIN` | Explanation | non_fiction | causal connectives, present tense, technical vocabulary, process description |
| `GEN-PERSUADE` | Persuasion | non_fiction | rhetorical devices, emotive language, logical argument, audience address |
| `GEN-DISCUSS` | Discussion | non_fiction | for/against structure, balanced argument, connectives for contrast, justified conclusion |
| `GEN-INFO` | Information | non_fiction | reference, encyclopaedia, glossary, index, cross-references |

### Secondary genres (KS3-KS4, additional)

| genre_id | name | genre_family | conventions |
|---|---|---|---|
| `GEN-FICT` | Literary Fiction | fiction | narrative voice, characterisation, theme, structure, style |
| `GEN-DRAMA` | Drama | drama | dialogue, stage directions, dramatic irony, soliloquy, theatrical convention |
| `GEN-LITNF` | Literary Non-Fiction | non_fiction | travel writing, memoir, essay, journalism, personal voice |
| `GEN-TRANS` | Transactional | non_fiction | letter, article, speech, review, report (purpose-driven forms) |
| `GEN-CREAT` | Creative Writing | fiction | narrative, descriptive, experimental (exam component) |

### Genre progressions

```
GEN-TRAD (KS1-KS2) --[:PROGRESSES_TO]--> GEN-NARR (KS2-KS3) --[:PROGRESSES_TO]--> GEN-FICT (KS3-KS4)
GEN-RECOUNT (KS1-KS2) --[:PROGRESSES_TO]--> GEN-LITNF (KS3-KS4)
GEN-PERSUADE (KS2) --[:PROGRESSES_TO]--> GEN-TRANS (KS3-KS4)
GEN-DISCUSS (KS2) --[:PROGRESSES_TO]--> GEN-TRANS (KS3-KS4)
GEN-PLAY (KS2-KS3) --[:PROGRESSES_TO]--> GEN-DRAMA (KS3-KS4)
GEN-POET (KS1-KS4) -- continuous, no progression break, but sub-genre expectations increase
```

---

## Appendix B: VehicleTemplate Requirements

The English ontology requires these VehicleTemplates (some existing, some new):

| template_id | name | session_structure | KS | Status |
|---|---|---|---|---|
| VT-07 | `text_study` | shared_reading -> analysis -> vocabulary -> planning -> drafting -> editing -> publishing | KS1-KS3 | EXISTS |
| VT-11 | `discussion_and_debate` | text_stimulus -> pair_discussion -> structured_debate -> reflection -> written_response | KS1-KS4 | EXISTS |
| VT-12 | `creative_response` | stimulus -> exploration -> experimentation -> creation -> sharing -> evaluation | KS1-KS4 | EXISTS |
| VT-23 | `text_study_literature` | introduction -> close_reading -> analysis -> contextualisation -> essay_planning -> essay_writing -> peer_review | KS4 | EXISTS (FINAL-SCHEMA) |
| VT-24 | `writers_workshop` | mini_lesson -> independent_writing -> conferencing -> sharing -> revision | KS1-KS3 | EXISTS (FINAL-SCHEMA) |
| VT-NEW-1 | `grammar_in_context` | text_exploration -> pattern_identification -> rule_articulation -> guided_practice -> independent_application | KS1-KS3 | NEEDED |
| VT-NEW-2 | `reading_for_pleasure` | book_talk -> independent_reading -> reading_journal -> discussion -> recommendation | KS1-KS3 | NEEDED |
| VT-NEW-3 | `spoken_language_performance` | text_selection -> rehearsal -> technique_practice -> performance -> evaluation | KS1-KS4 | NEEDED |
| VT-NEW-4 | `unseen_analysis` | first_reading -> annotation -> structural_analysis -> language_analysis -> comparative_writing | KS4 | NEEDED |

---

## Appendix C: Estimated Node Counts

| Label | Estimated count | Basis |
|---|---|---|
| `Genre` | 16 | 11 primary + 5 secondary (see Appendix A) |
| `EnglishUnit` | ~120-150 | ~8 per year group x 11 years (Y1-Y11) + ~30 KS4 set text units |
| `SetText` | ~60-80 | ~8 Shakespeare x 4 boards (with dedup) + ~9 19th C x 4 + ~11 modern x 4 + ~7 poetry anthologies. Many texts appear on multiple boards but are modelled per board. |
| **Total new nodes** | **~200-250** | Manageable addition to a ~10,000 node graph |

---

## Appendix D: Migration from Existing ContentVehicle Data

The 8 existing English Y4 ContentVehicle nodes (`EN-Y4-CV001` through `EN-Y4-CV008`) map cleanly to `EnglishUnit` nodes:

| ContentVehicle | EnglishUnit | Notes |
|---|---|---|
| EN-Y4-CV001 (Adventure Narrative) | EU-EN-Y4-001 | Direct mapping. All properties transfer. |
| EN-Y4-CV002 (Greek Myths) | EU-EN-Y4-002 | Direct mapping. |
| EN-Y4-CV003 (Persuasive Writing) | EU-EN-Y4-003 | Direct mapping. |
| EN-Y4-CV004 (Poetry) | EU-EN-Y4-004 | Direct mapping. |
| EN-Y4-CV005 (Information Text) | EU-EN-Y4-005 | Direct mapping. |
| EN-Y4-CV006 (Fairy Tales) | EU-EN-Y4-006 | Direct mapping. |
| EN-Y4-CV007 (Spelling) | EU-EN-Y4-007 | `unit_type: "spelling_and_vocabulary"`. |
| EN-Y4-CV008 (Discussion) | EU-EN-Y4-008 | Direct mapping. Template changes from text_study to discussion_and_debate. |

The existing `EnglishTopicSuggestion` data from `english_y4.json` (8 nodes) was derived from these ContentVehicles and maps identically to the `EnglishUnit` schema.

No data loss. No structural incompatibility. The migration is additive: new properties (`unit_type`, `text_features_to_teach`, `spoken_language_outcome`) are added; existing properties are renamed for clarity (`text_features` -> `text_features_to_teach`); the `Genre` and `SetText` nodes are created fresh.
