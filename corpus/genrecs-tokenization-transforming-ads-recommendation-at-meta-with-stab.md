---
title: 'GenRecs Tokenization: Transforming Ads Recommendation at Meta with Stable
  Model Vocabulary'
source_url: https://engineering.fb.com/2026/10/19/ml-applications/genrecs-tokenization-transforming-ads-recommendation-at-meta-with-stable-model-vocabulary
company: meta
date: '2026-10-19'
evidence_tier: 2
language: en
track: modeling
full_text: complete
---

- Generative Recommenders (GenRecs) represent a paradigm shift from scoring every ad to reasoning about ad content and user preferences together in order to predict the best outcome for advertisers. Leveraging the world knowledge built into LLMs makes ad matching more intelligent and precise, compounding gains for advertisers.

- GenRecs Tokenization is the foundational data representation that makes this possible. Rather than maintaining a dedicated ID for every item, GenRecs Tokenization represents each item with a set of tokens from a stable semantic vocabulary.

- Paired with Meta’s Generative Ads Model (GEM) and Meta’s Adaptive Ranking Model , GenRecs Tokenization has delivered a +0.35% lift in conversions across surfaces for advertisers.

GenRecs improves the way Meta’s ads recommendation systems make predictions today. Short for Generative Recommenders , GenRecs shifts our approach from scoring every individual ad candidate to leveraging LLM architecture to deeply reason about ad content and user preferences simultaneously. By pairing pre-trained world knowledge with a semantic understanding of what an ad actually represents, the system moves beyond click-pattern matching to understand underlying user preferences. This allows the model to predict the most relevant ad for each person, even when surfacing brand-new products with no past product, ad or company engagement history.

GenRecs Tokenization is the foundational data representation that makes this possible. Instead of maintaining a dedicated ID for every concept in the world, language models compose a small vocabulary of semantic tokens to represent any concept. Because tokens describe what an item (e.g., ads, products, services, etc.) is, the model can relate an item it has never seen engagement for, to items it knows well. A newly launched “trail shoe” inherits what the model has already learned about that category, rather than starting a new representation with no signal.

GenRecs Tokenization introduces a structured vocabulary approach for ad recommendations, enabling GenRecs for both retrieval and ranking across every item type in the system, including ads, products, pages, and pixels.

Meta’s state-of-the-art ads recommendation system drives ongoing advertiser performance improvements by learning about individual items and how they perform . LLMs present a unique opportunity to further improve the performance of recommendation systems by leveraging semantic tokenization in several ads use cases:

- Accelerating learning from new entities: Semantic tokenization helps models to infer relevance and establish relationships through shared concepts. New entities include newly created ads, niche products, and pages with limited engagement.

- Enabling cross-campaign transfer: Semantic tokenization creates a stable vocabulary that allows the models to carry insights across campaigns for advertisers.

- LLM scaling benefits: Semantic tokenization allows the benefits to compound with the LLM scaling curve’s improving performance.

- Infusing world knowledge: Semantic tokenization gives pre-trained language models a direct interface to reason about ad content and user intent.

Once items are migrated to semantic tokens, models learn from token patterns much like LLMs do. In production, this yields:

- Prediction accuracy improvements in production: Paired with Meta’s GEM and Adaptive Ranking Model , GenRecs Tokenization delivered a +0.35% lift 1 in conversions.

- Compounding feedback loop: Better tail predictions yield better lessons from tail ads which enrich the training data to further improve predictions for all ads from the model, creating a performance improving feedback loop.

- A new way to scale: Across production ranking and retrieval, tokens bend the scaling curve along sequence length, training data, and model architecture.

1 Meta Internal Data, measured in February 2026.

## Introducing GenRecs Tokenization

Pre-trained multimodal models read each ad, product, and page, including its text and images, and encode the items into an embedding that carries world knowledge. The tokenizer combines that content signal with representations learned from how people engage with the items, then quantizes the result into a short sequence of discrete tokens. Similar items share tokens, much as related words share roots. For example, there’s overlap between two running shoe ads from the previous season to the current season, so the new campaign immediately benefits from everything the model has already learned about the previous season’s products.

At the heart of GenRecs Tokenization is a three-stage pipeline that:

- Encodes each item into a semantic embedding space.

- Decomposes that embedding into independent subspaces.

- Quantizes by mapping each subspace to an entry in a codebook.

Maximizing ads recommendation quality requires diverse combinations of these stages depending on entity and feature semantics. For example, for many ad representations, GenRecs Tokenization uses prefix n-grams that combine a learned encoder, residual decomposition,  learned vector codebooks, and token parametrization .

## Token Quality Predicts Ranking Accuracy

Independently of downstream ranking gain, tokenizer model quality can be evaluated against intrinsic measures like:

- Cluster purity: The items that share a code tend to share a category, giving the model a cleaner signal per token;

- Distribution balance: Items spread evenly across semantic IDs instead of crowding into a few.

- Codebook utilization: A larger share of codes holds at least one item, so the vocabulary expresses more distinctions.

Across the eight tokenizer versions we tested, we see a strong correlation between these intrinsic quality metrics and downstream ranking prediction accuracy. Tokenizer versions that scored better on these metrics also had better CTR prediction accuracy for ads models.

## The Tokenization Flywheel

Tokenization maximizes the efficiency of high-volume campaigns by uncovering deeper semantic patterns across their vast product catalogs. For tail ads that accumulate fewer impressions, tokenization enables ads recommendation models to generalize across them via shared content structure, recovering cold-start performance and enabling cross-entity transfer. When a sportswear brand launches next season’s trail shoe, tokenization lets the new product and its ads build on what the model learned from last season’s shoe, even before anyone sees the new ad.

By improving tail ad prediction quality, tokenization not only lets tail ads be ranked accurately, but also improves the training data, which then improves prediction quality for all ads. Each pass through this self-reinforcing flywheel improves the quality of model predictions.

## The Foundations of LLM Recommendation

Tokenizer improvements are not confined to the model they were tuned for. Optimizing codebook quality through diversity loss, dead code resets, and contrastive objectives produces measurably better downstream performance when the resulting tokens train generative recommenders. Our work on LLM-native retrieval shows how far this can go. A two-tower architecture built on a shared LLM encoder reaches state-of-the-art retrieval quality while remaining efficiently servable, matching classic two-tower performance on a fraction of the training data. Building on this, we are now extending reasoning-aware ranking on top of the same vocabulary.

## The Future of GenRecs Tokenization

We are continuing to push GenRecs Tokenization toward the ROI-optimal frontier along three directions:

Deepening cold-start generalization: Tail ad inventory is where semantic tokens contribute most and where advertiser impact is largest. We are scaling the coverage of tokenization across all items to deliver better performance to advertisers.

Treating tokenizer quality as a first-class objective: Engagement-aligned training, unified cross-entity vocabulary, and codebook improvements are active areas of investment. Because intrinsic quality measures predict downstream ranking gains, we can iterate on the tokenizer without waiting on a full model training cycle.

Serving LLM-native architectures efficiently: Fully verbalized tokenization gives a model the richest view of an ad, but requires context windows that are impractical at ads scale. We are combining compacted verbalized tokens with semantic IDs to retain reasoning quality while maintaining acceptable latency.

Looking further out, we are exploring whether the same vocabulary that improves ads ranking today could unify representation across surfaces. A shared token space spanning ads content across text, image, audio, and video, would let models reason about what a person is interested in and what an advertiser has to offer with one representation, rather than stitching together separately learned embeddings.

As recommendation systems evolve from discriminative scoring to include generative reasoning, the data foundation benefits from evolving from ephemeral IDs to stable semantic representations. GenRecs Tokenization provides the foundation, translating the complexity of Meta’s ads ecosystem into a vocabulary that generative models can learn, reason about, and generate from.

## Acknowledgements

We would like to thank Weifeng Cui, Ling Leng, Luke Simon, Hadar Ohana, Jimmy Chen, Minghai Chen, Chiyu Zhang, Dinesh Ramasamy, Debajyoti Roy, Shawn Shi, Gajanan Golegaonkar, Xiao Yang, Ashkan Aleali, Anuj Gargava, Xizhou Feng, Liquan Huang, Frank Shyu, Xiaoyu Chen, Kungang Li, Chonglin Sun, Matt Steiner, Sandeep Pandey,  Santanu Kolay, Anuj Madan, Tak Yan, and the entire team behind the development and productionization of the first large scale semantic tokenization effort in Meta’s ad recommendation system.

The post GenRecs Tokenization: Transforming Ads Recommendation at Meta with Stable Model Vocabulary appeared first on Engineering at Meta .
