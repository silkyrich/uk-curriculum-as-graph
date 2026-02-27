# Project Direction

**What this repo is, why it exists, and where it's heading.**

---

## The starting observation

Most edtech platforms treat curriculum as a flat catalogue: a list of topics with some loose ordering. The student picks a topic, works through exercises, and the system tracks completion. This is the IXL model, and it works well enough for drill-and-practice on isolated skills.

But curriculum is not flat. The England National Curriculum is a dependency graph: fractions depend on place value, which depends on counting. Rivers depend on the water cycle, which depends on states of matter. Reading comprehension depends on decoding, which depends on phonics. These dependencies cross subject boundaries, span years, and create non-obvious bottlenecks.

The pre-AI edtech stack couldn't exploit this structure because the content was handcrafted. Each exercise was authored, reviewed, illustrated, and published as a fixed unit. The curriculum graph was implicit -- locked inside the heads of experienced teachers and curriculum designers -- because there was no way to compile it into materials at scale.

LLMs change the economics. If you can describe what to teach precisely enough, the model can draft the materials. The bottleneck shifts from content authoring to curriculum specification: knowing exactly what to teach, in what order, at what difficulty, using what representations, avoiding what misconceptions.

That's what this repo is: a machine-readable specification of the England National Curriculum dense enough to drive automated content generation.

---

## What this repo is

A **curriculum compiler** -- an intermediate representation (IR) of the England National Curriculum stored as a Neo4j knowledge graph, with compilation targets that produce teacher-facing and (eventually) child-facing artifacts.

The graph encodes:

- **Structure**: Key stages, years, subjects, programmes, domains, objectives, concepts (1,351 concepts across EYFS through KS4, 55 subjects)
- **Dependencies**: 1,354+ prerequisite relationships with confidence, type, strength, and rationale -- enabling sequencing and prerequisite gating
- **Difficulty tiers**: 4,952 DifficultyLevel nodes with grounded descriptions, example tasks, model responses, and common errors per level -- enabling differentiation
- **Representation stages**: CPA (Concrete-Pictorial-Abstract) progression for 154 primary maths concepts -- encoding the tools-and-transition journey
- **Delivery readiness**: Every concept classified by what combination of AI, teacher, and specialist expertise is needed to teach it (79% AI-addressable)
- **Pedagogical patterns**: 24 VehicleTemplates with age-banded prompts, 10 ThinkingLens cognitive frames, 326 typed study/unit nodes with subject-specific metadata
- **Lesson grouping**: 626 ConceptClusters with sequencing, co-teachability signals, and thinking lens assignments
- **Age-appropriate constraints**: Learner profiles (interaction types, content guidelines, pedagogy profiles, feedback rules) per year group
- **Disciplinary skills**: 105 epistemic skills across 6 subject types, linked at both programme and concept level

The graph is the shared IR. Different compilation targets query subsets of the graph and assemble outputs for different audiences.

---

## What this repo is not

- **Not a shipping product.** This is R&D. The graph and its compilation pipeline are exploratory. Nothing here is deployed to end users.
- **Not an LLM application.** The graph is the structured layer *under* LLM generation, not an LLM output. Some data was initially drafted using LLMs, but all of it has been through structured extraction, validation, and teacher review. The compilation targets are deterministic queries, not prompts.
- **Not a content library.** The graph doesn't contain lessons. It contains the specification from which lessons can be compiled.

---

## The teacher planner: first compilation target

The teacher planner is the first practical proof that the graph produces useful artifacts. It is the lowest-risk compilation target because:

1. **The audience is professional.** Teachers can evaluate quality, identify errors, and compensate for gaps. A wrong difficulty level in a planner is a nuisance. A wrong difficulty level in a child session is a pedagogical failure.
2. **The output is deterministic.** No LLM in the loop -- the planner is assembled by querying the graph and rendering markdown/PPTX/DOCX. Bugs are reproducible and fixable.
3. **The feedback loop is fast.** A teacher can read a planner and tell you what's wrong in minutes. A child session requires setting up an adaptive engine, running sessions, and analysing interaction data.

The teacher planner pipeline is now automated via CI/CD: push to main triggers a full graph build (Neo4j service container), planner generation, and GitHub Release with downloadable PPTX/DOCX archives.

### What the planner validates

Each generated planner exercises most of the graph's layers: concept descriptions, difficulty levels, representation stages, thinking lenses, prerequisite chains, co-teachability signals, topic suggestions with subject-specific metadata, vehicle templates, and epistemic skills. If the planner reads well, the underlying data is sound. If it doesn't, the graph needs fixing -- not the renderer.

---

## The primary boundary

Primary education (EYFS through KS2, ages 4-11) is where the graph has highest coverage and where AI content generation is most viable:

- **100% concept coverage** for Mathematics, Science, Computing, English
- **100% AI-addressable** for Mathematics and Computing (no specialist teacher or physical resource requirements)
- **DifficultyLevel coverage** for all primary subjects (1,296 of 1,351 concepts)
- **RepresentationStage coverage** for all primary maths (154 concepts, CPA framework)
- **Per-subject ontology** with typed study nodes, cross-curricular links, and pedagogical metadata

Secondary (KS3-KS4) is a routing and constraint layer. The graph covers it -- all subjects extracted, difficulty levels generated, delivery modes classified -- but the pedagogical metadata is thinner and the delivery mode classification shows why: Drama is 0% AI-addressable, PE is 12%, and the subjects that are AI-addressable at secondary level (Maths, Science, Computing) require more sophisticated assessment than primary.

The practical implication: the first child-facing compilation targets will be primary, where the graph is densest and the risk is lowest.

---

## Architecture direction

### The local-widget insight

The most important architectural decision, not yet implemented, is that child-facing interactions should be **deterministic question widgets rendered on-device**, not free-form LLM conversations.

The graph already encodes the interaction types each year group supports (33 InteractionTypes: phoneme splitter, bus stop division, fraction wall, drag-to-categorise, etc.). Each is a small, self-contained UI component with defined inputs and outputs. The LLM's job is to populate the widget parameters -- not to conduct a conversation.

This matters because:

- **Deterministic widgets emit clean event streams.** A drag-to-categorise widget produces `{item: "whale", target: "mammal", correct: true, time_ms: 2400}`. An LLM conversation produces ambiguous natural language that requires interpretation.
- **Knowledge tracing needs structured events.** BKT, PFA, and graph-based KT models require binary or graded skill observations. Widgets produce these directly.
- **Safety is compositional.** Each widget can be reviewed, tested, and certified independently. An open-ended LLM conversation requires runtime safety monitoring that is harder to validate.

### The compilation stack (not yet built)

```
Graph (IR)
  |
  v
Session query: (cluster_id, difficulty_target, topic_suggestion_id) -> context
  |
  v
Compilation target: Teacher Planner | LLM Session Prompt | Parent Guide
  |                                   |                      |
  v                                   v                      v
Deterministic render               LLM populates           LLM generates
(md/pptx/docx)                    widget parameters        plain-English guide
                                       |
                                       v
                                  Widget runtime
                                  (on-device, deterministic)
                                       |
                                       v
                                  Event stream
                                  (to knowledge tracing)
```

The three compilation targets are specified in [`docs/design/OUTPUT_SCHEMAS.md`](OUTPUT_SCHEMAS.md). They share a single underlying graph query; the difference is what subset of the graph they pull and how they render it.

---

## What validation has been done

### Teacher panel reviews

Three rounds of simulated teacher panel review (V4, V5, V7), each with 8-9 persona-based evaluations across primary subjects. The V7 review (with DifficultyLevels, per-subject ontology, and ThinkingLenses) scored average content generation readiness at 7.2/10, up from 6.6/10 in V5. DifficultyLevels were identified as the highest-leverage addition by 9/9 reviewers.

### Automated validation

`validate_schema.py` runs 40+ integrity checks covering node completeness, relationship integrity, property completeness, and cross-layer consistency. The CI pipeline runs this on every push.

### What hasn't been validated

- No real teacher has seen the generated planners (simulated review only)
- No child has used any output from this graph
- The adaptive engine (knowledge tracing, sequencing) does not exist yet
- The LLM session prompt (Schema B) has not been tested end-to-end
- The parent guide (Schema C) has not been generated or evaluated

These are honest gaps. The graph is an R&D artifact; its fitness for production use is unproven.

---

## Open questions

1. **Misconception structure.** Misconceptions are currently prose fields on Concept nodes and structured `common_errors` arrays on DifficultyLevel nodes. For the LLM session prompt to reliably surface misconceptions as distractor options and counter-prompts, these likely need to become first-class nodes with `symptom`, `counter_prompt`, and `distractor_template` fields. This is a significant extraction effort (~1,300 concepts).

2. **Knowledge tracing model.** The research briefing (`docs/design/RESEARCH_BRIEFING.md`) recommends hierarchical BKT as the starting point, with graph-based KT (GKT) as the target once interaction data exists. The prerequisite graph is the natural input to both. No implementation exists.

3. **Session routing.** Given a student's current mastery state, which cluster do you teach next? The outer-fringe query (all prerequisites mastered, target not yet learned) is a starting point, but real routing needs to balance spacing, interleaving, and motivational factors. This is the adaptive engine, and it doesn't exist yet.

4. **Secondary depth.** KS3-KS4 coverage is structurally complete but pedagogically thin compared to primary. Whether to deepen it (more study nodes, richer teaching guidance) or leave it as a routing layer depends on whether the platform ever targets secondary directly.

---

## What's built vs what's planned

| Component | Status | Notes |
|---|---|---|
| Knowledge graph (EYFS-KS4) | Built | ~10,675 nodes, ~23,740+ relationships |
| Difficulty levels | Built | 4,952 nodes across 1,296 concepts |
| Representation stages | Built | 462 nodes across 154 primary maths concepts |
| Delivery readiness | Built | All 1,351 concepts classified |
| Per-subject ontology | Built | 326 study nodes, 255 reference nodes, 24 templates |
| Teacher planner pipeline | Built | CI/CD: push to main -> GitHub Release |
| LLM session prompt assembly | Specified | Schema in OUTPUT_SCHEMAS.md, not implemented |
| Parent guide generation | Specified | Schema in OUTPUT_SCHEMAS.md, not implemented |
| Widget runtime | Not started | Architecture direction only |
| Knowledge tracing | Not started | Research complete, no implementation |
| Adaptive engine (routing) | Not started | Outer-fringe query exists as proof of concept |
| Real teacher validation | Not started | Simulated reviews only |
| Child-facing sessions | Not started | Requires all of the above |

---

## Related documents

| Document | Relationship |
|---|---|
| [README](../../README.md) | Project overview and setup -- links into this document for rationale |
| [OUTPUT_SCHEMAS.md](OUTPUT_SCHEMAS.md) | Detailed specs for all three [compilation targets](OUTPUT_SCHEMAS.md#comparison-what-each-schema-pulls-from-the-graph) referenced above |
| [RESEARCH_BRIEFING.md](RESEARCH_BRIEFING.md) | Evidence base for the [pedagogical principles](RESEARCH_BRIEFING.md#5-novel-approaches-being-ignored-by-mainstream-edtech) and [knowledge tracing models](RESEARCH_BRIEFING.md#1-learner-modelling-and-knowledge-tracing) discussed in open questions |
| [SOURCES.md](../research/SOURCES.md) | Annotated bibliography with [18 primary sources](../research/SOURCES.md#summary-table) |
| [PLAN_DELIVERY_MODE_CLASSIFICATION.md](PLAN_DELIVERY_MODE_CLASSIFICATION.md) | Design rationale for the [delivery readiness classification](PLAN_DELIVERY_MODE_CLASSIFICATION.md#classification-rules) that underpins the "79% AI-addressable" claim |
| [CHILD_PROFILE_CONSENT.md](CHILD_PROFILE_CONSENT.md) | [Legal framework](CHILD_PROFILE_CONSENT.md#1-legal-framework) and [ethical constraints](CHILD_PROFILE_CONSENT.md#7-ethical-framework-beyond-legal-compliance) for any future child-facing system |
| [INTERACTION_MODES.md](INTERACTION_MODES.md) | Detailed specs for the [deterministic widget types](INTERACTION_MODES.md#implementation-summary) referenced in the local-widget insight |
| [DATA_CLASSIFICATION.md](../../core/compliance/DATA_CLASSIFICATION.md) | [Data tier definitions](../../core/compliance/DATA_CLASSIFICATION.md#tier-0-identity) for the event-stream architecture |
| [UK curriculum layer](../../layers/uk-curriculum/README.md) | Foundation layer that the graph is built on |
| [Per-subject ontology](../../layers/topic-suggestions/README.md) | Study nodes that [compilation targets query](../../layers/topic-suggestions/README.md#how-compilation-targets-use-this-layer) |
| [Learner profiles](../../layers/learner-profiles/README.md) | Age-appropriate constraints used by [LLM session prompts](OUTPUT_SCHEMAS.md#output-contract-1) |
