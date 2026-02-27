# UK Curriculum as a Knowledge Graph

A machine-readable specification of the England National Curriculum (EYFS through KS4, ages 4-16) stored as a Neo4j knowledge graph. The graph serves as an [intermediate representation](docs/design/PROJECT_DIRECTION.md#what-this-repo-is) from which [teacher planners](docs/design/OUTPUT_SCHEMAS.md#schema-a-teacher-planner), [LLM session prompts](docs/design/OUTPUT_SCHEMAS.md#schema-b-llm-child-session-prompt), and [parent guides](docs/design/OUTPUT_SCHEMAS.md#schema-c-parent-home-educator-guide) can be compiled. This is an [R&D project](docs/design/PROJECT_DIRECTION.md#what-this-repo-is-not), not a shipping product.

**Why a graph?** Curriculum is a [dependency structure](docs/design/PROJECT_DIRECTION.md#the-starting-observation): fractions depend on place value, rivers depend on the water cycle, reading comprehension depends on decoding. A flat topic list loses this structure. A graph preserves it -- and makes it queryable for [prerequisite-aware sequencing](docs/design/RESEARCH_BRIEFING.md#aleks), [spacing and interleaving](docs/design/RESEARCH_BRIEFING.md#spacing-and-interleaving-bjork), and differentiation.

**Why "compiler"?** The graph doesn't contain lessons. It contains the specification from which lessons can be assembled. Different [compilation targets](docs/design/OUTPUT_SCHEMAS.md) query subsets of the graph and render outputs for different audiences: teachers get [planners](docs/design/OUTPUT_SCHEMAS.md#schema-a-teacher-planner), LLMs get [structured session prompts](docs/design/OUTPUT_SCHEMAS.md#schema-b-llm-child-session-prompt), parents get [step-by-step guides](docs/design/OUTPUT_SCHEMAS.md#schema-c-parent-home-educator-guide). Same data, [three outputs](docs/design/OUTPUT_SCHEMAS.md#comparison-what-each-schema-pulls-from-the-graph).

For the full rationale, architecture direction, and honest assessment of what's built vs planned: **[`docs/design/PROJECT_DIRECTION.md`](docs/design/PROJECT_DIRECTION.md)**.

---

## What's in the graph

~10,675 nodes, ~23,740+ relationships in a Neo4j instance.

### Curriculum structure

The [foundation layer](layers/uk-curriculum/README.md) encodes the statutory England National Curriculum as a queryable graph. Every node traces back to a [DfE source document](https://www.gov.uk/government/collections/national-curriculum).

| Layer | Count | What it encodes | Details |
|---|---|---|---|
| Programmes | 55+ | One per subject x key stage | [UK curriculum layer](layers/uk-curriculum/README.md#graph-structure) |
| Domains | 316 | Strand/topic groupings within each programme | [UK curriculum layer](layers/uk-curriculum/README.md#node-types) |
| Objectives | 1,559+ | Statutory and non-statutory requirements | [Source traceability](layers/uk-curriculum/README.md#source-document-traceability) |
| Concepts | 1,351 | Teachable/testable units of knowledge, skill, or process | [Key properties](layers/uk-curriculum/README.md#key-properties) |
| Prerequisites | 1,354+ rels | Dependency chain with confidence, type, strength, rationale | [Cross-KS linking](layers/uk-curriculum/README.md#notes) |
| EYFS | 53 concepts | Early Years (Reception), with [34 cross-stage links to KS1](layers/eyfs/README.md#graph-integration) | [EYFS layer](layers/eyfs/README.md) |

### Enrichment layers (what makes it compilable)

These layers turn raw curriculum structure into data dense enough to [compile into teacher materials](docs/design/PROJECT_DIRECTION.md#the-teacher-planner-first-compilation-target) and (eventually) [child-facing session prompts](docs/design/OUTPUT_SCHEMAS.md#schema-b-llm-child-session-prompt).

| Layer | Count | What it encodes | Details |
|---|---|---|---|
| [DifficultyLevel](layers/uk-curriculum/README.md) | 4,952 nodes | Grounded tiers per concept (entry -> greater_depth / emerging -> mastery) with example tasks, model responses, common errors | [How planners use them](docs/design/OUTPUT_SCHEMAS.md#output-contract) |
| [RepresentationStage](layers/uk-curriculum/README.md) | ~462 nodes | [CPA](https://en.wikipedia.org/wiki/Concrete%E2%80%93Pictorial%E2%80%93Abstract_approach) (Concrete-Pictorial-Abstract) for primary maths, with resources and transition cues | [Parent guide converts to household materials](docs/design/OUTPUT_SCHEMAS.md#why-llm-generation-is-necessary-for-this-output) |
| [DeliveryMode](docs/design/PLAN_DELIVERY_MODE_CLASSIFICATION.md) | 4 nodes, 1,351 rels | AI teachability: [79% of concepts AI-addressable](docs/design/PLAN_DELIVERY_MODE_CLASSIFICATION.md#purpose) (59.5% AI Direct, 19.5% AI Facilitated) | [Classification rules](docs/design/PLAN_DELIVERY_MODE_CLASSIFICATION.md#classification-rules) |
| [ConceptCluster](layers/uk-curriculum/README.md) | 626 nodes | Lesson-sized groupings with sequencing, co-teachability, thinking lens assignments | [How session prompts use them](docs/design/OUTPUT_SCHEMAS.md#schema-b-llm-child-session-prompt) |
| [ThinkingLens](layers/uk-curriculum/README.md) | 10 nodes, 1,222 rels | Cross-subject cognitive frames with [age-banded prompts](layers/uk-curriculum/README.md) per key stage | [Lens requirement in session prompts](docs/design/OUTPUT_SCHEMAS.md#output-contract-1) |
| [Per-subject ontology](layers/topic-suggestions/README.md) | 605 nodes | Typed study/unit/reference nodes ([HistoryStudy](layers/topic-suggestions/README.md), [GeoStudy](layers/topic-suggestions/README.md), [ScienceEnquiry](layers/topic-suggestions/README.md), etc.) | [Subject-specific metadata](layers/topic-suggestions/README.md) |
| [VehicleTemplate](layers/topic-suggestions/README.md) | 24 nodes | Reusable pedagogical patterns with age-banded agent prompts | [Session structure in prompts](docs/design/OUTPUT_SCHEMAS.md#output-contract-1) |
| [Epistemic skills](layers/epistemic-skills/README.md) | 105 nodes | Disciplinary skills ([Working Scientifically](layers/epistemic-skills/README.md#node-types-skill-types), [Historical Thinking](layers/epistemic-skills/README.md#node-types-skill-types), etc.) | [Progression modelling](layers/epistemic-skills/README.md#progression-modeling) |
| [Learner profiles](layers/learner-profiles/README.md) | 71 nodes | Age-appropriate [interaction types](layers/learner-profiles/README.md#interactiontype-29-nodes-shared), [content guidelines](layers/learner-profiles/README.md#contentguideline-9-nodes-one-per-year), [pedagogy](layers/learner-profiles/README.md#pedagogyprofile-9-nodes-one-per-year) and [feedback profiles](layers/learner-profiles/README.md#feedbackprofile-9-nodes-one-per-year) | [Research basis](docs/design/RESEARCH_BRIEFING.md) |
| [Assessment](layers/assessment/README.md) | 268 codes | KS2 test framework [content domain codes](layers/assessment/README.md#content-domain-codes) | [Curriculum-to-test alignment](layers/assessment/README.md#integration-points) |
| [CASE standards](layers/case-standards/README.md) | 1,783 items | US comparison: [NGSS](layers/case-standards/README.md#ngss-next-generation-science-standards), [Common Core Math](layers/case-standards/README.md#common-core-mathematics) | [Cross-layer alignments](layers/case-standards/README.md#cross-layer-alignments) |

### Subject coverage

**[EYFS](layers/eyfs/README.md):** Communication & Language, PSED, Physical Development, Literacy, Mathematics, Understanding the World, Expressive Arts & Design

**[KS1-KS2](layers/uk-curriculum/README.md):** Art & Design, Computing, Design & Technology, English, Geography, History, Languages, Mathematics, Music, Physical Education, Science

**[KS3](layers/uk-curriculum/README.md):** Art & Design, Citizenship, Computing, Design & Technology, English, Geography, History, Languages, Mathematics, Music, Physical Education, Science

**[KS4](docs/design/PLAN_POST_KS3.md):** Art & Design, Biology, Business, Chemistry, Citizenship, Computing, Design & Technology, Drama, English Language, English Literature, Food Preparation & Nutrition, Geography, History, Languages (MFL), Mathematics, Media Studies, Music, Physical Education, Physics, Religious Studies

---

## First compilation target: teacher planners

The teacher planner is the [first proof that the graph produces useful artifacts](docs/design/PROJECT_DIRECTION.md#the-teacher-planner-first-compilation-target). It is the lowest-risk target because teachers can evaluate quality directly, the output is deterministic (no LLM), and the feedback loop is fast.

The pipeline is automated: push to `main` triggers a [CI build](.github/workflows/generate-planners.yml) that stands up a fresh Neo4j instance, imports all layers, generates PPTX + DOCX planners for every study node, and publishes a GitHub Release with a downloadable zip.

Each planner exercises most of the graph: concept descriptions, [difficulty levels](docs/design/OUTPUT_SCHEMAS.md#output-contract), [representation stages](docs/design/OUTPUT_SCHEMAS.md#output-contract), [thinking lenses](docs/design/OUTPUT_SCHEMAS.md#output-contract), prerequisite chains, [topic suggestions](docs/design/OUTPUT_SCHEMAS.md#output-contract), [vehicle templates](docs/design/OUTPUT_SCHEMAS.md#output-contract), and [epistemic skills](docs/design/OUTPUT_SCHEMAS.md#output-contract). If the planner reads well, the [underlying data is sound](docs/design/PROJECT_DIRECTION.md#what-the-planner-validates).

```bash
# Generate locally
python3 scripts/generate_all_planners.py --all

# Or use just
just generate
```

Two further compilation targets are [specified but not yet implemented](docs/design/PROJECT_DIRECTION.md#whats-built-vs-whats-planned):

- **[LLM child session prompt](docs/design/OUTPUT_SCHEMAS.md#schema-b-llm-child-session-prompt)** -- assembles a [priority-stacked structured prompt](docs/design/OUTPUT_SCHEMAS.md#output-contract-1) for an LLM to populate [deterministic question widgets](docs/design/PROJECT_DIRECTION.md#the-local-widget-insight), not conduct a free-form conversation. The prompt encodes [hard constraints](docs/design/OUTPUT_SCHEMAS.md#output-contract-1) (session length, vocabulary level, gamification ban), an [exact output schema](docs/design/OUTPUT_SCHEMAS.md#output-contract-1), [pedagogy algorithm](docs/design/OUTPUT_SCHEMAS.md#output-contract-1) (productive failure, worked examples, interleaving), and [allowed interaction types](docs/design/OUTPUT_SCHEMAS.md#output-contract-1).

- **[Parent/home educator guide](docs/design/OUTPUT_SCHEMAS.md#schema-c-parent-home-educator-guide)** -- LLM-generated plain-English lesson guide. The LLM converts graph data into [warm, jargon-free prose](docs/design/OUTPUT_SCHEMAS.md#what-the-generated-guide-looks-like-example-structure): [household resource substitution](docs/design/OUTPUT_SCHEMAS.md#why-llm-generation-is-necessary-for-this-output) ("Dienes blocks" -> "dried pasta"), [dialogue scripts for misconceptions](docs/design/OUTPUT_SCHEMAS.md#why-llm-generation-is-necessary-for-this-output), and [adaptive branching](docs/design/OUTPUT_SCHEMAS.md#why-llm-generation-is-necessary-for-this-output) ("if they find it easy" / "if they find it hard").

See the [comparison table](docs/design/OUTPUT_SCHEMAS.md#comparison-what-each-schema-pulls-from-the-graph) showing exactly what graph data each target uses, and the [implementation order](docs/design/OUTPUT_SCHEMAS.md#implementation-order).

---

## Graph model (v4.3)

### Core curriculum
```
Curriculum
  +--[HAS_KEY_STAGE]--> KeyStage
       +--[HAS_YEAR]--> Year --[PRECEDES]--> Year
            +--[HAS_PROGRAMME]--> Programme --[FOR_SUBJECT]--> Subject
                  +--[HAS_DOMAIN]--> Domain
                  |     +--[CONTAINS]--> Objective --[TEACHES]--> Concept
                  |     +--[HAS_CLUSTER]--> ConceptCluster
                  |     |     +--[GROUPS]--> Concept
                  |     |     +--[SEQUENCED_AFTER]--> ConceptCluster
                  |     |     +--[APPLIES_LENS {rank, rationale}]--> ThinkingLens
                  |     +--[HAS_SUGGESTION]--> HistoryStudy / GeoStudy / ScienceEnquiry / ...
                  |           +--[DELIVERS_VIA {primary}]--> Concept
                  +--[HAS_CONCEPT]--> Concept
                  |                    <--> [PREREQUISITE_OF]
                  |                    <--> [CO_TEACHES]
                  |                    +--[HAS_DIFFICULTY_LEVEL]--> DifficultyLevel
                  |                    +--[HAS_REPRESENTATION_STAGE]--> RepresentationStage
                  |                    +--[DELIVERABLE_VIA {primary, confidence, rationale}]--> DeliveryMode
                  |                    +--[HAS_TEACHING_REQUIREMENT]--> TeachingRequirement
                  +--[DEVELOPS_SKILL]--> WorkingScientifically / ReadingSkill / ...

ThinkingLens --[PROMPT_FOR {agent_prompt, question_stems}]--> KeyStage
VehicleTemplate --[TEMPLATE_FOR {agent_prompt}]--> KeyStage
TeachingRequirement --[IMPLIES_MINIMUM_MODE]--> DeliveryMode
```

### [Learner profiles](layers/learner-profiles/README.md) (linked from Year)
```
Year --[HAS_CONTENT_GUIDELINE]--> ContentGuideline
     --[HAS_PEDAGOGY_PROFILE]--> PedagogyProfile --[USES_TECHNIQUE]--> PedagogyTechnique
     --[HAS_FEEDBACK_PROFILE]--> FeedbackProfile
     --[SUPPORTS_INTERACTION]--> InteractionType --[PRECEDES]--> InteractionType
```

### [Assessment](layers/assessment/README.md) + [CASE standards](layers/case-standards/README.md)
```
TestFramework --[HAS_PAPER]--> TestPaper --[INCLUDES_CONTENT]--> ContentDomainCode
Framework --[HAS_DIMENSION]--> Dimension --[HAS_PRACTICE]--> Practice --[ALIGNS_TO]--> Concept
```

---

## Setup

### Prerequisites
- Python 3.10+
- Neo4j 5.x (local or Aura cloud)
- `pip install -r requirements.txt`

### Build the graph
```bash
export NEO4J_URI="neo4j://127.0.0.1:7687"  # or neo4j+s://xxx.databases.neo4j.io
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your-password"

python3 core/scripts/create_schema.py
python3 core/scripts/import_all.py
python3 core/scripts/validate_schema.py
```

The [orchestrator](core/README.md) (`import_all.py`) handles dependency order. Use `--skip-case` or `--skip-oak` to exclude optional layers. See [`CLAUDE.md`](CLAUDE.md) for the full manual import sequence.

### Local development with [just](https://github.com/casey/just)
```bash
just build          # schema + import + validate
just generate       # all planners (md + pptx + docx)
just generate-md    # markdown only (fast)
just clean          # remove generated binaries
```

---

## Example queries

**Prerequisites for a concept (upstream chain)** -- the [dependency graph](docs/design/PROJECT_DIRECTION.md#the-starting-observation) that makes sequencing possible
```cypher
MATCH path = (prereq:Concept)-[:PREREQUISITE_OF*]->(target:Concept {concept_id: 'MA-KS3-C042'})
RETURN path
```

**[Outer fringe](docs/design/RESEARCH_BRIEFING.md#aleks)** -- concepts ready to learn (all prerequisites mastered, from [Knowledge Space Theory](docs/research/SOURCES.md#3-intelligent-tutoring-systems))
```cypher
WITH ['MA-Y4-C001', 'MA-Y4-C002'] AS mastered
MATCH (c:Concept) WHERE NOT c.concept_id IN mastered
AND ALL(p IN [(c)<-[:PREREQUISITE_OF]-(prereq) | prereq.concept_id] WHERE p IN mastered)
RETURN c.concept_name, c.key_stage
```

**Lesson sequence with [thinking lenses](layers/uk-curriculum/README.md)**
```cypher
MATCH (d:Domain {domain_id: 'MA-Y3-D001'})-[:HAS_CLUSTER]->(cc:ConceptCluster)
OPTIONAL MATCH (cc)-[:APPLIES_LENS {rank: 1}]->(lens:ThinkingLens)
RETURN cc.name, cc.cluster_type, lens.name AS thinking_lens
ORDER BY cc.cluster_id
```

**[Difficulty levels](docs/design/OUTPUT_SCHEMAS.md#output-contract) for differentiation**
```cypher
MATCH (c:Concept {concept_id: 'MA-Y3-C014'})-[:HAS_DIFFICULTY_LEVEL]->(dl:DifficultyLevel)
RETURN dl.label, dl.description, dl.example_task, dl.common_errors
ORDER BY dl.level_number
```

**[Delivery mode](docs/design/PLAN_DELIVERY_MODE_CLASSIFICATION.md) distribution for a subject**
```cypher
MATCH (p:Programme)-[:HAS_DOMAIN]->(d:Domain)-[:HAS_CONCEPT]->(c:Concept)
      -[dv:DELIVERABLE_VIA {primary: true}]->(dm:DeliveryMode)
WHERE p.programme_id STARTS WITH 'PROG-Mathematics'
RETURN dm.name, count(c) AS concepts ORDER BY concepts DESC
```

---

## Repository layout

```
layers/                          Layer-based data organization
  uk-curriculum/                 Foundation: curriculum structure + derived layers
    data/extractions/            KS1-KS4 JSONs (55 files)
    data/cluster_definitions/    ConceptCluster definitions per subject
    data/thinking_lenses/        ThinkingLens + age-banded prompts
    data/difficulty_levels/      DifficultyLevel JSONs (148 files)
    data/representation_stages/  RepresentationStage JSONs (12 files)
    data/delivery_modes/         DeliveryMode classification JSONs (62 files)
    scripts/                     Import, enrichment, generation scripts
  eyfs/                          Early Years Foundation Stage
  assessment/                    KS2 test frameworks
  epistemic-skills/              Disciplinary skills (6 types)
  topic-suggestions/             Per-subject ontology: typed study nodes + templates
  learner-profiles/              Age-appropriate design constraints
  case-standards/                US standards comparison (NGSS, Common Core)
  visualization/                 Neo4j Bloom perspectives

core/                            Shared infrastructure
  scripts/                       Schema, validation, config, import orchestrator
  migrations/                    Rerunnable enrichment scripts
  compliance/                    Data classification, consent rules, DPIA

scripts/                         Compilation targets (teacher planner renderers)
generated/                       Output artifacts (planners, review reports)
docs/                            Design docs, research, user stories
```

Each layer has its own README: [`uk-curriculum`](layers/uk-curriculum/README.md) | [`eyfs`](layers/eyfs/README.md) | [`assessment`](layers/assessment/README.md) | [`epistemic-skills`](layers/epistemic-skills/README.md) | [`topic-suggestions`](layers/topic-suggestions/README.md) | [`learner-profiles`](layers/learner-profiles/README.md) | [`case-standards`](layers/case-standards/README.md) | [`visualization`](layers/visualization/README.md) | [`core`](core/README.md)

---

## Research foundation

The graph design and platform principles are grounded in learning science. Each claim links to the relevant research document and primary source.

### What the evidence says works

- **[Prerequisite-aware sequencing](docs/design/RESEARCH_BRIEFING.md#aleks).** The "outer fringe" -- always teaching at the boundary of what a student has mastered -- is the key innovation in [ALEKS](docs/research/SOURCES.md#3-intelligent-tutoring-systems) ([Knowledge Space Theory](docs/design/RESEARCH_BRIEFING.md#aleks)). In this graph, it's a Cypher query on the prerequisite chain, not a separate system to build.

- **[Retrieval practice over re-study](docs/design/RESEARCH_BRIEFING.md#retrieval-practice-roediger-karpicke).** Every question is a learning event, not just an assessment event. Testing from memory strengthens retention more than reading or watching -- even when the test is failed. ([Roediger & Karpicke, 2006](docs/research/SOURCES.md#5-cognitive-learning-science))

- **[Productive failure before instruction](docs/design/RESEARCH_BRIEFING.md#productive-failure-kapur).** Presenting a problem *before* explaining the concept produces significantly better conceptual understanding (Cohen's d = 0.36-0.58). The prerequisite graph determines readiness: all prerequisites mastered, target concept not yet learned. ([Sinha & Kapur meta-analysis, 2021](docs/research/SOURCES.md#5-cognitive-learning-science))

- **[Spacing and interleaving](docs/design/RESEARCH_BRIEFING.md#spacing-and-interleaving-bjork).** Spaced, interleaved practice outperforms blocked practice on delayed tests by 30-40%, despite feeling more difficult during learning. ([Bjork, 2011](docs/research/SOURCES.md#5-cognitive-learning-science))

- **[Informational feedback](docs/design/RESEARCH_BRIEFING.md#self-determination-theory-sdt).** Self-comparative feedback ("you were faster than two weeks ago") supports competence without controlling behaviour. Leaderboards and social comparison do not. ([Ryan & Deci, 2000](docs/research/SOURCES.md#4-motivation-and-engagement))

### What the evidence says doesn't work

- **[No gamification](docs/design/RESEARCH_BRIEFING.md#the-failure-of-gamification).** Visible progress bars and leaderboards trigger social comparison. The [2024 "ghost effect" research](docs/research/SOURCES.md#4-motivation-and-engagement) found gamification produces students who are physically present but mentally absent. Extroverted students benefit; introverted students are actively harmed. ([Jose et al., Frontiers in Education](docs/research/SOURCES.md#4-motivation-and-engagement))

- **[No expected rewards](docs/design/RESEARCH_BRIEFING.md#the-overjustification-effect).** Expected tangible rewards for intrinsically interesting activities undermine that motivation. Badges, unlockable games, and earned rewards are consistently net-negative. ([Lepper, Greene & Nisbett, 1973](docs/research/SOURCES.md#4-motivation-and-engagement))

- **[LLMs without structured domain models](docs/design/RESEARCH_BRIEFING.md#llm-tutors-and-natural-language-interaction) hallucinate.** Independent evaluations find [35% of LLM-generated hints](docs/research/SOURCES.md#6-llm-and-ai-tutoring) are too general, incorrect, or solution-revealing. The productive architecture is LLM over structured domain model -- the graph provides curriculum grounding, the LLM provides natural language.

Full research briefing: **[`docs/design/RESEARCH_BRIEFING.md`](docs/design/RESEARCH_BRIEFING.md)** | Annotated bibliography (18 sources): **[`docs/research/SOURCES.md`](docs/research/SOURCES.md)**

---

## Privacy and compliance

This project is designed for an adaptive learning platform serving children (ages 4-14). The core rule: **the AI learns HOW the child learns, not WHO the child is.** Development is governed by the [ICO Children's Code](docs/research/SOURCES.md#7-architecture-and-privacy), UK GDPR, and the project's [own ethical framework](docs/design/CHILD_PROFILE_CONSENT.md#7-ethical-framework-beyond-legal-compliance).

No learner data exists in this repository. The graph contains only curriculum design metadata. Compliance documents define the rules for any future system that processes learner data:

| Document | What it covers |
|---|---|
| **[`DATA_CLASSIFICATION.md`](core/compliance/DATA_CLASSIFICATION.md)** | [4-tier data classification](core/compliance/DATA_CLASSIFICATION.md#tier-0-identity): identity (Tier 0) is architecturally separated from [learning events](core/compliance/DATA_CLASSIFICATION.md#tier-1-learning-events) (Tier 1). [Prohibited data](core/compliance/DATA_CLASSIFICATION.md#prohibited-never-collected-under-any-circumstances) (emotional state, interests, device fingerprints) is never collected. |
| **[`CONSENT_RULES.md`](core/compliance/CONSENT_RULES.md)** | [5 unbundled consent purposes](core/compliance/CONSENT_RULES.md#1-consent-purposes-unbundled): adaptive learning, teacher sharing, analytics, camera/mic, safety. Each with separate toggle and [lawful basis](core/compliance/CONSENT_RULES.md#1-consent-purposes-unbundled). |
| **[`CHILD_PROFILE_CONSENT.md`](docs/design/CHILD_PROFILE_CONSENT.md)** | Full legal analysis: [which laws apply](docs/design/CHILD_PROFILE_CONSENT.md#1-legal-framework), [the profiling problem](docs/design/CHILD_PROFILE_CONSENT.md#3-the-profiling-problem-our-hardest-compliance-question) (adaptive learning *is* profiling -- our [compelling reason](docs/design/CHILD_PROFILE_CONSENT.md#the-resolution)), [consent verification](docs/design/CHILD_PROFILE_CONSENT.md#4-consent-verification-how-we-know-its-the-parent), [data architecture](docs/design/CHILD_PROFILE_CONSENT.md#8-practical-architecture-for-compliance), [what we refuse to build](docs/design/CHILD_PROFILE_CONSENT.md#73-what-we-refuse-to-build-even-if-legal). |

See also the [research sources on children's data protection](docs/research/SOURCES.md#8-privacy-compliance-and-consent-added-2026-02-20).

---

## Documentation guide

**Start here:**

| Document | What you'll learn |
|---|---|
| **[`PROJECT_DIRECTION.md`](docs/design/PROJECT_DIRECTION.md)** | [Why this repo exists](docs/design/PROJECT_DIRECTION.md#the-starting-observation), [what it is and isn't](docs/design/PROJECT_DIRECTION.md#what-this-repo-is-not), [the primary boundary](docs/design/PROJECT_DIRECTION.md#the-primary-boundary), [architecture direction](docs/design/PROJECT_DIRECTION.md#architecture-direction), [what's built vs planned](docs/design/PROJECT_DIRECTION.md#whats-built-vs-whats-planned) |
| **[`OUTPUT_SCHEMAS.md`](docs/design/OUTPUT_SCHEMAS.md)** | [Teacher planner spec](docs/design/OUTPUT_SCHEMAS.md#schema-a-teacher-planner), [LLM session prompt spec](docs/design/OUTPUT_SCHEMAS.md#schema-b-llm-child-session-prompt), [parent guide spec](docs/design/OUTPUT_SCHEMAS.md#schema-c-parent-home-educator-guide), [comparison table](docs/design/OUTPUT_SCHEMAS.md#comparison-what-each-schema-pulls-from-the-graph), [token budgets](docs/design/OUTPUT_SCHEMAS.md#token-budget-estimates) |
| **[`RESEARCH_BRIEFING.md`](docs/design/RESEARCH_BRIEFING.md)** | [Knowledge tracing models](docs/design/RESEARCH_BRIEFING.md#1-learner-modelling-and-knowledge-tracing), [ITS systems review](docs/design/RESEARCH_BRIEFING.md#3-intelligent-tutoring-systems-its), [motivation science](docs/design/RESEARCH_BRIEFING.md#4-motivation-and-engagement-what-the-evidence-actually-says), [cognitive learning science](docs/design/RESEARCH_BRIEFING.md#5-novel-approaches-being-ignored-by-mainstream-edtech), [what has evidence vs what's hype](docs/design/RESEARCH_BRIEFING.md#what-is-hype-vs-what-has-evidence) |

**Design decisions:**

| Document | What it covers |
|---|---|
| [`INTERACTION_MODES.md`](docs/design/INTERACTION_MODES.md) | [10 interaction modes](docs/design/INTERACTION_MODES.md#implementation-summary) beyond typing: [manipulatives](docs/design/INTERACTION_MODES.md#mode-4-manipulatives-draggable-objects), [animation scrubbing](docs/design/INTERACTION_MODES.md#mode-5-animation-scrubbing-video-timeline-control), [spatial exploration](docs/design/INTERACTION_MODES.md#mode-6-spatial-exploration-3d-environment), [AR](docs/design/INTERACTION_MODES.md#mode-10-augmented-reality-ar-overlay), etc. |
| [`PLAN_DELIVERY_MODE_CLASSIFICATION.md`](docs/design/PLAN_DELIVERY_MODE_CLASSIFICATION.md) | [4 delivery modes](docs/design/PLAN_DELIVERY_MODE_CLASSIFICATION.md#deliverymode-4-nodes), [15 teaching requirements](docs/design/PLAN_DELIVERY_MODE_CLASSIFICATION.md#teachingrequirement-15-nodes), [classification rules](docs/design/PLAN_DELIVERY_MODE_CLASSIFICATION.md#classification-rules), [subject-specific rules](docs/design/PLAN_DELIVERY_MODE_CLASSIFICATION.md#subject-specific-rules) |
| [`CHILD_PROFILE_CONSENT.md`](docs/design/CHILD_PROFILE_CONSENT.md) | [Legal framework](docs/design/CHILD_PROFILE_CONSENT.md#1-legal-framework), [data tiers](docs/design/CHILD_PROFILE_CONSENT.md#2-what-we-need-to-know-about-the-child-data-tiers), [profiling justification](docs/design/CHILD_PROFILE_CONSENT.md#3-the-profiling-problem-our-hardest-compliance-question), [ethical framework](docs/design/CHILD_PROFILE_CONSENT.md#7-ethical-framework-beyond-legal-compliance) |
| [`PLAN_POST_KS3.md`](docs/design/PLAN_POST_KS3.md) | KS4 extension: phased approach, GCSE layer architecture |
| [`PLAN_EYFS_INTEGRATION.md`](docs/design/PLAN_EYFS_INTEGRATION.md) | EYFS design rationale: play-based pedagogy, cross-stage linking |

**Research:** [`docs/research/SOURCES.md`](docs/research/SOURCES.md) (annotated bibliography), [`docs/research/learning-science/`](docs/research/learning-science/) (16 papers by theme), [`docs/README.md`](docs/README.md) (full navigation guide)

**For AI agents:** [`CLAUDE.md`](CLAUDE.md) (full architecture, import pipeline, conventions, compliance rules)

## Data sources

**UK National Curriculum (England):** [DfE programmes of study (2013)](https://www.gov.uk/government/collections/national-curriculum) | [KS2 Maths test framework (2016)](https://www.gov.uk/government/publications/key-stage-2-mathematics-test-framework) | [KS2 Reading test framework (2016)](https://www.gov.uk/government/publications/key-stage-2-english-reading-test-framework) | [KS2 GPS test framework (2016)](https://www.gov.uk/government/publications/key-stage-2-english-grammar-punctuation-and-spelling-test-framework) | [EYFS statutory framework](https://www.gov.uk/government/publications/early-years-foundation-stage-framework--2) | [Development Matters](https://www.gov.uk/government/publications/development-matters--2)

**US Standards (comparison layer):** [NGSS](https://www.nextgenscience.org/) and [Common Core Math](http://www.corestandards.org/Math/) via [OpenSALT](https://opensalt.net) CASE packages
