---
title: 'PFA: Attention Can Be Progressively Focused in Long-Sequence Generative Recommendation'
source_url: https://arxiv.org/abs/2610.39273v1
company: bytedance
date: '2026-10-29'
evidence_tier: 1
language: en
track: modeling
full_text: complete
---

# Computer Science > Information Retrieval

# Title: PFA: Attention Can Be Progressively Focused in Long-Sequence Generative Recommendation

Abstract: Long user behavioral sequences improve the performance of generative recommendation (GR), but computing full attention over long histories during autoregressive beam search decoding incurs substantial online inference latency. To accelerate long-sequence decoding, existing approaches typically rely on static history compression or dynamic top-k sparse attention; however, the former risks losing critical semantics, whereas the latter incurs significant overhead from repeated token selection and non-contiguous memory access. In this work, we thoroughly analyze attention patterns during GR decoding and reveal two key properties: (i) progressive attention focusing, where attention progressively focuses on a small subset of critical historical tokens; and (ii) cross-step ranking consistency, where their importance rankings remain relatively stable across subsequent decoding steps. Motivated by these observations, we propose Progressively Focused Attention (PFA), an efficient sparse decoding framework for long-sequence GR. PFA retains full attention at the initial decoding step to explore global historical preferences. It then establishes a shared importance ranking through cross-beam weighted aggregation and reorders the key-value cache of the selected tokens into a contiguous memory layout. Subsequent decoding steps reuse this ranking and geometrically reduce the token budget, preserving critical semantics while lowering computational and memory access overhead. Extensive experiments on two public benchmarks and a large-scale industrial dataset demonstrate that PFA outperforms state-of-the-art baselines. A 7-day online A/B test on a large-scale e-commerce advertising platform further confirms that PFA delivers substantial business gains while maintaining low inference latency. Our code is publicly available at this https URL .

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
