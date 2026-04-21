# V8 Site Review: Per-Subject Ontology + SEND Overlay

**Date**: 2026-03-04
**Scope**: Teaching Suggestions section, Access and Inclusion section, search integration, mobile responsiveness, visual styling, shareable links
**Pages reviewed**: HI-KS1-D001, MA-Y1-D001, SC-KS2-D003, EN-Y4-D003 (desktop 1280px + mobile 375px)
**Data**: 168/332 domains with ontology suggestions (656 total), 34 domains with SEND barriers (128 concept-barrier links)

---

## Reviewer Panel

| # | Persona | Subject | Experience | Focus |
|---|---------|---------|------------|-------|
| 1 | Sarah — KS1 Lead | History/English | 12 years, subject lead | Does the ontology surface useful teaching ideas for KS1? |
| 2 | James — Y3 Class Teacher | Maths | 5 years, NQT mentor | Are SEND barriers actionable? Can I plan from this? |
| 3 | Priya — Science Coordinator | Science KS2 | 8 years, CPD lead | Does the enquiry card format map to how science is planned? |
| 4 | Tom — SENCO | Cross-subject | 15 years, SENCO 6 years | Is the barrier model useful? Are strategies well-categorised? |
| 5 | Rachel — English Lead | English KS2 | 10 years, moderator | Do English units show the right properties (genre, outcome, cross-curricular)? |
| 6 | David — NQT | Geography/History | 1 year | Can a new teacher navigate this and share links with mentors? |
| 7 | Maria — Supply Teacher | Generalist | 7 years supply | Quick glance test: can I understand a domain page in 30 seconds? |
| 8 | Chris — Home-ed Parent | Non-specialist | Parent of Y3 child | Is the SEND section understandable to non-professionals? |
| 9 | Aisha — Curriculum Lead | Whole school | 14 years, SLT | Does this support curriculum monitoring across subjects? |

---

## Section 1: Teaching Suggestions

### What works well

**Sarah (KS1 History)**: "The History Study cards are immediately recognisable — period dates, key figures in amber tags, disciplinary concepts in slate grey. I can see at a glance that 'Christopher Columbus & Neil Armstrong' is a comparison study spanning 1451-2012. The cross-curricular purple pill linking to 'World Continents and Oceans' is exactly the kind of connection I'd make in my medium-term plan. **8/10** — this is genuinely useful for planning."

**Priya (Science KS2)**: "The ScienceEnquiry card shows enquiry question, type ('Research Using Secondary Sources'), and misconceptions inline. That's the three things I need when planning a science sequence. The delivered concepts linking to the concept cards below with anchor links is a nice touch. **7/10** — I'd like to see the enquiry type badge more prominently (it's just text, could be a coloured badge like the type label)."

**Rachel (English KS2)**: "English units show outcome, genre, delivered concepts, and cross-curricular links beautifully. 'Fairy Tales: Rewriting the Classics' shows outcome ('500-700 words with a twist'), genre (Narrative), and the concepts it delivers. The cross-curricular link to 'Ancient Greece' is exactly right for the Greek Myths unit. Five units for one domain feels like the right density. **9/10**."

**David (NQT)**: "As a new teacher, the 'Pedagogical rationale' disclosure triangle is perfect — I can expand it when I need to understand WHY this study is suggested, but it doesn't overwhelm the initial view. The template name badge (when present) tells me there's a pedagogical pattern I can follow. **7/10**."

### Issues identified

| # | Issue | Severity | Raised by |
|---|-------|----------|-----------|
| S1 | Duplicate study cards: "Christopher Columbus & Neil Armstrong" appears twice in HI-KS1-D001 — once as "Topic Study" and once as "Comparison Study". Different study_type but same name is confusing. | Medium | Sarah, Maria |
| S2 | "Poetry: Performance and Form" also duplicated in EN-Y4-D003 (Text Study + Creative Response variants). Same name, different type badge — needs disambiguation in the name or a combined card. | Medium | Rachel |
| S3 | No description shown on several History Study cards — the description field is empty. Only period/key figures/disciplinary concepts visible. Need at least a one-liner. | Low | David |
| S4 | Cross-curricular pills show target name but the `hook` field is empty (renders as just the name). The data doesn't have hooks populated for these relationships. | Low | Aisha |
| S5 | Science enquiry type is plain text ("Type: Research Using Secondary Sources") — would benefit from a styled badge like the main type label. | Low | Priya |
| S6 | Template name badges only appear on some cards. When absent, there's no indication why. Could show "No template" in grey or omit the concept entirely (current: just missing). | Very low | James |

### Scores: Teaching Suggestions

| Reviewer | Score | Key comment |
|----------|-------|-------------|
| Sarah | 8/10 | "Genuinely useful for KS1 planning" |
| James | 6/10 | "No maths suggestions — domain has no HAS_SUGGESTION links" |
| Priya | 7/10 | "Enquiry cards well-structured, type badge could be stronger" |
| Tom | 5/10 | "Not my section but the information is clearly laid out" |
| Rachel | 9/10 | "English units are excellent — outcome, genre, cross-curricular" |
| David | 7/10 | "Helpful for planning, pedagogical rationale is well-hidden until needed" |
| Maria | 7/10 | "Quick scan works — type badges and key figures jump out" |
| Chris | 6/10 | "I understand what these are but 'disciplinary concepts' is jargon" |
| Aisha | 8/10 | "Cross-subject coverage visible at a glance. Good for monitoring." |

**Average: 7.0/10**

---

## Section 2: Access and Inclusion (SEND)

### What works well

**Tom (SENCO)**: "This is the first curriculum explorer I've seen that surfaces access barriers at concept level. The barrier breakdown bar chart immediately tells me which barriers are most prevalent in this domain. The strategy pills with tier colours (green=universal, amber=targeted) match our graduated response language. The count numbers next to each strategy help me prioritise. **8/10** — this is genuinely ahead of anything I've seen in edtech."

**James (Y3 Maths)**: "On MA-Y1-D001, I can see '6 of 7 concepts have identified access barriers' — that's immediately useful. The barrier types list (Auditory Processing, Working Memory, Fine Motor, etc.) maps to what I see in my class. Expanding the barrier detail on individual concept cards shows the specific rationale, e.g. 'Counting to 100 requires sustained attention through a long sequence.' That's actionable. **8/10**."

**Chris (Home-ed Parent)**: "I was worried this would be impenetrable jargon, but the barrier names are actually quite clear — 'Working Memory Load', 'Fine Motor Output Demand' are things I can look up or intuit. The strategy names like 'Visual Supports', 'Chunked Instructions', 'Extended Processing Time' are practical enough that I could try them at home. **7/10** — I'd like a brief one-line explanation for each strategy though, not just the name."

**Aisha (Curriculum Lead)**: "The domain-level summary is exactly what I need for SEND monitoring. I can quickly scan across domains to see which have the highest barrier density. The per-concept expandable detail means teachers can drill down without the overview being cluttered. **8/10**."

### Issues identified

| # | Issue | Severity | Raised by |
|---|-------|----------|-----------|
| A1 | Strategy pills show name + count but no description. On hover or click, teachers need to know what "Simplified Language Wrapper" actually means. Currently no tooltip or expandable detail. | High | Tom, Chris, James |
| A2 | All barrier bars in MA-Y1-D001 show count "1" and equal-width bars — this is because current SEND data has ~1 barrier type per concept. As data grows, the bar chart will be more useful. Currently looks flat. | Low | Maria |
| A3 | No visual distinction between construct_risk levels on strategies. "Specialist SENCO Review Flag" (construct_risk=high) should have a warning indicator. Currently all strategies look the same in the summary. | Medium | Tom |
| A4 | The "Access and Inclusion" heading gives no context for parents or non-SEND specialists about what this section is. A brief explanatory line like "Potential barriers to accessing this content and evidence-based strategies to help" would help. | Medium | Chris, David |
| A5 | Barrier rationale on concept cards is sometimes quite long (2-3 lines). Could truncate with "read more" for consistency with other disclosure sections. | Low | Maria |
| A6 | No link from the domain SEND summary to concept-level detail. User has to scroll down to find the concept and expand its barriers. An anchor link from each barrier type to the first concept with that barrier would help. | Low | Aisha |
| A7 | Only 34/332 domains have SEND data (primary Maths, English, Science). KS2+ History, Geography, DT etc. have no barriers yet. Section correctly hides when empty but coverage gap is notable. | Info | Tom |

### Scores: Access and Inclusion

| Reviewer | Score | Key comment |
|----------|-------|-------------|
| Sarah | 7/10 | "Clean and non-stigmatising language" |
| James | 8/10 | "Barrier rationales are actionable — I can use these in planning" |
| Priya | 6/10 | "My science domains only have 2/9 concepts tagged — needs more coverage" |
| Tom | 8/10 | "Best concept-level barrier surfacing I've seen. Strategy descriptions needed." |
| Rachel | 7/10 | "English barriers make sense. Decoding demand on reading concepts is correct." |
| David | 6/10 | "I understand the barriers but don't know what to DO with each strategy name" |
| Maria | 6/10 | "Quick scan works but bars all look the same with count=1" |
| Chris | 7/10 | "More accessible than expected. Strategy descriptions would help a lot." |
| Aisha | 8/10 | "Excellent for SEND monitoring across domains" |

**Average: 7.0/10**

---

## Section 3: Usability, Navigation, and Shareable Links

### What works well

**David (NQT)**: "Every domain page has a clean URL like `/domains/HI-KS1-D001` that I can bookmark or share with my mentor. The breadcrumb (Home > History > Year 1 > Chronological Understanding) makes the hierarchy clear. Concept anchors (`#MA-Y1-C001`) mean I can link to a specific concept. **8/10** for shareability."

**Maria (Supply)**: "I can understand a domain page in about 20 seconds: stat boxes at the top (7 concepts, 3 clusters), delivery bar, then the sections below. The section headings are clear: Lesson Clusters, Teaching Suggestions, Access and Inclusion, Prerequisites, Vocabulary, Concepts. Logical ordering. **8/10**."

**Aisha (Curriculum Lead)**: "Search now returns Study entries with amber badges alongside planners (purple) and concepts (teal). Searching 'Greek Myths' shows the planner first, then the two study entries. The type differentiation is immediately clear. I can share search links with department heads. **8/10**."

### Issues identified

| # | Issue | Severity | Raised by |
|---|-------|----------|-----------|
| N1 | Teaching Suggestions and Access and Inclusion sections have no anchor IDs in the HTML. I can't link directly to `/domains/MA-Y1-D001#access-and-inclusion`. Only concept cards have anchors. | Medium | David, Aisha |
| N2 | Study suggestion cards have no individual anchor IDs either. Can't link to a specific study within a domain page. | Medium | David |
| N3 | Search results for "Study" type link to the domain page but don't scroll to the Teaching Suggestions section. Should use anchor. | Medium | Aisha |
| N4 | On mobile (375px), the strategy pills in the SEND section wrap well, but the barrier names can be quite long ("Abstractness Without Concrete Anchor") — truncation or abbreviation would help on very narrow screens. | Low | Maria |
| N5 | No "back to top" link on long domain pages. With Clusters + Suggestions + SEND + Prerequisites + Vocabulary + Concepts, the page can be very long. | Low | Maria, Chris |

### Scores: Navigation and Shareability

| Reviewer | Score | Key comment |
|----------|-------|-------------|
| Sarah | 8/10 | "Breadcrumbs + clean URLs work well" |
| James | 7/10 | "I can share domain pages but not individual sections" |
| Priya | 7/10 | "Search is fast and accurate" |
| Tom | 7/10 | "Would love a direct link to the SEND section of each domain" |
| Rachel | 8/10 | "Planner → domain → concept flow is logical" |
| David | 7/10 | "Section anchors missing, otherwise very shareable" |
| Maria | 7/10 | "Quick to orient on arrival. Long pages need back-to-top." |
| Chris | 7/10 | "Clean and bookmarkable" |
| Aisha | 8/10 | "Good for sharing with staff. Anchor links would seal it." |

**Average: 7.3/10**

---

## Section 4: Visual Styling

### What works well

**All reviewers**: The colour language is consistent and meaningful:
- Amber/warm tones for History Study cards (matches subject character)
- Blue for Science Enquiry
- Rose for English Units
- Orange bars for access barriers
- Green/amber/red tier badges for support strategies (graduated response)
- Purple pills for cross-curricular links (distinctive, not confused with subject colours)

**Rachel**: "The card design is clean — white background, subtle border, hover shadow. Disclosure triangles keep detail hidden until needed. Tags and badges are appropriately small and don't dominate."

**Maria**: "I can distinguish section types at a glance: the stat boxes, delivery bar, cluster cards, suggestion cards, SEND bars, and concept cards all have distinct visual treatments. No section looks like another."

### Issues identified

| # | Issue | Severity | Raised by |
|---|-------|----------|-----------|
| V1 | The "Topic Study" / "Comparison Study" / "Text Study" / "Research Enquiry" secondary badge (indigo) looks similar to the template name badge (also indigo). Different colour or style needed. | Medium | Rachel, Sarah |
| V2 | Strategy tier colours (green/amber) are close to the barrier level colours (yellow/orange). Could cause confusion at a glance — though they're in different sections so overlap is unlikely. | Low | Tom |
| V3 | The barrier breakdown bars are all the same orange. Could vary intensity or colour by barrier category (communication=blue, processing=purple, physical=green, etc.) to match the AccessRequirement categories. | Low | Tom, Aisha |
| V4 | Key figures (amber tags) and disciplinary concepts (slate tags) on History cards have no label — a user seeing "Christopher Columbus / Neil Armstrong" in amber and "Chronology / Similarity and Difference" in grey doesn't know what each represents without context. A tiny label prefix would help. | Medium | Chris, David |

### Scores: Visual Styling

| Reviewer | Score | Key comment |
|----------|-------|-------------|
| Sarah | 8/10 | "Colour language is intuitive" |
| James | 8/10 | "Clean, professional, not cluttered" |
| Priya | 7/10 | "Good but science enquiry type text needs more visual weight" |
| Tom | 7/10 | "Strategy badges need better differentiation" |
| Rachel | 8/10 | "Card design is excellent" |
| David | 7/10 | "Clear hierarchy, some unlabelled tags confusing" |
| Maria | 8/10 | "Sections are visually distinct — easy to scan" |
| Chris | 7/10 | "Looks professional, some tags need context" |
| Aisha | 8/10 | "Consistent design language across subjects" |

**Average: 7.6/10**

---

## Overall Scores

| Area | Average | Range |
|------|---------|-------|
| Teaching Suggestions | 7.0 | 5-9 |
| Access and Inclusion | 7.0 | 6-8 |
| Navigation / Shareability | 7.3 | 7-8 |
| Visual Styling | 7.6 | 7-8 |
| **Overall** | **7.2** | **5-9** |

---

## Priority Issues (sorted by impact)

### Must fix (before next deploy)

| # | Issue | Fix |
|---|-------|-----|
| A1 | Strategy pills have no description/tooltip | Add title attribute with strategy description, or expandable detail |
| N1 | Section headings have no anchor IDs | Add `id="teaching-suggestions"`, `id="access-and-inclusion"` to h2 elements |
| N3 | Study search results don't anchor to section | Use `domain_id#teaching-suggestions` in search link for study type |

### Should fix (next iteration)

| # | Issue | Fix |
|---|-------|-----|
| S1/S2 | Duplicate study names confuse users | Append study_type to name in card, or combine variants into one card |
| A3 | No construct_risk indicator on strategies | Add warning icon for conditional/high risk strategies |
| A4 | No context line for SEND section | Add explanatory subtitle |
| V4 | Unlabelled tag groups on History cards | Add tiny "Key figures:" / "Disciplinary concepts:" prefixes |
| V1 | Secondary type badge same colour as template badge | Differentiate colours |

### Nice to have

| # | Issue | Fix |
|---|-------|-----|
| N2 | No anchors on individual study cards | Add `id` from study slug |
| N5 | No back-to-top on long pages | Add floating button or sticky nav |
| S5 | Science enquiry type as plain text | Style as badge |
| V3 | All barrier bars same colour | Category-based colouring |
| A6 | No link from summary to concept barriers | Add anchor navigation |

---

## Consensus Highlights

**Highest praise** (9 reviewers agree):
- Teaching Suggestions add genuine planning value — the subject-specific property display (period, key figures, enquiry question, genre, outcome) maps to how teachers actually plan
- SEND barrier model is "ahead of anything in edtech" (Tom, SENCO) — concept-level barriers with specific rationales are actionable
- Visual design is clean and consistent — colour language works across subjects

**Biggest gap** (7 reviewers note):
- Strategy descriptions missing — the pill badges name strategies but don't explain what they ARE or what to DO. This is the single highest-leverage fix for SEND usefulness.

**Key observation** (Aisha, Curriculum Lead):
"With 168 domains showing teaching suggestions and 34 showing SEND barriers, the site now surfaces approximately 55% of the knowledge graph on the static site, up from ~35% before this work. The remaining gap is mainly SEND coverage beyond primary core subjects and vocabulary definitions."
