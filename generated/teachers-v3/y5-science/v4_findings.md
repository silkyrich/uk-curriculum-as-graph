# V4 Findings — Mr Raj Kapoor, Y5/6 Science

**Date:** 22 February 2026
**Teacher:** Mr Raj Kapoor, 10 years' experience, Science Lead
**School:** Primary, Leicester
**Domains evaluated:** Light (D005), Forces and Magnets (D006), Living Things and Their Habitats (D007), Properties and Changes of Materials (D011), Earth and Space (D012), Evolution and Inheritance (D014)
**Additional data reviewed:** CASE standards reference, Working Scientifically extraction, Learner Profile (Y3/KS2), Lesson plan (25 lessons), Teaching log (v3)

---

## Executive Summary

The graph contains **26 concepts across 6 domains**, with **16 curated ConceptClusters**, **rich teaching guidance and misconceptions data**, **prerequisite chains** within and across domains, and **CO_TEACHES relationships** that signal co-teachable concepts. The learner profile and interaction types provide useful scaffolding guidance for AI-generated content.

**Overall verdict: 7.5/10 for content generation, 4/10 for investigation generation, 5/10 for assessment generation, 6/10 for teaching resource generation.**

The graph is strongest on "what to teach" and weakest on "how to investigate." Science teaching at primary level is fundamentally practical — the investigation IS the lesson — and the graph's architecture doesn't yet support practical science adequately.

---

## 1. Half-Term Planning Exercise

I attempted to plan a half-term (6 weeks, 12 lessons) on Light and Forces using only the graph data.

### What the graph gave me

| Resource | Quality | Usable? |
|----------|---------|---------|
| Concept sequence (prerequisites) | Excellent | Yes — C022/C024 before C067, C025/C027 before C026 |
| Cluster groupings | Good | Yes — 4 clusters map onto 4 lesson blocks |
| Teaching guidance per concept | Excellent | Yes — specific activities, demonstrations, progressions |
| Common misconceptions | Excellent | Yes — research-backed, specific to age group |
| Key vocabulary | Good | Yes — 15-17 terms per concept, ready for working walls |
| Statutory objectives | Complete | Yes — all 15 objectives for these 2 domains |
| CO_TEACHES pairings | Moderate | Useful for confirming cluster pairings; less useful when everything links to everything (Light) |
| Learner profile (content guidelines) | Good | Yes — Lexile range, sentence length, vocabulary approach |
| Interaction types | Good | Yes — drag to categorise, matching pairs, MC suitable for science |

### What the graph didn't give me (and I had to plan independently)

| Missing element | Impact | Could an NQT plan without it? |
|----------------|--------|-------------------------------|
| Year group attribution (Y3/Y4/Y5/Y6) within KS2 | Critical — I compressed Y3 retrieval content to 2 lessons, gave Y6 content 4 lessons. Without NC knowledge, a teacher would give equal weight to all. | No |
| Y5 Forces domain (D013: gravity, air resistance, mechanisms) | Critical — domain exists in graph but missing from my context. Half my forces teaching can't be planned. | No |
| Working Scientifically integration | High — every lesson needs a WS focus (fair test, pattern seeking, classification, observation). Not linked to content. | Would struggle |
| Equipment lists | High — I need torches, mirrors, magnets, ramps, force meters, iron filings. The teaching guidance mentions them in prose but there's no structured list. | Would manage but slowly |
| Risk assessments | High — laser pointers, darkened rooms, sharp mirrors, chemicals (vinegar + bicarb for irreversible changes). Nothing in graph. | No — would need separate resource |
| Enquiry type mapping | Moderate — which concepts suit fair tests vs observation vs research? I know, but the graph should tag this. | Would struggle |
| Time allocations per cluster | Low — removed in v3.7, which is correct. My professional judgement is better than a formula. | N/A (correctly omitted) |

### Half-term plan I produced

| Week | Lessons | Focus | WS Focus (my addition) |
|------|---------|-------|------------------------|
| 1 | 1-2 | Light: vision, shadows (retrieval from Y3) | Fair testing (shadow size) |
| 2 | 3-4 | Light: straight-line model, ray diagrams (Y6 new) | Observation, modelling |
| 3 | 5-6 | Light: reflection, how we see, assessment | Pattern seeking, evidence |
| 4 | 7-8 | Forces: contact/non-contact, friction investigation | Fair testing (core WS lesson) |
| 5 | 9-10 | Forces: magnetic materials, poles and fields | Systematic observation, pattern seeking |
| 6 | 11-12 | Forces: assessment + bridge to Y5 Forces (D013) | Communicating findings |

This worked. The graph gave me the concept sequence and the pedagogical detail to flesh out each lesson. But I needed my own knowledge for the WS mapping, the practical resource planning, and the year group differentiation.

---

## 2. Can the Graph Generate Science Content?

### 2a. Interactive science lessons — Yes, with gaps

An AI could generate a lesson on "Light Travels in Straight Lines" from the graph data:
- The teaching guidance describes the torch-and-cards demonstration step by step
- The misconceptions identify the "emission theory" error (children think light goes from eye to object)
- The vocabulary list provides the key terms to introduce
- The prerequisite chain tells the AI that C022, C023, C024 must come first
- The learner profile says to start with a challenge problem (productive failure), then worked example, then retrieval practice with interleaving

**What's missing for a good interactive lesson:**
- **No simulation/model specifications.** "Draw a ray diagram" — what does the ray diagram look like? What are the components? The graph doesn't include visual specifications for the models it asks children to use.
- **No scaffolded task sequence.** The teaching guidance gives the overview but not the step-by-step differentiated tasks. The learner profile says "3 hint tiers" but the hints are generic maths examples ("What do you already know about this?"), not science-specific.
- **No WS skill progression within the lesson.** A good investigation lesson moves from question → prediction → method → results → conclusion. This structure isn't encoded anywhere.

### 2b. Science investigations — No, not adequately

This is the critical gap. KS2 science is built around five enquiry types: fair testing, observation over time, pattern seeking, identifying/classifying, and research using secondary sources. The graph does not model these.

**What an AI would need to generate a fair test investigation:**
1. The scientific question (e.g., "How does the surface affect how far a car travels?")
2. The independent variable (surface type)
3. The dependent variable (distance travelled)
4. The control variables (car, ramp angle, release point)
5. Equipment list (ramp, toy car, ruler, 5 surfaces)
6. Method steps (set up, predict, test, record, repeat, average, conclude)
7. Recording format (table with surface | distance trial 1 | trial 2 | trial 3 | mean)
8. Graph type (bar chart because independent variable is categorical)
9. Expected pattern (rougher surfaces → shorter distance)
10. Risk assessment (nothing hazardous for this one)

The graph gives me #1 (from the concept description), #9 (from the teaching guidance), and fragments of #5 (mentioned in prose). It gives me none of #2-4, #6-8, or #10 as structured data. An experienced teacher fills these in automatically. An AI or an NQT cannot.

**Recommendation:** Add an `investigations` property or linked node to concepts that are primarily taught through practical work. At minimum: enquiry type, variables (if fair test), equipment, recording format, expected outcome. This would transform the graph's usefulness for science.

### 2c. Teacher demonstrations — Partially

The teaching guidance for C067 (Light Travels in Straight Lines) essentially describes a teacher demonstration: "Shine a torch through a series of cards with holes — the light only reaches the end if all holes are aligned." This is good. But it lacks:
- Step-by-step setup instructions
- Equipment specifications (how many cards? what size holes? what torch?)
- Safety notes for laser pointers
- What to say at each step (talk script / key questions)
- Common problems and solutions ("What if the room isn't dark enough?")

For a demonstration, the teaching guidance gets you 60% of the way. A teacher with experience fills in the rest. An NQT would benefit from more structured guidance.

---

## 3. Can the Graph Generate Test Content?

### 3a. Misconception-targeting quizzes — Yes, this is a strength

The misconceptions data is the single most powerful feature for assessment generation. Every concept has 3-4 specific, research-backed misconceptions. An AI could generate:

- **True/False with correction:** "The Moon produces its own light." (False — it reflects sunlight.) Derived directly from SC-KS2-C022 misconceptions.
- **Multiple choice with misconception distractors:** "Why can we see the Moon at night?" A) It produces light B) It reflects light from the Sun C) Our eyes adjust to darkness D) Street lights illuminate it. Options A, C, D are all documented misconceptions from the graph.
- **Explanation questions:** "Explain why a shadow has the same shape as the object that casts it." Model answer derivable from C067 teaching guidance.

The interaction types (MC-3, MC-4, drag to categorise, matching pairs) map well onto these assessment formats.

### 3b. Investigation planning tasks — No

"Plan a fair test to find out which surface produces the most friction" — the graph cannot generate the mark scheme for this because it doesn't encode variables, method, or recording format (see Section 2b).

### 3c. Assessment aligned to national frameworks — No

The assessment layer contains KS2 Maths and English GPS test frameworks only. No science assessment framework exists in the graph. The KS2 science sampling tests (STA) use specific question types and mark schemes that could inform AI-generated assessments, but this data isn't present. The graph's science objectives are statutory NC objectives, not assessment framework content domain codes.

---

## 4. Can the Graph Generate Teaching Resources?

### 4a. Lesson slides — Partially

An AI could generate slide content (title, key vocabulary, key question, main teaching points, misconception to address) from the graph data. It could not generate:
- Diagrams or visual models (ray diagrams, classification hierarchies, life cycle diagrams)
- Practical activity instructions with sufficient detail
- Differentiated tasks for mixed-ability classes
- Plenary activities

### 4b. Equipment lists — No (not as structured data)

Equipment is mentioned in teaching guidance prose ("torches, mirrors, darkened rooms," "magnets, iron filings, paper clips") but not as a structured property. An AI parsing natural language could extract some of this, but it would miss items and couldn't generate a complete list with quantities.

### 4c. Risk assessments — No

No safety data at all. The teaching guidance mentions "teacher-operated laser pointer, safely" and "adult-supervised burning" but there are no CLEAPSS references, no hazard classifications, no control measures. This is a compliance issue for schools — every practical lesson needs a risk assessment.

---

## 5. Structural Analysis

### 5a. What the graph gets right

**Prerequisite chains are accurate and useful.** The progression from KS1 Material Properties → KS2 Friction, from KS1 Animal Life Cycles → KS2 Comparative Life Cycles, from KS2 Fossil Formation → Evolution — all correct. Cross-domain prerequisites (e.g., Magnetic Properties → Extended Material Properties) are genuinely helpful for sequencing. The two-pass import that resolves cross-KS links is architecturally sound.

**ConceptClusters (v3.7) are well-curated.** The 16 clusters across my 6 domains group concepts sensibly. Highlights:
- D005-CL002 (Reflection + Straight Line model) — the strongest cluster. Correct pairing, correct sequencing, genuinely co-teachable.
- D007-CL002 (Formal Classification + Micro-organisms) — strong. These are inseparable in practice.
- D014-CL003 (Adaptation + Evolution) — the "Darwin narrative" cluster. Exactly right.
- D011-CL003 (Reversible + Irreversible Changes) — the conceptual culmination of materials. Correct.

**Teaching guidance and misconceptions are the standout feature.** Specific, practical, age-appropriate, evidence-informed. These alone justify the graph's existence as a planning tool. The misconception that "all metals are magnetic" (C026), that "dissolving and melting are the same" (C048), that "light travels from the eye to the object" (C067) — these are exactly the errors I see in my classroom. Having them documented per concept with suggested teaching responses is invaluable.

**NGSS cluster inspiration tags are interesting.** Each cluster cites an NGSS core idea (e.g., "Inspired by: NGSS PS4.B - Electromagnetic Radiation"). This is a useful lens even without formal alignment links — it signals where the US curriculum might offer complementary framings or activities.

### 5b. What the graph gets wrong or misses

**1. Year group attribution — the most critical missing property.**

Every concept is "KS2, Age 7-11." For my 6 domains:
- Light: C022, C023, C024 are Y3. C067 is Y6. Teaching weight should vary dramatically by year group.
- Forces & Magnets: All Y3. The entire domain is retrieval for Y5/6.
- Living Things: C028, C029, C030 are Y4. C044, C045 are Y5. C058, C059 are Y6. Three different year groups in one domain.
- Materials: All Y5.
- Earth & Space: All Y5.
- Evolution: All Y6.

The concept descriptions contain this information in prose. It is not available as a structured property. This is the difference between "the AI sends Y5 children six lessons on Y3 content at full teaching weight" and "the AI compresses Y3 retrieval into a starter activity and focuses new learning time on Y5/Y6 content."

**Recommendation:** Add `nc_year: [3]` or `nc_year: [5, 6]` as a property on every concept. The data already exists in the descriptions — it just needs structuring.

**2. Y5 Forces domain (SC-KS2-D013) exists but was omitted from my context.**

The graph contains the domain with 3 concepts (Gravity, Resistance Forces, Mechanisms as Force Multipliers) and 3 statutory objectives. It simply wasn't pulled into my context file. This is a context generation issue, not a graph modelling issue. When a teacher is assigned "Y5 Science," the context generator should pull both D006 (Forces and Magnets, Y3 foundation) and D013 (Forces, Y5 new content).

**3. Working Scientifically is structurally disconnected from content.**

The epistemic skills layer has 8 WS skills for KS2 with progression links to KS3. These are excellent — "Planning enquiries and controlling variables" (WS-KS2-003), "Classifying and identifying patterns" (WS-KS2-004), "Using evidence to support or refute ideas" (WS-KS2-008). But the graph model uses `DEVELOPS_SKILL` from Programme nodes, not from Concept or Cluster nodes. This means:
- There's no way to query "which concepts are best taught through fair testing?"
- There's no way to ensure WS coverage across a unit
- An AI generating a lesson doesn't know which WS skills to weave in

In primary science, WS skills are not taught separately — they are taught through content. The friction investigation IS the fair testing lesson. The classification key IS the classifying lesson. The Darwin evidence discussion IS the evaluating evidence lesson. The graph's separation of WS from content mirrors the NC's structure (WS is listed separately) but not primary teaching reality (WS is embedded in every lesson).

**Recommendation:** Add `ws_enquiry_types: ["fair_test", "observation"]` to concepts, or create `DEVELOPS_SKILL` relationships from ConceptCluster to WorkingScientifically nodes.

**4. NGSS crosscutting concepts are absent.**

The CASE standards reference lists NGSS practices and core ideas but the crosscutting concepts section is empty. This is a significant missed opportunity. The seven NGSS crosscutting concepts — Patterns, Cause and Effect, Scale/Proportion/Quantity, Systems and System Models, Energy and Matter, Structure and Function, Stability and Change — map powerfully onto UK science:

| NGSS Crosscutting Concept | UK KS2 Science Application |
|---------------------------|----------------------------|
| Patterns | Shadow size patterns, life cycle patterns, classification patterns |
| Cause and Effect | Forces cause motion changes, environmental change affects habitats |
| Systems and System Models | Solar system, food chains, human body systems |
| Structure and Function | Plant/animal adaptations, material properties for purpose |
| Stability and Change | Reversible/irreversible changes, evolution over time |

These are exactly the conceptual lenses that connect topics across domains. "Cause and Effect" links Forces (force causes acceleration) with Environmental Change (pollution causes habitat loss) with Evolution (environmental change causes selection pressure). If the graph encoded these crosscutting concepts and linked them to UK content, it would enable genuinely powerful cross-domain connections that currently don't exist.

**5. No cross-subject links exist.**

The CASE standards reference shows "Total alignment relationships in graph: 0." My science domains have no connections to Maths (measurement, data handling, graphs), English (scientific writing, vocabulary, reading for information), or Geography (habitats, environmental change, Earth and space). In primary teaching, these connections are fundamental. I've messaged Henderson (Maths) and Okonkwo (English) about this — I suspect it's the same from their side.

**6. No science assessment framework.**

The assessment layer covers KS2 Maths and English GPS only. No science test framework, no question type taxonomy, no mark scheme patterns. This means the graph can generate misconception-based quizzes (strong) but cannot generate assessment that reflects national testing patterns (weak).

### 5c. CO_TEACHES analysis

| CO_TEACHES relationship | Strength | Useful? |
|------------------------|----------|---------|
| C023 ↔ C067 (Reflection ↔ Straight Lines) | Strong | Yes — reflection explained by straight-line model |
| C058 ↔ C059 (Classification ↔ Micro-organisms) | Strong | Yes — micro-organisms are a classification group |
| C066 ↔ C065 (Evolution ↔ Adaptation) | Strong | Yes — adaptation leads to evolution |
| C051 ↔ C050 (Irreversible ↔ Reversible) | Strong | Yes — the key distinction in materials |
| C030 ↔ C059 (Environmental Change ↔ Micro-organisms) | Moderate | Yes — decomposers in environmental systems |
| C053 ↔ C052 (Earth's Rotation ↔ Solar System) | Strong | Yes — rotation explains day/night within solar system |
| C027 ↔ C025 (Friction ↔ Contact Forces) | Strong | Yes — friction is the exemplar contact force |
| C027 ↔ C026 (Friction ↔ Magnets) | Weak | No — domain proximity, not pedagogical affinity |

**Recommendation:** Add a strength property (strong/moderate/weak) to CO_TEACHES. Currently all relationships appear equal. The C027↔C026 link (friction and magnets) is not a real co-teaching signal — it just means they share a domain. The C058↔C059 link (classification and micro-organisms) is genuinely inseparable. These should be distinguishable.

---

## 6. The Practical Science Gap — Why It Matters

Primary science is not a reading subject. It is a doing subject. The NC says: "Pupils should be helped to develop their understanding of scientific ideas by using different types of scientific enquiry... including observing changes over different periods of time, noticing patterns, grouping and classifying things, carrying out comparative and fair tests and finding things out using a wide range of secondary sources of information."

The graph models the conceptual knowledge beautifully. It does not model the practical activity that delivers that knowledge. Here is what a science lesson actually looks like in my classroom:

**Lesson: Friction Investigation (C027)**
1. (5 min) Retrieval starter: "Name 3 contact forces and 2 non-contact forces" — graph can generate this
2. (5 min) Question: "How does the surface affect how far a toy car travels?" — graph mentions this
3. (5 min) Prediction: "I think the car will travel furthest on ___ because ___" — graph cannot generate
4. (5 min) Method planning: variables, equipment, steps — graph cannot generate
5. (15 min) Practical investigation: testing 5 surfaces, 3 repeats each — graph cannot generate
6. (10 min) Recording results in table, calculating means — graph cannot generate
7. (5 min) Drawing bar chart — graph cannot generate
8. (5 min) Conclusion: "The rougher the surface, the more friction, the shorter the distance" — graph can generate
9. (5 min) Evaluation: "Was it a fair test? What would you change?" — graph cannot generate

The graph can generate steps 1, 2, 8 — the conceptual bookends. It cannot generate steps 3-7, 9 — the actual science. An AI using only this graph would produce a quiz with explanation, not an investigation.

**This is the single most important gap for science content generation.** If the graph is to support "generate interactive science lessons" and "generate practical investigations," it needs an investigation layer or investigation properties on concepts. Without it, science lessons will be comprehension exercises dressed up as science.

---

## 7. NGSS Comparison — What the US Model Does Better

The NGSS 3D model (Practices + Core Ideas + Crosscutting Concepts) is architecturally superior to the UK graph model for science content generation, even though the UK curriculum content is richer.

| Dimension | NGSS | UK Graph | Gap |
|-----------|------|----------|-----|
| Content knowledge | Core Ideas | Concepts (with rich guidance) | UK is richer |
| Practices/skills | 8 SEPs linked to every PE | WS skills exist but disconnected | Critical gap |
| Cross-domain themes | 7 Crosscutting Concepts | Nothing | Major gap |
| Performance expectations | Specific assessable statements | Statutory objectives | Comparable |

The NGSS model is designed for exactly the question this platform is asking: "Given a topic, what should a child know (core idea), be able to do (practice), and see as a pattern (crosscutting concept)?" The UK graph answers the first question excellently, the second question partially (WS exists but isn't linked), and the third question not at all.

**Recommendation:** Even without formal NGSS alignment, adding a "crosscutting concept" tag to UK concepts would be transformative. C067 (Light Travels in Straight Lines) is a "Cause and Effect" concept. C030 (Environmental Change) is a "Stability and Change" concept. C058 (Formal Classification) is a "Patterns" concept. These tags would enable cross-domain quiz generation, thematic unit planning, and more coherent AI-generated explanations.

---

## 8. Colleague Discussions

Messages sent to:
- **Osei (KS3 Science):** KS2→KS3 transition analysis. Flagged Y5 Forces gap, WS disconnection, absence of crosscutting concepts, no science assessment framework. Asked whether KS3 data explicitly models KS2 concepts as prerequisites.
- **Henderson (Y2 Maths):** Cross-subject maths-science dependencies. Science investigations require measurement, data handling, averages, graph drawing — none linked in graph. Without maths prerequisites, AI can't scaffold science investigations appropriately by age.
- **Okonkwo (Y4 English):** Science literacy connections. Science requires reading for information, technical vocabulary, explanation writing, evidence-based argument — all English skills, none linked to science concepts. The content guideline sentence length max (14 words) conflicts with scientific writing needs.

---

## 9. Recommendations (Priority Order)

### Must-have (blocks content generation quality)

1. **Add `nc_year` property to all KS2 concepts.** Values: 3, 4, 5, or 6. Data already exists in concept descriptions. Without this, AI cannot differentiate retrieval from new learning.

2. **Fix context generation to include Y5 Forces (D013).** The domain exists. It wasn't pulled. This is a bug, not a feature request.

3. **Add investigation/enquiry metadata to science concepts.** Minimum: `enquiry_type` (fair_test | observation | pattern_seeking | classifying | secondary_research), `suggested_variables` (for fair tests), `equipment` (structured list), `recording_format` (table | bar_chart | line_graph | diagram). This is the difference between generating a quiz and generating a science lesson.

### Should-have (significantly improves quality)

4. **Link WS skills to content concepts or clusters.** Either add `ws_skills: ["WS-KS2-003"]` to concepts, or create `DEVELOPS_SKILL` relationships from ConceptCluster to WorkingScientifically nodes.

5. **Add CO_TEACHES strength indicator.** "strong" / "moderate" / "weak" — so AI can distinguish genuinely co-teachable pairs from domain-proximity noise.

6. **Add crosscutting concept tags.** Even without NGSS alignment, tagging UK concepts with "patterns," "cause_and_effect," "systems," "structure_and_function," "stability_and_change" would enable powerful cross-domain connections.

7. **Add a science assessment framework to the assessment layer.** KS2 science sampling test content domains would enable assessment-aligned quiz generation.

### Nice-to-have (improves teacher resource generation)

8. **Add equipment lists as structured data per concept.** Currently buried in prose.

9. **Add risk assessment references.** CLEAPSS codes or hazard categories per practical activity.

10. **Add cross-subject links.** Science → Maths (measurement, data handling), Science → English (scientific writing, vocabulary), Science → Geography (habitats, Earth and space).

---

## 10. Final Verdict

**The graph is a strong conceptual framework that does not yet understand practical science.**

It excels at modelling what children should know. The concept definitions, prerequisite chains, misconception data, and curated clusters are excellent — significantly better than a raw curriculum document. A teacher with 2+ years' experience can use this to plan efficiently. An AI can use it to generate quizzes, vocabulary activities, and explanation-based content.

It fails at modelling what children should do. The graph cannot generate a science investigation, a practical demonstration with full instructions, or an equipment list. It cannot tell an AI which Working Scientifically skills to weave into a lesson. It cannot connect science to the maths skills that every investigation depends on. For a subject where "working scientifically" IS the subject — this is the gap that matters most.

The good news: the architecture supports adding this. The ConceptCluster layer already groups concepts into teachable units. Adding investigation metadata to clusters (or to concepts) would close the biggest gap without restructuring the graph. The WS skills already exist as nodes — they just need connecting to content. The crosscutting concepts just need tagging.

The graph is 70% of what primary science needs. The missing 30% is the practical, procedural, cross-curricular layer that turns conceptual knowledge into science lessons. I would use this graph today for planning support. I would not yet trust an AI to generate a complete science lesson from it without significant teacher oversight.

---

*V4 findings complete. Mr Raj Kapoor, February 2026.*
