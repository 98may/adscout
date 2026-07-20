---
title: 'LERA: LLM-Enhanced RAG for Ad Auction in Generative Chatbots'
source_url: https://arxiv.org/abs/2605.16474v1
company: bytedance
date: '2026-05-15'
evidence_tier: 1
language: en
track: modeling
full_text: complete
---

# Computer Science > Information Retrieval

# Title: LERA: LLM-Enhanced RAG for Ad Auction in Generative Chatbots

Abstract: The integration of advertising auction mechanisms into large language model (LLM)-based chatbots presents a significant opportunity for commercialization, yet poses unique challenges in balancing relevance, efficiency, and user experience. Recently, Feizi et al.~\citep{feizi2023online} and Hajiaghayi et al.~\citep{hajiaghayi2024ad} outlined a retrieve-then-generate paradigm that decouples retrieval and generation, offering lightweight ad insertion and payment determination. However, current retrieval relies solely on text embedding similarity, which may lead to commercial misinterpretation and issues such as repetitive insertions. In this paper, we propose LERA, a two-stage retrieve-then-generate auction framework tailored for LLM chatbots. In the first stage, embedding-based coarse filtering pre-selects a small set of candidate advertisers. In the second stage, the LLM itself is queried with a carefully designed prompt to produce logits over candidates, which serve as refined organic relevance scores. These scores are combined with bids, and a critical-value payment rule accounts for both the coarse-filtering and fine-ranking thresholds, ensuring truthfulness for utility-maximizing advertisers. The framework naturally extends to multiple ad insertions within dynamic dialogue flows and long responses. Experiments on a synthetic advertiser-query benchmark show that LERA substantially improves ad selection accuracy and insertion diversity while incurring only controllable latency overhead.

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
