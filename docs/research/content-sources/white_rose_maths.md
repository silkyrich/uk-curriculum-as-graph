# White Rose Maths — Content Source Research
**Source:** https://whiteroseeducation.com/
**Researched:** 2026-02-17
**Type:** No API; mixed free/paid content with URL-based scheme structure
**Access:** Free (schemes of learning, some worksheets); paid (slides, assessments, videos)

## What it is
White Rose Maths (White Rose Education) is the dominant structured maths scheme used in English primary schools. Their Scheme of Learning organises maths into Blocks (topics) per year group per term. Extremely well-aligned to NC and widely understood by UK primary teachers. Not-for-profit organisation based in Bradford.

## No API
No public API. Content available via website portal and PDF downloads. Premium content requires subscription (£30–£72/year).

## Content hierarchy and identifiers
```
Year Group → Term (Autumn/Spring/Summer) → Block (numbered 1–6) → Small Step
```
URL/file pattern: `Y{year}_{term}_Block_{number}_{topic}`
- Example: `Y3_Autumn_Block_1_Place_value`
- Example: `Y4_Spring_Block_2_Multiplication_and_division`

Small Steps within blocks (individual learning objectives) do not have stable URL identifiers.

## Licensing
- Schemes of Learning (curriculum plans): free download, not openly licensed
- Teaching slides, assessments, videos: paid subscription, proprietary
- Not compatible with OGL or CC licensing — cannot be embedded in a commercial platform

## What we derived from this
1. White Rose Block references are widely understood by UK primary teachers — adding them to Domain nodes as reference metadata has teacher-facing value even without API access
2. Block-level mapping to our Domain nodes is straightforward: `Y3_Autumn_Block_1` → `MA-Y3-D001` (Place Value)
3. No programmatic content pull possible
4. Small Step granularity (closest to our Concept nodes) has no stable identifiers
5. The White Rose teaching sequence is a useful independent validation of our prerequisite ordering, as it is empirically validated across thousands of schools

## Caveats
- No API — reference codes only
- Paid content cannot be embedded or reproduced
- Block-level only; no stable identifiers at concept granularity
- Would need to be included as metadata only, not a content source
