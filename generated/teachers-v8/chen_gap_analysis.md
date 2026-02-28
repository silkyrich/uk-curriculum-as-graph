# Gap Analysis: Ms. Chen -- Science (KS1)
**Planner:** Which Material Is Best?
**Date:** February 2026 (V8 review)
**V7 score:** 6.0/10 --> **V8 score:** 7.5/10

---

## Top 5 Data Additions That Would Improve This Planner

1. **Add cross-curricular links for KS1.** The planner provides only one cross-curricular link (DT: Moving Pictures). For KS1 teaching, where the curriculum is thematic and cross-curricular planning is the norm, this is a significant gap. At minimum, the ScienceEnquiry node should link to: English (non-fiction writing about materials; "The Three Little Pigs" as a text link for material suitability), Maths (sorting and classifying by property, a core Y1 maths skill), and Art (collage using different textures/materials). These are standard KS1 cross-curricular connections that any materials unit would include.

2. **Populate vocabulary definitions.** Eight terms are listed with empty definitions. For KS1, vocabulary definitions need to be especially child-friendly: "waterproof" should be defined as "does not let water through" rather than a technical definition. The concept descriptions contain usable definitions embedded in their text (e.g., "waterproof/not waterproof, absorbent/not absorbent" from the Material Properties concept) -- the generator should extract these into the word mat. Additionally, the word mat is missing several essential KS1 terms: "object", "made from", and the paired property descriptors (hard/soft, rough/smooth, shiny/dull) that are explicitly listed in the Material Properties concept.

3. **Include a unit-level structure, not just an investigation plan.** The planner covers 5 concepts but is framed as a 2-lesson investigation. In practice, a KS1 materials unit is 6-8 lessons: naming materials, describing properties, sorting and classifying, then the investigation. The planner should indicate where the waterproofing test sits within the wider unit. A minimal skeleton -- "Lessons 1-2: naming and handling materials (concepts C024, C025), Lessons 3-4: describing and comparing properties (C026), Lessons 5-6: Which material is best? investigation (C002, C003)" -- would transform this from an investigation plan into a unit plan.

4. **Add KS2 progression links.** The planner has no sequencing section. For KS1 teachers, knowing that "Material Properties is a prerequisite for Y3 Light and Shadows" and "Simple Testing leads to Y5 Fair Testing" provides a powerful reason to teach the concepts thoroughly. This data exists in the graph (PREREQUISITE_OF relationships from KS1 to KS2 concepts) -- the generator simply needs to surface it. A single line like "This lays the foundation for: Y3 Light and Shadows (opaque/transparent), Y2 Uses of Everyday Materials, Y5 Properties of Materials" would add significant value.

5. **Add a "children's language" section or adapt the enquiry type description.** The Fair Test definition reads: "A controlled investigation where one variable is deliberately changed while all others are kept the same, to determine whether the changed variable has an effect on a measured outcome." This is teacher-level language that is inappropriate for KS1. The planner should include a KS1 reframing: "We change one thing and keep everything else the same, to find out if the thing we changed makes a difference." The EnquiryType node could store age-banded descriptions, or the generator could pull the ContentGuideline for Y1/Y2 and adjust reading level accordingly.

---

## What the Auto-Generator Does Well

**KS1-appropriate concept descriptions.** The Object vs Material Distinction concept is described in language that a non-specialist teacher could understand and act on. The teaching routine ("Use a 'what is it made of?' routine when handling objects. Deliberately choose objects made from one obvious material first, then introduce objects made from multiple materials") is practical, sequenced, and grounded in how KS1 classrooms work. This is not dumbed-down KS2 content -- it reads as genuinely KS1-authored.

**Differentiation tables calibrated for 5-7 year olds.** The Entry level for Object vs Material reads: "Beginning to distinguish between what an object is and what it is made from, when prompted by the teacher." The example task asks a child to identify the object and material of a wooden spoon -- a concrete, sensory task with a familiar object. The common error ("Answering 'spoon' for both questions") is the exact response Y1 children give. Across all five concepts, the differentiation tables maintain this age-appropriate calibration. The Greater Depth descriptors push genuine reasoning ("Explaining that the same material can be used to make many different objects, and the same object can be made from different materials") without requiring abstract thinking beyond KS1 capacity. Getting KS1 differentiation right is harder than KS2 because the cognitive gap between Entry and Greater Depth is narrower -- the tables navigate this well.

**Equipment list is child-safe and practical.** The inclusion of specific material samples (fabric, plastic bag, foil, paper, card, cling film) covers the range needed for a comparative investigation. The safety note about not using glass for the waterproof test shows awareness of the KS1 classroom environment. The water spray bottle option (rather than just "pour water") gives teachers a controlled-delivery method that reduces flooding -- a practical detail that matters enormously with 5-6 year olds.

**Pitfalls are KS1-specific and actionable.** "Children pour different amounts of water on each material" is the #1 KS1 fair testing error. "Recording is verbal only and not captured -- provide a simple table with material names pre-printed" addresses a real KS1 challenge: children can observe and discuss but struggle to record. The solution (pre-printed table with names, tick/draw format) is standard KS1 practice and shows the data author understands the recording capabilities of this age group.

---

## What the Auto-Generator Gets Wrong

**Source document mismatch.** The SourceDocument field reads "Art and Design (KS1/KS2) - National Curriculum Programme of Study" for a Science planner. This is a data join error -- the generator is pulling the wrong source document, possibly because the Subject node links to multiple SourceDocument nodes and the query is not filtering by subject.

**Enquiry type language is not age-adapted.** The Fair Test definition uses "variable", "deliberately changed", "measured outcome" -- vocabulary that Y1/2 children would not understand and that many KS1 teachers would not use. The planner applies the same definition text regardless of key stage. For KS1, the concept should be expressed as keeping things the same and changing one thing, not as "controlling variables."

**Only one cross-curricular link.** KS1 teaching is inherently cross-curricular. A single DT link is inadequate. The planner format appears to surface whatever CROSS_CURRICULAR relationships exist on the ScienceEnquiry node, but the node itself has insufficient links. This is a data coverage issue rather than a generator issue.

**No sequencing context.** No follows/leads-to information. The planner does not indicate that this investigation should follow naming and handling materials lessons, or that it connects forward to Y2 "Uses of everyday materials" and eventually to KS2 materials science. This progression context is stored in the graph via PREREQUISITE_OF but not rendered.

**Subject field empty on cross-curricular link.** The one link shows "None" for Subject. Same rendering bug as all planners.

**Vocabulary word mat is incomplete and empty.** Beyond the empty definitions, the word mat is missing core KS1 materials vocabulary: "object", "made from", and the paired property descriptors from the NC specification. The concept description explicitly lists these (hard/soft, stretchy/stiff, shiny/dull, rough/smooth, bendy/not bendy) but they are not in the word mat.

---

## Comparison: Hand-Written vs Auto-Generated Planner

A hand-written KS1 materials unit plan would differ substantially in several ways:

**Thematic integration.** A KS1 teacher would plan the materials unit around a theme or story. "The Three Little Pigs" is the classic vehicle: straw, sticks, and bricks as materials with different properties, and the wolf's huffing and puffing as a "test" of material strength. This thematic framing makes the science memorable and meaningful for 5-6 year olds. The auto-planner provides curriculum content without narrative context.

**Sensory exploration structure.** A human planner would front-load the unit with structured sensory exploration: feely bags, material hunts around the classroom, sorting hoops on the carpet. The auto-planner jumps to the investigation without establishing the exploratory phase that KS1 children need. The concept descriptions hint at this ("Classroom hunts where pupils label each object and its material(s)") but the planner does not structure it as a lesson.

**Recording scaffolds.** A human planner would include photocopiable recording templates: a sorting grid with material images, a prediction sheet with tick boxes, a results table with smiley/sad face columns for "kept teddy dry/did not keep teddy dry." The auto-planner mentions "simple tables, verbal descriptions" but provides no template or structure.

**Display and celebration.** A KS1 teacher would plan a class display: "Our Materials Investigation" with photographs, children's sorting work, and the results. The auto-planner does not reference display, class books, or sharing outcomes -- all of which are standard KS1 practice.

**What the auto-planner does better than most human planners:** The concept-level detail is superior. Most school-level KS1 plans say "children learn about materials and their properties" without specifying the object/material distinction, the full range of paired descriptors, or the progression from naming to describing to testing. The auto-planner provides curriculum depth that many KS1 teachers would not articulate in their own planning. The differentiation tables are more rigorous than typical KS1 differentiation (which is often "some children may need support / some children may be challenged") and give a genuine four-tier assessment framework.

---

## Verdict

This is a well-structured planner for a KS1 materials investigation with strong concept descriptions, age-appropriate differentiation, and practical equipment guidance. It would be immediately useful to a KS1 teacher as the investigation component of a wider materials unit -- saving approximately 30 minutes of planning for the test itself and providing differentiation data that would normally take an hour to construct.

The gap to "unit plan" quality is mainly in scope and pedagogy: the planner covers the investigation but not the broader unit (naming, sorting, handling materials); it provides teacher-facing content but not child-facing resources; and it lacks the thematic and cross-curricular integration that defines KS1 teaching. These are addressable gaps -- a unit-level structure, more cross-curricular links, and KS1-adapted vocabulary would close most of them.

Among the three V8 planners reviewed by our group, this one has the strongest KS1 calibration. The concept descriptions, misconceptions, and differentiation tables read as though they were written by someone who teaches Reception or Y1. For a system that was originally designed around KS2 clusters, this level of KS1 quality is a notable achievement.
