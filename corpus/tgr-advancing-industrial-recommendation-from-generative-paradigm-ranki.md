---
title: 'TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking
  toward Unified Generation and Reasoning'
source_url: https://arxiv.org/abs/2609.00986v1
company: bytedance
date: '2026-09-01'
evidence_tier: 1
language: en
track: modeling
full_text: complete
---

# Computer Science > Information Retrieval

# Title: TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking toward Unified Generation and Reasoning

Abstract: Industrial recommender systems typically rely on cascaded retrieval, pre-ranking, ranking, and reranking stages, whose separately optimized models limit scaling, fragment decision making, and lack semantic knowledge and reasoning. We present TGR (Tencent Generative Recommendation), an industrial framework that advances recommendation toward the generative paradigm along three coupled directions. TGR-GenRank upgrades ranking through CCFormer, which combines unified feature tokenization, a scalable Transformer backbone, feature-field separated cross attention, subspace token mixing, and hierarchical sequence compression while retaining per-item multi-task outputs. TGR-GenRec explores end-to-end generation under two paradigms: BARGE bridges item-boundary loss and semantic drift in hierarchical semantic-ID generation through item context-aware attention, hierarchical path reranking, and orthogonal dual-path decoding; HiGR performs whole-slate generation with prefix-structured semantic IDs, coarse-to-fine decoding, and listwise multi-objective alignment. TGR-Reason injects offline-generated semantic-ID reason tokens into online decoding, providing reasoning without request-time rollout. TGR is deployed across Tencent production surfaces serving hundreds of millions of users. CCFormer delivers significant gains in five A/B-tested scenarios and is fully launched in two, including +3.57% CTR and +1.71% advertising revenue. BARGE improves Hit@5 by 10.2-16.9% and yields +0.60% CTR and +1.70% reading time after full rollout. HiGR improves offline slate quality by 15.9-21.3% with a 5x inference speedup and achieves up to +1.22% watch time and +1.73% video views. TGR-Reason raises cold-start new-user Hit@1 by 477.8% and delivers +1.75% effective consumption and +13.09% new-user exposure-to-conversion online.

## Submission history

## Access Paper:

- View PDF

- HTML (experimental)

- TeX Source

### Additional Features

- Audio Summary

### Current browse context:

### References & Citations

- NASA ADS

- Google Scholar

- Semantic Scholar

## BibTeX formatted citation

### Bookmark

# Bibliographic and Citation Tools

# Code, Data and Media Associated with this Article

# Demos

# Recommenders and Search Tools

- Author

- Venue

- Institution

- Topic

# arXivLabs: experimental projects with community collaborators

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? Learn more about arXivLabs .
