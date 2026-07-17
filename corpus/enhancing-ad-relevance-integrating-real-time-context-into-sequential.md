---
title: 'Enhancing Ad Relevance: Integrating Real-Time Context into Sequential Recommender Models'
source_url: https://medium.com/pinterest-engineering/enhancing-ad-relevance-integrating-real-time-context-into-sequential-recommender-models-bc3a2f9b682e
company: pinterest
date: '2026-05-08'
evidence_tier: 2
language: en
track: modeling
full_text: complete
---

**Authors:** Huiqin Xin, Lakshmi Manoharan, Karthik Jayasurya, Ziwei Guo, Alina Liviniuk

## Motivation: The Need for Real-Time Context

Pinterest Engineering previously introduced a sequential candidate generator using "a Transformer-based two-tower model to leverage a user's offsite conversion history." However, this system lacked online context awareness. User embeddings relied solely on historical behavior, meaning the model couldn't access what users were currently browsing on Pinterest.

This limitation proved critical for contextual surfaces like Related Pins and Search. "For example, on the Related Pins surface, if a user is viewing a Pin of a 'vintage leather armchair,' the recommended ads should be highly relevant to that specific item, not just their general, long-term interests." The previous production system saw less than 1% of Related Pins impressions attributed to this candidate generator.

## The Contextual Sequential Modeling Solution

The team developed the Contextual Sequential Two Tower Model to incorporate real-time context through three approaches: architectural changes, novel training methods, and hybrid serving flows.

## Model Architecture: Integrating the Context Layer

The updated architecture integrates "a context layer directly into the query tower of the two-tower model." The design concatenates Transformer encoder output with context layer output, feeding the combined representation into a final Multi-Layer Perceptron for user embedding generation.

For Related Pins, context inputs derive from the subject Pin's interest categories weighted by confidence scores. The user representation layer was enhanced with demographic embeddings including age, country, and gender.

## Model Training with Synthetic Context

Since real-time context only exists at serving time, the team employed synthetic augmented data during training. "During model training, we artificially inject pseudo-context information derived from the positive label (the conversion event) into the input sequence."

The approach uses high dropout rates in the context layer to ensure the model maintains reliance on historical sequences. The team chose synthetic data over real context due to technical challenges merging onsite and offsite data.

## Hybrid User Embedding Inference

The serving architecture splits inference into two components:

**Offline:** The majority of the user tower computes daily, storing "the last hidden state of the transformer" in feature storage for users with new offsite activity.

**Online:** The context layer and final MLP head compute at request time using real-time context features and pre-computed offline signals.

This enables embeddings that are "both personalized (from sequence) and contextually relevant."

## Results and Business Impact

### Offline evaluation

Testing on Related Pins using logged ad data showed substantial improvements. The contextual model achieved "a 3x to 10x increase in Recall@K compared to the production model," measuring positive items surviving the ranking funnel.

### Survival Rate & Relevance

The new approach successfully improved candidate survival on Related Pins. "The median relevance of the candidates went up by approximately 275–300%," with overall ads relevance improving by 1.08%. Candidate delivery increased 2x.

### Topline Business Metrics

The relevance improvements translated to business gains: approximately 0.7% measurable lift in Return on Ad Spend (ROAS). Top revenue countries achieved approximately 1.4% ROAS improvement.

## Future work

Planned enhancements include:

1. **Context Surface Expansion:** Extending the model to Search surfaces, where maintaining relevance between ads and search queries remains crucial.
2. **Advanced Fusion Techniques:** Moving beyond concatenation to implement cross-attention-based fusion, where context embeddings query sequential encoder outputs to "dynamically capture the importance of each history event based on the real-time context."
