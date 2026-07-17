---
title: GPU-Serving Two-Tower Models for Lightweight Ads Engagement Prediction
source_url: https://medium.com/pinterest-engineering/gpu-serving-two-tower-models-for-lightweight-ads-engagement-prediction-5a0ffb442f3b
company: pinterest
date: '2026-02-13'
evidence_tier: 2
language: en
track: modeling
full_text: complete
---

**Authors:** Yuanlu Bai, Yao Cheng, Xiao Yang, Zhaohong Han, Jinfeng Zhuang

## Introduction

Pinterest's ads recommendation system uses lightweight ranking as an intermediate stage to "efficiently narrow down the set of candidate ads before passing them to downstream, more complex ranking models." The platform employs a two-tower design where the Pin tower processes ads offline while the query tower generates user embeddings in real-time.

The company launched its first GPU-serving engagement prediction model in 2025. This new architecture combines Multi-gate Mixture-of-Experts (MMOE) with Deep & Cross Networks (DCN). The improvements yielded "a 5–10% reduction in offline loss compared to our previous production model for click-through rate (CTR) prediction." By separating standard and shopping ad scenarios, the team achieved an additional 5–10% loss reduction and doubled offline model iteration speed.

## Model Architecture

The redesigned model shifted from the previous Multi-Task Multi-Domain (MTMD) approach to an MMOE-DCN design. The MMOE structure uses "an MLP gating mechanism" to address multi-domain multi-task challenges. Each expert incorporates both full-rank and low-rank DCN layers.

## Training Efficiency Improvement

To address increased model complexity and larger datasets, the team implemented several optimizations:

- **Dataloader enhancements:** GPU prefetching and optimized worker thread counts
- **Code efficiency:** Direct GPU operations instead of CPU allocations and fused kernel usage
- **Training configuration:** BF16 precision adoption and increased batch sizes

## Evaluation

The model uses "prediction scores from downstream ranking models as training labels" and employs KL divergence as the loss function. Results demonstrated significant improvements across all metric slices both offline and online, with reductions in cost-per-click and increases in click-through rate.

## Conclusion

This launch represents "an important step forward in scaling our recommender systems with more complex, efficient, and effective models" through GPU infrastructure, architectural improvements, and training optimizations.

## References

[1] Li, Jiacheng, et al. "Multi-gate-Mixture-of-Experts (MMoE) model architecture and knowledge distillation in Ads Engagement modeling development." Pinterest Engineering Blog.

[2] Yang, Xiao, et al. "MTMD: A Multi-Task Multi-Domain Framework for Unified Ad Lightweight Ranking at Pinterest." AdKDD 2025.

[3] Kullback, Solomon, and Richard A. Leibler. "On information and sufficiency." The annals of mathematical statistics 22.1 (1951): 79–86.

[4] Pinterest Internal Data, US, 2025.
