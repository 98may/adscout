---
title: 'HubMixer: Progressive Latent Hub Mixing for Parameter-Efficient Feature Interaction
  in Recommendation'
source_url: https://arxiv.org/abs/2608.27991v2
company: bytedance
date: '2026-08-28'
evidence_tier: 1
language: en
track: modeling
full_text: complete
---

# Computer Science > Information Retrieval

# Title: HubMixer: Progressive Latent Hub Mixing for Parameter-Efficient Feature Interaction in Recommendation

Abstract: Learning effective feature interactions is central to industrial recommendation and advertising ranking systems. Recent token-mixing architectures simplify self-attention with lightweight mixing operators, improving hardware efficiency and enabling large-scale deployment. However, recommendation tokens are fundamentally heterogeneous: user profiles, item attributes, behavioral sequences, context features, statistical signals, and business-side features live in different semantic spaces and interact in sparse, sample-specific patterns. Directly mixing all tokens in the raw heterogeneous token space may therefore be parameter-inefficient, as the model must implicitly discover which feature groups should interact and how such interactions should be routed. In the paper, we propose HubMixer, a parameter-efficient latent hub mixing architecture for feature interaction in recommendation. Instead of directly mixing raw feature tokens, HubMixer introduces a small set of learnable latent hubs to organize feature interactions through an `induction--interaction--readout` paradigm. First, hub induction summarizes heterogeneous tokens into compact latent hubs, where latent hubs query input tokens through cross-attention. Second, hub interaction performs high-order interaction in the cleaner latent hub space. Third, token-conditioned readout lets each original token selectively read from the interacted hubs, injecting global interaction semantics while preserving token-level field identity. Extensive offline experiments on industrial recommendation tasks show that HubMixer outperforms the SOTA models. Online A/B testing in the Kuaishou short-video recruitment business further shows a statistically significant 5.48% improvement in resume submission conversion rate, and HubMixer has been fully deployed in production.

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
