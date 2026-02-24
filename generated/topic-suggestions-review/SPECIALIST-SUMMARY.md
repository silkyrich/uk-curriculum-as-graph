# Specialist Review Summary — 6 Subject Reviews Consolidated

## Consensus Areas

### 1. All 6 want controlled vocabularies for subject-specific enums (strongest signal)

### 2. 5/6 want more VehicleTemplates (23 new proposed, current 14 insufficient)

### 3. 3/6 note their subject's "topics" are fundamentally different from History's
- English: organised around texts/genres, not topics
- Maths: organised around concepts/representations, not topics
- Foundation: spans making, performing, coding, ethical enquiry

### 4. Safety/sensitivity notes needed (Science: required; History: safeguarding; DT: tool safety)

### 5. `cross_curricular_hooks` should be structured objects, not plain strings

### 6. `suggestion_type` enum needs expansion (current 7 values insufficient)

## New Properties Proposed by Subject

### History adds: `disciplinary_concepts` (required), `significance_claim` (required), `sensitive_content_notes`, `enquiry_questions`, `comparison_pairs`, `interpretations`, `period_start_year`, `period_end_year`

### Geography adds: `map_types` (required), `scale` (required), `theme_category` (required), `fieldwork_potential`. MODIFIES: `location` -> `locations` (string[]), `data_sources` -> required

### Science adds: `misconceptions` (required, min 2), `recording_format` (required), `science_discipline` (required), `hazard_level` (required), `variables` (object), `secondary_enquiry_types`. MODIFIES: `enquiry_type` vocab to 7 values, `equipment`/`safety_notes`/`expected_outcome` all -> required

### English adds: `writing_outcome` (required), `grammar_focus` (required KS1-3), `reading_level` (required), `text_type` (required), `spoken_language_focus`, `exam_board_status`, `assessment_mode`, `literary_terms`. MODIFIES: `genre` -> string[] with controlled vocab, `suggested_texts` -> object[] with structured fields

### Maths adds: `fluency_targets` (required), `reasoning_prompts`, `application_contexts`, `nc_aim_emphasis` (required), `cpa_notes`. MODIFIES: `cpa_stage` -> 6-value enum, `manipulatives`/`representations` -> required. REMOVES: `common_errors` (defer to DifficultyLevel)

### Foundation proposes 3 NEW typed labels:
- **ArtTopicSuggestion**: artist, art_movement, medium (required), techniques (required), visual_elements
- **MusicTopicSuggestion**: composer, piece, genre, musical_elements (required), activity_focus (required), instrument
- **DTTopicSuggestion**: dt_strand (required), design_brief (required), materials (required), tools, techniques (required), evaluation_criteria, safety_notes

### Universal adds: `year_groups` (optional), `duration_lessons` (optional). MODIFIES: `curriculum_reference` -> string[]

## VehicleTemplate Proposals (23 new)

History: `source_enquiry`, `significance_enquiry`, `local_history_enquiry`
Geography: `place_study`, `decision_making_exercise`, `mystery`
Science: `modelling_enquiry`, `identifying_and_classifying`, `secondary_data_analysis`
English: `writers_workshop`, `grammar_in_context`, `reading_for_pleasure`, `spoken_language_performance`, `unseen_analysis`, + split `text_study` into primary/literature
Maths: `fluency_practice`, `reasoning_task`, `problem_solving_task`, `mathematical_investigation`, `pre_teaching_diagnostic`
Foundation: `performance`, `design_make_evaluate`, `ethical_enquiry`

## Key Tension: Template Count

14 existing + 23 proposed = 37 total. Risk of template sprawl. Some overlap exists. Consolidation needed.
