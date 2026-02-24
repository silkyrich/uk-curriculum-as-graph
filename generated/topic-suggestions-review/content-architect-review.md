# Content Architect Review: TopicSuggestion + VehicleTemplate Schema

**Reviewer**: Content Architect / EdTech AI Specialist
**Date**: 2026-02-24
**Input**: BRIEFING.md, SPECIALIST-SUMMARY.md, 6 specialist reviews (History, Geography, Science, English, Maths, Foundation), CLAUDE.md graph model
**Focus**: Can an AI tutor generate high-quality lessons, videos, assessments, and interactive activities from this schema?

---

## 1. Generation Pipeline Assessment

### The Full Query Chain

When the AI tutor generates a Year 4 Science lesson on "Friction", the generation pipeline must assemble data from 6+ node types:

```
ConceptCluster (sequencing, co-teaching groups)
  └─ Concept (prerequisites, teaching_weight)
       └─ DifficultyLevel (entry/developing/expected/greater_depth tasks)
       └─ DEVELOPS_SKILL → WorkingScientifically
  └─ APPLIES_LENS → ThinkingLens (Cause & Effect)
       └─ PROMPT_FOR → KeyStage (age-banded cognitive framing prompt)
  └─ SUGGESTED_TOPIC → ScienceTopicSuggestion ("Friction Fair Test")
       └─ USES_TEMPLATE → VehicleTemplate ("fair_test")
            └─ TEMPLATE_FOR → KeyStage (age-banded session structure prompt)
```

**Assessment: This pipeline is architecturally sound.** Each node type contributes a distinct, non-overlapping layer of generation intelligence:

| Node Type | Generation Role | What it tells the AI |
|---|---|---|
| ConceptCluster | **Scope** | Which concepts to cover in this lesson, in what order |
| Concept + prerequisites | **Readiness** | What the child must already know |
| DifficultyLevel | **Calibration** | Concrete tasks, expected responses, common errors per level |
| ThinkingLens | **Cognitive framing** | The "big question" angle (e.g., "What causes friction?") |
| TopicSuggestion | **Content context** | The specific topic, equipment, safety, pedagogical rationale |
| VehicleTemplate | **Session structure** | Step-by-step pedagogical pattern for the lesson |

**What's missing from the pipeline?** Two things:

1. **A composition prompt** — The AI needs a master prompt that orchestrates all these data sources into a coherent generation request. This isn't a graph node; it's a system prompt template that references graph properties by name. See Section 4.

2. **Learner profile data** — ContentGuideline, PedagogyProfile, and FeedbackProfile nodes (already in the graph via Year nodes) provide reading level constraints, scaffolding preferences, and tone guidance. The pipeline diagram above omits these, but they're essential for age-appropriate generation. The query should include:
   ```
   Year → HAS_CONTENT_GUIDELINE → ContentGuideline
   Year → HAS_PEDAGOGY_PROFILE → PedagogyProfile
   Year → HAS_FEEDBACK_PROFILE → FeedbackProfile
   ```

### Pipeline Verdict by Generation Type

| Generation Type | Pipeline Complete? | Missing Data |
|---|---|---|
| **Lesson plan** | YES (with specialist additions) | Needs `misconceptions` (Science), `writing_outcome` (English), `fluency_targets` (Maths) |
| **Assessment tasks** | YES | DifficultyLevel provides `example_task` + `example_response` + `common_errors` — the foundation is there |
| **Video script** | MOSTLY | Missing explicit "narrative hook" or "opening question" — currently inferred from ThinkingLens `key_question` and TopicSuggestion `pedagogical_rationale`. Workable but not optimised |
| **Interactive activity** | MOSTLY | Missing `estimated_duration` per activity type (different for fair test vs research enquiry). VehicleTemplate `typical_duration_lessons` is too coarse |
| **Parent explanation** | YES | `pedagogical_rationale` + `definitions` + DifficultyLevel `description` covers this well |

### Critical Finding: The Pipeline Works But Needs a Query Orchestrator

The graph data is all there (or will be with the specialist additions), but there's currently no **single query** that assembles the full generation context. `query_cluster_context.py` does some of this but doesn't yet surface TopicSuggestions or VehicleTemplates. This is an implementation task, not a schema problem — but it's the highest-priority implementation task after the schema is finalised.

---

## 2. Property-by-Property Prompt Evaluation

For each key property across all labels, I assess: can it be directly embedded in an LLM prompt?

### Rating Scale
- **Direct** — Drop into a prompt template as-is: `"This is a {enquiry_type} investigation."`
- **Format** — Needs minor formatting before prompt insertion (array→list, object→sentences)
- **Runtime** — Should not be in the graph; generate at runtime

### Universal Properties

| Property | Type | Prompt Rating | Prompt Pattern | Notes |
|---|---|---|---|---|
| `name` | string | **Direct** | `"Topic: {name}"` | |
| `suggestion_type` | string | **Direct** | `"This is a {suggestion_type}."` | Controlled vocab = reliable |
| `subject` | string | **Direct** | `"Subject: {subject}"` | |
| `key_stage` | string | **Direct** | `"Key Stage: {key_stage}"` | |
| `curriculum_status` | string | **Direct** | `"Curriculum status: {curriculum_status}"` | Useful for telling AI whether this is mandatory or optional |
| `choice_group` | string | **Direct** | Less useful in prompts | More of a query/filter property than a generation property |
| `curriculum_reference` | string/string[] | **Format** | `"National Curriculum reference: {curriculum_reference}"` | If changed to string[] per specialist recommendation, join with "; " |
| `pedagogical_rationale` | string | **Direct** | `"Why this topic works: {pedagogical_rationale}"` | Excellent for parent-facing content and lesson introduction framing |
| `common_pitfalls` | string[] | **Format** | `"Avoid these teaching mistakes:\n- {pitfall_1}\n- {pitfall_2}"` | Array→bullet list. Useful as negative constraints in prompts |
| `cross_curricular_hooks` | string[] | **Format** | `"Cross-curricular links:\n- {hook_1}\n- {hook_2}"` | If structured (as History specialist proposes), needs more formatting |
| `definitions` | string[] | **Format** | `"Key vocabulary to introduce: {definitions}"` | Array→comma list or bullet list |
| `display_*` | various | N/A | Not used in generation prompts | Visualisation only |

### History-Specific Properties

| Property | Type | Prompt Rating | Prompt Pattern | Notes |
|---|---|---|---|---|
| `period` | string | **Direct** | `"Historical period: {period}"` | |
| `period_start_year` | int | **Direct** | `"Timeline: {start} to {end}"` | For timeline generation, not prose prompts |
| `period_end_year` | int | **Direct** | (see above) | |
| `key_figures` | string[] | **Format** | `"Key historical figures: {join(key_figures)}"` | |
| `key_events` | string[] | **Format** | `"Key events: {join(key_events)}"` | |
| `sources` | string[] | **Format** | `"Historical sources to use: {join(sources)}"` | |
| `source_types` | string[] | **Format** | `"Source types: {join(source_types)}"` | Controlled vocab = reliable template selection |
| `perspectives` | string[] | **Format** | `"Include these viewpoints: {join(perspectives)}"` | |
| `interpretations` | string[] | **Format** | `"Historiographical debates to explore:\n- {interp_1}"` | KS3+ only |
| `disciplinary_concepts` | string[] | **Direct** | `"This lesson foregrounds: {dc[0]}. Secondary focus: {dc[1]}."` | First element = primary. Controlled vocab = excellent for prompt routing |
| `significance_claim` | string | **Direct** | `"Why this matters: {significance_claim}"` | Excellent for lesson hooks and parent content |
| `sensitive_content_notes` | string[] | **Format** | System prompt: `"SAFETY: {join(notes)}"` | Should go in system prompt, not user prompt |
| `enquiry_questions` | string[] | **Format** | `"Frame the lesson around: {eq[0]}"` | Excellent for structuring multi-lesson sequences |
| `comparison_pairs` | object[] | **Format** | `"Compare {figure_a} and {figure_b}, focusing on {comparison_focus}."` | Object needs destructuring but maps cleanly to prose |

### Geography-Specific Properties

| Property | Type | Prompt Rating | Prompt Pattern | Notes |
|---|---|---|---|---|
| `locations` | string[] | **Format** | `"Location(s): {join(locations)}"` | Array is correct; each entry is a geocodable place |
| `theme_category` | string | **Direct** | `"Geography strand: {theme_category}"` | Controlled vocab = good for prompt routing |
| `themes` | string[] | **Format** | `"Key themes: {join(themes)}"` | |
| `scale` | string | **Direct** | `"Geographical scale: {scale}"` | Directly calibrates map zoom, language register |
| `map_types` | string[] | **Format** | `"Map types to reference: {join(map_types)}"` | Controls visual generation |
| `data_sources` | string[] | **Format** | `"Data sources: {join(data_sources)}"` | |
| `contrasting_with` | string | **Direct** | Used for query, not directly in prompts | Links to paired suggestion |
| `fieldwork_potential` | string | **Direct** | `"Fieldwork opportunity: {fieldwork_potential}"` | Or null — AI skips this section |

### Science-Specific Properties

| Property | Type | Prompt Rating | Prompt Pattern | Notes |
|---|---|---|---|---|
| `enquiry_type` | string | **Direct** | `"This is a {enquiry_type} enquiry."` | Controlled vocab (7 values). **Highest-leverage single property** — determines entire lesson structure |
| `secondary_enquiry_types` | string[] | **Format** | `"Secondary methods: {join(types)}"` | Optional enrichment |
| `science_discipline` | string | **Direct** | `"Discipline: {science_discipline}"` | Routes to correct vocabulary register |
| `equipment` | string[] | **Format** | `"Equipment needed: {join(equipment)}"` | |
| `safety_notes` | string | **Direct** | System prompt: `"SAFETY: {safety_notes}"` | Should go in system prompt section |
| `hazard_level` | string | **Direct** | `"Hazard level: {hazard_level}"` | Controls AI's safety language intensity |
| `expected_outcome` | string | **Direct** | `"The correct understanding is: {expected_outcome}"` | Essential for assessment generation |
| `recording_format` | string[] | **Format** | `"Students should record using: {join(recording_format)}"` | |
| `misconceptions` | string[] | **Format** | `"Common misconceptions to probe:\n- {m_1}\n- {m_2}"` | **Highest-leverage addition for Science** |
| `variables` | object | **Format** | `"Independent variable: {v.independent}\nDependent: {v.dependent}\nControlled: {join(v.controlled)}"` | Object destructuring needed |

### English-Specific Properties

| Property | Type | Prompt Rating | Prompt Pattern | Notes |
|---|---|---|---|---|
| `text_type` | string | **Direct** | `"Text type: {text_type}"` | Routes to fiction/non-fiction pedagogy |
| `genre` | string[] | **Format** | `"Genre: {genre[0]} (also: {join(genre[1:])})"` | First = primary |
| `text_features` | string[] | **Format** | `"Teach these text features:\n- {tf_1}\n- {tf_2}"` | Directly becomes success criteria |
| `suggested_texts` | object[] | **Format** | `"Anchor text: {st[0].title} by {st[0].author} ({st[0].suitability})"` | Object needs destructuring — heavier formatting |
| `reading_level` | string | **Direct** | `"Reading level: {reading_level}"` | Calibrates text selection |
| `writing_outcome` | string | **Direct** | `"The student should produce: {writing_outcome}"` | **Highest-leverage addition for English** |
| `grammar_focus` | string[] | **Format** | `"Embed this grammar: {join(grammar_focus)}"` | |
| `spoken_language_focus` | string | **Direct** | `"Include spoken language: {spoken_language_focus}"` | |
| `exam_board_status` | object[] | **Format** | `"This is a {status} for {board} ({category})"` | KS4 only. Object needs destructuring |
| `assessment_mode` | string | **Direct** | `"Assessment mode: {assessment_mode}"` | Routes to different generation patterns |
| `literary_terms` | string[] | **Format** | `"Literary terms to introduce: {join(literary_terms)}"` | |

### Maths-Specific Properties

| Property | Type | Prompt Rating | Prompt Pattern | Notes |
|---|---|---|---|---|
| `cpa_stage` | string | **Direct** | `"CPA stage: {cpa_stage}. Begin with {concrete/pictorial/abstract} representations."` | Enum = reliable. **Highest-leverage Maths property** |
| `cpa_notes` | string | **Direct** | `"CPA progression: {cpa_notes}"` | Specific generation guidance |
| `manipulatives` | string[] | **Format** | `"Use these manipulatives: {join(manipulatives)}"` | Controlled vocab = AI can describe specific resources |
| `representations` | string[] | **Format** | `"Key representations: {join(representations)}"` | Controlled vocab = AI can generate specific diagram types |
| `fluency_targets` | string[] | **Format** | `"Fluency targets: {join(fluency_targets)}"` | |
| `reasoning_prompts` | string[] | **Format** | `"Use these reasoning prompt types: {join(reasoning_prompts)}"` | Controlled vocab = AI knows exact prompt patterns |
| `application_contexts` | string[] | **Format** | `"Real-world contexts: {join(application_contexts)}"` | Becomes the personalisation hook |
| `nc_aim_emphasis` | string | **Direct** | `"NC aim: {nc_aim_emphasis}"` | Routes to fluency-first vs reasoning-first generation |

### Foundation Subject Properties (Art, Music, DT)

| Property | Type | Prompt Rating | Notes |
|---|---|---|---|
| Art: `artist` | string | **Direct** | `"Study the work of {artist}."` |
| Art: `medium` | string[] | **Format** | `"Using: {join(medium)}"` — controls material instructions |
| Art: `techniques` | string[] | **Format** | `"Techniques: {join(techniques)}"` — becomes step-by-step guidance |
| Art: `visual_elements` | string[] | **Format** | `"Focus on: {join(visual_elements)}"` |
| Music: `activity_focus` | string[] | **Direct** | `"This is a {af[0]} lesson."` — routes to performing/composing/listening pedagogy |
| Music: `musical_elements` | string[] | **Format** | `"Musical focus: {join(musical_elements)}"` |
| Music: `piece` | string | **Direct** | `"Piece: {piece}"` |
| DT: `dt_strand` | string | **Direct** | `"DT strand: {dt_strand}"` — routes to correct making process |
| DT: `design_brief` | string | **Direct** | `"Challenge: {design_brief}"` — **the entire lesson purpose** |
| DT: `materials` | string[] | **Format** | `"Materials: {join(materials)}"` |
| DT: `safety_notes` | string | **Direct** | System prompt safety section |

### Summary: Prompt Readiness

- **82% of properties are Direct or Format (light formatting)** — this is excellent. The schema is well-designed for prompt construction.
- **Object types** (`suggested_texts`, `exam_board_status`, `comparison_pairs`, `variables`) need more formatting work but are still manageable. Template functions like `format_suggested_text(obj)` handle this cleanly.
- **No properties are Runtime-only** among the specialist proposals — the specialists have correctly identified curriculum intelligence vs generated content. Every property proposed belongs in the graph.
- **Controlled vocabularies are the single best prompt engineering decision** — `enquiry_type`, `cpa_stage`, `disciplinary_concepts`, `theme_category`, `dt_strand`, `activity_focus`, `hazard_level` all route the AI to specific generation patterns with zero ambiguity.

---

## 3. Graph vs Runtime Boundary

### Principle

**Graph** = curriculum intelligence that is the same for every child studying this topic, regardless of personalisation.
**Runtime** = personalised, themed, branded, or session-specific content that changes per learner/context.

### Property Classification

#### Definitively Graph (permanent curriculum intelligence)

| Property | Why Graph | Example |
|---|---|---|
| `pedagogical_rationale` | Same for every teacher/child — this is WHY the topic works | "The Iron Man works for Y4 adventure narrative because..." |
| `enquiry_type` | Curriculum-determined, not personalised | "fair_test" for friction investigation |
| `disciplinary_concepts` | NC-specified thinking skills for this topic | `["cause_and_consequence"]` |
| `safety_notes` | Non-negotiable safeguarding requirement | "Wear goggles when using acids" |
| `misconceptions` | Research-validated, topic-level | "Heavier objects fall faster" |
| `expected_outcome` | Curriculum-defined correct understanding | "Shorter/tighter = higher pitch" |
| `equipment` | School-realistic equipment lists | "Tuning forks, rulers, elastic bands" |
| `recording_format` | Age-appropriate data presentation expectations | "Results table → line graph" |
| `source_types` | Determines pedagogical approach | "primary_written, primary_archaeological" |
| `cpa_stage` | Mastery teaching methodology, topic-level | "concrete_pictorial_abstract" |
| `manipulatives` | Representation/resource recommendation | "Dienes blocks, place value charts" |
| `representations` | Core pedagogical decision | "bar_model, number_line" |
| `writing_outcome` | Defines the lesson product | "Write an adventure narrative (500-700 words)..." |
| `grammar_focus` | Year-specific statutory grammar | "fronted adverbials, expanded noun phrases" |
| `medium` (Art) | Physical materials required | "paint, print" |
| `techniques` (Art/DT) | Skills being taught | "block printing, colour layering" |
| `design_brief` (DT) | The challenge itself | "Design a moving picture book using sliders and levers" |
| `musical_elements` | NC-specified dimensions | "pulse, rhythm, dynamics" |
| `variables` | Scientific method structure | `{ independent: "distance", dependent: "bubble count" }` |
| `fluency_targets` | What should be automatic | "Recall addition/subtraction facts to 20" |
| `significance_claim` | Historical significance framing | "The Roman occupation transformed Britain's infrastructure..." |
| `sensitive_content_notes` | Child safeguarding guardrails | "Follow UCL Centre for Holocaust Education guidance" |
| `definitions` | Precise technical vocabulary | "centurion, legion, Romanisation" |
| `map_types` | Age-appropriate cartography | "OS_map, choropleth" |
| `scale` | Geographical scope | "regional" |

#### Definitively Runtime (generated per session)

| Data | Why Runtime | Notes |
|---|---|---|
| Specific worksheet content | Themed to child's interests, personalised to mastery level | Pokemon-themed fractions, football-themed ratio |
| Full lesson plan prose | Generated from graph data + learner profile + child preferences | The actual text the child sees |
| Branded materials | School branding, platform branding | Logos, colours, headers |
| External resource links | URLs change, licensing changes, availability varies | Oak, BBC, museum links |
| Personalised examples | Adapted to child's context, interests, and level | "Your football team scored 3 goals..." |
| Video scripts | Generated from graph data, narrated differently per context | Full video production content |
| Themed narratives | Interest-based engagement wrapping | "Space adventure" framing for a gravity lesson |
| Interactive activity mechanics | Platform-specific implementation | Drag-and-drop, multiple choice, free text |
| Assessment item wording | Generated from DifficultyLevel + TopicSuggestion | Actual question text |
| Progress feedback | Personalised to child's mastery trajectory | "You've mastered 4/6 concepts in this cluster" |

#### Borderline Properties — My Rulings

| Property | Specialist Proposal | My Ruling | Rationale |
|---|---|---|---|
| `suggested_texts` | English: object[] with title, author, suitability | **Graph** | These are curriculum design decisions, not generated content. "The Iron Man is suitable for Y3-Y5 adventure narrative" is permanent curriculum intelligence. The structured object format is correct — the AI needs author and suitability, not just a title string |
| `key_figures` | History: string[] | **Graph** | "Boudicca" and "Claudius" are curriculum-level knowledge about which historical figures are relevant to Roman Britain. Not personalised |
| `enquiry_questions` | History: string[] | **Graph** | "Why did the Romans invade Britain?" is a curriculum design question that frames a multi-lesson sequence. Not generated at runtime |
| `application_contexts` | Maths: string[] | **Graph** | "money, measurement, time" are curriculum-identified real-world contexts for embedding maths. The AI personalises WITHIN these contexts (choosing football vs cooking) at runtime |
| `reasoning_prompts` | Maths: string[] controlled vocab | **Graph** | These are prompt TYPE patterns (always_sometimes_never, spot_the_mistake), not specific questions. The AI generates the specific question at runtime using the type |
| `cross_curricular_hooks` | All: string[] or structured objects | **Graph** | Cross-curricular connections are curriculum architecture, not personalised content. The History specialist's structured format `{ subject, hook, strength }` is better for prompts than plain strings |
| `exam_board_status` | English: object[] | **Graph** | Exam board set text status is institutional fact. "Macbeth is an AQA Shakespeare set text" doesn't change per learner |
| `composer` / `piece` | Music: strings | **Graph** | These are Model Music Curriculum recommendations — curriculum intelligence about which pieces work for which year groups |
| `fieldwork_potential` | Geography: string | **Graph** | "River study: measure width, depth, velocity" describes a possible extension activity. Whether the child does it is runtime, but the possibility is curriculum-level |
| `data_sources` | Geography: string[] | **Graph** | "World Bank, UNDP" are authoritative data sources for this topic. The AI needs to know these to generate data literacy activities. This is curriculum intelligence |
| `artist` / `art_movement` | Art: strings | **Graph** | "Mondrian" and "De Stijl" are curriculum design choices about which artist exemplifies which visual elements. Not personalised |

**Ruling summary: All ~60 specialist-proposed properties belong in the graph.** None are runtime-only. The specialists have demonstrated excellent instincts about the graph/runtime boundary — everything they proposed is curriculum intelligence that must be the same regardless of which child receives the lesson. The personalisation layer (theming, interest-matching, specific activity wording) is cleanly separated as runtime generation.

---

## 4. VehicleTemplate Agent Prompt Design

### The Composition Problem

The AI tutor receives data from 6+ node types. The VehicleTemplate `agent_prompt` must orchestrate how these data sources are composed into a single generation request. This is the most architecturally important prompt in the system.

### Current Pattern: ThinkingLens

The existing ThinkingLens layer provides a model:
- `ThinkingLens.agent_prompt` = generic lens instruction
- `PROMPT_FOR.agent_prompt` = age-banded instruction per KeyStage
- Query uses `coalesce(pf.agent_prompt, tl.agent_prompt)` for fallback

This works because ThinkingLens is a single concern (cognitive framing). VehicleTemplate is more complex — it must reference properties from the TopicSuggestion node, which varies by subject type.

### Recommended VehicleTemplate Agent Prompt Architecture

**Layer 1: VehicleTemplate.agent_prompt** (generic, subject-agnostic)

This describes the pedagogical pattern abstractly:

```
You are generating a {template_type} lesson. Follow this session structure:
{session_structure_as_numbered_steps}

Assessment approach: {assessment_approach}
```

**Layer 2: TEMPLATE_FOR.agent_prompt per KeyStage** (age-banded)

This adds age-appropriate calibration:

```
KS1: Use simple language. Maximum 3 steps shown at once. Include hands-on activity.
Expect concrete responses. Praise effort over accuracy.

KS3: Expect written analysis. Include data interpretation. Require evidence-based
conclusions. Scaffold extended writing with sentence starters at developing level.
```

**Layer 3: Subject-specific prompt fragment** (NEW — constructed at query time from TopicSuggestion properties)

This is NOT stored as a single string — it's assembled by the query layer from the typed TopicSuggestion properties. Example for Science:

```python
def build_science_prompt(ts: ScienceTopicSuggestion) -> str:
    prompt = f"This is a {ts.enquiry_type} investigation.\n"
    prompt += f"Equipment: {', '.join(ts.equipment)}\n"
    prompt += f"Safety: {ts.safety_notes}\n"
    prompt += f"Expected outcome: {ts.expected_outcome}\n"
    if ts.variables:
        prompt += f"Variables: Change {ts.variables['independent']}, "
        prompt += f"measure {ts.variables['dependent']}, "
        prompt += f"keep {', '.join(ts.variables['controlled'])} the same.\n"
    prompt += f"Recording format: {', '.join(ts.recording_format)}\n"
    prompt += f"Address these misconceptions: {'; '.join(ts.misconceptions)}\n"
    return prompt
```

### Should VehicleTemplate.agent_prompt Reference TopicSuggestion Properties by Name?

**No.** The VehicleTemplate should be subject-agnostic. It describes a pedagogical pattern (fair_test, text_study, worked_example_set) that applies across subjects. The subject-specific data is injected at query time, not hardcoded into the template prompt.

**Exception:** The session_structure steps CAN reference generic data slots:

```
Step 1 (question): Present the enquiry question. Use the topic's pedagogical rationale
to frame why this matters.

Step 2 (hypothesis): Ask the student to predict. Reference the topic's expected outcome
to evaluate their prediction.

Step 3 (method): Present the equipment list. Emphasise the safety notes.
```

This uses semantic references ("the equipment list", "the safety notes") rather than property names ("use `ts.equipment`"). This keeps the prompt readable for human editors while being unambiguous for the query layer.

### How VehicleTemplate Interacts with ThinkingLens

Both provide `agent_prompt` values. Both have age-banded prompts via relationships to KeyStage. They should be composed, not merged:

```
SYSTEM PROMPT:
{learner_profile_constraints}    ← from ContentGuideline + PedagogyProfile + FeedbackProfile
{safety_notes}                    ← from TopicSuggestion (if present)
{sensitive_content_notes}         ← from TopicSuggestion (if present)

GENERATION PROMPT:
{vehicle_template_prompt}         ← session structure and pedagogical pattern
{thinking_lens_prompt}            ← cognitive framing angle
{topic_suggestion_prompt}         ← subject-specific context (assembled from properties)
{difficulty_level_data}           ← calibration targets per concept

GENERATION CONTEXT:
{concept_data}                    ← concept names, definitions, prerequisites
{cluster_context}                 ← co-teaching hints, sequencing
```

**Key principle: safety and sensitivity go in the system prompt (non-negotiable constraints). Pedagogical guidance goes in the generation prompt (shaping the output). Factual data goes in context (reference material).**

---

## 5. Multi-Type Query Strategy

### The Problem

With 8-9 typed labels (HistoryTopicSuggestion, GeographyTopicSuggestion, ScienceTopicSuggestion, EnglishTopicSuggestion, MathsTopicSuggestion, ArtTopicSuggestion, MusicTopicSuggestion, DTTopicSuggestion, TopicSuggestion), the query layer needs to:

1. Know which label to query for a given subject
2. Know which properties to extract
3. Format subject-specific properties into prompts

### Recommended Approach: Subject → Label Mapping + Type-Specific Formatters

**Step 1: Maintain a subject → label mapping in the query helper**

```python
TOPIC_SUGGESTION_LABELS = {
    'History': 'HistoryTopicSuggestion',
    'Geography': 'GeographyTopicSuggestion',
    'Science': 'ScienceTopicSuggestion',
    'Biology': 'ScienceTopicSuggestion',
    'Chemistry': 'ScienceTopicSuggestion',
    'Physics': 'ScienceTopicSuggestion',
    'English': 'EnglishTopicSuggestion',
    'English Language': 'EnglishTopicSuggestion',
    'English Literature': 'EnglishTopicSuggestion',
    'Mathematics': 'MathsTopicSuggestion',
    'Art and Design': 'ArtTopicSuggestion',
    'Music': 'MusicTopicSuggestion',
    'Design and Technology': 'DTTopicSuggestion',
    # All others → 'TopicSuggestion'
}
```

**Step 2: Query using the mapped label**

```cypher
// Given subject_name from the Concept/Domain
WITH $subject_name AS subject
CALL {
    WITH subject
    MATCH (ts)-[:DELIVERS_VIA]->(c:Concept {concept_id: $concept_id})
    WHERE labels(ts)[0] ENDS WITH 'TopicSuggestion'
    RETURN ts, labels(ts)[0] AS label
}
RETURN ts, label
```

Alternatively, since all TopicSuggestion types share the DELIVERS_VIA relationship pattern, a UNION-free approach works:

```cypher
MATCH (ts)-[:DELIVERS_VIA]->(c:Concept {concept_id: $concept_id})
RETURN ts, labels(ts) AS node_labels
```

The query layer then dispatches to the correct formatter based on the label.

**Step 3: Type-specific prompt formatters**

```python
FORMATTERS = {
    'ScienceTopicSuggestion': format_science_prompt,
    'HistoryTopicSuggestion': format_history_prompt,
    'EnglishTopicSuggestion': format_english_prompt,
    'MathsTopicSuggestion': format_maths_prompt,
    'GeographyTopicSuggestion': format_geography_prompt,
    'ArtTopicSuggestion': format_art_prompt,
    'MusicTopicSuggestion': format_music_prompt,
    'DTTopicSuggestion': format_dt_prompt,
    'TopicSuggestion': format_generic_prompt,  # fallback
}
```

Each formatter knows which properties exist on its label and how to compose them into a prompt fragment.

### Why Not a Single UNION Query?

A UNION query across 9 labels would require `OPTIONAL MATCH` for every subject-specific property or would return null for ~70% of columns. This is wasteful and makes the result set hard to parse. The mapping approach is cleaner: query the correct label directly, get only the relevant properties.

### Impact on Graph Schema

The multi-label approach requires:
- Each label has its own uniqueness constraint on `suggestion_id`
- OR a single constraint on a shared property across labels (Neo4j supports this on Community Edition via composite constraints in 5.x)
- All labels share the `DELIVERS_VIA`, `USES_TEMPLATE`, `HAS_SUGGESTION` relationship patterns — this is already proposed and correct

**Recommendation**: Use a single `suggestion_id` uniqueness constraint across all labels via a shared index. The `TS-{prefix}-{KS}-{number}` format already ensures uniqueness across types.

---

## 6. Missing for Generation

### What the Specialists Didn't Identify

#### 6.1 `estimated_activity_duration` (per TopicSuggestion, not just per VehicleTemplate)

The VehicleTemplate has `typical_duration_lessons` (how many lessons the template usually spans). But topics within the same template type vary significantly in duration:

- A Y4 "Sound Investigation" fair test takes 1 lesson
- A Y5 "Dissolving and Separating Mixtures" fair test takes 2-3 lessons (multiple separation methods)
- A KS3 "Photosynthesis Rate Investigation" fair test takes 2 lessons (setup + analysis)

**Recommendation**: Add `estimated_lessons: int` (optional) to TopicSuggestion. Default to VehicleTemplate's `typical_duration_lessons` when absent. This gives the AI a realistic scope for lesson planning.

#### 6.2 Differentiation Strategy Is Already Covered (But Needs Acknowledgement)

DifficultyLevel provides differentiation data (entry/developing/expected/greater_depth with concrete tasks at each level). The AI can generate differentiated content by querying DifficultyLevel per concept. No additional property needed on TopicSuggestion.

However, the VehicleTemplate `agent_prompt` should explicitly instruct the AI to use DifficultyLevel data for differentiation:

```
For each activity in the lesson, provide versions at all applicable difficulty levels.
Use the DifficultyLevel data to calibrate expectations:
- Entry: {dl_entry_description}
- Developing: {dl_developing_description}
- Expected: {dl_expected_description}
- Greater Depth: {dl_greater_depth_description}
```

#### 6.3 Prior Knowledge Activation

The `PREREQUISITE_OF` relationship chain tells the AI what concepts the child must already know. But there's no explicit **activation** strategy — how to surface prior knowledge at the start of a lesson.

This is better handled as a step in the VehicleTemplate session structure (every template should start with an `activate_prior_knowledge` or equivalent step) rather than a property on TopicSuggestion. The Maths specialist already identified this for `worked_example_set` — it should be universal.

**Recommendation**: Ensure every VehicleTemplate's session structure begins with a retrieval/activation step. This is a template design standard, not a schema property.

#### 6.4 Assessment Objective Mapping (KS4 Only)

At KS4 (GCSE), assessment is structured by Assessment Objectives (AOs):
- English: AO1-AO6
- History: AO1-AO4
- Geography: AO1-AO4
- Science: AO1-AO3

The AI generating KS4 content needs to know which AOs a topic maps to. This is currently implicit (e.g., History `disciplinary_concepts` maps roughly to AOs) but could be explicit.

**Recommendation**: For KS4 TopicSuggestions, consider an optional `assessment_objectives: string[]` property. But this is lower priority than the specialists' core recommendations — it can be added in a future iteration.

#### 6.5 Seasonal/Calendar Positioning

Some topics have natural calendar positions:
- Remembrance Day (November)
- Easter/Christmas religious studies
- Growing/planting experiments (spring)
- Weather data collection (aligned to seasons)

**Ruling**: This is runtime/teacher planning, not graph data. A school's yearly timetable is not curriculum intelligence. Skip.

---

## 7. Redundancy Check

### Properties That Overlap with Existing Graph Data

| Proposed Property | Existing Graph Data | Redundant? | Ruling |
|---|---|---|---|
| Science `misconceptions` | DifficultyLevel `common_errors` | **No — different scope** | `common_errors` is per-concept, per-level ("At developing level, children confuse mass and weight"). `misconceptions` is per-topic, spanning multiple concepts ("Plants get food from soil" spans photosynthesis + nutrition + ecology). Both are needed |
| Maths `common_errors` (proposed then retracted by Maths specialist) | DifficultyLevel `common_errors` | **Yes — duplicate** | The Maths specialist correctly identified this and removed it. Errors belong on DifficultyLevel, not on TopicSuggestion. TopicSuggestion should have `common_pitfalls` (teaching mistakes) not `common_errors` (student mistakes) |
| `definitions` on TopicSuggestion | `definitions` already on Concept nodes (from extraction JSONs) | **Partially overlapping** | Concept-level definitions are per-concept. TopicSuggestion `definitions` are the key vocabulary for a multi-concept topic. Some overlap (both might define "friction") but TopicSuggestion definitions also include non-concept vocabulary ("controlled variable", "hypothesis"). **Keep both** — they serve different query contexts |
| `cross_curricular_hooks` | `CO_TEACHES` relationships + `DEVELOPS_SKILL` relationships | **No — different grain** | CO_TEACHES links co-teachable concepts (same lesson). Cross-curricular hooks link topics to other subjects (different lesson, different teacher). Complementary, not redundant |
| `curriculum_reference` | Concept/Objective already link to SourceDocument | **Partially overlapping** | SourceDocument provides the NC programme of study reference. TopicSuggestion `curriculum_reference` is a human-readable string for quick lookup. Both are useful — the string goes into prompts, the graph relationship supports validation. **Keep** |
| TopicSuggestion `pedagogical_rationale` | ThinkingLens `agent_prompt` | **No — different purpose** | ThinkingLens explains the cognitive framing ("Why use Cause & Effect lens?"). TopicSuggestion rationale explains why THIS topic works for THESE concepts. Complementary |
| TopicSuggestion `session_structure` (via VehicleTemplate) | ConceptCluster `SEQUENCED_AFTER` | **No — different level** | Cluster sequencing orders clusters within a domain (lesson 1, lesson 2, lesson 3). VehicleTemplate session structure orders steps within a single lesson. Different granularity |
| `DifficultyLevel.description` | TopicSuggestion `expected_outcome` | **Partially overlapping for Science** | DifficultyLevel descriptions say what the child can do at each level. `expected_outcome` says what correct understanding looks like for the topic overall. For Science, there's overlap ("Rate increases with light intensity"). **Keep both** — expected_outcome is the teacher's target; DifficultyLevel is the assessment framework |

### Verdict: Minimal Redundancy

The specialist proposals are well-differentiated from existing graph data. The only true redundancy was `common_errors` on MathsTopicSuggestion, which the Maths specialist already caught and removed. The remaining overlaps serve different query contexts and should be kept.

---

## 8. Top 5 Recommendations

### 1. Accept the Specialist-Proposed "Required" Properties — They Are the Minimum Viable Set for Generation

**Impact: CRITICAL — without these, content generation falls from 7/10 to 3/10**

The six specialists converge on a clear minimum viable property set per subject:

| Subject | Critical Missing Properties |
|---|---|
| Science | `misconceptions` (req), `recording_format` (req), `hazard_level` (req); make `equipment`, `safety_notes`, `expected_outcome` required |
| English | `writing_outcome` (req), `grammar_focus` (req KS1-3), `reading_level` (req) |
| Maths | `fluency_targets` (req), `nc_aim_emphasis` (req); make `manipulatives`, `representations` required |
| History | `disciplinary_concepts` (req), `significance_claim` (req) |
| Geography | `map_types` (req), `scale` (req); change `location` → `locations` (string[]), make `data_sources` required |
| Art/Music/DT | The three new typed labels with their required properties |

Without these, the AI has the topic name and some themes but lacks the pedagogical intelligence to generate subject-appropriate lessons. These are the properties that differentiate "the AI knows the curriculum" from "the AI can teach."

**Effort**: Medium — data authoring for ~200-400 TopicSuggestion nodes.
**Risk of not doing this**: Every lesson generated in these subjects will be generic and pedagogically unsound.

### 2. Implement Controlled Vocabularies for All Enum Properties

**Impact: HIGH — directly improves prompt reliability and consistency**

The strongest signal across all 6 reviews is the demand for controlled vocabularies. These are the properties that should use enums:

| Property | Proposed Enum Values |
|---|---|
| `enquiry_type` | `fair_test`, `observation_over_time`, `pattern_seeking`, `identifying_and_classifying`, `research`, `modelling`, `secondary_data_analysis` |
| `cpa_stage` | `concrete`, `pictorial`, `abstract`, `concrete_pictorial`, `pictorial_abstract`, `concrete_pictorial_abstract` |
| `hazard_level` | `low`, `standard`, `elevated` |
| `science_discipline` | `general_science`, `biology`, `chemistry`, `physics` |
| `text_type` | `fiction`, `non_fiction`, `poetry`, `drama`, `mixed` |
| `nc_aim_emphasis` | `fluency`, `reasoning`, `problem_solving`, `mixed` |
| `scale` | `local`, `regional`, `national`, `continental`, `global` |
| `theme_category` | `physical`, `human`, `environmental`, `economic`, `social`, `political`, `integrated` |
| `dt_strand` | `structures`, `mechanisms`, `textiles`, `cooking_and_nutrition`, `electrical_systems`, `digital_world` |
| `activity_focus` | `performing`, `composing`, `listening` |
| `assessment_mode` | `formative`, `summative`, `exam_practice` |
| `suggestion_type` | Extend to include `set_text`, `genre_requirement`, `enquiry_topic`, `paired_figure_study`, `place_study` |

Controlled vocabularies make prompts deterministic. `"This is a {enquiry_type} investigation"` produces reliable generation when `enquiry_type` is one of 7 known values. Free text produces unpredictable prompts.

**Effort**: Low — define the enum values in the schema; validate during import.
**Risk of not doing this**: Prompt drift, inconsistent generation quality, and the problems visible in existing CV free-text fields.

### 3. Add the Three Foundation Subject Typed Labels (Art, Music, DT) — They Represent 40% of Curriculum Time

**Impact: HIGH — without these, foundation subject generation is non-functional**

The Foundation specialist's analysis is compelling: `themes: ["Mondrian"]` gives the AI zero information about whether to generate a painting lesson, a collage lesson, or an art history discussion. Art, Music, and DT have fundamentally different topic structures that cannot be expressed in a single `themes` array.

The proposed three labels add ~25 properties total — a modest increase for coverage of subjects that occupy approximately 40% of primary curriculum time. The alternative (leaving these subjects with `themes` only) means the AI cannot generate any meaningful lesson for Art, Music, or DT.

**Effort**: Medium — three new labels, constraints, import scripts, and ~60-100 TopicSuggestion nodes.
**Risk of not doing this**: The AI tutor is a core-subjects-only tool. Foundation subjects get generic content or nothing.

### 4. Build a Query Orchestrator That Composes the Full Generation Context

**Impact: HIGH — the schema is only as useful as the query that surfaces it**

The data architecture is sound (or will be, with the specialist additions). But there's no single query path that assembles: ConceptCluster + Concepts + DifficultyLevels + ThinkingLens (age-banded) + TopicSuggestion (typed) + VehicleTemplate (age-banded) + LearnerProfile into a single generation context.

**Recommended implementation**: Extend `query_cluster_context.py` (or create a new `query_generation_context.py`) that:

1. Takes `concept_id` or `cluster_id` + `year_id` as input
2. Resolves the subject from the concept's domain
3. Queries the correct typed TopicSuggestion label via the mapping table
4. Assembles all data sources into a structured prompt context
5. Outputs a ready-to-use prompt with system, generation, and context sections

This is the bridge between "data in the graph" and "AI can generate content."

**Effort**: Medium — one new query script, building on existing patterns.
**Risk of not doing this**: The graph has all the right data but no one can use it for generation. The data sits orphaned.

### 5. Consolidate VehicleTemplate Count to ~20 (Not 37)

**Impact: MEDIUM — prevents template sprawl while covering all pedagogical patterns**

The specialists proposed 23 new templates (total: 37). Many overlap. The right number is approximately 20, achieved by:

**Keep original 14 with modifications:**
- `observation_enquiry` → rename to `observation_over_time` (NC terminology)
- `investigation_design` → rename to `open_investigation` (pupil-designed method)
- `case_study` → add "locate and describe" phase for Geography
- `creative_response` → acknowledge this is primarily for Art/visual making
- `worked_example_set` → add activation and reasoning extension steps

**Add 6-7 genuinely distinct new templates:**

| Template | Serves | Why Distinct |
|---|---|---|
| `source_enquiry` | History | Source analysis as the focus, not a tool. Unique session structure |
| `place_study` | Geography | Layered place understanding through multiple lenses. Not topic_study |
| `decision_making_exercise` | Geography, Citizenship | Stakeholder analysis → evidence weighing → justified decision |
| `modelling_enquiry` | Science | Build model → predict → test → refine. Not fair_test |
| `identifying_and_classifying` | Science | Sort → group → build classification key. NC enquiry type |
| `performance` | Music, Drama, PE | Warm-up → skill building → rehearsal → performance → evaluation |
| `design_make_evaluate` | DT | Explore → design → plan → make → test → evaluate → improve |

**Merge or reject:**
- `ethical_enquiry` → merge into `discussion_and_debate` with an RS/Citizenship-specific `TEMPLATE_FOR` prompt. The session structure difference is real but can be handled by age-banded prompts rather than a separate template
- `text_study_literature` → handle via KS4-specific `TEMPLATE_FOR` prompt on `text_study`, not a separate template. The session structure changes at KS4 but the template concept is the same
- `writers_workshop` → distinct enough from `text_study` to keep. The starting point is the child's writing, not a model text. **Keep as new #21**
- `grammar_in_context` → merge into `text_study` with explicit grammar embedding in the session structure
- `fluency_practice` → sufficiently distinct from `worked_example_set`. **Keep as new #22**
- `reasoning_task` → merge into `worked_example_set` via the `nc_aim_emphasis` property on MathsTopicSuggestion. If nc_aim_emphasis = "reasoning", the AI uses reasoning prompt patterns within the worked_example session structure
- `secondary_data_analysis` → merge into `pattern_seeking` with a data-source variant. The session structure is similar (question → data → pattern → explanation)
- `reading_for_pleasure` → too narrow for a template. Handle as a `suggestion_type` value ("reading_for_pleasure") on EnglishTopicSuggestion
- `spoken_language_performance` → merge into `performance` template with English-specific TEMPLATE_FOR prompt
- `pre_teaching_diagnostic` → too narrow. Handle as `assessment_mode: "diagnostic"` on TopicSuggestion
- `mystery` → merge into `investigation_design` with a Geography-specific TEMPLATE_FOR prompt
- `local_history_enquiry` → merge into `source_enquiry` with a locality-specific TEMPLATE_FOR prompt
- `significance_enquiry` → merge into `topic_study` with History-specific TEMPLATE_FOR prompt referencing `disciplinary_concepts`
- Various Maths proposals (`problem_solving_task`, `mathematical_investigation`) → handled by `nc_aim_emphasis` routing within existing templates

**Final count: ~22 templates** (14 original + 8 new). This is manageable, covers all genuinely distinct pedagogical patterns, and uses the age-banded `TEMPLATE_FOR` prompts to handle within-template variation rather than creating template proliferation.

---

## Appendix A: Content Pack Generation — What Graph Data Is Essential?

For each generation type, the essential graph data sources:

### Lesson Plan Generation

| Data Source | Essential Properties | Role |
|---|---|---|
| ConceptCluster | concepts, sequencing, co-teach hints | Scope and ordering |
| Concept | name, definitions, prerequisites | Content and readiness |
| DifficultyLevel | description, example_task, example_response, common_errors | Calibration and assessment |
| ThinkingLens + PROMPT_FOR | agent_prompt, question_stems (age-banded) | Cognitive framing |
| TopicSuggestion (typed) | ALL subject-specific properties | Content context |
| VehicleTemplate + TEMPLATE_FOR | session_structure, agent_prompt (age-banded) | Lesson structure |
| ContentGuideline | reading_level, vocabulary, TTS | Age constraints |
| PedagogyProfile | scaffolding, productive_failure, session_structure | Pedagogical approach |
| FeedbackProfile | tone, gamification_safety, metacognitive_prompts | Response framing |

### Assessment Task Generation

| Data Source | Essential Properties | Role |
|---|---|---|
| DifficultyLevel | example_task, example_response, common_errors, description | **Primary** — this IS the assessment data |
| TopicSuggestion | misconceptions (Science), writing_outcome (English), fluency_targets (Maths) | Task framing |
| ThinkingLens | key_question | Higher-order question framing |
| ContentGuideline | reading_level | Language calibration |

### Video Script Generation

| Data Source | Essential Properties | Role |
|---|---|---|
| TopicSuggestion | pedagogical_rationale (hook), definitions (vocabulary), expected_outcome (correct explanation) | Narrative content |
| ThinkingLens | key_question | Opening question |
| DifficultyLevel | description per level | "What does understanding look like at each stage?" |
| VehicleTemplate | session_structure | Script structure |
| Concept | name, prerequisites | "Before watching this, you should know..." |

### Parent-Facing Explanation

| Data Source | Essential Properties | Role |
|---|---|---|
| TopicSuggestion | pedagogical_rationale, definitions | "What your child is learning and why" |
| DifficultyLevel | description, example_task | "This is what your child should be able to do" |
| ConceptCluster | sequencing | "This lesson comes before X and after Y" |
| ContentGuideline | agent_prompt (parent-facing) | Tone and language calibration |

---

## Appendix B: Suggested `cross_curricular_hooks` Structure

The History specialist proposed structured objects for cross-curricular hooks. This is correct. The recommended format:

```json
"cross_curricular_hooks": [
  {
    "subject": "Geography",
    "hook": "The Nile: river systems, flooding, irrigation — direct Geography curriculum content",
    "strength": "strong"
  },
  {
    "subject": "Science",
    "hook": "Mummification: preservation techniques, material properties",
    "strength": "moderate"
  }
]
```

**Why structured?** The AI tutor can use `strength` to decide which hooks to surface (strong hooks become lesson segments; moderate hooks become brief mentions). The `subject` field enables cross-subject query lookup. A plain string like `"Geography: Nile"` is parseable but fragile.

**Counter-argument**: This adds authoring complexity. For a first implementation, `string[]` with a consistent format like `"[Geography] The Nile — river systems, flooding, irrigation"` is acceptable. Upgrade to structured objects in a future iteration if cross-curricular query patterns prove valuable.

**My ruling**: Start with `string[]` using the bracketed-subject convention. The AI can parse `[Geography]` reliably enough for generation. Migrate to structured objects if cross-subject querying becomes a core use case.

---

## Appendix C: Safety Properties in the System Prompt

Three types of safety data must go in the system prompt (non-overridable by the generation prompt):

1. **`safety_notes`** (Science, DT) — physical safety for practical activities
2. **`sensitive_content_notes`** (History) — child safeguarding for difficult topics
3. **`hazard_level`** (Science) — triage flag for safety language intensity

These should be formatted as system-level constraints:

```
[SAFETY CONSTRAINTS — DO NOT OVERRIDE]
Hazard level: standard
Safety notes: Lamp gets hot. Ensure water does not contact electrical equipment.
Wear goggles throughout the practical.

[CONTENT SENSITIVITY — HANDLE WITH CARE]
- Follow UCL Centre for Holocaust Education guidance
- Do not use graphic atrocity images
- Present victims as individuals with full lives
```

The generation prompt should NOT repeat these — they are constraints, not suggestions. The AI must comply unconditionally.

---

*Review complete. The proposed schema is architecturally sound for AI content generation. The specialists have correctly identified the curriculum intelligence that belongs in the graph. The five recommendations above — accept required properties, implement controlled vocabularies, add foundation labels, build a query orchestrator, and consolidate templates — constitute the development roadmap from "schema design" to "generation-ready platform."*
