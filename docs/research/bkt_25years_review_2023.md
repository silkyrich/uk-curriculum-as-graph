# Twenty-Five Years of Bayesian Knowledge Tracing: A Systematic Review
**Citation:** Author(s) not confirmed from fetch. (2023). Twenty-five years of Bayesian Knowledge Tracing: A systematic review. *User Modeling and User-Adapted Interaction*. https://doi.org/10.1007/s11257-023-09389-4
**Source:** https://link.springer.com/article/10.1007/s11257-023-09389-4
**Fetched:** 2026-02-18
**Type:** systematic review
**Access:** briefing summary only (Springer redirect / paywall)

## Summary
This systematic review covers 25 years of Bayesian Knowledge Tracing (BKT) research in *User Modeling and User-Adapted Interaction*, one of the primary journals for adaptive learning systems. It synthesises findings across 13 enhancement dimensions, characterises the conditions under which BKT variants outperform the standard model, and documents the known limitations of vanilla BKT. The review identifies individualised BKT as the most consistently superior enhancement and expectation-maximisation (EM) as the de facto standard for parameter estimation.

## Key findings
- Individualised BKT (per-student learning rate parameters, i.e. hierarchical BKT) consistently outperforms vanilla BKT on prediction accuracy across the literature
- The expectation-maximisation (EM) algorithm is the de facto standard for BKT parameter estimation
- Vanilla BKT treats each skill as independent — directly conflicting with graph-based curricula where concepts have rich prerequisite dependencies
- Identifiability problems with the four-parameter BKT model: multiple parameter combinations can produce identical predictions; the model is underspecified for small datasets (Van de Sande, 2016, analysis cited in briefing)
- Hierarchical BKT (hBKT), where each student has a learning rate sampled from a population distribution, is tractable and substantially more accurate than vanilla BKT
- For the cold-start problem (new platform, limited interaction data), BKT variants are more defensible than deep KT models

## Direct quotes
From the briefing summary:

"Individualised BKT (per-student learning rate parameters) consistently outperforms vanilla."

"EM algorithm is de facto standard."

"Vanilla BKT treats skills as independent (problem for graph-based curriculum)."

"Identifiability problems with 4-parameter model."

## Relevance to platform
This review confirms that the correct starting KT model for the platform is hierarchical BKT (not vanilla BKT, and not deep KT until data volume justifies it), and that the four-parameter vanilla model's identifiability issues mean it should not be deployed on sparse per-concept data; the prerequisite graph in Neo4j directly addresses BKT's independence assumption, making graph-extended hierarchical BKT the architecturally sound choice.
