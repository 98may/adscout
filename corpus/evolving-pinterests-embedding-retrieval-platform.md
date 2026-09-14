---
title: Evolving Pinterest’s Embedding Retrieval Platform
source_url: https://medium.com/pinterest-engineering/evolving-pinterests-embedding-retrieval-platform-aede4e831e01
company: pinterest
date: '2026-09-11'
evidence_tier: 2
language: en
track: modeling
full_text: complete
---

# Evolving Pinterest’s Embedding Retrieval Platform

Listen

Share

Authors: Bowen Zhou | Staff Software Engineer; Shan Gao | Senior Software Engineer; Jingwen Hu | Software Engineer II; Wenjiang Chu | Staff Software Engineer

## The Billion-Embedding Challenge

At Pinterest, the “signal” is our lifeblood. Whether it’s a home decor enthusiast finding the perfect rug or a fashion seeker discovering a new aesthetic, our discovery engine relies on understanding deep semantic relationships to help our users find inspirations. Over the last few years, the explosive growth of embedding-based retrieval has fundamentally transformed how we surface these signals — and at the heart of that transformation is Manas, Pinterest’s in-house distributed search platform.

Embedding Retrieval is one of the core capabilities of Manas, supporting multiple approximate nearest neighbor search algorithms, hybrid queries with both token and embedding clauses, as well as real-time updates to ensure fresh contents become searchable within seconds. Deployed on over 80 clusters and serving billions of embeddings, Manas embedding retrieval powers all major product surfaces at Pinterest including Home Feed, Search, Related Pins, Ads, and Notifications.

However, as our corpus scales toward tens of billions of embeddings and our models capture increasingly complex interactions, we face mounting challenges around cost efficiency, scalability, and flexibility. On the infrastructure side, traditional ANN algorithms like HNSW are notoriously memory-hungry — they require the entire index to reside in RAM to maintain low query latency, making cost grow linearly with corpus size. On the modeling side, the classic two-tower retrieval paradigm is too restrictive: it reduces each candidate to a single embedding and scores relevance through a simple dot product, leaving little room to express richer, context-dependent notions of similarity.

To tackle these challenges, our team has been evolving Manas’s embedding retrieval stack across three fronts:

- Quantization. We reduce the memory footprint of embedding indices by compressing vectors into lower-bit representations with fewer effective dimensions. Quantization has been rolled out to all major use cases, delivering over 50% memory reduction in embedding indices and 20–30% cost savings in serving infrastructure.

- SSD-based Serving. Rather than holding entire indices in RAM, we serve ANN queries directly from SSD by carefully bounding the I/O per request — sustaining high throughput with low tail latencies at a fraction of the memory cost. Early experiments demonstrate a 10x reduction in memory usage and 40% CPU savings compared to in-memory serving

- Multi-embedding Retrieval. We move beyond the single-vector-per-candidate constraint of the two-tower model by supporting richer scoring functions that consider multiple embeddings per candidate. This unlocks more expressive ranking at the retrieval stage. We are currently partnering with a product team to launch a pilot use case.

In this blog post, we will delve into the technical details and results of each initiative, and discuss what’s next for embedding retrieval in Manas.

## Quantization: Redefining the Footprint of High-Recall Search

For a long time, serving embeddings in 16-bit or 32-bit float precision was considered the common practice. But at Pinterest’s scale, raw precision is a luxury that often provides diminishing returns. We discovered that quantization — transforming these high-dimensional float vectors into compact integer representations — is one of our most effective ways to better cost efficiency.

### Evaluating the Trade-offs: SQ vs. PQ

In the Manas stack, we focused our implementation on two primary quantization algorithms: Scalar Quantization (SQ) and Product Quantization (PQ) . The core of these methodologies lies in partitioning the vector space into disjoint subspaces and mapping each vector into an integer representation: SQ applies uniform discretization from float to integer per dimension, while PQ performs a K-Means clustering in each subspace and maps a subvector to the ID of the closest cluster centroid.

Benchmarks on a 100-million-embedding GraphSage dataset confirmed this intuition. We evaluated both SQ and PQ across two ANN algorithms (HNSW and IVF) and observed a clear trade-off: PQ achieves higher compression but with a significant recall decrease, while SQ delivers strong compression with minimal loss on recall.

- PQ reduces the HNSW index by 74% and the IVF index by 93%, with a recall in the range of 70–80%

- SQ reduces the HNSW index by 59% and the IVF index by 75%, with a recall over 90% consistently

Given the trade-off demonstrated by the offline benchmarking exercise, we ran online A/B experiments in production to select the best performing quantizer for each use case, and ensure negligible impact on user engagement metrics when enabling quantization. We launched SQ and PQ across major product use cases, reducing the total memory allocation significantly and realizing 20–30% cost savings for serving.

### Technical Deep Dive: SIMD and Linear Scaling

Shifting to 8-bit or 4-bit representations isn’t just a memory win; it’s a compute challenge. Usually, SQ requires a decoding step before distance computation, which can become a CPU bottleneck. To solve this, we implemented Linear Scaling SQ , which quantizes a vector by scaling only, and thus eliminates the decoding step before distance computation. The key enabler here is SIMD intrinsics, which allows the CPU to perform multiple 8-bit integer operations with each instruction, and hence reduces the total computing resources needed per query by 10–15% in our use cases.

## SSD Serving: Moving Beyond the Constraints of RAM

Our journey of improving embedding retrieval cost efficiency led us to exploring alternative ANN algorithms that take advantage of recent NVMe SSD performance advancements. The current generation of SSD devices are roughly an order of magnitude cheaper per gigabyte, but with the latency increased from nanoseconds to microseconds, which can slow down queries if I/O operations are not carefully managed. To bridge this gap, we experimented with I/O-aware ANN algorithms that were designed to minimize the number of random reads issued per query while retaining a recall score as good as memory-based algorithms.

### DiskANN vs. SPANN

In our experiments, we benchmarked two disk-based ANN algorithms, DiskANN and SPANN, with a 100M-embedding corpus collected from a Pinterest Search use case. While DiskANN is a robust graph-based approach, SPANN emerged as the better option for the Manas use cases.

Our team’s key observation was applying PQ quantization to the on-disk embedding store while retaining the full precision centroids helped the search accuracy and throughput significantly — a slight tweak from the original SPANN paper. This makes SPANN+PQ 4.5x faster than plain SPANN and achieves over 3x the QPS of DiskANN with 1/3 the latency, with a slight 5% recall drop.

### Implementing SPANN in Manas

We implemented the SPANN algorithm in Manas, which stores the centroid index in the memory and the large posting lists in the disk, and guarantees both disk-access efficiency (low latency) and high recall by effectively reducing the disk access number per request. In the index-building stage, we adopt the hierarchical balanced clustering algorithm from SPANN for selecting the centroids, which ensures evenly distributed cluster sizes, and hence similar lengths of posting lists to keep the tail latency low. We build the centroid index using HNSW, which is well-suited for in-memory search over a relatively small set of centroids. In a preliminary evaluation with a Pin recommendation use case that indexes over 5 billion embeddings, our SPANN implementation saves over 40% of CPU time for production queries when compared with HNSW, with a <5% recall drop. Our next step is to adopt SPANN across all major use cases.

## Multi-Embedding Retrieval: The Shift Toward Late Interaction

As we improve cost efficiency, we are also evolving the expressivity of the Manas embedding retrieval stack. The traditional “Two-Tower” model, while efficient, collapses an entire Pin or query into a single vector, often losing the nuanced, token-level semantics that define high-quality discovery.

### Contrast in Paradigms: Sum of MaxSim

We are now moving toward Late Interaction models , such as ColBERT. Unlike the single dot product of two-tower models, late interaction represents documents and queries as lists of vectors. We use the “Sum of MaxSim” scoring logic to capture the maximum similarity between each query token and the document’s tokens.

Integrating this into Manas required comprehensive changes in our serving stack. We integrated the multi-embedding retrieval as a new query type and updated Manas to handle multiple query embeddings rather than a single vector per query. This required updating the Manas query parser to understand these complex queries, as well as running multiple ANN searches from a multi-embedding query simultaneously. Currently, we are working with a client team to launch a pilot use case for the multi-embedding query support in Manas. This represents the next frontier of Pinterest search: moving from “two tower” to true model-based retrieval.

## Looking Ahead

The future of vector search at Pinterest lies at the intersection of infrastructure efficiency and retrieval model innovation. Over the next five years, our central goal is to evolve Manas embedding retrieval into an architecture that is scalable, cost-efficient, and open to new retrieval paradigms. We are pursuing this along three directions: adopting SPANN and SPFresh to push CPU and memory costs even lower for billion-scale indices; building first-class support for multi-embedding retrieval models like ColBERT that enable richer, interaction-based scoring at the retrieval stage; and embracing GPU-based retrieval systems like SilverTorch and TIGER to unlock new model capabilities.

## Acknowledgements

Many people from Core and Ads Delivery Infra teams contributed to the projects discussed in this blog post. Special thanks to Ellie Madsen, Jennifer Kong, and Jiawei Kuang for working on various Manas embedding retrieval projects. Thanks to our collaborators from client teams, including Bowen Deng, Jiaxing Qu, Ryan Hou, Minhazul Islam SK, Wei-Ting Lin, J.J. Hu, Konik Kothari, Yujiao Guo, Hanlin Lu, Bella Huang, Ai Zhang, Janvi Palan. Last but not least, many thanks to Van Lam, Tao Yang, Deeksha Sharma, Kartik Paramasivam, Abhishek Tayal, Zheng Liu for leadership support.
