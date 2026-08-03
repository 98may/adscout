---
title: 'UniVA: Unified Value Alignment for Generative Recommendation in Online Advertising
  at Tencent'
source_url: https://arxiv.org/abs/2605.05803v2
company: bytedance
date: '2026-05-07'
evidence_tier: 1
language: en
track: modeling
full_text: complete
---

# Computer Science > Information Retrieval

# Title: UniVA: Unified Value Alignment for Generative Recommendation in Online Advertising at Tencent

Abstract: Generative Recommendation (GR) reformulates recommendation as next-token generation over item Semantic IDs (SIDs) and has shown promise in industrial applications. However, extending GR to advertising is non-trivial, as advertising recommendation must jointly account for user relevance and commercial value. This creates a mismatch: high generation likelihood does not necessarily imply high advertising utility. As a result, valuable ads may be poorly distinguished in the SID space, pruned during autoregressive decoding, or missed when request-invalid branches consume limited beam capacity during online serving. To address this problem, we propose UniVA, a Unified Value Alignment framework for generative advertising recommendation. UniVA aligns commercial value across the entire pipeline of SID construction, autoregressive decoding, and online serving. Commercial SID Tokenization injects business attributes and bid information into SID construction. A Generation-as-Ranking SID Decoder then fuses generation scores with token-level value estimates during autoregressive decoding. {Finally, Value-Aware Constrained Serving restricts the fused decoding process to request-valid SID paths through a personalized trie.} Experiments on the Tencent WeChat Channels advertising platform show that UniVA achieves a 37.04\% relative improvement in offline Hit Rate@100 over the baseline and lifts gross merchandise value (GMV) by 1.5\% in online A/B tests.

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
