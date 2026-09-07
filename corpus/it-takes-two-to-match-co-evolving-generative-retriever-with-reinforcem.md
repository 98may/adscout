---
title: 'It Takes Two to Match: Co-Evolving Generative Retriever with Reinforcement
  Learning'
source_url: https://arxiv.org/abs/2609.00638v1
company: bytedance
date: '2026-09-01'
evidence_tier: 1
language: en
track: modeling
full_text: complete
---

# Computer Science > Information Retrieval

# Title: It Takes Two to Match: Co-Evolving Generative Retriever with Reinforcement Learning

Abstract: Retrieval is the first stage of modern search and advertising systems, selecting a candidate set from a large item universe for downstream ranking and auction. Recent work increasingly leverages LLMs to improve retrieval through query expansion, data synthesis, and retrieval-feedback training. However, the generative component is typically used for query-side augmentation, while final matching is still delegated to a downstream retriever. We introduce CoGR, a retrieval framework that instead trains LLMs to directly construct retrieval representations on both query and item sides. Each generator produces a compact set of keywords, which are matched directly through an inverted index, preserving compatibility with existing keyword-based retrieval infrastructure. CoGR uses a two-stage training pipeline. Supervised fine-tuning first establishes an aligned keyword space, after which co-evolving reinforcement learning alternately optimizes the query- and item-side generators with GRPO against the opposite side's frozen index. Both sides optimize the same query-to-item retrieval $F_1$ objective: the query side receives retrieval $F_1$ directly, while the item side receives a counterfactual marginal reward measuring the change in query-side $F_1$ caused by its generated keywords. Across 10 representative sparse, dense, and generative baselines, CoGR achieves the best performance on both an internal APP Marketplace dataset and the public WANDS benchmark, improving $F_1$ over the strongest baseline by $10.9\%$ and $36.1\%$, respectively. Further analysis shows stable co-evolution and increasingly aligned query--item keyword spaces over training.

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
