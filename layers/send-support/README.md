# SEND Support Layer

## Why This Layer Exists

The UK National Curriculum is designed for all children, but approximately 15% of pupils in England are identified as having Special Educational Needs or Disabilities (SEND). The Children and Families Act 2014 and the SEND Code of Practice (2015) establish a graduated approach to meeting these needs: Assess, Plan, Do, Review.

This layer encodes the **barrier and support** relationships between curriculum concepts and the access requirements they impose, enabling the platform to automatically identify potential barriers and suggest evidence-based support strategies — without requiring specialist teacher knowledge at the point of delivery.

### The Barrier/Support Principle

The core design principle is: **adjust the delivery, not the curriculum**.

Every child should access the same curriculum content. What changes is:
- How information is presented (input)
- How the child demonstrates understanding (output)
- How the task is structured (scaffolding)
- How much time is allowed (pacing)

The SEND layer never modifies WHAT is taught — it modifies HOW it is taught. This aligns with the statutory duty to provide a broad and balanced curriculum to all children, including those with SEND.

## What This Layer Models

### Node Types

| Label | Count | Description |
|---|---|---|
| `NeedArea` | 4 | The four statutory SEND areas from the Code of Practice |
| `AccessRequirement` | 16 | Barriers that curriculum concepts can impose on learners |
| `SupportStrategy` | 20 | Mitigations the platform can apply to reduce barriers |

### NeedArea (4 nodes)

The four broad areas of need defined by the SEND Code of Practice (2015, section 6.28-6.35):

1. **Communication and Interaction** — SLCN, autism, social communication
2. **Cognition and Learning** — MLD, SLD, SpLD (dyslexia, dyscalculia, dyspraxia)
3. **Social, Emotional and Mental Health** — ADHD, anxiety, attachment, executive function
4. **Sensory and Physical** — VI, HI, physical disability, sensory processing

These are structural anchors, not diagnostic labels. A child may have needs across multiple areas.

### AccessRequirement (16 nodes)

Specific barriers that a curriculum concept can impose on a learner. Each access requirement describes a cognitive, linguistic, physical, or sensory demand that may block access to the learning objective.

Categories:
- **Communication** (3): language_load, vocabulary_novelty, auditory_processing_reliance
- **Literacy** (1): decoding_demand
- **Processing** (2): multi_step_instruction_demand, working_memory_load
- **Executive function** (3): sustained_attention_demand, task_switching_demand, time_pressure
- **Physical** (2): fine_motor_output_demand, handwriting_copying_load
- **Sensory** (2): visual_crowding_dense_layout, sensory_stimulation_load
- **Social** (1): social_inference_demand
- **Conceptual** (2): abstractness_without_concrete_anchor, open_ended_response_demand

Key property: `construct_sensitive` (boolean) — when true, removing the barrier may change what is being assessed. For example, removing decoding demand from a reading lesson removes the learning objective itself.

### SupportStrategy (20 nodes)

Evidence-based mitigations the platform can apply. Organised in three tiers:

- **Universal** (7): benefit all learners, no assessment validity risk — chunked instructions, visual supports, TTS, vocabulary pre-teaching, reduced visual clutter, calm mode, extended processing time
- **Targeted** (12): benefit children with identified needs, conditional construct risk — sentence starters, concrete manipulatives (extended), word bank, alternative response mode, explicit inference teaching, task breakdown with checklist, simplified language wrapper, worked example first, micro-breaks, adaptive difficulty stepping, predictable session structure, scaffolded recording template
- **Specialist** (1): requires human expert — SENCO review flag

Each strategy has:
- `construct_risk` — low, conditional, or high
- `blocked_when_assessing` — array of access_req_ids where the strategy would invalidate assessment
- `prompt_rules` — direct LLM instruction for applying the strategy
- `ui_implications` — platform features needed to implement the strategy

### Relationships

```cypher
// Access requirements tagged to SEND need areas
(:AccessRequirement)-[:TAGGED_AS]->(:NeedArea)

// Support strategies mitigate access requirements
(:SupportStrategy)-[:MITIGATES {strength, notes}]->(:AccessRequirement)
// strength: "strong" | "moderate" | "partial"

// Support strategies commonly used for need areas
(:SupportStrategy)-[:COMMONLY_USED_FOR]->(:NeedArea)

// Concepts have access requirements (from concept_support_links files)
(:Concept)-[:HAS_ACCESS_REQUIREMENT {level, rationale, source}]->(:AccessRequirement)
// level: "low" | "medium" | "high"
```

## What This Layer Does NOT Model

This layer deliberately excludes:

- **Individual learner profiles** — no child data, no diagnostic labels, no personal information
- **EHCP content** — Education, Health and Care Plans are legal documents maintained by local authorities, not graph data
- **Diagnostic categories** — the layer uses barrier-based modelling, not diagnosis-based modelling. A child is not "dyslexic" in the graph; specific concepts have "high decoding demand" that the platform can mitigate
- **Behaviour management** — SEMH needs are modelled as cognitive/executive function barriers, not behavioural challenges
- **Medical information** — no health data, medication schedules, or clinical assessments
- **Staffing implications** — the layer models what the platform can do, not what humans should do

## V1 Scope

The v1 release covers:

- **All 4 need areas** from the SEND Code of Practice
- **16 access requirements** covering the primary barrier categories
- **20 support strategies** across universal, targeted, and specialist tiers
- **Concept support links** for primary maths (Y1-Y4), primary English (KS1-Y4), and primary science (KS1-KS2)
- Approximately 130 concept-barrier annotations across the three subjects

### Future Phases

- **Phase 2**: Extend concept support links to Y5-Y6 and secondary subjects (KS3-KS4)
- **Phase 3**: Add EYFS-specific access requirements (developmental rather than curriculum-based)
- **Phase 4**: Add cross-concept barrier accumulation analysis (multiple sequential high-barrier concepts)
- **Phase 5**: Teacher/SENCO validation of concept-barrier annotations against real classroom experience

## Safety and Privacy Boundaries

### What this layer stores
- Curriculum metadata about barrier characteristics of concepts (Tier 3: aggregated curriculum analysis)
- No individual learner data
- No diagnostic information
- No personal data of any kind

### What the runtime platform would store (out of scope for this layer)
- A learner's active support strategies would be stored as Tier 0 (identity-adjacent) data
- Any SEND-related preferences are parental consent items under the consent architecture
- See `core/compliance/DATA_CLASSIFICATION.md` and `core/compliance/CONSENT_RULES.md`

### Guard rails
- The platform must NEVER label a child with a diagnostic term based on barrier patterns
- Support strategies are presented to parents, not children — the child experiences adapted delivery seamlessly
- The SENCO review flag (SS-20) routes to a human, never to an automated classification
- Construct-sensitive barriers must be checked before applying support strategies in assessment contexts

## Data Files

| File | Contents |
|---|---|
| `data/need_areas.json` | 4 NeedArea definitions |
| `data/access_requirements.json` | 16 AccessRequirement definitions |
| `data/support_strategies.json` | 20 SupportStrategy definitions |
| `data/concept_support_links/primary_maths.json` | ~48 concept-barrier links for Y1-Y4 maths |
| `data/concept_support_links/primary_english.json` | ~40 concept-barrier links for KS1-Y4 English |
| `data/concept_support_links/primary_science.json` | ~40 concept-barrier links for KS1-KS2 science |

## Import

```bash
# Import SEND support layer (depends on UK curriculum layer)
python3 layers/send-support/scripts/import_send_support.py

# Validate
python3 layers/send-support/scripts/validate_send_support.py
```

## References

- SEND Code of Practice (2015): Sections 6.28-6.35 (areas of need), Chapter 6 (graduated approach)
- Children and Families Act 2014: Part 3 (children with special educational needs)
- Equality Act 2010: Reasonable adjustments duty
- EEF Special Educational Needs in Mainstream Schools (2020): Evidence-based guidance
- Sweller, J. (1988): Cognitive Load Theory — basis for worked examples and chunking
- Bruner, J. (1966): CPA framework — basis for concrete manipulatives strategy
