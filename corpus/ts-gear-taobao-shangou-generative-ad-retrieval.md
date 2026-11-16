---
title: 'TS-GEAR: Taobao Shangou GEnerative Ad Retrieval'
source_url: https://arxiv.org/abs/2611.12180v1
company: bytedance
date: '2026-11-09'
evidence_tier: 1
language: en
track: modeling
full_text: complete
---

# Computer Science > Information Retrieval

# Title: TS-GEAR: Taobao Shangou GEnerative Ad Retrieval

Abstract: On-demand delivery platforms such as DoorDash and Uber Eats impose a constraint absent in traditional e-commerce: merchants beyond the user's delivery range are invalid candidates rather than merely low-ranked. Generative retrieval has recently shown strong potential in large-scale retrieval systems. Adapting it to this setting, however, poses three challenges. First, existing semantic IDs encode geography only as a soft signal, so reachability can only rely on a non-differentiable post-generation hard truncation. Second, user preferences vary substantially across both regions and queries, so aggregating historical behaviors without conditioning on geography and the current query yields biased interest estimates. Third, the retrieved candidate set is evaluated by its collective value, yet autoregressive training scores each sequence independently, with no set-level signal to discourage redundant near-duplicates. To address the challenges, we propose TS-GEAR, a unified generative retrieval framework for on-demand delivery: (1) Geo-Semantic ID splits merchant identifiers into geographic prefixes and semantic suffixes, making reachability a prediction target rather than a post-hoc filter; (2) Query-Geo Target Attention aggregates historical behaviors using the real-time query and location as dual targets, while encoding each behavior's own location into its attention key; (3) GMPO (Group Marginal Policy Optimization) rewrites advantages using a deduplicated group reward and marginal advantage within GRPO, avoiding auxiliary diversity objectives. Deployed online with a lightweight 0.1B backbone, TS-GEAR serves over 150 million queries per day in the search advertising pipeline of Taobao Shangou, consistently outperforming state-of-the-art generative retrieval methods on both HitRate and geographic validity, and achieving 3.8% gains in ad impressions and 4.2% in ad revenue.

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
