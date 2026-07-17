---
title: 'From Clicks to Conversions: Architecting Shopping Conversion Candidate Generation at Pinterest'
source_url: https://medium.com/pinterest-engineering/from-clicks-to-conversions-architecting-shopping-conversion-candidate-generation-at-pinterest-04cae5e1455b
company: pinterest
date: '2026-04-27'
evidence_tier: 2
language: en
track: modeling
full_text: complete
---

**Authors:** Richard Huang, Yu Liu, Ziwei Guo, Andy Mao, Supeng Ge

## Introduction

Pinterest prioritizes conversion ads for matching users with purchasable products. The company's shopping ads historically relied on engagement-based models, which weren't designed to optimize for lower-funnel conversions. This motivated development of a dedicated candidate generation model for conversions. The first shopping conversion model launched in 2023, with further iterations in 2025 improving Return on Ad Spend for advertisers across Pinterest's 600+ million monthly active users.

## Training Data Design

Modeling conversion events presents challenges because offsite conversions are sparse, noisy, and delayed compared to frequent onsite engagements. The team made several key design decisions:

**Multi-Surface Model:** Training one model across all shopping surfaces (Homefeed, Related Pins, Search) prevents fragmenting sparse conversion labels while incorporating surface-specific features.

**Dual Positive Signals:** The model supplements conversion signals with onsite engagement data using a log-based re-weighting function based on click duration to mitigate noise and false positives.

**Negative Sampling:** Beyond in-batch negatives, ad impressions without engagement serve as harder negatives, reflecting real served ads distribution and promoting robust contrastive learning.

The multi-task approach uses engagement prediction as an auxiliary task to stabilize training while balancing tasks to prevent dilution of high-value conversion signals.

## Feature Engineering

User-side features split into context features capturing real-time intent and preference/historical features capturing long-term interests. Pin-side features incorporate ID features, multi-modal content features for semantic understanding, and performance features tracking engagement.

## Model Architecture and Loss Function Design

### Parallel DCN v2 and MLP Cross Layers Architecture

Early iterations used sequential architecture where DCN v2 cross network processed input first, feeding output into MLP for dimension reduction. The team hypothesized this imposed learning capacity limits. They designed parallel architecture with MLP running simultaneously, eliminating information bottlenecks. Both cross network and deep network learn directly from same input features, allowing cross network to capture richer explicit feature interactions while MLP learns implicit patterns. This design achieved "+11% gain in offline recall@1000" and was subsequently adopted by all production engagement retrieval models.

### From Multi-Head to Unified Multi-Task Architecture

The initial 2023 model used multi-head structure with shared encoders followed by engagement and conversion heads trained simultaneously using distinct sampled softmax loss. Through data analysis and experiments, the team identified conversion label sparsity and noise as bottlenecks. They moved to unified single-head multi-task architecture merging conversion and engagement heads, allowing final embeddings to benefit from multi-task optimization during serving.

The team also introduced advertiser-level loss function as additional training objective to address high variance in Pin-level conversion data. This approach achieved "+42% recall@100" compared to the 2023 model.

## Conclusion

The modeling journey addressed sparsity and noise of offsite conversion events through loss design and architectural innovations. Key decisions included unified model across surfaces and strategic use of conversion and click duration-weighted engagement data. The 2023 production launch delivered "2.3% increase in shopping conversion volume" and "2.7% lift for shopping impression to conversion rate." Beyond conversions, it improved user experience with "CTR increasing by 1.5%" and "CTR over 30 seconds rising by 2.2%." Further 2025 iterations achieved "3.1% improvement in RoAS for US shopping campaigns."

## References

The article references three sources including work on ads conversion optimization, graph representation learning (GraphSAGE), and Deep & Cross Network v2 research.
