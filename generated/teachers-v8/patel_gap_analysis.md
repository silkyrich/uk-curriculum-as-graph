# Gap Analysis: Ms. Patel — English (KS1)

**Planner:** Traditional Tales: The Three Billy Goats Gruff
**Date:** February 2026 (V8 review)
**V7 score:** 5.5/10 -> **V8 score:** 7.5/10

---

## Top 5 Data Additions That Would Improve This Planner

### 1. Oral Rehearsal and Talk-for-Writing Scaffolds (HIGH PRIORITY)

This is the single most important missing element for KS1 English. The planner correctly names "Oral rehearsal" (EN-KS1-C043) as a secondary concept — "Saying sentences out loud before writing them down." But the planner provides no guidance on HOW to scaffold oral rehearsal.

In Y1, the pathway from listening to writing goes: listen to the story -> retell with actions -> retell with talk partner -> say your sentence aloud -> write your sentence. This is the talk-for-writing methodology that underpins most KS1 English teaching in England. The planner jumps from "here is the story" to "write 4-6 sentences" without modelling the oral stages in between.

**What I need:** A `rehearsal_scaffolds` property on EnglishUnit nodes (or a linked node type) that specifies:

- **Actions map:** Physical actions for each part of the story (e.g., stamp feet for "Trip, trap," arms wide for "biggest billy goat," crouch down for "under the bridge")
- **Story map template type:** For Billy Goats Gruff, a linear 4-box sequence map (bridge x3, then meadow)
- **Oral sentence stems:** "First, the _____ billy goat went over the _____." / "Then the troll said, '_____!'"
- **Talk partner protocol:** "Partner A retells the beginning. Partner B retells the middle. Swap."

This is not optional pedagogy — it is how KS1 writing happens. Without oral rehearsal, many Y1 children cannot compose even a single written sentence. The graph acknowledges this by including oral rehearsal as a concept; it just does not operationalise it.

**Impact:** Would make the planner genuinely teach-ready for KS1 rather than requiring the teacher to design the entire oral-to-written pathway.

### 2. Cross-Curricular Links for KS1 (HIGH PRIORITY)

The planner has no cross-curricular section at all. For KS1, this is a more significant gap than for KS2 because most primary schools teach Y1 through a topic-based approach where the core text drives learning across multiple subjects for 1-2 weeks.

**What I need:** Auto-generated cross-curricular connections from the EnglishUnit to related study nodes or concepts in other subjects. For Billy Goats Gruff, the obvious connections are:

| Subject | Connection | Study node (if exists) |
|---------|------------|----------------------|
| Art & Design | Making troll masks; painting bridge and meadow settings | ArtTopicSuggestion (KS1) |
| DT | Build a bridge strong enough for the biggest billy goat (materials and structures) | DTTopicSuggestion (KS1) |
| Drama/Speaking & Listening | Role-play, freeze frames, hot-seating the troll | EN-KS1 Spoken Language domain |
| Maths | Comparing sizes (small/medium/large), counting in threes, sequencing | MA-Y1 concepts |
| PSHE | Standing up to bullies, helping each other, facing fears | -- |
| Music | Creating sound effects for the refrain, composing "troll music" and "goat music" | MusicTopicSuggestion (KS1) |

The per-subject ontology has ArtTopicSuggestion, MusicTopicSuggestion, and DTTopicSuggestion nodes for KS1. If CROSS_CURRICULAR relationships exist between these and the EnglishUnit nodes, the planner generator should surface them.

**Impact:** Would transform this from an English-only planner into a cross-curricular planning hub, which is how KS1 teachers actually work.

### 3. Specific Text Edition Recommendations with Visual Suitability Notes (MEDIUM PRIORITY)

The planner suggests "The Three Billy Goats Gruff (Traditional, various illustrators)" with the note "Use a version with clear, large illustrations for shared reading." This is too vague for KS1 text selection, where the illustrations are as important as the words.

**What I need:** 3-4 specific editions with metadata:

| Edition | Illustrator | Why this version | Reading level |
|---------|-------------|-----------------|---------------|
| *The Three Billy Goats Gruff* | Paul Galdone | Classic illustrations, bold colours, text matches shared reading speed | Lilac/Pink band |
| *The Three Billy Goats Gruff* | Mary Finch / Roberta Arenson | Multicultural retelling, lively language | Pink/Red band |
| *The Three Billy Goats Gruff* | Jerry Pinkney | Stunning watercolours, wordless sections support inference | Red/Yellow band |
| *The Three Billy Goats Gruff* (Flip-up) | Ladybird | Interactive flaps for engagement, simplified text | Lilac band |

The graph's SetText and Genre nodes exist for KS3-KS4 English. A simpler equivalent for KS1-KS2 — with illustrator, format (picture book / chapter book / big book), and suitability notes — would be extremely valuable.

**Impact:** Would help teachers (especially NQTs) make informed text choices without spending an hour in the school library comparing editions.

### 4. Vocabulary Definitions with Visual Cue Notes (MEDIUM PRIORITY)

The word mat lists 6 terms with no definitions. For KS1, vocabulary displays MUST be visual — the word alone is not accessible to 5-6 year olds who are still learning to decode. Every term needs a definition AND a note about what visual support to provide.

**What I need:**

| Term | Definition (KS1 appropriate) | Visual cue |
|------|-------------------------------|-----------|
| troll | A scary creature in the story who lives under the bridge | Picture of troll under bridge |
| bridge | A path that goes over water or a gap | Picture of stone bridge |
| refrain | The part of the story that is said again and again | Speech bubble with "Trip, trap, trip, trap!" |
| character | A person or creature in a story | Three goats and the troll |
| story | Something that tells us what happened, with a beginning, middle and end | Three boxes: beginning, middle, end |
| retell | To tell a story again in your own words | Speech bubble with story map |

The missing sequencing vocabulary is critical: **first, then, next, finally** are the words the writing outcome requires children to use, but they do not appear on the word mat. These words ARE the scaffold for Y1 narrative writing. Their absence from the vocabulary section is an oversight.

**Impact:** Would make the vocabulary section functional for KS1 rather than decorative.

### 5. Session Sequence with Phase Timings for KS1 (LOWER PRIORITY)

KS1 lessons are shorter than KS2 (30-45 minutes vs 60 minutes), and the balance between shared reading, oral rehearsal, and writing is different. The planner needs a session sequence that reflects KS1 pedagogy.

**What I need:** A standard Genre Study sequence adapted for KS1:

| Lesson | Focus | Duration | Activities |
|--------|-------|----------|-----------|
| 1 | Story introduction | 35 min | Shared reading with big book, introduce vocabulary, respond through drawing |
| 2 | Story exploration | 35 min | Reread with actions, identify characters and setting, innovate the refrain |
| 3 | Story structure | 35 min | Story map (draw 4 scenes in sequence), identify beginning/middle/end |
| 4 | Oral rehearsal | 35 min | Say sentences aloud with talk partner, use sentence stems, rehearse retelling |
| 5 | Modelled writing | 35 min | Teacher writes retelling on board, children contribute, shared writing |
| 6 | Independent writing | 35 min | Children write own retelling using story map and word mat |
| 7 | Editing and sharing | 35 min | Reread own writing, check capitals and full stops, read aloud to class |

The VehicleTemplate nodes (24 templates, TEMPLATE_FOR KeyStage) should contain this kind of phase structure for a "Genre Study" at KS1. If they do, the planner generator should surface the relevant template.

**Impact:** Would provide the lesson-by-lesson framework that KS1 teachers need, especially NQTs who are less confident with sequencing a unit.

---

## What the Auto-Generator Does Well

1. **The DifficultyLevel differentiation table is the standout feature.** The entry/developing/expected/greater depth progression for "Narrative sequencing" is the single most useful element in the planner. The example tasks are Y1-appropriate (not scaled-down Y4 tasks), and the common errors describe real Y1 writing behaviours. "Writing sentences about different, unrelated topics" at Entry level and "Using the same connective ('then') for every sentence" at Developing level — I see both of these every day. This data did not exist in V7 and it transforms the planner's value for differentiation and assessment.

2. **The writing outcome is perfectly pitched for Y1.** "Retell the story in 4-6 sentences using the repeated refrain and sequencing words (first, then, next, finally)" — this is not too ambitious (the V7 unit-level outcomes were sometimes unrealistic) and not too simple. It specifies exactly what success looks like. A Y1 child can understand this target. A teaching assistant can assess against it.

3. **The text type features are KS1-specific and useful.** Repeated refrain, rule of three, good versus evil, beginning-middle-end — these are exactly the features of traditional tales that KS1 teachers teach explicitly. Naming "rule of three" is particularly helpful because many teachers teach it implicitly without giving it a name. The planner validates the pedagogical approach.

4. **The pitfalls show genuine understanding of KS1 English teaching.** "Spending too long on drama and retelling without moving to written output" is the single most common planning error I see in Y1 classrooms. "Writing task too ambitious for Y1" is the second. These pitfalls are not generic warnings — they are specific to this unit at this stage.

5. **The secondary concept selection is pedagogically sound.** Including oral rehearsal (EN-KS1-C043), sentence composition (EN-KS1-C044), and sentence boundaries (EN-KS1-C052) alongside the primary narrative sequencing concept describes the complete set of skills a Y1 child needs to retell this story in writing. The concept selection shows that the graph understands the reading-to-writing pathway at KS1.

6. **The genre description for Traditional Tale is well-written.** "The entry point to narrative for KS1 children because the familiar structures scaffold retelling and independent composition" — this is an accurate and helpful framing of why traditional tales matter pedagogically, not just culturally.

---

## What the Auto-Generator Gets Wrong

1. **Source document is wrong.** "Art and Design (KS1/KS2) - National Curriculum Programme of Study" has nothing to do with a Y1 English planner. The generator is assigning source documents incorrectly.

2. **No cross-curricular section at all.** This is more damaging for KS1 than KS2. In Y1, the core text drives the entire curriculum. Billy Goats Gruff naturally connects to Art (masks), DT (bridge building), Drama (role-play), Maths (counting/comparing), Music (sound effects), and PSHE (bullying). A planner that treats this as English-only misunderstands KS1 pedagogy.

3. **Sequencing vocabulary missing from the word mat.** The writing outcome requires children to use "first, then, next, finally" — but these words do not appear on the vocabulary word mat. The word mat and the writing outcome are not aligned. This is a data consistency error in the generator.

4. **Only one suggested text.** A KS1 unit should suggest at least 2-3 versions (for comparison) plus 1-2 other traditional tales with similar structures (for transfer). A single unspecified edition is insufficient.

5. **No oral rehearsal guidance despite naming it as a concept.** The planner identifies oral rehearsal (EN-KS1-C043) as a secondary concept but provides no guidance on how to structure it. For KS1, oral rehearsal is not supplementary — it is the mechanism by which children compose sentences before writing. Including it as a concept name without operationalising it is like listing "calculation" in a Maths planner without showing a worked example.

6. **Secondary concepts are one-line summaries.** The six secondary concepts are listed with truncated descriptions. For a unit planner, I would need at least the teaching guidance and common misconceptions for each — especially for sentence boundaries and capital letters, which are the mechanical skills Y1 children find hardest.

---

## Comparison: Hand-Written vs Auto-Generated Planner

| Aspect | My current hand-written planning | V8 auto-generated planner |
|--------|----------------------------------|---------------------------|
| Time investment | 2-3 hours for a 1-2 week unit | 0 minutes |
| Text selection | I choose a specific edition based on my class and our book stock | One unspecified edition |
| Differentiation | Based on my knowledge of my 30 individual children | DifficultyLevel table — generic but well-structured |
| Oral rehearsal | Detailed: actions, story map, talk partner protocol, sentence stems | Named as concept but not scaffolded |
| Cross-curricular | I plan the whole week around the text — Art, DT, Drama, Music | No cross-curricular section |
| Writing scaffolds | Sentence stems on strips, word mats on tables, writing frames in books | None provided |
| Assessment | I assess against school framework + NC expectations | No success criteria, no rubric |
| Vocabulary | 10-15 words with pictures and definitions on the working wall | 6 words with no definitions or visual notes |
| Lesson sequence | 6-8 lessons with clear reading/oral/writing balance | Unit overview only |
| Usefulness | Ready to teach from | Ready to START planning from |

**Summary:** The auto-generated planner gives me a stronger curriculum reference than my own planning (the differentiation table is better than anything I produce manually). But it gives me a weaker teaching plan (no session sequence, no oral rehearsal scaffolds, no cross-curricular links, no vocabulary definitions). My hand-written plan reflects my knowledge of my class and my school context; the planner reflects the curriculum structure. Both are needed — the ideal would be the planner's curriculum intelligence combined with my contextual knowledge.

---

## Verdict

The V8 planner represents a 2-point improvement over V7 for KS1 English. The DifficultyLevel differentiation data is genuinely transformative — it gives me assessment anchors and targeted teaching guidance that V7 completely lacked for English. The move from cluster context to text-based unit planner is the right structural decision for English, and the text type features, writing outcome, and pitfalls are all well-pitched for KS1.

The planner's biggest weakness for KS1 specifically is the absence of oral rehearsal scaffolds and cross-curricular links. These are not nice-to-haves at KS1 — they are how the subject is taught. A Y1 writing unit without oral rehearsal is pedagogically incomplete. A Y1 planner without cross-curricular connections misunderstands how the Early Years and KS1 curriculum operates in practice.

The comparison with V7 is instructive. V7 gave me the pedagogical framework (thinking lens, session structure, interaction types, feedback guidance) but no curriculum content for English. V8 gives me the curriculum content (differentiation, text features, writing outcome, genre) but no pedagogical framework. The ideal V9 planner would merge both.

For a KS1 teacher, this planner saves genuine time. It tells me what to teach, what the differentiation looks like, what features to focus on, what pitfalls to avoid, and where the unit leads next. That is the first 60-90 minutes of a 3-hour planning process. The remaining 90-120 minutes — designing the oral rehearsal, choosing the text edition, creating vocabulary displays, planning the cross-curricular links, and writing the session sequence — still falls to me.

**V7: 5.5/10 -> V8: 7.5/10.** A 2-point improvement, the largest gain of the three reviewers. The DifficultyLevel data drove most of the improvement. The next point requires oral rehearsal scaffolds, cross-curricular links, and vocabulary definitions.
