# Generator-Grade Topic Spec: Delta Specification

**Status:** Proposed
**Date:** 2026-02-27
**Scope:** All TopicSuggestion types + Concept extraction schema
**Worked example:** KS2 Computing — Networks and the Internet

---

## Problem

The topic suggestion layer currently provides good curriculum labels and pedagogical rationale, but lacks the operational constraints that stop a lesson generator producing glossy-but-hollow output. Across 5+ reviewed examples, the same failure modes appear:

1. **Statutory alignment is a label, not a constraint.** `curriculum_reference` cites the statutory text, but nothing forces the generator to cover every element, at age-appropriate depth, with observable outcomes.
2. **The concept → lesson bridge is under-specified.** Strong concept descriptions and misconceptions exist, but no atomised knowledge the generator can target, sequence, and assess.
3. **Vocabulary mats are systematically incomplete.** Multiple units ship with `definitions` as a bare term list (no meanings). This guarantees inconsistent output.
4. **Session structure can mis-shape the subject.** "Research Enquiry" for Computing risks poster syndrome. "Practical Application" for Art can miss statutory breadth requirements.
5. **Assessment is product-led, not knowledge-led.** End products (portfolio, report, presentation) are specified, but hinge questions, misconception probes, spaced retrieval, and KC-mapped assessment items are absent.

---

## Six Changes (one set of upgrades, all subjects)

### 1. `knowledge_components[]` on Concept nodes

**Where:** Extraction JSONs (`layers/uk-curriculum/data/extractions/`)
**What:** Array of atomised, testable facts/skills for each concept. Each KC has an ID, a statement, a testable-as type, and prerequisites referencing other KCs in the same concept.

**Schema:**
```json
{
  "knowledge_components": [
    {
      "kc_id": "KC-NET-01",
      "statement": "A network is two or more connected devices that share data and resources.",
      "testable_as": "define_and_give_example"
    }
  ],
  "knowledge_component_progression": [
    {
      "from": "KC-NET-01",
      "to": "KC-NET-02",
      "rationale": "Must understand a single network before network-of-networks."
    }
  ]
}
```

**KC ID format:** `KC-{TOPIC_SLUG}-{NN}` (e.g. `KC-NET-01`, `KC-CAM-01`, `KC-3DP-01`)

**`testable_as` enum:**
- `define_and_give_example` — pupil defines a term and gives an example
- `define_and_distinguish` — pupil defines and distinguishes from a near-miss
- `two_option_contrast` — pupil explains the difference between two items
- `label_diagram` — pupil labels components on a diagram
- `explain_in_own_words` — pupil explains a mechanism or process
- `identify_and_correct` — pupil spots a misconception and corrects it
- `evaluate_and_justify` — pupil evaluates options and justifies a choice

**Why this matters:** Without atomic KCs, the generator has no target smaller than "the whole concept". It can't sequence within a lesson, can't check understanding of specific facts, and can't build retrieval schedules that revisit specific knowledge.

**Rollout:** Start with concepts that deliver prescribed/mandatory topic suggestions. ~50 concepts across all subjects. Do not attempt all 1,300+ concepts.

---

### 2. `statutory_decomposition[]` on TopicSuggestion nodes

**Where:** Topic suggestion JSONs (`layers/topic-suggestions/data/`)
**What:** Break each `curriculum_reference` string into atomic requirements the generator must cover.

**Schema:**
```json
{
  "statutory_decomposition": [
    {
      "sd_id": "SD-NET-01",
      "requirement": "understand computer networks",
      "source_objective_id": "CO-KS12-O010",
      "kc_ids": ["KC-NET-01", "KC-NET-04"],
      "assessment_required": true
    },
    {
      "sd_id": "SD-NET-02",
      "requirement": "including the internet",
      "source_objective_id": "CO-KS12-O010",
      "kc_ids": ["KC-NET-02", "KC-NET-05"],
      "assessment_required": true
    },
    {
      "sd_id": "SD-NET-03",
      "requirement": "multiple services, such as the world wide web",
      "source_objective_id": "CO-KS12-O010",
      "kc_ids": ["KC-NET-03"],
      "assessment_required": true
    }
  ]
}
```

**SD ID format:** `SD-{TOPIC_SLUG}-{NN}`

**Why this matters:** The current `curriculum_reference` is a label. A generator can cite it and then teach a subset. Decomposition + `assessment_required: true` forces coverage. If a statutory element has no assessment item targeting its KCs, the generator has failed.

---

### 3. `vocabulary_mat[]` replaces `definitions[]`

**Where:** All TopicSuggestion / study node JSONs
**What:** Change from bare term list to structured array with definitions and example sentences.

**Before (current):**
```json
"definitions": ["network", "internet", "router", "packet"]
```

**After:**
```json
"vocabulary_mat": [
  {
    "term": "network",
    "definition": "Connected devices that can share data and resources.",
    "example_sentence": "Our classroom computers and printer are on a network."
  }
]
```

**Validation rule:** No entry in `vocabulary_mat` may have an empty `definition`. If `vocabulary_mat` is present, all terms from the concept's `key_vocabulary` that appear in this unit must be covered.

**Why this matters:** Blank vocabulary definitions are a major quality leak found in 4 of 5 reviewed units (Computing, D&T KS2, D&T KS3, Art KS3). A generator inheriting blank definitions produces inconsistent vocabulary instruction.

**Migration path:** The `definitions` field remains valid for backward compatibility. The import script treats `vocabulary_mat` as the authoritative source when present. A validation warning fires for any unit that still uses bare `definitions`.

---

### 4. `depth_boundary` on Concept nodes

**Where:** Extraction JSONs (`layers/uk-curriculum/data/extractions/`)
**What:** Explicit in-scope / out-of-scope boundary per key stage to prevent generator drift.

**Schema:**
```json
{
  "depth_boundary": {
    "in_scope": [
      "Networks as connected devices sharing resources",
      "Internet as network of networks",
      "Web as one service; email and streaming as others",
      "Packets as chunks of data; may take different routes",
      "Search engines index and rank pages"
    ],
    "out_of_scope": [
      "TCP/IP protocol stack detail",
      "OSI model layers",
      "DNS resolution process",
      "HTTP request/response headers",
      "IP address classes or subnetting"
    ],
    "rationale": "KS2 pupils need conceptual understanding of how the internet works, not protocol-level detail. The DifficultyLevel 'expected' tier defines the ceiling."
  }
}
```

**Why this matters:** The current DifficultyLevel `expected` tier for CO-KS12-C004 names "TCP/IP" in its model response. That's beyond KS2 depth. Without an explicit boundary, a generator treating DL expected as the target will overshoot. The `depth_boundary` sets guardrails the generator can check against.

---

### 5. `assessment_items[]` on TopicSuggestion nodes

**Where:** Topic suggestion JSONs
**What:** A small library of assessment item templates, each tagged to KC IDs and typed.

**Schema:**
```json
{
  "assessment_items": [
    {
      "type": "hinge_true_false_justify",
      "stem": "The web is the same as the internet: True or False? Explain.",
      "expected": "False. The internet is the global network. The web is a service on the internet.",
      "kc_ids": ["KC-NET-02", "KC-NET-03"],
      "misconception_targeted": "Internet and web are the same thing"
    },
    {
      "type": "label_diagram",
      "stem": "Label the client, server, and router on this network diagram.",
      "expected": "Client = the device requesting data. Server = the device storing/serving data. Router = the device directing packets between networks.",
      "kc_ids": ["KC-NET-04", "KC-NET-05"],
      "misconception_targeted": null
    },
    {
      "type": "misconception_probe",
      "stem": "A pupil says: 'The internet is inside my computer.' What would you say to help them understand?",
      "expected": "The internet is not inside any computer. It is a network of networks — cables, routers, and servers connecting millions of devices. Your computer connects to the internet through a router.",
      "kc_ids": ["KC-NET-01", "KC-NET-02"],
      "misconception_targeted": "The internet is inside my computer"
    }
  ]
}
```

**Assessment item type enum:**
- `hinge_true_false_justify` — True/False + one-sentence justification
- `hinge_multiple_choice` — 3 options, one correct
- `two_option_contrast` — explain the difference between two items
- `label_diagram` — label components on a diagram
- `explain_in_own_words` — free response (1-2 sentences)
- `misconception_probe` — present a misconception, pupil corrects
- `evaluate_and_justify` — choose from options and justify

**Validation rule:** Every named `common_misconception` in the concept must have at least one `misconception_probe` or `misconception_targeted` reference in the assessment items. Every KC must be targeted by at least one assessment item.

**Why this matters:** Without KC-tagged assessment items, assessment defaults to "make a poster/presentation" — product-led, not knowledge-led. This is the single biggest quality lever: if the generator knows *what to check* and *how to check it*, the lesson structure follows.

---

### 6. Anti-degeneration constraints on VehicleTemplate nodes

**Where:** VehicleTemplate JSONs (`layers/topic-suggestions/data/vehicle_templates/`)
**What:** Typed constraints per session structure that prevent known failure modes.

**Schema (addition to VehicleTemplate):**
```json
{
  "activity_constraints": [
    {
      "activity_type": "research",
      "rules": {
        "source_count_minimum": 2,
        "credibility_rationale_required": true,
        "output_format_blacklist": ["poster"],
        "knowledge_check_after": true
      },
      "rationale": "Prevents research degenerating into unassessed poster-making."
    },
    {
      "activity_type": "design_make",
      "rules": {
        "mechanism_understanding_check": true,
        "evaluation_against_specification": true,
        "knowledge_check_after": true
      },
      "rationale": "Prevents D&T becoming 'make a nice thing' without understanding."
    }
  ],
  "quality_gates": {
    "alignment_minimum_pct": 80,
    "misconception_coverage": "each named misconception must have at least 1 probe + 1 corrective explanation",
    "cognitive_load_max_new_terms_per_lesson": 6,
    "structured_talk_minimum_per_lesson": 2,
    "worked_example_minimum_per_lesson": 1
  }
}
```

**Why this matters:** "Research Enquiry" as a session structure for Computing can produce poster syndrome. "Design, Make, Evaluate" for D&T can produce "nice toy, no understanding". The constraints are activity-type-level guardrails, not topic-specific rules.

---

## What doesn't change

- **ConceptCluster** and **ThinkingLens** layers are unaffected. They operate at a different level of abstraction (cluster grouping, cognitive framing) and remain valid.
- **DifficultyLevel** nodes remain as-is. They provide attainment tiers, not lesson sequencing. The `depth_boundary` property on Concept complements them by setting the ceiling.
- **DeliveryMode** classification is unaffected. It classifies what combination of AI/human is needed, not how the lesson is structured.
- **Existing `definitions` arrays** are not deleted. They are superseded by `vocabulary_mat` when present; a validation warning fires for files still using bare `definitions`.

---

## Implementation order

1. Add `knowledge_components` + `knowledge_component_progression` to CO-KS12-C004 in the extraction JSON (worked example).
2. Add `vocabulary_mat` to TS-CO-KS2-004, replacing `definitions` (worked example).
3. Add `statutory_decomposition` to TS-CO-KS2-004 (worked example).
4. Add `depth_boundary` to CO-KS12-C004 in the extraction JSON (worked example).
5. Add `assessment_items` to TS-CO-KS2-004 (worked example).
6. Add `activity_constraints` + `quality_gates` to VT-06 (the template used by Networks).
7. Add vocabulary completeness validation rule.
8. Update CLAUDE.md with new property documentation.

Steps 1-6 produce the worked example (Networks before/after). Steps 7-8 set up enforcement for future rollout.

---

## Worked example: KS2 Computing — Networks and the Internet

See the actual data files for the before/after:
- **Concept (before/after):** `layers/uk-curriculum/data/extractions/primary/Computing_KS1-2_extracted.json` — CO-KS12-C004
- **TopicSuggestion (before/after):** `layers/topic-suggestions/data/computing_studies/computing_studies_ks2.json` — TS-CO-KS2-004

---

## Cross-cutting patterns found across reviewed examples

| Pattern | Units affected | Fix |
|---------|---------------|-----|
| Vocabulary definitions blank | Computing KS2, D&T KS2, D&T KS3, Art KS3 | `vocabulary_mat` with validation |
| Statutory reference cited but not decomposed | All 5 reviewed | `statutory_decomposition` |
| Assessment is product-only | D&T KS2 (portfolio), D&T KS3 (portfolio), Computing KS2 (report) | `assessment_items` tagged to KCs |
| Session structure can mis-shape subject | Computing (Research Enquiry → posters), Art (Practical → misses breadth) | Anti-degeneration constraints on VehicleTemplate |
| Concept has no atomised facts | All 5 reviewed | `knowledge_components` on Concept |
| Generator can overshoot KS depth | Computing KS2 (TCP/IP in model response) | `depth_boundary` on Concept |
