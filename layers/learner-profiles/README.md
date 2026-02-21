# Learner Profiles Layer

Age-appropriate design constraints for AI lesson generation. Provides structured nodes that an AI agent can query alongside curriculum content to know *how* to present material to a given year group.

---

## Why This Exists

When an AI agent queries the graph to build a lesson, it needs more than just the curriculum content. It needs to know:

- **What interaction types** are developmentally appropriate (can this child type? do they need TTS?)
- **What reading level** to pitch the content at (Lexile range, sentence length, vocabulary level)
- **What pedagogy sequence** to follow (productive failure first? worked example first?)
- **How to give feedback** (never say "well done" to Y1; never use badges for Y6)

All of this is queryable in one Cypher pattern:

```cypher
MATCH (y:Year {year_code: 'Y3'})
MATCH (y)-[:HAS_PROGRAMME]->(p:Programme {subject_name: 'Science'})-[:HAS_DOMAIN]->(d:Domain)-[:CONTAINS]->(o:Objective)
MATCH (y)-[:HAS_CONTENT_GUIDELINE]->(cg:ContentGuideline)
MATCH (y)-[:HAS_PEDAGOGY_PROFILE]->(pp:PedagogyProfile)
MATCH (y)-[:HAS_FEEDBACK_PROFILE]->(fp:FeedbackProfile)
MATCH (y)-[:SUPPORTS_INTERACTION {primary: true}]->(it:InteractionType)
RETURN y, cg, pp, fp, collect(DISTINCT it) AS interactions, collect(DISTINCT o) AS objectives
```

---

## Node Types

### `:InteractionType` (29 nodes, shared)

Reusable UI/pedagogical patterns. Each Year links to the InteractionTypes it supports.

| interaction_id | Name | Category |
|---|---|---|
| `voice_input` | Voice Input | input |
| `multi_choice_2` | Multiple Choice — 2 | selection |
| `multi_choice_3` | Multiple Choice — 3 | selection |
| `multi_choice_4` | Multiple Choice — 4 | selection |
| `multi_choice_5` | Multiple Choice — 5 | selection |
| `text_input_word` | Text Input — Word | text_input |
| `text_input_phrase` | Text Input — Phrase | text_input |
| `text_input_sentence` | Text Input — Sentence | text_input |
| `text_input_paragraph` | Text Input — Paragraph | text_input |
| `code_input` | Code Input | text_input |
| `drag_drop_place` | Drag to Place | manipulation |
| `drag_reorder` | Drag to Reorder | manipulation |
| `drag_categorise` | Drag to Categorise | manipulation |
| `sentence_assembly` | Sentence Assembly | manipulation |
| `matching_pairs` | Matching Pairs | manipulation |
| `image_annotation` | Image Annotation | manipulation |
| `number_line_scrubber` | Number Line | maths_tool |
| `bus_stop_division` | Bus Stop Division | maths_tool |
| `column_addition` | Column Addition | maths_tool |
| `column_subtraction` | Column Subtraction | maths_tool |
| `fraction_visualizer` | Fraction Visualiser | maths_tool |
| `area_model_multiplication` | Area Model | maths_tool |
| `place_value_blocks` | Place Value Blocks | maths_tool |
| `text_highlight` | Text Highlight | reading_tool |
| `text_annotation` | Text Annotation | reading_tool |
| `pattern_discovery` | Pattern Discovery | higher_order |
| `inference_task` | Inference Task | higher_order |
| `compare_contrast_table` | Compare and Contrast | higher_order |
| `rhythm_analyser` | Rhythm Analyser | specialist |

Each node has:
- `agent_prompt` — instruction string for the AI agent on how to use this interaction
- `ui_notes` — implementation notes for the front-end developer
- `requires_literacy`, `requires_numeracy` — boolean flags
- `subject_affinity` — JSON array of applicable subjects or `["All"]`

### `:ContentGuideline` (9 nodes, one per Year)

Language and reading level constraints.

Key properties:
- `reading_level_description` — plain English summary
- `lexile_min`, `lexile_max` — Lexile band (null for Y1–Y2)
- `flesch_kincaid_grade_max` — FK grade level ceiling
- `max_sentence_length_words`, `avg_sentence_length_words`
- `vocabulary_level` — enumerated level descriptor
- `academic_vocabulary_ok` — boolean
- `tts_required` — boolean (true for Y1–Y2)
- `tts_available` — boolean (available for accessibility throughout)
- `agent_content_prompt` — LLM instruction for content generation

### `:PedagogyProfile` (9 nodes, one per Year)

Session structure and scaffolding constraints. Research-backed from:
- Sinha & Kapur (2021): productive failure meta-analysis (d=0.36–0.58)
- Bjork (2011): desirable difficulties — spacing and interleaving
- ASSISTments (2025): immediate feedback effect size 0.37
- Knowledge Space Theory (ALEKS): outer-fringe prerequisite gating

Key properties:
- `session_length_min_minutes`, `session_length_max_minutes`
- `hint_tiers_max` — maximum hint depth (2–4 depending on year)
- `productive_failure_appropriate` — boolean (false Y1–Y2, true Y3+)
- `scaffolding_level` — `maximum | moderate | light | minimal`
- `session_sequence` — JSON array of session phase names
- `desirable_difficulties` — JSON array of enabled techniques
- `spacing_interval_days_min`, `spacing_interval_days_max`
- `agent_pedagogy_prompt` — LLM instruction for session sequencing

### `:FeedbackProfile` (9 nodes, one per Year)

Feedback style and motivational safety constraints. Research-backed from:
- Ryan & Deci (2000): Self-Determination Theory — informational vs. controlling feedback
- Lepper et al. (1973): overjustification effect — expected rewards undermine intrinsic motivation
- Jose et al. (2024): gamification ghost effect — badges harm introverts in mixed classrooms

Key properties:
- `feedback_style` — e.g. `informational_celebratory`, `specific_competence`, `gcse_exam_style`
- `ai_tone` — e.g. `warm_nurturing`, `intellectual_peer`, `examination_coach`
- `gamification_safe`, `progress_bars_safe`, `leaderboards_safe`, `badge_systems_safe` — all false
- `unexpected_delight_safe` — true (unexpected rewards are motivationally safe)
- `delight_frequency` — `frequent | semi_random | occasional | very_rare | none`
- `counter_misconceptions_explicit` — boolean (false Y1–Y2, true Y3+)
- `metacognitive_reflection` — boolean (false Y1–Y5, true Y6+)
- `feedback_example_correct`, `feedback_example_incorrect` — example strings
- `avoid_phrases` — JSON array of prohibited phrases
- `agent_feedback_prompt` — LLM instruction for feedback generation

---

## Relationships

```
(Year)-[:HAS_CONTENT_GUIDELINE]->(ContentGuideline)
(Year)-[:HAS_PEDAGOGY_PROFILE]->(PedagogyProfile)
(Year)-[:HAS_FEEDBACK_PROFILE]->(FeedbackProfile)
(Year)-[:SUPPORTS_INTERACTION {primary: bool}]->(InteractionType)
```

`SUPPORTS_INTERACTION.primary = true` means this is the preferred/default interaction for that year group.

---

## Useful Queries

### All primary interactions for a year group
```cypher
MATCH (y:Year {year_code: 'Y4'})-[:SUPPORTS_INTERACTION {primary: true}]->(i:InteractionType)
RETURN i.interaction_id, i.name, i.category ORDER BY i.category, i.name
```

### Years that require TTS
```cypher
MATCH (y:Year)-[:HAS_CONTENT_GUIDELINE]->(cg:ContentGuideline {tts_required: true})
RETURN y.year_code, cg.reading_level_description
```

### Which interactions require no literacy (good for Y1–Y2)
```cypher
MATCH (i:InteractionType {requires_literacy: false})
RETURN i.interaction_id, i.name, i.category
```

### Full lesson-generation context for an agent
```cypher
MATCH (y:Year {year_code: 'Y3'})
MATCH (y)-[:HAS_PROGRAMME]->(p:Programme {subject_name: 'Science'})
-[:HAS_DOMAIN]->(d:Domain)-[:CONTAINS]->(o:Objective)
MATCH (y)-[:HAS_CONTENT_GUIDELINE]->(cg:ContentGuideline)
MATCH (y)-[:HAS_PEDAGOGY_PROFILE]->(pp:PedagogyProfile)
MATCH (y)-[:HAS_FEEDBACK_PROFILE]->(fp:FeedbackProfile)
MATCH (y)-[:SUPPORTS_INTERACTION {primary: true}]->(it:InteractionType)
RETURN y.year_code,
       cg.agent_content_prompt,
       pp.agent_pedagogy_prompt,
       fp.agent_feedback_prompt,
       collect(DISTINCT it.agent_prompt) AS interaction_prompts,
       collect(DISTINCT o.description) AS objectives
```

### Maths tools by year group
```cypher
MATCH (y:Year)-[:SUPPORTS_INTERACTION]->(i:InteractionType {category: 'maths_tool'})
RETURN y.year_code, collect(i.interaction_id) AS maths_tools ORDER BY y.year_code
```

---

## Data Sources

All learner profile data is authored from the following research:

| Paper | Finding applied |
|---|---|
| Létourneau et al. (2025) — AI ITS Systematic Review | ITS effectiveness; hint quality; blended > ITS alone |
| LLM Education Review (2025) | 35% of LLM hints unhelpful; structured model + LLM superior |
| Sinha & Kapur (2021) — Productive Failure meta-analysis | d=0.36–0.58; problem-first sequences; Y3+ |
| Ryan & Deci (2000) — Self-Determination Theory | Informational feedback; no gamification |
| Lepper et al. (1973) — Overjustification | No expected rewards; unexpected delight safe |
| Bjork (2011) — Desirable Difficulties | Spacing +10–30%; interleaving +30–40% |
| Roediger & Karpicke (2006) — Testing Effect | Retrieval > re-study; post-error correction essential |
| ASSISTments (2025) | Immediate feedback ES=0.37; tiered hints |
| ALEKS — Knowledge Space Theory | Outer-fringe prerequisite gating |
| Jose et al. (2024) — Ghost Effect | Gamification harms introverts; remove for Y3+ |
| Carnegie Learning Research | Blended ITS doubles gains; low-prior-attainment students benefit most |

Full research notes at `docs/research/`.

---

## Import

```bash
python3 layers/learner-profiles/scripts/import_learner_profiles.py
```

This is idempotent — safe to re-run. All writes use MERGE.

### Data files
```
extractions/
  interaction_types.json     # 29 InteractionType definitions
  content_guidelines.json    # 11 ContentGuideline profiles (Y1–Y11)
  pedagogy_profiles.json     # 11 PedagogyProfile profiles (Y1–Y11)
  feedback_profiles.json     # 11 FeedbackProfile profiles (Y1–Y11)
  year_interactions.json     # Year → InteractionType mapping (primary/secondary)
```
