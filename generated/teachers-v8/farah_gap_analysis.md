# Gap Analysis: Ms. Farah -- History (KS2)
**Planner:** Roman Britain
**Date:** February 2026 (V8 review)
**V7 score:** 5.5/10 --> **V8 score:** 7.5/10

---

## Top 5 Data Additions That Would Improve This Planner

1. **Populate vocabulary definitions.** The word mat lists 9 terms but every definition is blank. The graph stores key_vocabulary at the concept level (16 terms with contextual descriptions in the concept text) and the HistoryStudy node presumably has vocabulary data. The auto-generator needs to map these into the word mat table. This is the simplest fix on this list -- the data exists, it just is not being rendered.

2. **Add a lesson-by-lesson sequence skeleton.** The planner says "12 lessons" but provides no breakdown. Even a minimal structure would help: which enquiry question drives which lessons, which sources are used when, which concepts are introduced in which order. The graph has CHRONOLOGICALLY_FOLLOWS relationships between HistoryStudy nodes, and the disciplinary concepts table implicitly suggests a sequence (Cause first, then Evidence, then Significance as summative). Generating a skeleton sequence from this data is tractable.

3. **Include thinking lens data.** The V7 cluster review surfaced ThinkingLens nodes with age-banded KS2 prompts and question stems. The planner format has dropped these entirely. Adding a "Thinking lens" section that shows the primary lens (Cause and Effect), its key question, and its KS2 question stems would restore one of the system's proven strengths without any new data generation.

4. **Provide simplified source extracts or transcripts.** The Vindolanda tablet section names specific tablets (Claudia Severa's birthday invitation, the warm socks request) but does not include the text. A 2-3 sentence simplified transcript of each named tablet, stored as a property on the HistoricalSource node, would close the biggest practical gap for classroom use. These are public-domain texts available from the Vindolanda Trust -- the simplification is the value-add.

5. **Fix the source document field.** The header references "KS2 English Grammar, Punctuation and Spelling Test Framework 2016" for a History planner. This is a data join error in the auto-generator. The correct source document should be the National Curriculum History programme of study. This fix requires debugging the generator's document lookup, not adding new data.

---

## What the Auto-Generator Does Well

**Source pedagogy framing.** The "How to use" field on each primary source is the planner's standout feature. Rather than just naming "Vindolanda tablets", it says: "Read a simplified Vindolanda tablet (e.g. the birthday invitation from Claudia Severa). Ask: 'What does this tell us about daily life for a Roman soldier?' Then: 'These are personal letters. How is this different from an official Roman record?'" This is teaching guidance that a non-specialist could follow. It bridges the gap between "source exists" and "source is used in a classroom" that I flagged as the critical gap in V7.

**Disciplinary concept integration.** The table connecting four disciplinary concepts to their roles in this specific study is not generic -- it is tailored. "At KS2, identify multiple causes of the Roman invasion (trade, resources, prestige, military ambition) and rank them" is actionable guidance for this study, not a definition of "Cause and Consequence" in the abstract.

**Perspectives and sensitivity.** Including "enslaved person" alongside Roman coloniser, Briton, and Roman soldier shows that the data authors have engaged with current thinking about KS2 History teaching. The pitfalls section ("presenting the Romans as unambiguously civilising") and sensitivity notes (slavery, conquest violence) are appropriate and reflect a curriculum-literate perspective.

**DifficultyLevel tables for History concepts.** In V7, I rated success criteria 5/10 because there were no differentiation tiers for History and I had to invent everything. Now I have four tiers per concept with specific descriptors and common errors. The "Greater Depth" tier for Historical Evidence ("evaluating the reliability and utility of sources for answering specific historical questions") is calibrated correctly for high-attaining Y4 pupils. This alone accounts for most of the score increase.

---

## What the Auto-Generator Gets Wrong

**Source document mismatch.** The SourceDocument field links to the English GPS test framework rather than the History programme of study. This is clearly a bug in how the generator resolves source_document relationships -- it appears to be pulling the wrong SourceDocument node, possibly matching on KeyStage rather than Subject. The field should reference the History NC document.

**Empty trailing commas on source types.** Each primary source entry has a format like "Built Heritage, " with a trailing comma and blank space (line 93: "Hadrian's Wall (Built Heritage, )"). This suggests a second property (perhaps era or date_range) exists in the schema but is null for these records. The generator should suppress trailing commas when the second field is empty.

**Subject field empty on cross-curricular links.** All three cross-curricular entries show "None" in the Subject column, despite the connections clearly involving Geography, English, and DT. The CROSS_CURRICULAR relationship presumably stores the target subject somewhere -- the generator is not resolving it.

**Missing definitions in vocabulary word mat.** Nine terms listed, zero definitions provided. The concept-level key_vocabulary fields contain these terms with implicit definitions in the surrounding text. The generator either cannot extract definitions from concept descriptions, or the HistoryStudy node lacks a vocabulary_definitions property. Either way, a word mat with empty cells is worse than omitting the section.

**No thinking lenses section.** This is a design choice in the planner format rather than a data error, but it results in losing one of the system's most praised features. The ThinkingLens + APPLIES_LENS + PROMPT_FOR data exists in the graph; the planner template simply does not include a section for it.

---

## Comparison: Hand-Written vs Auto-Generated Planner

A hand-written planner by a History subject lead would differ in several ways:

**Lesson-by-lesson narrative.** A subject specialist would structure this as a journey: "Lesson 1 -- Who were the Romans? Timeline and context. Lesson 2 -- Why did they invade? Cause sorting activity with cards. Lesson 3 -- What happened when the Romans arrived? Boudicca drama. Lessons 4-5 -- Vindolanda tablets source work..." The auto-generated planner provides ingredients without a recipe.

**Activity descriptions.** A human planner would include specific activities: hot-seating as Boudicca, a "Diamond 9" ranking of causes, a walking debate on significance, a freeze-frame dramatisation of the invasion. The auto-planner has none. It assumes the teacher will design activities.

**Simplified source materials.** A human planner would include (or link to) photocopiable source extracts at the appropriate reading level. The auto-planner names the sources and suggests how to use them, but the artefacts themselves remain the teacher's responsibility.

**Assessment design.** A human planner would include a summative assessment task -- typically a piece of extended writing ("Write a letter from a Roman soldier explaining why you are in Britain and what life is like") or a structured argument ("Was the Roman invasion good or bad for Britain?"). The auto-planner provides differentiation descriptors but no assessment tasks.

**What the auto-planner does better than most human planners:** The historiographical debate section, the explicit listing of perspectives to include, and the structured mapping of disciplinary concepts to their role in this specific study. Many commercial schemes do not include this level of disciplinary rigour. The auto-planner also provides prerequisite information (follows/leads-to) that most hand-written planners omit.

---

## Verdict

This planner is a substantial and usable starting point for planning a Roman Britain study. A History specialist with 3+ years' experience could use it as the backbone of a medium-term plan, adding their own activities, simplified sources, and lesson-by-lesson structure. The disciplinary concepts, perspectives, source guidance, and differentiation tables are all at a professional standard.

The gap to "scheme of work" quality is mainly in the production layer: no lesson sequence, no simplified source artefacts, no activities, no assessment tasks, no vocabulary definitions. These are solvable -- several (vocabulary, thinking lenses, lesson skeleton) by improving the auto-generator, and others (source extracts, activities) by adding new data to the graph.

For a non-specialist teaching History for the first time, this planner would be helpful but insufficient on its own. They would struggle to move from "disciplinary concepts" to "what do I do on Monday morning" without additional support. For a specialist, it is a strong planning aid that saves significant time on the curriculum-intelligence layer while leaving the creative-pedagogical layer to the teacher.
