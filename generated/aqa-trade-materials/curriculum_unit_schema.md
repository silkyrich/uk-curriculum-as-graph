# Curriculum Unit Object Model — Schema

A `curriculum_unit.json` is the single source of truth for a teaching unit.
All outputs (PPTX, teacher notes, question bank, student notes) are compiled from it.

## Top-Level Structure

```
curriculum_unit.json
├── meta              Unit identity, spec ref, branding, build config
├── spec_coverage[]   AQA content points this unit addresses (completeness check)
├── concepts{}        Concept registry — keyed by concept_id
├── sections[]        Ordered array of teachable sections (order = delivery order)
└── resources[]       External links, videos, past papers
```

## Invariants (enforced by validate_unit.py)

1. **Concept introduction** — A concept_id appearing in a slide bullet `concept_refs`,
   question `concepts_tested`, or teacher note `key_concepts` must be declared in
   `concepts_introduced` of that section OR a section with a lower index.

2. **Spec coverage completeness** — Every item in `spec_coverage` must appear in at
   least one section's `spec_refs`. Warn on uncovered items.

3. **Question numbering** — Questions have a `q_id` that is stable (e.g. S02-Q01).
   Sequential display numbers (Q1, Q2…) are assigned at build time by section order.
   Cross-references use `q_id`, not display numbers.

4. **Slide numbering** — Slides have `slide_id` (e.g. S03-SL02). Absolute slide
   numbers assigned at build time. Speaker notes may use `{{slide_ref:S03-SL02}}`
   which resolves to "Slide 14" at build time.

5. **Section reordering safety** — Moving a section earlier than the section that
   introduces a concept it uses is a validation error. Moving it later is always safe.

## Section Object

```json
{
  "section_id": "S03",
  "number": 3,                         // display number — reassigned at build
  "title": "Tariffs: Mechanism and Welfare Effects",
  "spec_refs": ["3.2.6.2-tariffs"],    // AQA spec points covered
  "estimated_minutes": 25,
  "concepts_introduced": ["C005", "C006"],
  "concepts_reinforced": ["C001"],     // introduced in earlier section

  "learning_objectives": [
    {"text": "Define a tariff and explain its mechanism", "ao": "AO1"},
    {"text": "Draw and interpret a tariff diagram", "ao": "AO2"},
    {"text": "Analyse welfare effects of a tariff using areas A/B/C/D", "ao": "AO3"}
  ],

  "teacher": {
    "prerequisite_knowledge": "Students must know supply/demand and consumer/producer surplus.",
    "teaching_sequence": "Hook → define → diagram build (9 steps) → welfare analysis → misconception fix",
    "misconceptions": [
      {
        "error": "Students draw a supply curve shift rather than a price floor at Pw+T",
        "correction": "The tariff is added to the world price — the domestic supply curve does not move",
        "source": "AQA Examiner Report Jun 2022"
      }
    ],
    "board_work": "Build tariff diagram in 9 steps. Label axes FIRST. Draw Sd and Dd. Mark Pw. Mark free-trade quantity imported. Add T to get Pw+T. Label ABCD areas.",
    "timing": { "hook": 3, "instruction": 10, "guided_practice": 8, "independent": 4 },
    "differentiation": {
      "stretch": "Terms of trade improvement argument for large economies",
      "support": "Provide pre-drawn axes with Sd/Dd curves; student adds Pw, tariff wedge, labels"
    }
  },

  "slides": [
    {
      "slide_id": "S03-SL01",
      "type": "section_header",
      "section_number": "{{section.number}}",  // resolved at build
      "section_title": "{{section.title}}",
      "subtitle": "The most examined diagram in Paper 2",
      "speaker_notes": "..."
    },
    {
      "slide_id": "S03-SL02",
      "type": "diagram",
      "title": "The Tariff Diagram — Step by Step",
      "concept_refs": ["C005"],
      "diagram_description": "...",
      "diagram_steps": ["..."],
      "annotation_notes": "...",
      "speaker_notes": "..."
    }
  ],

  "questions": [
    {
      "q_id": "S03-Q01",
      "type": "definition",
      "marks": 2,
      "ao_tags": ["AO1"],
      "concepts_tested": ["C005"],
      "question_text": "Define the term 'tariff'. [2 marks]",
      "mark_scheme": "Award 1 mark for: a tax on imports. Award second mark for: which raises the domestic price above the world price / reduces the quantity imported.",
      "examiner_trap": null
    },
    {
      "q_id": "S03-Q02",
      "type": "diagram_analysis",
      "marks": 9,
      "ao_tags": ["AO1", "AO2", "AO3"],
      "concepts_tested": ["C005", "C006"],
      "links_to_slide": "S03-SL02",
      "question_text": "Using a diagram, explain the welfare effects of imposing a tariff on imports. [9 marks]",
      "mark_scheme": "...",
      "examiner_trap": "Students describe the diagram rather than explain the process — capped at Level 1"
    }
  ]
}
```

## Concept Registry Object

```json
{
  "C005": {
    "name": "Tariff",
    "definition": "A tax imposed on imported goods, raising their domestic price above the world price.",
    "ao_level": "AO1",
    "spec_ref": "3.2.6.2",
    "introduced_in_section": "S03",   // set automatically by validate_unit.py
    "tier": 3                          // Beck's tier (domain-specific vocabulary)
  }
}
```

## Resources Object

```json
{
  "resource_id": "R01",
  "title": "Econplusdal — Tariff Diagram Explained",
  "url": "https://...",
  "type": "video",
  "free": true,
  "relevance": ["S03-SL02"],          // slide_ids this supplements
  "concept_refs": ["C005", "C006"],
  "notes": "9-minute walkthrough; covers axes labelling error explicitly"
}
```

## Build Outputs

| Script | Input | Output |
|---|---|---|
| `build_pptx.py` | `curriculum_unit.json` | `{unit}.pptx` |
| `build_teacher_notes.py` | `curriculum_unit.json` | `teacher-notes.md` |
| `build_question_bank.py` | `curriculum_unit.json` | `question-bank.md` |
| `build_student_notes.py` | `curriculum_unit.json` | `student-notes.md` |
| `build_all.py` | `curriculum_unit.json` | all of the above |
| `validate_unit.py` | `curriculum_unit.json` | validation report |

## What `build_all.py` does on section reorder

1. Validate — abort if any concept introduced after its first use
2. Assign section display numbers (1, 2, 3…) from array order
3. Assign absolute slide numbers from section order × slides per section
4. Assign sequential question display numbers (Q1, Q2…) from section order
5. Resolve `{{slide_ref:S03-SL02}}` → "Slide 14" in all speaker notes
6. Resolve `{{section.number}}` → "3" in all section_header slides
7. Build all four outputs
