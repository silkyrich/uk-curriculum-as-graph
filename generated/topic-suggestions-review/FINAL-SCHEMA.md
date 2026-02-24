# Final Schema: TopicSuggestion + VehicleTemplate (Post-Panel Consensus)

**Date**: 2026-02-24
**Status**: LOCKED after 8-agent teacher panel review
**Input**: 6 subject specialist reviews + curriculum-lead arbitration + content-architect evaluation

## Labels (9 total)

| # | Label | Subjects |
|---|---|---|
| 1 | `HistoryTopicSuggestion` | History |
| 2 | `GeographyTopicSuggestion` | Geography |
| 3 | `ScienceTopicSuggestion` | Science, Biology, Chemistry, Physics |
| 4 | `EnglishTopicSuggestion` | English, English Language, English Literature |
| 5 | `MathsTopicSuggestion` | Mathematics |
| 6 | `ArtTopicSuggestion` | Art & Design |
| 7 | `MusicTopicSuggestion` | Music |
| 8 | `DTTopicSuggestion` | Design & Technology |
| 9 | `TopicSuggestion` | Computing, RS, Citizenship, Drama, PE, Business, Food, Media Studies |

Cross-label query: `MATCH (n) WHERE n.display_category = 'Topic Suggestion'` returns all.

## VehicleTemplates (24 total)

### Retained (14, some renamed/modified)
1. `topic_study` - History, Geography, RS, Citizenship
2. `case_study` - Geography, Business, Science (add locate_and_describe phase)
3. `fair_test` - Science
4. `observation_over_time` - Science, Art (renamed from observation_enquiry)
5. `pattern_seeking` - Science, Maths, Geography
6. `research_enquiry` - Science, History, RS
7. `text_study` - English KS1-KS3
8. `worked_example_set` - Maths (add activation + reasoning extension)
9. `open_investigation` - Science, Geography (renamed from investigation_design)
10. `fieldwork` - Geography, Science
11. `discussion_and_debate` - English, RS, Citizenship, History
12. `creative_response` - Art, English
13. `practical_application` - Maths, DT, Computing, Food
14. `comparison_study` - Geography, History, RS

### New (10)
15. `source_enquiry` - History
16. `modelling_enquiry` - Science, Geography
17. `identifying_and_classifying` - Science
18. `secondary_data_analysis` - Science, Geography, Maths
19. `place_study` - Geography
20. `performance` - Music, Drama, PE
21. `design_make_evaluate` - DT
22. `ethical_enquiry` - RS, Citizenship
23. `text_study_literature` - English KS4
24. `writers_workshop` - English

## suggestion_type Enum (9 values)

`prescribed_topic`, `exemplar_topic`, `open_slot`, `exemplar_figure`, `exemplar_event`, `exemplar_text`, `set_text`, `genre_requirement`, `teacher_convention`

## Universal Properties (all 9 labels)

| Property | Type | Required |
|---|---|---|
| `suggestion_id` | string | Yes |
| `name` | string | Yes |
| `suggestion_type` | string (9-value enum) | Yes |
| `subject` | string | Yes |
| `key_stage` | string | Yes |
| `curriculum_status` | string (mandatory/menu_choice/exemplar/convention) | Yes |
| `choice_group` | string | No |
| `curriculum_reference` | string[] | No |
| `pedagogical_rationale` | string | Yes |
| `common_pitfalls` | string[] | No |
| `cross_curricular_hooks` | string[] | No |
| `sensitive_content_notes` | string[] | No |
| `year_groups` | string[] | No |
| `duration_lessons` | int | No |
| `definitions` | string[] | Yes |
| `display_category` | string | Yes |
| `display_color` | string | Yes |
| `display_icon` | string | Yes |

## Per-Label Properties

### HistoryTopicSuggestion
| Property | Type | Required |
|---|---|---|
| `period` | string | Yes |
| `period_start_year` | int | No |
| `period_end_year` | int | No |
| `key_figures` | string[] | No |
| `comparison_pairs` | object[] | No |
| `key_events` | string[] | No |
| `sources` | string[] | No |
| `source_types` | string[] | Yes |
| `perspectives` | string[] | Yes |
| `interpretations` | string[] | No |
| `disciplinary_concepts` | string[] | Yes |
| `significance_claim` | string | Yes |
| `enquiry_questions` | string[] | No |

### GeographyTopicSuggestion
| Property | Type | Required |
|---|---|---|
| `locations` | string[] | Yes |
| `theme_category` | string | Yes |
| `themes` | string[] | Yes |
| `scale` | string | Yes |
| `map_types` | string[] | Yes |
| `data_sources` | string[] | Yes |
| `contrasting_with` | string | No |
| `fieldwork_potential` | string | No |

### ScienceTopicSuggestion
| Property | Type | Required |
|---|---|---|
| `enquiry_type` | string (7-value enum) | Yes |
| `secondary_enquiry_types` | string[] | No |
| `science_discipline` | string | Yes |
| `equipment` | string[] | Yes |
| `safety_notes` | string | Yes |
| `hazard_level` | string | Yes |
| `expected_outcome` | string | Yes |
| `recording_format` | string[] | No |
| `misconceptions` | string[] | Yes |
| `variables` | object | No |

### EnglishTopicSuggestion
| Property | Type | Required |
|---|---|---|
| `text_type` | string | Yes |
| `genre` | string[] | Yes |
| `text_features` | string[] | Yes |
| `suggested_texts` | object[] | No |
| `reading_level` | string | Yes |
| `writing_outcome` | string | Yes |
| `grammar_focus` | string[] | No |
| `spoken_language_focus` | string | No |
| `exam_board_status` | object[] | No |
| `assessment_mode` | string | No |
| `literary_terms` | string[] | No |

### MathsTopicSuggestion
| Property | Type | Required |
|---|---|---|
| `cpa_stage` | string (6-value enum) | Yes |
| `cpa_notes` | string | No |
| `manipulatives` | string[] | Yes |
| `representations` | string[] | Yes |
| `fluency_targets` | string[] | Yes |
| `reasoning_prompts` | string[] | No |
| `application_contexts` | string[] | No |
| `nc_aim_emphasis` | string (4-value enum) | Yes |

### ArtTopicSuggestion
| Property | Type | Required |
|---|---|---|
| `artist` | string | No |
| `art_movement` | string | No |
| `medium` | string[] | Yes |
| `techniques` | string[] | Yes |
| `visual_elements` | string[] | No |
| `themes` | string[] | No |

### MusicTopicSuggestion
| Property | Type | Required |
|---|---|---|
| `composer` | string | No |
| `piece` | string | No |
| `genre` | string | No |
| `musical_elements` | string[] | Yes |
| `activity_focus` | string[] | Yes |
| `instrument` | string[] | No |
| `themes` | string[] | No |

### DTTopicSuggestion
| Property | Type | Required |
|---|---|---|
| `dt_strand` | string | Yes |
| `design_brief` | string | Yes |
| `materials` | string[] | Yes |
| `tools` | string[] | No |
| `techniques` | string[] | Yes |
| `evaluation_criteria` | string[] | No |
| `safety_notes` | string | No |
| `themes` | string[] | No |

### TopicSuggestion (generic)
| Property | Type | Required |
|---|---|---|
| `themes` | string[] | Yes |
| `computational_concept` | string[] | No |
| `programming_paradigm` | string | No |
| `software_tool` | string | No |
| `religion` | string[] | No |
| `ethical_issue` | string | No |
| `civic_domain` | string | No |
| `activity_type` | string | No |
| `performance_style` | string | No |
| `practitioner` | string | No |

## Relationships

```cypher
(ts)-[:DELIVERS_VIA {primary: bool}]->(c:Concept)
(ts)-[:USES_TEMPLATE]->(vt:VehicleTemplate)
(:Domain)-[:HAS_SUGGESTION]->(ts)
(:ConceptCluster)-[:SUGGESTED_TOPIC {rank: int}]->(ts)
(:VehicleTemplate)-[:TEMPLATE_FOR {agent_prompt: str}]->(:KeyStage)
(:GeographyTopicSuggestion)-[:CONTRASTS_WITH]->(:GeographyTopicSuggestion)
```

## VehicleTemplate Properties

| Property | Type | Required |
|---|---|---|
| `template_id` | string | Yes |
| `name` | string | Yes |
| `template_type` | string | Yes |
| `description` | string | Yes |
| `session_structure` | string[] | Yes |
| `assessment_approach` | string | Yes |
| `agent_prompt` | string | Yes |
| `typical_duration_lessons` | int | Yes |
| `subjects` | string[] | Yes |
| `key_stages` | string[] | Yes |
| `display_category` | string | Yes |
| `display_color` | string | Yes |
| `display_icon` | string | Yes |
