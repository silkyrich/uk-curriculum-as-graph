# Deep Knowledge Tracing
**Citation:** Piech, C., Bassen, J., Huang, J., Ganguli, S., Sahami, M., Guibas, L., & Sohl-Dickstein, J. (2015). Deep Knowledge Tracing. *Advances in Neural Information Processing Systems (NeurIPS)*, 28.
**Source:** https://arxiv.org/abs/1506.05908
**Fetched:** 2026-02-18
**Type:** academic paper
**Access:** briefing summary only (arxiv fetch failed)

## Summary
Piech et al. introduced Deep Knowledge Tracing (DKT), applying an LSTM recurrent neural network to the knowledge tracing problem. Rather than modelling each skill with a small set of hand-specified parameters as in Bayesian Knowledge Tracing, DKT treats a student's entire interaction history as a sequence and learns to predict the probability of a correct response on any future item. It significantly outperformed BKT on the standard ASSISTments benchmark dataset and triggered a decade of deep-learning-based knowledge tracing research.

## Key findings
- LSTM applied to knowledge tracing substantially outperformed Bayesian Knowledge Tracing on the ASSISTments dataset
- Sequential interaction history is sufficient signal to predict future performance without explicit skill parameter specification
- The model generalises across knowledge components implicitly, learning inter-skill relationships from data
- Triggered a decade of follow-on deep KT research: DKVMN (2017), AKT (2020), GKT (2019), DyGKT (2024) and many others
- As of a 2024 IEEE Education Society review, 37 papers on deep KT were published in 2024 alone

## Direct quotes
None available — full text not fetched; the following is paraphrased from the briefing.

"Piech et al.'s 2015 DKT paper applied an LSTM network to the knowledge tracing problem, treating a student's interaction history as a sequence and predicting future performance. It significantly outperformed BKT on the benchmark ASSISTments dataset and triggered a decade of deep-learning-based knowledge tracing research."

## Relevance to platform
DKT establishes that sequence-aware deep models substantially outperform BKT on large datasets, but the data-hungry nature of LSTM models means hierarchical BKT is the more defensible starting point for a new platform with cold-start constraints; once sufficient interaction data is accumulated, the graph-aware DKT variants (GKT, DyGKT) that can read the Neo4j prerequisite structure are the natural upgrade path.
