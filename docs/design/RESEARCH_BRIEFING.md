# Research Briefing: Learner Layer Design
## UK Curriculum-as-Graph Platform — State of the Art Review

**Prepared:** February 2026
**Scope:** Six research areas covering learner modelling, standards, ITS systems, motivation science, cognitive learning science, and architecture

---

## Executive Summary

This briefing synthesises the current state of the art across six domains relevant to designing the learner layer of a Neo4j-backed UK curriculum knowledge graph platform. The platform's already-committed design choices — AI-driven encouragement, semi-random parent notifications, semi-random delight moments, no visible progress bars, no gamification — align well with the evidence base. Several of these decisions are better supported by research than the approaches taken by the mainstream edtech market.

---

## 1. Learner Modelling and Knowledge Tracing

### Bayesian Knowledge Tracing (BKT)

BKT, introduced by Corbett and Anderson in 1994, remains the theoretical backbone of most deployed adaptive learning systems. It models each skill as a hidden binary state — mastered or not — and uses four parameters: prior probability of mastery, probability of learning on each opportunity, probability of a correct response despite non-mastery (guess), and probability of an incorrect response despite mastery (slip). A 2023 systematic review in *User Modeling and User-Adapted Interaction* — covering 25 years of BKT research across 13 enhancement dimensions — found that individualised BKT (where learning rate parameters vary per student) consistently outperforms the vanilla model on prediction accuracy. The expectation-maximisation algorithm has become the de facto standard for parameter estimation.

**What works:** BKT is interpretable, computationally light, and reasonably predictive for single-skill mastery. It pairs naturally with mastery-gated learning (a student stays on a concept until the posterior mastery probability exceeds a threshold, typically 0.95).

**What doesn't:** Vanilla BKT treats each skill as independent, which directly conflicts with a graph-based curriculum where concepts have rich prerequisite dependencies. It also has identifiability problems: multiple parameter combinations can produce identical predictions, and the four-parameter model is underspecified for small datasets. A 2016 analysis by Van de Sande showed the parameters are weakly identified unless the training dataset is large.

**Relevance to this platform:** The prerequisite graph already built in Neo4j encodes exactly the structural information that vanilla BKT ignores. The platform should use a hierarchical or graph-extended variant of BKT rather than flat-skill BKT. Hierarchical BKT (hBKT) — where each student has their own learning rate sampled from a population distribution — is tractable and substantially more accurate. See: Pardos & Heffernan (2010).

### Deep Knowledge Tracing (DKT)

Piech et al.'s 2015 DKT paper applied an LSTM network to the knowledge tracing problem, treating a student's interaction history as a sequence and predicting future performance. It significantly outperformed BKT on the benchmark ASSISTments dataset and triggered a decade of deep-learning-based knowledge tracing research.

Subsequent variants include:
- **DKVMN** (Zhang et al. 2017): dynamic key-value memory networks that maintain a concept-keyed memory matrix, allowing explicit tracking of multiple skills simultaneously
- **AKT** (Ghosh et al. 2020): attention-based knowledge tracing incorporating question context
- **GKT** (Nakagawa et al. 2019, ICLR): Graph-based Knowledge Tracing using graph neural networks to explicitly model concept dependency relationships as directed edges

The 2024 review by Zitao Liu (*IEEE Education Society*) counted 37 papers on deep KT in 2024 alone, with the dominant trend being hybrid/meta models combining attention mechanisms with graph structures.

**What works:** Deep models outperform BKT on large datasets, capture complex temporal patterns, and — in graph variants — can leverage prerequisite structure. DyGKT (2024) extends this to dynamic graphs that evolve as the student learns.

**What doesn't:** Deep KT models are data-hungry. They require thousands of student-skill interaction sequences before outperforming simpler models. For a new platform with a cold-start problem, BKT variants are more defensible. DKT models are also harder to interpret: teachers and parents cannot be shown "the model thinks your child is 73% likely to know fractions" without having some mechanistic explanation.

**Relevance to this platform:** The knowledge graph in Neo4j is a natural input to GKT-style models. Once the platform has sufficient learner interaction data (likely after several thousand student-sessions), a graph-aware deep KT model that uses the existing concept nodes and prerequisite edges as its graph structure would be worth implementing. Until then, hierarchical BKT is the defensible starting point. The critical design insight: **the graph is the curriculum structure; the KT model reads the graph, not a flat skill list**.

### Performance Factor Analysis (PFA) and Item Response Theory (IRT)

PFA (Pavlik, Cen & Koedinger, 2009) extends BKT by modelling success counts and failure counts separately for each knowledge component, making it better suited to items where the cost of a wrong attempt differs from the benefit of a correct one. A 2024 *Frontiers in Education* paper demonstrated that augmenting PFA with attention mechanisms and item similarity significantly improves prediction across polytomous items.

IRT (classical test theory's successor) models item difficulty and student ability as continuous parameters, typically on a logit scale. It is the gold standard for standardised assessment but less suitable for real-time adaptive tutoring because it estimates a static ability rather than a dynamic learning state. A 2022 *Educational Data Mining* paper proposed an Online IRT (OIRT) model that combines IRT with PFA to enable real-time ability estimation as a student progresses.

**Relevance to this platform:** IRT is most valuable for initial placement assessment — estimating where a student sits across the curriculum graph before personalised sequencing begins. PFA is worth considering as an alternative to BKT for knowledge components where the platform has clear binary "opportunity" events (attempted, correct/incorrect). A hybrid: IRT for placement, BKT/PFA for ongoing knowledge tracing.

---

## 2. Educational Knowledge Graph Standards

### xAPI (Experience API / IEEE 9274.1.1-2023)

xAPI — now standardised as IEEE 9274.1.1-2023 (xAPI 2.0, released October 2023) — defines a triple-structure statement format: **Actor → Verb → Object**, stored in a Learning Record Store (LRS). It is the most widely adopted standard for capturing granular learning events across diverse platforms. The standard is governed by the ADL Initiative and maintained by 1EdTech.

**What it offers:** A lingua franca for learner event data. Any event that a learning system generates — "learner X answered question Y correctly", "learner X spent 4 minutes on concept Z" — can be expressed as an xAPI statement and shipped to an LRS for cross-system aggregation. xAPI profiles extend the base vocabulary with domain-specific verbs and activity types.

**What it doesn't offer:** xAPI is a data transport/storage standard, not a knowledge model. It says nothing about curriculum structure, prerequisite relationships, or how to compute mastery. Plugging raw xAPI statements into a KT model still requires significant architectural work.

**Relevance to this platform:** The platform should emit xAPI statements as its canonical learner event format, even if the primary storage is internal. This creates future interoperability (schools wanting to pull learner data into their MIS) and audit capability. The event format maps naturally to the domain model: `{ actor: student_id, verb: "answered", object: question_id, result: { success: true, duration: "PT42S" }, context: { concept_node: "fractions/equivalent" } }`. Storing the Neo4j concept node GUIDs in the context extension field is straightforward.

### CASE (Competencies and Academic Standards Exchange)

1EdTech's CASE specification (v1.0, v1.1) defines a machine-readable format for curriculum frameworks using hierarchically structured CFItems (Curriculum Framework Items) identified by GUIDs. The JSON-LD binding allows curriculum standards to be expressed as linked data. CASE is designed to replace PDF curriculum documents with API-accessible, UUID-identified standards trees.

**What it offers:** A vendor-neutral way to publish a curriculum graph that third-party tools can align to. Publishers, assessment tools, and LMS platforms can pull a CASE document and automatically align their content to the standard.

**What it doesn't offer:** CASE is hierarchical (a tree of standards), not a graph. It does not natively represent prerequisite relationships, co-requisite skills, or epistemic skill types. It is better than the status quo (PDFs), but weaker than a proper knowledge graph.

**Relevance to this platform:** The Neo4j graph is more expressive than CASE. However, publishing a CASE-compatible view of the curriculum graph (flattening prerequisites into parent-child relationships) would allow the platform to be referenced by third-party content aligned to the UK National Curriculum. This is a useful compatibility layer, not the core data model.

### ASN (Achievement Standards Network)

The ASN, originally funded by NSF and now operated by D2L, provides RDF/XML and JSON-LD representations of learning standards. It introduced `asn:Statement` and `asn:StandardDocument` as RDF types, with predicates for prerequisite, related, and broader/narrower relationships. It predates CASE and is now less active, though the Credential Engine Registry has adopted the CTDL-ASN profile for credential alignment.

**Relevance to this platform:** Low. ASN has primarily US standards mapped. It is architecturally similar to CASE but older and less well supported. It is worth knowing about for completeness and for the RDF vocabulary ideas, but the platform does not need to adopt it.

### IMS Global Caliper Analytics

Caliper Analytics (v1.2, 1EdTech) is the counterpart to xAPI in the IMS ecosystem: it defines a structured event vocabulary for learning analytics with typed metric profiles (Assessment, Reading, Forum, Annotation, etc.). Like xAPI, it uses an Actor-Action-Object triple structure. Caliper is more prescriptive about event types than xAPI; xAPI is more widely deployed in K-12.

**Relevance to this platform:** If the platform targets UK MATs (Multi-Academy Trusts) or integrates with platforms that have adopted Caliper (more common in higher education), Caliper events may be required. For a K-12 consumer product, xAPI is the more pragmatic choice.

---

## 3. Intelligent Tutoring Systems (ITS)

### Carnegie Learning / MATHia

MATHia is the commercial descendent of Carnegie Learning's Cognitive Tutor, which was built on ACT-R cognitive theory by John Anderson and colleagues at CMU. It uses model-tracing (matching student actions to a production rule model) and knowledge tracing (BKT) to provide step-level feedback on mathematical problem-solving.

**Evidence:** A 2021 RAND Corporation study — described by Carnegie Learning as "Gold Standard" — found that the blended approach (MATHia plus teacher instruction) nearly doubled growth in performance on standardised tests in the second year of implementation. A 2024 white paper found statistically significant correlations between MATHia's APLSE score and Smarter Balanced summative assessments (r = 0.40–0.56 by grade level). An IES-funded study with Student Achievement Partners found stronger Algebra I effects for students who had completed more MATHia workspaces in middle school, with effects largest for low-prior-attainment students.

**What it gets right:** Step-level feedback (not just answer-level), model tracing that can diagnose specific misconceptions, explicit prerequisite sequencing within the curriculum model, and a blended model that keeps teachers informed.

**What it gets wrong for the UK context:** MATHia is US-curriculum-aligned (Common Core) and costs money per seat in a market where significant free alternatives exist. Its model-tracing approach requires hand-authored production rule models for every problem type — an expensive, brittle knowledge engineering process. It has been criticised for producing anxiety in students who feel "watched" by the system. The UI is utilitarian and the "mastery bar" is prominently visible — exactly the visible progress metric this platform has chosen to avoid.

### ALEKS

ALEKS implements Knowledge Space Theory (KST), a mathematical framework from cognitive science (Doignon & Falmagne, 1985) that models all feasible knowledge states as a lattice. It uses adaptive assessment to efficiently place a student in their knowledge state, then serves items from the "outer fringe" — concepts the student doesn't know but is ready to learn given their current state.

**Evidence:** A 2021 meta-analysis (*Investigations in Mathematics Learning*) found ALEKS performance roughly equivalent to traditional instruction alone (Hedge's g = 0.05), but significantly more effective as a supplement to instruction (g = 0.43). A 2021 MDPI study found that students using ALEKS reported reduced self-regulated learning skills over a semester, suggesting the system may be over-directing learning.

**What it gets right:** The knowledge state lattice is the closest mainstream commercial approach to what this platform has built. The "ready to learn" concept — only showing items whose prerequisites are mastered — is directly applicable. ALEKS's assessment phase is also fast and accurate at placing students.

**What it gets wrong:** KST assumes the knowledge space is static and pre-specified. In practice, the feasible knowledge states must be hand-crafted by subject matter experts, which does not scale to a full national curriculum. The system is also opaque to students; it does not explain why certain items appear. Students cannot see their own knowledge state.

**Relevance to this platform:** The "outer fringe" concept from KST maps directly to the prerequisite graph. A learner is eligible to work on concept C if and only if all prerequisite concepts in the graph have mastery probability above threshold. This is implementable as a Cypher query against the Neo4j graph.

### ASSISTments

ASSISTments (Worcester Polytechnic Institute) is a free platform combining assignment delivery with immediate formative feedback. It has one of the strongest evidence bases in edtech: a 2019 IES Tier 1 study found significant positive effects on middle school mathematics (effect size ~0.18–0.22), one of few edtech systems to achieve this rigour. A controlled study found students learned 12% more with immediate feedback versus delayed feedback (effect size 0.37).

**What it gets right:** The hint system is scaffolded — students can request increasingly specific hints rather than receiving the full answer. Research on the ASSISTments data shows that students who attempt before hinting outperform those who hint first. The platform explicitly tracks and reports on hint usage to inform teacher intervention.

**What it gets wrong:** ASSISTments is teacher-facing, not child-facing. It is designed as a homework and formative assessment tool, not as an adaptive learning engine. Problem sequencing is teacher-controlled, not algorithmically driven.

### Khanmigo (Khan Academy AI)

Khanmigo is Khan Academy's LLM-powered AI tutor, using a Socratic approach: it asks questions rather than giving answers, guiding students toward self-discovery. As of 2024–25, Khanmigo had expanded from 68,000 to 700,000 users in US district partnerships. Common Sense Media rated it 4 stars above other AI tools. A November 2024 Khan Academy efficacy report noted that their platform produces positive learning gains but acknowledged the central challenge: achieving meaningful student engagement.

**Evidence quality:** Limited. Most studies are correlational (time on platform vs. outcomes) rather than causal. The largest challenge with LLM-based tutors for children is that 35% of generated hints in independent studies were too general, incorrect, or solution-revealing (Springer, *IJAIED* 2025). Quality control mechanisms are not yet solved.

**What it gets right:** Conversational, patient, on-demand, no time pressure. The Socratic approach aligns with productive failure principles — guiding students to struggle and discover rather than delivering answers.

**What it gets wrong for UK curriculum context:** Khanmigo is built on US curriculum alignment, conversational (text-heavy) interaction that may not suit younger KS1/KS2 learners, and requires sufficient LLM capability to faithfully model the UK curriculum's specific epistemic skill requirements (WorkingScientifically, HistoricalThinking, etc.). A UK-specific curriculum graph provides the structured domain model that LLM-based tutors typically lack.

**Relevance to this platform:** The most promising near-term architecture is an LLM layer that sits on top of the Neo4j curriculum graph: the graph provides structured knowledge state and prerequisite information; the LLM provides the natural language encouragement, hint generation, and conversational scaffolding. Neither alone is sufficient.

---

## 4. Motivation and Engagement — What the Evidence Actually Says

### Self-Determination Theory (SDT)

Ryan and Deci's SDT is the most robustly evidenced motivational framework in education. It posits three basic psychological needs whose satisfaction drives intrinsic motivation: **autonomy** (feeling volitional control over one's actions), **competence** (feeling effective and capable), and **relatedness** (feeling connected to others). Cross-cultural evidence across decades confirms that environments supporting all three needs produce higher intrinsic motivation, deeper learning, and better wellbeing.

The critical design implication: **extrinsic controls that undermine autonomy — including visible performance tracking, comparative ranking, and mandatory gamification — suppress intrinsic motivation**. "Informational" feedback (you-did-this-well) supports competence and is motivationally safe; "controlling" feedback (you-must-do-better) is damaging.

**Direct alignment with product decisions:** This platform's choice to remove visible progress bars and leaderboards is strongly supported by SDT. The AI encouragement system ("You're on a roll!") delivers informational feedback that supports competence without being controlling. The key word is *informational*: feedback should acknowledge the learner's agency and effort, not compare them to a standard they must meet.

### Growth Mindset (Dweck)

Dweck's mindset theory proposes that students with a "growth mindset" — believing intelligence is developed through effort — respond better to challenge and setback than those with a "fixed mindset". The theory has generated significant implementation interest in edtech.

However, **evidence for mindset interventions is weaker than commonly claimed.** A 2018 meta-analysis found only weak correlations between growth mindset and academic achievement. A 2024 review in *Higher Education* found mixed evidence for scalable mindset interventions. Dweck herself has noted that "maybe we originally put too much emphasis on sheer effort" and that many implementations incorrectly reduce growth mindset to "try harder" without structural support.

**What is well-evidenced:** The specific feedback language matters. Praising effort ("you worked hard on that") over ability ("you're so smart") consistently produces better resilience responses to failure. The 2024 *ScienceDirect* study across 32 OECD countries found that process-focused feedback from teachers and parents mediated growth mindset in digital reading performance. Critically, **parent feedback quality matters as much as system feedback**.

**Relevant design implication:** The AI encouragement system should praise specific, observable effort and process ("You tried three different approaches to that problem") rather than innate ability or comparative rank. The semi-random parent notifications ("Your child just mastered fractions") should similarly be effort-framing ("Your child kept practising until they got it") rather than achievement-announcement.

### The Failure of Gamification

The evidence against conventional gamification in education has become more robust. A 2024 *Frontiers in Education* paper documented the "ghost effect" — students who are physically present but mentally absent, going through gamified motions without cognitive engagement. Their analysis found:

- Point and badge systems encourage superficial, perfunctory engagement
- Competition-focused design creates anxiety and learned helplessness in lower-performing students
- Intrinsic motivation is displaced by extrinsic incentive-seeking
- Extroverted students benefit; introverted students are actively harmed

A systematic mapping in *Information and Software Technology* (2022) reviewed 87 papers finding undesired effects of gamification elements, with badges and leaderboards the most consistently negative elements. A British Journal of Educational Technology meta-analysis (2024) of studies from 2008–2023 found moderate average effect sizes (~0.4) but extreme heterogeneity — positive in some contexts, zero or negative in others.

**The platform decision to remove all visible gamification elements is robustly evidence-supported**, particularly the removal of leaderboards and explicit progress bars. The evidence specifically exonerates two elements this platform *is* using: unexpected positive reinforcement (semi-random delight) and autonomy-supporting features.

### Variable Ratio Reinforcement — Ethical Design

Variable ratio (VR) schedules produce the highest and most persistent response rates in operant conditioning. The mechanism: responses are motivated by anticipation of reward after an *unpredictable* number of actions, creating a slot-machine-like effect. Social media platforms exploit this deliberately; the "likes" on Instagram are a canonical example.

**The ethical distinction is crucial:** VR reinforcement applied to *engagement metrics* (keep scrolling, keep playing) is addictive by design and ethically problematic for children. VR reinforcement applied to *learning progress milestones* — where the reward (a delight moment) is tied to genuine learning events, not arbitrary engagement — is different in kind. The platform's "semi-random delight moments" should be:
1. Always triggered by actual learning events (a concept mastered, a problem chain completed), never by mere time-on-platform
2. Unpredictable in *timing* and *form* (which creates the pleasant surprise), not in whether learning is required to trigger them
3. Designed to support, not interrupt, the learning state

This is the ethical use of variable reinforcement: rewarding genuine learning with occasional unexpected joy, rather than rewarding engagement with addictive unpredictability.

### The Overjustification Effect

The classic Lepper, Greene & Nisbett (1973) study showed that children given expected rewards for drawing — an activity they previously enjoyed spontaneously — lost interest in drawing after rewards were withdrawn. The meta-analytic evidence (Deci et al. 1999, Cameron & Pierce 1994) establishes that **expected, tangible rewards for activities a learner already finds intrinsically interesting reliably undermine that intrinsic motivation**. Unexpected rewards given after task completion do not produce this effect.

**Critical nuance:** Informational feedback that acknowledges competence ("you solved that elegantly") has no undermining effect and can increase intrinsic motivation. The undermining effect is specific to tangible rewards (stickers, points, badges) that are *expected* and *contingent on performance*.

**Alignment with product decisions:** The platform's AI encouragement is informational feedback, not a tangible reward. The delight moments are unexpected. This is precisely the profile that avoids overjustification. The design is doing the right things for the right reasons.

### Flow State (Csikszentmihalyi)

Flow — optimal experience characterised by deep engagement, time distortion, and effortless focus — requires challenge-skill balance. Too difficult → anxiety. Too easy → boredom. The flow channel is the narrow band between these states.

Research within ITS contexts (Springer, 2014; Springer, 2014b) found that boredom is more common for poorly-known material and frustration common for both very difficult *and* very easy material — validating the flow model but also complicating it. Automatic flow detection from interaction data (response time distributions, error rates, help requests) has been a research topic since the early 2010s.

**Practical design implication:** The knowledge tracing model should gate problems to the outer fringe of the learner's mastered concept graph — concepts one step beyond current mastery. This is computationally equivalent to maintaining flow: always working in the zone of proximal development.

### Parental Involvement

A Columbia University study (2017) found that middle and high school parents receiving weekly texts about their child's grades had 18% higher student attendance and 39% reduction in course failures. A 2021 systematic review (*European Journal of Education*) found that technology-mediated parental engagement correlates with positive outcomes, though **no study has yet cleanly established causality from digital notifications to learning gains**.

**What is robustly evidenced:** The quality of parental engagement matters more than quantity. Parents who discuss the *content* of learning ("what did you learn today about fractions?") produce stronger effects than parents who simply monitor grades. The platform's semi-random parent notifications should therefore be content-rich: "Your child spent 20 minutes exploring how fractions relate to division today — you could ask them to show you what they discovered." This prompts qualitative engagement, not just passive monitoring.

---

## 5. Novel Approaches Being Ignored by Mainstream Edtech

### Productive Failure (Kapur)

Productive Failure (PF) is a counter-intuitive instructional sequence: students first attempt to solve a problem using their own methods before receiving instruction. They typically fail, or produce suboptimal solutions. Then instruction is delivered. Students in PF conditions consistently outperform those receiving instruction first on conceptual understanding and transfer tests.

A 2021 meta-analysis (*Review of Educational Research*, Sinha & Kapur) of 53 studies with 166 comparisons found:
- Cohen's d = 0.36 in favour of PF over direct instruction
- At high fidelity to PF principles, Cohen's d = 0.58 (approximately 3x a typical teacher year effect)
- The effect is robust across mathematics and physics; evidence is sparse outside STEM

The mechanism: initial failed attempts activate prior knowledge, generate awareness of knowledge gaps, and prepare cognitive "slots" for incoming instruction. Students who struggle first are primed to learn the canonical solution more deeply.

**Critically ignored by mainstream edtech:** Most adaptive learning platforms sequence instruction before practice. MATHia, ALEKS, Khan Academy all deliver worked examples or explanation before asking students to apply them. This inverts the most effective pedagogical sequence for conceptual learning.

**Direct relevance to this platform:** For conceptual knowledge components (understanding *why* fractions behave as they do), the platform should sequence exploration before exposition. Before introducing a concept through instruction, surface a challenge problem and let the student attempt it, fail, and explore. The prerequisite graph determines when a student is sufficiently prepared to productively fail on a new concept — they need the prerequisite concepts mastered, but not the target concept.

### Retrieval Practice (Roediger & Karpicke)

The testing effect — first robustly demonstrated by Roediger & Karpicke (2006) — establishes that retrieving information from memory strengthens it more than re-studying the same information, even when the test is failed. The mechanism is the strengthening of retrieval routes, not just encoding.

Delayed tests (days or weeks later) show the largest testing effect. Re-reading produces equivalent performance on immediate tests but substantially worse performance on delayed tests. A 2019 review (*Psychological Science in the Public Interest*) confirmed the testing effect is one of the most replicable findings in cognitive psychology.

**What mainstream edtech gets wrong:** Most platforms use retrieval as assessment (to measure mastery), not as the primary learning mechanism. Retrieval *is* the learning — frequent, low-stakes, spaced testing drives long-term retention better than explanatory content.

**Relevance to this platform:** Every question the platform asks is a retrieval practice event, not just an assessment event. The knowledge tracing model should be designed with this in mind: a "failed" retrieval attempt is not just a failure signal, it is a learning event. Post-error correction (showing the right answer with explanation immediately after an error) should be standard. The spacing algorithm (when to next surface a concept) should implement spaced retrieval, not just spaced review.

### Spacing and Interleaving (Bjork)

The spacing effect (distributed practice over time beats massed practice) is among the most replicated findings in memory research. Interleaving (mixing problem types within a session) produces better long-term outcomes than blocking (all practice of one type, then all of another), despite feeling harder and producing lower performance *during* practice.

The Bjork lab has established the "learning vs. performance paradox": conditions that slow apparent learning rate (spacing, interleaving, reduced feedback) often produce superior long-term retention. Students and teachers typically prefer blocked, massed practice because it *feels* more productive in the moment.

**Quantified effects:** Students practising interleaved mixed problem sets outperform blocked practice by 30–40% on delayed tests. For the spacing effect, distributing practice across days with gaps produces retention ~10–30% better than massing the same amount of practice.

**Relevance to this platform:** The problem sequencing algorithm should implement:
1. **Spaced review:** Concepts mastered should be reviewed at increasing intervals (SM-2/FSRS algorithm or equivalent)
2. **Interleaved sessions:** Within-session problem sets should not be blocked by concept; mix recent mastery reviews with new learning on a nearby concept
3. **Honest session design:** Interleaved sessions will feel harder. The platform's encouragement ("You're tackling different types of problems — that's what actually makes you better") should contextualise this difficulty to prevent frustration

### Worked Examples vs. Problem Solving

Cognitive load theory (Sweller, 1988) predicts — and empirical research confirms — that worked examples are optimal for novices because they reduce intrinsic cognitive load, allowing schema formation. As expertise develops, the expertise reversal effect means fully guided instruction becomes redundant and then counter-productive.

**Practical implications:**
- A student encountering a concept type for the first time: start with a worked example, then attempt near-transfer problems
- A student revisiting a previously mastered concept: problem-solving first (productive failure), minimal examples
- The prerequisite graph directly encodes this: distance from the learner's current knowledge frontier determines the optimal instructional mode

This interacts with Kapur's productive failure: PF is not a contradiction of the worked example effect but a different application — PF is used to prime conceptual understanding before canonical instruction, not to replace the instruction itself.

### LLM Tutors and Natural Language Interaction

A 2025 systematic review (*PMC*) of AI-driven ITS in K-12 education found that systems with real-time feedback and personalisation produce medium-to-large effect sizes versus traditional instruction. The frontier is LLM integration.

Current evidence on LLM tutors:
- Positive: conversational, patient, available, can scaffold Socratic questioning, generate novel problem variations, explain in multiple ways
- Negative: 35% of hints in evaluation studies were too general, incorrect, or solution-revealing; LLMs do not natively maintain a persistent student model (each conversation starts fresh without explicit prompting); LLMs can confidently produce incorrect content in niche curriculum areas

The most productive architecture is **LLM over a structured domain model**: the knowledge graph provides the structured curriculum and the learner model (what is known, what is the prerequisite chain, what has been recently attempted); the LLM provides natural language generation for hints, encouragement, and explanation. Neither alone is sufficient for K-12 curriculum-aligned tutoring.

**For children specifically:** Short, warm, curiosity-inviting language outperforms formal instructional language. The platform's design — minimal baseline UI with occasional dramatic delight moments — aligns with research showing that novelty and emotional salience increase encoding (dopamine-mediated memory consolidation is a well-established mechanism).

---

## 6. Learner Domain Architecture

### Separation of Curriculum and Learner Data

Production edtech systems universally separate:
1. **Domain model:** Curriculum structure, concept definitions, prerequisite relationships, item banks, epistemic skill taxonomies — largely static
2. **Learner model:** Per-student knowledge state estimates, interaction history, mastery probabilities — highly dynamic, per-student

For this platform, the Neo4j graph is the domain model. The learner model layer should be architecturally separate, though it reads from and annotates the graph.

The learner model should expose:
- Per-student posterior mastery probability for each concept node
- Recent interaction history (last N events per concept)
- Next-recommended concept(s) from the outer fringe of the mastery graph
- Readiness score for any given concept (proportion of prerequisites mastered above threshold)

### Event-Sourced Learner State

Event sourcing is the architectural pattern where learner state is derived from an append-only log of events rather than stored as mutable state. Each interaction — `QuestionAttempted`, `ConceptMastered`, `SessionStarted`, `HintRequested` — is written to the log. The current learner state is a projection over the event log.

**Advantages for this platform:**
- Auditability: every state change is traceable to a causative event (important for GDPR Article 22, which gives individuals rights regarding automated decisions)
- Replay: if the knowledge tracing model is improved, historical events can be replayed through the new model to recompute current state
- Debugging: support staff can trace exactly why the system served a particular problem ("because concept X posterior = 0.96 and concept Y is on the outer fringe")
- Privacy: selective deletion of events is technically possible without corrupting the event schema

An xAPI-formatted event log effectively implements event sourcing while meeting the interoperability standard simultaneously.

### Privacy and Data Minimisation for Children

Under GDPR (UK GDPR post-Brexit), children receive enhanced protections. The ICO's Age Appropriate Design Code (Children's Code, 2020) applies to online services likely to be accessed by under-18s in the UK and requires:
- Data minimisation: collect only what is strictly necessary for the educational purpose
- Best interests: default privacy settings at the highest level
- No profiling for commercial purposes
- No nudge techniques exploiting children's vulnerabilities

COPPA (US, relevant if the platform has US users) similarly prohibits collecting personal information from under-13s without verifiable parental consent.

**What data you actually need to drive adaptive learning:**
- A pseudonymous learner identifier (no name needed in the learning event store)
- Timestamps and concept node GUIDs per interaction event
- Correct/incorrect (boolean) per attempt
- Response time (seconds) — valuable signal for confidence vs. guessing
- Help/hint requested (boolean)

**What you do not need:**
- Name, photo, school (these belong in a separate identity store with restricted access)
- Device fingerprint, IP address (no purpose for curriculum adaptation)
- Engagement metrics beyond session events (no tracking of eye movement, emotional state inference beyond explicit signals)

The principle: the knowledge tracing model should be fully functional using only anonymised interaction events. Identity is a separate concern, needed only for displaying progress to parents or teachers and for account management.

### Minimum Viable Learner Model Schema

A pragmatic schema for the event log (xAPI-compatible):

```
LearnerEvent {
  learner_id:     UUID (pseudonymous, not name)
  timestamp:      ISO 8601
  event_type:     ENUM [question_attempted, hint_requested, session_start, session_end]
  concept_id:     Neo4j node GUID
  item_id:        Question bank reference
  correct:        Boolean (nullable for session events)
  response_ms:    Integer (response time in milliseconds)
  attempt_number: Integer (within this item)
}
```

From this minimal schema, all knowledge tracing models (BKT, PFA, DKT variants) can be computed. Learning path recommendations, parent notifications, and encouragement triggers can all be derived. Nothing sensitive need be stored in the event log itself.

---

## Summary: Alignment with Product Decisions

| Product Decision | Evidence Support | Mechanism |
|---|---|---|
| No visible progress bars | Strong (SDT, gamification literature) | Removes controlling feedback; preserves autonomy |
| No leaderboards/badges | Strong (gamification negative effects) | Prevents extrinsic displacement of intrinsic motivation |
| AI encouragement ("You're on a roll!") | Strong (SDT informational feedback; growth mindset language) | Supports competence need without control |
| Effort-framing encouragement | Moderate-strong (Dweck, cross-OECD study) | Effort attribution improves resilience to setbacks |
| Semi-random parent notifications | Moderate (parental involvement literature) | Enables quality home discussion; informational not controlling |
| Semi-random delight moments | Moderate (surprise/delight UX; dopamine-salience research) | Unexpected rewards avoid overjustification effect |
| Graph-based curriculum (Neo4j) | Strong (KST outer-fringe concept, GKT research) | Prerequisite awareness is the key gap in mainstream KT models |

---

## Priority Papers and Systems for Deeper Investigation

1. **Corbett & Anderson (1994)** — Original BKT: foundational, read for the model formulation
2. **Piech et al. (2015)** — Deep Knowledge Tracing: foundational for deep KT; [arXiv 1506.05908](https://arxiv.org/abs/1506.05908)
3. **Nakagawa et al. (2019)** — Graph-Based Knowledge Tracing (ICLR): most directly relevant to this platform's structure; [paper](https://rlgm.github.io/papers/70.pdf)
4. **Sinha & Kapur (2021)** — Productive Failure meta-analysis: *Review of Educational Research* — strong effect size, clear design principles
5. **Ryan & Deci (2000)** — SDT: the foundational paper on intrinsic motivation and educational environments
6. **Roediger & Karpicke (2006)** — Testing effect: *Perspectives on Psychological Science* — the most directly actionable cognitive learning science result for question-sequencing
7. **Bjork & Bjork (2011/2020)** — Desirable Difficulties: key framework for session design (interleaving, spacing)
8. **Twenty-five years of BKT (Springer, 2023)** — systematic review: [link](https://link.springer.com/article/10.1007/s11257-023-09389-4)
9. **AI-driven ITS in K-12 (PMC, 2025)** — most current systematic review: [link](https://pmc.ncbi.nlm.nih.gov/articles/PMC12078640/)
10. **1EdTech CASE Specification** — for curriculum standard interoperability: [link](https://www.1edtech.org/standards/case)
11. **IEEE xAPI 2.0** — for learner event standard: [ADL Initiative](https://www.adlnet.gov/experience-api/)
12. **ASSISTments Evidence of Impact** — strongest evidence base in free-to-use edtech: [link](https://www.assistments.org/evidence-of-impact)

---

## What Is Hype vs. What Has Evidence

**Well-evidenced (use with confidence):**
- Spaced retrieval practice improves long-term retention (replication rate: very high)
- Immediate feedback outperforms delayed feedback (ASSISTments RCT: effect size 0.37)
- Worked examples for novices, problem-solving for developing experts (robust literature)
- Productive failure before instruction for conceptual learning (meta-analytic, d = 0.36–0.58)
- Informational (not controlling) feedback supports intrinsic motivation (SDT: decades of evidence)
- Interleaving outperforms blocking on delayed tests (30–40% improvement)
- Parental involvement correlates with outcomes (though mechanism and causal direction unclear)

**Moderately evidenced (use with awareness of caveats):**
- Growth mindset language: the *language framing* effect is real; large-scale *intervention* effects are modest
- LLM-based tutoring: promising, early evidence; quality control is unsolved
- Graph-based knowledge tracing: technically superior to flat KT; limited production deployment evidence
- Flow state detection and maintenance: theoretically sound; technically hard to implement reliably

**Hype (use with caution or avoid):**
- Gamification (badges, leaderboards, progress bars): net neutral to negative for intrinsic motivation
- Learning styles (VAK, etc.): not well evidenced; do not design around them
- "AI will personalise everything" without a structured domain model: LLMs without curriculum graphs produce hallucinations and misaligned content
- Mindset interventions as silver bullets: weak causal evidence for large-scale deployment

---

## Related documents

| Document | Relationship |
|---|---|
| [README](../../README.md) | Summarises key findings and links back here for [each research claim](../../README.md#research-foundation) |
| [SOURCES.md](../research/SOURCES.md) | [Annotated bibliography](../research/SOURCES.md#summary-table) with access-level metadata for every source cited above |
| [PROJECT_DIRECTION.md](PROJECT_DIRECTION.md) | [Architecture direction](PROJECT_DIRECTION.md#architecture-direction) informed by this briefing's findings on [knowledge tracing](#1-learner-modelling-and-knowledge-tracing) and [widget-based interaction](#llm-tutors-and-natural-language-interaction) |
| [OUTPUT_SCHEMAS.md](OUTPUT_SCHEMAS.md) | [Pedagogy algorithm](OUTPUT_SCHEMAS.md#output-contract-1) in Schema B implements [productive failure](#productive-failure-kapur), [spacing](#spacing-and-interleaving-bjork), and [SDT feedback](#self-determination-theory-sdt) |
| [CHILD_PROFILE_CONSENT.md](CHILD_PROFILE_CONSENT.md) | [Profiling justification](CHILD_PROFILE_CONSENT.md#3-the-profiling-problem-our-hardest-compliance-question) draws on this briefing's ITS evidence |
| [Learner profiles layer](../../layers/learner-profiles/README.md) | Implements the [age-appropriate constraints](#6-learner-domain-architecture) and [feedback rules](#4-motivation-and-engagement-what-the-evidence-actually-says) from this briefing |
| [Research papers](../research/learning-science/) | 16 source papers organised by theme: [knowledge-tracing](../research/learning-science/knowledge-tracing/), [intelligent-tutoring](../research/learning-science/intelligent-tutoring/), [motivation-and-engagement](../research/learning-science/motivation-and-engagement/), [cognitive-learning](../research/learning-science/cognitive-learning/), [llm-in-education](../research/learning-science/llm-in-education/) |

---

*Sources referenced: [Twenty-five years of BKT, Springer 2023](https://link.springer.com/article/10.1007/s11257-023-09389-4) — [Deep Knowledge Tracing, Piech et al. 2015](https://arxiv.org/abs/1506.05908) — [Graph-Based Knowledge Tracing, ICLR 2019](https://rlgm.github.io/papers/70.pdf) — [DyGKT 2024](https://arxiv.org/html/2407.20824v1) — [xAPI IEEE Standard](https://www.adlnet.gov/experience-api/) — [1EdTech CASE](https://www.1edtech.org/standards/case) — [ASN](http://www.achievementstandards.org/) — [1EdTech Caliper](https://www.1edtech.org/standards/caliper) — [Carnegie Learning Research](https://www.carnegielearning.com/why-cl/research/) — [ALEKS Knowledge Space Theory](https://www.aleks.com/about_aleks/knowledge_space_theory) — [ASSISTments Evidence](https://www.assistments.org/evidence-of-impact) — [Khanmigo](https://www.khanmigo.ai/) — [Khan Academy Efficacy Nov 2024](https://blog.khanacademy.org/khan-academy-efficacy-results-november-2024/) — [AI-driven ITS K-12 systematic review, PMC 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12078640/) — [LLM in Education systematic review, ScienceDirect 2025](https://www.sciencedirect.com/science/article/pii/S2666920X25001699) — [Ryan & Deci SDT 2000](https://selfdeterminationtheory.org/SDT/documents/2000_RyanDeci_SDT.pdf) — [Intrinsic/Extrinsic motivation, ScienceDirect 2020](https://www.sciencedirect.com/science/article/abs/pii/S0361476X20300254) — [Gamification ghost effect, Frontiers 2024](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2024.1474733/full) — [Negative effects of gamification, IST 2022](https://www.sciencedirect.com/science/article/abs/pii/S0950584922002518) — [Gamification meta-analysis BJET 2024](https://bera-journals.onlinelibrary.wiley.com/doi/full/10.1111/bjet.13471) — [Productive Failure meta-analysis, Sinha & Kapur 2021](https://journals.sagepub.com/doi/10.3102/00346543211019105) — [Roediger & Karpicke 2006](http://psychnet.wustl.edu/memory/wp-content/uploads/2018/04/Roediger-Karpicke-2006_PPS.pdf) — [Bjork Desirable Difficulties 2011](https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/04/EBjork_RBjork_2011.pdf) — [Worked examples effect, ScienceDirect 2010](https://www.sciencedirect.com/science/article/abs/pii/S0361476X1000055X) — [Overjustification effect Wikipedia](https://en.wikipedia.org/wiki/Overjustification_effect) — [Overjustification USC paper](https://ceo.usc.edu/wp-content/uploads/2013/02/2013-05-G13-05-624-Negative_Effects_of_Extrinsic_Rewards.pdf) — [ALEKS meta-analysis, Investigations in Mathematics Learning 2021](https://www.tandfonline.com/doi/full/10.1080/19477503.2021.1926194) — [PFA 2009](https://pact.cs.cmu.edu/koedinger/pubs/AIED%202009%20final%20Pavlik%20Cen%20Keodinger%20corrected.pdf) — [EdTech GDPR COPPA architecture](https://6b.education/insight/building-privacy-compliant-systems-edtech-development-under-gdpr-coppa-and-ferpa/) — [Technology-mediated parental engagement systematic review](https://www.tandfonline.com/doi/full/10.1080/13803611.2021.1924791) — [Growth mindset controversies PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8299535/) — [Flow in ITS, SpringerLink 2014](https://link.springer.com/chapter/10.1007/978-3-642-39112-5_5) — [KG-based learning path recommendation, MDPI 2025](https://www.mdpi.com/2079-9292/15/1/238)*
