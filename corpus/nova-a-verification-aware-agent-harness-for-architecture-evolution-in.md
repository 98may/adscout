---
title: 'NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial
  Recommender Systems'
source_url: https://arxiv.org/abs/2606.27243v3
company: bytedance
date: '2026-06-25'
evidence_tier: 1
language: en
track: modeling
full_text: complete
---

# Computer Science > Information Retrieval

# Title: NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems

Abstract: Industrial advertising recommender systems are continually improved through architecture modifications, yet production iteration remains expert-intensive because coordinated changes to model topology, feature configuration, and interaction modules must satisfy strict interface, resource, and serving constraints. AutoML is limited to predefined search spaces, while generic coding agents verify runnability rather than recommender-specific semantic validity. Executable candidates may therefore violate architectural contracts, while the lack of structured reuse of semantic diagnostics and evaluation outcomes can lead to repeated invalid or ineffective modifications. We present NOVA, a verification-aware agent harness that organizes production architecture modification as multi-round search over concrete implementations within a fixed evaluation budget. At each round, NOVA generates multiple candidates under production constraints, rejects semantic violations, and ranks the valid survivors for local testing and offline evaluation. Across rounds, trajectory memory synthesizes semantic diagnostics, local-test outcomes, and offline metric changes into modification directions and forbidden patterns that guide subsequent search. Under the same maximum offline-evaluation budget for automated methods, NOVA achieves the highest effective pass rate, reaching 53.3% on ScaleUp and 51.7% on Literature-to-Production tasks. In a production A/B test covering 5% of traffic in an advertising system serving over one billion users, the selected Literature-to-Production candidate yields GMV gains of +1.25%, +1.70%, and +2.02% across three major pCVR objectives, with corresponding relative reductions in absolute pCVR bias of 58.8%, 66.7%, and 37.3%, respectively.

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
