# Gap Analysis: Mr. Kowalski — English (KS2)

**Planner:** Traditional Tales: Myths from Around the World
**Date:** February 2026 (V8 review)
**V7 score:** 6.0/10 -> **V8 score:** 7.0/10

---

## Top 5 Data Additions That Would Improve This Planner

### 1. Thinking Lens and Learner Profile Integration (HIGH PRIORITY)

The V7 cluster context included a named thinking lens with question stems, a pedagogy sequence, scaffolding levels, interaction types, and feedback guidance. The V8 planner has none of this. The per-subject ontology (EnglishUnit) does not appear to inherit the thinking lens or learner profile data that ConceptClusters carry.

**What I need:** Each EnglishUnit node should either carry its own thinking lens assignment or inherit one from its primary concept's parent cluster. The learner profile data (pedagogy sequence, scaffolding level, interaction types) should be surfaced for the relevant year group. This is not new data — it already exists in the graph. The planner generator just needs to pull it through.

**Impact:** Would restore the V7 pedagogical framework and enable session-level planning. Without it, the planner is a content specification without a teaching methodology.

### 2. Vocabulary Definitions on the Word Mat (HIGH PRIORITY)

The vocabulary word mat lists 8 terms with an empty "Meaning" column. The graph stores key_vocabulary arrays on Concept nodes, but these are term lists, not glossaries. For a Y3 classroom, every vocabulary display needs definitions.

**What I need:** Either a `vocabulary_definitions` property on Concept nodes (mapping term to child-friendly definition) or a separate Vocabulary/Glossary node type. Definitions must be age-appropriate — the content guidelines specify Lexile 150-350L for Y3, max FK grade 2.

**Example for this planner:**

| Term | Definition |
|------|-----------|
| myth | A very old story that explains how the world works, often with gods or supernatural beings |
| supernatural | Something that cannot happen in real life, like magic or gods |
| archetype | A type of character that appears again and again in stories, like the hero or the trickster |
| quest | A long journey to find or achieve something important |

**Impact:** Would make the vocabulary section immediately usable rather than requiring teacher completion. This is one of the easiest data additions — definitions can be generated from existing concept descriptions.

### 3. Broader Text Recommendations with Diversity Metadata (MEDIUM PRIORITY)

The planner suggests two texts, both from Mediterranean classical traditions. A unit on "Myths from Around the World" needs texts from diverse cultures. The graph's EnglishUnit and SetText nodes should carry richer text metadata.

**What I need:** 5-8 suggested texts per unit, each with: title, author, culture/tradition of origin, reading level (Lexile or book band), key features demonstrated, and a diversity tag (continent/culture of origin). For this unit specifically:

- West African tradition: *Anansi the Spider* (Gerald McDermott) or *A Story, A Story* (Gail Haley)
- Norse tradition: *Norse Myths* (Kevin Crossley-Holland, abridged)
- Hindu tradition: *The Illustrated Mahabharata* (DK) or Rama and Sita retellings
- Indigenous Australian: Dreamtime stories collections
- Greek: *The Orchard Book of Greek Myths* (already listed)
- Egyptian: *Tales of Ancient Egypt* (already listed)

**Impact:** Would ensure the unit delivers on its "around the world" promise and meets the Ofsted expectation for diverse representation in the English curriculum.

### 4. Session Sequence / Unit Planning Structure (MEDIUM PRIORITY)

The planner provides a unit overview but no lesson-by-lesson sequence. For English, the unit structure follows a well-known pattern: immerse in the genre (Week 1), analyse text features (Week 1-2), plan and draft (Week 2), edit and publish (Week 3). The graph should encode this.

**What I need:** A `session_sequence` property on EnglishUnit nodes — or a linked `:UnitPhase` node type — that outlines the typical phases for this study type (Genre Study). For a Genre Study, the phases would be:

1. **Immersion** (3-4 lessons): Read and discuss multiple examples of the genre
2. **Analysis** (2-3 lessons): Identify and analyse text type features; teach grammar in context
3. **Planning** (1-2 lessons): Oral rehearsal, story maps, planning templates
4. **Drafting** (2-3 lessons): Write first draft using success criteria
5. **Editing and Publishing** (1-2 lessons): Peer review, edit, produce final version

This is the standard English teaching cycle. The VehicleTemplate nodes (24 templates with TEMPLATE_FOR KeyStage) appear to contain this kind of pedagogical structure, but none is surfaced in the planner.

**Impact:** Would turn the planner from a content specification into a teachable unit plan.

### 5. Success Criteria and Sensitive Content Sections (LOWER PRIORITY)

The geography planner includes a "Success criteria" section with "Pupils can..." statements and specific assessment targets. The English planner has none. The writing outcome serves as an implicit criterion, but explicit success criteria are standard in English planning.

**What I need:** Auto-generated success criteria derived from the primary concept's DifficultyLevel data. At "Expected" level for this unit:

- I can retell a myth in my own words, keeping the key events in order
- I can include supernatural elements and a moral in my retelling
- I can explain the difference between a myth, a legend, and a fairy tale
- I can use multi-clause sentences with conjunctions (when, because, although)
- I can organise my writing into paragraphs

The planner should also flag sensitive content. Myths contain religious themes (creation myths, polytheism), violence (monster-slaying, divine punishment), and cultural specificity that needs respectful handling. A brief guidance note would prevent common mistakes.

**Impact:** Would bring the English planner to parity with the geography planner in terms of assessment readiness.

---

## What the Auto-Generator Does Well

1. **DifficultyLevel differentiation is the standout improvement.** The entry/developing/expected/greater depth table for the primary concept is the single most useful addition since V7. The example tasks are specific, the common errors are accurate, and the progression makes sense. If I could only keep one section of this planner, it would be this.

2. **Text type features are precise and actionable.** "Supernatural elements, heroic quest structure, moral or origin explanation, archetypal characters" — I could turn these directly into a success criteria checklist for writing. This is better than V7's vehicle-level text features because it is specific to this unit rather than generic to the genre.

3. **The writing outcome is clear and assessable.** "Retell a myth from a different culture (400-500 words) preserving key features of the genre including supernatural elements, a quest, and a moral" — this is a complete writing brief. I know the word count, the genre features, and the task. V7 had "Write an adventure narrative (500-700 words)" which was broader but less specific.

4. **Pitfalls are practical and non-obvious.** "All myths treated as interchangeable" is the kind of planning error that a teacher might not spot until mid-unit. Having it flagged in advance saves wasted lessons.

5. **Concept teaching guidance is detailed.** The teaching guidance for EN-Y3-C020 walks through how to distinguish fairy stories, myths, and legends, suggests reading from different cultures, and recommends using myths as models for writing. This is more than a curriculum statement — it is pedagogical advice.

6. **Grammar focus correctly identified from Appendix 2.** Multi-clause sentences, paragraphs, and present perfect tense are the right grammar targets for Y3 and are explicitly linked to the statutory appendix.

---

## What the Auto-Generator Gets Wrong

1. **Source document is incorrect.** The planner cites "KS2 English Grammar, Punctuation and Spelling Test Framework 2016" as the source for a reading comprehension unit. This is wrong — the SPaG test framework does not cover reading comprehension. The generator appears to apply the same source document to all English planners without checking domain relevance.

2. **Cross-curricular subject field is broken.** Both cross-curricular links list "None" in the Subject column instead of "Art and Design" and "History." The data is in the graph (the links themselves are correctly described) but the subject field is not being populated by the generator.

3. **Genre section duplicates information.** The "Genre" section provides descriptions of "Traditional Tale" and "Narrative" that are generic rather than unit-specific. The Traditional Tale description is useful, but the Narrative description ("Extended prose fiction...") does not add value to a myths planner. This section could be tighter.

4. **Secondary concepts are truncated.** The five secondary concepts are listed as single-line summaries that appear to be cut off mid-sentence (lines end with "..."). The planner should either show full descriptions or clearly indicate these are summaries with a link to full data.

5. **No "Follows" in sequencing.** The planner shows what this unit leads to (Adventure Narrative: The BFG) but not what precedes it. A unit planner should show both directions of the sequence.

---

## Comparison: Hand-Written vs Auto-Generated Planner

| Aspect | Hand-written (my current planning) | V8 Auto-generated planner |
|--------|-----------------------------------|---------------------------|
| Time to create | 3-4 hours for a 3-week unit | 0 minutes (auto-generated) |
| Curriculum accuracy | Good (I check the NC) but can miss details | Excellent — statutory references are precise |
| Text selection | 5-8 texts from my personal library and school stock | 2 texts, both classical Mediterranean |
| Differentiation | Based on my knowledge of my class | Based on DifficultyLevel data — generic but well-structured |
| Grammar in context | I plan which grammar to teach through which text | Grammar focus listed but not mapped to specific lessons |
| Lesson sequence | Full 10-15 lesson breakdown | Unit overview only — no lesson breakdown |
| Model texts | I write them or select extracts from the core text | None provided |
| Vocabulary | I select 10-15 words with definitions and display | 8 words without definitions |
| Assessment | Rubric based on school assessment framework | No rubric, no success criteria |
| Cross-curricular | I plan with year group team — Drama, Art, History | 2 links with broken subject field |

**Summary:** The auto-generated planner gives me a stronger curriculum foundation than my hand-written plans (statutory references, misconceptions, differentiation tiers). But it gives me a weaker teaching plan (no lesson sequence, no model texts, no vocabulary definitions, no assessment rubric). My hand-written plan is ready to teach from; the auto-generated planner is ready to plan from. That is meaningful progress — it saves me the first hour of a 4-hour planning process.

---

## Verdict

The V8 planner represents genuine progress over V7 for English. The DifficultyLevel differentiation data, text type features, writing outcome, and pitfalls are all new and useful. Moving from ConceptCluster context to a unit-level planner (EnglishUnit from the per-subject ontology) is the right structural decision — English teachers plan in units, not clusters.

However, the planner loses V7's pedagogical infrastructure (thinking lens, learner profile, session structure) without replacing it with unit-level equivalents. The result is a planner that is stronger on curriculum content but weaker on teaching methodology than V7. The ideal V9 planner would merge both: V8's unit framing with V7's pedagogical scaffolding.

The core English gap — no model texts, no vocabulary definitions, no lesson-level planning — remains. This is the gap that separates "a useful reference document" from "a teaching tool." Closing it requires vocabulary definitions (easy), broader text recommendations (medium), and session sequencing (medium). Model texts remain the hardest gap because they require authored content, not just structured data.

**V7: 6.0/10 -> V8: 7.0/10.** A one-point improvement driven by DifficultyLevel data and unit-level framing. The next point requires restoring the thinking lens and learner profile, adding vocabulary definitions, and providing a session sequence.
