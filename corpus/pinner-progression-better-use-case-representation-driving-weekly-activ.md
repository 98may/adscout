---
title: 'Pinner Progression: Better Use-Case Representation Driving Weekly Active User
  Growth at Pinterest'
source_url: https://medium.com/pinterest-engineering/pinner-progression-better-use-case-representation-driving-weekly-active-user-growth-at-pinterest-bd2131ab238a
company: pinterest
date: '2026-07-27'
evidence_tier: 2
language: en
track: modeling
full_text: complete
---

# Pinner Progression: Better Use-Case Representation Driving Weekly Active User Growth at Pinterest

Listen

Share

Part 1 of 2

## Authors

Personalization (Homefeed): Yuke Yan, Chuxi Wang, Andreanne Lemay, Olafur Gudmundsson, Anna Kiyantseva, Krystal Benitez, Jongho Kim, Jiacong He, Rahul Goutam, James Li, Dylan Wang User Understanding: Simin Li, Sufyan Suliman, Yingjian Ding, Hongbo Deng Data Science: Armando Ordorica, Yan Chen, Ellie Zhang, Karim Wahba

## Introduction

Pinterest’s mission is to help people discover the inspiration to create a life they love. Our recommendation system serves hundreds of millions of users, surfacing billions of Pins across interests ranging from home renovation to meal planning to wedding decor. The home feed , where much of that discovery happens, is powered by a multi-stage pipeline spanning retrieval, lightweight scoring, ranking, and re-ranking [1][2][3].

Most of our prior work on this pipeline has been optimized for engagement : clicks, saves, downloads, closeups. These are strong signals of immediate relevance, and optimizing for them has driven significant gains across the system [4][5]. The problem is that engagement and retention are different things. A user can save ten sourdough recipes today and churn next month anyway. All we did was feed them more of what they already liked: we never helped them find something new for next time.

This post is one of two that introduces Pinner Progression, a program that reframes the home feed recommendation system around retention as a first-class objective. Our core insight is that by augmenting sequential, action-by-action user understanding with holistic, persistent use-case representation, we can reliably anticipate the user’s next moves and start to serve recommendations that ignite their serendipitous discovery. In this post, we introduce the key use-case representation signal: User Interest Clusters (UICs) — and describe its construction, integration into the recommendation stack, and impact on engagement on retention metrics. A follow-up will cover how we predict unseen UICs and conduct systematic user-interest exploration.

## When Engagement Optimization Is Not Enough

Sustainable growth doesn’t come from purely chasing short-term engagement bumps, but from building lasting, repeatable relationships between users and specific use-cases. What sets apart our most reliable weekly active users is not the breadth of their activity, but strong habits formed around distinctive reasons to come back to Pinterest, such as DIY inspiration, recipe discovery, fandom engagement, etc.

As part of the motivation, we analyzed how changes in use-case adoption relate to changes in retention across users on our platform. The key learning was that use-case adoption captures durable and sustained engagement actions (e.g. multiple Repins and long clicks) beyond mere curiosity-driven shallow actions, and is therefore a good proxy for user value. More notably, we found the relationship is as expected, and non-linear. The retention benefit is modest for moderate increases in adoption but accelerates sharply at the top decile, suggesting there may be a threshold effect where breadth of adoption meaningfully compounds retention.

Modern recommendation systems are excellent at learning what a user likes right now . Transformer-based ranking models like TransAct [4] consume real-time action sequences; learned retrieval systems [1] encode long-term preferences into two-tower architectures; diversification layers [6] balance topic coverage within each session. These systems model the user as a set of recent actions in feature space, resulting in a feed that feels highly relevant to the present moment.

However, existing systems do not model the lifecycle of use-case that these recent actions represent. A user’s “apartment decorating” era might be accelerating (they just signed a lease), while their “sourdough” phase is decaying (they mastered the recipe months ago). To a point-estimate model, content in both categories looks equally engaging, but only the former is capable of maintaining or lifting the user’s visitation frequency in the long-run.

Instrumenting this distinction requires us to answer a novel question: what does this user need to see to sustain a long-term relationship with the platform? Our earlier work on multi-embedding representation in retrieval [9] showed us that it requires a richer representation than a single embedding vector. We need to see every use-case as having its own lifecycle: from being newly discovered, to gaining traction and becoming a regular habit, and finally either stabilizing as an evergreen activity or fading entirely as new use-cases supplant it.

## User Interest Clusters: A Stateful Interest Representation

## From PinnerSage/OmniSage to UICs

Pinterest has a strong lineage of multi-modal user representations. PinnerSage [7] introduced the idea of representing each user with multiple embeddings by clustering their engagement history and using cluster medoids as retrieval queries. This was a significant step beyond single-embedding models, enabling the system to capture diverse use-cases simultaneously. OmniSage [8] advanced this significantly via multi-entity graph representation, which fuses visual/semantic features, interaction graph signals, and Pin-Board topology into a unified representation.

Our new User Interest Cluster ( UIC ) representation has innovated on top of this foundation in three critical ways:

1. Personalized clustering over engaged content only. Rather than clustering in a global embedding space, we cluster over only the Pins a user has engaged with. This makes the problem tractable and the clusters semantically coherent: each cluster corresponds to a use-case the user is actively pursuing, not a region of the global content catalog. The exact same Pin with the exact same OmniSage embedding may end up in very different clusters for different users, representing the innately personal nature of what a “use-case” represents. See the following illustration whereby the last Labubu Pin means something very different for 3 different users.

2. Dynamic cluster count. Users don’t have a fixed number of interests. A new user exploring Pinterest for the first time might have two clusters; a power user planning a wedding, remodeling a kitchen, and training for a marathon might have fifteen. Motivated by the foundational work in our recent Multi-Embedding work [9], we let the clustering algorithm determine the natural number of clusters per user based on the coherence threshold, rather than forcing a fixed k .

3. Stateful lifecycle metadata. Each UIC carries temporal and behavioral metadata that allows the system to reason about where the interest is in its lifecycle. Traditional signals struggle to distinguish between fleeting curiosity and true emerging habits. Each UIC carries temporal and behavioral metadata (e.g. recency and frequency of engagement) that gives the system a starting point for reasoning about where an interest is in its lifecycle. While this does not fully solve the hard problem of distinguishing fleeting curiosity from a true emerging habit, it provides a structured signal that downstream layers (ranking, diversity) can use to treat interests differently based on their maturity.

## The Embedding Space

Each UIC is defined by both a medoid as well as a group of landmark Pins, all of which are represented in the OmniSage embedding space. The critical property of OmniSage [8] for our purposes is that “closeness” encodes functional utility as well as visual similarity. A hiking boot and a trail mix bar are neighbors in this space because they are co-curated on “Hiking Trip” boards and co-engaged by the same users. For UIC, this means that when we cluster a user’s engaged Pins in OmniSage space, the resulting clusters correspond to something coherent in the user’s life (planning a camping trip, redecorating a bedroom) rather than just visual categories.

## Signal Construction

To generate UICs, we collect each user’s recent engagement sequence — their last 500 actions on Pinterest, including closeups, saves, and clicks — and perform Complete Linkage Agglomerative Hierarchical Clustering on the action embeddings.

The algorithm starts with every engaged Pin in its own singleton cluster, then greedily merges the two most similar clusters until no remaining pair exceeds a similarity threshold τ (or the cluster count hits an upper bound). The key is the distance function: complete linkage defines the similarity between two clusters as the similarity of their least similar pair:

where cos(eᵢ, eⱼ) is the cosine similarity between OmniSage embedding vectors. A merge is only allowed if every point in cluster A is sufficiently similar to every point in cluster B.

At each step, the algorithm selects the cluster pair with the highest complete-link similarity above τ:

The process repeats until no pair exceeds the threshold or the maximum cluster count is reached.

A worked example. Consider a user who has engaged with five Pins: three cat images and two jeans images. The algorithm begins by computing all pairwise cosine similarities in OmniSage space:

The cat Pins are mutually similar (cosine similarities 0.7+), and the jeans Pins are mutually similar, but the cross-category similarities all fall below τ. The algorithm proceeds:

Step 1: Merge the two most similar Pins (two cat images, highest complete-link similarity). Now we have four clusters {p2} and {p3} because their cosine similarity is 0.755 which is >0.7:

Step 2: The jeans pair has the next highest complete-link similarity above τ. Merge them. Three clusters remain.

Step 3: Cat Pin₁ merges into the existing cat cluster — the complete-link similarity (the minimum pairwise similarity between Cat Pin₁ and both members of {Cat Pin₂, Cat Pin₃}) still exceeds τ. Two clusters remain.

Step 4: The only remaining pair is {cats} vs. {jeans}. The complete-link similarity (the minimum cross-pair) falls below τ. The algorithm stops.

## System-Level Integration

To make use-case-aware recommendations work in home feed, we needed to integrate the same UIC signal across multiple layers of the serving stack. Each stage solves a different problem: retrieval and early funnel determine what content is available downstream, ranking predicts which content is most likely to generate engagement value, and blending ensures the final feed has sufficient diversity between use-cases.

Our approach is to use UIC as a shared abstraction across these layers. To generate UICs, rather than representing a user with a single global interest vector, we represent them instead as a set of interest clusters, each corresponding to a distinct use-case. This lets different parts of the system reason about whether a candidate belongs to an established use-case, an emerging one, or a less developed one that may still be worth nurturing.

One of the most important design decisions at this stage was externalizing UICs to a shared feature store rather than coupling them to a single model. This means the UIC annotation of all the candidates in the funnel only needs to happen once, reducing unnecessary latency associated with multiple fetches of the signal. As a next step for improving the signal itself, we plan to extend UIC with a compact, information-dense long-sequence representation that preserves temporal dynamics (including decay) while staying efficient to compute, store, and serve.

## Retrieval

Our first integration point is retrieval. Conditional Learned Retrieval (CLR) [1] [2] generates candidates by combining user information with a “condition”, such as a board, Pin, or topic, to ensure semantic relevance between the retrieved Pins and the condition. Previously, one of the primary conditions was the topics that the user selected during onboarding called followed-interests. In practice, followed-interests skewed heavily toward a user’s dominant interests, retrieving large volumes of candidates in well-established categories while leaving smaller or emerging interests with little representation. The signal was also static as it did not evolve with a user’s changing behavior.

We replaced the followed-interest condition entirely with UIC clusters in a UIC-conditioned CLR. This makes retrieval more personalized because the conditions are derived from each user’s own engagement clusters rather than a global interest taxonomy, and more flexible because the system can control how many candidates are allocated per use-case (e.g. sampling 5 of a user’s 10 clusters and retrieving candidates for each). Early iterations selected a representative Pin (“landmark”) from each cluster using recency and action-type weighting, which was effective for relevance but inherently exploit-heavy. A later iteration introduced frontier sampling, which selects landmarks at the boundary of a cluster in embedding space, farthest from the medoid. This shifts retrieval toward a more exploratory distribution without sacrificing engagement.

In production, a key challenge of UIC-conditioned retrieval was effective budgeting to avoid overwhelming downstream stages. Because UIC clusters are scoped to a user’s currently active interests — clusters that contain recent engagement and exceed a coherence threshold — we avoid retrieving candidates for stale or decayed interests that are unlikely to convert. This reduced overfetch (broadly relevant but ultimately unused candidates) and translated to meaningful infrastructure cost savings, while keeping the total candidate volume sent to downstream stages unchanged.

## L1 Utility

L1 Utility is a control layer that sits between lightweight scoring (LWS) and full ranking, where we can impose global constraints on the candidate set before it advances downstream. Without intervention at this stage, the candidate pool tends to be dominated by a user’s most established interests; these Pins score highest in LWS because the engagement signal is strongest, leaving newer or growing use-cases with very few surviving candidates by the time they reach the ranker.

To address this, we annotate each candidate Pin with both its UIC assignment (via cosine similarity to UIC medoids). We then apply a penalty-based diversity mechanism: Pins that duplicate an already-well-represented UIC receive a discounted score, giving under-represented interests room to advance. Concretely, the L1 Utility score becomes:

where UIC_dupes count how many higher-scoring Pins share the same UIC assignment. This turned UIC from a passive feature into an active control surface: L1 Utility now shapes not only which Pins score well individually, but whether the overall candidate set represents a healthy spread of use-cases.

## Ranking

In ranking, UIC signals inform the utility function that converts raw Pinnability [4] model predictions into final ranking scores. The key idea of doing so is that the definition of a good recommendation changes depending on where an interest is in its lifecycle.

For a nascent interest the user is just beginning to explore, curiosity signals (clicks, closeups) matter more than commitment signals (saves). For a mature, stabilized interest, the reverse is true — the user wants depth and utility, not breadth. By making utility weights state-dependent, we align the ranking objective with the user’s actual needs at each point in their interest lifecycle, without adding new prediction heads to the ranking model (which would increase serving latency).

## Diversity

The final integration point of UIC is SSD (Sliding Spectrum Decomposition) during the Blending layer [6], which is the algorithm that determines the final ordering of Pins in a user’s feed. Prior to this work, SSD optimized variety at the individual Pin level — ensuring adjacent Pins looked and felt different — but had no awareness of the higher-level use-cases a user is engaged with. As a result, a feed could appear visually diverse while still being dominated by a single interest category (e.g., ten visually distinct “apartment decorating” Pins crowding out everything else).

We introduced a UIC-aware penalty term directly into SSD scoring. Each Pin is associated with a UIC by computing cosine similarity between its OmniSage embedding and each cluster medoid; the cluster with the highest similarity above a threshold (0.85) is assigned, and unmatched Pins fall into a default group. SSD then penalizes Pins proportionally to how much their UIC is already represented in the selected set:

where UIC_coverage_i is the fraction of already-selected Pins that share cluster i. As Pins are selected sequentially, the penalty for over-represented clusters grows with each selection. This means that Pins from under-represented interests are increasingly favored as the feed gets longer. In practice, this is how newer interests surface: not by overriding relevance at the top of the feed, but by naturally winning in later positions where the dominant clusters have already accumulated enough penalty.

In online experiments, UIC-aware SSD led to meaningful engagement gains, much more diversity of the content that was interacted with, and increases in longer sessions, confirming that balancing use-case representation translates to deeper engagement.

## What’s Coming

The UIC representation tells us where a user’s use-cases are today and how fast they’re moving. The natural next question is: where will they be tomorrow? In Part 2, we will describe our work on predicted UICs: generating future coordinates before the user explicitly signals a newly developed interest. This work spans three complementary approaches: geometric prediction strategies that leverage the structure of the embedding space, model-based serendipity prediction, and LLM-based interest reasoning. We will also describe the reinforcement learning feedback loop that governs systematic exploration, balancing the introduction of new use-cases against the risk of recommendation noise.

## References

[1] B. Deng, Z. Fan, D. He, et al. “Establishing a Large Scale Learned Retrieval System at Pinterest.” Pinterest Engineering Blog, 2025.

[2] Z. Fan, B. Deng, H Xia, Y. Yan, et. al. “Advancements in Embedding-Based Retrieval at Pinterest Homefeed.” Pinterest Engineering Blog, 2025.

[3] D. He, A. Liu, D. Badani, et. al. “Pinterest Home Feed Unified Lightweight Scoring: A Two-tower Approach.” Pinterest Engineering Blog, 2021.

[4] X. Xia, N. Gu, D. Badani, A. Zhai. “How Pinterest Leverages Realtime User Actions in Recommendation to Boost Homefeed Engagement Volume” (TransAct). Pinterest Engineering Blog, 2022; KDD 2023.

[5] X. Xia, S. Joshi, K. Rajesh, et al. “Next-Level Personalization: How 16k+ Lifelong User Actions Supercharge Pinterest’s Recommendations” (TransActV2). Pinterest Engineering Blog, 2025.

[6] J. He, D. He, J. Cheng, et al. “Evolution of Multi-Objective Optimization at Pinterest Home Feed.” Pinterest Engineering Blog, 2026.

[7] A. Pal, C. Eksombatchai, Y. Zhou, et al. “PinnerSage: Multi-Modal User Embedding Framework for Recommendations at Pinterest.” KDD 2020.

[8] A. Badrinath, et al. “OmniSage: Large scale, multi-entity heterogeneous graph representation learning.” Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V. 2. 2025.

[9] Z. Fan, et al. “Synergizing Implicit and Explicit User Interests: A Multi-Embedding Retrieval Framework at Pinterest.” Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V. 2. 2025.
