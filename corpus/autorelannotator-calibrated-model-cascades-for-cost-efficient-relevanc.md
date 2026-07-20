---
title: 'AutoRelAnnotator: Calibrated Model Cascades for Cost-Efficient Relevance Evaluation
  in Sponsored Search'
source_url: https://arxiv.org/abs/2606.25871v1
company: bytedance
date: '2026-06-24'
evidence_tier: 1
language: en
track: modeling
full_text: complete
---

# Computer Science > Information Retrieval

# Title: AutoRelAnnotator: Calibrated Model Cascades for Cost-Efficient Relevance Evaluation in Sponsored Search

Abstract: How can we generate high-quality relevance annotations at scale without the cost and delays of human labeling? Relevance annotations are the backbone of search ranking systems which is needed for training data preparation, NDCG evaluation, and root cause analysis. However, human annotation is slow and off-the-shelf LLMs suffer from accuracy on domain-specific tasks. We propose a calibrated model cascade, a systematic approach for cost-efficient offline relevance annotation by routing queries through progressively larger fine-tuned classifiers. Our central insight is that accuracy and cost are orthogonal optimizations: domain-specific fine-tuning drives accuracy, cascading drives cost, and per-class isotonic calibration adds a small but reliable gain on top. Our contribution is threefold: (a) we decompose the gains and show that fine-tuning contributes 20 accuracy points while cascading is approximately accuracy-neutral but halves compute cost, (b) we introduce per-class isotonic calibration as one component of the cascade, contributing a small but statistically significant gain (+0.6 points over the strongest calibration baseline), and (c) we validate the system in production across six offline use cases, processing 150M+ annotations and enabling faster experimentation cycles. Our work is a building block for scalable, high-quality offline annotation pipelines in search and advertising systems.

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
