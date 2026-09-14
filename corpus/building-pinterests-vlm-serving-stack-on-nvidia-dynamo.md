---
title: Building Pinterest’s VLM Serving Stack on NVIDIA Dynamo
source_url: https://medium.com/pinterest-engineering/building-pinterests-vlm-serving-stack-on-nvidia-dynamo-0dce6e93d0f3
company: pinterest
date: '2026-09-10'
evidence_tier: 2
language: en
track: modeling
full_text: complete
---

# Building Pinterest’s VLM Serving Stack on NVIDIA Dynamo

Listen

Share

Lei Pan | Senior Software Engineer; Salina Wu | Senior Software Engineer; Cristian Lopez | Software Engineer I; Guangtong Bai | Staff Software Engineer; Soam Acharya | Principal Engineer; Saurabh Vishwas Joshi | Principal Engineer; Chia-Wei Chen | Staff Software Engineer; Ambud Sharma | Principal Engineer

## Why VLM Serving Matters at Pinterest

Pinterest is a visual search and discovery platform, so its AI systems must reason over both language and visual content. Vision-language models (VLMs), which can interpret images, compare visual candidates, and respond naturally to user intent, are becoming the foundation for the next generation of Pinterest experiences: Pinterest Assistant, hybrid search, multimodal reranking, content understanding, signal generation, content safety, and more.

This direction also reflects Pinterest’s broader strategy to customize open-source models to meet its product & scale needs. Pinterest Assistant is a standout example. This multi-turn conversational experience covers both user language and visual content. Serving it requires low-latency VLM inference over rich multimodal context as well as reworking Qwen3-VL with proprietary multimodal embeddings to cut runtime cost while improving performance.

Serving VLMs, however, introduces more challenges compared to text-only LLM workloads. Requests may carry multiple images, require extra vision encoder computation, incur larger and more variable prefill cost, and create higher KV cache pressure. To support this new class of models & product experiences, we built Pinterest’s VLM serving stack on top of NVIDIA Blackwell GPUs and NVIDIA Dynamo. Blackwell GPUs incorporate many architectural innovations that are uniquely positioned for today’s most demanding AI workloads — including higher BF16/FP8 compute throughput, increased memory bandwidth, and larger HBM memory capacity — that enable dramatically higher performance for inference. Dynamo provides a distributed inference orchestration layer that gives us the flexibility to optimize multimodal workloads across the full serving path, including disaggregated encoder/prefill/decode serving, multimodal support in the Dynamo frontend and vLLM, multimodal KV-aware routing with custom payloads, and KV cache offloading.

## The Serving Challenge

As mentioned above, serving VLM for Pinterest use cases present several challenges:

Request payloads and preprocessing : For text-only serving, the request payload is just text (or tokens), so preprocessing is mostly tokenization plus applying a standard chat template; there are no external assets to fetch and no image-specific constraints. For VLM serving, the payload includes both text and images (URLs, base64, or precomputed embeddings), so the serving stack must download or load images, run image preprocessing (resize, enforce min/max pixels, normalization), map them into the model’s multimodal input format, and build prompts that mix both text and image content while inserting any required vision tokens or projectors, otherwise images get dropped or misinterpreted. Complexity is increased as requests include more images — Pinterest use cases sometimes require sending thousands of images per request.

Expensive prefill : In text-only serving, the expensive part is typically decode, with relatively modest and uniform prompt lengths, so KV cache pressure is more predictable. In VLM serving, requests often include many images or content items per query, which makes prefill dominant (encoding visual context is costly), drives much larger and more irregular KV caches, and requires our serving stack to support KV-aware routing, cache offloading, as well as careful prompt design to stay within latency and memory SLOs.

Multi-turn workloads : In text-only serving, multi-turn chat mainly increases prompt length and token costs but stays within a uniform text interface, so the serving logic is mostly about truncation and history management. In VLM serving, multi-turn workloads combine long dialog history with repeated or evolving visual context (e.g., revisiting or adding images/boards across turns), which makes prefill much heavier, complicates how visual state is represented across turns, and requires benchmarks and SLOs that reflect realistic multi-turn multimodal interaction patterns rather than single-shot prompts.

KV cache memory pressure : For text-only models, KV cache growth is driven by text token counts and is relatively predictable per request and per turn, so standard cache sizing and eviction often suffice. For VLM models, large visual contexts and long conversations can produce far bigger KV states per request, so serving must treat KV as a first-class constraint — using KV-aware routing, offloading, and disaggregated Encoder/Prefill/Decode designs — to avoid frequent evictions and maintain throughput under multimodal, prefill-heavy traffic.

Custom model and payload support : Text-only serving can often treat models as interchangeable behind a standard chat/completions API with generic JSON payloads and minimal per-model customization. VLM serving, by contrast, typically requires model-specific support for image fields, multimodal content arrays, projector layers (e.g., custom embedding projections), and custom routing or headers; the serving stack has to understand these payload shapes and model capabilities explicitly, and deployment artifacts and routers must be able to encode and route these richer, non-uniform multimodal requests correctly.

All of these VLM serving challenges required us to build a robust, flexible system that can meet our multimodal requirements. To build our serving stack, we relied on NVIDIA Dynamo’s multimodal serving capabilities.

## Scaling with Blackwell and Building on NVIDIA Dynamo

Pinterest has been an early industry pioneer in adopting NVIDIA GPUs for online model serving at internet scale, starting with recommendation systems and expanding into LLM and VLM serving. Token costs and performance matters significantly for the viability of these products. Building on that foundation, we standardized on NVIDIA Blackwell GPUs B200 due to their market leading TCO for LLM/VLM inference. Blackwell also makes our LLM/VLM hardware stack future proof as our use cases and models continue to evolve. This cutting edge hardware enables Pinterest to be able to continue to get better TCO over time as we explore quantizations, improved kernels and multi-node inference.

Our in-house Gen AI Serving Solution is an end-to-end customizable stack centered around NVIDIA Dynamo as the serving orchestration framework. We use the OpenAI Chat Completions API, model-based Envoy routing and a model-aware gateway, Model Router, to provide a centralized way for all customers to call our system, ensuring a smooth client experience. Under the hood, we use vLLM as our inference engine and Weights and Biases for model management. Our compute infrastructure, PinCompute, is built on Pinterest’s internal centralized platform infrastructure that leverages AWS Elastic Kubernetes Service (EKS) along with NVIDIA GPUs. With the help of the Infra org, we manage dedicated EKS clusters that host all Gen AI Serving use cases. Notably, this is one of the first PinCompute EKS (PEKS) use cases at Pinterest. The Dynamo operator and components are installed through Helm charts, and our Dynamo workloads use the DynamoGraphDeployment CRD deployed as K8s manifests. To tailor the deployments to Pinterest’s requirements we inject additional sidecars and add custom containers to support functionality like Envoy (service mesh), model loading, and metrics scraping.

Our journey to Dynamo started with evaluating several Kubernetes-native frameworks that we found easy to start with but lacked flexibility in traffic management or forced reliance on a single inference ecosystem. We ultimately selected Dynamo as it is Kubernetes native, compatible with Pinterest Kubernetes and service discovery solution, inference engine agnostic, provides a flexible traffic solution, and uses a performant Rust-based router. During this process we developed a close relationship with the NVIDIA Dynamo team who have provided us with exceptional support. Pinterest utilizes many key features of Dynamo that provide flexibility and performance optimizations when powering our Gen AI Serving Stack.

P/D disaggregated serving

Our platform uses disaggregated prefilling and decoding inference to tailor serving to specific latency requirements (Time-to-First-Token (TTFT) or Inter-Token Latency (ITL)), optimizing hardware allocation by separating the distinct computational phases of LLM requests. This architecture is particularly effective for unblocking product launches with high traffic volume and tight latency requirements, especially for TTFT. Dynamo provides an easy to use solution to orchestrate distributed, disaggregated inference that allows us to explore the Pareto curve between the ratio of encoder (E), prefill (P), and decode (D) workers.

KV cache offloading

We leverage KV cache offloading, specifically via LMCache, for multi-tier offloading to CPU memory and disk, which is critical in high QPS, multi-turn scenarios. LMCache serves as a sophisticated extension for the inference engine, providing tiered storage across GPU, CPU DRAM, and local disk (NVMe) to preserve generation latency while managing high GPU memory pressure. This tiered approach includes asynchronous prefetching and compression, contributing to lower TTFT and increased throughput by effectively managing long-context scenarios where visual tokens would otherwise overwhelm available VRAM. LMCache fits seamlessly into Dynamo as one of the many KV cache integration option for KV cache offloading

Multimodal support in Dynamo frontend/vLLM

Pinterest’s image-based products have specific multi-modal serving requirements. We worked closely with the NVIDIA Dynamo team to develop corresponding multimodality features, including a frontend image decoder, multi-modal disaggregated serving, and multimodal KV router support to reduce recomputation for VLMs. These enhancements enable the serving stack to handle complex multimodal payloads, such as base64 encoded images or image URLs, and perform necessary image preprocessing directly in the Dynamo frontend. Furthermore, the implementation of multimodal KV-aware routing allows the system to track prefix cache overlap for visual content, which is essential for maintaining production latency in multi-turn interactions with high visual token counts.

Custom modality support: Projection Embeddings

Pinterest Assistant workloads often need to reason over large visual contexts: Pins, boards, products, and other image-heavy inputs that may appear across multi-turn interactions. Sending all of that context as raw image pixels is expensive for VLM serving because each request may require image loading, decoding, preprocessing, and online vision encoder computation before the language model can use the visual information. To reduce that cost, we added support for projection embeddings using PinCLIP, Pinterest’s internal image encoder, for generating Pin embeddings. Instead of sending raw images through the serving path, Assistant requests can send precomputed PinCLIP embeddings. Dynamo and the underlying inference engine then run a projector that maps those precomputed embeddings into the target VLM’s native visual token space, letting us reuse visual representations that already exist for many Pinterest entities while avoiding the most expensive parts of pixel-based image serving.

The performance impact of this approach has been significant. Compared with pixel-based image inputs in Dynamo, incorporating projection embeddings into Dynamo have yielded results that are substantially faster across our benchmarks: average gains are roughly 85x faster TTFT, 7.3x faster end-to-end latency, and 1.1x faster TPOT. Peak gains are even larger, reaching approximately 369x faster TTFT, 44x faster end-to-end latency, and 2.6x faster TPOT. Just as importantly, this makes much larger visual contexts practical: requests with 250 images represented as PinCLIP visual tokens reached latencies comparable to pixel-based requests with roughly 10 images, while carrying 25x more visual context. Even at that scale, the serving profile remained reasonable and production-ready.

Supporting this required changes across the API, artifact, serving, and engine layers. We introduced an updated ChatCompletions request format for projection embeddings, defined a model artifact contract so training and serving teams could package projector weights, model weights, and configs together into a single model artifact, added the new modality path in vLLM alongside image and video to decode embeddings, validate types and shapes, invoke the correct projector, and insert projected visual tokens into the model input sequence, and updated Dynamo to accept and route the new request format while preserving the multimodal contract. Adding multimodal KV-aware routing support for our modality delivered meaningful tail-latency gains: the strongest result improved TTFT p99 by 5.92x, and across the full benchmark matrix Multimodal(MM) KV-aware routing delivered about 1.42x average speedup on TTFT p99. Additionally, because embedding payloads are larger than ordinary text inputs, vLLM frontend processing latency became a bottleneck in some cases; Dynamo’s Rust frontend helps by providing an efficient path for receiving, parsing, and forwarding larger multimodal payloads.

Tool calling Lastly, Dynamo fully supports tool calling with custom chat templates and multi-modal inputs, which is essential for providing flexibility for Pinterest’s agentic AI systems. This capability allows our agents to interact with internal tools and APIs in the Pinterest ecosystem, enabling more complex workflows that go beyond simple text for text and hybrid search, and other internal services. By leveraging custom chat templates, we can precisely define how the model should format its tool requests and handle the subsequent tool outputs, ensuring seamless integration with Pinterest’s internal services. Furthermore, the support for multi-modal inputs in tool calling means our agents can use visual information to inform their tool use, such as identifying an object in an image and then calling a specific search or recommendation tool to find similar products.

## Benchmarking Real Multimodal Workloads with AIPerf

We use AIPerf, NVIDIA’s distributed benchmarking tool for standardizing our AI inference performance measurement, as the execution layer for our performance benchmarks. AIPerf is designed as a modular benchmarking framework, which makes it a better fit for complex generative AI workloads than tools focused mainly on single request/response patterns.

This is especially important as both Pinterest and the broader industry move toward agentic AI systems. These workloads are rarely a single model call. They often involve retrieval, routing, multiple model calls, tool use, multimodal inputs, and intermediate reasoning steps before producing a final response. This allows our optimizations to have grounding data and guardrails on whether we are improving or regressing.

AIPerf’s DAG support is a big part of why it works well for us. Instead of flattening an agentic workflow into one artificial request, we can model the actual execution graph: nodes represent meaningful stages in the system, and edges capture dependencies between steps. This lets us benchmark workflows that branch, fan out, join, or depend on earlier outputs, patterns that are increasingly common in real AI applications.

Just as importantly, AIPerf lets us shape the benchmark traffic to look more like real production usage. We can run benchmarks with configurable QPS, realistic Poisson request arrival patterns, multi-turn interactions, multimodal inputs, and configurable prompt characteristics such as system prompt size, prefix length, input token length, and number of visual/embedding items. This makes the benchmark less about testing an isolated model call and more about understanding how the full workload behaves under realistic load.

Internally, we pair AIPerf’s execution output with Pinterest-specific reporting. We use the results to power dashboards and summaries for latency, throughput, token usage, success rate, per-request details, and aggregate comparisons. That gives teams a practical way to compare runs, catch regressions, and understand whether a model or deployment can meet production SLOs under realistic multimodal and agentic workloads.

## Product Use Cases Enabled

The VLM serving stack described above was built to support Pinterest Assistant, but the same architecture now serves as a reusable foundation for many GenAI and multimodal use cases across Pinterest. By standardizing on Dynamo for orchestration, vLLM for inference, and a common Chat Completions-compatible API, teams can launch new model-backed product experiences on top of this extensible serving platform.

## Pinterest Assistant: Real-Time Multimodal Interactions

Pinterest Assistant is one of the first major product use cases enabled by this stack. As a conversational agent, Pinterest Assistant needs to support natural multi-turn interactions while reasoning over Pinterest’s visual content. A user may ask for help refining an idea, exploring a style, comparing products, or finding inspiration based on a set of Pins or images. Unlike a text-only assistant, this requires the serving system to handle both dialogue history and multimodal context in real time. Pinterest Assistant inference runs on NVIDIA B200 instances, which showed a greater than 2x latency improvement over Hopper during preliminary benchmarking.

Pinterest Assistant also benefits from custom modality support such as projection embeddings. Instead of always sending raw image pixels through the serving path, Assistant requests can use precomputed visual embeddings for Pinterest entities such as Pins, boards, and products. This allows the model to reason over much larger visual context while avoiding repeated image decoding and vision encoder computation, making richer real-time conversations practical.

## A Shared Stack for Multimodal Product Patterns

As more Pinterest product surfaces adopt GenAI and multimodal models, this shared stack lets us support a growing range of patterns: conversational agents, re-rankers, OCR, safety systems, signal generation, and future VLM-powered experiences. The result is a serving platform that is not tied to a single product launch, but designed as a reusable foundation for multimodal AI at Pinterest.

Although Pinterest Assistant motivated many of the original requirements, the serving stack has grown to support a much broader set of use cases. Dynamo has become the out-of-the-box default for many GenAI serving workloads at Pinterest because it offers a flexible path for both text-only and multimodal deployment:

- Multimodal reranking uses VLMs to compare candidate content across textual and visual signals

- OCR workloads extract or reason over text in images

- Safety guardrails apply multimodal understanding to check whether responses or retrieved content meet product and policy requirements

- And more across signal generation, embedding-based workflows, and agentic systems

Dynamo’s LoRA hot loading has also accelerated experimentation under limited GPU capacity. Instead of standing up a separate full deployment per adapter — which increases GPU usage and operational overhead — client teams can load and evaluate multiple sets of LoRA weights dynamically against an existing base model. This shortens experimentation cycles and creates a smoother path from adapter training to production validation.

With a common serving foundation, teams reuse the same APIs, deployment patterns, routing layer, model management, observability, benchmarking, and GPU infrastructure rather than each building a custom solution. This gives product teams a paved path to focus on model behavior, integration, and evaluation. Dynamo is powering a reusable foundation for multimodal AI at Pinterest.

## Lessons Learned and What’s Next

In building our Gen AI Serving platform, we’ve learned that VLM workloads are fundamentally prefill-heavy and cache-sensitive: encoding large visual contexts and long histories, not just decode, drives both latency and GPU memory utilization, so KV-aware routing, cache offload tiers, and disaggregated serving need to be designed explicitly. Dynamo’s multimodal KV-aware router and E/PD disaggregation and LMCache-based KV offloading turned out to be essential. We also found that payload design and routing are core serving problems, not just interface glue: the way we encode multimodal content arrays, choose image resolutions, and structure prompts directly determines whether Dynamo can reuse prefixes, route efficiently, and keep TTFT within product targets. On the evaluation side, we learned that benchmarks must reflect real multimodal product traffic — including multi-turn conversations, many images per request, and agentic DAGs — so we invested in AIPerf-based DAG benchmarks that mirror production QPS patterns instead of synthetic single-shot prompts. Finally, a shared serving platform built on Dynamo, vLLM, and EKS has significantly accelerated experimentation: once the stack supported multimodal routing, KV offload, and model management, new use cases like Pinterest Assistant and multimodal reranking could launch by reusing the same paved path instead of re-inventing infra per team.

Looking ahead, we’re investing in several new directions.

AI Configurator: Dynamo’s AI Configurator is a performance optimization tool that can simulate 10K+ deployment configurations in seconds, finding optimal prefill/decode worker counts, tensor/expert/data parallelism settings, and deployment parameters. It evaluates both aggregated and disaggregated serving architectures, and uses hardware-specific performance models to predict TTFT, ITL, and throughput across different GPUs. This tooling can help us create optimized deployments with lower lift, increasing performance and developer velocity across teams.

Dynamo Planner: As our workloads scale, so will the need to introduce autoscaling in order to maintain a highly available yet cost-efficient compute infrastructure. Dynamo’s Planner will provide a VLM/LLM-optimized autoscaler, which dynamically adjusts prefill and decode replica counts through four optimization targets: throughput (static queue/KV thresholds), latency (aggressive low-latency thresholds), load (user-defined prefill queue and decode KV utilization thresholds), and SLA (regression-based models targeting specific TTFT/ITL values)

## Conclusion

NVIDIA Dynamo has given us a strong foundation for building Pinterest’s VLM serving stack and expanding it across emerging multimodal use cases. Its flexibility has been critical as we move from individual product launches toward a shared platform for production GenAI serving.

We’re excited to continue partnering with the NVIDIA Dynamo team and the broader community to push the limits of VLM and multimodal serving, and to make real-time multimodal AI systems faster, more efficient, and easier to deploy at scale.

## Acknowledgements

This work would not be possible without the contributions from our partners and collaborators. Our thanks to:

### Pinterest

AI Platform: Neha Upadhyay, Ananya Prabhu Angadi, Nazanin Farahpour, Howard Nguyen Product ML Infra: Li Tang, Yayun Wang, Archer Liu ATG: Yash Upadhyay, David Xue Cloud Runtime Team: Vaibhav Shankar CDP: Khoi Nguyen Traffic: Peter Leng, James Fish, Scott Beardsley Production Engineering: One Marino, Juan Pablo Daniel Borgna Product Management: Colin Leatherbury Leadership: Karthik Anantha Padmanabhan, Bo Liu, Roger Wang, Kartik Paramasivam, Matthias Zenger

NVIDIA Elijah Soba, Qi Wang, Anthony Casagrande, Guan Luo, Kris Hung, Ryan McCormick, Harry Kim, Akshatha Kamath, Matthew Rawson
