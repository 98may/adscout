---
title: 'UGR: Unified Generative Ranking for Heterogeneous E-commerce Recommendation'
source_url: https://arxiv.org/abs/2610.39426v1
company: bytedance
date: '2026-10-29'
evidence_tier: 1
language: en
track: modeling
full_text: complete
---

# Computer Science > Information Retrieval

# Title: UGR: Unified Generative Ranking for Heterogeneous E-commerce Recommendation

Abstract: List-wise ranking in e-commerce recommendation must balance user utility and commercial value across organic content, ads, and candidates from other businesses, while modeling candidate interactions and sequential dependencies. Existing generative ranking methods typically learn from logged exposure sequences and operate on truncated candidate sets from a single business. Exposure-sequence learning may not fully exploit post-exposure feedback signals. Meanwhile, generative ranking over heterogeneous, multi-business candidates remains less explored, particularly when recommendation scores and advertising value must be jointly modeled under generalized second-price (GSP) auctions. We propose Unified Generative Ranking (UGR), which performs generative ranking over the full request-level multi-business heterogeneous candidate set, typically comprising around a thousand candidates in production, and directly generates multi-business ranking lists through candidate-aware autoregressive decoding. To go beyond exposure-sequence imitation, UGR introduces complementary feedback supervision through weighted supervised fine-tuning and permutation preference optimization, which respectively leverage observed post-exposure feedback and feedback-derived preferences among permutations. UGR uses a training-time advertising debiasing tower to model historical ad exposure effects and incorporates current ad value during serving while preserving the existing allocation and GSP pricing rules. Multi-value sequence retrieval produces candidate ranking lists, and the existing downstream evaluator selects the final list for exposure. Offline experiments demonstrate consistent gains in ranking quality, while online A/B tests on Taobao's Guess You Like recommendation service yield improvements of 1.76% in Core IPV, 3.29% in Transaction Volume, and 2.10% in GMV over the production baseline.

## Submission history

## Access Paper:

- View PDF

- HTML (experimental)

- TeX Source

### Additional Features

- Audio Summary

### Current browse context:

### References & Citations

- SciX

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
