---
title: One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical
  Text Representations
source_url: https://arxiv.org/abs/2609.18296v1
company: bytedance
date: '2026-09-16'
evidence_tier: 1
language: en
track: modeling
full_text: complete
---

# Computer Science > Information Retrieval

# Title: One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations

Abstract: Traditional retrieval systems typically use multi-stage cascading architectures (MCA), where each module is optimized independently, leading to inconsistent objectives and the premature elimination of high-potential candidates. Recent LLM-based generation methods offer end-to-end solutions but use discrete semantic identifiers (SIDs) to retrieve ads, which are not learned by the base LLM and require memorization of numerous SID-to-ad mappings during SFT, suffering from limited generalization to unseen ads, high maintenance and update costs. The one-to-one mapping between SIDs and advertisements leads to inefficient decoding. Moreover, these methods rely on a small reward model (e.g. pctr) for relevance and ranking, limiting the LLM's ability to fully assess ads' commercial value. To address these challenges, we propose A uNified Generation-discriminative-ranking reaL-time rEtrieval (ANGLE) framework. ANGLE uses LLM-generated hierarchical textual representations, which consist of commercial intent that provide high-level overviews and ad abstract that deliver fine-grained details. Additionally, ANGLE integrates retrieval, relevance, and ranking directly within a single LLM, enabling precise and efficient ranking of ads by leveraging the full capabilities of the LLM. We applied ANGLE to the real-world search scenarios, achieving a 1.81% increase in consumption and a 2.16% increase in gross merchandise volume (GMV). We also conducted offline evaluations of ANGLE and seven baselines, with ANGLE outperforming all across key metrics such as HR and ACR.

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
