# Gap Analysis: Ms. Brennan -- Art KS2 (Lowry Industrial Landscapes)

**Planner:** Lowry Industrial Landscapes
**Date:** February 2026 (V8 review)
**V7 score:** 7.5/10 (Fractions cluster) -> **V8 early score:** 8.5/10 (Measurement cluster with CPA) -> **V8 planner score:** 5.5/10

---

## Top 5 Data Additions That Would Improve This Planner

### 1. Vehicle Template Integration -- Surface a Lesson Sequence

The graph has 24 VehicleTemplate nodes with TEMPLATE_FOR relationships to KeyStages. An Art KS2 artist study template should provide a generic lesson structure: introduce the artist and context, study techniques, experiment with materials, develop skills through practice, create a final piece. The planner currently has "Estimated duration: 5 lessons" but no indication of what those 5 lessons contain.

If the auto-generator surfaced the relevant vehicle template with its age-banded `agent_prompt`, a non-specialist would have a complete sequence without needing to invent one. This is the single highest-impact addition because it transforms the planner from a content briefing into an actionable teaching plan.

### 2. Vocabulary Definitions -- Populate the Word Mat

The vocabulary word mat lists 8 terms with empty "Meaning" columns. The concept nodes contain `key_vocabulary` lists, and the concept descriptions contain enough contextual information to derive definitions. But the auto-generator has not populated the definitions.

This is likely a generator bug rather than a data gap -- the Maths planners have definitions (written by the teacher persona in V7), so the underlying data exists in a form that could be extracted. For Art-specific terms like "muted palette," "composition," and "perspective," the definitions need to be age-appropriate for Y3-Y4 children. Adding a `vocabulary_definition` property to the concept node or the ArtTopicSuggestion node would solve this cleanly.

### 3. Thinking Lens Integration -- Connect Ontology to Lenses

The ConceptCluster layer has APPLIES_LENS relationships to ThinkingLens nodes, with ranked lenses and rationales. But this planner draws from ArtTopicSuggestion nodes, not ConceptClusters, and the thinking lens integration has not been extended to the per-subject ontology.

For this Lowry study, "Perspective and Interpretation" would be the natural primary lens: "What was the artist trying to show us about industrial Britain? How does your own perspective differ from Lowry's?" The graph already has this lens with age-banded prompts. Connecting ArtTopicSuggestion nodes to ThinkingLens via a new APPLIES_LENS relationship would bring the ontology layer to parity with the cluster layer.

### 4. Technique Teaching Guidance -- Practical Instructions for Non-Specialists

The "techniques" field lists "colour mixing (muted tones), perspective drawing, figure drawing, compositional planning" but provides no teaching instructions. For Maths, the teaching guidance on Concept nodes is detailed and procedural ("Use physical fraction circles, divide into equal groups, count one group"). For Art, the equivalent would be:

- Colour mixing (muted tones): "Start with white. Add a small amount of a colour (raw umber, burnt sienna, Prussian blue). Mix thoroughly. To mute a bright colour, add a small amount of its complementary colour or a touch of grey. Show children that Lowry rarely used pure colour -- his palette was dominated by whites, greys, and muted earth tones."
- Figure drawing: "Study Lowry's figures as a class. Note: they are tall and thin, not stick figures. They have coats, hats, posture. Children should draw figures starting with the overall body shape (an elongated oval), then add limbs and clothing details. Avoid starting with the head."

This level of detail exists for Maths concepts but not for Art techniques. It could be added as a `technique_guidance` property on the ArtTopicSuggestion node or as an expansion of the existing "techniques" field.

### 5. Specific Artwork References -- Which Lowry Paintings to Use

The planner names "L.S. Lowry" as the artist but does not reference any specific paintings. For a 5-lesson study, the teacher needs to know which works to display and discuss. A curated selection might include:

- "Going to the Match" (1953) -- figures in motion, industrial backdrop, community
- "Industrial Landscape" (1955) -- full industrial scene with factories, chimneys, muted palette
- "Coming from the Mill" (1930) -- his most famous composition, foreground figures, background buildings
- "A Street Scene" (1935) -- simpler composition, good for Y3 drawing focus

Adding an `artwork_refs` array property on the ArtTopicSuggestion node (with title, date, and what to focus on pedagogically) would give teachers the visual starting points they need.

---

## What the Auto-Generator Does Well

### 1. Concept Differentiation Tables
The three-level differentiation for Art History (Entry/Developing/Expected) is genuinely useful. The progression from "recall one fact about an artist" to "compare artists from different times and cultures, explaining how context shapes their work" gives clear assessment criteria. This is DifficultyLevel-quality data even though it comes from the per-subject ontology rather than explicit DifficultyLevel nodes.

### 2. Pitfalls
The three pitfalls are specific, practical, and classroom-tested. "Pupils draw figures as stick men rather than Lowry's distinctive elongated forms" is exactly the kind of warning a non-specialist needs. This data comes from the ArtTopicSuggestion node and demonstrates that the per-subject ontology can carry practical teaching intelligence.

### 3. Subject-Specific Metadata
The Art focus section (artist, movement, medium, techniques, visual elements, cultural context) is structured and clear. This is information a primary generalist would otherwise need to research. The per-subject ontology is doing exactly what it was designed to do -- providing typed, subject-specific data rather than a generic blob.

### 4. Cross-Curricular Hooks
The History and Geography connections to Lowry's industrial context are natural and well-identified. The auto-generator is correctly finding cross-curricular links from the ontology data, even if the "Subject: None" rendering needs fixing.

---

## What the Auto-Generator Gets Wrong

### 1. Source Document Error
The planner cites "KS2 English Grammar, Punctuation and Spelling Test Framework 2016" as the source document for an Art and Design planner. This is a join error in the auto-generator. It should reference the KS2 Art and Design Programme of Study from the National Curriculum 2014. This kind of error would seriously undermine teacher trust in the system -- if it cannot even cite the correct source document, why would I trust the content?

### 2. Empty Vocabulary Definitions
A vocabulary word mat with 8 terms and no definitions is worse than no word mat at all. It implies the system knows the important terms but cannot be bothered to define them. Either populate the definitions or do not include the section.

### 3. No Lesson Structure Despite Having Duration
Stating "Estimated duration: 5 lessons" and then providing no lesson-by-lesson structure creates an expectation gap. The planner promises a multi-lesson study but delivers a single-page content briefing. Either remove the duration estimate (and present this as a content guide) or surface a vehicle template that structures the 5 lessons.

### 4. Asymmetric Differentiation
The Art History concept has full differentiation with example tasks, but Drawing Mastery and Painting Mastery only have "what success looks like" and "common errors." For a practical subject where the making IS the learning, this asymmetry is backwards. I need differentiated tasks for Drawing and Painting more than I need them for Art History knowledge.

---

## Comparison: Hand-Written vs Auto-Generated Planner

If I were planning this Lowry unit from scratch (without the auto-generated planner), I would:

1. Start with the National Curriculum statement and identify the key skills and knowledge (30 minutes)
2. Research Lowry -- select 4-5 paintings, note key facts about his life and context (20 minutes)
3. Plan a 5-lesson sequence with clear progression from study to experiment to create (45 minutes)
4. Design differentiated activities for each lesson with clear success criteria (30 minutes)
5. Create a vocabulary list with child-friendly definitions (10 minutes)
6. Source visual resources -- high-quality reproductions, technique demonstration videos (20 minutes)
7. Write cross-curricular links into the History/Geography/English planning (10 minutes)

Total: approximately 2 hours 45 minutes.

With the auto-generated planner, I still need to do steps 2, 3, 4 (partially), 5, and 6. The planner saves me step 1 (curriculum alignment) and partially saves step 7 (cross-curricular links). Time saving: approximately 40 minutes.

Compare this to my V8 Maths experience, where the planner saved approximately 2 hours of the 3-hour planning process. The Art planner saves roughly 25% of my planning time. The Maths planner saves roughly 65%.

---

## Verdict

This planner reveals the maturity gap between the core curriculum layers (where Maths has DifficultyLevels, ThinkingLenses, RepresentationStages, PedagogyProfiles, and InteractionTypes) and the per-subject ontology layer (where Art has artist metadata, techniques lists, and concept differentiation but little pedagogical infrastructure).

The auto-generator is constrained by the data available. For Art, the data is thin. The planner it produces is an honest reflection of that thinness -- useful as a content briefing, insufficient as a teaching plan.

The path to 7-8/10 for Art planners:
1. Surface vehicle templates to provide lesson structure (+1.0)
2. Populate vocabulary definitions (+0.5)
3. Connect thinking lenses to ontology nodes (+0.5)
4. Add technique teaching guidance (+0.5)
5. Add specific artwork references (+0.5)
6. Add success criteria and sensitive content notes (+0.5)

These are achievable additions. Items 1-3 are infrastructure connections (the data already exists elsewhere in the graph -- it just is not being surfaced for ontology-based planners). Items 4-6 require new data authoring on the ArtTopicSuggestion nodes.

The fundamental architecture of the per-subject ontology is sound. The typed nodes (ArtTopicSuggestion with artist, movement, medium, techniques) carry the right kind of subject-specific information. The gap is in the pedagogical layers that sit on top of that information -- lesson structure, assessment, differentiation of practical skills, and vocabulary support.
