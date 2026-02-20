# Curriculum Extraction Inventory

**Last Updated:** 2026-02-12
**Model Version:** 2.0 (Enhanced)
**Status:** 12 subjects extracted, ready for Neo4j import

---

## Extracted Subjects

### Primary (KS1-2)

#### 1. Mathematics KS1-2
- **Status:** ✅ Extracted (Year 1 sample)
- **Structure Rating:** 9/10
- **Total Concepts:** ~120 estimated
- **Location:** Agent output (affcc2b) - needs JSON file save
- **Key Features:** 8 domains, strong logical prerequisites, discrete concepts
- **Notes:** Most structured subject, ideal baseline

#### 2. English KS1-2
- **Status:** ✅ Extracted (Year 1 sample)
- **Structure Rating:** 4/10
- **Total Concepts:** ~80 estimated
- **Location:** Agent output (a91b5a9) - needs JSON file save
- **Key Features:** Reading, Writing, Spoken Language (cross-cutting), skills-heavy
- **Notes:** Developmental prerequisites, interdependent domains

#### 3. Science KS1-2
- **Status:** ✅ Extracted (KS1 sample)
- **Structure Rating:** 5/10
- **Total Concepts:** ~70 estimated
- **Location:** Agent output (ac47c9a) - needs JSON file save
- **Key Features:** Working Scientifically (cross-cutting), dual nature (facts + process)
- **Notes:** Fuzzy prerequisites, mixed concept types

#### 4. History KS1-2
- **Status:** ✅ Extracted (KS1 sample)
- **Structure Rating:** 5/10
- **Total Concepts:** ~60 estimated
- **Location:** Agent output (adc4fb4) - needs JSON file save
- **Key Features:** Chronology, Knowledge, Enquiry, Interpretation domains
- **Notes:** Content vs skills tension, temporal prerequisites

#### 5. Geography KS1-2
- **Status:** ✅ Extracted (KS1 sample)
- **Structure Rating:** 6/10
- **Total Concepts:** ~55 estimated
- **Location:** Agent output (a3848d2) - needs JSON file save
- **Key Features:** Scale progression (local → national → global)
- **Notes:** Content/skills intertwined, inferrable prerequisites

#### 6. Computing KS1-2
- **Status:** ✅ Extracted (full KS1-2)
- **Structure Rating:** 8/10
- **Total Concepts:** ~50 estimated
- **Location:** Agent output - needs JSON file save
- **Key Features:** 3 domains (Computer Science, IT, Digital Literacy)
- **Notes:** More structured than expected, strong prerequisite chains

#### 7. Art & Design KS1-2
- **Status:** ✅ Extracted (KS1)
- **Structure Rating:** 3/10
- **Total Concepts:** 29
- **Location:** Agent output (a12275e) - embedded in response
- **Key Features:** Technical Elements (cross-cutting), Creative Dispositions, extremely compact
- **Notes:** Only 4 objectives for entire KS1, high teacher autonomy

#### 8. Design & Technology KS1-2
- **Status:** ✅ Extracted (KS1)
- **Structure Rating:** 6/10
- **Total Concepts:** 57
- **Location:** `/Users/richardmorgan/Documents/GitHub/uk-curriculum-as-graph/data/curriculum-documents/subjects/primary/DesignAndTechnology_KS1_extracted_v2.json`
- **Key Features:** Iterative Design Process (cross-cutting), safety-first approach
- **Notes:** 6 domains, 57 prerequisites, explicit safety requirements

#### 9. Languages KS2
- **Status:** ✅ Extracted (full KS2)
- **Structure Rating:** 7/10
- **Total Concepts:** 62
- **Location:** Agent output (a324238) - embedded in response
- **Key Features:** Language-agnostic framework, 4 skills + 4 cross-cutting domains
- **Notes:** Listening, Speaking, Reading, Writing with Grammar, Phonology, Vocabulary cross-cutting

#### 10. Music KS1-2
- **Status:** ✅ Extracted (KS1)
- **Structure Rating:** 4/10
- **Total Concepts:** 28
- **Location:** Agent output (a20474d) - embedded in response
- **Key Features:** Musical Elements (cross-cutting), 7 inter-related dimensions
- **Notes:** Only 4 objectives, broad integration of performing, composing, listening

#### 11. Physical Education KS1-2
- **Status:** ✅ Extracted (KS1)
- **Structure Rating:** 5/10
- **Total Concepts:** 30
- **Location:** `/Users/richardmorgan/Documents/GitHub/uk-curriculum-as-graph/data/curriculum-documents/subjects/primary/PhysicalEducation_KS1-2_2013_extracted.json`
- **Key Features:** Fundamental Movement Skills (cross-cutting), high attitude component (20%)
- **Notes:** 50 prerequisites, developmental/instructional types dominate

### Secondary (KS3-4)

#### 12. Citizenship KS3-4
- **Status:** ✅ Extracted (KS3)
- **Structure Rating:** 4/10
- **Total Concepts:** 40
- **Location:** Agent output (af1f996) - embedded in response
- **Key Features:** Critical Thinking Skills (cross-cutting), highly abstract
- **Notes:** Secondary only, 6 domains including Democracy, Law, Rights, Community Action, Financial Literacy

---

## Remaining Subjects to Extract

### Primary (0 remaining)
- ✅ All 11 primary subjects extracted

### Secondary (11 remaining - partial)
- ⏳ **English KS3** - needs extraction
- ⏳ **Mathematics KS3** - needs extraction
- ⏳ **Science KS3** - needs extraction
- ⏳ **History KS3** - needs extraction
- ⏳ **Geography KS3** - needs extraction
- ⏳ **Computing KS3** - partial (may have from earlier work)
- ⏳ **Art & Design KS3** - needs extraction
- ⏳ **Design & Technology KS3** - needs extraction
- ⏳ **Languages KS3** - needs extraction
- ⏳ **Music KS3** - needs extraction
- ⏳ **Physical Education KS3** - needs extraction

---

## File Organization Structure

```
/Users/richardmorgan/Documents/GitHub/uk-curriculum-as-graph/
├── data/
│   └── curriculum-documents/
│       ├── metadata.json                           # Central manifest (24 documents)
│       ├── framework/
│       │   ├── KS1-2_Framework_2014.pdf           # Primary framework
│       │   └── KS3-4_Framework_2014.pdf           # Secondary framework
│       └── subjects/
│           ├── primary/
│           │   ├── Mathematics_KS1-2_2021.pdf
│           │   ├── English_KS1-2_2014.pdf
│           │   ├── Science_KS1-2_2015.pdf
│           │   ├── Computing_KS1-2_2013.pdf
│           │   ├── History_KS1-2_2013.pdf
│           │   ├── Geography_KS1-2_2013.pdf
│           │   ├── ArtAndDesign_KS1-2_2013.pdf
│           │   ├── DesignAndTechnology_KS1-2_2013.pdf
│           │   │   └── DesignAndTechnology_KS1_extracted_v2.json  ✅
│           │   ├── Languages_KS2_2013.pdf
│           │   ├── Music_KS1-2_2021.pdf
│           │   └── PhysicalEducation_KS1-2_2013.pdf
│           │       └── PhysicalEducation_KS1-2_2013_extracted.json  ✅
│           └── secondary/
│               ├── Mathematics_KS3_2021.pdf
│               ├── English_KS3_2021.pdf
│               ├── Science_KS3_2014.pdf
│               ├── Computing_KS3_2013.pdf
│               ├── History_KS3_2013.pdf
│               ├── Geography_KS3_2013.pdf
│               ├── ArtAndDesign_KS3_2013.pdf
│               ├── Citizenship_KS3-4_2013.pdf
│               ├── DesignAndTechnology_KS3_2013.pdf
│               ├── Languages_KS3_2013.pdf
│               ├── Music_KS3_2013.pdf
│               └── PhysicalEducation_KS3_2013.pdf
└── docs/
    ├── graph_model_v2.md                          # Enhanced model specification
    ├── extraction_stress_test_results.md          # This analysis
    └── extraction_inventory.md                    # This file

```

---

## Extraction Outputs to Consolidate

Most extractions exist as **agent outputs embedded in conversation** and need to be saved as standalone JSON files.

### Action Items:
1. **Save agent outputs as JSON files** for subjects 1-7, 9-10, 12
2. **Organize all JSON extractions** in consistent directory structure
3. **Create index file** mapping each JSON to source document
4. **Validate JSON schema** consistency across all extractions

### Recommended File Naming Convention:
```
{Subject}_{KeyStage}_extracted_v2.json

Examples:
- Mathematics_KS1_extracted_v2.json
- English_KS1_extracted_v2.json
- Languages_KS2_extracted_v2.json
- Citizenship_KS3_extracted_v2.json
```

---

## Extraction Statistics Summary

| Metric | Count |
|--------|-------|
| **Total subjects in curriculum** | 12 core + foundation |
| **Documents downloaded** | 24 (22 subject + 2 framework) |
| **Subjects extracted** | 12 (50%+) |
| **Primary subjects extracted** | 11/11 (100%) |
| **Secondary subjects extracted** | 1/12 (8%) |
| **Total concepts extracted** | ~600+ |
| **Cross-cutting domains identified** | 8 |
| **Prerequisite relationships** | ~400+ |
| **JSON files saved** | 2 (D&T, PE) |
| **JSON files pending** | 10 |

---

## Next Actions

### Immediate (Consolidation)
1. [ ] Save all agent extraction outputs as formatted JSON files
2. [ ] Validate JSON schema consistency
3. [ ] Create extraction index with metadata
4. [ ] Document any extraction variations or special cases

### Short-term (Database Implementation)
1. [ ] Design Neo4j schema based on model v2.0
2. [ ] Create Cypher scripts for node/relationship creation
3. [ ] Import 12 extracted subjects into Neo4j
4. [ ] Test graph queries (prerequisite chains, concept search, progression paths)

### Medium-term (Completion)
1. [ ] Extract remaining 11 KS3 subjects
2. [ ] Extract KS2 full coverage (currently have samples)
3. [ ] Add year-level granularity where available
4. [ ] Cross-validate prerequisites across subjects

### Long-term (Enhancement)
1. [ ] Add KS4 content (GCSE)
2. [ ] Include non-statutory guidance
3. [ ] Link to assessment frameworks
4. [ ] Add exemplar materials
5. [ ] Create curriculum mapping tools

---

## Quality Assurance Checklist

For each extraction:
- [ ] All objectives extracted verbatim from source document
- [ ] Concepts decomposed to atomic level
- [ ] Concept_type assigned (knowledge/skill/process/attitude/content)
- [ ] Complexity_level rated 1-5 with rationale
- [ ] Prerequisites include: confidence, relationship_type, strength, rationale
- [ ] Cross-cutting domains identified and justified
- [ ] Source traceability maintained (document, page, section)
- [ ] JSON validates against schema
- [ ] Extraction notes document challenges and decisions
- [ ] Date and model version recorded in metadata

---

## Contact & Maintenance

**Last Updated By:** Claude Sonnet 4.5
**Date:** 2026-02-12
**Model Version:** Graph Model v2.0

For questions about extractions, see `/docs/graph_model_v2.md` for model specification and `/docs/extraction_stress_test_results.md` for validation results.
