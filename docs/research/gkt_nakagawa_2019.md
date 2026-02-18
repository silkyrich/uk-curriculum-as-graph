# Graph-Based Knowledge Tracing: Modeling Student Proficiency Using Graph Neural Network
**Citation:** Nakagawa, H., Iwasawa, Y., & Matsuo, Y. (2019). Graph-Based Knowledge Tracing: Modeling Student Proficiency Using Graph Neural Network. *Proceedings of the IEEE/WIC/ACM International Conference on Web Intelligence (WI 2019)*; also presented at the IRLG Workshop at ICLR 2019.
**Source:** https://rlgm.github.io/papers/70.pdf
**Fetched:** 2026-02-18
**Type:** academic paper
**Access:** briefing summary only

## Summary
Nakagawa et al. introduced Graph-Based Knowledge Tracing (GKT), which uses graph neural networks to model concept dependency relationships explicitly. Rather than treating knowledge components as independent (as in vanilla BKT) or learning implicit inter-skill relationships from sequences (as in DKT), GKT takes a directed graph of concept prerequisites as structural input and propagates information through it to estimate per-concept mastery probabilities. It is the most directly relevant prior work to this platform's architecture.

## Key findings
- Uses graph neural networks (GNNs) to model concept dependency relationships as directed edges
- Concept prerequisite graph is structural input to the model, not learned implicitly from data
- Outperforms vanilla BKT and early DKT variants when the concept graph structure is informative
- Directly addresses the fundamental limitation of flat-skill KT models: concepts are not independent
- Foundational paper for the subsequent wave of graph-aware KT research including DyGKT (2024)

## Direct quotes
None available — full text not fetched from this cache entry; known from the briefing summary.

"GKT (Nakagawa et al. 2019, ICLR): Graph-based Knowledge Tracing using graph neural networks to explicitly model concept dependency relationships as directed edges."

## Relevance to platform
This is the single most architecturally relevant KT paper for the platform: GKT uses exactly the kind of directed prerequisite graph that has already been built in Neo4j as its structural input, meaning the existing curriculum graph can serve directly as the GKT domain model once sufficient learner interaction data is available.
