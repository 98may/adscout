---
title: Long-History User Transformers for Real-Time Ad Ranking
source_url: https://arxiv.org/abs/2607.14331v1
company: bytedance
date: '2026-07-15'
evidence_tier: 1
language: en
track: modeling
full_text: complete
---

# Computer Science > Information Retrieval

# Title: Long-History User Transformers for Real-Time Ad Ranking

Abstract: Long interaction histories are among the most informative inputs for click-through rate (CTR) prediction, yet in online advertising they collide with a hard serving constraint: ads must be scored within a few hundred milliseconds to enter the auction, which rules out running a large sequence encoder at request time. We describe how a production advertising system resolves this conflict by decoupling history encoding from real-time inference. A high-capacity offline transformer asynchronously encodes the user's full cross-surface interaction history into a compact representation cached in a feature store, while a lightweight runtime model combines this cached representation with the user's most recent events and the request context at serving time. The offline encoder is pre-trained autoregressively on large-scale interaction logs with a dual objective - feedback prediction and next-item prediction - and the two-stage architecture is then fine-tuned for CTR prediction on the target advertising surface. Offline, the split design recovers 72-80% of the quality of a full-history runtime transformer that would be too expensive to deploy, and the cached representation is robust enough to staleness to permit inexpensive refresh policies. In production A/B experiments, the system improves the primary ranking metric by +2.77% in search advertising and +2.1% on the Yandex Advertising Network, with revenue gains of +2.26% and +0.43% respectively - without increasing serving latency.

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
