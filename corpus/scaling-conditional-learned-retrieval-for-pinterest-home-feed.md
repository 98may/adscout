---
title: Scaling Conditional Learned Retrieval for Pinterest Home Feed
source_url: https://medium.com/pinterest-engineering/scaling-conditional-learned-retrieval-for-pinterest-home-feed-ecfba7e5a426
company: pinterest
date: '2026-08-26'
evidence_tier: 2
language: en
track: modeling
full_text: complete
---

# Scaling Conditional Learned Retrieval for Pinterest Home Feed

Listen

Share

Devin Kreuzer | Sr. Machine Learning Engineer; Yichi Wang | Machine Learning Engineer I; Sujan Reddy Ale | Machine Learning Engineer I; Zelun Wang | Sr. Machine Learning Engineer; Hongtao Lin | Sr. Machine Learning Engineer; Piyush Maheshwari | Staff Machine Learning Engineer

Pinterest home feed candidate generation is a large-scale User-to-Pin retrieval problem. A common approach is a two-tower model: a user tower encodes the user, an item tower encodes candidate Pins, and approximate nearest neighbor search retrieves Pins close to the user embedding. But Pinterest users often have multiple intentions at once — planning a renovation, saving recipes, exploring fashion, or organizing travel ideas. A single retrieval embedding can struggle to capture this diversity.

Conditional Learned Retrieval, or CLR, extends the two-tower setup by conditioning the user tower on an explicit retrieval context. Instead of producing only one user embedding, CLR can generate condition-aware embeddings that reflect different aspects of a user’s interests while still grounding retrieval in the user’s overall behavior.

Prior Pinterest work studied this formulation in two settings. The RecSys’24 paper: Bootstrapping Conditional Retrieval for User-to-Item Recommendations described how to bootstrap conditional retrieval by constructing training data for (user, condition) -> item retrieval from existing user-item and condition signals, and applied it to interest-based notifications. The KDD’25 paper: Synergizing Implicit and Explicit User Interests: A Multi-Embedding Retrieval Framework at Pinterest placed Conditional Retrieval within a broader multi-embedding retrieval framework for home feed, where explicit interest conditions complement implicit interests extracted from user behavior.

In this blog, we describe how CLR evolved from early interest-conditioned retrieval into a broader retrieval system for Pinterest home feed. We focus on three areas: expanding CLR to support more retrieval use cases, scaling the model foundations through sequence modeling and more general condition representations, and redesigning the serving infrastructure to make multi-condition retrieval efficient at production scale.

## Expanding CLR Across Use Cases

Increasing diversity of the retrieval candidates is a reliable source to drive engagement impact, because they provide a broad range of content for ranking and blending to work with. With CLR, this becomes scalable by either expanding to new types of conditions or providing new sources of conditions given a user.

To support each condition type, we need to train CLR models using (user, condition, engaged Pin) triplets. Fortunately we already have a few heuristic-based candidate generators in home feed that can help bootstrap these use cases.

Interest Conditions At Pinterest, we have a predefined interest taxonomy to categorize Pins. We initially launched CLR in home feed by sampling a few interests from user-to-interest signals. Later we leveraged a new user interest signal generated from LLMs as conditions.

Pin Conditions We later introduced Pins as conditions, by clustering users’ recently engaged Pins, selecting medoids of those clusters and leveraging pre-training embeddings to represent them in the model. In doing so, we were able to deprecate legacy heuristic CGs in favour of CLR; yielding impressive metric wins while simplifying our serving stack.

Board Conditions At Pinterest, users interact with Pins which are distributed across various Boards on the platform. We can think of Pins and Boards as forming a bipartite graph with Pins on one side, linked to Boards on another. By leveraging random walks, we can traverse this graph to recommend not only Pins, but also Boards to users. Similarly to the above, we then constructed Board conditions using pre-training embeddings in the same space as Pins to represent them, yielding large metric wins and simplified serving stack once more.

Agentic Condition Budget Tuning Following the migration to GPU-based serving, which significantly reduced latency and freed capacity, the team leveraged Claude Code to automate experimentation by continually reading experiment feedback to optimize the number of conditions inferred per request for CLR across Interest, Pin and Board conditions. By utilizing automated tuning policies, we successfully improved key engagement metrics including with low cost increase.

### Pin tower improvement: large id embedding table and semantic ids

ID embedding is an important feature in our recommendation systems. We began with using image signatures to represent Pin ids ( ref ), which behave like random hash numbers. Since this id space is huge (billion-scale), we ended up pretraining an id embedding table of size 20GB for sufficient memorization and tolerable collisions. We used TorchRec to shard this embedding table across multiple GPUs to support efficient training.

We later introduced semantic ids to complement image signatures. We built semantic ids by quantizing static content embeddings (PinClip fusion ref ) using residual-quantized VAEs. These semantic ids are hierarchical codes that cluster similar contents together, thus visually and semantically similar Pins could share nearby codes. Long-tail Pins suffer from cold start issues and limited training data. Semantic ids enable long-tail Pins to share the same id embedding space with popular Pins, thus can borrow their collaborative signal. Our semantic ids have five hierarchical layers, each layer has 2048 possible codes. Instead of using another large id embedding table, we found using five small embedding tables (one per layer) for these codes to be sufficient. After semantic id embeddings are looked up from these tables, we use a stack of five MLP layers to fuse these id embeddings sequentially. Finally, the image signature embedding and semantic id embedding are fed into the feature cross layer on the Pin tower.

## Scaling CLR Model Foundations

### Scaling User Understanding: From User Sequences to Foundation Models

Conditional user sequence transformer Early CLR models could condition retrieval on an explicit context, but the user representation was still largely built from static or aggregated features. This made it harder to decide which parts of a user’s recent history mattered for a given Interest, Board, or Pin condition.

To make CLR sequence-aware, we introduced a Conditioned User Sequence Transformer. The model converts raw condition features into condition tokens, appends them to the user sequence, and encodes the combined sequence with a Transformer. The condition token acts like a query over recent user actions, helping the model focus on the sequence signals most relevant to the retrieval context.

The Transformer outputs encoded condition tokens, encoded recent user sequence tokens, and raw condition features through a residual path, which are passed into the User Tower DHEN layer. This established the core abstraction for later model scale-ups: represent the condition as tokens, append them to user history, and encode the extended sequence.

The next step was to make this encoder more powerful. As CLR became more central to home feed retrieval, we wanted to capture richer action context, longer-term behavior patterns, and stronger alignment between user history and candidate Pins. This motivated the move toward a Foundation Model based CLR architecture.

Foundation model in CLR To capture deeper user sequence understanding, we upgraded the sequence encoder by integrating the PinFM ( ref ) into the CLR user tower. The Foundation Model is a large-scale transformer trained on global user action sequences across multiple Pinterest surfaces before being fine-tuned within the Unified CLR framework.

The foundation model uses a large ID embedding table in addition to OmniSage embeddings to memorize the engagement-oriented representations of Pins. This ID embedding table is reused even at the Pin tower to encode the candidate Pin. We believe that using this consistent representation of Pins on both sides of the tower will make it easier for them to align. To reinforce the pretraining objective during finetuning, we also use the next token loss during fine tuning as this helps the model adapt to the user sequence in the CLR dataset. We use positive actions such as saves, repins, sends and downloads to construct this loss. In addition to pooling the user sequence and condition outputs, we also apply an attention pooling to get a weighted average of the user sequence transformer outputs. This would give the feature cross an holistic view of the entire sequence.

We also introduce a contrastive alignment loss between the condition token representation and the candidate Pin representation. This encourages the condition token to be closely aligned with Pins embedding space, which makes it easier to rationalize a Query-key similarity in cross-attention.

### Scaling Condition Representation: Unified CLR and Router Simplification

As CLR expanded beyond its first use cases, the condition interface became an important scaling challenge. Supporting each condition type with its own model, feature, and serving setup would make every new condition more expensive to launch and maintain. To scale CLR, we needed the model to support heterogeneous conditions through a shared architecture.

Unified CLR The first step was Unified CLR. Before unification, home feed served separate CLR models for different condition types: Interest CLR used an interest ID in the user tower, while Board CLR used a board embedding. Both were effective, but maintaining separate models created duplicated work across training pipelines, feature upgrades, experiments, serving configs, and indexing.

Unified CLR consolidated these use cases into a single model trained on both interest and board conditions. The model was modified to accept multiple condition types, with missing condition features imputed by default values, and training used conditional filtering to focus on examples with valid conditions. This gave the team one shared foundation for future condition types, surfaces, feature upgrades, and model architecture improvements.

Router Simplification While Unified CLR brought our models under a single roof, the interface for defining conditions still suffered from an underlying scaling bottleneck. Historically, our routing logic was highly condition-specific. Introducing a new condition type (e.g., Board, Interest, or Pin) required adding bespoke features to the model and heavily zero-padding the master feature container. This legacy approach led to feature explosion, siloed learning, and high engineering maintenance overhead. To break this bottleneck, we refactored the routing logic into a condition-agnostic Slot Architecture. Instead of creating custom pipelines for every new condition, we bucketed incoming features into three predefined, shared slots:

- condition_os slot: Houses Omnisage-compatible embeddings (e.g., Pin OS, Board OS, or interest text embeddings).

- condition_id slot: Houses specific identifier embeddings (e.g., Interest IDs or Semantic IDs).

- condition_type_id slot: Encodes the condition type into a 32-dimensional learned embedding to preserve candidate generator identities.

## Scaling CLR Training Efficiency

Integrating a large-scale foundation model into the user tower significantly increased computational complexity. To maintain high developer velocity and support larger batch training, we introduced two key lossless infrastructure optimizations that increased our training throughput by 2x.

Request-level-training Within a single training batch, user features are often repeated across different candidate conditions. We deduplicate these identical user features using a unique combination of user-id and condition identifiers. This drastically reduces the effective batch size passing through the user tower. Post-forward pass, the generated embeddings are re-duplicated to match the original batch size for contrastive loss calculation.

M-Falcon Optimization Since we use causal attention, the representation of the user sequence is always independent of the condition tokens. So within a batch, we append all conditions for a user to a single user sequence and ensure the same user sequence is not redundantly computed in the batch. We use a custom block attention mask to ensure that condition tokens cannot attend to each other, while still allowing them to fully attend to the underlying user sequence. This drastically cuts the effective batch size moving through the transformer layers, lowering the GPU memory footprint for both ID embeddings and activations.

Attention mask

## Scaling CLR Serving Infrastructure

During initial CLR work, we treated each condition as an additional user-level feature — resulting in one model request per condition. As we began scaling to more and more conditions, the cost on our compute clusters was growing rapidly, and we achieved great cost savings and scale unlocking with the following methods:

Single Model Request Noting that each model request contains duplicate features, we optimized CLR serving by consolidating multiple separate CLR model requests per backend request into a single one with deduplicated request-level features. To achieve this, we modified the model’s TorchScript to batch these features internally and used Torch Jit to parallelize forward passes, shifting the bottleneck from network to CPU while keeping latency neutral.

GPU Serving + NVEmbed We optimized our logic further by shifting to a paradigm of CLR being a ranker of conditions, leveraging improved internal compute capabilities to form batches; where conditions are treated as items and user level features get broadcasted across these items. This allowed us to significantly simplify our models logic, align CLR inference with the “1 query — N doc” paradigm, mirroring our L2 ranker’s structure. We exported a CUDA-compatible model, deployed on g6e.4xlarge machines, and refactored the serving path — deprecating earlier model-side batch formation logic and improving output parsing.

Furthermore, to help serve and experiment with multiple large ID embedding tables post Foundation Model launch, our team has adopted NVEmbed; a framework for unifying embedding tables and dense models in a single servable torchscript artifact.

Key Wins & Impact:

- Financial & Performance: 7 figure cost savings and reduced p90 model latency by 85% (80ms to 12ms)

- Scalability: Unblocked major initiatives, including CLR FM and Search CLR, while enabling more conditions per user. 1

- Dev Velocity: The simplified infrastructure reduces technical debt and lowers the barrier for scaling future conditions.

## Future work

Looking ahead, we plan to continue scaling CLR beyond its current home feed use cases. CLR is designed to support multiple condition types through a shared model architecture; it can also serve as a foundation for retrieval across multiple surfaces. Expanding to new surfaces will also enable training on broader and more diverse training data. As we scale the training data, condition coverage, and model capacity, CLR can become a more general retrieval model for personalized learned retrieval across Pinterest.

## Conclusion

Conditional Learned Retrieval started as a way to add explicit retrieval context to Pinterest’s two-tower candidate generation system. By conditioning the user tower on signals, CLR helps home feed retrieve candidates that better reflect different aspects of a user’s intent.

Scaling CLR required us to make condition retrieval both more expressive and more efficient. On the modeling side, we improved how the system understands user behavior and represents different retrieval contexts. On the infrastructure side, we made it practical to evaluate many conditions per request to production scale. Together, these changes helped CLR grow from an early interest condition model to a broader retrieval framework for home feed, with a path toward more surfaces, condition types in the future.

## Acknowledgements

Matthew Lawhon, Zili Li, Matt Chun, James Li, Dylan Wang, Bowen Deng, Tao Mo, Nezanin Farahpour
