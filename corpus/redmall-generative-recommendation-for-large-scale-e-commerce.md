---
title: 'RedMall: Generative Recommendation for Large-Scale E-commerce'
source_url: https://arxiv.org/abs/2611.08519v1
company: bytedance
date: '2026-10-26'
evidence_tier: 1
language: en
track: modeling
full_text: complete
---

# Computer Science > Information Retrieval

# Title: RedMall: Generative Recommendation for Large-Scale E-commerce

Abstract: Generative recommendation has shown considerable potential in industrial recommendation systems. However, the performance of existing generative methods is limited by several challenges. 1) Semantic IDs (SIDs) are treated as one-dimensional sequences, overlooking the hierarchical dependencies among different layers. 2) Next-token prediction used is unable to explicitly optimize session-wise recommendation. 3) Although reinforcement learning has been applied to align generated recommendations with user preferences, few existing methods explicitly optimize the ranking of positive items in session-wise recommendation. To address the above issues, we propose RedMall, a generative recommender designed for large-scale e-commerce. Firstly, RedMall constructs hierarchical SIDs through residual quantization over multimodal representations. Secondly, RedMall introduces a lightweight SID encoder to explicitly model layer-wise dependencies in SIDs. Moreover, RedMall incorporates sparse mixture-of-experts, dual gated attention, and multi-target prediction to scale model size, enhance user interest representation, and optimize session-wise recommendation. We further design an exposure-aware loss that treats exposed but unclicked items as negative feedback. To better align user preferences and list-wise ranking objectives, we combine Group Relative Policy Optimization with an auxiliary LambdaRank loss, using both real user feedback and item ranking to guide optimization. Experiments on four public datasets-Amazon Beauty, Amazon Toys, Amazon Food, and MovieLens-1M---show that RedMall outperforms the evaluated baselines across all reported Recall and NDCG metrics. Online A/B tests show improvements of 2.24% in advertiser value (ADVV) and 0.59% in click-through rate (CTR) for e-commerce advertising, as well as gains of 1.08% in GMV and 0.95% in daily active buyers (DAB) for e-commerce recommendations.

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
