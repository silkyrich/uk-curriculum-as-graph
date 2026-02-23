# Teaching Log -- KS3 Chemistry Planning (Revised)
## Dr Osei, Science Department, Bristol

**Date:** 2026-02-22
**Domains covered:** SC-KS3-D007 (Atoms, Elements and Compounds) and SC-KS3-D008 (Chemical Reactions)
**Total concepts:** 20 (10 per domain)
**Planned lessons:** ~24 across two half-terms
**Graph version:** v3.7 with curated cross-domain CO_TEACHES and assessment clusters removed

---

## 1. Initial Observations on the Graph Data

### What I have

The context file provides data for two chemistry domains: SC-KS3-D007 (Atoms, Elements and Compounds, 10 concepts, 4 clusters) and SC-KS3-D008 (Chemical Reactions, 10 concepts, 4 clusters). Each concept has a teaching weight (1-6), complexity rating, teaching guidance, common misconceptions, and key vocabulary. Prerequisite chains are provided within and between domains. CO_TEACHES relationships are provided within each domain and -- this is new -- across domains.

The total cluster count is now 8 (4 per domain), down from the 15 I was working with last time (7 in D007, 8 in D008). This is a dramatic structural improvement and I will explain why below.

### What has changed since my last planning pass

Three significant changes have been made to the graph data since I last evaluated it, and all three address concerns I raised explicitly in my previous teaching log. I want to acknowledge that.

**First, assessment and consolidation clusters have been removed.** Previously, every content cluster was followed by an assessment cluster of equal lesson count and sometimes a consolidation cluster as well. This was the single biggest structural problem I identified: 5-lesson or 10-lesson assessment blocks that no real teacher would ever plan. D007 previously had CL002 (5-lesson assessment), CL005 (10-lesson assessment), and CL007 (10-lesson consolidation). D008 had CL002, CL004, CL006, and CL008 -- all assessment or consolidation blocks. All of these are now gone. The remaining clusters are typed as "introduction" or "practice," which is a much more honest representation of what these groupings actually are: units of teaching, not units of assessment. I will plan my own assessment around them.

**Second, cross-domain CO_TEACHES relationships have been added.** These are the three curated connections I specifically requested:

- C074 (Chemical symbols) <-> C082 (Chemical equations) -- with rationale: "Chemical symbols are the language, equations are the grammar."
- C073 (Atoms, elements, compounds) <-> C081 (Reactions as atom rearrangement) -- with rationale: "Teaching atoms/elements/compounds and chemical reactions is a continuous narrative."
- C075 (Conservation of mass) <-> C081 (Reactions as atom rearrangement) -- with rationale: "Conservation of mass only makes sense when demonstrated through actual reactions."

These are attributed to me ("Osei identified..."), which I appreciate. The rationales accurately capture the pedagogical reasoning I described. I will analyse them in detail in section 3.

**Third, the cluster types have been streamlined.** D007 now has 1 introduction cluster and 3 practice clusters. D008 has 1 introduction cluster and 3 practice clusters. The distinction between "introduction" and "practice" is applied more consistently than before, though I still have a quibble about "practice" labels on genuinely new content (see below).

### What has not changed

The Learner Profile section still appears as a heading with no content. Working Scientifically skills are still absent from the context file. These remain gaps, though they are outside the scope of what the cluster restructuring aimed to fix, so I will note them but not dwell on them.

---

## 2. Domain-by-Domain Cluster Analysis

### SC-KS3-D007: Atoms, Elements and Compounds

#### SC-KS3-D007-CL001 -- Describe atoms, elements and compounds using the Dalton model
**Type:** Introduction | **Keystone:** Yes | **Curated:** Yes
**Concepts:** C072 (Dalton atomic model, weight 2), C073 (Atoms, elements, compounds, weight 3)
**Sequenced after:** None (first cluster)

**Decision: FOLLOW. Allocate 3 lessons.**

This is unchanged from the previous version and remains the correct starting point. The Dalton model (C072) is prerequisite for atoms/elements/compounds (C073), and these two concepts form the conceptual gateway to all of KS3 chemistry. The rationale is well written: "the conceptual entry point for all KS3 chemistry classification."

With the assessment clusters removed, I no longer need to plan around a phantom 5-lesson assessment block after this cluster. Instead, I will embed a brief formative check (10-minute quiz) at the end of lesson 3 before moving on. This is how assessment actually works in a classroom.

**Lesson allocation:** Lesson 1 (Dalton model, historical narrative, molecular models), Lesson 2 (atoms vs elements vs compounds, sorting activity), Lesson 3 (practice and consolidation with particle diagrams, formative check). Total weight = 5; I am compressing slightly because both concepts are accessible at this age and the heavy application comes later.

**Cross-domain CO_TEACHES note:** C073 now has a curated cross-domain link to C081 (reactions as atom rearrangement) with reason "continuous_narrative." This is accurate -- when I teach atoms, elements and compounds in lesson 2, I will explicitly flag that "in the second half-term, we will see what happens when atoms of different elements rearrange." This forward hook is now supported by the graph data rather than being something I add informally.

#### SC-KS3-D007-CL002 -- Use chemical symbols and apply IUPAC naming to elements and compounds
**Type:** Practice | **Curated:** Yes
**Concepts:** C023 (Chemical nomenclature, weight 3), C074 (Chemical symbols, weight 2)
**Sequenced after:** CL001

**Decision: FOLLOW, but reclassify mentally as "new content." Allocate 4 lessons.**

The cluster label says "practice," but pupils are encountering chemical symbols and IUPAC naming for the first time. This is new content. I raise this point again because it matters for how I structure lessons -- "practice" implies pupils have already been introduced to the ideas, which they have not. The cluster rationale correctly describes these as "the language tools of chemistry," which is an introduction, not practice.

That said, the grouping itself is spot on. C074 and C023 co-teach naturally (the CO_TEACHES link between them is confirmed), and the sequencing after CL001 is correct -- you need to know what elements and compounds are before you can name them.

**Lesson allocation:** Lesson 4 (chemical symbols, periodic table orientation, common element symbols), Lesson 5 (writing simple formulae -- H2O, CO2, NaCl -- counting atoms), Lesson 6 (IUPAC nomenclature rules: -ide, -ate, -ite suffixes; naming from formulae), Lesson 7 (practice: periodic table treasure hunt, naming challenge, formative check). This cluster needs 4 lessons because nomenclature requires repeated practice. The total teaching weight is 5; I am allocating 4 lessons, which is a slight compression justified by the fact that symbols and naming overlap heavily.

**Cross-domain CO_TEACHES note:** C074 now links to C082 (chemical equations) with the curated rationale "symbols are the language, equations are the grammar." This is exactly right. In lessons 4-5, I will tell pupils explicitly: "You need to know these symbols fluently because in the second half-term, you will write equations using them." The graph now provides the structural basis for this forward reference.

#### SC-KS3-D007-CL003 -- Distinguish pure substances from mixtures and apply separation techniques
**Type:** Practice | **Curated:** Yes
**Concepts:** C076 (Pure substances, weight 2), C077 (Mixtures, weight 2), C079 (Separation techniques, weight 3), C080 (Identifying pure substances, weight 3)
**Sequenced after:** CL002

**Decision: FOLLOW the grouping. Allocate 6 lessons.**

This is the practical heart of D007. Four concepts, all tightly co-taught (the within-domain CO_TEACHES matrix for C076/C077/C079/C080 is extremely dense -- every concept links to every other). The cluster rationale correctly notes the "practical application of filtration, distillation and chromatography."

Previously, this cluster had 10 lessons and I argued for reducing to 7-8. Now with assessment clusters removed, the cluster itself does not carry a lesson count -- it is simply a grouping. I can allocate what I think is right. 6 lessons gives me:

- Lesson 8: Pure substances vs mixtures (theory, definitions, melting point data)
- Lesson 9: Mixtures and dissolving (solute, solvent, solution, saturated solutions)
- Lesson 10: Separation practical 1 (filtration and evaporation -- sand/salt separation)
- Lesson 11: Separation practical 2 (distillation -- separating ink from water)
- Lesson 12: Separation practical 3 (chromatography -- separating food dyes)
- Lesson 13: Identifying pure substances (melting point determination, chromatography Rf values, end-of-topic formative assessment)

The prerequisite chain C076 -> C077 -> C079 -> C080 is linear and I will follow it exactly. Separation techniques (C079) at weight 3 still underestimates the practical time required -- each technique needs a full lesson with setup, execution, and write-up -- but now that lesson counts are not auto-generated from weights, this is my problem to solve rather than the graph's.

**Removing assessment clusters improved this cluster significantly.** Previously, CL004 (content) was followed by CL005 (assessment, 10 lessons) and CL007 (consolidation, 10 lessons). The total allocation for this content was 30 lessons. Now it is a single cluster with no prescribed lesson count, and I allocate 6. That is a move from absurd to usable.

#### SC-KS3-D007-CL004 -- Explain diffusion in chemistry and conservation of mass in changes
**Type:** Practice | **Curated:** Yes
**Concepts:** C075 (Conservation of mass, weight 3), C078 (Diffusion in chemistry, weight 3)
**Sequenced after:** CL003

**Decision: PARTIALLY FOLLOW. Teach diffusion here; relocate conservation of mass to D008. Allocate 2 lessons for diffusion.**

**The C075 sequencing issue is still present.** This is my most important finding. The cluster places conservation of mass (C075) in D007-CL004, which is sequenced before any D008 cluster. But the external prerequisite data clearly states: C081 (Reactions as atom rearrangement, in D008) -> C075 (Conservation of mass). The curated cross-domain CO_TEACHES link even carries my own rationale: "conservation of mass only makes sense when demonstrated through actual reactions."

So the graph data is internally contradictory. The cross-domain CO_TEACHES relationship correctly identifies that C075 and C081 should be co-taught with reactions providing context. But the cluster structure still places C075 in a D007 cluster that precedes D008. The cluster algorithm has not consumed the cross-domain relationship data when determining sequencing.

This is the same issue I flagged in my previous log. The cross-domain CO_TEACHES link is a step forward -- it gives me the rationale I need to justify moving C075. But the cluster itself has not been fixed.

**My solution is the same as before:** I will teach C078 (diffusion) here as the final topic of D007 (1-2 lessons: bromine diffusion demo, KMnO4 in water practical, rate of diffusion comparison). Then I will teach C075 (conservation of mass) at the start of D008, integrated with C081 (reactions as atom rearrangement), where the prerequisite places it.

**Diffusion (C078)** fits well at the end of D007. It connects back to mixtures (C077 CO_TEACHES C078) and to the particle model (external prerequisite from C068). It is a good bridging topic between the "substances and mixtures" content and the "reactions" content -- it reminds pupils of particle behaviour before we introduce the idea that particles rearrange in reactions.

**Lesson allocation for D007-CL004:** Lesson 14 (diffusion theory and demos), Lesson 15 (diffusion practical and rate comparison). Conservation of mass moves to D008.

**D007 total: 15 lessons (half-term 1 plus 3 weeks of half-term 2).**

---

### SC-KS3-D008: Chemical Reactions

#### SC-KS3-D008-CL001 -- Explain reactions as atom rearrangement and write chemical equations
**Type:** Introduction | **Keystone:** Yes | **Curated:** Yes
**Concepts:** C081 (Reactions as atom rearrangement, weight 3), C082 (Chemical equations, weight 4)
**Sequenced after:** None (first D008 cluster)

**Decision: FOLLOW, with C075 (Conservation of mass) integrated. Allocate 5 lessons.**

This is correctly identified as the keystone introduction for chemical reactions. The rationale is accurate: "the conceptual model and its symbolic representation are the foundation of all chemical reaction understanding." C081 and C082 are the right pair. Chemical equations (C082) at weight 4 remains the highest-weighted concept across both domains, correctly reflecting that balancing equations is the most challenging KS3 chemistry skill.

I will integrate C075 (conservation of mass, moved from D007-CL004) into this cluster. The sequence becomes: C081 (reactions rearrange atoms) -> C075 (atoms are conserved, so mass is conserved) -> C082 (we represent this with balanced equations). This is a coherent narrative: what happens -> why it matters -> how we write it down.

The curated cross-domain CO_TEACHES link between C075 and C081 directly supports this integration. The rationale states "these concepts should be co-taught with reactions providing the concrete context." I agree completely. Conservation of mass is not an abstract principle -- you demonstrate it by weighing a sealed reaction vessel before and after a reaction, showing that the mass does not change. You need actual reactions for that demonstration.

**Lesson allocation:**
- Lesson 16: Reactions as atom rearrangement (molecular models, animations, contrast with physical changes)
- Lesson 17: Conservation of mass (sealed container reaction on balance, open vs closed system)
- Lesson 18: Word equations (reactants, products, arrow notation)
- Lesson 19: Symbol equations and balancing (counting atoms, adjusting coefficients)
- Lesson 20: Balancing practice (progressively harder equations, molecular models alongside written equations)

C082 gets 3 of the 5 lessons, reflecting its weight of 4 and the fact that equation balancing requires sustained practice. This is one concept where you cannot rush -- pupils need to develop procedural fluency through repetition.

#### SC-KS3-D008-CL002 -- Identify and describe different types of chemical reactions
**Type:** Practice | **Keystone:** Yes | **Curated:** Yes
**Concepts:** C083 (Types of reactions, weight 3), C088 (Catalysts, weight 2)
**Sequenced after:** CL001

**Decision: FOLLOW. Allocate 3 lessons.**

Combustion, thermal decomposition, oxidation, displacement, and catalysts. The grouping of C083 with C088 is justified by the CO_TEACHES link and by the fact that catalysis is best taught through a specific reaction type (catalytic decomposition of hydrogen peroxide). The rationale correctly identifies this connection.

I still note that the "practice" label is misleading -- pupils are meeting these reaction types for the first time. But with assessment clusters removed, the label matters less; I know what I am teaching regardless of what the cluster calls it.

**Lesson allocation:**
- Lesson 21: Combustion and thermal decomposition (burning Mg demo, heating CuCO3)
- Lesson 22: Oxidation and displacement (iron rusting, Zn + CuSO4 practical)
- Lesson 23: Catalysts (MnO2 + H2O2 demo, enzyme connection to SC-KS3-C040, writing equations for all reaction types studied)

Three lessons is tight but achievable. Each lesson includes a practical demonstration and equation writing. The teaching weight sum is 5; I am compressing to 3 because each reaction type is conceptually straightforward at KS3 -- the challenge is in writing the equations, which pupils have already practised in CL001.

#### SC-KS3-D008-CL003 -- Investigate acids and alkalis using the pH scale and neutralisation
**Type:** Practice | **Keystone:** Yes | **Curated:** Yes
**Concepts:** C084 (Acids and alkalis, weight 3), C085 (pH scale, weight 2), C086 (Acid-metal reactions, weight 2), C087 (Neutralisation, weight 2)
**Sequenced after:** CL002

**Decision: FOLLOW. This is excellent. Allocate 4 lessons.**

This is the strongest cluster in either domain. The grouping of C084/C085/C086/C087 is exactly how every experienced chemistry teacher organises the acids topic. The CO_TEACHES matrix for these four concepts is extremely dense, confirming they form a natural teaching unit. The rationale ("coherent practical investigation sequence with indicators and neutralisation experiments") is accurate and actionable.

The prerequisite structure is clear: C084 (acids and alkalis) is the gateway, with C085, C086, and C087 all depending on it but not on each other. This gives me flexibility in sequencing after the introductory lesson.

**Lesson allocation:**
- Lesson 24: Acids, alkalis and the pH scale (household substances with universal indicator, pH paper and meters, introduce the concepts together since C085 is essentially the measurement tool for C084)
- Lesson 25: Acid-metal reactions (Mg + HCl, squeaky pop test, different metals to link to reactivity series)
- Lesson 26: Neutralisation (NaOH + HCl with indicator, antacid investigation, temperature measurement to foreshadow energy cluster)
- Lesson 27: Acids topic consolidation and formative assessment (writing equations for all acid reactions, practical skills assessment)

The teaching weight total is 9; I allocate 4 lessons. This compression is justified because the four concepts overlap heavily -- you are essentially teaching one topic (acids) through four lenses, not four separate topics. The practical work is what takes the time, and each lesson has a clear practical focus.

#### SC-KS3-D008-CL004 -- Explain energy changes in chemical reactions and changes of state
**Type:** Practice | **Curated:** Yes
**Concepts:** C089 (Energy in state changes, weight 2), C090 (Exothermic and endothermic, weight 3)
**Sequenced after:** CL003

**Decision: FOLLOW. Allocate 2 lessons.**

C089 and C090 are correctly paired. Energy in state changes provides the bridge from the physical chemistry of D007 to the thermochemistry that underpins reaction understanding. Exothermic and endothermic reactions are a qualitative treatment at KS3 -- no calculations, just classification and simple energy diagrams.

The external prerequisite (C071, changes of state -> C089) is satisfied because the particle model was taught earlier in the year. The CO_TEACHES link between C089 and C090 confirms they should be taught together.

**Lesson allocation:**
- Lesson 28: Energy in state changes and exothermic/endothermic (heating curves, hand warmers, cold packs, citric acid + NaHCO3, energy level diagrams)
- This could be 2 lessons if I split state changes from reaction energy, but in practice Year 8 pupils can handle both in a well-structured double lesson or in a single lesson if I am efficient with the practicals.

I will use this as the final teaching lesson, followed by an end-of-unit assessment in a separate lesson (not counted in my 24-lesson allocation, as assessments are scheduled by the department).

**D008 total: ~14 lessons (remainder of half-term 2).**
**Combined total: ~28-29 lessons including assessment, but 24-26 for new content and practice.**

---

## 3. Cross-Domain Planning

### Evaluating the curated cross-domain CO_TEACHES links

The three curated cross-domain links between D007 and D008 are the most significant improvement in this version of the graph data. Let me evaluate each one.

**C073 (Atoms, elements, compounds) <-> C081 (Reactions as atom rearrangement)**
Reason: continuous_narrative
Rationale: "Teaching atoms/elements/compounds and chemical reactions is a continuous narrative."

This is accurate and well articulated. When I teach C073, the distinction between elements and compounds is partly defined by what happens in chemical reactions -- compounds are formed when atoms of different elements bond, and those bonds can be broken and reformed in reactions. The concept of C081 (atom rearrangement) is the dynamic counterpart to the static classification of C073. The "continuous_narrative" reason correctly captures this -- these are not just related concepts, they are sequential chapters of the same story.

**How I use this link:** In lesson 2 (C073), I will say "compounds form when atoms bond together -- and in half-term 2, we will see that chemical reactions are what happens when those bonds break and reform." In lesson 16 (C081), I will begin by recalling C073: "Remember how we classified substances into elements and compounds? Now we are going to see what happens when compounds react." The cross-domain link gives me explicit permission to make this forward and backward reference.

**C074 (Chemical symbols) <-> C082 (Chemical equations)**
Reason: continuous_narrative
Rationale: "Chemical symbols are the language, equations are the grammar."

This is the most practically useful of the three links. Symbol fluency is genuinely prerequisite for equation writing, and the metaphor of language/grammar captures the relationship well. In my experience, pupils who struggle with balancing equations almost always have weak symbol recall -- they cannot focus on the logic of balancing because they are still trying to remember what Fe or Na means.

**How I use this link:** I will explicitly tell pupils in lessons 4-5 (C074) that symbol fluency is the key to success in the equations work. I will design a symbols quiz that I repeat at the start of every lesson in the D008 sequence until pupils achieve automaticity. The cross-domain link justifies this spaced retrieval practice.

**C075 (Conservation of mass) <-> C081 (Reactions as atom rearrangement)**
Reason: continuous_narrative
Rationale: "Conservation of mass only makes sense when demonstrated through actual reactions."

This is the link that addresses my previous sequencing concern. The rationale is correct -- conservation of mass is an abstract principle that only becomes concrete when you can weigh reactants and products. The "continuous_narrative" reason is appropriate: atom rearrangement explains WHY mass is conserved (no atoms created or destroyed), and conservation of mass is the observable CONSEQUENCE of atom rearrangement.

**How I use this link:** As described above, I integrate C075 into D008-CL001 rather than teaching it in D007-CL004. The cross-domain CO_TEACHES link provides the justification. However, I note again that the cluster structure itself has not been updated to reflect this -- C075 is still assigned to D007-CL004. The link tells me what to do; the cluster does not yet do it automatically.

### Cross-domain connections still missing

The three curated links are a strong start, but there are additional cross-domain connections that would be valuable:

1. **C079 (Separation techniques, D007) <-> C083 (Types of reactions, D008).** The distinction between physical separation (filtration, distillation) and chemical reactions (combustion, decomposition) is a fundamental conceptual boundary. Pupils need to understand that separation techniques do not change substances, while reactions create new substances. This contrast is one of the most important teaching points when transitioning between D007 and D008.

2. **C077 (Mixtures, D007) <-> C084 (Acids and alkalis, D008).** Acid solutions are mixtures (acid dissolved in water). Understanding what a solution is (from the mixtures work) is essential for understanding what happens when you add a metal to an acid solution or mix an acid with an alkali. This is a prerequisite relationship that the graph does not currently capture.

3. **C023 (Chemical nomenclature, D007) <-> C086 (Acid-metal reactions, D008) and C087 (Neutralisation, D008).** Naming the salt products of acid reactions is a direct application of nomenclature rules: hydrochloric acid produces chlorides, sulfuric acid produces sulfates. Pupils need C023 to predict and name products in C086 and C087. This is a continuous_narrative connection that would be very useful.

4. **C080 (Identifying pure substances, D007) <-> C083 (Types of reactions, D008).** Chromatography is used to identify the products of some reactions. More broadly, knowing how to test for purity is relevant when you are making products by chemical reaction.

---

## 4. Overall Assessment

### Rating: 8/10

This is a meaningful improvement over the previous version, which I rated 7/10. The two-point areas of improvement are:

- **Removing assessment clusters (+1).** This single change transforms the usability of the data. Previously, 7 of the 15 clusters were assessment or consolidation blocks with inflated lesson counts that no teacher would follow. Now all 8 clusters are teaching units. I no longer need to mentally filter out half the data. This is the most impactful change.

- **Adding cross-domain CO_TEACHES links (+0.5).** The three curated links between D007 and D008 are accurate, well-rationed, and directly actionable. They encode pedagogical knowledge about the transition between domains that was previously invisible in the graph.

- **Curated cluster rationales (+0.5).** The [CURATED] tag and the NGSS-inspired rationales add transparency about why clusters are structured as they are. The rationales for D008-CL001 and D008-CL003 are particularly good.

I deduct 2 points for the following remaining issues:

- **C075 sequencing is still structurally unresolved (-0.5).** The cross-domain CO_TEACHES link correctly identifies the issue, but the cluster assignment has not changed. C075 is still in D007-CL004. A teacher who follows the clusters as written will teach conservation of mass before reactions. The graph data is internally contradictory: the relationship says "co-teach these," but the cluster says "teach C075 first, in a different domain." This needs to be resolved by either moving C075 to D008-CL001 or creating a cross-domain cluster.

- **No Working Scientifically integration (-0.5).** Still absent. Every practical lesson in this sequence develops Working Scientifically skills (planning, measuring, recording, analysing), and the graph should surface which skills each cluster develops. This is a statutory requirement of the National Curriculum.

- **Missing Learner Profile data (-0.5).** The section heading exists but remains empty. For Year 8 planning, I need to know about recommended reading level, mathematical demand, and appropriate levels of abstraction.

- **"Practice" label on new content clusters (-0.5).** D007-CL002, D007-CL003, D008-CL002, and D008-CL003 are all labelled "practice" but contain concepts pupils encounter for the first time. A cluster where pupils first meet chemical symbols, separation techniques, reaction types, or the pH scale is not "practice" -- it is introduction. The type taxonomy needs a clearer definition or a third category.

### Top 3 remaining gaps

1. **C075 cluster assignment contradicts its own prerequisite and CO_TEACHES data.** Fix: move C075 to D008-CL001 or flag the cross-domain dependency in the cluster sequencing algorithm.

2. **Working Scientifically skills are not linked to any concept or cluster.** Fix: add CO_TEACHES or DEVELOPS_SKILL relationships from concepts to WorkingScientifically nodes, so the context file can surface which skills each cluster develops.

3. **Missing cross-domain CO_TEACHES links for nomenclature -> acid naming (C023 <-> C086/C087) and mixtures -> acid solutions (C077 <-> C084).** These are high-value connections for teaching the transition between D007 and D008 that the graph does not yet capture.

### Specific recommendations for improvement

1. **Resolve the C075 contradiction.** Either move C075 into a D008 cluster, or split D007-CL004 so that diffusion (C078) stands alone in D007 and conservation of mass (C075) is explicitly assigned to D008-CL001. The cross-domain CO_TEACHES link already provides the rationale.

2. **Define cluster types more precisely.** "Introduction" should mean "first encounter with these concepts." "Practice" should mean "applying or reinforcing previously introduced concepts." Currently, "practice" is used for clusters that contain genuinely new content. This confuses the signal.

3. **Add Working Scientifically tagging.** Each cluster should list 1-2 Working Scientifically skills it develops. For example, D007-CL003 (separation techniques) develops "making accurate measurements" and "planning enquiries." D008-CL003 (acids) develops "recording data" and "evaluating methods." This would make the context file usable as a complete planning tool rather than a content-only reference.

4. **Add 2-3 more cross-domain CO_TEACHES links** as described in section 3, particularly C023 <-> C086/C087 (nomenclature to salt naming) and C077 <-> C084 (mixtures to acid solutions).

5. **Consider adding suggested assessment checkpoints.** Rather than dedicated assessment clusters, add a property to clusters indicating natural assessment points. For example, D007-CL001 (keystone) could carry a flag "formative check recommended after this cluster." D008-CL003 could carry "summative assessment point -- end of acids topic." This gives teachers assessment guidance without consuming lesson time.

### Final reflection

The graph data is now a genuinely useful starting point for chemistry planning. The concept groupings are sound, the CO_TEACHES relationships encode real pedagogical knowledge, the teaching guidance and misconceptions are classroom-ready, and the removal of assessment clusters has made the structure much more realistic. An experienced teacher can take these 8 clusters and build a coherent 24-lesson scheme of work with minimal deviation. A less experienced teacher would benefit from the rationales and CO_TEACHES connections as a guide to sequencing decisions they might otherwise struggle with.

The remaining issues -- C075 sequencing, Working Scientifically, cluster type labels -- are all fixable without restructuring the core model. The cross-domain CO_TEACHES links are the most promising new feature, and expanding them to cover the nomenclature-to-naming and mixtures-to-solutions connections would add further value.

This is good work. I can plan from this.

-- Dr Osei, 22 February 2026
