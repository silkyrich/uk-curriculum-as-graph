# Research Sources — Learner Layer Design
**Last updated:** 2026-02-18
**Purpose:** Annotated bibliography documenting the research foundation for the platform's learner layer design decisions.

This is an honest audit trail. Each entry records what was actually fetched (full text, page summary, or briefing summary only) so that the confidence level of any derived design decision can be assessed. Nothing is presented as fully verified when only a summary was available.

---

## Summary table

| # | Short name | Year | Type | Access | Relevance | Key contribution to platform |
|---|---|---|---|---|---|---|
| 1 | DKT (Piech) | 2015 | academic paper | briefing summary only | High | Foundational deep KT; establishes the upgrade path from BKT once data volume is sufficient |
| 2 | DyGKT | 2024 | academic paper | briefing summary only | Medium | Dynamic graph extension of GKT; long-term architecture target |
| 3 | GKT (Nakagawa) | 2019 | academic paper | briefing summary only | High | Most directly relevant KT architecture; uses prerequisite graph as structural input |
| 4 | BKT 25yr review | 2023 | systematic review | briefing summary only | High | Confirms individualised hierarchical BKT as the defensible starting model |
| 5 | AI ITS K-12 review | 2025 | systematic review | full text fetched | High | ITS effect sizes; confirms pedagogy > AI sophistication; flags ethics gap |
| 6 | Gamification ghost effect | 2024 | academic paper | full text fetched | High | Evidence base for removing gamification; ghost effect concept |
| 7 | ASSISTments evidence | ongoing | vendor/RCT summary | page summary fetched | High | Strongest free-platform evidence; immediate feedback ES = 0.37 |
| 8 | ALEKS KST | ongoing | vendor | page summary fetched | High | Outer fringe concept; prerequisite-gated sequencing in commercial practice |
| 9 | Carnegie Learning | ongoing | vendor/RCT summary | page summary fetched | Medium | Blended model evidence; Year 2 effect; low-attainment equity gains |
| 10 | CASE standard | ongoing | standard | page summary fetched | Medium | Curriculum interoperability layer for school integrations |
| 11 | xAPI standard | 2023 | standard | page summary fetched | High | Canonical learner event format; LRS architecture |
| 12 | Ryan & Deci SDT | 2000 | academic paper | page summary fetched | High | Theoretical foundation for all anti-gamification and encouragement design |
| 13 | Bjork desirable difficulties | 2011 | academic paper | page summary fetched | High | Spacing and interleaving algorithm design; session sequencing |
| 14 | Lepper overjustification | 1973 | academic paper | briefing summary only | High | Justifies unexpected vs expected reward design; no-badges decision |
| 15 | Roediger & Karpicke | 2006 | academic paper | briefing summary only | High | Every question is a learning event; post-error correction standard |
| 16 | Productive failure meta | 2021 | meta-analysis | briefing summary only | High | Problem-before-instruction sequencing; d = 0.36–0.58 |
| 17 | KG learning path | 2025 | academic paper | briefing summary only | High | Direct application of knowledge graphs to learning path recommendation |
| 18 | LLM education review | 2025 | systematic review | briefing summary only | High | LLM over structured domain model architecture; 35% hint failure rate |
| 19 | ICO Children's Code | 2020 | regulatory standard | no cache — briefing only | High | UK GDPR / data minimisation requirements for children's platforms |
| 20 | ICO EdTech Guidance | 2023 | regulatory guidance | web search summaries | Critical | Determines in-scope status; controller vs processor distinction |
| 21 | UK GDPR Art. 8 / DPA 2018 s.9 | 2018 | legislation | multiple secondary sources | Critical | Age 13 consent threshold; parental consent verification |
| 22 | ICO Profiling Standards (5 & 12) | 2021 | regulatory guidance | web search summaries | Critical | Profiling-off-by-default; compelling reason test for adaptive learning |
| 23 | ICO DPIA Requirements (Standard 2) | 2021 | regulatory guidance | web search summaries | High | DPIA mandatory; Annex D template; children-specific risk assessment |
| 24 | ICO Best Interests: Profiling for ADM | 2023 | regulatory guidance | web search summaries | High | Automated decision-making framework; Recital 71 |
| 25 | ICO Best Interests: Content Personalisation | 2023 | regulatory guidance | web search summaries | High | Content delivery profiling rules; compelling reason examples |
| 26 | Data (Use and Access) Act | 2025 | legislation | web search references | Medium | All ICO guidance under review from June 2025 |
| 27 | Online Safety Act 2023 | 2023 | legislation | web search references | Medium | Protection of Children Codes from July 2025 |
| 28 | Proposed education-specific code | 2025+ | proposed legislation | web search references | Medium | Would directly address AI profiling in education |

---

## 1. Learner Modelling and Knowledge Tracing

### DKT — Piech et al. (2015)
**Citation:** Piech, C., Bassen, J., Huang, J., Ganguli, S., Sahami, M., Guibas, L., & Sohl-Dickstein, J. Deep Knowledge Tracing. *Advances in Neural Information Processing Systems (NeurIPS)*, 28. 2015.
**URL:** https://arxiv.org/abs/1506.05908
**Type:** academic paper
**Access:** briefing summary only (arxiv fetch failed)
**Relevance:** High

**What it is:** The paper that applied LSTM recurrent neural networks to knowledge tracing for the first time, significantly outperforming BKT on the ASSISTments benchmark and triggering a decade of deep-learning KT research.

**Key insights:**
- LSTM over interaction sequences substantially outperforms BKT on large datasets
- Implicit inter-skill relationships are captured from sequence data without hand-specification
- Triggered the entire deep KT literature including GKT, DyGKT, DKVMN, AKT

**What we derived from it:** DKT establishes the upgrade path from hierarchical BKT to graph-aware deep KT once the platform has accumulated sufficient interaction data (likely several thousand student-sessions). Until that threshold, simpler models are more defensible.

**Caveats:** DKT models are data-hungry and opaque — not interpretable to teachers or parents. The ASSISTments benchmark advantage does not guarantee real-world superiority over simpler models in small-data settings. No full text fetch — derived from briefing.

**Cached at:** `docs/research/learning-science/dkt_piech_2015.md`

---

### DyGKT (2024)
**Citation:** Author(s) not confirmed. DyGKT: Dynamic Graph-Based Knowledge Tracing. *arXiv preprint* arXiv:2407.20824. 2024.
**URL:** https://arxiv.org/html/2407.20824v1
**Type:** academic paper
**Access:** briefing summary only (fetch failed)
**Relevance:** Medium

**What it is:** An extension of Graph-Based Knowledge Tracing (GKT) that replaces static prerequisite graphs with dynamic graphs that evolve as a student learns, representing the current frontier in graph-aware KT.

**Key insights:**
- Graph topology can be updated during learning rather than fixed at session start
- Captures temporal shifts in concept relationships as knowledge state changes
- Part of a 2024 wave of 37 deep KT papers

**What we derived from it:** The Neo4j graph need not be treated as a permanently fixed input — as the platform accumulates data, empirically observed co-mastery patterns can inform edge weights, making the graph itself learnable over time.

**Caveats:** Fetch failed; details from briefing only. Authors not confirmed. Production deployment evidence unknown. Data requirements likely high.

**Cached at:** `docs/research/learning-science/dygkt_2024.md`

---

### GKT — Nakagawa et al. (2019)
**Citation:** Nakagawa, H., Iwasawa, Y., & Matsuo, Y. Graph-Based Knowledge Tracing: Modeling Student Proficiency Using Graph Neural Network. *IEEE/WIC/ACM WI 2019*; IRLG Workshop at ICLR 2019.
**URL:** https://rlgm.github.io/papers/70.pdf
**Type:** academic paper
**Access:** briefing summary only
**Relevance:** High

**What it is:** The paper introducing Graph-Based Knowledge Tracing, which uses GNNs to model concept dependency relationships explicitly as directed edges, taking a prerequisite graph as structural input rather than learning inter-skill structure from sequences alone.

**Key insights:**
- Prerequisite graph is structural input, not implicitly learned
- Outperforms vanilla BKT and early DKT when concept graph is informative
- Addresses the fundamental independence assumption failure in flat KT models
- Foundational for DyGKT and subsequent graph-aware KT research

**What we derived from it:** The existing Neo4j curriculum graph can serve directly as the GKT domain model. This is the natural medium-term KT architecture for the platform once data volume is sufficient — it reads the graph directly rather than ignoring prerequisite structure.

**Caveats:** Briefing summary only. IRLG workshop paper, not a main-track venue — verify claims against follow-up work. GKT performance advantage over DKT depends on quality of hand-authored prerequisite graph.

**Cached at:** `docs/research/learning-science/gkt_nakagawa_2019.md`

---

### BKT 25-Year Review (2023)
**Citation:** Author(s) not confirmed. Twenty-five years of Bayesian Knowledge Tracing: A systematic review. *User Modeling and User-Adapted Interaction*. 2023. https://doi.org/10.1007/s11257-023-09389-4
**URL:** https://link.springer.com/article/10.1007/s11257-023-09389-4
**Type:** systematic review
**Access:** briefing summary only (Springer redirect / paywall)
**Relevance:** High

**What it is:** A systematic review of 25 years of BKT research across 13 enhancement dimensions, identifying which modifications consistently improve performance and documenting the model's known limitations.

**Key insights:**
- Individualised / hierarchical BKT (per-student learning rate parameters) consistently outperforms vanilla BKT
- EM algorithm is the de facto standard for parameter estimation
- Vanilla BKT's independence assumption is directly problematic for graph-based curricula
- Four-parameter vanilla BKT has identifiability problems on small datasets

**What we derived from it:** The platform should start with hierarchical BKT (hBKT), not vanilla BKT, and not deep KT until data volume is sufficient. The Neo4j graph addresses the independence limitation directly.

**Caveats:** Authors not confirmed from paywalled fetch. Briefing summary only. Review scope (which 25 years of BKT papers were included, which were excluded) is not verifiable from the summary.

**Cached at:** `docs/research/learning-science/bkt_25years_review_2023.md`

---

## 2. Educational Knowledge Graph Standards

### CASE Standard
**Citation:** 1EdTech Consortium. CASE (Competencies and Academic Standards Exchange) Specification. v1.0 and v1.1.
**URL:** https://www.1edtech.org/standards/case
**Type:** standard
**Access:** page summary fetched
**Relevance:** Medium

**What it is:** A 1EdTech specification for machine-readable hierarchical academic standards expressed as JSON-LD with UUID-identified items, designed to replace PDF curriculum documents with API-accessible standards trees.

**Key insights:**
- GUIDs per item enable cross-platform standards alignment
- Hierarchical (tree), not a graph — no native prerequisite or co-requisite relationships
- Part of 1EdTech ecosystem with LTI, OneRoster, Open Badges
- UK National Curriculum could be exposed as a CASE document for third-party alignment

**What we derived from it:** Publishing a CASE-compatible view of the curriculum graph (flattening prerequisites into parent-child relationships) is a useful compatibility layer for school integrations, not the core data model. The Neo4j graph is more expressive than CASE allows.

**Caveats:** Page summary only; CASE v1.1 specification details not fully reviewed. Active adoption rate in UK school MIS ecosystem is not documented in the fetch.

**Cached at:** `docs/research/interoperability/case_standard.md`

---

### xAPI Standard (IEEE 9274.1.1-2023)
**Citation:** ADL Initiative / 1EdTech Consortium. Experience API (xAPI), IEEE 9274.1.1-2023. 2023 (standardised; originally xAPI 1.0, 2013).
**URL:** https://adlnet.gov/projects/xapi/
**Type:** standard
**Access:** page summary fetched
**Relevance:** High

**What it is:** The IEEE-standardised triple-structure learner event format (Actor → Verb → Object) with a Learning Record Store (LRS) architecture for storing and federating learning data across systems.

**Key insights:**
- Data transport standard, not a knowledge model
- Context extensions can carry domain-specific identifiers (Neo4j node GUIDs)
- Multiple LRSs can federate — enables cross-institution data aggregation
- Most widely adopted K-12 learner event standard, more pragmatic than Caliper for this context

**What we derived from it:** The platform's learner event log should be xAPI-formatted from the start. Neo4j concept node GUIDs in the context extension field create future interoperability while keeping the core data structure clean. The event-sourced learner model and xAPI format are architecturally compatible.

**Caveats:** Page summary only. The gap between the xAPI 1.0 ecosystem (2013–2023) and IEEE v2.0 (2023) means some existing LRS implementations may not be fully v2.0 compliant. Semantic interoperability (Profiles) requires additional specification work.

**Cached at:** `docs/research/interoperability/xapi_standard.md`

---

### KG Learning Path Recommendation (2025)
**Citation:** Author(s) not confirmed. Knowledge graph-based learning path recommendation. *MDPI Electronics*, 15(1), 238. 2025. https://doi.org/10.3390/electronics15010238
**URL:** https://www.mdpi.com/2079-9292/15/1/238
**Type:** academic paper
**Access:** briefing summary only (403 error on fetch)
**Relevance:** High

**What it is:** A 2025 MDPI Electronics paper directly addressing learning path recommendation using knowledge graphs, at the intersection of graph database technology and adaptive sequencing.

**Key insights:**
- Knowledge graphs can drive principled learning path recommendation respecting prerequisite dependencies
- Directly applicable to Neo4j-backed curriculum structures

**What we derived from it:** This paper confirms that the technical approach of using a Neo4j prerequisite graph for sequencing is an active research area with current literature support, not just an engineering choice. The outer fringe Cypher query pattern is the practical implementation.

**Caveats:** Fetch failed (403); authors not confirmed. MDPI is an open-access publisher with mixed peer-review reputation; quality should be independently verified before citing in external documents.

**Cached at:** `docs/research/learning-science/kg_learning_path_2025.md`

---

## 3. Intelligent Tutoring Systems

### AI ITS K-12 Systematic Review (2025)
**Citation:** Létourneau, A., Deslandes Martineau, M., Charland, P., Karran, J. A., Boasen, J., & Léger, P. M. A systematic review of AI-driven intelligent tutoring systems (ITS) in K-12 education. *Frontiers in Education*. 2025. PMC12078640.
**URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC12078640/
**Type:** systematic review
**Access:** full text fetched
**Relevance:** High

**What it is:** A systematic review of 28 studies (4,597 K-12 students) examining AI-driven ITS effectiveness, comparing ITS against conventional instruction and against non-intelligent digital systems, and identifying core effective features.

**Key insights:**
- 7 of 8 ITS vs. conventional instruction comparisons showed medium-to-large positive effects (d = 0.31 to d = 1.30)
- Only 1 of 4 ITS vs. non-intelligent system comparisons showed a clear AI advantage
- Core effective features: personalisation, immediate feedback, adaptivity, self-regulation support
- ITS most effective as complement to teacher instruction, not replacement
- No reviewed study addressed ethical implications — a gap the platform should fill proactively

**What we derived from it:** Pedagogical design (personalisation, immediate feedback, prerequisite-gating) drives outcomes more than AI sophistication. The ethics gap identified is a direct mandate to address privacy, data minimisation, and the ICO Children's Code from the outset.

**Caveats:** Full text fetched but authors' systematic review methodology details (search strategy, inclusion criteria) not independently audited here. The Yixue Squirrel AI 4.19x effect size is a striking outlier and likely context-dependent (Chinese educational context, intensive implementation).

**Cached at:** `docs/research/learning-science/ai_its_k12_systematic_review_2025.md`

---

### ASSISTments Evidence of Impact
**Citation:** ASSISTments Research Team, Worcester Polytechnic Institute. Evidence of Impact. (Ongoing; citing IES-rated RCT studies.)
**URL:** https://www.assistments.org/evidence-of-impact
**Type:** vendor / evidence summary (citing independent IES-rated RCTs)
**Access:** page summary fetched
**Relevance:** High

**What it is:** Summary of randomised controlled trial evidence for the ASSISTments free formative assessment platform, achieving IES "Positive effects without reservation" and ESSA Tier 1 status — among the strongest evidence standards in edtech.

**Key insights:**
- Maine RCT (2,769 students): 60% more learning, ES = 0.22; achievement gap narrowed
- North Carolina RCT (5,991 students): 30% more learning one year later, ES = 0.10 delayed; stronger for disadvantaged students
- Immediate feedback: 12% more learning, ES = 0.37
- Lower-achieving students: approximately 2x learning acceleration

**What we derived from it:** Immediate post-attempt feedback (not deferred to session end) should be a hard requirement, not an optimisation. The scaffolded hint model (increasingly specific hints rather than full answer delivery) is a validated design reference for the platform's hint system.

**Caveats:** Page summary only; vendor page. The immediate feedback ES = 0.37 is for the specific ASSISTments context (US 7th grade maths homework); direct transfer to UK curriculum contexts requires caution.

**Cached at:** `docs/research/learning-science/assistments_evidence.md`

---

### ALEKS and Knowledge Space Theory
**Citation:** ALEKS Corporation / McGraw-Hill. Knowledge Space Theory in ALEKS. (Corporate white paper / product description.)
**URL:** https://www.aleks.com/about_aleks/knowledge_space_theory
**Type:** vendor
**Access:** page summary fetched
**Relevance:** High

**What it is:** ALEKS's description of its implementation of Knowledge Space Theory (Doignon & Falmagne, 1985), the closest mainstream commercial approach to the platform's prerequisite graph architecture.

**Key insights:**
- Knowledge state lattice models all feasible knowledge states
- Algebra: ~350 fundamental concepts; state determined in ~25–30 questions via Markovian assessment
- Outer fringe concept: only serve items whose prerequisites are all mastered
- 2021 meta-analysis: ALEKS roughly equivalent to traditional instruction alone (g = 0.05) but significantly more effective as supplement (g = 0.43)

**What we derived from it:** The outer fringe concept is directly implementable as a Cypher query against the Neo4j graph. The ALEKS placement assessment approach (efficient Markovian state determination) informs the platform's initial placement assessment design.

**Caveats:** Vendor page; full KST technical detail is in academic literature (Doignon & Falmagne 1985), not the page itself. The 2021 meta-analysis finding of equivalence to traditional instruction when used standalone is a caution against over-reliance on adaptive sequencing alone without teacher integration.

**Cached at:** `docs/research/learning-science/aleks_knowledge_space_theory.md`

---

### Carnegie Learning Research
**Citation:** Carnegie Learning, Inc. Research Evidence Overview. (Corporate research summary, citing multiple independent studies.)
**URL:** https://www.carnegielearning.com/why-cl/research/
**Type:** vendor (citing independent RCT and quasi-experimental studies)
**Access:** page summary fetched
**Relevance:** Medium

**What it is:** Carnegie Learning's evidence base for MATHia, the commercial descendent of the CMU Cognitive Tutor research programme using ACT-R, model tracing, and BKT.

**Key insights:**
- RAND study: blended MATHia + teacher nearly doubled growth in Year 2
- EMERALDS: more MATHia workspaces completed in middle school → better Algebra I outcomes; effect largest for low-prior-attainment students
- Blended = ESSA Tier 1; standalone = ESSA Tier 2
- Year 2 effect suggests implementation quality and teacher familiarity are significant moderators

**What we derived from it:** Prerequisite-gated sequencing produces disproportionate gains for students with knowledge gaps — directly validating the platform's outer fringe approach. The Year 2 / implementation quality finding argues for a phased rollout with teacher-facing features.

**Caveats:** Vendor page; the RAND study details are not independently reviewed from this fetch. MATHia is US (Common Core) curriculum-aligned and its model-tracing approach requires hand-authored production rules — expensive and brittle compared with graph-based sequencing.

**Cached at:** `docs/research/learning-science/carnegie_learning_research.md`

---

## 4. Motivation and Engagement

### Ryan & Deci — Self-Determination Theory (2000)
**Citation:** Ryan, R. M., & Deci, E. L. Self-Determination Theory and the facilitation of intrinsic motivation, social development, and well-being. *American Psychologist*, 55(1), 68–78. 2000.
**URL:** https://selfdeterminationtheory.org/SDT/documents/2000_RyanDeci_SDT.pdf (PDF binary; see also https://selfdeterminationtheory.org/theory/)
**Type:** academic paper (foundational theoretical review)
**Access:** page summary fetched (PDF binary issue; summary from SDT website and briefing)
**Relevance:** High

**What it is:** The canonical synthesis of Self-Determination Theory, the most robustly evidenced motivational framework in education, establishing three universal basic psychological needs (Autonomy, Competence, Relatedness) and the conditions under which social environments support or undermine intrinsic motivation.

**Key insights:**
- Controlling feedback (explicit performance demands, visible progress requirements) suppresses intrinsic motivation
- Informational feedback (acknowledging competence) supports intrinsic motivation and can strengthen it
- Extrinsic controls including visible tracking and comparative ranking specifically undermine autonomy
- Cross-cultural replication over decades; universality of three-need structure is robust

**What we derived from it:** The theoretical foundation for removing visible progress bars (controlling feedback), removing leaderboards (social comparison undermines autonomy), and designing AI encouragement as informational rather than controlling. SDT is the strongest single theoretical justification for the platform's motivation architecture.

**Caveats:** Page summary only; full text is a PDF binary that was not parsed. The paper is from 2000 — very well established but should be supplemented with more recent SDT meta-analyses for any academic-facing documentation.

**Cached at:** `docs/research/learning-science/ryan_deci_sdt_2000.md`

---

### Gamification Ghost Effect (2024)
**Citation:** Jose, B., Cherian, J., Jaya, P. J., Kuriakose, L., & Rosy Leema, P. W. The Ghost Effect: How Gamification Can Hinder Genuine Learning. *Frontiers in Education*, 9. 2024. https://doi.org/10.3389/feduc.2024.1474733
**URL:** https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2024.1474733/full
**Type:** academic paper
**Access:** full text fetched
**Relevance:** High

**What it is:** A 2024 Frontiers in Education paper introducing the "ghost effect" concept — students physically present in gamified environments but mentally absent — and documenting the conditions under which gamification produces negative outcomes, with analysis of personality moderation.

**Key insights:**
- Ghost students: physically present, mentally absent — perfunctory compliance with gamified mechanics without cognitive engagement
- Badges and points: surface-level engagement, undermine intrinsic motivation
- Leaderboards: demoralise lower-performing students, reduce self-efficacy, produce learned helplessness
- Personality moderation: extraverts benefit; introverts experience increased anxiety and pressure
- Over-reliance on immediate rewards weakens capacity for self-directed inquiry and tolerating productive difficulty

**What we derived from it:** The most specific recent justification for the platform's removal of all gamification elements. The ghost effect concept is directly applicable to a platform serving children across attainment ranges; competitive mechanics would harm the students the platform most needs to serve.

**Caveats:** Full text fetched. Frontiers in Education is an open-access journal with broad scope — peer review rigour varies. The "ghost effect" is a new conceptual framing; empirical measurement methodology should be reviewed in the full text. The personality moderation finding (extraversion vs. introversion) requires the original instruments to be verified.

**Cached at:** `docs/research/learning-science/gamification_ghost_effect_2024.md`

---

### Lepper, Greene & Nisbett — Overjustification Effect (1973)
**Citation:** Lepper, M. R., Greene, D., & Nisbett, R. E. Undermining children's intrinsic interest with extrinsic reward: A test of the "overjustification" hypothesis. *Journal of Personality and Social Psychology*, 28(1), 129–137. 1973.
**URL:** https://ceo.usc.edu/wp-content/uploads/2013/02/2013-05-G13-05-624-Negative_Effects_of_Extrinsic_Rewards.pdf (PDF binary)
**Type:** academic paper (original experimental study)
**Access:** briefing summary only (PDF binary)
**Relevance:** High

**What it is:** The foundational experimental demonstration of the overjustification effect, showing that expected tangible rewards for intrinsically interesting activities reliably undermine subsequent intrinsic motivation after reward withdrawal.

**Key insights:**
- Expected tangible rewards undermine intrinsic motivation; unexpected post-completion rewards do not
- Effect requires anticipation: the mechanism is attributional (reward anticipation causes external attribution of behaviour)
- Informational competence feedback does not produce the effect and can increase intrinsic motivation
- Meta-analytically confirmed by Deci et al. (1999)

**What we derived from it:** No badges, no points, no achievement streaks visible to the student. Delight moments must be unexpected. AI encouragement must be informational (competence acknowledgment) not reward delivery. These design choices are precisely the conditions that avoid the overjustification effect.

**Caveats:** Briefing summary only; PDF binary not parsed. 1973 study using drawing as the intrinsic activity — direct transfer to digital learning interactions should be treated as plausible but not proven. Some debate in the meta-analytic literature (Cameron & Pierce 1994) about boundary conditions; the Deci et al. 1999 meta-analysis is the more reliable synthesis.

**Cached at:** `docs/research/learning-science/lepper_overjustification_1973.md`

---

## 5. Cognitive Learning Science

### Bjork — Desirable Difficulties (2011)
**Citation:** Bjork, E. L., & Bjork, R. A. Making things hard on yourself, but in a good way: Creating desirable difficulties to enhance learning. In *Psychology and the Real World* (pp. 56–64). Worth Publishers. 2011.
**URL:** https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/04/EBjork_RBjork_2011.pdf (PDF binary)
**Type:** academic paper (book chapter / review)
**Access:** page summary fetched (PDF binary; summary from Bjork lab site and briefing)
**Relevance:** High

**What it is:** The Bjork lab's accessible synthesis of desirable difficulties — conditions that impede immediate performance but enhance long-term retention — covering spacing, interleaving, and retrieval practice as the three most robustly supported techniques.

**Key insights:**
- Spacing: distributed practice 10–30% better retention than massed practice; one of psychology's most replicated findings
- Interleaving: 30–40% better delayed test performance than blocked practice
- Key paradox: conditions producing best immediate performance often yield worst long-term retention
- Learners systematically prefer blocked, massed practice due to misleading fluency cues

**What we derived from it:** The problem sequencing algorithm should implement spaced review (SM-2 or FSRS algorithm), interleaved within-session problem sets, and the AI encouragement layer should explicitly contextualise difficulty to prevent the fluency paradox from causing student disengagement.

**Caveats:** Page summary only; PDF binary not parsed. The 30–40% interleaving advantage figure and 10–30% spacing figure are from the briefing's reading of the chapter — precise experimental contexts should be verified against primary sources before external citation.

**Cached at:** `docs/research/learning-science/bjork_desirable_difficulties_2011.md`

---

### Roediger & Karpicke — Testing Effect (2006)
**Citation:** Roediger, H. L., & Karpicke, J. D. Test-enhanced learning: Taking memory tests improves long-term retention. *Psychological Science*, 17(3), 249–255. 2006.
**URL:** http://psychnet.wustl.edu/memory/wp-content/uploads/2018/04/Roediger-Karpicke-2006_PPS.pdf (PDF binary)
**Type:** academic paper (experimental study)
**Access:** briefing summary only (PDF binary)
**Relevance:** High

**What it is:** The canonical modern demonstration of the testing effect (retrieval practice effect): active retrieval from memory strengthens it more than re-studying, even when the retrieval attempt fails.

**Key insights:**
- Retrieval > re-study for long-term retention; effect strongest at delayed tests
- Even failed retrieval attempts strengthen memory (post-error correction should be standard)
- 2019 *Psychological Science in the Public Interest* review: most replicable finding in cognitive psychology
- Most platforms use retrieval as assessment; it should be the primary learning mechanism

**What we derived from it:** Immediate post-error correction (correct answer + explanation) after every incorrect response is a hard requirement. The knowledge tracing model should treat failed attempts as learning events, not just failure signals. Spaced review intervals should be designed around the retrieval practice mechanism.

**Caveats:** Briefing summary only; PDF binary not parsed. 2006 study context (prose passages, college students) — the retrieval practice effect is broadly replicated but specific effect sizes in K-12 curriculum contexts should not be assumed to match the original study.

**Cached at:** `docs/research/learning-science/roediger_karpicke_testing_2006.md`

---

### Productive Failure Meta-Analysis — Sinha & Kapur (2021)
**Citation:** Sinha, T., & Kapur, M. When problem solving precedes instruction: A meta-analytic review of productive failure. *Review of Educational Research*, 91(4), 505–539. 2021. https://doi.org/10.3102/00346543211019105
**URL:** https://journals.sagepub.com/doi/10.3102/00346543211019105
**Type:** meta-analysis
**Access:** briefing summary only (paywalled)
**Relevance:** High

**What it is:** The definitive meta-analytic synthesis of Productive Failure research (53 studies, 166 comparisons), quantifying the effect size advantage of problem-before-instruction sequencing over direct instruction first, especially at high design fidelity.

**Key insights:**
- Cohen's d = 0.36 overall (PF > direct instruction)
- At high design fidelity: Cohen's d = 0.58 (~3x a typical teacher year effect)
- Robust across mathematics and physics; sparse evidence outside STEM
- Most adaptive platforms invert this sequence — this is the most under-exploited evidence-based opportunity in edtech

**What we derived from it:** For conceptual knowledge components, the platform should present challenge problems before delivering instruction. The prerequisite graph determines when a student is ready to productively fail on a new concept (prerequisites mastered; target concept not yet mastered). This is a Cypher-queryable sequencing decision.

**Caveats:** Briefing summary only; paywalled. The d = 0.58 high-fidelity figure depends on careful implementation; degraded implementations may not achieve this. Evidence is sparse outside STEM — the platform's humanities and literacy components should not assume the same effect size.

**Cached at:** `docs/research/learning-science/productive_failure_meta_2021.md`

---

## 6. LLM and AI Tutoring

### LLM Education Systematic Review (2025)
**Citation:** Author(s) not confirmed. Large language models in education: A systematic review. *Computers and Education: Artificial Intelligence* (ScienceDirect). 2025. S2666920X25001699.
**URL:** https://www.sciencedirect.com/article/pii/S2666920X25001699
**Type:** systematic review
**Access:** briefing summary only
**Relevance:** High

**What it is:** A 2025 systematic review of LLM applications in education, with particular attention to the quality control problem in LLM-generated hints and the architectural implications of LLMs' lack of native persistent student models.

**Key insights:**
- 35% of LLM-generated hints in evaluation studies were too general, incorrect, or solution-revealing
- LLMs do not maintain persistent student models without explicit architectural mechanisms
- LLMs can confidently produce incorrect content in niche curriculum areas
- Most productive architecture: LLM constrained by structured domain model (curriculum graph + learner model)

**What we derived from it:** The platform architecture is validated: the Neo4j graph + BKT learner model provide the structured state that LLMs lack natively; the LLM generates natural language anchored to specific concept nodes and prerequisite states. The 35% hint failure rate establishes a concrete quality benchmark to beat.

**Caveats:** Briefing summary only; authors not confirmed. The 35% figure requires verification against the specific evaluation methodology — it may reflect particular systems or hint types and should not be assumed to apply uniformly to all LLM hint architectures.

**Cached at:** `docs/research/learning-science/llm_education_review_2025.md`

---

## 7. Architecture and Privacy

### ICO Age Appropriate Design Code (Children's Code, 2020)
**Citation:** Information Commissioner's Office (ICO). Age Appropriate Design Code. UK. 2020. Effective from 2 September 2021.
**URL:** https://ico.org.uk/for-organisations/guide-to-data-protection/ico-codes-of-practice/age-appropriate-design-a-code-of-practice-for-online-services/
**Type:** regulatory standard
**Access:** no cache — briefing only
**Relevance:** High

**Note on access:** No specific paper was cached for this entry. The following is derived from the platform briefing, which draws on the published ICO Code and related UK GDPR guidance. For full compliance review, the ICO Code should be read directly.

**What it is:** The UK Information Commissioner's statutory Code of Practice for online services likely to be accessed by children under 18. It translates UK GDPR principles into specific design requirements for children's digital services, creating a legal compliance baseline that also serves as a positive design framework.

**Key insights:**
- Data minimisation: collect only what is strictly necessary for the educational purpose; nothing more
- Best interests default: default privacy settings must be at the highest level, not requiring children to opt out of data collection
- No profiling for commercial purposes: learner data may not be used to build commercial profiles or serve targeted advertising
- No nudge techniques: design must not exploit psychological vulnerabilities — no dark patterns, no engagement-maximising mechanics that exploit children's psychology
- Pseudonymous learner identifiers: names and personal identifiers are not needed in the event log and should be architecturally separated from interaction data
- UK GDPR Article 22: individuals have rights regarding automated decisions affecting them — the event-sourced architecture (append-only log, auditable state derivation) directly supports this right

**What we derived from it:** The minimum viable learner model schema (pseudonymous UUID, timestamps, concept GUIDs, correct/incorrect, response time, hint requested) is sufficient to drive all KT algorithms without storing any personally identifiable information in the event log. Identity is a separate concern handled in a restricted access store. The ICO Code's "no nudge" requirement directly supports the design decision to avoid variable-schedule engagement mechanics and to restrict delight moments to genuine learning events.

**Caveats:** This entry has no cached file. The ICO Code is a live regulatory document that is updated; any compliance review must use the current version from ico.org.uk. The Code applies to services "likely to be accessed by under-18s" — if the platform serves both children and adults, the more protective children's regime should apply by default.

**Cached at:** Not cached — regulatory document; consult ico.org.uk directly for current version.

---

## 8. Privacy, Compliance, and Consent (Added 2026-02-20)

### ICO EdTech Guidance (2023)
**Citation:** Information Commissioner's Office (ICO). The Children's Code and Education Technologies (EdTech). 2023.
**URL:** https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/the-children-s-code-and-education-technologies-edtech/
**Type:** regulatory guidance
**Access:** web search summaries only (ICO site returned 403 on direct fetch)
**Relevance:** Critical

**What it is:** ICO guidance clarifying when the Children's Code applies to education technology providers. Establishes the controller/processor distinction and the three conditions that must ALL be met for edtech to be out of scope.

**What we derived from it:** Our platform is in scope because we are a direct-to-consumer service that determines the purposes and means of processing. Full compliance with all 15 standards is required.

**Cached at:** `docs/research/privacy-compliance/ico_edtech_guidance.md`

---

### UK GDPR Article 8 / DPA 2018 s.9 — Parental Consent
**Citation:** UK GDPR Article 8; Data Protection Act 2018 Section 9.
**URLs:** https://gdpr-info.eu/art-8-gdpr/ ; https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/children-and-the-uk-gdpr/what-are-the-rules-about-an-iss-and-consent/
**Type:** legislation + regulatory guidance
**Access:** multiple secondary sources (Fieldfisher, Sprintlaw, ICO web search summaries)
**Relevance:** Critical

**What it is:** The legal mechanism for parental consent for under-13s in the UK. Sets the age threshold at 13, requires "reasonable efforts" to verify parental responsibility, and defines when consent vs other lawful bases apply.

**What we derived from it:** Consent is our primary lawful basis. Email loop + micro-charge verification is proportionate for our risk level. The consent flow in CHILD_PROFILE_CONSENT.md implements these requirements.

**Cached at:** `docs/research/privacy-compliance/uk_gdpr_art8_parental_consent.md`

---

### ICO Profiling Standards (Standards 5 and 12)
**Citation:** ICO Age Appropriate Design Code, Standards 5 and 12. 2021.
**URLs:** https://ico.org.uk/.../12-profiling/ ; https://ico.org.uk/.../profiling-for-automated-decision-making/ ; https://ico.org.uk/.../profiling-for-content-delivery/
**Type:** regulatory guidance
**Access:** web search summaries only (403 on direct fetch)
**Relevance:** Critical

**What it is:** The two standards most challenging for adaptive learning: Standard 5 (no detrimental use of data) and Standard 12 (profiling off by default, compelling reason test). Together they define the boundary conditions for our core functionality.

**What we derived from it:** Our compelling reason argument for adaptive learning profiling (core to service, evidence-based pedagogy, no harmful content, full safeguards). Documented in CHILD_PROFILE_CONSENT.md Section 3.

**Cached at:** `docs/research/privacy-compliance/ico_profiling_standards.md`

---

### ICO DPIA Requirements (Standard 2)
**Citation:** ICO Age Appropriate Design Code, Standard 2: Data Protection Impact Assessments. 2021.
**URL:** https://ico.org.uk/.../2-data-protection-impact-assessments/
**Type:** regulatory guidance
**Access:** web search summaries only
**Relevance:** High

**What it is:** DPIA is mandatory for any online service likely to be accessed by children. Must be embedded in design, completed before launch, cover children-specific risks, and follow the Annex D template.

**What we derived from it:** A formal DPIA is required before beta launch. The Annex D template should be downloaded from ICO and populated with the risk analysis from CHILD_PROFILE_CONSENT.md Section 6. This is listed as a gap in our current documentation.

**Cached at:** `docs/research/privacy-compliance/ico_dpia_requirements.md`

---

### Upcoming Legislation: Data (Use and Access) Act, Online Safety Act, Education Code
**Citations:** Data (Use and Access) Act 2025; Online Safety Act 2023; Proposed education-specific code of practice.
**Type:** legislative tracking
**Access:** web search references and secondary analysis
**Relevance:** Medium

**What it is:** Three pieces of legislation that may affect our compliance architecture. The Data (Use and Access) Act (June 2025) puts all ICO guidance under review. The Online Safety Act (July 2025) adds complementary safety duties. A proposed education-specific code would directly address AI profiling in education.

**What we derived from it:** The regulatory direction is toward MORE scrutiny of automated systems serving children. Our transparency-first architecture positions us well, but we should monitor ICO guidance updates and engage with the education code consultation if possible.

**Cached at:** `docs/research/privacy-compliance/upcoming_legislation.md`

---

*End of annotated bibliography. Learning science papers are cached in `docs/research/learning-science/`; interoperability specs in `docs/research/interoperability/`; privacy and compliance sources in `docs/research/privacy-compliance/`. For each entry, the access level field indicates the confidence that should be placed in derived design decisions: full text fetched is the highest confidence; briefing summary only means the design decision is based on secondary characterisation and should be verified against primary sources before external academic citation.*
