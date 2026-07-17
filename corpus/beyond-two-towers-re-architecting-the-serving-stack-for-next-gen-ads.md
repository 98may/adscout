---
title: 'Beyond Two Towers: Re-architecting the Serving Stack for Next-Gen Ads Lightweight Ranking Models (Part 1)'
source_url: https://medium.com/pinterest-engineering/beyond-two-towers-re-architecting-the-serving-stack-for-next-gen-ads-lightweight-ranking-models-1992f2b76cbb
company: pinterest
date: '2026-02-02'
evidence_tier: 2
language: en
track: modeling
full_text: complete
---

**Authors:** Xiao Yang, Ang Xu, Yao Cheng, Yuanlu Bai, Yuan Wang, Sihan Wang, Ken Xuan

## Introduction

The industry has traditionally relied on "Two-Tower" model architectures for retrieval and lightweight ranking stages in recommendation systems. This approach involves "one neural network tower encodes the user, another encodes the item, and at serving time, the ranking score is reduced to a simple dot product between two vectors."

However, this efficiency comes with limitations. The structure struggles to leverage interaction features—detailed signals showing how specific users engage with specific items. It also prevents advanced patterns like target attention or early feature crossing, where "user and candidate features interact deep within the network layers rather than just at the very end."

To improve recommendation quality, Pinterest needed to deploy more complex neural networks capable of modeling deep interactions. This required introducing a GPU-based model inference stage into their existing serving infrastructure—a significant architectural challenge given latency constraints.

## The Challenge: Serving at Scale

Pinterest's traditional serving funnel followed these steps:

1. Feature expansion for thousands of candidates
2. Retrieval and lightweight ranking using Two-Tower dot products
3. Downstream funnel stages including heavy ranking and auctions

Simply adding GPU inference to this flow would have created unacceptable latency. The volume of data involved—"fetching features for tens of thousands of documents, serializing them, transferring them over the network to the GPU, running inference, and sending results back"—would have become a critical bottleneck.

The team recognized they needed to restructure the entire serving funnel, not just optimize the model alone.

## Optimization 1: The Feature Fetching Dilemma

Feature fetching at the lightweight ranking scale (handling 10,000 to 100,000 documents per request) significantly contributed to latency. Network I/O for fetching remote features often took longer than model inference itself.

Pinterest implemented an Inventory Segmentation Strategy:

**Segment 1:** For approximately one million high-value documents contributing significantly to revenue, features were "bundled directly inside the PyTorch model file as registered buffers." These features became part of the model's state, effectively residing in the GPU's high-bandwidth memory, eliminating network overhead during requests. The tradeoff involved reduced flexibility in feature updates, though the team plans to explore GPU-based cache solutions.

**Segment 2:** For the remaining one billion documents in the long tail, the team used a high-performance Key-Value store combined with in-host caching.

## Optimization 2: Moving Business Logic into the Model

Traditionally, models functioned as pure scoring engines, with serving systems handling business logic on the CPU. This meant "streaming scores for O(100K) documents back from the GPU to the CPU, only to have the CPU discard 99% of them after applying filtering logic."

Pinterest moved business logic—utility calculations, diversity rules, deduplication, and top-k sorting—directly into PyTorch models. This approach had multiple benefits:

- Reduced data transmission between device and host (outputting only ~1,000 final results instead of 100,000 scores)
- Full GPU parallelization of business logic calculations
- Feasibility because lightweight ranking business logic is "algorithmically straightforward enough to be efficiently implemented directly in PyTorch tensors"

## Optimization 3: Taming GPU Inference

Initial GPU inference showed unacceptable latency at p90 of 4,000 milliseconds. Through targeted systems optimizations, the team reduced this to 20 milliseconds:

1. **Multi-Stream CUDA:** Using different CUDA streams for different workers allows Host-to-Device transfers, compute kernels, and Device-to-Host transfers to overlap, eliminating serialization.
2. **Worker Alignment:** Aligning worker threads to physical CPU cores avoided costly context switching and lock contention.
3. **Kernel Fusion:** Utilizing Triton kernels to fuse common patterns (like Linear followed by Activation) reduced memory read/write operations, alleviating memory bandwidth pressure.
4. **BF16:** Brain Floating Point 16 format offered faster math operations and lower memory footprint compared to FP32.

Tools used included PyTorch Profiler and Nvidia Nsight Systems.

## Optimization 4: Rethinking Retrieval Data Flow

The legacy retrieval engine returned row-wise lists of heavy Thrift structures containing metadata for every candidate. At 100,000 documents scale, serialization and transmission became bottlenecks.

Pinterest split retrieval into two phases:

**Phase 1 (Lightweight):** The retrieval engine now returns a "column-wise, lightweight Thrift structure containing only the absolute essentials: IDs and Bids." This primitive-datatype structure serializes and transmits quickly.

**Phase 2 (Lazy Fetching):** Heavy metadata is fetched only for the final ~1,000 top-k documents after filtering.

Additional optimization involved auditing the metadata payload—deprecating one-third of unused fields and deferring another third to parallel processing with downstream stages. These changes achieved a 3x reduction in metadata size, lowering retrieval stage latency from 200 milliseconds to 75 milliseconds.

## Optimization 5: Graph Execution & Targeting

The system previously waited to fetch all features before beginning work. Pinterest optimized the execution graph by splitting feature expansion into two parallel paths:

1. **Targeting-Only Features:** A small subset required specifically for targeting and filtering
2. **Full Features:** The remaining features needed for ranking

This allowed targeting and filtering to start earlier, overlapping with heavier feature fetching processes. This graph optimization reduced end-to-end latency by an additional 10 milliseconds.

## Optimization 6: The Challenge of Online Metrics & Distribution Shift

During online A/B experiments, the team observed unexpected shifts in metrics despite not changing the lightweight models or ranking logic. Analysis revealed the root cause involved differences between local and global ranking approaches:

**Production (Local Ranking):** The retrieval engine uses a "root-leaf" architecture, partitioning documents across multiple leaf nodes. Each leaf retrieves a fixed quota and performs local ranking. The root node aggregates these locally-ranked winners, meaning "the final top 1,000 documents are not necessarily the global top 1,000; they are a composition of local winners."

**New Design (Global Ranking):** The GPU-based model processes all eligible documents in a single batch, performing true global ranking to select the top 1,000 candidates from the entire pool.

While global ranking is theoretically superior, this shift caused "a distribution shift in the makeup of the candidate set." Some metrics improved while others regressed due to "the composition of ads served to users had fundamentally changed." The team invested significant effort analyzing and tuning this distribution shift to ensure the new system met or exceeded production performance.

## Summary

Transitioning from CPU-based Two-Tower architecture to GPU-based general-purpose inference required complete re-architecture of their serving foundation. The work involved "a close collaboration between the modeling and infrastructure teams" driven by "a complete model-infra co-design philosophy."

By integrating features into model weights, moving business logic into neural networks, and redesigning data protocols, Pinterest maintained neutral end-to-end latency while introducing sophisticated GPU inference. "Early offline results already show step-function improvements in model performance, reducing loss by around 20%."

This foundation enables future modeling innovations beyond Two-Tower limitations, with the team promising additional technical details about their "Segment 2" solution in future publications.
