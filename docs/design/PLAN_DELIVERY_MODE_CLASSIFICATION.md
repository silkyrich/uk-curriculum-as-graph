# Delivery Mode Classification — Design Document

**Version**: 1.0
**Date**: 2026-02-27
**Status**: Active
**Layer**: Derived (lives within `layers/uk-curriculum/`)

---

## Purpose

Classify every curriculum concept by its **delivery suitability** — what combination of technology, human facilitation, and specialist expertise is needed to teach it effectively. This enables:

1. **Platform scoping**: Which concepts can the AI platform teach directly? Which need hybrid delivery? Which are out-of-scope without a teacher?
2. **Lesson template generation**: Templates know upfront whether they're designing for AI-led, facilitated, or teacher-led delivery
3. **Coverage maximisation**: A top-down view across all ~1,351 concepts showing the platform's addressable surface
4. **Partnership planning**: What support materials do non-specialist adults need? Where is a qualified teacher irreplaceable?

---

## Ontological Model

### New Node Types

#### DeliveryMode (4 nodes)

The four delivery channels, ordered by decreasing digital autonomy:

| mode_id | name | description |
|---|---|---|
| `DM-AI` | AI Direct | AI/software teaches end-to-end via interactive sessions. Answers are objectively assessable or the interaction pattern is well-structured enough for AI delivery. |
| `DM-AF` | AI Facilitated | AI delivers core instruction; a non-specialist adult facilitates specific moments — setting up physical materials, observing a physical task, mediating a brief discussion. |
| `DM-GM` | Guided Materials | Well-designed materials enable a non-qualified adult to teach this. The human is essential throughout but the expertise is encoded in the materials, not the teacher. |
| `DM-ST` | Specialist Teacher | Requires a teacher with subject expertise for real-time pedagogical judgement — assessing creative work, managing extended discussion, demonstrating physical technique, or handling sensitive topics. |

#### TeachingRequirement (15 nodes)

Atomic pedagogical requirements that drive the delivery mode classification. Each requirement implies a minimum delivery mode.

| requirement_id | name | category | implies_minimum_mode |
|---|---|---|---|
| `TR-OBJ` | Objective Assessment | assessment | `DM-AI` |
| `TR-DIG` | Digital Tools Available | resource | `DM-AI` |
| `TR-VIS` | Visual/Interactive Representation | resource | `DM-AI` |
| `TR-AUD` | Audio Interaction | resource | `DM-AI` |
| `TR-SPR` | Structured Practice | pedagogy | `DM-AI` |
| `TR-PHY` | Physical Manipulatives | resource | `DM-AF` |
| `TR-OBS` | Physical Observation | assessment | `DM-AF` |
| `TR-APP` | Physical Apparatus/Equipment | resource | `DM-AF` |
| `TR-GDI` | Guided Discussion | pedagogy | `DM-GM` |
| `TR-NAR` | Narrative/Source Materials | resource | `DM-GM` |
| `TR-MOD` | Adult Modelling | pedagogy | `DM-GM` |
| `TR-CRA` | Creative Assessment | assessment | `DM-ST` |
| `TR-PER` | Performance Assessment | assessment | `DM-ST` |
| `TR-SPK` | Specialist Subject Knowledge | knowledge | `DM-ST` |
| `TR-PAS` | Pastoral Sensitivity | safety | `DM-ST` |

### New Relationships

```cypher
// Primary classification: which delivery mode suits this concept
(:Concept)-[:DELIVERABLE_VIA {primary: bool, confidence: str, rationale: str}]->(:DeliveryMode)

// Teaching requirements that drive the classification
(:Concept)-[:HAS_TEACHING_REQUIREMENT]->(:TeachingRequirement)

// Structural: which requirements imply which minimum mode
(:TeachingRequirement)-[:IMPLIES_MINIMUM_MODE]->(:DeliveryMode)
```

**Properties on DELIVERABLE_VIA:**
- `primary` (boolean): True for the recommended delivery mode; false for viable alternatives
- `confidence` (string): `high` | `medium` | `low`
- `rationale` (string): Brief explanation of why this mode was assigned

### Display Properties

| Node | display_category | display_color | display_icon |
|---|---|---|---|
| DeliveryMode | `"Delivery Readiness"` | `#10B981` (Emerald-500) | `settings_input_antenna` |
| TeachingRequirement | `"Delivery Readiness"` | `#10B981` (Emerald-500) | `checklist` |

### ID Format

- DeliveryMode: `DM-AI`, `DM-AF`, `DM-GM`, `DM-ST`
- TeachingRequirement: `TR-OBJ`, `TR-PHY`, etc.

---

## Classification Signals (Input)

The classification script reads these signals from the existing graph/data:

### Direct Concept Properties
1. **concept_type** — strongest categorical signal (attitude → Specialist; skill in maths → AI Direct)
2. **teaching_weight** (1-6) — complexity proxy
3. **is_keystone** + **prerequisite_fan_out** — cascading importance
4. **teaching_guidance** — free text parsed for physical materials, discussion, group work mentions
5. **common_misconceptions** — complexity of misconceptions

### Related Node Signals
6. **RepresentationStage.resources** — physical manipulative references (primary maths only)
7. **DifficultyLevel.example_task** — encodes concrete vs abstract task modes
8. **ConceptCluster.cluster_type** — introduction vs practice
9. **ThinkingLens** — cognitive mode (patterns = digital; perspective_interpretation = discussion)
10. **InteractionType affinities** — via subject and year

### Structural Signals
11. **Subject** — PE/Art/Music/DT inherently less digital
12. **Key Stage / Year** — younger children need more physical/concrete
13. **Domain structure_type** — process/applied/developmental harder to digitise
14. **Epistemic skill enquiry_type** — fair_test/observation = physical

---

## Classification Rules

### Hard Rules (Override Everything)

| Condition | Mode | Rationale |
|---|---|---|
| concept_type == 'attitude' | DM-ST minimum | Attitudes require human modelling and relationship |
| Subject is PE | DM-ST | Physical skills require physical presence and expert correction |
| Subject is Drama (KS4) | DM-ST | Performance and devising are embodied |
| Science concept with enquiry_type 'fair_test' | DM-AF minimum | Needs physical apparatus |
| English Spoken Language domain | DM-ST | Requires live dialogue and social interaction |

### Subject-Specific Rules

**Mathematics:**
- skill concepts Y1-Y3 with concrete RepresentationStage → DM-AF (physical manipulatives needed)
- skill concepts Y4-Y6 where abstract stage is primary → DM-AI
- knowledge concepts (e.g. place value understanding) → DM-AI
- process concepts (problem solving, reasoning) → DM-AF (structured but needs observation)

**English:**
- Grammar, punctuation, spelling → DM-AI (rule-based, assessable)
- Reading comprehension (factual retrieval) → DM-AI
- Reading comprehension (inference, evaluation) → DM-GM (needs discussion materials)
- Composition → DM-GM (needs human feedback on creative quality)
- Handwriting → DM-AF (physical skill, needs materials)

**Science:**
- Substantive knowledge concepts → DM-AI (factual, can be quizzed/diagnosed)
- Working Scientifically: classifying, secondary research → DM-AI
- Working Scientifically: fair test, observation → DM-AF (physical practical)
- Enquiry planning, variable control → DM-GM (needs structured guidance materials)

**History:**
- Substantive knowledge → DM-AI (dates, events, civilisations)
- Source analysis, interpretation → DM-GM (needs curated source materials + discussion guide)
- Perspective, empathy → DM-GM (needs structured discussion)

**Geography:**
- Locational/place knowledge → DM-AI (factual, can use digital maps)
- Map skills → DM-AI (digital mapping tools)
- Fieldwork → DM-ST (requires real-world observation)
- Human/physical geography knowledge → DM-AI

**Art & Design:**
- Art history, artist knowledge → DM-AI
- Making skills (drawing, painting, sculpture) → DM-ST (physical technique, expert assessment)
- Sketchbook/process → DM-GM (guided by materials)

**Music:**
- Theory, notation, history → DM-AI (can use audio tools)
- Listening and appraising → DM-AI (audio-based)
- Composition → DM-AF (digital composition tools + adult support)
- Performance, ensemble → DM-ST (requires instruments and expert guidance)

**Design & Technology:**
- Material knowledge, mechanisms theory → DM-AI
- Design process → DM-GM (structured materials)
- Making skills → DM-ST (tools, safety, technique)
- Food preparation → DM-ST (kitchen, safety, technique)

**Computing:**
- Most concepts → DM-AI (inherently digital)
- Collaborative/debugging → DM-AF

**Languages (MFL):**
- Reading, listening → DM-AI (text/audio exercises)
- Grammar knowledge → DM-AI
- Writing → DM-AF (needs some human feedback)
- Speaking → DM-AF (speech recognition + human support)

**Religious Studies / Citizenship:**
- Knowledge of beliefs, practices → DM-AI
- Ethical reasoning, discussion → DM-GM (structured discussion materials)
- Sensitive topics → DM-ST (pastoral care)

---

## Data Files

Per-subject JSON files in `layers/uk-curriculum/data/delivery_modes/`:
- `{subject}_{key_stage_or_year}.json`
- Example: `mathematics_y3.json`, `english_ks1.json`, `science_ks2.json`

### File Format
```json
[
  {
    "concept_id": "MA-Y3-C001",
    "primary_mode": "ai_direct",
    "confidence": "high",
    "rationale": "Procedural counting skill with clear right/wrong answers; digital number line tools exist.",
    "alternative_modes": ["ai_facilitated"],
    "teaching_requirements": ["TR-OBJ", "TR-DIG", "TR-SPR"],
    "notes": "Concrete stage (Dienes blocks) may benefit from physical setup at entry level."
  }
]
```

---

## Queries Enabled

```cypher
// All concepts teachable by AI
MATCH (c:Concept)-[:DELIVERABLE_VIA {primary: true}]->(dm:DeliveryMode {mode_id: 'DM-AI'})
RETURN c.concept_id, c.concept_name

// Coverage by subject
MATCH (c:Concept)-[:DELIVERABLE_VIA {primary: true}]->(dm:DeliveryMode)
MATCH (o:Objective)-[:TEACHES]->(c)
MATCH (d:Domain)-[:CONTAINS]->(o)
MATCH (p:Programme)-[:HAS_DOMAIN]->(d)
RETURN p.subject_name, dm.name, count(c) AS concept_count
ORDER BY p.subject_name, dm.mode_id

// Concepts needing physical materials
MATCH (c:Concept)-[:HAS_TEACHING_REQUIREMENT]->(tr:TeachingRequirement {requirement_id: 'TR-PHY'})
RETURN c.concept_id, c.concept_name

// Platform addressable surface (AI Direct + AI Facilitated)
MATCH (c:Concept)-[:DELIVERABLE_VIA {primary: true}]->(dm:DeliveryMode)
WHERE dm.mode_id IN ['DM-AI', 'DM-AF']
RETURN count(c) AS platform_teachable
```

---

## QA Process

1. Classification script generates initial assignments using rule-based + signal analysis
2. Per-subject JSON files are human-reviewable
3. Teacher panel review (V8) validates boundary cases
4. Music, Art, DT, and English composition warrant closest teacher scrutiny

---

## Dependencies

- Requires: UK Curriculum (concepts must exist)
- Optionally reads: DifficultyLevel, RepresentationStage, ConceptCluster, ThinkingLens
- Import order: Run AFTER all other curriculum enrichment layers
