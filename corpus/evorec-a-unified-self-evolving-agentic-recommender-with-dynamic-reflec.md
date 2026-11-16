---
title: 'EvoRec: A Unified Self-Evolving Agentic Recommender with Dynamic Reflection
  Trees'
source_url: https://arxiv.org/abs/2611.01977v1
company: bytedance
date: '2026-11-01'
evidence_tier: 1
language: en
track: modeling
full_text: complete
---

# Computer Science > Information Retrieval

# Title: EvoRec: A Unified Self-Evolving Agentic Recommender with Dynamic Reflection Trees

Abstract: Conventional recommender systems rely on fixed cascaded pipelines, limiting their ability to adapt to evolving user needs and feedback. Existing agentic recommenders introduce reasoning and tool use but often lack end-to-end decision control and systematic failure reflection. We propose EvoRec, a unified agentic recommendation framework that combines autonomous decision-making with reflection-driven self-evolution. A Need Agent infers user needs from long-term, short-term, and working memory. A Planning Agent adaptively allocates retrieval budgets between Behavior Continuation and Need Satisfaction, selects retrieval tools, and sets ranking-fusion weights. An Acting Executor executes the plan and records decision traces. Following user feedback, a Dynamic Reflection Tree identifies failures in need inference, planning, or previous repairs, proposes personalized corrections, and validates them through replay. Verified repairs update working memory and are distilled into reusable cross-user strategies, enabling continual improvement without parameter updates. Experiments on a Kuaishou local-services advertising dataset show a 15.7% Hit@50 improvement over the strongest baseline. Hierarchical reflection further improves Hit@50 by 13.1% among users with prior repairs. In a seven-day online A/B test, nearline EvoRec increases advertising revenue by 4.6% and CTCVR by 3.5%, with a 14.5% revenue gain for high-intent users. These results demonstrate the effectiveness of reflection-driven self-evolution in industrial-scale recommendation.

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
