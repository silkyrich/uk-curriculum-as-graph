# KS3 Science Evaluation — Dr Kwame Osei

**Role:** KS3 Science Teacher (Chemistry specialist), 12 years experience, Birmingham secondary school
**Scope:** All 15 KS3 Science domains (Biology: 4, Chemistry: 5, Physics: 6) + Working Scientifically + NGSS comparison
**Date:** 2026-02-22

---

## Executive Summary

The graph captures the **content** of KS3 Science with impressive depth — 146 concepts across 15 domains, each with teaching guidance, misconceptions, and vocabulary that reads like a well-researched teacher handbook. The Chemistry narrative is coherent and the cross-domain connections (diffusion across bio/chem/physics, catalysts bridging biology and chemistry, atmospheric pressure linking breathing to gas laws) demonstrate genuine understanding of how science is taught as interconnected disciplines.

However, the graph captures **what** to teach but not **how** to teach it as science. Working Scientifically is listed but not integrated. Practical work is described in text but not structured as data. The NGSS comparison reveals a fundamental gap: their 3D model (practices woven into every standard) versus our flat domain list with skills bolted on as an appendix. For content generation, the graph is strong. For practical lesson generation, risk assessments, and Working Scientifically progression, significant gaps remain.

**Overall verdict: 7/10 for content generation, 4/10 for practical lesson generation, 6/10 for assessment generation.**

---

## 1. Content Quality: What the Graph Gets Right

### 1.1 Concept-Level Detail Is Excellent

Every concept includes:
- **Teaching guidance** that reads like an experienced teacher's notes (not generic textbook summaries)
- **Common misconceptions** that are genuinely the ones I encounter daily in the classroom
- **Key vocabulary** that is comprehensive and specific

Examples of particularly strong misconception capture:
- C040 (Enzymes): "Students often say enzymes are 'killed' by heat — enzymes are proteins that are 'denatured'" — this exact correction is one I make weekly
- C075 (Conservation of mass): "Students often think mass is lost when substances burn" — the foundational misconception for all of KS3 chemistry
- C042 (Plant nutrition): "Students commonly believe plants get their food from the soil" — the single most persistent misconception in biology, present from KS1 to A-level
- C121 (Forces): "Students often think a force is needed to keep an object moving" — the Aristotelian misconception that Newton's first law exists to correct

### 1.2 The Chemistry Narrative Is Coherent

The five Chemistry domains follow the logical teaching progression I would use:

1. **D006 - Particulate Nature of Matter** → the foundational model
2. **D007 - Atoms, Elements, Compounds** → classifying what things are made of
3. **D008 - Chemical Reactions** → what happens when things change
4. **D009 - Periodic Table and Materials** → patterns and predictions
5. **D010 - Earth and Atmosphere** → applied chemistry in the real world

This mirrors how Chemistry is actually taught in schools and builds conceptual understanding layer by layer.

### 1.3 Cross-Domain Links Are the Standout Feature

The curated CO_TEACHES relationships between domains capture genuine pedagogical connections that a non-scientist might miss:

| Link | Why It Matters |
|------|---------------|
| Diffusion: Biology (C030) ↔ Chemistry (C078) ↔ Physics (C161) | Same phenomenon, three different framings — must be co-taught |
| Catalysts (C088) ↔ Enzymes (C040) | The bio-chem bridge: enzymes ARE biological catalysts |
| Breathing mechanism (C044) ↔ Atmospheric pressure (C130) | The bell jar model IS a physics pressure demonstration |
| Biomechanics (C034) ↔ Moments (C124) | The arm IS a lever system — biology meets physics |
| Food energy (C036/C037) ↔ Food energy values (C107) | Nutrition in biology, energy in physics — same food labels |
| Photosynthesis (C051) ↔ Carbon cycle (C104) ↔ Climate change (C106) | The biology-chemistry thread that links to the biggest issue of our time |

The "continuous_narrative" links between D007→D008 (atoms/elements/compounds leading into chemical reactions) are particularly important — and I note with satisfaction that the graph attributes these to me. They are correct: you cannot teach conservation of mass in isolation; it only makes sense when demonstrated through actual reactions.

### 1.4 ConceptClusters Are Well-Designed

The clusters follow a sensible pedagogical pattern:
- **Introduction** clusters establish core knowledge
- **Practice** clusters apply and extend
- **Assessment** gates (where present) check understanding at keystones

Chemistry D008 is particularly well-clustered:
1. Reactions as rearrangement + equations (foundation)
2. Types of reactions + catalysts (classification)
3. Acids, pH, acid-metal, neutralisation (the big practical sequence)
4. Energy changes in reactions and state changes (the energy dimension)

This matches how I would plan a half-term's teaching.

---

## 2. What the Graph Gets Wrong or Misses

### 2.1 CRITICAL: Working Scientifically Is Listed but Not Integrated

The 12 Working Scientifically skills (WS-KS3-001 to WS-KS3-012) are listed as a flat appendix. They are **not linked** to any specific concepts, domains, or clusters.

This is the single biggest structural gap. Working Scientifically is not a separate skill to be taught in isolation — it IS how science is taught. Every lesson should develop at least one WS skill. For example:

| WS Skill | Where It Should Be Linked |
|----------|--------------------------|
| WS-KS3-003 (Designing controlled experiments) | Enzyme activity (C040), diffusion rate (C030/C078), Hooke's Law (C127) |
| WS-KS3-005 (Tables and graphs) | Distance-time graphs (C119), force-extension (C127), heating curves (C071) |
| WS-KS3-006 (Interpreting data) | Climate data (C106), variation data (C064), food labels (C107) |
| WS-KS3-009 (Evaluating evidence) | DNA discovery (C063), Mendeleev predictions (C092) |
| WS-KS3-012 (Risk assessment) | Every practical — but no concept captures this |

**The NGSS does this correctly.** Their 8 Science and Engineering Practices are dimensionally integrated into every Performance Expectation. The UK curriculum says "Working Scientifically should be embedded in teaching across all domains" — the graph needs to make this explicit through relationships.

**Recommendation:** Create `DEVELOPS_SKILL` relationships from specific Concept nodes to WorkingScientifically nodes, similar to the existing `(:Programme)-[:DEVELOPS_SKILL]->(:WorkingScientifically)` but at concept granularity. The teaching guidance text already mentions the relevant practicals — this data could be extracted.

### 2.2 CRITICAL: No Practical Work Layer

The teaching guidance mentions practicals extensively — and they're the right practicals. But there is no structured data for:

- **Equipment lists** per practical
- **Method sheets** (step-by-step instructions)
- **Risk assessments** (hazards, control measures, CLEAPSS references)
- **Practical classification** (teacher demo vs class practical vs investigation)
- **Required practical mapping** (which practicals are expected/essential)

This means the graph **cannot generate practical lessons** in any usable form. A teacher needs to know: "What equipment do I need for the enzyme investigation? What are the hazards? What does the method look like?" The graph says "investigate enzyme activity" but doesn't say how.

**This is non-negotiable for science.** If this platform claims to generate science resources, it must include practical work or disclaim the gap. Approximately 40% of KS3 Science teaching time involves practical work.

**Recommendation:** Add a Practical node type linked to Concepts, with properties for equipment, method_steps, hazard_level, CLEAPSS_reference, practical_type (demo/class/investigation), and estimated_time.

### 2.3 SIGNIFICANT: NGSS Comparison Is Empty

The CASE standards reference shows:
- 8 NGSS practices listed (no descriptions)
- 20 core ideas listed (no descriptions)
- Crosscutting concepts section is **empty**
- **0 alignment relationships** between UK and US standards

The ConceptCluster "Inspired by" fields reference NGSS ideas (e.g., "Inspired by: NGSS LS1.A - Structure and Function"), which provides useful context. But the actual alignment layer is non-functional.

The most valuable comparison would be structural: the NGSS 3D model (Practices × Core Ideas × Crosscutting Concepts) versus the UK's 2D model (Domains × Working Scientifically). The seven NGSS Crosscutting Concepts — Patterns, Cause and Effect, Scale/Proportion/Quantity, Systems, Energy/Matter, Structure/Function, Stability/Change — are powerful organising principles that the UK curriculum lacks. Adding these as a lens would improve the graph's ability to generate higher-order thinking questions.

### 2.4 SIGNIFICANT: No Assessment Scaffolding

The misconceptions are perfect raw material for diagnostic questions. Every misconception is essentially a ready-made distractor for a multiple-choice question. But the graph provides no:

- Question type guidance per concept (MC, short answer, extended response, practical-based)
- Mark scheme templates or success criteria
- Bloom's taxonomy / cognitive demand classification (the complexity 1-5 scale exists but maps to nothing specific)
- Diagnostic vs summative assessment differentiation
- How to use misconceptions to write questions (the data is there, the method is not)

**Example of what could be generated from existing data:**

Concept C075 (Conservation of mass), Misconception: "mass is lost when substances burn"

> **Diagnostic question (MC):** A student burns 5g of magnesium ribbon in air. The magnesium oxide produced weighs 8.3g. Which statement best explains the mass increase?
> A) Oxygen from the air has combined with the magnesium (CORRECT)
> B) Heat energy has been converted into mass
> C) The balance was not zeroed correctly
> D) Magnesium oxide is a denser material than magnesium
>
> Distractor B targets the mass-energy misconception. Distractor D targets confusion between density and mass.

The graph has ALL the information needed to generate questions like this. It just needs the structural scaffold.

### 2.5 Missing "Big Idea" Narrative Arcs

KS3 Science tells three stories:
- **Biology:** The story of LIFE — from cells → organisms → ecosystems → evolution
- **Chemistry:** The story of MATTER — what things are made of → how they react → patterns → Earth chemistry
- **Physics:** The story of ENERGY and FORCES — what makes things move → why → energy transformations

The ConceptCluster sequencing captures this within domains. But the inter-domain narrative (how D006 Particle Model feeds into D008 Chemical Reactions, which feeds into D010 Earth Chemistry) is only implicit through prerequisites, not explicitly encoded.

**Recommendation:** Consider adding a "Narrative" or "BigIdea" node type that groups domains into their disciplinary stories. This would help the AI generate introductory framing for each topic: "Last half-term we learned what atoms are. This half-term we'll find out what happens when they rearrange..."

### 2.6 Chemistry-Specific Gaps

1. **No hazard/safety data** — The graph mentions "bromine gas" in teaching guidance (C078) but doesn't flag that this is a teacher-only demonstration requiring a fume cupboard. CLEAPSS hazard cards should be referenced.

2. **Flame tests missing** — A standard KS3 practical for identifying metals (lithium = red, sodium = yellow, potassium = lilac, copper = blue-green). Not mentioned anywhere in D009.

3. **Conservation of mass sequencing** — I flagged that C075 (conservation of mass, in D007) only makes sense when demonstrated through reactions (D008). The cross-domain CO_TEACHES captures this, but the cluster structure still places them in separate domains. In practice, I would teach C075 AFTER C081 (reactions as rearrangement), not before.

4. **No practical method for making a salt** — The neutralisation concept (C087) describes the reaction but doesn't include the classic practical: acid + alkali → salt + water, with evaporation to crystallise the salt. This is a core KS3 practical.

### 2.7 Physics-Chemistry Overlap

Two domains cover very similar ground:
- D006 (Chemistry - Particulate Nature of Matter): particle model, states, gas pressure, changes of state
- D015 (Physics - Matter): states properties, particle arrangements, diffusion, physical vs chemical changes, temperature, internal energy

The cross-domain CO_TEACHES links these heavily (9 connections), which correctly flags the overlap. But a teacher planning a scheme of work needs to know: do I teach these as one unit or two? The answer is one — you don't teach the particle model twice. The domain separation creates a false boundary.

---

## 3. Chemistry Term Plan Using Graph Data

To test whether the graph can drive lesson planning, I planned a 12-week Y7 Autumn Chemistry term using only the graph data:

| Week | Domain | Cluster | Content | Practicals (from guidance) |
|------|--------|---------|---------|---------------------------|
| 1-2 | D006 | CL001-CL002 | Particle model, states, gas pressure, changes of state | Heating/cooling water, collapsing can, marshmallow in vacuum |
| 3-4 | D007 | CL001-CL002 | Dalton model, atoms/elements/compounds, symbols, nomenclature | Model building, element samples, periodic table |
| 5-6 | D007 | CL003-CL004 | Pure substances, mixtures, separation, conservation of mass, diffusion | Filtration, evaporation, distillation, chromatography, baking soda + vinegar |
| 7-8 | D008 | CL001-CL002 | Reactions as rearrangement, equations, types of reactions, catalysts | Burning Mg, thermal decomposition CuCO₃, catalase + H₂O₂ |
| 9-10 | D008 | CL003-CL004 | Acids, pH, acid-metal, neutralisation, energy changes | Indicator testing, acid + Mg, neutralisation, exo/endothermic |
| 11 | D009 | CL001-CL002 | Periodic table, Mendeleev, metal/non-metal properties | Element investigation, property comparison |
| 12 | D009 | CL003-CL004 | Reactivity series, metal extraction, materials | Displacement reactions, copper oxide + carbon |

**Verdict:** This works. The graph provides enough structure for a coherent scheme of work. The concept-level detail (teaching guidance, misconceptions, vocabulary) is rich enough to generate lesson content for each session. The cluster sequencing provides the teaching order.

**What I had to add myself:** Practical methods, equipment lists, safety notes, timings, differentiation, Working Scientifically focus for each lesson, homework tasks.

---

## 4. Assessment Generation Potential

### Can the graph generate diagnostic questions?

**Yes, with effort.** Every misconception is a diagnostic question waiting to be written:

| Concept | Misconception | Diagnostic Question Type |
|---------|--------------|------------------------|
| C040 Enzymes | "Enzymes are killed by heat" | MC: distinguish denaturation from death |
| C075 Conservation of mass | "Mass is lost when things burn" | Practical: weigh sealed vs open container |
| C082 Chemical equations | "Change subscripts to balance" | Calculation: spot the error in an equation |
| C084 Acids | "All acids are dangerous" | MC: identify safe acids from a list |
| C121 Forces | "A force is needed for constant motion" | Diagram: identify forces on an object at constant velocity |

The complexity rating (1-5) gives some cognitive demand indication. The keystone flags identify gateway concepts where assessment is critical.

**What's missing:** Mark schemes, grade boundaries, question difficulty calibration, link between complexity rating and Bloom's taxonomy.

### Can the graph generate end-of-topic tests?

**Partially.** A test for D008 (Chemical Reactions) could be constructed:
- MC questions from misconceptions (4-5 questions)
- Short answer from key vocabulary (2-3 questions)
- Extended response from teaching guidance (1 question)
- Practical question from method descriptions (1 question)

But the graph doesn't provide: how many marks per question, what constitutes a good answer, or how to calibrate difficulty.

---

## 5. NGSS Comparison: What We Can Learn

### The 3D Model vs Our 2D Model

| Feature | NGSS | UK (in this graph) |
|---------|------|-------------------|
| Content knowledge | Core Ideas (45) | Concepts (146) — more granular |
| Scientific practices | 8 Practices (integrated) | 12 WS skills (separate) |
| Crosscutting themes | 7 Crosscutting Concepts | None |
| Integration | Every standard = Practice × Core Idea × Crosscutting | Concepts listed by domain, WS listed separately |

**The NGSS advantage:** When NGSS says "Develop a model to describe the cycling of matter" (MS-LS2-3), it integrates the practice (Developing and Using Models), the core idea (LS2.B: Cycles of Matter and Energy Transfer in Ecosystems), and the crosscutting concept (Energy and Matter). The UK curriculum just says "the carbon cycle" (SC-KS3-O092).

**What we should steal from NGSS:**
1. **Crosscutting Concepts** — Adding Pattern, Cause/Effect, Scale, Systems, Energy/Matter, Structure/Function, and Stability/Change as organising nodes would dramatically improve higher-order question generation
2. **Practice integration** — Every concept should link to which WS skills it develops
3. **Performance Expectations** — The NGSS specifies what students should be able to DO, not just what they should know. Our objectives are mostly "knowledge of..." rather than "explain how..." or "investigate why..."

---

## 6. Can the Graph Support These Use Cases?

### 6.1 Generate Learning Content (Interactive Lessons, Simulations)

**YES (7/10).** The concept-level detail is sufficient for text-based lessons, explanation sequences, and vocabulary activities. The misconceptions enable diagnostic question generation. The CO_TEACHES links allow the AI to make connections between related concepts in different disciplines.

**Missing:** Interactive simulation specifications, animation descriptions, practical video scripts.

### 6.2 Generate Test Content (End-of-Topic, Diagnostic)

**PARTIALLY (6/10).** Misconceptions = distractor bank. Key vocabulary = recall questions. Teaching guidance = extended answer prompts. But no mark scheme scaffolding, no difficulty calibration, no question type templates.

### 6.3 Generate Teaching Resources (Slides, Practicals, Risk Assessments)

**PARTIALLY for slides (6/10), NO for practicals (2/10).** The content is there for slide generation. The vocabulary lists are there for keyword activities. But practical methods, equipment lists, and risk assessments are completely absent.

---

## 7. Recommendations (Priority Order)

1. **Integrate Working Scientifically** — Create concept-level `DEVELOPS_SKILL` links to WS nodes. This is the most impactful single change.

2. **Add a Practical Work layer** — Equipment, methods, hazards, CLEAPSS references. Without this, the graph cannot serve science teachers.

3. **Add Crosscutting Concepts** — Borrow from NGSS: Pattern, Cause/Effect, Scale, Systems, Energy/Matter, Structure/Function, Stability/Change. Apply as tags or relationships to existing concepts.

4. **Complete NGSS alignment** — The 0-relationship alignment layer needs populating. The ConceptCluster "Inspired by" fields already contain implicit alignments.

5. **Add assessment scaffolding** — Question type templates, mark scheme patterns, Bloom's mapping for the complexity scale.

6. **Strengthen KS2→KS3 prerequisite links** — Only a handful of cross-key-stage links exist. Y7 teachers need to know exactly what prior knowledge to expect and test for.

7. **Resolve D006/D015 overlap** — Either merge or explicitly sequence these two particle-model domains with clear guidance on teaching order.

8. **Add narrative arc metadata** — "Big Idea" labels that group domains into disciplinary stories (the story of Matter, the story of Life, the story of Energy).

---

## 8. Colleague Messages Sent

- **Kapoor (KS2 Science):** Flagged thin KS2→KS3 prerequisite links; asked about misconception quality in KS2 data
- **Adeyemi (Geography/History):** Flagged Science-Geography overlap in Earth/Atmosphere domain; asked about plate tectonics, climate change, natural hazards cross-links
- **Henderson (Maths):** Flagged heavy numeracy demands in KS3 Science (8+ equations, graph skills, unit conversion); asked about Maths↔Science alignment layer
- **Okonkwo (English):** Flagged scientific literacy demands (1500+ technical vocabulary items, scientific writing conventions); asked about vocabulary scaffolding and writing skill alignment

---

## Summary Table

| Aspect | Rating | Notes |
|--------|--------|-------|
| Content accuracy | 9/10 | Concepts, misconceptions, and vocabulary are excellent |
| Teaching guidance | 8/10 | Practical, detailed, sounds like a real teacher wrote it |
| Cross-domain connections | 8/10 | Best feature — captures genuine scientific interconnections |
| Cluster sequencing | 7/10 | Good within domains, weak between domains |
| Working Scientifically | 3/10 | Listed but not integrated — structural gap |
| Practical work support | 2/10 | Mentioned in text, not structured as data |
| Assessment scaffolding | 4/10 | Misconceptions = raw material, but no scaffolding |
| NGSS comparison | 2/10 | Empty alignment layer, no crosscutting concepts |
| KS2→KS3 transition | 3/10 | Too few explicit prerequisite links |
| Lesson generation potential | 7/10 | Strong for text-based content |
| Test generation potential | 6/10 | Possible with misconception data, needs scaffolding |
| Resource generation potential | 4/10 | Good for slides, poor for practicals |

**Bottom line:** The graph knows WHAT to teach in KS3 Science. It does not yet know HOW to teach it as science — which means integrating practical work, Working Scientifically, and the disciplinary practices that distinguish science from reading about science.
