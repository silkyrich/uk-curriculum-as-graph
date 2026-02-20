# ICO Children's Code (Age Appropriate Design Code)
**Source:** https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/
**Fetched:** 2026-02-20
**Type:** regulatory code (statutory code of practice)
**Access:** web search summaries only (ICO site returned 403 on direct fetch)

## What it is

The UK's first statutory code of practice for protecting children's data online. Came into force September 2021. Created by the ICO under the Data Protection Act 2018. Applies to any online service likely to be accessed by under-18s in the UK.

It is a set of 15 flexible standards — they do not ban or specifically prescribe — that provides built-in protection ensuring that the best interests of the child are the primary consideration when designing and developing online services.

**Note:** Due to the Data (Use and Access) Act coming into law on 19 June 2025, this guidance is under review and may be subject to change.

## The 15 Standards

| # | Standard | Summary |
|---|---|---|
| 1 | Best interests of the child | Primary consideration in all design decisions |
| 2 | Data protection impact assessments | DPIA required before launch; must focus on children's rights |
| 3 | Age appropriate application | Risk-assess based on age ranges; different treatment per age band |
| 4 | Transparency | Privacy info must be understandable by children; age-appropriate language |
| 5 | Detrimental use of data | Do not use children's data in ways shown to be detrimental to wellbeing |
| 6 | Policies and community standards | Published, enforced, child-appropriate terms |
| 7 | Default settings | Highest privacy settings by default |
| 8 | Data minimisation | Only collect data child is "actively and knowingly engaged" in |
| 9 | Data sharing | Do not disclose children's data unless compelling reason |
| 10 | Geolocation | Off by default; obvious sign when active |
| 11 | Parental controls | Child notified when monitored; parental controls age-appropriate |
| 12 | Profiling | Off by default unless compelling reason; safeguards against harmful effects |
| 13 | Nudge techniques | Do not use nudges to encourage providing unnecessary data or weaken privacy |
| 14 | Connected toys and devices | Specific requirements for IoT devices used by children |
| 15 | Online tools | Easy mechanisms to exercise data rights (deletion, account removal, etc.) |

## Key principles for our platform

1. **High privacy by default**: No algorithmic curation, location tracking, or behavioural profiling by default. All must be actively opted into.
2. **Data minimisation**: Only collect what is "strictly necessary" for the service the child is actively engaged in.
3. **No nudge techniques**: No dark patterns to encourage data provision or weaken privacy.
4. **No detrimental use**: No engagement maximisation, no addictive patterns, no commercial profiling.
5. **Profiling off by default**: Must demonstrate "compelling reason" for any profiling. Must have safeguards against harmful effects.
6. **Analytics restricted**: Even service-enhancement analytics cannot be collected by default.

## Relevance to platform

This is the primary regulatory framework governing our platform. Every design decision in the adaptive learning system must be assessed against these 15 standards. The profiling standard (12) is the most challenging for us because adaptive learning inherently requires profiling — see `ico_profiling_standards.md` for detailed analysis.

## Caveats

All content derived from web search result summaries and secondary sources. The full ICO guidance pages were not directly fetched (403 errors). A manual review of the complete guidance is recommended before finalising the compliance architecture.
