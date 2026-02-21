# ICO DPIA Requirements for Children's Services (Standard 2)
**Sources:**
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/2-data-protection-impact-assessments/
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/annex-d-dpia-template/
- https://www.esrb.org/privacy-certified-blog/the-icos-age-appropriate-design-code-dpias-and-governance/
**Fetched:** 2026-02-20
**Type:** regulatory guidance
**Access:** web search summaries only (ICO direct fetch returned 403)

## What it is

Standard 2 of the Children's Code requires a Data Protection Impact Assessment (DPIA) for any online service likely to be accessed by children. The ICO provides a specific template (Annex D) and worked examples for different service types.

## When a DPIA is required

The ICO's published list of processing operations requiring a DPIA includes:
- Use of personal data of children for marketing, profiling, or automated decision-making
- Offering online services directly to children
- Innovative technology (AI, machine learning)
- Large-scale profiling
- Biometric data
- Online tracking

In practice: if you offer an online service likely to be accessed by children, you must do a DPIA. This applies to us on multiple criteria.

## DPIA timing

- Must be embedded into the design process (not a rubber stamp at the end)
- Must be completed BEFORE the service is launched
- Must be repeated for any significant changes to processing operations
- Outcomes must be able to influence the design

## What the DPIA must cover

1. **Systematic description of processing**: What data, what purposes, what flows
2. **Necessity and proportionality**: Why each data element is needed; why less intrusive alternatives won't work
3. **Risk assessment**: Risks to children's rights and freedoms, including potential for material, physical, psychological, or social harm
4. **Mitigation measures**: Technical and organisational measures for each risk
5. **Children's Code compliance**: How each of the 15 standards is met
6. **Age-specific assessment**: Different ages, capacities, and developmental needs
7. **Consultation**: DPO review, user testing, input from children's rights groups

The DPIA must have a particular focus on risks to children that arise from the specific data processing, not just generic data protection risks.

## Consultation requirements

Must consult:
- Data Protection Officer (if appointed)
- Where appropriate: individuals, relevant experts, children's rights groups
- Options: existing user feedback, public consultation, market research, user testing

This should include feedback on the child's ability to understand how their data is used.

## ICO resources

- **Annex D**: DPIA template specifically for Children's Code compliance
- **Worked examples**: Available for online retail, connected toys, mobile gaming apps
- No worked example specifically for adaptive learning platforms (gap in guidance)

## Application to our platform

We need a formal DPIA that covers:
- Core adaptive learning processing (knowledge tracing, error detection, spacing)
- LLM inference (what data enters the prompt, processor agreements)
- Camera/microphone activities (local processing claims, consent per modality)
- Anomaly detection (legitimate interests basis)
- Parent dashboard (data display, sharing controls)
- Data retention and deletion

The DPIA should follow the ICO Annex D template and be completed before any beta launch. It should be a living document updated as features change.

## Gap in current project

No formal DPIA exists yet. The privacy architecture documented in user-stories/README.md and CHILD_PROFILE_CONSENT.md provides the foundation, but it needs to be translated into the formal DPIA template structure. This is listed as a gap in CHILD_PROFILE_CONSENT.md Section 9.

## Caveats

DPIA template and worked examples could not be directly fetched from ICO (403). The Annex D template should be manually downloaded from the ICO website and used as the starting structure for our DPIA.
