# ICO Children's Code: Profiling Standards (Standards 5 and 12)
**Sources:**
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/12-profiling/
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/how-to-use-our-guidance-for-standard-one-best-interests-of-the-child/best-interests-framework/profiling-for-automated-decision-making/
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/how-to-use-our-guidance-for-standard-one-best-interests-of-the-child/best-interests-framework/profiling-for-content-delivery/
**Fetched:** 2026-02-20
**Type:** regulatory guidance
**Access:** web search summaries only (ICO direct fetch returned 403)

## What it is

The two most challenging standards for an adaptive learning platform: Standard 5 (detrimental use) and Standard 12 (profiling). These define what forms of automated processing of children's data are permitted and under what conditions.

## Standard 5: Detrimental Use of Data

"Do not use children's personal data in ways that have been shown to be detrimental to their wellbeing, or that go against industry codes of practice, other regulatory provisions or Government advice."

Requirements:
- Keep up to date with sector-specific recommendations and advice
- Do not process children's data in ways that are obviously detrimental
- Do not process in ways formally identified as requiring further research to establish whether they are detrimental

Examples of detrimental use:
- Using data to encourage prolonged engagement (addictive design)
- Behavioural advertising of prohibited products to children
- Algorithmic recommendation of harmful content based on profile

## Standard 12: Profiling

"Switch options which use profiling 'off' by default, unless you can demonstrate a compelling reason for profiling to be on by default, taking account of the best interests of the child. Only allow profiling if you have appropriate measures in place to protect the child from any harmful effects (in particular, being fed content that is detrimental to their health or wellbeing)."

### What counts as profiling

"Any form of automated processing of personal data that assesses or predicts people's behaviour, interests or characteristics." This includes:
- Content recommendation algorithms
- Behavioural analysis
- Knowledge tracing and adaptive learning (our use case)
- Service personalisation

### The compelling reason test

Profiling may be switched ON by default if the organisation can demonstrate a compelling reason, taking account of the child's best interests. Examples from ICO guidance:

- **Safeguarding**: Profiling to meet a legal or regulatory requirement
- **Accessibility**: Identifying that a child needs subtitles, signed or supported services
- **Age assurance**: Profiling to verify age
- **Core service**: Where profiling is essential to deliver the service's core function (e.g., a banking app reliant on spending data)
- **Content moderation**: Profiling to protect children from harmful content

### Differentiate profiling purposes

Services must:
- Differentiate between different types of profiling for different purposes
- Offer different privacy settings for each purpose
- NOT bundle them into one consent notice or privacy setting

### Automated decision-making (ADM)

GDPR Recital 71 states that automated decision-making "should not concern a child." The Children's Code reinforces this. However, the ICO's best interests framework for profiling for ADM acknowledges that some automated decisions may be in the child's best interests if:
- The decision serves the child's welfare
- Appropriate safeguards exist
- The processing is transparent and explainable
- There are measures to avoid bias
- The child is not exposed to harmful content as a result

### No blanket education exception for profiling

The ICO does not provide a specific exemption for "adaptive learning" or "educational profiling." However, the compelling reason framework could encompass educational profiling if:
1. It is genuinely core to the service
2. It serves the child's best interests (evidence-based pedagogy)
3. Safeguards prevent harmful effects
4. A residual service exists without profiling (even if degraded)
5. Parent can view and control the profiling

## Application to our platform

### Our compelling reason argument

1. **Core to service**: Adaptive learning cannot function without knowledge tracing. Without profiling, we are a static worksheet generator.
2. **Best interests**: Personalised instruction has effect sizes of 0.3-0.5 SD (documented in RESEARCH_BRIEFING.md). Not profiling harms educational outcomes.
3. **No harmful content exposure**: All content is curriculum-grounded. The profiling cannot recommend harmful material because the content universe is the National Curriculum.
4. **Safeguards**: Full parent transparency, one-click deletion, no competitive framing, session limits, no engagement maximisation.
5. **Residual service**: Static practice mode available if profiling consent is withdrawn.

### Unbundled consent for different profiling purposes

| Purpose | Type | Default | Consent |
|---|---|---|---|
| Knowledge tracing (mastery estimation) | Core adaptive learning | Off until consented | Required for full service |
| Error pattern detection | Pedagogical profiling | Part of core consent | Same as above |
| Spacing interval optimisation | Pedagogical profiling | Part of core consent | Same as above |
| Anomaly detection (sibling gaming) | Safety profiling | On (legitimate interests) | Cannot be disabled while service active |
| Teacher progress sharing | Data sharing | Off | Separate optional consent |
| Anonymised aggregate analytics | Research | Off | Separate optional consent |

## Upcoming education-specific guidance

The proposed education-specific code of practice would require consideration of:
- "The impact of profiling and automated decision-making on children's access to education opportunities"
- "The need for transparency and evidence of efficacy on the use of AI systems in the provision of education"

This legislation is still proposed, not enacted. But it signals regulatory direction.

## Relevance to platform

Standards 5 and 12 are the hardest compliance challenge for our platform. The compelling reason argument is defensible but has not been tested against the ICO specifically for adaptive learning. We should seek ICO sandbox engagement or legal counsel opinion before launch.

## Caveats

All ICO guidance content derived from web search summaries. The full guidance pages (particularly the best interests framework worked examples) could not be directly fetched. The nuance of worked examples may change the analysis. Manual review strongly recommended.
