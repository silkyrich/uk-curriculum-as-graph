# Gap Analysis: Ms. Oduya -- Science (KS2)
**Planner:** Friction Investigation
**Date:** February 2026 (V8 review)
**V7 score:** 6.0/10 --> **V8 score:** 7.0/10

---

## Top 5 Data Additions That Would Improve This Planner

1. **Populate misconception descriptions.** Two misconceptions are named ("Smooth surfaces have no friction" and "Friction is always unhelpful") but their description fields are empty. The concept-level misconceptions cover similar ground, but the investigation-specific misconceptions should include: what children typically say, why they think it, and how to challenge the misconception through the investigation itself. For example: "'Smooth surfaces have no friction' -- children observe that a car slides easily on a smooth surface and conclude there is zero friction. Challenge by asking: if smooth surfaces had no friction, why does the car eventually stop on the smooth surface too?"

2. **Add sequencing data.** The planner has no "Follows" or "Leads to" section. A friction investigation should sit within the Y5 Forces progression: gravity and weight first (so children understand forces as a concept), then friction and air resistance (contact forces), then mechanisms and simple machines (application). The graph has CHRONOLOGICALLY_FOLLOWS or sequencing data for HistoryStudy nodes -- the same pattern should exist for ScienceEnquiry nodes, or at minimum the domain-level cluster sequencing (SEQUENCED_AFTER) should be surfaced.

3. **Include a results table template or structure.** The planner specifies "results table" as a recording format but does not suggest column headers or structure. For a fair test with 5 surface types and repeated measurements, the template should include: Surface type | Distance (attempt 1) | Distance (attempt 2) | Distance (attempt 3) | Average distance. This is not creative work -- it is a direct derivation from the stated variables. The generator could produce it automatically from the independent variable (rows), dependent variable (columns), and a standard 3-repeats convention.

4. **Restore thinking lens data.** The V7 cluster review included a "Cause and Effect" lens with KS2 question stems: "What caused this to happen, and how do we know?" This mapped perfectly to fair test enquiry. Adding a single section with the primary lens, its key question, and 3-4 question stems would restore a proven strength. The data exists on ThinkingLens and PROMPT_FOR nodes -- the planner template simply needs to include it.

5. **Add a broader context or application section.** The planner is tightly focused on the toy car investigation but does not connect friction to the real world. A "Real-world applications" field on the ScienceEnquiry node could include: car brakes (friction is useful), ice skating (low friction surface), shoe tread design (varying friction for different purposes), bicycle brakes. This contextualises the investigation and supports the "friction is not always unhelpful" corrective to the named misconception.

---

## What the Auto-Generator Does Well

**Variables specification.** The explicit listing of independent, dependent, and controlled variables with specific examples is the highest-value addition to the Science planner format. In V7, I had to extract variables from concept teaching guidance and invent the controlled variables myself. Now the planner hands me a complete fair test specification that I could share with children directly: "We are changing the surface type. We are measuring how far the car travels. We are keeping the ramp angle, car mass, and release point the same." This single section saves 15-20 minutes of planning time.

**Equipment list with practical detail.** The list (ramp, toy car, metre stick, surface samples, masking tape) is complete and specific. The inclusion of masking tape -- needed to secure surfaces flat, a detail that many teachers discover mid-lesson -- shows that the data author has run this investigation. The surface sample list (carpet, wood, sandpaper, tile, fabric) uses materials available in any primary school, not specialist equipment.

**Safety notes proportionate to risk.** "Low risk. Ensure ramp is stable and surfaces are secured flat. Keep floor area clear." This is exactly right -- not over-cautious (which erodes credibility with experienced teachers) and not dismissive. The note about floor area and tripping is the kind of practical safety consideration that CLEAPSS would approve.

**Pitfalls are investigation-specific.** "Inconsistent release of the car on the ramp leads to unreliable data -- model a consistent release technique before starting." This is not a generic "plan carefully" statement -- it identifies the specific source of error for this specific investigation and tells the teacher what to do about it ("model a consistent release technique"). A student teacher could read this and avoid the most common Y5 friction investigation failure.

---

## What the Auto-Generator Gets Wrong

**Source document mismatch.** The SourceDocument field references the "KS2 English Grammar, Punctuation and Spelling Test Framework 2016" for a Science planner. This is the same cross-layer join error visible in the History planner. The correct source document is the KS2 Science NC programme of study.

**Empty misconception descriptions.** The "Known misconceptions" section names two misconceptions but provides no explanatory text. The format shows a name followed by a blank description (lines 94-95: "**Smooth surfaces have no friction:** " with nothing after the colon). This is likely a rendering issue where the ScienceEnquiry node has a `misconceptions` array with name-only entries, or where the ADDRESSES_MISCONCEPTION relationship points to Misconception nodes that have names but empty `description` properties. Either way, named misconceptions without explanations are of limited value.

**Empty vocabulary definitions.** Same issue as every planner: terms listed, definition cells blank. The concept-level key_vocabulary field contains 15 well-chosen terms for this topic -- the generator is not mapping them into the word mat.

**Subject field empty on cross-curricular links.** Both entries show "None" in the Subject column. The connections clearly involve English and DT. The generator is not resolving the target subject from the CROSS_CURRICULAR relationship.

**No sequencing section.** Unlike the History planner (which has Follows/Leads-to), the Science planner has no sequencing information. This is either a data gap (ScienceEnquiry nodes may not have chronological or pedagogical sequencing relationships) or a generator omission. Either way, knowing where this investigation sits in the Y5 Forces unit is essential for medium-term planning.

**Enquiry type description is generic.** The Fair Test definition ("A controlled investigation where one variable is deliberately changed...") is the same text for any fair test. A friction-specific note would be more useful: "This is a fair test because we are testing whether changing the surface causes a change in distance. The key control is the release method -- if we push the car with different forces on different surfaces, we cannot claim the surface caused the difference." The EnquiryType node likely has only a generic description; an investigation-specific application note would add value.

---

## Comparison: Hand-Written vs Auto-Generated Planner

A hand-written Science investigation plan by a subject lead would differ in several ways:

**Method steps.** A human planner would include numbered method steps: (1) Set up the ramp at 30 degrees against a table, (2) Tape the first surface sample to the floor at the base of the ramp, (3) Place the car at the top of the ramp with its front wheels on the masking tape line, (4) Release the car without pushing, (5) Measure from the base of the ramp to where the car stops, (6) Record in the results table, (7) Repeat 3 times for each surface. The auto-planner gives variables and equipment but no method. This is the single biggest gap for a Science investigation planner.

**Prediction prompt.** A human planner would include a structured prediction: "Before we start, predict: which surface do you think will make the car travel furthest? Why?" with space for children to write and draw. The auto-planner implies prediction through the enquiry question but does not structure it as a classroom activity.

**Model results and conclusion.** A human planner would include an example of what "good" results look like (approximate distances for each surface) and a model conclusion: "I found that the car travelled furthest on the tile (87 cm average) and shortest on the carpet (23 cm average). This shows that smooth surfaces produce less friction than rough surfaces. I know my test was fair because I used the same car, the same ramp angle, and the same release point every time." The auto-planner provides the expected outcome but not a model response.

**What the auto-planner does better than most human planners:** The differentiation tables are more rigorous than typical school-level planning. Most hand-written Science plans differentiate by task complexity or support level, not by conceptual progression. The auto-planner's four-tier framework (Entry through Greater Depth) describes what understanding looks like at each level, which is more useful for assessment than "Group A uses a writing frame, Group B writes independently."

---

## Verdict

This planner is a solid foundation for a Y5 friction investigation. The variables, equipment, safety, and expected outcome sections give me the practical specification I need, and the differentiation tables provide assessment structure. A Science subject lead could use this to plan the investigation in 30-40 minutes rather than the 60-90 minutes it would take from scratch.

The gap to "ready to teach" is mainly in the procedural layer: no method steps, no results table template, no model conclusion, no prediction activity. These are standard components of a Science investigation plan that could be generated algorithmically from the existing data (variables determine the table structure; expected outcome determines the model conclusion; enquiry question determines the prediction prompt).

The score improvement from V7 (6.0 to 7.0) reflects the addition of variables, equipment, and safety -- the practical elements that were entirely absent from the cluster format. The score would reach 8+ if the generator also produced method steps, restored thinking lenses, populated the misconception and vocabulary descriptions, and added sequencing context.
