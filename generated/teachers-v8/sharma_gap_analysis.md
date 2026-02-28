# Gap Analysis: Mr. Sharma -- Design and Technology KS2 (Bridges: Beam, Arch and Truss)

**Planner:** Bridges: Beam, Arch and Truss
**Date:** February 2026 (V8 review)
**V7 score:** 6.0/10 (Y5 Maths Prime/Composite cluster) -> **V8 score:** 6.5/10

---

## Top 5 Data Additions That Would Improve This Planner

### 1. Structural Engineering Content -- Explain Beam, Arch, and Truss

The planner names three bridge types as the central design choice but does not explain what they are, how they work, or why one might be stronger than another. This is the core subject knowledge of the unit and it is entirely absent.

What is needed on the DTTopicSuggestion node (or a linked reference node):

```
beam_bridge:
  description: "A flat horizontal deck resting on two supports (piers). The simplest
    bridge form. The deck bends under load -- the top surface is compressed and the
    bottom surface is in tension."
  strengths: "Simple to build. Uses minimal material. Easy to understand."
  weaknesses: "Cannot span long distances without sagging. Bending increases with
    span length."
  classroom_model: "A piece of card laid across a 30cm gap. Observe how it sags
    when weight is added to the centre."

arch_bridge:
  description: "A curved structure that transfers load sideways into supports
    (abutments). The arch converts downward force into outward thrust."
  strengths: "Very strong for its weight. Can span longer distances than beam."
  weaknesses: "Needs strong abutments. More complex to construct."
  classroom_model: "Cut a card strip, bend into an arch shape between two book
    stacks. Note: the arch pushes the books apart -- this is why abutments matter."

truss_bridge:
  description: "A framework of triangles. Triangulation makes the structure rigid
    because a triangle cannot deform without changing the length of a side."
  strengths: "Very strong and lightweight. Distributes forces across the whole
    structure."
  weaknesses: "Complex to build. Requires many joints, and joints are failure points."
  classroom_model: "Build a square from 4 lollipop sticks and tape. Push the corner
    -- it deforms. Now add a diagonal brace -- it cannot deform. This is why
    triangles are the strongest shape in engineering."
```

This kind of subject knowledge content exists for Science enquiries (variables, misconceptions) and History studies (primary sources, disciplinary concepts). It does not exist for DT structures. Adding it would make the planner teachable by a non-specialist.

### 2. Vehicle Template Integration -- Investigate-Design-Make-Evaluate Cycle

DT has a statutory process cycle: investigate, design, make, evaluate. Every DT unit should be structured around this cycle. The graph's VehicleTemplate nodes should include a DT-specific template that provides this structure with age-banded guidance.

For a Y5-Y6 structures unit, the template would look like:

- **Investigate (Lesson 1):** Examine real bridge images and simple models. Test beam, arch, and truss structures using card and weights. Record which type holds the most weight.
- **Design (Lesson 2):** Draw annotated designs showing chosen bridge type, dimensions, materials, and construction sequence. Justify choice based on investigation findings.
- **Make (Lessons 3-4):** Build the bridge. Focus on accurate measuring, cutting, and joining. Test joints before completing the full structure.
- **Evaluate (Lesson 5):** Load test all bridges. Record maximum weight held. Identify failure points. Compare results across design types.
- **Communicate (Lesson 6):** Present findings. Evaluate design against original brief. Suggest improvements.

This template already exists conceptually in the VehicleTemplate schema. It needs populating for DT structures specifically.

### 3. Mathematics Cross-Curricular Links -- The Most Natural Connection

Bridge building is inherently mathematical. The planner identifies History and Science cross-curricular links but misses Mathematics entirely. This needs explicit cross-curricular relationship data:

| DT Concept | Maths Connection | Maths Concept |
|---|---|---|
| Measuring and cutting to length | Y5 Convert between metric units | MA-Y5-C030 or equivalent |
| Recording test results | Y5 Statistics -- interpret tables and line graphs | MA-Y5-D006 concepts |
| Comparing bridge performance | Y5 Calculating differences, comparing measures | MA-Y5 addition/subtraction |
| Scale and proportion (model vs real) | Y5 Multiplication and division, scaling | MA-Y5-D003 concepts |

These should be CROSS_CURRICULAR relationships on the DTTopicSuggestion node, similar to how HistoryStudy nodes have CROSS_CURRICULAR links to ScienceEnquiry nodes. The DT-to-Maths connection is at least as strong as the History-to-Geography connections already encoded.

### 4. Vocabulary Definitions -- Populate the Empty Word Mat

Ten well-chosen terms with no definitions. The definitions are essential for DT because the vocabulary is technical and many primary teachers cannot define "compression," "tension," or "triangulation" correctly from memory.

For DT structures specifically, the definitions need to be concrete and visual:

| Term | Child-friendly definition |
|---|---|
| beam | A horizontal structure that rests on supports at each end, like a plank across a gap |
| arch | A curved structure that pushes weight sideways and downwards into its supports |
| truss | A framework built from triangles, making it very strong and rigid |
| span | The distance a bridge covers from one support to the other |
| load | The weight or force placed on a structure |
| compression | A pushing or squashing force -- when something is being pressed together |
| tension | A pulling or stretching force -- when something is being pulled apart |
| reinforce | To make a structure stronger by adding extra material or supports |
| brace | A diagonal support that stops a structure from twisting or collapsing |
| triangulation | Using triangles in a framework to make it rigid -- triangles cannot change shape without breaking |

These could be added as a `vocabulary_definitions` property on the DTTopicSuggestion node or generated from the concept `key_vocabulary` with an associated definition field.

### 5. Technique Demonstration Instructions -- How to Build, Not Just What to Build

The planner lists techniques (triangulation, laminating for strength, arch construction, joint reinforcement, load testing) but does not explain how to do them. For a non-specialist primary teacher, this is the critical gap. Knowing that triangulation is a technique is useless without knowing how to demonstrate it.

What is needed, either as expanded technique guidance or as a linked resource:

**Triangulation:** "Take 4 lollipop sticks and make a square frame with tape at each corner. Push one corner -- the square collapses into a parallelogram. Now add one diagonal stick across the square. Push again -- it holds firm. That diagonal turned the square into two triangles. This is triangulation. In a truss bridge, every section is made of triangles for this reason."

**Laminating for strength:** "Take one piece of card and bend it -- it flexes easily. Now glue three pieces of card together and let them dry. The laminated card is much harder to bend. This is how plywood works. Use laminating to make bridge decks stiffer."

**Joint reinforcement:** "The joint is the weakest point. Demonstrate: tape two sticks together at a right angle. It's wobbly. Now add a triangular gusset (a small card triangle) across the inside of the joint. It's rigid. Gussets reinforce joints."

This kind of procedural teaching guidance exists for Maths concepts (step-by-step calculation methods) and Science enquiries (how to set up fair tests). DT needs the equivalent for making techniques.

---

## What the Auto-Generator Does Well

### 1. Design Brief Quality
The design brief is the standout feature of this planner. "Design and build a bridge to span a 30cm gap between two tables. The bridge must hold the maximum possible weight. You may choose beam, arch, or truss design -- but must justify your choice." This is a well-constrained, testable, and educationally rich brief. It gives children genuine design freedom (choice of bridge type) within clear constraints (30cm span, weight test). The justification requirement elevates it from craft to engineering.

### 2. Materials and Safety
The materials list (card strips, lollipop sticks, straws, string, tape, PVA glue) is realistic, affordable, and specific. The safety notes about glue guns and gradual weight loading are practical. This is immediately useful information that saves a teacher from having to figure out what materials to order.

### 3. Primary Concept Differentiation
The Accurate Making differentiation table is strong. The progression from "measuring and cutting to a marked line" (Entry) through "measuring, marking, and cutting across different materials" (Developing) to "working with precision, selecting appropriate tools, explaining how accuracy affects quality" (Expected) is a clear skill progression with practical assessment criteria.

### 4. Pitfalls
All three pitfalls are specific and immediately actionable. "Joints as the failure point, not the structure" is the single most important teaching point for a structures unit and it is correctly identified as a pitfall rather than buried in the concept description.

### 5. Evaluation Criteria
The four evaluation criteria provide a clear assessment framework: span coverage, weight capacity, design justification, and joint quality. These could be directly converted into a peer assessment sheet.

---

## What the Auto-Generator Gets Wrong

### 1. Source Document Error
"KS2 English Grammar, Punctuation and Spelling Test Framework 2016" cited as the source for a DT planner. This is the same systematic bug reported in the Art planner review. It must be fixed at the generator level -- it appears across multiple subjects.

### 2. Missing Core Subject Knowledge
The planner assumes the teacher already understands beam, arch, and truss bridges. A DT structures unit where the teacher cannot explain how an arch transfers load is not a successful unit. This is not a minor gap -- it is the absence of the subject matter itself.

### 3. No Lesson Structure for a Process-Based Subject
DT is explicitly structured around investigate-design-make-evaluate. This is statutory. A planner that provides 6 lessons of content with no process structure is missing the fundamental pedagogical framework of the subject.

### 4. Missing the Strongest Cross-Curricular Link
Not identifying Mathematics as a cross-curricular opportunity for a bridge-building unit is a significant oversight. The History link (Brunel/Telford) is valid but secondary. The Science link (forces) is valid and important. The Maths link (measurement, data, proportion) is the most naturally integrated and the most immediately useful for a classroom teacher, and it is absent.

---

## Comparison: Hand-Written vs Auto-Generated Planner

Planning this unit from scratch (no planner):
1. Research bridge types and structural principles (30 minutes -- I am a Maths teacher, not an engineer)
2. Design the investigation-design-make-evaluate sequence (30 minutes)
3. Source and test materials -- actually build the three bridge types myself to check they work (60 minutes)
4. Write differentiated design briefs and success criteria (20 minutes)
5. Create vocabulary resources and safety documentation (15 minutes)
6. Plan Maths integration points -- measurement skills, data recording, proportional reasoning (20 minutes)
7. Write assessment approach (10 minutes)

Total: approximately 3 hours 5 minutes.

With the auto-generated planner, I save the materials research (step 3 partially -- the list is given, but I would still build test models), the design brief writing (step 4 partially), and the safety documentation (step 5 partially). I still need to do the subject knowledge research (step 1), the lesson sequencing (step 2), the Maths integration (step 6), and the assessment design (step 7).

Time saving: approximately 45-60 minutes. The planner reduces my preparation from 3 hours to about 2 hours.

Compare this to the Maths graph experience. In V7, the Maths cluster planner gave me statutory objectives, prerequisite chains, misconceptions, vocabulary, pedagogy techniques, thinking lenses, cross-domain links, and assessment codes. It saved about 60-75% of planning time for the intellectual work (but not the artefact creation). This DT planner saves about 30-35% of planning time. The DT planner is more useful for the practical/logistical aspects (materials, safety) but weaker for the pedagogical aspects (lesson structure, differentiation breadth, assessment).

---

## Verdict

This planner demonstrates that the per-subject ontology can carry genuinely useful subject-specific content. The design brief, materials list, safety notes, and evaluation criteria are practical, accurate, and immediately usable -- something the generic ConceptCluster approach could not provide for DT.

However, the planner also exposes what happens when the ontology carries subject metadata without the pedagogical infrastructure. There are no thinking lenses, no lesson structure, no vehicle template, no vocabulary definitions, and no explanation of the core subject knowledge (structural engineering principles). The planner gives a teacher everything needed to set up the making activity but not everything needed to teach the unit.

The score of 6.5/10 reflects a planner that is more practically useful than my V7 Maths experience (6.0/10) -- the design brief and materials data are directly actionable -- but less pedagogically complete than the V8 Maths planners Brennan reviewed (8.5/10) where DifficultyLevels, RepresentationStages, and ThinkingLenses provided a full teaching framework.

The path forward for DT planners:
1. Add structural engineering content to DTTopicSuggestion nodes (+1.0)
2. Surface vehicle templates for the DT process cycle (+1.0)
3. Populate vocabulary definitions (+0.5)
4. Add Mathematics cross-curricular relationships (+0.5)
5. Connect thinking lenses to ontology nodes (+0.5)

These additions would take this planner from 6.5/10 to approximately 9.0/10. The foundation is solid -- the design brief, materials, and safety content demonstrate that the per-subject ontology is the right architecture. It just needs the subject knowledge depth and pedagogical layers added on top.
