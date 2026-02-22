# Year 2 Mathematics — Teacher Evaluation (v4)

**Evaluator:** James Henderson, Year 2 class teacher (Maths lead), 15 years' experience
**Date:** 2026-02-22
**Scope:** All 8 Year 2 Maths domains (23 concepts, 34 objectives, 16 concept clusters)

---

## 1. Half-Term Planning Exercise (Autumn 1, 6 weeks)

I attempted to plan a full half-term using only what the graph provides. Here's what I produced and where I hit problems.

### Proposed Sequence

| Week | Domain | Cluster | Concepts | Notes |
|------|--------|---------|----------|-------|
| 1 | Number & Place Value | CL001 | C001 (Counting in 2s, 3s, 5s), C011 (Odd/even) | Counting in 3s is new; link odd/even to 2x table from Day 3 |
| 2 | Number & Place Value | CL002 | C002 (Place value), C003 (Comparing with < > =) | Dienes blocks essential all week; flexible partitioning by Friday |
| 3 | Addition & Subtraction | CL001 | C004 (Recall facts to 20, derived to 100) | Rapid-fire bond practice daily; bridge 6+4=10 to 60+40=100 |
| 4 | Addition & Subtraction | CL001 cont. | C005 (Two-digit add/sub) | Column recording introduced; crossing tens boundary by Thursday |
| 5 | Addition & Subtraction | CL002 | C006 (Commutativity), C007 (Inverse) | Fact families; bar model for inverse; link C006 forward to multiplication commutativity |
| 6 | Number & Place Value | CL003 + Assessment | C021 (Patterns) + formative assessment | Patterns standalone; end-of-half-term assessment covering Weeks 1-5 |

### What worked

1. **The cluster sequencing is genuinely sound.** CL001 before CL002 in each domain follows the pedagogical dependency chain correctly. The graph knows that you can't teach comparing numbers until you've taught place value, and it knows you can't teach commutativity until children can actually add. This is right.

2. **The prerequisite chains are excellent.** The external prerequisites (Y1 → Y2) would be invaluable for September baseline assessment. If I know a child hasn't mastered MA-Y1-C008 (Number bonds within 20), I know they're not ready for MA-Y2-C004. An AI could use this to generate a diagnostic assessment in the first week of term. This is genuinely useful.

3. **The CO_TEACHES relationships map to how I actually teach.** The cross-domain link from C001 (counting in steps) to C008 (times tables) is exactly what I'd do — when we start multiplication in Spring, I'd reference the counting work from Autumn. The fact that the graph captures this is impressive. The Henderson annotations on these (yes, they used my name — I assume from a previous review) are accurate.

4. **The concept-level detail is the strongest part of the whole thing.** Teaching guidance, common misconceptions, key vocabulary — all 23 concepts have these, and they're good. The misconception for C002 ("pupils think the 3 in 37 means 3, not 30") is the single most common error I see in Year 2 maths. Getting this right matters.

5. **The CC Math cluster inspirations are a nice touch.** Seeing that CL001 in Addition maps to CC Math 2.OA.B.2 ("Fluently add and subtract within 20") gives useful international perspective. The US has been more systematic about fluency benchmarks.

### What didn't work

1. **No lesson count per cluster.** This is a significant gap. My half-term plan allocates 2 weeks to Addition CL001, but the graph gives me no indication of whether that's right. CL001 contains C004 (weight 3) and C005 (weight 3, keystone), and in practice this is easily 10 lessons. But CL002 in Position & Direction (single concept, weight 3) might be 3-4 lessons. The teaching_weight hints at relative importance but doesn't translate to time. **An AI generating a scheme of work needs lesson-count estimates per cluster, or at minimum a heuristic: weight × some multiplier = suggested lessons.**

2. **No differentiation data at all.** My class of 30 has at least 4 children still working on Y1 number bonds, 20 children at expected Y2, and 6 children who could handle Y3 content. The graph has a single path through each concept. There's no "if the child is below expected, scaffold with X" or "if above expected, extend with Y." For content generation, this means the AI produces one-size-fits-all material. **Need: within-concept difficulty tiers or a simple below/at/above pathway per concept.**

3. **No concrete-pictorial-abstract (CPA) progression is structured as data.** The teaching guidance mentions Dienes blocks, number lines, bar models — but only in free text. An AI generating a lesson or slide deck can't reliably extract "Step 1: Show 3 tens-sticks and 7 unit cubes" from a paragraph of prose. **Need: a structured CPA field per concept, e.g. `concrete: ["Dienes blocks", "straws bundled in tens"]`, `pictorial: ["place value chart", "number line"]`, `abstract: ["37 = 30 + 7"]`.**

4. **No worked examples.** The pedagogy profile says "Worked examples required" but there isn't a single actual worked example in the graph. The teaching guidance describes what to teach, not how to walk through a specific problem step by step. For an AI to generate a lesson, it needs model problems. **Need: at least 2-3 worked examples per concept, showing the step-by-step thinking a teacher would narrate.** E.g., for C005: "Let's add 34 + 27. First, I partition: 30 + 20 = 50, and 4 + 7 = 11. Now 50 + 11 = 61."

5. **No question specifications for assessment.** The graph can tell me what to assess (the objectives) but gives me nothing about how to construct a good question. For C002 (place value), a good diagnostic question would be: "In the number 47, what does the 4 represent? A) 4  B) 40  C) 47" — this directly tests the most common misconception. But the graph has no item templates, no difficulty tiers within a concept, no specification of what makes a question diagnostic vs. practice vs. summative. **Need: question type specifications per concept, linking misconceptions to diagnostic distractors.**

6. **No timing guidance for individual activities.** The pedagogy profile says sessions are 8-15 minutes with 3 activities. But a Year 2 maths lesson in school is typically 45-60 minutes. Are we talking about the AI-delivered portion only? This needs clarifying. If so, how does the AI-delivered activity relate to the teacher-led lesson? **Need: explicit statement of whether the graph is modelling a full lesson or an AI-assisted activity within a lesson.**

---

## 2. Critical Data Error: Wrong Learner Profile

**The context file includes the Y1 learner profile, not Y2.** This is a serious generation error.

| Field | Context file says (Y1) | Actual Y2 data | Impact |
|-------|----------------------|----------------|--------|
| Number range | 1-20 oral, 1-10 written | **0-100** | AI would generate content for 5-year-olds, not 6-7-year-olds |
| Sentence length | Max 8 words, avg 4 | Max 10, avg 6 | Content would be oversimplified |
| FK grade max | 0 | 1 | Reading level too low |
| Session length | 5-12 min, 2 activities | 8-15 min, 3 activities | Sessions too short |
| TTS | All text must be voiced, no text without audio | Required for main content, tap-to-hear available | Overusing audio, not building reading independence |
| Vocabulary | Concrete everyday only | Concrete + simple abstract | Missing "cause/effect", "equal parts" etc. |
| Interaction types (primary) | Includes phoneme_splitter, letter_toggler | Includes sentence_assembly, voice_recorder | Maths-irrelevant Y1 tools promoted |

**This would produce completely inappropriate content.** A child who can work with numbers to 100 would be given questions using numbers to 10. The reading support would be excessive (Y2 children are consolidating phonics, not beginning them). The session would be too short and too simple.

**Recommendation:** Fix the context generation pipeline to pull the correct Year's learner profile. This is the single highest-priority bug.

---

## 3. Assessment and Testing Content

### What the graph enables

- **Concept-referenced formative assessment:** The objectives are clear enough to write questions against. "Recall and use addition and subtraction facts to 20 fluently" (O008) gives an AI a clear target.
- **Prerequisite-based diagnostic testing:** The prerequisite chains could generate a diagnostic test at the start of a topic: "Before we learn two-digit addition, let's check you know your number bonds to 20."
- **Misconception-informed distractors:** The common misconceptions are rich enough that an AI could construct multiple-choice questions where the wrong answers correspond to known errors (e.g., for 37 = ? + ?, offering 3 + 7 as a distractor alongside 30 + 7).

### What's missing for testing

- **No item difficulty levels.** Within C005 (two-digit addition), there's a massive range: 34 + 5 (no exchange) is much easier than 47 + 36 (exchange in ones). The graph doesn't distinguish these. **Need: difficulty sub-levels within concepts, or at minimum a specification of the calculation types (e.g., 2-digit + 1-digit, 2-digit + tens, 2-digit + 2-digit no exchange, 2-digit + 2-digit with exchange).**
- **No success criteria.** What does "mastery" look like in concrete, assessable terms? The pedagogy profile says "5 correct in 10 days (80%)" but correct at what? 5 correct single-digit additions isn't the same as 5 correct two-digit additions with exchange.
- **No diagnostic question templates.** The misconceptions are there, but they're not structured as assessment items. A field like `diagnostic_question: { stem: "What does the 4 in 47 represent?", correct: "40", misconception_distractor: "4", misconception_targeted: "face_value_error" }` would be transformative for AI test generation.
- **No link between assessment clusters and the concepts they assess.** The cluster types include "assessment" but there are none in my Y2 data — all clusters are introduction or practice. Where's the assessment gate?

---

## 4. Teacher Resource Generation (Slide Decks, Lesson Plans)

### Could an AI generate a good Year 2 maths lesson from this data?

**Partial yes for the narrative structure. Definite no for the visual/concrete resources.**

The teaching guidance gives an AI enough to write a lesson plan narrative: "Start with Dienes blocks showing 37 as 3 tens and 7 ones. Ask children to partition. Progress to place value charts. Introduce flexible partitioning: 37 = 20 + 17."

But a slide deck needs:
- **Images of concrete resources** (Dienes blocks, hundred squares, number lines) — not in the graph
- **Specific worked examples with step-by-step visuals** — not in the graph
- **Practice question sets at graded difficulty** — not in the graph
- **Plenary/assessment questions** — not in the graph
- **Key questions for the teacher to ask** (e.g., "How do you know 47 is greater than 39?") — mentioned in prose but not structured

### What would make teacher resource generation viable

1. **Structured worked examples** (2-3 per concept, with explicit steps)
2. **CPA resource lists** as structured data, not prose
3. **Key questions** per concept (the questions a teacher asks during the lesson to check understanding)
4. **Graded practice sets** or at least difficulty specifications
5. **Lesson timing suggestions** (5 min review, 10 min input, 15 min practice, 5 min plenary — or whatever the intended model is)

---

## 5. The CASE Standards Reference

The reference file is essentially empty for maths. It lists NGSS science practices and core ideas, but **there is no Common Core Mathematics content at all**. The "Inspired by" references on the clusters (e.g., "CC Math 2.OA.B.2") are useful anchors, but I can't look up what CC Math 2.OA.B.2 actually says because it's not in the graph.

This is a missed opportunity. Common Core Maths has:
- **Explicit fluency standards** ("Fluently add and subtract within 20 using mental strategies") — these could benchmark our mastery thresholds
- **Standards for Mathematical Practice** (8 practices that parallel our epistemic skills) — these could enrich the reasoning skills layer
- **Cluster headings** that the graph already references but doesn't include the actual content of

**Recommendation:** Either populate the CC Math content in the graph or remove the CC Math references from the clusters. Having references you can't look up is worse than having no references.

---

## 6. The Epistemic Skills

The 5 MathematicalReasoning skills for KS1 are appropriate and well-described. But they're not connected to specific concepts or domains in any structured way. When I'm teaching place value, I need to develop MR-KS1-002 (explaining mathematical ideas) differently from when I'm teaching statistics.

**Need: domain-specific instantiations of each epistemic skill.** E.g., MR-KS1-002 in the context of Addition might be "Explain why you chose to partition 34 + 27 as 30 + 20 + 4 + 7" while in Fractions it might be "Explain why 2/4 is the same as 1/2."

---

## 7. The Interaction Types

The maths-specific interaction types are promising:
- **Number line scrubber** — excellent for C001 (counting), C003 (comparing), C012 (fractions)
- **Place value blocks** — perfect for C002, and would be excellent for C005 (two-digit addition)
- **Column addition** — appropriate for C005, though Year 2 is preparation for formal methods, not formal methods themselves

**Missing interaction types for Year 2 maths:**
- **Array builder** — critical for C008 (times tables), C009 (multiplication notation), C010 (commutativity). Arrays are the primary concrete representation for multiplication and the graph's teaching guidance mentions them repeatedly, but there's no array interaction type.
- **Part-whole model / bar model** — mentioned in the teaching guidance for C004, C007 (inverse) and fractions, but no interaction type for it. This is the single most important visual model in primary maths.
- **Coin manipulative** — C015 (money) needs children to drag and combine coins. None of the existing interaction types handle this.
- **Clock face** — C016 (telling time) needs an interactive analogue clock. Not present.
- **Fraction strips/wall** — C012 and C013 need fraction visualisation beyond what the generic fraction_visualizer might offer. A fraction wall where children can see equivalence is essential.

**The interaction types feel like they were designed top-down rather than from the concept content outward.** An AI trying to generate an activity for "telling the time to five minutes" has no clock face interaction to use. It would fall back on multiple choice, which is a poor substitute for actually moving clock hands.

---

## 8. Overall Verdict

### What's genuinely good

- **Concept quality is high.** The 23 concepts with teaching guidance, misconceptions, and vocabulary are the best part of this graph. An experienced teacher would recognise these as accurate and useful.
- **Prerequisite chains are correct and useful.** Both within-year and cross-year. This is hard to get right and they've done it.
- **CO_TEACHES relationships capture real pedagogical connections.** The cross-domain links (place value ↔ addition, counting in steps ↔ times tables) match how I'd actually plan.
- **Cluster sequencing is pedagogically sound.** The domain-level ordering works.
- **The learner profile concept is excellent** — when it's the right year's data. Having feedback rules, interaction types, and content guidelines attached to the year group is exactly what an AI needs.

### What needs fixing (priority order)

1. **CRITICAL: Fix the learner profile year mapping.** Y1 data attached to Y2 context. Would produce age-inappropriate content.
2. **HIGH: Add worked examples.** 2-3 per concept with explicit steps. Without these, an AI can describe what to teach but can't model how to teach it.
3. **HIGH: Add difficulty sub-levels within concepts.** At minimum, specify the calculation types/problem types that constitute easy, medium, and hard for each concept.
4. **HIGH: Add missing maths interaction types** (array builder, part-whole model, coin manipulative, clock face). Without these, the AI can't generate appropriate interactive activities for 4 of 8 domains.
5. **MEDIUM: Structure the CPA progression** as queryable data, not prose. List the concrete resources, pictorial representations, and abstract notation per concept.
6. **MEDIUM: Add diagnostic question templates** linking misconceptions to assessment items.
7. **MEDIUM: Add lesson-count estimates per cluster** or a heuristic formula.
8. **LOW: Populate Common Core Maths content** or remove the dangling references.
9. **LOW: Add domain-specific epistemic skill instantiations.**

### Can an AI generate content from this data today?

- **A quiz?** Partially. It could generate questions at the right curriculum level but couldn't grade difficulty within a concept or construct truly diagnostic items.
- **A lesson?** The narrative structure, yes. The concrete resources and worked examples, no. The interactive activity would be limited by missing interaction types.
- **A slide deck?** No. Not enough structured visual/resource data. The teaching guidance is prose, not a slide-ready format.
- **A scheme of work?** The domain and cluster structure gets you 70% there. The missing 30% is lesson counts, differentiation, and cross-curricular links.

### The 70% problem

This graph is about 70% of what you'd need for genuinely good AI-generated content. The 70% it has is the hard part — getting the curriculum structure, prerequisites, and concept detail right. The remaining 30% is more mechanical (worked examples, question templates, resource lists) but it's the 30% that makes the difference between "correct but generic" and "actually usable in a classroom."

---

## 9. Cross-Team Discussion Findings (added post-evaluation)

The following insights emerged from discussion with Okonkwo (Y4 English), Kapoor (Y5 Science), Osei (KS3 Biology), and Adeyemi (KS3 Geography/History). These sharpen and extend my original findings.

### 9.1 Content Generation Readiness Spectrum (Okonkwo)

Content generation readiness falls on a three-tier spectrum that applies across all subjects:

| Tier | Type | Maths examples | English examples | Graph readiness | Gap |
|------|------|---------------|-----------------|-----------------|-----|
| 1 | Rule-based | Times tables, number bonds, column arithmetic | Spelling rules, grammar rules, punctuation | High | Small — add worked examples / exercise templates |
| 2 | Context-dependent | Word problems, measurement in context | Vocabulary in context, sentence construction for purpose | Medium | Moderate — needs cross-subject links + difficulty grading |
| 3 | Text/resource-dependent | Investigations, open-ended problem solving | Reading comprehension, writing composition, literary analysis | Low | Large — the teaching vehicle is entirely absent |

This maps to Bloom's taxonomy: the graph is strongest at knowledge/comprehension, weakest at application and above. Higher-order skills need richer context, and the graph is context-poor.

**Readiness by subject:** Maths ~70%, English ~55%, Science ~50-60%, Geography ~40%, History ~20%. The more a subject depends on structured, rule-based content, the higher the readiness. The more it depends on rich contextual content (sources, case studies, texts), the lower.

### 9.2 The WS-as-Bridge Architecture for Cross-Subject Links (Kapoor)

The single most actionable architectural proposal from the whole evaluation. Instead of linking hundreds of science concepts directly to maths concepts, route through Working Scientifically skills:

```
Science Concept → DEVELOPS_SKILL → WS-KS2-005 (Recording data)
WS-KS2-005 → REQUIRES_MATHS → MA-Y4 Statistics (bar charts)
WS-KS2-005 → REQUIRES_MATHS → MA-Y6 Statistics (line graphs)
```

This extends to English literacy too:
```
WS-KS2-007 (Communicating findings) → REQUIRES_LITERACY → EN-Y4-C047 (Organisational devices)
```

**~35 new relationships through an existing node type (WS skills are already in the graph but currently disconnected).** Solves cross-subject for science AND English without linking every concept individually. The graph already has all the nodes; it just needs the bridge relationships.

Kapoor also proposed a formality property on cross-subject links: `REQUIRES_MATHS {formality: "informal", introduced_via: "science_investigation", formal_from: "Y6"}` — enabling an AI to scaffold maths that's been introduced informally in science before being formally taught in maths.

Specific cross-subject links identified:
- Kapoor: 7 KS2 Science → Maths prerequisites
- Osei: 9 KS3 Science → Maths prerequisites (formula rearrangement, graphing, unit conversion)
- Henderson: 2 Y2 Statistics → Science data recording links
- **Total: 18 specific, actionable relationships**

### 9.3 Graph + Companion Resource Layer Architecture (Adeyemi)

The graph should remain the curriculum structure and relationship layer. It should NOT try to store rich unstructured content (texts, case studies, primary sources, investigation templates). Instead, it needs a companion resource layer that it can reference:

- The graph says: "GE-KS3-C001 teaches plate tectonics and needs a contrasting earthquake case study"
- The resource layer provides: "Haiti 2010 case study pack: data table, satellite imagery, newspaper sources, assessment questions"
- The graph points to the resource; the resource is stored elsewhere

This preserves what the graph does well (structure, relationships, prerequisites, misconceptions) without asking it to do what it does badly (store rich unstructured content).

### 9.4 Progression Stages as Structured Data (Okonkwo + Henderson)

Every subject has a pedagogical progression model that the teaching guidance describes in prose but doesn't structure as data:

- **Maths:** Concrete → Pictorial → Abstract (CPA)
- **English:** Oral → Scaffolded → Independent
- **Science:** Guided → Structured → Open
- **Geography:** Descriptive → Analytical → Evaluative
- **History:** Factual → Interpretive → Argumentative

If the graph had `progression_stages` as structured data per concept, an AI could generate stage-appropriate activities. Same data structure, different subject content.

### 9.5 Learner Profile Bug Pattern Confirmed

The context generation pipeline indexes by key stage, not year group:
- Henderson (Y2): Got Y1 profile (KS1 → Y1)
- Kapoor (Y5): Got Y3 profile (KS2 → Y3) — number range 0-1000 instead of 0-1,000,000
- Okonkwo (Y4): Got Y3 profile (KS2 → Y3) — broadly ok but imprecise
- Adeyemi (KS3): Profile doesn't differentiate between subjects — 100-200 word responses when History needs 500-800

**The per-year data EXISTS in the raw extraction files.** The pipeline just pulls the wrong year. This is a straightforward fix with outsized impact.

### 9.6 Misconceptions as Immediate Quick Win

Every teacher independently identified misconception data as the single most valuable asset. Misconceptions can generate diagnostic questions NOW without any structural changes. **Recommended quick win: build a diagnostic question generator that takes misconception text as input and produces assessment items with misconception-informed distractors.** Works across all subjects immediately.

---

## 10. Revised Recommendations (Post-Discussion)

| Priority | Recommendation | Effort | Impact | Source |
|----------|---------------|--------|--------|--------|
| 1 | Fix learner profile pipeline (index by year, not KS) | Small | Prevents all wrong-level content | Henderson, Kapoor |
| 2 | Build diagnostic question generator from misconceptions | Small-Medium | Works across ALL subjects immediately | All 5 teachers |
| 3 | Add ~35 WS-bridge cross-subject relationships | Small (1-2 days) | Transforms science content generation KS2-3 | Kapoor, Osei, Henderson |
| 4 | Add worked examples (2-3 per concept, rule-based first) | Medium | Enables Tier 1 content generation | Henderson, Okonkwo |
| 5 | Add within-concept difficulty sub-levels (introductory/developing/secure) | Medium | Enables differentiation and adaptive progression | Henderson, Okonkwo |
| 6 | Add progression_stages structured data per concept | Medium | Enables stage-appropriate activity generation | Okonkwo, Henderson |
| 7 | Add subject-specific interaction types | Medium | Enables appropriate interactive activities | Henderson |
| 8 | Design companion resource layer interface | Large | Enables text/case study/source-dependent content | Adeyemi |
| 9 | Curate cross-subject topic context links (requires teacher input) | Large | Enables contextualised teaching across primary curriculum | Okonkwo, Henderson |
| 10 | Populate resource layer for humanities | Large | Raises History from 20% to viable | Adeyemi |

---

*James Henderson, Maths Lead*
*"If the misconceptions are right, the rest can be fixed. And the misconceptions are right."*
