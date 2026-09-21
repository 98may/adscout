---
title: 'ChronicleRec: Pre-training Temporally Anchored Tokens for Lifelong User Modeling'
source_url: https://arxiv.org/abs/2609.12375v1
company: bytedance
date: '2026-09-11'
evidence_tier: 1
language: en
track: modeling
full_text: complete
---

# Computer Science > Information Retrieval

# Title: ChronicleRec: Pre-training Temporally Anchored Tokens for Lifelong User Modeling

Abstract: Modeling ultra-long user behavior sequences is crucial for industrial recommendation and online advertising, yet directly feeding thousands of historical actions into ranking models is computationally prohibitive, while truncation discards long-range signals. Existing lifelong-interest methods retrieve target-relevant behaviors for each candidate, coupling long-sequence modeling with candidate scoring and repeated online cost. Recent target-independent compression methods enable cached user summaries, but often append query tokens at the sequence end and use bidirectional encoding, producing unordered and redundant summaries that overlook temporal structure. We propose ChronicleRec, a pre-train-and-transfer framework that compresses an ultra-long behavior sequence once into a chronologically ordered set of Chronicle Tokens. ChronicleRec applies a recency-aware multi-granularity merge, preserving recent behaviors while coarsening distant history. It then interleaves query tokens with the merged sequence and uses a causal encoder, so each query summarizes only the history before its temporal anchor. A multi-horizon design masks different recent-history windows across parallel branches to learn complementary long-range interests. The compressor is pre-trained with a mask-and-predict objective that reconstructs held-out recent behaviors from compressed older history, aligning historical signals with near-present intent. Since Chronicle Tokens are target-independent, they can be cached per user, decoupling ultra-long sequence modeling from online candidate scoring. Experiments on KuaiRand and Tencent AdLive show that ChronicleRec outperforms recent-window and single-pass compression baselines while approaching full-attention performance. Token analyses reveal temporally organized and complementary representations, and a seven-day online A/B test confirms significant production gains.

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
