---
title: Unified Value Alignment for Generative Recommendation in Industrial Advertising
source_url: https://arxiv.org/abs/2605.05803v1
company: bytedance
date: '2026-05-07'
evidence_tier: 1
language: en
track: modeling
full_text: complete
---

# Computer Science > Information Retrieval

# Title: Unified Value Alignment for Generative Recommendation in Industrial Advertising

Abstract: Generative Recommendation (GR) reformulates recommendation as a next-token generation problem and has shown promise in industrial applications. However, extending GR to industrial advertising is non-trivial because the system must optimize not only user interest but also commercial value. Existing GR pipelines remain largely semantics-centric, making it difficult to align value signals across tokenization, decoding, and online serving. To address this issue, we propose UniVA, a Unified Value Alignment framework for advertising recommendation. We first introduce a Commercial SID tokenizer that injects value-related attributes into SID construction, yielding value-discriminative item representations. We then develop a Generation-as-Ranking SID Decoder jointly optimized by supervised learning and eCPM-aware reinforcement learning, which fuses value scores into next-item SID generation to perform generation and ranking in one decoding process. Finally, we design a value-guided personalized beam search that reuses generation-as-ranking logits as online value guidance and applies a personalized trie tree to constrain decoding to request-valid SID paths. Experiments on the Tencent WeChat Channels advertising platform show that UniVA achieves a 37.04\% improvement in offline Hit Rate@100 over the baseline and a 1.5\% GMV lift in online A/B tests.

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
