# Teaching Log -- Mr Kapoor, Y5/6 Science Planning (v3 Graph Data)

**Date:** 22 February 2026
**Teacher:** Mr Kapoor, 12 years' experience, mixed Y5/6 class (28 pupils)
**School:** Rural primary, North Yorkshire
**Domains:** Light (SC-KS2-D005), Forces and Magnets (SC-KS2-D006), Living Things and Their Habitats (SC-KS2-D007)
**Planned teaching:** ~24 science lessons across three half-terms (roughly 8 per half-term, 2 lessons per week)

---

## 1. Initial Observations on the Graph Data

I have used earlier versions of this graph context for planning. This v3 iteration gives me three domains with 14 concepts, 8 clusters (down from 12 previously), prerequisite chains, CO_TEACHES relationships, full teaching guidance, misconceptions, and vocabulary. Two structural changes are immediately apparent.

**Assessment clusters have been removed.** In the previous version I was given 12 clusters including assessment and consolidation types -- several of which suggested 8, 10, even 13 lessons of assessment for two or three concepts. I spent a good portion of my last planning log complaining about those. They have been stripped out entirely. What remains are introduction and practice clusters only. This is a significant improvement. Assessment is a professional judgement that varies by class, by cohort, by the time of year. Encoding it as a fixed cluster with a lesson count was never going to work. Good decision to remove them.

**Cross-domain CO_TEACHES relationships now exist in the system.** The graph has been enriched so that concepts from different domains can be flagged as naturally co-teachable. However -- and this is important for my planning -- for my three domains (Light, Forces and Magnets, Living Things and Their Habitats), the context file confirms there are no cross-domain CO_TEACHES links. All CO_TEACHES relationships are within-domain only. I will return to whether this is correct in Section 3.

**What I have in front of me:**

| Domain | Concepts | Clusters | Objectives |
|--------|----------|----------|------------|
| SC-KS2-D005 Light | 4 | 2 | 9 |
| SC-KS2-D006 Forces and Magnets | 3 | 2 | 6 |
| SC-KS2-D007 Living Things and Their Habitats | 7 | 4 | 7 |
| **Total** | **14** | **8** | **22** |

Eight clusters for 14 concepts across three domains. That is a far more manageable structure than the 12 I had before. My immediate instinct is that 8 clusters for ~24 lessons gives roughly 3 lessons per cluster, which feels about right as a planning unit -- though I will want to vary this significantly by cluster.

First concern, unchanged from last time: **the graph does not distinguish year groups within KS2.** All concepts are labelled "KS2, Age 7-11." For a mixed Y5/6 teacher, knowing which concepts are Y3 retrieval, which are Y5 new learning, and which are Y6 new learning is critical. I can infer this from my own knowledge of the National Curriculum, but the graph should make it explicit. The concept descriptions helpfully mention "In Year 3..." and "In Year 6..." within the text, but there is no structured property I could filter on.

Second concern, also unchanged: **Y5 Forces content is missing.** Domain SC-KS2-D006 covers forces at Y3 level (contact/non-contact, friction, magnets) but not Y5 level (gravity, air resistance, water resistance, levers, pulleys, gears). The domain is named "Forces and Magnets" rather than "Forces" -- which is the Y3 NC programme title -- so perhaps the Y5 content sits in a separate domain. But it was not included in my context, and for a Y5/6 teacher planning "Forces" this is a serious gap. I will note this again in Section 4.

---

## 2. Domain-by-Domain Cluster Analysis

### Domain: Light (SC-KS2-D005) -- 4 concepts, 2 clusters

This domain covers the full KS2 Light progression: the Y3 foundational concepts (light and vision, reflection, shadows) and the Y6 explanatory model (light travels in straight lines). Four concepts, nine statutory objectives, two clusters.

**SC-KS2-D005-CL001 -- "Investigate light sources, vision, and the formation of shadows"**
Type: introduction | Concepts: SC-KS2-C022 (Light and Vision), SC-KS2-C024 (Shadow Formation)

Verdict: **Follow, with compression.**

The pairing is correct. Light and vision (we need light to see, dark is the absence of light) and shadow formation (light blocked by opaque objects) are the two observable, hands-on phenomena that ground the domain. The co_teach_hints link C024 to C067 and C022 to C023, which the cluster rationale acknowledges -- it has correctly placed the foundational pair together and saved the explanatory concepts for the second cluster.

However, for my Y5/6 class this is retrieval content. Both C022 and C024 are Y3 curriculum. My pupils covered this two or three years ago. I will not teach six fresh lessons on "we need light to see." I will compress this cluster into 2 lessons: a retrieval lesson on light sources, vision, luminous versus non-luminous objects (with sun safety from objective O027, which is listed but not linked to any concept -- I will park it here), and an investigation lesson on shadows, opaque/translucent/transparent materials, and how shadow size changes with distance. The second lesson doubles as a Working Scientifically fair test opportunity.

Teaching_weight of 3 on both concepts is reasonable for a Y3 class meeting them for the first time. For my Y5/6 class, the effective weight is more like 1-2 each.

Removing assessment clusters has improved this domain considerably. Previously there was a third cluster (CL003, assessment type) that duplicated the CL002 concepts and suggested 8 lessons of assessment. That is gone. The domain now has a clean two-cluster structure: introduce the phenomena, then explain them. This is exactly right.

**CO_TEACHES within this domain:**
- C023 (Reflection) and C022 (Light and Vision) -- useful; reflection is how we see non-luminous objects
- C023 (Reflection) and C024 (Shadow Formation) -- moderately useful; both are Y3 observable phenomena
- C067 (Straight Lines) and C024 (Shadow Formation) -- very useful; the straight-line model explains shadow shape
- C023 (Reflection) and C067 (Straight Lines) -- very useful; the straight-line model explains reflection
- C024 (Shadow Formation) and C067 (Straight Lines) -- same as above, redundant listing

Five CO_TEACHES relationships for four concepts -- essentially everything is linked to everything. This is accurate for Light: it is a tightly integrated domain where every concept connects. But because everything links to everything, the CO_TEACHES data does not help me discriminate. The cluster assignments (CL001: C022+C024, CL002: C023+C067) do a better job of making the pedagogical cut: phenomena first, explanatory model second.

**SC-KS2-D005-CL002 -- "Explain how light travels in straight lines and is reflected from surfaces"**
Type: practice | Sequenced after: CL001 | Concepts: SC-KS2-C023 (Reflection of Light), SC-KS2-C067 (Light Travels in Straight Lines)

Verdict: **Follow. This is the strongest cluster in my entire context.**

C067 (Light Travels in Straight Lines) is complexity 4, teaching_weight 5 -- the highest in the domain -- and it is genuinely the hardest concept here. It is the Y6 explanatory model that underpins everything: why we see objects, why shadows have the same shape as the object, how reflection works. Pairing it with C023 (Reflection) is exactly right because reflection is the main application of the straight-line model and the most investigable one (mirrors, torch beams, periscopes).

The prerequisite chain confirms this sequencing: C022, C023, and C024 all feed into C067. You establish the phenomena, then introduce the model that explains them.

I will allocate 4 lessons to this cluster: the torch-and-cards straight-line demonstration, ray diagrams for shadows (connecting back to CL001), reflection investigation with mirrors, and a synthesis lesson on "how we see objects" that draws the full ray diagram from source to object to eye. This is the core of my Light unit and where the real Y6 learning happens.

**My Light allocation: 6 lessons total** (2 for CL001, 4 for CL002). Previously I planned 6 lessons and that still holds. The removal of the assessment cluster has not changed my lesson count because I was already ignoring it and planning my own single assessment activity within the final lesson.

**Lesson count realism:** With two clusters totalling 6 lessons, this domain now sits comfortably in a half-term alongside another short unit. The previous version with three clusters and inflated counts was unwieldy on paper even though I was already mentally discounting it. The v3 structure matches how I would actually plan.

---

### Domain: Forces and Magnets (SC-KS2-D006) -- 3 concepts, 2 clusters

Three concepts, six statutory objectives, two clusters. All of this is Y3 content: contact and non-contact forces, friction, magnets.

**SC-KS2-D006-CL001 -- "Identify and compare contact and non-contact forces"**
Type: introduction | Concepts: SC-KS2-C025 (Contact and Non-Contact Forces), SC-KS2-C027 (Friction and Movement on Surfaces)

Verdict: **Follow, with compression.**

The contact/non-contact framework is the correct organising idea for this domain, and friction as the most investigable contact force belongs with it. The CO_TEACHES relationship C027-C025 confirms the pairing. The cluster rationale mentions that friction is "the most investigable example at KS1/early KS2" -- I would quibble with "KS1" since this is KS2 content, but the point stands.

For my Y5/6 class this is again retrieval territory. My pupils did this in Y3. I will teach 2 lessons: a retrieval lesson on the contact/non-contact framework with force arrows, and a friction investigation lesson (ramp, toy car, different surfaces -- the classic fair test). The friction investigation is valuable even as retrieval because it is one of the best Working Scientifically opportunities in the entire science curriculum. Controlling variables, measuring distance, recording in tables, drawing bar charts -- it hits every WS skill.

The external prerequisite from SC-KS1-C026 (Material Properties) to C027 (Friction) is a nice touch. It confirms that understanding different surface textures (rough, smooth) from KS1 Materials underpins the friction investigation. I can use this as a retrieval starter: "What do you remember about the properties of different materials?"

**SC-KS2-D006-CL002 -- "Investigate the properties and uses of magnets"**
Type: practice | Sequenced after: CL001 | Concepts: SC-KS2-C026 (Magnetic Properties)

Verdict: **Follow. Well-sized.**

A single-concept cluster with teaching_weight 3. This is one of the few clusters where the scope feels exactly right. Magnetic properties is a self-contained investigable topic: testing which materials are magnetic, exploring poles and attraction/repulsion, visualising the magnetic field with iron filings, testing whether magnetism passes through materials. Three lessons is appropriate: one for materials testing, one for poles and fields, one for application and assessment.

The CO_TEACHES link between C026 (Magnetic Properties) and C027 (Friction) is, frankly, not useful. These concepts share a domain but they do not naturally co-teach. Friction is about surfaces slowing objects down. Magnetism is about non-contact attraction and repulsion. I would never combine them in a single lesson. I said this last time and I will say it again: CO_TEACHES needs a strength indicator. The C026-C027 link reflects domain proximity, not pedagogical affinity.

**My Forces and Magnets allocation: 5 lessons total** (2 for CL001, 3 for CL002). Same as my previous plan. The removal of the assessment cluster makes no difference here because the previous version only had these two clusters for this domain anyway.

**The elephant in the room: where is Y5 Forces?** The NC requires Year 5 to learn about gravity ("unsupported objects fall towards the Earth because of the force of gravity acting between the Earth and the falling object"), air resistance, water resistance, and mechanisms (levers, pulleys, gears). None of this appears in SC-KS2-D006. I am assuming it sits in a separate domain (perhaps SC-KS2-D0XX "Forces") that was not pulled into my context. For a Y5/6 teacher who has been asked to plan "Forces," receiving only the Y3 content is like being asked to plan a meal and being given only the starter. I need at least another 5-6 lessons for the Y5 content, which I will have to plan independently of the graph.

This is the single biggest gap in my context data. I have raised it before and it remains unresolved.

---

### Domain: Living Things and Their Habitats (SC-KS2-D007) -- 7 concepts, 4 clusters

The largest of my three domains. Seven concepts spanning Y4, Y5, and Y6 content. Four clusters. Previously this domain had seven clusters (including three assessment/consolidation types with absurd lesson counts). The reduction to four is a major improvement.

**SC-KS2-D007-CL001 -- "Classify living things and use classification keys"**
Type: introduction | Concepts: SC-KS2-C028 (Classification Keys), SC-KS2-C029 (Variety of Classification Criteria)

Verdict: **Follow.**

Classification keys and classification criteria are genuinely inseparable. You cannot teach one without the other. The prerequisite chain confirms C029 feeds into C028 (understand that different criteria exist before building a key from specific criteria), and this cluster respects that by including both. This is Y4 content that my class should have covered, but classification keys are notoriously poorly retained. I will use 3 lessons: grouping with different criteria (Venn diagrams, Carroll diagrams), using published branching keys, and making their own keys in a fieldwork session.

Teaching_weight of 3 on each concept is appropriate. Both are complexity 3 skill/knowledge concepts that require practice rather than deep conceptual understanding.

**SC-KS2-D007-CL002 -- "Apply the formal biological classification system including microorganisms"**
Type: practice | Sequenced after: CL001 | Concepts: SC-KS2-C058 (Formal Biological Classification), SC-KS2-C059 (Micro-organisms)

Verdict: **Follow. Strong pairing.**

Formal biological classification (Linnaeus, vertebrates/invertebrates, flowering/non-flowering plants) and micro-organisms belong together because micro-organisms are one of the major classification groups. The CO_TEACHES link C058-C059 is one of the strongest and most genuinely useful in my context. These are Y6 concepts -- new learning for my Year 6 pupils and preview/extension for my Year 5 pupils. Both are complexity 4, teaching_weight 5, reflecting genuine conceptual challenge.

I will allocate 4 lessons: Linnaeus and the classification hierarchy, vertebrate groups and invertebrate diversity (with specimen sorting), micro-organisms (helpful and harmful, with the yeast/bread mould practical), and a classification challenge applying the system to tricky organisms (fungi, coral, whale, bat).

Previously, this cluster was followed by an assessment clone (CL003, 10 lessons). Its removal is an unqualified improvement. I will fold a brief assessment activity into the classification challenge lesson rather than devoting a separate lesson to it.

**SC-KS2-D007-CL003 -- "Compare the life cycles of different types of animals"**
Type: practice | Sequenced after: CL002 | Concepts: SC-KS2-C044 (Comparative Life Cycles), SC-KS2-C045 (Reproduction in Plants and Animals)

Verdict: **Follow. Excellent pairing.**

Life cycles and reproduction are two faces of the same biological idea. The prerequisite C044 -> C045 is correctly modelled: you need to understand what a life cycle looks like before you can understand the reproductive processes that drive it. Both concepts are complexity 4, teaching_weight 5. This is Y5 content -- new learning for my Year 5 pupils, consolidation for Year 6.

The CO_TEACHES link C058-C044 (Formal Classification and Comparative Life Cycles) is interesting. I can see the logic: when you classify organisms you note their reproductive strategies (mammals give live birth, insects undergo metamorphosis). I would make this connection verbally when teaching but would not restructure my cluster sequence for it. It is a useful cross-reference rather than a reason to co-teach.

I will allocate 4 lessons: mammal and bird life cycles, amphibian and insect metamorphosis, sexual and asexual reproduction in plants (with cuttings/runners practical), and a comparison lesson drawing together all reproductive strategies.

Previously this cluster also had an assessment clone. Gone. Good.

**SC-KS2-D007-CL004 -- "Analyse how environmental change affects habitats and living things"**
Type: practice | Sequenced after: CL003 | Concepts: SC-KS2-C030 (Environmental Change and Impact)

Verdict: **Follow. Well-sized.**

A single-concept cluster, teaching_weight 3, complexity 3. Environmental change is Y4 content but connects powerfully to current affairs (climate change, habitat loss, conservation) and to geography. Sequencing it last in the Living Things domain is correct: pupils need to understand classification, life cycles, and reproduction before they can discuss how environmental change threatens species.

The CO_TEACHES link C030-C059 (Environmental Change and Micro-organisms) is genuinely useful. Micro-organisms are decomposers; pollution can kill decomposer communities; this disrupts nutrient cycling. I will make this connection explicit when teaching environmental change and reference back to the micro-organisms lesson. This is the kind of cross-concept link that CO_TEACHES data should surface, and it does.

I will allocate 2 lessons: one on types of environmental change (natural and human-caused) with a food chain impact analysis, and one on conservation case studies with a link to geography.

Previously this domain had a consolidation cluster (CL007, 13 lessons for three concepts). Mercifully removed. I will include a brief end-of-unit assessment within my final lesson rather than dedicating a separate cluster to it.

**My Living Things allocation: 13 lessons total** (3 for CL001, 4 for CL002, 4 for CL003, 2 for CL004). This is my largest unit by far, which matches the fact that it has nearly half my total concepts and spans three year groups of content.

---

### Summary of lesson counts versus cluster structure

| Cluster | Type | Graph concepts | My lessons | Notes |
|---------|------|---------------|------------|-------|
| D005-CL001 | introduction | C022, C024 | 2 | Compressed -- Y3 retrieval for Y5/6 |
| D005-CL002 | practice | C023, C067 | 4 | Core Y6 new learning |
| D006-CL001 | introduction | C025, C027 | 2 | Compressed -- Y3 retrieval |
| D006-CL002 | practice | C026 | 3 | Well-sized as-is |
| D007-CL001 | introduction | C028, C029 | 3 | Y4 retrieval but worth revisiting |
| D007-CL002 | practice | C058, C059 | 4 | Y6 new learning |
| D007-CL003 | practice | C044, C045 | 4 | Y5 new learning |
| D007-CL004 | practice | C030 | 2 | Y4 content, strong geography link |
| | | | **24** | |

Twenty-four lessons. At two per week, that is twelve weeks -- one lesson short of a full three half-terms if I allow for assessment weeks, trips, and SATS preparation. Realistic. The cluster structure gives me eight planning units that map cleanly onto lesson sequences, each with 2-4 lessons. This is genuinely usable.

---

## 3. Cross-Domain Planning

The graph confirms no cross-domain CO_TEACHES relationships for my three domains. Light, Forces and Magnets, and Living Things and Their Habitats are flagged as entirely independent. Is this correct?

**Mostly, yes.** These are three distinct National Curriculum programmes of study with different conceptual foundations. Light is about electromagnetic phenomena. Forces is about mechanical interactions. Living Things is about ecology and classification. A child does not need to understand shadows to learn about magnets, or classification to understand friction.

**But there are connections a teacher would make:**

First, Light (C067, straight-line model) and Forces (C025, non-contact forces). Light is energy that travels in straight lines. Gravity and magnetism are non-contact forces. There is a conceptual parallel: things that "act at a distance" without physical contact. I would draw this parallel in class discussion. However, I agree with the graph that this is not a co-teaching relationship -- the concepts are taught differently and assessed differently.

Second, Living Things (C030, Environmental Change) and Forces (C027, Friction/Surfaces). This is a stretch, but in rural North Yorkshire we discuss how soil erosion (a friction/weathering process) changes habitats. Again, this is a teacher's cross-curricular link, not a co-teaching relationship. The graph is right not to flag it.

Third, Living Things (C059, Micro-organisms) connects naturally to the Year 4 Animals domain (digestive system) and the Year 5 Animals domain (human circulation), but those domains are not in my context. The CO_TEACHES data might pick up those connections within the wider graph -- I cannot tell from my context file.

**My verdict: the graph is correct that these three domains are independent for planning purposes.** I will teach them sequentially rather than interleaving, and the order is flexible. No cross-domain prerequisites, no mandatory co-teaching. This gives me freedom to sequence by practical considerations (equipment availability, fieldwork timing, assessment calendar) rather than conceptual dependency.

My sequencing decision:
1. **Light** (Autumn 2, 6 lessons) -- strong practicals with torches and mirrors, works well in darker months
2. **Forces and Magnets** (Spring 1, 5 lessons) -- short unit, pairs well with Y5 Forces extension content I will plan separately
3. **Living Things** (Spring 2 into Summer 1, 13 lessons) -- fieldwork for classification keys benefits from spring weather; environmental change links to summer geography

---

## 4. Overall Assessment

### Rating: 7 out of 10

This is a meaningful improvement over the previous version. The removal of assessment clusters has fixed the most egregious problem (absurd lesson counts for assessment and consolidation). The remaining 8 clusters are well-constructed, with sensible concept pairings and logical sequencing. The enrichment data -- teaching guidance, misconceptions, vocabulary -- remains excellent and is the single most valuable feature. The CO_TEACHES relationships within domains are useful for confirming concept pairings, even if they lack discrimination (everything links to everything in a small domain like Light).

I am not giving it higher than 7 because two structural problems remain unresolved, and a third has emerged.

### Top 3 Remaining Gaps

**1. Year group attribution within KS2 -- still missing, still critical.**

Every concept in my context is labelled "KS2, Age 7-11." For a mixed Y5/6 class, I need to know: is this Y3 retrieval content that my pupils covered two years ago? Y4 content they covered last year? Y5 new learning for half the class? Y6 new learning for the other half? I can work this out from my knowledge of the NC, but the graph should encode it. The concept descriptions mention year groups in prose ("In Year 3, this is the observable phenomenon; in Year 6, it is explained using the straight-line model") -- this information exists in the data, it simply is not structured as a filterable property. Adding a `year_group` or `nc_year` property to each concept would transform the usefulness of this tool for any teacher in a year-group or mixed-age class, which is every primary teacher in England.

**2. Y5 Forces content is absent from my context.**

Domain SC-KS2-D006 (Forces and Magnets) contains only Y3 content. The Y5 Forces programme -- gravity, air resistance, water resistance, mechanisms (levers, pulleys, gears) -- is not here. I have been asked to plan "Forces" for a Y5/6 class and have received only the Y3 foundation. This may be a data extraction issue (the Y5 content might sit in a separate domain that was not included in my pull) or a gap in the curriculum modelling. Either way, it means I cannot plan roughly a third of my forces teaching from the graph data. I will need to plan gravity, air resistance, and mechanisms from the NC document directly.

Specifically, I would expect concepts like: "gravity as a force that pulls unsupported objects towards the Earth," "air resistance, water resistance, and friction as forces that act between moving surfaces," and "simple mechanisms including levers, pulleys, and gears allow a smaller force to have a greater effect." These are statutory Y5 content. Their absence is a significant gap.

**3. No Working Scientifically integration with content concepts.**

This is not new, but it becomes more noticeable when the cluster structure is cleaner. The NC specifies that Working Scientifically skills should be taught through content domains, not in isolation. The graph has a separate WS domain (SC-KS2-D001) with its own concepts, but none of those WS concepts are linked to my content concepts or clusters. For primary science, where the practical investigation IS the lesson, this is a major omission. Even a simple tag per concept or cluster -- "fair_test," "observation," "classification," "pattern_seeking," "secondary_research" -- would help teachers plan WS coverage. Currently I have to design all practical investigations from my own experience, which I can do after 12 years, but a less experienced teacher would struggle.

### Specific Recommendations for Improvement

1. **Add `nc_year` property to concepts.** Values: Y3, Y4, Y5, Y6. Even where the NC groups content across years (e.g., "Lower KS2"), the standard teaching allocation is well established and uncontroversial.

2. **Locate and include Y5 Forces content.** If it exists in a separate domain, include it when a teacher requests "Forces" for Y5/6. If it does not exist, extract it from the NC and create the concepts. The statutory objectives are O063-O068 (roughly -- the "explain that unsupported objects fall towards the Earth" block).

3. **Add WS skill tags to content concepts or clusters.** A property like `ws_enquiry_type: ["fair_test", "observation"]` on each concept would allow teachers to plan WS coverage across a unit without needing to do it manually.

4. **Add strength to CO_TEACHES.** A simple "strong" / "moderate" / "weak" label would help distinguish genuinely inseparable pairs (C058-C059, Classification and Micro-organisms) from domain-proximity associations (C026-C027, Magnets and Friction).

5. **Link orphan objectives to concepts.** Objective SC-KS2-O027 (sun safety) is listed under Light but not connected to any concept. I had to manually place it. Any objective without a concept link should be flagged.

### What I will use from the graph, and what I will ignore

**Using:**
- Cluster concept pairings (all 8 clusters) -- as the basis for my lesson groupings
- Prerequisite chains -- for sequencing within and across domains
- CO_TEACHES C058-C059, C044-C045, C023-C067, C030-C059 -- genuinely useful co-teaching signals
- Teaching guidance and misconceptions -- excellent, practical, specific
- Vocabulary lists -- will form the basis of my working walls
- External prerequisites (e.g., KS1 Material Properties -> Friction) -- for retrieval starters

**Ignoring or supplementing:**
- Cluster lesson counts (not explicitly given in v3, which is an improvement -- I set my own)
- CO_TEACHES C026-C027 (Magnets and Friction) -- domain proximity, not pedagogical affinity
- The absence of Y5 Forces content -- I will plan this independently
- The absence of WS integration -- I will map my own WS skills onto content lessons
- The lack of year group attribution -- I will use my NC knowledge to differentiate Y5 and Y6 expectations

### Final reflection

The v3 graph data is noticeably more usable than what I had before. Removing the assessment clusters was the right call -- it eliminated the most unrealistic element and left a clean structure of introduction and practice clusters that I can actually map onto my weekly planning. The concept pairings within clusters are sound, the sequencing is logical, and the enrichment data (guidance, misconceptions, vocabulary) remains the standout feature.

The two persistent structural gaps -- year group attribution and missing Y5 Forces -- prevent this from being a complete planning tool. I still need the NC document open alongside the graph context. But as a starting framework that saves me from a blank page and gives me well-reasoned concept groupings, accurate prerequisite chains, and rich pedagogical notes, it earns its place in my planning workflow. An NQT or second-year teacher would benefit enormously from the teaching guidance and misconceptions data alone. The graph is getting closer to being something I would recommend to colleagues.

---

*Teaching log complete. Mr Kapoor, February 2026.*
