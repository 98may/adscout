---
title: 'OneTrans-GSR: A Generative Slate Ranking Paradigm Unifying Reranking and Mix-Ranking
  with One Autoregressive Transformer'
source_url: https://arxiv.org/abs/2611.04720v1
company: bytedance
date: '2026-11-03'
evidence_tier: 1
language: en
track: modeling
full_text: complete
---

# Computer Science > Information Retrieval

# Title: OneTrans-GSR: A Generative Slate Ranking Paradigm Unifying Reranking and Mix-Ranking with One Autoregressive Transformer

Abstract: Industrial recommender systems allocate substantial computation to pointwise candidate scoring, yet separate reranking and mix-ranking stages still assemble the final exposure slate using hand-crafted rules and specialized low-capacity models. Mix-ranking combines product cards, short videos, livestreams, and advertising cards supplied by distinct upstream business channels. Although these rules and models encode valuable domain knowledge, they are inherently limited in leveraging additional data and computation. They constrain the combinatorial space of candidate slates and determine objective trade-offs through manual tuning. To enable scalable and effective slate generation, we reformulate reranking and mix-ranking as a unified learning problem whose performance can improve with computation. Specifically, we instantiate this formulation across the reranking and mix-ranking stages and propose OneTrans-GSR, a single decoder-only policy that extends our deployed OneTrans backbone to generate the exposure slate end-to-end. During training, a reward model evaluates complete slates and guides reinforcement learning toward slate-level and long-term objectives. During decoding, business constraints are explicitly enforced. Offline evaluation shows that slate quality consistently improves as reward-model and policy compute increase. Deployed in a large-scale industrial recommendation system, OneTrans-GSR mixes heterogeneous content types within a unified slate. In online A/B tests, it improves GMV/u by 2.63%, advertiser value by 2.06%, and repurchase rate by 2.03%, while reducing end-to-end latency across the reranking and mix-ranking stages by 13%. These results mark a paradigm shift in slate generation: moving beyond human-engineered heuristics toward a general learned policy creates a scalable path for further algorithmic optimization and compute-driven improvement.

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
