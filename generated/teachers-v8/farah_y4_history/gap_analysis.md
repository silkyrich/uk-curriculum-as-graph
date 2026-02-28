# Gap Analysis: HI-KS2-D004-CL001 — Y4 History (Cause, Consequence, Significance)

**Reviewer**: Ms. Farah — Y4 History specialist, 12 years' experience
**V7 score**: 5.5/10
**V8 score**: 7.5/10

---

## Overall Assessment

This is a genuinely useful context document for planning a disciplinary history lesson. The combination of DifficultyLevel tiers, Subject Reference nodes (HistoricalSource + DisciplinaryConcept), and VehicleTemplate agent prompts means I could plan a complete lesson from this document without having to invent the pedagogical structure from scratch. That is a meaningful step forward from V7, where I had concepts and difficulty levels but no sources, no disciplinary framework, and no pedagogical template.

The score moves from 5.5 to 7.5 -- a significant jump, but still not where it needs to be. The reasons are detailed below.

---

## Section-by-Section Evaluation

### Overview
**Sufficient.** The cluster identification, domain name, pedagogical rationale, and thinking lens recommendations were all clear and usable. The rationale for co-teaching Cause and Consequence with Significance is exactly right -- this is how I would plan it.

**Problem**: "Estimated teaching time: None lessons (~None weeks)" and "Year group: Y4 (None)" -- these None values are clearly bugs in the query. Not a content problem, but it looks unfinished and would confuse a less experienced teacher.

### Thinking Lenses
**Good.** Cause and Effect as primary lens, Evidence and Argument as secondary -- both are well chosen. The rationale for each is specific to *this cluster*, not generic. The question stems were directly usable in my lesson plan ("What caused this to happen? Is there more than one reason?"). The AI instruction for the Cause and Effect lens gave useful pedagogical structure ("prompt pupils to suggest reasons and test predictions... use 'if...then...because' structure").

**Minor issue**: The Cause and Effect AI instruction includes "encourage designing simple fair tests to check causal claims" -- this is science language, not history language. In history, you cannot design a fair test; you evaluate evidence and construct an argument. The age-banded prompt should be subject-aware, not a generic thinking-skills prompt. This is a small but telling gap.

### Prerequisite Knowledge
**Sufficient.** The prerequisites (Time and Chronology, Change and Continuity, Historical Sources and Evidence, Historical Evidence and Interpretation) are correct. Knowing that pupils should already have KS1 source skills and chronological understanding is useful for pitching the lesson.

**Missing**: No indication of what "secure" looks like at the prerequisite level. Do they need to be at Expected on KS1 chronology, or is Entry sufficient? Without this, I have to guess.

### Concepts (Cause and Consequence + Significance)
**Very good.** This was already strong in V7 and remains the best section. The concept descriptions are detailed, accurate, and clearly written by someone who understands disciplinary history. The teaching guidance is genuinely useful -- "use 'because' and 'therefore' to structure causal arguments" and "give pupils a range of possible causes and ask them to rank or categorise them" are exactly what I would advise a trainee teacher.

Key vocabulary lists are comprehensive and appropriate for Y4. Common misconceptions are specific and actionable (e.g., "pupils often identify single causes for complex historical events" -- yes, this is the number one issue at this age).

### Difficulty Levels
**Very good.** The four tiers (Entry through Greater Depth) are well grounded in specific, assessable tasks. The example tasks use real historical content (Romans, Anglo-Saxons, Vikings) that would actually be taught in Y4. The progression from "identify a single cause from options" to "evaluate relative importance and argue with evidence" is a genuine disciplinary progression, not just a Bloom's taxonomy ladder bolted onto history.

I used these directly as my success criteria without modification. That is the test of whether they work.

**One issue**: The example tasks reference specific historical content (e.g., "Why did the Anglo-Saxons settle in Britain?") that assumes a particular teaching sequence. If a school teaches Ancient Egypt before Anglo-Saxons, the examples do not transfer. The tiers themselves are fine -- but the examples should be flagged as illustrative, or there should be examples for multiple topic contexts.

### Topic Suggestions
**Sufficient but overwhelming.** There are 14 topic suggestions, all delivering both HI-KS2-C001 and HI-KS2-C002. This is correct -- cause and consequence and significance are second-order concepts that run through every historical topic. But the context document does not help me choose between them for this specific lesson.

**What I needed**: A recommended teaching sequence. The curriculum says "Roman Britain before Anglo-Saxons before Vikings" but gives schools choice on which ancient civilisation to study. The context should indicate which topics are mandatory (5 are: Stone Age, Roman Britain, Anglo-Saxons, Vikings, Ancient Greece, Local History, British History Beyond 1066) vs. menu choices (Ancient Egypt OR Sumer OR Indus Valley OR Shang OR Mayan OR Islamic Civilisation OR Benin). This information is partially in the rationale text but not surfaced as structured data.

**What I also needed**: Specific guidance on *which* topic is best for introducing cause and consequence as a disciplinary concept for the first time. Roman Britain is the obvious choice (it is referenced in the DifficultyLevel examples), but the context does not make this recommendation explicit.

### Subject Reference Nodes (NEW in V8)
**This is the biggest improvement.** In V7, I had concepts but no historical sources and no disciplinary framework. I had to invent every source and every disciplinary connection myself.

Now I have:
- **DisciplinaryConcept nodes** (Cause and Consequence, Change and Continuity, Evidence and Interpretation, Significance, Similarity and Difference, Chronology) with proper definitions that read like they were written by a history education academic. The description of Evidence and Interpretation -- "Different historians can reach different conclusions from the same evidence because they ask different questions, use different frameworks, or weigh evidence differently" -- is exactly how I would teach it.
- **HistoricalSource nodes** (Vindolanda Tablets, Roman Coins, Hadrian's Wall, Sutton Hoo, Bayeux Tapestry, Benin Bronzes, Rosetta Stone, etc.) attached to specific topic suggestions via USES_SOURCE relationships.

**What works well**: The sources are real, canonical, and well-chosen. The Vindolanda Tablets for Roman Britain, the Sutton Hoo Ship Burial for Anglo-Saxons, the Oracle Bones for the Shang Dynasty -- these are the sources I would choose myself. Having them pre-mapped to topics saves genuine planning time.

**What is missing**:
1. **No source descriptions.** The HistoricalSource nodes only have names. "Vindolanda Tablets" is listed but there is no description of what they are, what they contain, what period they come from, what they reveal, or why they are useful for teaching cause and consequence specifically. I had to supply all of this from my own knowledge. A less experienced teacher would be stuck.
2. **No source images or links.** Even a URL to a museum catalogue entry or a rights-free image would transform the usefulness of these nodes.
3. **No source-to-concept mapping.** The USES_SOURCE relationship connects a HistoricalSource to a HistoryStudy, but there is no indication of *which disciplinary concept* the source is best for. The Vindolanda Tablets are excellent for Evidence and Interpretation (personal letter, low bias) but less useful for Significance. This mapping would be enormously valuable.
4. **The DisciplinaryConcept descriptions are repeated verbatim** across every topic suggestion. The description of "Cause and Consequence" appears 9 times in the Subject Reference section with identical text. This is not useful -- I need to read it once, then I need to know *how it applies to each specific topic*. The FOREGROUNDS relationship should carry a per-topic rationale (e.g., "Roman Britain foregrounds Cause and Consequence because the invasion has well-documented multiple causes that are accessible to Y4 pupils").

### Vehicle Templates (NEW in V8)
**Useful.** Four templates are provided: Topic Study, Source Enquiry, Comparison Study, and Discussion and Debate. The agent prompts are well written and give a genuine pedagogical structure.

**What works well**: The Source Enquiry template -- "present 2-3 carefully selected historical sources with clear context about when and why each was made" -- is exactly right for disciplinary history. It foregrounds provenance and cross-referencing, which are the core skills. I used this template directly in my lesson plan.

**What is missing**:
1. **No guidance on which template to use for which concept.** Source Enquiry is ideal for Evidence and Interpretation; Discussion and Debate is ideal for Significance (contested judgements). The templates are listed generically against the topic suggestions but there is no recommendation linking template to disciplinary concept.
2. **No age-banding on the templates.** The agent prompt for Source Enquiry says "present 2-3 carefully selected historical sources" -- but for Y1-Y2, you would use one source; for Y4, 2-3 is right; for Y6, you might use 4-5 with contradictory evidence. The TEMPLATE_FOR relationship goes to KeyStage, but the prompts themselves do not appear age-differentiated in this context output.
3. **No example lesson structure.** The templates describe *what* to do but not *how long each phase takes* or *how to sequence them*. A "Source Enquiry" template should specify: context-setting (5 mins), source description (5 mins), source questioning (10 mins), cross-referencing (5 mins), interpretation (10 mins). I had to build this structure myself.

### Cross-Curricular Links (NEW in V8)
**Genuinely useful and well done.** 26 cross-curricular links across all 14 topic suggestions, connecting to Geography, English, Art, DT, and RE. Each has a specific hook that makes the connection pedagogically meaningful rather than tokenistic.

**Highlights**:
- "Roman Britain --> Spelling and Vocabulary: Word Detective [strong]: Latin roots in English vocabulary" -- I used this directly in my lesson plan. It is a real cross-curricular connection that enriches both subjects.
- "Anglo-Saxon and Scots Settlement --> Traditional Tales: Myths from Around the World [strong]: Anglo-Saxon poetry and riddles; Beowulf as a literary text" -- this is exactly how good primary schools plan their curriculum.
- "Benin --> Discussion and Debate: Should Animals Be Kept in Zoos? [strong]: Discussion and debate about whether the Benin Bronzes should be returned to Nigeria" -- the Benin Bronzes repatriation debate is one of the most powerful cross-curricular opportunities in the primary curriculum. The fact that it is connected to a Discussion and Debate English unit is intelligent.

**What is missing**:
1. **Strength ratings are not explained.** Links are tagged [strong] or [moderate] but there is no rubric for what this means. Does "strong" mean the connection is deep and could sustain a full cross-curricular unit? Does "moderate" mean it is a passing reference? Without this, the ratings are not actionable.
2. **No sequencing guidance.** If I am teaching Roman Britain in Autumn 1 and the English unit on Word Detective is in Spring 2, the cross-curricular link is useless in practice. The hooks are good but they assume simultaneous teaching. Medium-term planning alignment is the missing piece.

### Learner Profile
**Good.** Content guidelines (300-500L Lexile, FK grade 3, 18-word max sentence length), pedagogy profile (productive failure sequence, 15-25 min sessions, spacing 2-10 days), feedback profile (elaborated competence, respectful and precise), and interaction types are all detailed and well-specified.

The feedback examples are particularly good: "Your inference was correct -- the text never said the character was nervous, but you worked it out from the clues" is exactly the kind of precise, respectful feedback that builds disciplinary thinking.

**Issue**: The interaction types are generic across all subjects. "Area Model (Grid/Array for Multiplication)" and "Bus Stop Division" appear in the secondary interaction types for a History lesson. These are clearly from the Maths learner profile leaking into the History context. The query should filter interaction types by subject relevance, or the learner profile should be subject-aware.

---

## NEW: Subject References Quality

**Score: 6/10**

The DisciplinaryConcept nodes are excellent in concept -- having a formal definition of "Cause and Consequence" as a disciplinary concept, separate from the substantive concept content, is exactly what disciplinary history teaching requires. This did not exist in V7 and it is a meaningful addition.

The HistoricalSource nodes are a good start but critically incomplete. Source names without descriptions, provenance, or pedagogical notes are like giving a teacher a reading list with titles but no author, date, or synopsis. I know what Vindolanda Tablets are because I have been teaching for 12 years. An NQT would not.

The FOREGROUNDS relationship is the right abstraction -- connecting a study to the disciplinary concepts it develops -- but it needs a per-topic rationale rather than the same definition repeated 9 times.

---

## NEW: VehicleTemplate Quality

**Score: 7/10**

The templates are well conceived and the agent prompts are genuinely useful. Source Enquiry and Discussion and Debate are the two templates I use most in my teaching, and their descriptions accurately capture good disciplinary practice.

The gap is in specificity: the templates are general-purpose pedagogical patterns, not history-specific lesson structures. A Source Enquiry in History (interrogating provenance, cross-referencing, constructing interpretation) is fundamentally different from a Source Enquiry in Science (fair testing, variables, reliability of measurement). The template descriptions are closer to generic enquiry-based learning than to disciplinary history methodology.

---

## NEW: Cross-Curricular Links Quality

**Score: 8/10**

This is the strongest new addition. The links are specific, pedagogically meaningful, and cover a good range of subjects. The hook descriptions are detailed enough to use directly in planning. The connection between Benin and the repatriation debate, Anglo-Saxons and Beowulf, and Roman Britain and Latin vocabulary are all links I make in my own teaching.

The missing piece is practical: sequencing and timetabling. A cross-curricular link is only useful if both subjects are being taught at the same time, and this context gives no indication of when that might be.

---

## Comparison to V7

| Aspect | V7 (5.5/10) | V8 (7.5/10) | Change |
|---|---|---|---|
| Concepts + DifficultyLevels | Strong | Strong (unchanged) | -- |
| Historical Sources | None | Named but undescribed | +1.0 |
| Disciplinary Concepts | None (implicit in concept descriptions) | Explicit DisciplinaryConcept nodes with definitions | +0.5 |
| Pedagogical Templates | None -- I had to invent lesson structure | VehicleTemplate with agent prompts | +0.5 |
| Cross-Curricular Links | None | 26 links with specific hooks | +0.5 |
| Topic Suggestions | Basic list | Detailed rationales + source/concept mappings | +0.5 (partially offset by overwhelming volume) |
| Thinking Lenses | Present in V7 | Unchanged | -- |
| Learner Profile | Present in V7 | Unchanged | -- |

**Net improvement: +2.0 points (5.5 --> 7.5)**

The biggest single improvement is the existence of Subject Reference nodes at all. Having HistoricalSource names and DisciplinaryConcept definitions means the context now speaks the language of disciplinary history, which it did not before. The VehicleTemplates give me a starting pedagogical structure rather than a blank page. The cross-curricular links are genuinely useful for medium-term planning.

---

## Remaining Gaps: What Would Take This to 9/10

1. **HistoricalSource descriptions and provenance.** Each source node needs: a 2-3 sentence description, approximate date, what it reveals, what its limitations are, and ideally which disciplinary concepts it is best for teaching. This is the single highest-leverage improvement remaining.

2. **Source-to-DisciplinaryConcept mapping.** The FOREGROUNDS relationship connects studies to disciplinary concepts, but I need to know which *sources* are best for which *concepts*. "Vindolanda Tablets are best for Evidence and Interpretation; Roman Coins are best for Cause and Consequence (propaganda/motivation)."

3. **Per-topic FOREGROUNDS rationale.** The DisciplinaryConcept description should appear once. Each FOREGROUNDS relationship should carry a short rationale explaining why *this study* foregrounds *this concept* -- e.g., "Roman Britain foregrounds Cause and Consequence because the invasion has multiple, well-documented causes that are accessible to KS2 pupils and the sources allow genuine evidence-based reasoning about motivation."

4. **Recommended topic for first teaching of each concept.** The context offers 14 topics that all deliver Cause and Consequence. It should indicate which is best for *introducing* the concept (Roman Britain, because of the DifficultyLevel examples) versus *practising* it (Vikings, which adds the complication of multiple perspectives).

5. **Age-differentiated VehicleTemplate prompts.** The templates should specify different expectations by year group. A Y2 Source Enquiry is not the same as a Y4 Source Enquiry.

6. **Subject-filtered interaction types.** Remove Maths-specific interaction types from History lesson contexts. Add history-specific ones if they exist (e.g., timeline drag-to-reorder, source annotation).

7. **Fix the None values.** "Estimated teaching time: None lessons" and "Year group: Y4 (None)" are bugs, not content gaps, but they undermine confidence in the document.

8. **Enquiry question bank.** For each cluster, suggest 2-3 enquiry questions that could drive a teaching sequence. History teaching in England is structured around enquiry questions ("Why did the Romans invade Britain?" / "Were the Vikings just raiders?"). The context provides concepts and sources but not the organising questions that tie them together.

---

## Summary

V8 is a genuine step forward. The context now contains the raw materials for a disciplinary history lesson -- concepts, difficulty tiers, sources, disciplinary frameworks, pedagogical templates, and cross-curricular links. In V7, I had to invent three of those six. In V8, I had to flesh out the detail on sources and adapt the templates, but the skeleton was there.

The remaining gap is depth, not breadth. The system now knows *what* to include in a history context; it just needs richer descriptions on the HistoricalSource nodes and smarter mappings between sources, disciplinary concepts, and pedagogical templates. When those are in place, this will be a tool I would genuinely use for planning.
