# V4 Staff Room Report — Group Synthesis

**Date:** 2026-02-22
**Team:** Henderson (Y2 Maths), Okonkwo (Y4 English), Kapoor (Y5 Science), Osei (KS3 Science), Adeyemi (KS3 Geography + History)
**Total scope:** 41 domains, ~260 concepts, 5 subjects, KS1-KS4

---

## The Headline

**The graph knows WHAT to teach. It does not yet know HOW to teach it.**

Every teacher arrived at this conclusion independently. The concept-level content — teaching guidance, misconceptions, vocabulary, prerequisites — is excellent and in several cases better than published schemes of work. But the subject-specific materials that turn curriculum knowledge into classroom practice are absent: texts for English, practicals for Science, case studies for Geography, source documents for History, worked examples for Maths.

**Consensus rating: 7/10 for curriculum structure, 4/10 for content generation readiness.**

---

## 1. What We All Agree Is Good

These five findings were confirmed independently by all five teachers:

### 1.1 Concept quality is the standout feature
Every teacher rated concept-level detail (teaching guidance, misconceptions, vocabulary) as the strongest part of the graph. Henderson: "the misconception for C002 is the single most common error I see." Osei: "the misconception capture reads like an experienced teacher's notes, not generic textbook summaries." Kapoor: "significantly better than a raw curriculum document." This data is accurate, specific, and directly usable.

### 1.2 Prerequisite chains are correct and useful
Cross-year and cross-key-stage prerequisite links were validated by every teacher. Henderson highlighted Y1→Y2 links for baseline assessment. Kapoor confirmed KS1→KS2 material properties progressions. Adeyemi confirmed KS2→KS3 geography transitions. Osei confirmed KS3 internal chains. These are hard to get right and they are right.

### 1.3 CO_TEACHES relationships capture real pedagogy
Within-domain and curated cross-domain CO_TEACHES links were praised by all. Henderson: "cross-domain links match how I'd actually plan." Osei: "the diffusion link across bio/chem/physics is genuine." Adeyemi: "the most useful structural improvement since v3." Okonkwo: "the reading-writing connections are exactly the connections I teach."

### 1.4 ConceptCluster sequencing is pedagogically sound
Cluster ordering was validated across all subjects. Henderson: "follows the pedagogical dependency chain correctly." Kapoor: "4 clusters map onto 4 lesson blocks." Osei: "matches how Chemistry is actually taught." The topological sort produces defensible teaching sequences.

### 1.5 Misconception data could power diagnostic assessment today
Every teacher identified misconceptions as ready-made assessment material. Osei demonstrated generating MC questions with misconception-based distractors. Henderson showed how face-value errors become diagnostic items. Adeyemi noted "these are the exact misconceptions I encounter in Year 8 and Year 9." This is the graph's most immediately deployable feature.

---

## 2. What We All Agree Is Missing

These gaps were identified independently by 3+ teachers:

### 2.1 CRITICAL: Subject-specific content vehicles (5/5 teachers)
Every subject needs its own "content vehicle" — the medium through which curriculum knowledge is delivered:

| Subject | Content Vehicle | Status in Graph |
|---------|----------------|-----------------|
| English | Texts (novels, poems, model texts, passages) | Completely absent |
| Science | Practical investigations (equipment, methods, variables) | Completely absent |
| Geography | Case studies (places, data, maps) | Empty topic slots only |
| History | Source documents (primary/secondary sources, timelines) | Completely absent |
| Maths | Worked examples (step-by-step model problems) | Completely absent |

**This is the single most important finding.** The graph models curriculum structure excellently but contains none of the subject-specific materials that make lessons possible. An English lesson without a text, a Science lesson without a practical, a Geography lesson without a case study — these are not lessons.

### 2.2 CRITICAL: Working Scientifically / disciplinary skills disconnected from content (4/5 teachers)
Both Science teachers (Kapoor, Osei) flagged that Working Scientifically skills exist as nodes but are not linked to the content concepts they develop. Adeyemi flagged the same for Historical Thinking (collapsed into one concept instead of five separate skills). Okonkwo flagged that Spoken Language skills are disconnected from reading/writing.

The pattern: **epistemic/disciplinary skills are bolted on as appendices, not woven into content.** The NGSS 3D model (practices integrated into every standard) was cited by both Science teachers and Adeyemi as the correct architectural approach.

### 2.3 CRITICAL: No cross-subject links (4/5 teachers)
Henderson, Okonkwo, Kapoor, and Adeyemi all flagged the absence of cross-subject connections. Adeyemi's Geography-History overlap (Empire↔Development, Migration as both historical and geographical) was the most detailed analysis. Kapoor flagged Science→Maths dependencies (measurement, data handling, graphs). Okonkwo flagged English→everything (literacy across the curriculum). Henderson noted that Maths data skills should connect to Science/Geography data skills.

**0 cross-subject relationships exist in the graph.** This is not a minor gap — it means the graph models each subject as if it exists in isolation, which is the opposite of how schools work.

### 2.4 HIGH: No difficulty sub-levels within concepts (4/5 teachers)
Henderson: "34+5 (no exchange) is much easier than 47+36 (exchange)." Osei: "the complexity 1-5 scale maps to nothing specific." Kapoor: no year-group attribution within KS2. Adeyemi: single concepts covering entire half-terms of teaching.

Each concept spans a wide difficulty range but the graph treats it as a single point. An AI cannot generate appropriately scaffolded content without knowing where "easy" ends and "hard" begins within a concept.

### 2.5 HIGH: No assessment scaffolding beyond misconceptions (4/5 teachers)
All teachers acknowledged that misconceptions are excellent raw material for diagnostic questions. But none found: question type specifications, mark scheme templates, difficulty calibration, success criteria, or diagnostic question structures. Henderson: "the graph can tell me what to assess but gives me nothing about how to construct a good question." Osei: "how to use misconceptions to write questions — the data is there, the method is not."

### 2.6 HIGH: CASE/NGSS alignment layer is empty (3/5 teachers)
Osei, Kapoor, and Okonkwo all noted that the CASE standards reference contains structural nodes but empty descriptions, 0 alignment relationships, and missing sections (crosscutting concepts, CC ELA, CC Math content). The "Inspired by" fields on clusters provide useful context but cannot be looked up. Henderson: "having references you can't look up is worse than having no references." Both Science teachers specifically recommended adopting NGSS Crosscutting Concepts (Patterns, Cause/Effect, Systems, etc.) as organising tags for UK content.

### 2.7 MEDIUM: Learner profile year bug (2/5 teachers, affects all)
Henderson discovered that the Y2 Maths context contains the Y1 learner profile (number range 1-20 instead of 0-100, session length 5-12 min instead of 8-15 min). The query uses `years[0]` — the first year of the key stage. This affects every subject: KS1 gets Y1 profile (should be Y1 or Y2), KS2 gets Y3 profile (should be Y3-Y6), KS3 gets Y7 (correct for Y7, wrong for Y8-Y9).

---

## 3. Subject-Specific Findings

### Maths (Henderson) — 7/10 structure
- **Unique strength:** CPA progression described in teaching guidance (Dienes blocks → place value charts → abstract notation)
- **Unique gap:** Missing interaction types (array builder, part-whole model, coin manipulative, clock face) — 4 of 8 domains can't generate appropriate interactive activities
- **Unique recommendation:** Structure CPA as queryable data, not prose. Add `concrete: [...]`, `pictorial: [...]`, `abstract: [...]` per concept

### English (Okonkwo) — 7/10 accuracy, 4/10 content gen
- **Unique strength:** Reading↔Writing CO_TEACHES links are the best cross-domain feature in the entire graph
- **Unique gap:** No texts = no English. This is not fixable with metadata — it requires a content/resource layer or Oak National Academy integration
- **Unique gap:** Missing KS2 Reading content domain codes (2a-2h) — grammar codes are mapped but reading codes are not
- **Unique recommendation:** Add genre/text-type taxonomy. Narrative sub-genres, non-fiction text types, poetry forms. Flag Handwriting (D005) as `ai_non_deliverable`

### Primary Science (Kapoor) — 7.5/10 content, 4/10 investigation
- **Unique strength:** NGSS cluster inspiration tags provide useful international benchmarking
- **Unique gap:** No year-group attribution. "KS2, Age 7-11" covers 4 different year groups. Y3 retrieval content gets the same weight as Y6 new learning
- **Unique gap:** Y5 Forces domain exists in graph but was not pulled into context (context generation bug)
- **Unique recommendation:** Add `nc_year` property. Add investigation metadata: `enquiry_type`, `suggested_variables`, `equipment`, `recording_format`

### KS3 Science (Osei) — 7/10 content, 4/10 practical, 6/10 assessment
- **Unique strength:** Chemistry narrative across 5 domains is coherent and correctly sequenced
- **Unique strength:** Cross-domain CO_TEACHES (diffusion across bio/chem/physics, enzymes↔catalysts, breathing↔pressure) capture genuine scientific interconnections
- **Unique gap:** No practical work layer at all (equipment, methods, risk assessments, CLEAPSS references)
- **Unique gap:** D006/D015 overlap (Particle Model in both Chemistry and Physics) creates a false domain boundary
- **Unique recommendation:** Add Practical node type. Add "Big Idea" narrative arcs (Life, Matter, Energy/Forces). Add safety/hazard data

### Humanities (Adeyemi) — Geography 6/10, History 3/10
- **Unique strength:** Geography prerequisite chains from KS2 enable genuine transition planning
- **Unique gap:** History has 4 concepts for 1000 years. The Medieval period, Reformation, Industrial Revolution, World Wars, and social history are all missing. This is orders of magnitude too coarse
- **Unique gap:** No cross-subject links between Geography and History despite being taught by the same teachers in the same departments
- **Unique gap:** ~40% of statutory Geography content missing (rivers, coasts, glaciation, weather, economic sectors, energy)
- **Unique recommendation:** Break History into ~15 concepts (not 4). Break Geography into ~20 (not 6). Add cross-subject CO_TEACHES. Add fieldwork and source material layers

---

## 4. The Content Generation Matrix

Can the graph generate each content type today?

| Content Type | Maths | English | Science | Geography | History |
|-------------|-------|---------|---------|-----------|---------|
| **Diagnostic quiz** | Partial | Grammar: Yes, Reading: No | Yes (misconception-based) | Yes (misconception-based) | Partial |
| **End-of-topic test** | No (no difficulty levels) | Spelling: Yes, Grammar: Yes, Reading: No | Partial (no mark schemes) | Partial (no case studies) | No (no sources) |
| **Interactive lesson** | Partial (missing interaction types) | No (no texts) | Partial (no practicals) | No (no case studies/maps) | No (no sources/timeline) |
| **Lesson slides** | No (no worked examples) | No (no texts/models) | Partial (no diagrams/practicals) | No (no maps/data) | No (no sources) |
| **Scheme of work** | 70% (missing lesson counts) | Skills: Yes, Content: No | 70% (missing WS mapping) | 60% (missing case studies) | 30% (too coarse) |
| **Investigation/enquiry** | N/A | N/A | No (critical gap) | Partial (no fieldwork layer) | No |
| **Differentiated material** | No (no difficulty tiers) | No (no text difficulty data) | No (no year attribution) | No (too coarse) | No (too coarse) |

**Summary:** The graph can generate **diagnostic quizzes** from misconception data (the clearest win). It can generate **scheme of work structures** at 60-70%. It cannot yet generate **complete lessons, slides, tests, or differentiated material** for any subject.

---

## 5. Priority Recommendations (Consensus)

Ranked by number of teachers flagging + impact on content generation:

### Tier 1: Critical (blocks content generation for all subjects)

| # | Recommendation | Flagged by | Effort | Impact |
|---|---------------|------------|--------|--------|
| 1 | **Add subject-specific content vehicles** (texts, practicals, case studies, sources, worked examples) | All 5 | High — different per subject | Transforms content gen from 4/10 to 7/10 |
| 2 | **Integrate disciplinary skills into content** (WS→Concepts, Historical Thinking→Concepts) | Kapoor, Osei, Adeyemi, Okonkwo | Medium — relationships, not new nodes | Enables skill-aware lesson generation |
| 3 | **Add cross-subject relationships** | Henderson, Okonkwo, Kapoor, Adeyemi | Medium — curated CO_TEACHES | Enables integrated department planning |
| 4 | **Fix learner profile year mapping** | Henderson (affects all) | Low — code fix in graph_query_helper | Prevents age-inappropriate content |

### Tier 2: High (significantly improves content generation quality)

| # | Recommendation | Flagged by | Effort | Impact |
|---|---------------|------------|--------|--------|
| 5 | **Add difficulty sub-levels within concepts** | Henderson, Osei, Kapoor, Adeyemi | Medium — properties per concept | Enables differentiated content |
| 6 | **Add assessment scaffolding** (question templates, mark schemes, success criteria) | Henderson, Osei, Kapoor, Okonkwo | Medium — new properties | Enables test generation beyond diagnostic |
| 7 | **Add `nc_year` to KS2 concepts** | Kapoor | Low — data exists in descriptions | Enables year-appropriate content |
| 8 | **Break History concepts into sub-concepts** | Adeyemi | Medium — re-extraction | Makes History usable at all |
| 9 | **Add missing interaction types** (array builder, part-whole model, clock face, coin manipulative) | Henderson | Medium — new InteractionType nodes | Enables maths interactive activities |

### Tier 3: Medium (improves quality and cross-system analysis)

| # | Recommendation | Flagged by | Effort | Impact |
|---|---------------|------------|--------|--------|
| 10 | **Add NGSS Crosscutting Concepts as tags** | Osei, Kapoor | Low — tagging existing concepts | Enables cross-domain thematic connections |
| 11 | **Map KS2 Reading content domain codes** | Okonkwo | Low — mapping to existing nodes | Enables reading assessment generation |
| 12 | **Add CPA progression as structured data** | Henderson | Medium — new properties per concept | Enables concrete-first lesson generation |
| 13 | **Add genre/text-type taxonomy for English** | Okonkwo | Medium — new classification layer | Enables writing task generation |
| 14 | **Add missing statutory Geography content** | Adeyemi | High — new extractions needed | Completes ~40% missing coverage |
| 15 | **Populate CASE alignment layer** | Osei, Kapoor, Okonkwo | Medium — alignment relationships | Enables cross-system comparison |

---

## 6. The 70/30 Problem

Three teachers independently used the same metaphor: "70% of what you need."

- Henderson: "This graph is about 70% of what you'd need for genuinely good AI-generated content."
- Kapoor: "The graph is 70% of what primary science needs."
- Adeyemi: "The domain and cluster structure gets you 70% there [for a scheme of work]."

The 70% is the **hard part** — getting the curriculum structure, concept dependencies, and pedagogical detail right. This is intellectual work that requires deep subject expertise and curriculum analysis. The graph does this well.

The missing 30% is more **mechanical** — worked examples, question templates, resource lists, case study databases, practical methods, source document collections. This is not easy, but it's known work. It's the kind of data that teachers create every day. The question is how to get it into the graph.

**The architecture supports it.** The ConceptCluster layer, the CO_TEACHES relationships, the learner profile system, the interaction types — these are all well-designed infrastructure waiting for richer content to flow through them. Nothing needs to be rebuilt. Things need to be added.

---

## 7. The Big Picture

### What the graph is today
A **curriculum intelligence layer** — it knows the structure, dependencies, misconceptions, and pedagogical connections of the UK National Curriculum better than any single resource we've seen. It's a brilliant planning tool for experienced teachers and a solid foundation for AI-assisted content.

### What it needs to become
A **content generation engine** — capable of driving AI production of lessons, assessments, and teaching resources that a teacher would recognise as classroom-ready. This requires the subject-specific content vehicles (Tier 1, Recommendation 1) and the skill-content integration (Tier 1, Recommendation 2).

### The diagnostic quiz opportunity
The one content type that works TODAY is **misconception-powered diagnostic assessment**. Every subject has rich misconception data. Every teacher confirmed this data is accurate. Converting misconceptions into diagnostic questions is a well-defined transformation. If the platform wants a quick win for teachers, this is it.

### The text/resource layer question
The biggest architectural decision ahead: how to add subject-specific content (texts, practicals, case studies, sources, worked examples). Options:
- **Oak National Academy integration** — they have lesson resources. But availability, licensing, and coverage are unknowns
- **Curated resource layer** — new node types per subject (Text, Practical, CaseStudy, Source, WorkedExample) linked to concepts
- **AI generation with quality control** — use the graph to generate content, then human-validate it
- **Hybrid** — curate high-quality exemplars, generate at scale, validate

This decision shapes the next phase of development.

---

## 8. Cross-Team Discussion Findings

The teachers were asked to communicate with each other. These findings emerged from their peer-to-peer exchanges — insights none would have reached individually.

### 8.1 The Content Generation Readiness Spectrum (Okonkwo's framework, Henderson's synthesis)

Content falls into three tiers of AI-generation readiness:

| Tier | Type | Examples | Graph Readiness | Gap |
|------|------|----------|----------------|-----|
| **1: Rule-based** | Procedural, algorithmic | Times tables, spelling rules, grammar rules, number bonds | High (~80%) | Add worked examples, exercise templates |
| **2: Context-dependent** | Skills applied in context | Word problems, data interpretation, vocabulary in context | Medium (~50%) | Add cross-subject links, difficulty grading |
| **3: Text/resource-dependent** | Requires rich content vehicle | Reading comprehension, essay writing, source analysis, case study geography, open investigations | Low (~25%) | Needs a companion resource layer |

**Implication for development:** Start with Tier 1. Generate rule-based content first (spelling tests, times tables drills, grammar quizzes). Build the contextual and resource layers in parallel for Tier 2 and 3.

### 8.2 Eighteen Specific Cross-Subject Links Identified

The teachers didn't just flag the gap — they drafted the links:

**Science → Maths (Kapoor + Henderson: 9 links):**
- Measurement + place value → science observation recording
- Tables + tally charts → science results recording
- Bar charts → categorical science data
- Line graphs → continuous science data (distance-time, heating curves)
- Averages (mean) → repeated measurements in fair tests
- Scale reading → force meters, thermometers
- Ratio/proportion → concentration, magnification
- Formula substitution → speed, density, pressure
- Unit conversion → g/kg, mm/cm/m, mL/L

**Science → English (Okonkwo + Kapoor: 6 links):**
- Non-fiction reading (EN-Y4-C030) → reading for science information
- Technical vocabulary roots (EN-Y4-C003) → scientific terminology
- Explanation text structure → scientific report writing
- Evidence-based argument → scientific conclusions
- Formal register → scientific writing conventions
- Reading comprehension strategies → interpreting scientific texts

**Geography ↔ History (Adeyemi: 4 links):**
- Empire (HI-KS3-C002) ↔ Development (GE-KS3-C002)
- Empire (HI-KS3-C002) ↔ Migration (GE-KS3-C004)
- Climate Change (GE-KS3-C003) ↔ Power/Democracy (HI-KS3-C001)
- Historical Arguments (HI-KS3-C004) ↔ Geographical Skills (GE-KS3-C007)

### 8.3 The Literacy Transfer Cliff Edge (Okonkwo)

A structural gap between key stages:
1. KS2 English explicitly teaches non-fiction reading/writing using cross-curricular content
2. KS3 History/Geography/Science ASSUME those skills transferred and embed them as disciplinary skills
3. The graph models both sides but has no concept of the transfer between them

An AI using this graph would generate a Y4 English lesson teaching "retrieving information from non-fiction" with a generic text (no cross-subject link tells it to use a geography text), then generate a KS3 History lesson requiring "evidence-based essay writing" without checking prerequisite writing skills from English. The child practises retrieval in English and is expected to do retrieval in History without anyone bridging the gap.

**Key distinction (Okonkwo):** English teaches reading comprehension (inference, retrieval, summarising). History requires source evaluation (reliability, bias, corroboration, contextualisation). These are related but DISTINCT cognitive operations. The graph treats them as separate universes.

### 8.4 WS-as-Bridge Architecture (Kapoor)

Rather than creating cross-subject links from every science concept to every maths skill, route through Working Scientifically as bridge nodes:

```
Maths Concept → SUPPORTS_SKILL → WS Skill → DEVELOPS_IN → Science Concept
```

Example: `MA-Y5-C014 (Line graphs) → SUPPORTS_SKILL → WS-KS2-005 (Recording data) → DEVELOPS_IN → SC-KS2-C027 (Friction investigation)`

This is architecturally cleaner — it avoids N×M cross-subject links and leverages the WS nodes that already exist but are disconnected.

### 8.5 MISCONCEPTION_PERSISTS_TO (Kapoor → Osei)

Kapoor identified 7 KS2 misconceptions that persist into KS3 and proposed a new relationship type:

- "Light goes from eye to object" (KS2 C067 → KS3 C115)
- "All metals are magnetic" (KS2 C026 → KS3 materials)
- "Dissolving and melting are the same" (KS2 C048 → KS3 particle model)
- "Plants get food from soil" (KS2 C042 → KS3 C042)
- "A force is needed to keep an object moving" (KS2 → KS3 C121)
- "Mass is lost when things burn" (KS2 → KS3 C075)
- "Electric current is used up in a circuit" (KS2 → KS3 C137)

These persistent misconceptions need to be carried forward so a Y7 diagnostic can probe for KS2 gaps.

### 8.6 Graph as Structure Layer + Companion Resource Layer (Adeyemi via Henderson)

The architectural recommendation from cross-team discussion: the graph should remain the curriculum structure and relationship layer, but needs a **companion resource layer** (or external resource index) that it references. The graph says "this concept needs a contrasting earthquake case study." The resource layer provides the case study pack. The graph points to resources; resources are stored elsewhere.

This preserves the graph's strengths (relationships, dependencies, sequencing) without asking it to do what it structurally cannot (store rich unstructured content like historical sources, case study narratives, or model texts).

### 8.7 Learner Profile Per-Subject Override (Adeyemi + Henderson)

The learner profile doesn't differentiate between subjects at the same key stage. The "100-200 word" response length is fine for Geography paragraphs and Science explanations but inadequate for History essays (500-800 words by Year 9). Either a per-subject override in the learner profile or a `writing_demand` property on concepts would fix this.

Related: the sentence length max (14 words for KS2) applies to AI-generated text the child reads, but scientific writing the child produces needs 15-20 word multi-clause sentences. The profile needs a "presentation register" vs "target writing register" distinction (Okonkwo).

---

## Appendix: Individual Report Locations

| Teacher | File |
|---------|------|
| Henderson (Y2 Maths) | `generated/teachers-v3/y2-maths/v4_findings.md` |
| Okonkwo (Y4 English) | `generated/teachers-v3/y4-english/v4_findings.md` |
| Kapoor (Y5 Science) | `generated/teachers-v3/y5-science/v4_findings.md` |
| Osei (KS3 Science) | `generated/teachers-v3/ks3-biology/v4_findings.md` |
| Adeyemi (KS3 Geography + History) | `generated/teachers-v3/ks3-geography/v4_findings.md` |

---

*"If the misconceptions are right, the rest can be fixed. And the misconceptions are right."* — Henderson

*"The text IS the lesson."* — Okonkwo

*"The investigation IS the lesson."* — Kapoor

*"The graph knows WHAT to teach but not HOW to teach it as science."* — Osei

*"Geography and History are not separate subjects in a child's education — they are different lenses on the same world."* — Adeyemi
