# V6 Teacher Review — Year 5 Evaluation
## Ms Sarah Brennan, Year 5 Class Teacher (11 years' experience)

**Central question:** If an AI — Claude — had ONLY this graph data, could it sit with a Year 5 child and actually TEACH them?

**Date:** 2026-02-23
**Context file reviewed:** `generated/teachers-v5/y5/context.md` (5,939 lines)

---

## 1. Subject-by-Subject Evaluation

### Rating Scale
1-3: Claude would struggle significantly; data insufficient for meaningful teaching
4-6: Claude could partially teach; significant gaps remain
7-8: Claude could teach competently with minor gaps
9-10: Claude could teach as well as or better than a typical classroom interaction

### English (7 domains, ~37 concepts)

| Dimension | Rating | Evidence |
|---|---|---|
| **MODEL** | 8/10 | Excellent concept descriptions with step-by-step teaching guidance. Writing Composition includes explicit planning→drafting→editing→evaluating sequences. VGP concepts describe grammatical rules with worked reasoning (e.g., relative clauses, modal verbs). Reading Comprehension concepts include specific inference and retrieval strategies. The ConceptCluster sequencing (introduction→practice) gives Claude a natural pedagogical arc. |
| **SCAFFOLD** | 7/10 | Prerequisite chains are well mapped (Y4→Y5 Reading Comprehension, Y3→Y5 Spelling patterns). Complexity ratings differentiate concepts. CO_TEACHES relationships help Claude connect within-domain concepts. However, **no difficulty sub-levels within a concept** — Claude knows "modal verbs" is complexity 2, but not the difference between "might" (easy) and "should have been able to" (hard). The Learner Profile's 3-tier hint system is useful but generic. |
| **HAND OVER** | 7/10 | Assessment content domain codes (8 reading skills, RS-KS2-2a through 2h) give Claude clear success indicators. Success criteria on Content Vehicles (text_study type) define what mastery looks like. Mastery threshold (5/7 in 7 days, 80%) provides a numerical handover signal. Missing: **no rubric or exemplar responses** showing what a "good enough" answer looks like at Y5 level. |
| **RESPOND** | 8/10 | Common misconceptions are rich and specific. Example from VGP: "pupils may overuse commas where a full stop or semicolon would be more appropriate." Spelling misconceptions address specific error patterns (homophones, unstressed vowels). The Feedback Profile gives Claude concrete post-error scripts. Reading comprehension misconceptions distinguish between retrieval and inference errors. |
| **CONNECT** | 9/10 | CO_TEACHES relationships link Spelling↔Reading, VGP↔Composition, Reading↔Writing naturally. Cross-subject links exist via epistemic ReadingSkill skills (8 skills woven through all teaching). ThinkingLens connections (Patterns for Spelling, Structure & Function for VGP) give Claude cross-subject cognitive frames. The 4 Content Vehicles (EN-Y4-CV001 through CV004: Adventure Narrative, Persuasive Writing, Information Text, Poetry Anthology) bridge reading and writing through specific text types. |
| **OVERALL** | **7.8/10** | English is the strongest subject in the graph for Y5 teaching. The combination of fine-grained concept descriptions, rich misconception data, 8 assessment content domain codes, 4 Content Vehicles, and extensive prerequisite chains gives Claude a solid foundation. The main gap is the absence of actual text passages, model answers, and difficulty gradients within concepts. |

### Mathematics (8 domains, ~17 concepts)

| Dimension | Rating | Evidence |
|---|---|---|
| **MODEL** | 6/10 | Teaching guidance explains procedures (e.g., "formal written method of long multiplication"), but **no actual worked examples** despite `worked_example_set` being a vehicle type. The description says "Bus Stop Division" and "Place Value with Dienes" exist as concepts, but the graph contains no step-by-step numerical walkthroughs. Claude would have to generate these from concept descriptions alone. ConceptClusters sequence introduction→practice correctly (e.g., Fractions introduction before Fractions/Decimals/Percentages practice). |
| **SCAFFOLD** | 6/10 | Prerequisite chains are clear (Y4 Multiplication→Y5 Multiplication). The InteractionTypes include excellent maths-specific tools: Place Value Blocks (Dienes), Fraction Visualiser (bar/pizza/set model), Area Model for multiplication, Column Subtraction with exchange, Number Line. These give Claude concrete manipulative-based scaffolding. However, **no difficulty sub-levels**: Claude cannot distinguish "multiply 2-digit by 1-digit" from "multiply 4-digit by 2-digit" within the same concept. |
| **HAND OVER** | 5/10 | Assessment content domain codes exist but are less granular than English. Mastery threshold (5/7 in 80%) is defined but abstract — there's no item bank or question types specified. Success criteria on Maths Content Vehicles would help enormously but only 2 vehicles exist (worked_example_set type). **Critical gap: no actual assessment items or difficulty-calibrated questions.** |
| **RESPOND** | 7/10 | Common misconceptions are excellent and specific. Examples: "pupils may assume that multiplying always makes numbers bigger" (Fractions), "children may misalign digits when using column addition with numbers of different lengths" (Addition/Subtraction), "pupils may confuse area and perimeter" (Measurement). Claude could use these to diagnose specific errors. The post-error feedback script in the Learner Profile is maths-specific: "You got 7x8=54, but the correct answer is 56. If you know 7x7=49, then 7 more gives 56." |
| **CONNECT** | 7/10 | CO_TEACHES relationships connect Fractions↔Decimals↔Percentages, Addition↔Subtraction, Multiplication↔Division. Cross-domain curated links connect Maths↔Science (measurement in investigations), Maths↔Geography (scale on maps). Mathematical Reasoning epistemic skills (6 skills) are woven through teaching. ThinkingLens "Scale, Proportion and Quantity" frames much of Y5 maths naturally. |
| **OVERALL** | **6.2/10** | Maths is the most significant gap for Y5. The graph has excellent structural data (prerequisites, clusters, misconceptions, interaction types) but **lacks the worked examples and graded problem sets** that are the bread-and-butter of maths teaching. Claude knows WHAT to teach (long multiplication) and WHY children struggle (misaligned digits) but doesn't have the HOW (step-by-step numerical demonstrations with specific numbers). The Learner Profile's productive failure sequence ("start with challenge problem, then worked example") is pedagogically sound but requires Claude to generate all mathematical content from descriptions. |

### Science (14 domains, ~68 concepts)

| Dimension | Rating | Evidence |
|---|---|---|
| **MODEL** | 7/10 | Science concepts have detailed descriptions with explicit teaching guidance. Working Scientifically concepts describe enquiry types (fair test, pattern seeking, classification) with procedural steps. Content Vehicle investigations (SC-KS2-CV001 through ~CV010) include enquiry_type, variables, equipment, and expected_outcome — giving Claude structured investigation scripts. The distinction between "observational studies" and "fair tests" is clearly drawn. However, concepts describe phenomena qualitatively ("forces act on objects") rather than providing quantitative examples. |
| **SCAFFOLD** | 7/10 | Prerequisite chains within Science are strong: Y3 Light→Y5 Light (shadows), Y3 Forces→Y5 Forces (gravity, air resistance, friction). The Content Vehicle investigation structure (independent→dependent→controlled variables) provides built-in scaffolding. The Learner Profile's productive failure approach ("introduce challenge problem first") maps well to scientific enquiry. Equipment lists in investigations help Claude plan practical scaffolding. |
| **HAND OVER** | 6/10 | Content Vehicle success_criteria define what understanding looks like (e.g., "explain why objects fall towards Earth", "plan a fair test identifying variables"). Working Scientifically skills give Claude 8 distinct assessment dimensions. However, **no actual assessment questions or expected written responses** at Y5 level. Claude knows the child should "use evidence to support or refute ideas" but not what a good Y5 evidence paragraph looks like. |
| **RESPOND** | 8/10 | Misconception data is outstanding. Examples: "pupils may think heavier objects fall faster" (Forces), "pupils may think sound can travel through a vacuum" (Sound), "pupils may believe a shadow is a physical object" (Light), "pupils often confuse dissolving with melting" (Materials). These are precisely the errors Y5 children make. Content Vehicles include perspectives and source_types for History-of-science connections. The 34 concept→WorkingScientifically skill links mean Claude can trace exactly which enquiry skill a child is struggling with. |
| **CONNECT** | 8/10 | Science has the richest cross-layer connections. CO_TEACHES links connect Materials↔Chemistry, Forces↔Maths (measurement), Living Things↔Geography (habitats). Cross-subject concept skill links (34 Science→WS, 18 Geography→GS, 18 History→HT) are explicit. ThinkingLens assignments are well-chosen: Cause & Effect for Forces, Systems for Living Things, Evidence & Argument for Working Scientifically. Content Vehicles bridge multiple concepts (e.g., SC-KS2-CV005 delivers both Forces concepts and WS enquiry skills). |
| **OVERALL** | **7.2/10** | Science is strong, especially for conceptual teaching and misconception diagnosis. The Content Vehicles with their investigation structure (variables, equipment, expected outcomes) give Claude something close to lesson scripts. The main weakness is the absence of model written responses and the qualitative rather than quantitative nature of concept descriptions. A child asking "what number should I get?" during an investigation would find the graph's "expected_outcome" field helpful but insufficiently precise. |

### History (3 domains, ~5 concepts + 12 Content Vehicles)

| Dimension | Rating | Evidence |
|---|---|---|
| **MODEL** | 7/10 | Content Vehicles are the standout feature. 12 History vehicles (topic_study type) include sources, source_types, key_figures, key_events, perspectives, and period data. Claude can narrate Roman Britain using named sources and multiple perspectives. The Historical Thinking epistemic skills (18 concept links) give Claude disciplinary modelling tools: "use sources as evidence", "consider multiple perspectives", "construct historical narratives." |
| **SCAFFOLD** | 6/10 | Prerequisite chains exist (KS1 History→KS2 History) but within Y5, the progression between vehicles is less clear. Content Vehicles have success_criteria but no explicit difficulty gradient — the Roman Britain vehicle doesn't indicate which sources are easier or harder to interpret. ThinkingLens "Continuity and Change Over Time" provides a consistent cognitive scaffold across all History clusters. |
| **HAND OVER** | 6/10 | Success criteria on Content Vehicles define mastery (e.g., "explain how the Roman Empire influenced Britain using at least two types of evidence"). Assessment_guidance describes how to test understanding. However, **no model historical writing at Y5 level** — Claude doesn't know what a "good" Y5 history paragraph looks like in terms of length, vocabulary, or evidential reasoning. |
| **RESPOND** | 7/10 | Misconceptions are well-targeted: "pupils may view historical periods as static rather than dynamic", "pupils may conflate primary and secondary sources." Perspectives data on Content Vehicles enables Claude to respond when a child presents a one-sided view: "You've told me about the Roman perspective — what might the Britons have thought?" |
| **CONNECT** | 8/10 | History connects strongly to Geography (place knowledge), English (reading comprehension with historical texts), and Science (evidence-based reasoning). ThinkingLens "Perspective and Interpretation" is shared with English reading comprehension. Content Vehicle definitions provide cross-curricular vocabulary links. The 18 concept→HistoricalThinking skill links are explicit. |
| **OVERALL** | **6.8/10** | History benefits enormously from Content Vehicles — they transform the graph from abstract concepts to teachable content bundles. The 12 vehicles with their sources, perspectives, and success criteria give Claude rich material to work with. The gap is in the absence of age-appropriate model responses and difficulty gradients within sources. |

### Geography (4 domains, ~6 concepts + case study vehicles)

| Dimension | Rating | Evidence |
|---|---|---|
| **MODEL** | 6/10 | Concepts describe geographical knowledge clearly (locational knowledge, physical features, human geography), and the 6 prescribed topics give Claude structured content areas. The Geographical Skills concepts (OS maps, grid references, fieldwork) include procedural steps. However, Geography has fewer Content Vehicles than History and Science, meaning less ready-to-teach material. |
| **SCAFFOLD** | 5/10 | The KS1→KS2 prerequisite chain exists but is sparse. Within KS2, the progression from atlas use to OS map skills to fieldwork is implicit in the cluster sequencing but not granularly scaffolded. **~40% of statutory Geography content is not yet covered by Content Vehicles** (a finding from V5 review, confirmed by reading the data). |
| **HAND OVER** | 5/10 | Success criteria exist on available vehicles but coverage is incomplete. Geographical skills have clear benchmarks (4-figure grid references→6-figure grid references) but no assessment items. Fieldwork objectives are difficult for an AI tutor to assess without physical context. |
| **RESPOND** | 6/10 | Misconceptions exist but are less specific than Science or Maths. Example: "pupils may not understand the difference between weather and climate." The 18 concept→GeographicalSkill links help Claude identify which skill is weak. |
| **CONNECT** | 7/10 | Geography connects to Science (water cycle, habitats), Maths (scale, measurement), History (place knowledge in historical context). ThinkingLens "Scale, Proportion and Quantity" for map skills, "Systems and System Models" for human geography are well-chosen. |
| **OVERALL** | **5.8/10** | Geography is the weakest core subject for Y5 teaching readiness. The incomplete vehicle coverage (40% statutory content missing) and sparse scaffolding within concepts limit Claude's ability to deliver comprehensive lessons. The concepts that ARE covered are well-described, but significant curriculum areas have no teaching material beyond bare objectives. |

### Art and Design (3 domains, 6 concepts)

| Dimension | Rating | Evidence |
|---|---|---|
| **MODEL** | 5/10 | Concept descriptions are rich (drawing mastery, painting mastery, sculpture mastery, sketchbooks, art history, creativity). Teaching guidance names specific techniques (hatching, cross-hatching, impasto, glazing) and artists (Monet, Van Gogh, Klimt). However, **Art is fundamentally visual and physical** — Claude cannot demonstrate a pencil hold, show a brush technique, or produce visual exemplars from text descriptions alone. |
| **SCAFFOLD** | 4/10 | Prerequisites exist (KS1 Drawing→KS2 Drawing Mastery), but Art scaffolding requires visual and physical progression that the graph cannot encode. The concept "improve their mastery" implies iterative practice with feedback on physical output — Claude cannot see or evaluate a child's drawing. |
| **HAND OVER** | 4/10 | The only objective is broad: "improve their mastery of art and design techniques." There are no assessment criteria that an AI could evaluate without seeing physical work. Success in Art is inherently visual. |
| **RESPOND** | 5/10 | Misconceptions are well-identified ("pupils may equate drawing mastery with photographic accuracy") but Claude's ability to respond is limited by inability to see the child's work. |
| **CONNECT** | 6/10 | Art History connects well to History (periods, contexts), Design Technology (design communication), and English (descriptive vocabulary). ThinkingLens "Structure and Function" frames technique teaching well. |
| **OVERALL** | **4.8/10** | Art is inherently limited for AI teaching because it requires visual demonstration, physical manipulation, and evaluation of visual output. The graph data is well-structured for what it is, but the medium is wrong — this is not a data quality problem but a fundamental constraint. Claude could teach Art History and critical appreciation reasonably well, but not practical techniques. |

### Music (4 domains, 5 concepts)

| Dimension | Rating | Evidence |
|---|---|---|
| **MODEL** | 4/10 | Concept descriptions cover ensemble performance, improvisation, composition, music history, and staff notation. Teaching guidance is specific (call-and-response structures, graphic notation, aural memory). However, **Music requires sound** — Claude cannot play an instrument, demonstrate a rhythm, or perform a melody. Staff notation teaching guidance says "always connect written symbols to the sounds they represent," which Claude cannot do. |
| **SCAFFOLD** | 4/10 | Prerequisites are clear (KS1 Pulse & Rhythm→KS2 Ensemble Performance), but scaffolding in music requires auditory feedback that the graph cannot provide. |
| **HAND OVER** | 4/10 | Objectives are clear ("play and perform with increasing accuracy, fluency, control and expression") but assessment requires hearing the performance. |
| **RESPOND** | 5/10 | Misconceptions are practical: "pupils often focus only on their own part and do not listen to others." Claude could discuss these conceptually but cannot address them in practice. |
| **CONNECT** | 6/10 | Music History connects to History, Maths (pattern, time signatures), and Languages (songs and rhymes). ThinkingLens "Patterns" frames notation and composition well. |
| **OVERALL** | **4.6/10** | Like Art, Music is fundamentally limited for text-based AI teaching. Claude could teach music theory, notation reading, and music history effectively, but practical performance, ensemble skills, and composition require sound. |

### Design and Technology (5 domains, 13 concepts)

| Dimension | Rating | Evidence |
|---|---|---|
| **MODEL** | 6/10 | Concept descriptions are thorough: research-informed design, technical drawing, accurate making, mechanical systems (gears, pulleys, cams), electrical circuits, computing control, cooking techniques, and seasonality. Teaching guidance is procedural and specific. The progression from design→make→evaluate is explicit. |
| **SCAFFOLD** | 5/10 | Prerequisites chain well (KS1 Mechanisms→KS2 Advanced Mechanisms→Electrical Systems→Computing Control). However, DT requires physical making — cutting, joining, cooking — that Claude cannot scaffold physically. The computing control concept (micro:bit programming) is the one area where Claude could provide real-time interactive scaffolding. |
| **HAND OVER** | 5/10 | Evaluation against design criteria is well-described, but assessment of physical products requires seeing and testing them. |
| **RESPOND** | 6/10 | Misconceptions are practical: "pupils may rush measuring and marking," "pupils may select materials primarily for aesthetics." Claude could address these conceptually. |
| **CONNECT** | 7/10 | DT connects powerfully to Science (circuits, materials), Computing (programming), Maths (measurement, accuracy), and Geography (food miles, seasonality). |
| **OVERALL** | **5.8/10** | DT has a similar limitation to Art and Music — physical making cannot be taught through text. However, the design and evaluation phases, plus computing control, are well-suited to AI teaching. The cooking and nutrition domain could work well as a knowledge-teaching context (nutrition, seasonality, food systems). |

### Computing (2 domains, 4 concepts)

| Dimension | Rating | Evidence |
|---|---|---|
| **MODEL** | 7/10 | Concepts are well-described: algorithms, sequence/selection/repetition, decomposition/computational thinking, and networks/internet. Teaching guidance includes specific strategies (unplugged activities, Scratch to text-based transition, tracing code execution). The keystone concept (Algorithms, CO-KS12-C001) has high fan-out (3), correctly positioning it as foundational. |
| **SCAFFOLD** | 7/10 | The prerequisite chain (Algorithms→Programming→Decomposition) provides clear progression. ConceptCluster sequencing (introduction: algorithms+decomposition → practice: programming with control structures) is pedagogically sound. The Learner Profile's productive failure approach suits programming well — "try the code, see what happens, then learn why." |
| **HAND OVER** | 6/10 | Objectives are clear and assessable in a digital context. Claude could set and evaluate programming challenges (write a program that...). However, no specific assessment items or expected code outputs are provided. |
| **RESPOND** | 7/10 | Misconceptions are excellent: "algorithm is the idea/plan, program is the coded implementation," "a computer does exactly what it is told, not what we intended," "pupils write the same instruction multiple times instead of using a loop." Claude could diagnose and correct these through code review conversations. |
| **CONNECT** | 7/10 | Computing connects to Maths (logical reasoning, patterns), DT (computing control), and Science (data recording, modelling). ThinkingLens "Systems and System Models" frames decomposition well; "Cause and Effect" frames debugging well. |
| **OVERALL** | **6.8/10** | Computing is one of the better-suited subjects for AI teaching — the content is digital, the assessment can be interactive, and Claude can reason about code. The main gap is the absence of ready-made programming challenges and expected solutions. |

### Languages / MFL (4 domains, 8 concepts)

| Dimension | Rating | Evidence |
|---|---|---|
| **MODEL** | 5/10 | Concept descriptions cover phonology, vocabulary, grammar, communicative competence, reading, writing, and language awareness. Teaching guidance is pedagogically strong (echo-repeat, minimal pairs, spaced vocabulary practice, colour-coded gender). However, **the graph is language-agnostic** — it describes "the target language" without specifying French, Spanish, or German. Claude has no vocabulary lists, no specific phoneme inventories, no conjugation tables for any particular language. |
| **SCAFFOLD** | 5/10 | Prerequisites chain logically (Phonology→Communicative Competence, Vocabulary+Grammar→Writing). The progression from recognition→production is implicit. But without specific language content (word lists, phrase banks, grammar tables), scaffolding would be entirely generated by Claude. |
| **HAND OVER** | 4/10 | Objectives are clear ("write phrases from memory," "develop accurate pronunciation") but language-specific assessment requires language-specific content. |
| **RESPOND** | 5/10 | Misconceptions are universal language-learning errors: "applying English pronunciation to target language letters," "translating word-by-word," "not understanding grammatical gender." Useful but generic. |
| **CONNECT** | 7/10 | Language Awareness explicitly connects to English grammar. ThinkingLens "Patterns" frames grammar acquisition well. The concept of cognates creates natural cross-language connections. |
| **OVERALL** | **5.2/10** | Languages is significantly limited by the language-agnostic design. The pedagogical framework is sound, but Claude would need to generate ALL specific language content (vocabulary, grammar tables, pronunciation guides, example sentences) from its own training data rather than from the graph. This is the one subject where the graph provides the HOW but not the WHAT. |

### Physical Education (4 domains, 5 concepts)

| Dimension | Rating | Evidence |
|---|---|---|
| **MODEL** | 3/10 | Concept descriptions cover fundamental movement skills, game tactics, dance, and swimming. Teaching guidance is specific ("use relay and chasing games," "teach floating as distinct from stroke swimming"). But PE is **entirely physical** — Claude cannot demonstrate running technique, correct a throwing action, or lead a dance sequence. |
| **SCAFFOLD** | 3/10 | Prerequisites exist (EYFS Physical Development→KS1 Fundamental Movement) but physical scaffolding requires physical presence. |
| **HAND OVER** | 3/10 | Success in PE requires observing physical performance. Claude cannot assess swimming distance, movement quality, or tactical decision-making in games. |
| **RESPOND** | 4/10 | Misconceptions are relevant ("pupils may believe physical skill is innate rather than developed through practice") and Claude could address growth mindset in physical contexts. |
| **CONNECT** | 5/10 | PE connects to Science (health and fitness, body systems), PSHE (wellbeing), and Maths (scoring, timing). |
| **OVERALL** | **3.6/10** | PE is the least suitable subject for AI teaching. This is not a data quality issue — the graph data is well-structured for curriculum planning. But teaching PE requires physical demonstration, physical correction, and physical assessment. Claude could teach sports science, tactical theory, and health knowledge, but not the practical curriculum. |

---

## 2. Cross-Subject Patterns

### Pattern 1: The Practical/Theoretical Divide
The graph creates a sharp two-tier system of AI-teachability:

**Tier A — Strong AI teaching potential (6.0+/10):**
English (7.8), Science (7.2), Computing (6.8), History (6.8), Maths (6.2)

**Tier B — Fundamentally limited by medium (3.6-5.8):**
Geography (5.8), DT (5.8), Languages (5.2), Art (4.8), Music (4.6), PE (3.6)

The Tier B subjects are limited not by data quality but by the inherent constraints of text-based AI interaction. The graph's data for these subjects is often excellent — the Art concepts have rich teaching guidance, the Music misconceptions are spot-on — but the subjects require sensory modalities (visual, auditory, kinesthetic) that the current platform cannot deliver.

**Recommendation:** For Tier B subjects, position Claude as a **knowledge companion** rather than a primary instructor. Claude can teach Art History but not drawing technique; music theory but not performance; DT design evaluation but not physical making; sports science but not PE practice.

### Pattern 2: Content Vehicles Transform Teaching Readiness
Subjects with Content Vehicles show dramatically higher teaching readiness than those without:

| Subject | Has Vehicles? | Teaching Readiness |
|---|---|---|
| History | Yes (12 vehicles) | 6.8/10 |
| Science | Yes (~10 vehicles) | 7.2/10 |
| English | Yes (4 vehicles) | 7.8/10 |
| Maths | Yes (2 vehicles, thin) | 6.2/10 |
| Geography | Partial (~40% missing) | 5.8/10 |
| Computing | No | 6.8* |
| Art, Music, DT, PE, Languages | No | 3.6-5.8 |

*Computing's higher score despite no vehicles reflects its inherent suitability for AI teaching.

Content Vehicles provide the critical bridge between "what to teach" (concepts) and "how to teach it" (materials, activities, assessment). Without them, Claude has to generate all teaching content from concept descriptions — possible but significantly less reliable.

### Pattern 3: The Misconception Data is Consistently Excellent
Across ALL subjects, the common_misconceptions field is the single most valuable piece of data for AI teaching. These are:
- **Specific** (not generic): "pupils confuse dissolving with melting" not "pupils may struggle with this topic"
- **Actionable**: each misconception implies a specific teaching response
- **Evidence-based**: they reflect real classroom experience
- **Comprehensive**: even Art and Music have useful misconceptions

This is the graph's secret weapon. An AI tutor that can diagnose and address specific misconceptions is more valuable than one that can deliver perfect content. The misconception data turns Claude from a presenter into a responsive teacher.

### Pattern 4: The Learner Profile Provides a Credible Teaching Framework
The Y5 Learner Profile (lines 5856-5939) provides Claude with:
- **Content guidelines**: Flesch-Kincaid grade 2, max 14-word sentences, Lexile 150-350
- **Pedagogy**: productive failure sequence (challenge→attempt→worked example→interleaved retrieval practice)
- **Feedback**: specific competence feedback with error-specific correction scripts
- **Interaction types**: 15 interaction modes (6 primary) including maths-specific manipulatives
- **Pedagogy techniques**: spaced practice (2-7 day intervals) and interleaved practice (new this year at Y3+)

This is a coherent, evidence-based teaching framework. The productive failure sequence (Sinha & Kapur 2021, d=0.36-0.58) combined with interleaving (Bjork 2011, d=0.42) and spacing (Cepeda 2006, d=0.46) represents current best practice in learning science. Claude has clear instructions for session structure, difficulty calibration, feedback tone, and assessment frequency.

**Critical observation:** The Learner Profile is labelled "KS2, from Y3" — it applies to all of Y3-Y6. A Y5-specific profile would be more precise. By Y5, children are more metacognitively capable than Y3 children, yet the profile says "metacognitive prompts: not yet appropriate" and "metacognitive reflection: not yet." This seems conservative for Y5 — many Y5 children can benefit from self-monitoring strategies.

### Pattern 5: ThinkingLens Provides Cognitive Coherence but Needs Age Calibration
The 10 ThinkingLens nodes give Claude a consistent cognitive framing across subjects. The AI instruction prompts are genuinely useful — they provide specific questions Claude can ask ("What caused this?", "What patterns do you notice?", "Whose perspective is this?").

However, the V5 review finding that **Thinking Lens rationales are age-inappropriate for KS1** appears partially relevant for Y5 too. Some lens rationale text is written at adult academic level:
- "Decomposition requires pupils to model a complex problem as a system of smaller interacting parts" — this is a rationale for teachers, not a prompt for children
- The distinction between rationale (for teachers) and AI instruction (for Claude to use with children) is clear in the data, but Claude would need to be careful not to read the rationale TO the child

### Pattern 6: Epistemic Skills Create a Hidden Teaching Strength
The epistemic skills layer (Working Scientifically, Mathematical Reasoning, Reading Skills, Geographical Skills, Historical Thinking, Computational Thinking) provides 31 discipline-specific thinking skills that are explicitly mapped to Y5 concepts. These are labelled "should be woven through all teaching" — meaning Claude has a mandate to integrate them.

This is a genuine teaching advantage. A human teacher might cover "forces" without explicitly connecting to WS-KS2-003 (planning enquiries and controlling variables). Claude, with this data, would always connect content to the disciplinary thinking skill — making the thinking visible in a way that's often implicit in classroom teaching.

---

## 3. The Expressive Framework — Concrete Schema Proposals

### Proposal 1: Worked Example Nodes
**Problem:** Maths, Science, and Computing concepts describe WHAT to teach but not the step-by-step HOW.

```
(:WorkedExample {
  example_id: "MA-Y5-WE001",
  concept_id: "MA-Y5-C004",
  title: "Long multiplication: 2,345 x 67",
  difficulty_level: 3,  // 1-5 within concept
  steps: [
    {step: 1, action: "Partition 67 into 60 and 7", visual: "Place value grid"},
    {step: 2, action: "Multiply 2,345 x 7 = 16,415", visual: "Column method"},
    {step: 3, action: "Multiply 2,345 x 60 = 140,700", visual: "Column method with placeholder zero"},
    {step: 4, action: "Add partial products: 16,415 + 140,700 = 157,115", visual: "Column addition"}
  ],
  common_error_at_step: {2: "Forgetting to carry", 3: "Missing placeholder zero"},
  pupil_input_point: 2,  // "What would you do next?" after step 1
  cpa_stage: "abstract"
})
(:WorkedExample)-[:DEMONSTRATES]->(:Concept)
(:WorkedExample)-[:NEXT_DIFFICULTY]->(:WorkedExample)
```

**Impact:** Would lift Maths MODELLING from 6/10 to 8/10. Each concept could have 3-5 worked examples at escalating difficulty, giving Claude a complete progression to follow.

### Proposal 2: Difficulty Sub-Level Property on Concepts
**Problem:** Concepts have a single complexity rating (1-3) but no internal difficulty gradient.

```
// Add to Concept nodes:
difficulty_sublevels: [
  {level: 1, description: "Multiply 2-digit by 1-digit", example: "34 x 5"},
  {level: 2, description: "Multiply 3-digit by 1-digit", example: "245 x 7"},
  {level: 3, description: "Multiply 2-digit by 2-digit", example: "34 x 56"},
  {level: 4, description: "Multiply 4-digit by 2-digit", example: "2,345 x 67"}
]
```

**Impact:** Would lift SCAFFOLDING scores across all subjects by 1-2 points. Claude could place a child on the difficulty gradient and move them up or down based on performance.

### Proposal 3: Model Response Exemplars
**Problem:** Claude knows what good understanding looks like conceptually but not what good WRITTEN responses look like at Y5 level.

```
(:ModelResponse {
  response_id: "EN-Y5-MR001",
  concept_id: "EN-Y5-C016",  // Reading inference
  question: "Why do you think the character hid the letter?",
  exemplar_response: "I think he hid the letter because the text says 'he glanced nervously at the door' which shows he was worried someone might see it. This suggests the letter contained something he didn't want others to know about.",
  response_level: "expected",  // below_expected, expected, exceeding
  assessment_domain: "RS-KS2-2d",  // inference with textual evidence
  word_count: 42,
  features_demonstrated: ["inference from text", "textual evidence citation", "explanation of reasoning"]
})
(:ModelResponse)-[:EXEMPLIFIES]->(:Concept)
```

**Impact:** Would lift HAND OVER scores across English, Science, and History by 1-2 points. Claude would know not just WHAT a good answer contains but what it LOOKS like at Y5.

---

## 4. Worked Examples — Three Scenarios

### Scenario A: Maths — Long Multiplication (MA-Y5-C004)

**What Claude has from the graph:**
- Concept: "Multiplication and Division" with description mentioning "multiply numbers up to 4 digits by a one or two-digit number using a formal written method, including long multiplication for two-digit numbers"
- Misconceptions: "pupils may misalign digits," "pupils may forget the placeholder zero when multiplying by the tens digit"
- Prerequisite: Y4 Multiplication (short multiplication)
- Cluster: MA-Y5-D003-CL001 (introduction type)
- ThinkingLens: Patterns ("What patterns can I notice?")
- Interaction type: Place Value Blocks, Area Model (Grid/Array)
- Pedagogy: Productive failure first, then worked example
- Feedback: "Specific competence feedback: name the pattern, rule, or skill the child demonstrated"

**What a teaching session might look like:**

CLAUDE: "Here's a problem to have a go at: A school orders 23 boxes of pencils. Each box has 144 pencils. How many pencils is that altogether? Have a go — it's fine to get stuck."

[Child attempts — probably gets lost at the two-digit multiplication stage]

CLAUDE: "You set it up well — you knew it was a multiplication. Let me show you how to tackle 144 x 23 step by step..."

[Claude would need to generate the worked example from the concept description alone — no step-by-step walkthrough exists in the graph]

**What's missing:** The specific step-by-step method. Claude knows the child should use "formal written method, including long multiplication" and that they might "misalign digits" or "forget the placeholder zero" — but the graph doesn't show Claude the actual column layout with specific numbers. Claude must generate this from training data, not graph data.

**Verdict:** Claude can run a credible productive failure sequence but has to improvise the worked example. Reliability depends on Claude's own mathematical knowledge rather than the graph. **Score: 6/10**

### Scenario B: English — Reading Inference (EN-Y5-C016)

**What Claude has from the graph:**
- Concept: "Reading Comprehension — Inference" with detailed description of drawing inferences from text, justifying with textual evidence
- Misconceptions: "pupils may confuse inference with personal opinion," "pupils may not cite textual evidence to support their inferences"
- Assessment domain: RS-KS2-2d (Inference with textual evidence)
- Content Vehicle: EN-Y4-CV001 (Adventure Narrative — text_study) with genre, text_features, suggested_texts, grammar_focus
- Cluster: EN-Y5-D003-CL001 with ThinkingLens "Evidence and Argument"
- Interaction types: Pattern Discovery (I Notice/I Wonder), Text Input, Multiple Choice
- Pedagogy: "Start with a challenge problem — do not explain first"

**What a teaching session might look like:**

CLAUDE: "I'm going to read you a short passage. As you read, press 'I notice...' whenever something catches your attention."

[Passage presented — Claude would need to generate or select this, as the graph doesn't contain actual text passages]

CLAUDE: "Good — you noticed that the character 'kept looking over her shoulder.' What does that tell us about how she's feeling?"

CHILD: "She's scared?"

CLAUDE: "You made an inference — you figured out she's scared even though the text doesn't say 'scared.' The text says she 'kept looking over her shoulder' — that's your evidence. Can you put them together? 'I think she feels scared because...'"

**What's missing:** Actual text passages. The Content Vehicle suggests texts (e.g., adventure narratives) but doesn't contain passages. Claude must generate or select passages from training data.

**Verdict:** Claude can run a sophisticated inference lesson using the assessment domain framework, misconception data, and I Notice/I Wonder interaction type. The main gap is the passage itself. **Score: 7.5/10**

### Scenario C: Science — Forces and Gravity (SC-KS2-C030)

**What Claude has from the graph:**
- Concept: "Forces" with descriptions of gravity, air resistance, water resistance, friction
- Misconceptions: "heavier objects fall faster," "gravity only exists on Earth," "friction always slows things down"
- Content Vehicle: SC-KS2-CV005 (investigation type) with enquiry_type (fair_test), variables (independent: surface type, dependent: distance travelled, controlled: car mass, ramp angle), equipment list, expected_outcome
- Working Scientifically skills: WS-KS2-003 (planning enquiries, controlling variables)
- ThinkingLens: "Cause and Effect" with AI instruction: "prompt pupils to construct 'if... then... because...' explanations"
- Pedagogy: Productive failure first

**What a teaching session might look like:**

CLAUDE: "Here's a puzzle: I drop a feather and a marble at the same time from the same height. Which hits the ground first? What do you think, and why?"

CHILD: "The marble because it's heavier!"

CLAUDE: "That's what a lot of people think. Let me tell you something surprising — if there were no air, they'd hit at exactly the same time. Gravity pulls on everything equally. The feather is slower because of something else — air resistance pushes against it."

[ThinkingLens prompt] "Let's think about cause and effect: IF we removed the air, THEN what would happen? BECAUSE..."

CLAUDE: "Now, the Content Vehicle has an investigation for us. We're going to test how different surfaces affect friction. Here's what we need: a toy car, a ramp, and three different surfaces..."

[Variables from Content Vehicle data]

CLAUDE: "To make it a fair test, what do we need to keep the same? The graph tells me: car mass and ramp angle. What's the one thing we're changing?"

**What's missing:** Very little! The Content Vehicle investigation structure plus the misconception data plus the ThinkingLens prompt gives Claude a nearly complete lesson. The main gap is quantitative data — Claude can't say "you should expect the car to travel about 40cm on carpet and 80cm on smooth floor."

**Verdict:** This is the graph at its best. Content Vehicle + misconceptions + ThinkingLens + Working Scientifically skills + productive failure pedagogy = a coherent, evidence-based science lesson. **Score: 8/10**

---

## 5. Overall Verdict

### Can Claude teach a Year 5 child with ONLY this graph data?

**Answer: Yes, in 5 out of 11 subjects — with significant caveats.**

| Category | Subjects | Verdict |
|---|---|---|
| **Claude can teach well** | English, Science | 7-8/10. Rich data, good Content Vehicles, excellent misconceptions. Main gap: worked examples and model responses. |
| **Claude can teach adequately** | Maths, History, Computing | 6-7/10. Good structural data but needs more concrete teaching materials (worked examples for Maths, model responses for History, programming challenges for Computing). |
| **Claude can be a knowledge companion** | Geography, DT, Languages | 5-6/10. Good conceptual data but significant gaps in content coverage or language-specific material. |
| **Claude is fundamentally limited** | Art, Music, PE | 3-5/10. The subjects require physical/sensory modalities that text-based AI cannot deliver. Data quality is not the issue — the medium is. |

### The Three Things That Would Most Improve Teaching Readiness

1. **Add worked examples with difficulty sub-levels** (especially Maths). This single addition would lift the weakest core subject from 6.2 to approximately 8/10. Every Y5 teacher uses worked examples daily — they are the atomic unit of maths teaching.

2. **Complete Content Vehicle coverage** (especially Geography and Computing). Vehicles transform teaching readiness from "Claude knows what to teach" to "Claude has materials to teach with." The ~40% Geography gap and absent Computing vehicles are the largest structural holes.

3. **Add model response exemplars at Y5 level** (especially English and Science). Claude needs to know not just what understanding looks like conceptually but what it looks like in a child's written or spoken response. Without exemplars, Claude cannot reliably judge whether a child's answer meets the Y5 standard.

### What the Graph Does Exceptionally Well

- **Misconception data**: The single best feature for AI teaching. Specific, actionable, evidence-based.
- **Prerequisite chains**: Claude always knows what came before and what comes next.
- **Learner Profile pedagogy**: The productive failure + interleaving + spacing framework is current best practice.
- **ThinkingLens integration**: Gives every lesson a cognitive frame with specific questions to ask.
- **Content Vehicle structure**: Where they exist, they transform bare concepts into teachable bundles.

### What's Realistically Missing

- **Worked examples** (no step-by-step numerical or procedural demonstrations)
- **Difficulty sub-levels** (no internal progression within concepts)
- **Model responses** (no exemplar answers at Y5 standard)
- **Actual content** (no text passages, no vocabulary lists, no music recordings)
- **Y5-specific learner profile** (the "KS2 from Y3" profile is too broad — Y5 metacognition is more developed than Y3)
- **Interactive assessment items** (no question banks, no calibrated items)

### Final Score: 6.3/10 (weighted average across all subjects)

This is a strong foundation. The graph provides Claude with what most AI tutors lack: **curriculum coherence** (knowing where each concept sits in a learning progression), **diagnostic intelligence** (knowing what errors to expect and how to respond), and **pedagogical discipline** (knowing HOW to structure a session, not just what to put in it).

The path from 6.3 to 8+ is clear: add the concrete teaching materials (worked examples, model responses, difficulty gradients, assessment items) to the already-excellent structural framework. The architecture is right; it needs more content.

---

*Review completed by Ms Sarah Brennan, Y5 Class Teacher, 11 years' experience.*
*"I've taught Year 5 long enough to know that knowing the curriculum isn't the same as being able to teach it. This graph knows the curriculum exceptionally well. The question is whether it gives Claude enough to actually sit with a child and help them learn. For English and Science — yes, mostly. For Maths — nearly, but the absence of worked examples is like sending a teacher into a lesson without a whiteboard. For the practical subjects — we need to be honest that an AI tutor has limits, and that's fine."*
