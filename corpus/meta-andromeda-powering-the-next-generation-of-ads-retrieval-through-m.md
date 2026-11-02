---
title: 'Meta Andromeda: Powering the Next Generation of Ads Retrieval Through Model-System
  Co-Design'
source_url: https://engineering.fb.com/2026/10/28/ml-applications/meta-andromeda-next-gen-ads-retrieval-gpu-co-design
company: meta
date: '2026-10-28'
evidence_tier: 2
language: en
track: modeling
full_text: complete
---

- This post describes the next generation of Meta Andromeda, Meta’s personalized ads retrieval engine, and how co-designing the model, system, and GPU hardware unlocks a new efficiency frontier for ads retrieval.

- In production, the system scores every eligible ad with near ranking-level model performance at retrieval scale and surfaces the top candidates at over one billion ads per second, a new throughput benchmark for ads retrieval-stage models (i.e., a 100x lift compared to the 2024 Meta Andromeda system).

- For advertisers, this means better performance automatically from the retrieval system matching ads across a larger candidate pool, within the same latency budget. Since 2025, Meta Andromeda has delivered a 2.4% increase in conversions on Facebook.

Meta Andromeda is Meta’s machine learning system for personalized ads retrieval, the first stage of the ads recommendation pipeline. Retrieval narrows a vast pool of eligible ads down to a small set of strong candidates in milliseconds; a later, more computationally expensive ranking stage then scores those survivors in fine detail.

Historically, the deep modeling quality of the ranking stage has been too costly to apply at retrieval’s scale. Building on the retrieval foundation established with Andromeda’s 2024 launch on the NVIDIA GH200 Grace Hopper Superchip, this post shares how co-designing the model, system, and hardware together brings near ranking-level performance to the retrieval scale.

## Challenges and Opportunities in Scaling Retrieval

The 2024 Andromeda deployment reimplemented retrieval with an end-to-end optimized retrieval implementation from custom AI hardware with hierarchical indexing and GPU-native operators to a purpose-built ML model, growing model capacity by four orders of magnitude. Since then, generative AI creative tools have helped advertisers rapidly create hundreds of millions of new ads, growing Meta’s ads candidate pool to an unprecedented scale.

Scoring such a large ad candidate pool with a more accurate model at a much higher system throughput requires fundamental technology breakthroughs in model quality, system architecture, and hardware utilization jointly.

### Higher Model Performance Requires a New Architecture

Ads retrieval has an outsized ROI on incremental quality: Small improvements in retrieval model performance can drive large gains in advertiser value. The rapid expansion of our ads candidate pool makes optimizing for hardware capacity ROI an increasingly critical factor. The 2024 Meta Andromeda retrieval models have established a highly effective foundation with their GPU-optimized deep neural network architecture. To keep improving retrieval performance at a sustainable compute cost at our current scale, however, we must move beyond that paradigm. This requires a fundamental architectural evolution to push model performance boundaries significantly without a proportional increase in costs.

### New System Bottlenecks at Billion Scale

The 2024 Meta Andromeda system evaluates at tens of millions of ads per second per GPU card. Meeting the new business demand requires a throughput at multi-billion ads evaluated per second per card in the system. At billions of ads per second throughput, the memory bandwidth of passing ad tensors through memory hierarchy becomes the new bottleneck. Intermediate tensors between GPU kernels account for terabytes per second of memory traffic, and shipping ads between local CPU hosts and remote hardware accelerators evaluating models saturates the network link. This requires a new system co-design that unifies these fragmented, distributed workloads into a single GPU pipeline.

### Pushing Towards the Hardware Limits

With retrieval running on GPU, the important optimization question is “How close are we to the hardware ceiling, and how much room remains for future model growth?” Answering this requires pushing each component of the retrieval pipeline to the limits of the current hardware generation, a challenge that motivated a joint collaboration with NVIDIA.

Each of these challenges drove a corresponding advance.

## Unlocking Retrieval Performance Through Model-System Co-Design

### Next-Gen Retrieval Model Architecture — Retrieval Mixture-of-Experts

The latest iteration of Meta Andromeda introduces three synergistic architectural innovations that bring large language model (LLM)-inspired mixture-of-experts (MoE) into the retrieval (see Figure 1). With this highly expressive yet inference-efficient architecture, a new retrieval performance-efficiency Pareto frontier has been established: model performance approaches ranking-level in a typical retrieval-then-ranking system, at approximately 300x fewer inference-time FLOPs than the 2024 Meta Andromeda retrieval model.

On the user modeling side , we transitioned from a single user tower to an ensemble of specialized user towers as experts. This captures diverse, time-evolving, and contextualized user interests by integrating a vast array of high-fidelity signals: sequential ad engagement events, user-cohort representations, LLM-derived semantic features, and cross-surface co-engagement signals.

In the candidate ads tower , we employ a joint encoding strategy that incorporates real-time serving context, ensuring that downstream interaction models receive context-aware representations.

In the interaction overarch layer , the interaction model evolved from dense neural networks into an MoE attention-based gating network that dynamically routes candidates across the most relevant user experts, delivering near-ranking-level performance at a fraction of the FLOPs.

A defining property of the new architecture is that its performance is co-designed with the underlying hardware execution model. Model inference throughput has reached over 10 billion ads per second on a single GH200 GPU, and this efficiency allows model capacity to grow further, through richer feature interactions, additional expert sub-networks, and deeper architectures, without a proportional increase in GPU cost. Each incremental model advancement translates into greater advertiser value.

### Co-Designing the Model and System Onto a Single GPU Pipeline

The 2026 Meta Andromeda pushes the model-system co-design to the next level with two innovations — a single GPU kernel fusing both model and system workloads per user-ad interaction and a strategy to co-locate per user request logics with per user-ad GPU kernels in a single GPU box. To this end, a highly optimized and fully fused GPU pipeline is built to host the entire end-to-end Meta Andromeda workflow.

At a high level, Meta Andromeda’s inference time per user-ad workload is a compact sequence of operations across model execution and system logics — gathering embeddings, executing user-ad interaction models, and scoring. The ~300x FLOPs reduction in the retrieval MoE gating architecture creates the necessary headroom and is less resistant to fully fuse both model execution and non-model system workloads into a single GPU kernel, compared to the 2024 launch where only operations within the model execution were fused. Consequently, the fused kernel now runs at over 10 billion ads per second on a single GH200.

This matters because retrieval workloads are fundamentally memory-bandwidth bound. At billions of ads per second, even a small intermediate tensor per ad multiplies into terabytes per second of high bandwidth memory (HBM) traffic. The memory workload of these intermediate tensors, not arithmetic, becomes the dominant bottleneck in multi-kernel retrieval pipelines.

The fused kernel eliminates this bottleneck entirely. Rather than dispatching multiple small GPU kernels for model and system operations, it executes the entire per user-ad computation in one pass. Intermediate results stay in GPU registers and thread block shared memory and are never materialized to HBM, achieving high utilization of the GPU’s peak memory bandwidth rather than wasting it on redundant intermediate traffic.

Measured in isolation, the per user-ad fused kernel runs at multi-billion ads per second on a single GPU. However, per-user request operations such as the index matching (i.e., enforcing advertisers’ targeting rules) and top-K selection run on separate local CPU hosts and communicate with the fused GPU kernel scoring service on remote accelerators through the network connection. At multi-billion ads per second throughput, this traffic alone saturates the network link, making the network bandwidth become the bottleneck rather than GPU compute.

The co-design response was to collapse the system architecture to match the model architecture: co-locate index matching, scoring, and top-K selection on the same GPU. Instead of shipping large candidate lists across hosts, the system sends a compact request payload — user features and a targeting query — to a single GPU server, which runs the entire retrieval pipeline locally and returns only the final top-K results. This reduces network traffic by ~100x and shifts the system back to a GPU-compute-bound regime.

Moving index matching onto the GPU is not straightforward. Ads index matching evaluates complex advertiser-defined targeting logic across tens of feature categories, and must support real-time index updates as ads are created, modified, or expired throughout the day. Supporting this on GPU required redesigning the index structure for GPU-parallel execution while preserving the full fidelity of production targeting semantics.

A Single GPU Pipeline for Meta Andromeda

Combining the aforementioned two innovations, the fully co-located single GPU pipeline processes over one billion ads per second on a single GPU server while scoring every eligible ad in the candidate pool. This is a new throughput benchmark for ads retrieval-stage models, and as the next section describes, significant headroom remains.

### GPU-Accelerated Retrieval: The Meta-NVIDIA Collaboration

With the production pipeline running at over one billion ads per second, a natural question follows: How close is the system to the ceiling of the current generation hardware, and how much headroom remains for future model growth? In early 2026, Meta and NVIDIA launched a joint collaboration to answer this question — systematically optimizing each component of the retrieval pipeline to push throughput toward hardware limits. NVIDIA contributed optimized GPU kernels, and Meta integrated and benchmarked the full pipeline. Each component achieved 2x to 5x speedup over the baseline.

The optimized gating kernel improved by 5.3x, from 2.4 billion to over 10 billion ads per second, reaching ~85% of the GPU’s peak HBM bandwidth. At this throughput, the execution time / latency of the gating mechanism is just as fast as what a simple dot-product scoring kernel achieves on the same hardware — while the model is substantially more expressive. This is the co-design validation: the additional model complexity is essentially free on Tensor Core hardware. INT8 quantization achieved a further up to 2x throughput increase over the optimized FP16 kernels, with accuracy on par with 16-bit precision.

Through targeted GPU kernel optimizations, index matching throughput improved over 2x, reaching over 100 billion ads per second — an order of magnitude higher than the scoring network. This headroom means index matching can be re-run across multiple retrieval pathways without becoming a bottleneck.

Beyond individual kernels, the collaboration profiled the full retrieval flow and identified that data movement between pipeline components — not computation — accounted for a significant fraction of end-to-end latency. By co-designing data layouts across index matching and scoring to eliminate unnecessary indirection, the team removed this overhead. With all optimizations applied, the full pipeline benchmarks at multiple times the current production throughput on a single GPU server, with further gains expected as additional optimizations integrate into production.

Building on the Hopper results above, we are extending our optimization and co-design work to Grace Blackwell. Here, we are focusing on platform design optimizations that enable different CPU-to-GPU compute ratios, which our work so far suggests is an important factor for Andromeda-like workloads. We are evaluating how sensitive end-to-end application performance is to these ratios, using Grace-class CPU performance and Blackwell-class GPU performance for their respective parts of the workload.

More broadly, we are exploring how these findings extend to the next platform generation, where greater flexibility in CPU+GPU execution, resource ratios, and coupling could bring more of these architectural improvements to bear on Andromeda-like workloads.

These results confirm that the co-designed retrieval pipeline is not yet at its ceiling. With quantization unlocking further scoring throughput and index matching operating at an order of magnitude above the scoring network, the architecture is positioned to absorb significantly more model complexity — deeper interaction networks, richer feature spaces, and additional retrieval pathways — without proportional infrastructure growth.

## The Path Forward for Ads Retrieval

The advances described here follow a single principle: The largest gains come from designing model, system, and hardware as one integrated stack, rather than optimizing each in isolation. The retrieval MoE gating architecture delivers near-ranking-level expressiveness at no additional serving cost. Fusing the entire retrieval pipeline onto a single GPU eliminates network and memory bottlenecks. And pushing the pipeline towards its hardware ceiling confirms substantial headroom remains.

Looking ahead, the co-design principle that drove these results applies equally to next-generation model architectures and hardware platforms, with the demonstrated headroom enabling continued scaling without proportional infrastructure growth.

For people who use Meta’s products, this translates directly into better ads that are more relevant to them, delivered within the same latency budget. For advertisers, it means better customer matches and more conversions. For Meta, it means increased business from advertisers and lower costs, as each GPU now evaluates more ads per second. As the volume of eligible ads continues to grow, driven by Advantage+ automation and generative AI creative tools, Meta Andromeda’s co-designed architecture scales to meet it.

## Acknowledgements

We would like to thank Gosh Arzumanyan, Habiya Beg, Andrew Bocking, Zain Brohi, Rohit Chandel, Claire Chen, Jason Chen, Wenlin Chen, Zhenyu Chen, Yuze Dai, Zhou Fang, Junjie Feng, Stephen Fitz, Chunli Fu, Yicong Fu, Xiaorui Gan, Sohan Gantala, Yingsheng Gao, Golnaz Ghasemiesfeh, Ishu Goyal, Wentian Guo, George Han, Yihan He, Jun Hu, Xuan Hu, Kun Huang, Qin Huang, Tianchen Ji, Crystal Jin, Tao Ju, Rajat Karnwal, Santanu Kolay, Michael Kwan, Ilia Lewis, Baiyu Li, Chao Li, Jim Li, Li Li, Lin Li, Liyuan Li, Mingda Li, Ted Li, Xiaotian Li, Yanyu Liang, Yue Liang, Irene Liu, Gaoxiang Liu, Jason Liu, Siqi Liu, Wei Liu, Xiao Liu, Yuheng Long, Yining Lu, Siyi Luo, Anuj Madan, Swaroop Manjunath, Phalguna Mankar, Jiachen Mao, Yuji Mo, GP Musumeci, Guruswamy Namasivayam, Kexin Nie, Sandeep Pandey, Uladzimir Pashkevich, Clementine Plati, Heng Qiao, Hang Qu, Lei Qu, Anand Rajan, Jatin Sethi, Puneet Sharma, Ruchit Sharma, Yan Shi, Chang Shu, Sean Song, Alec Stashevsky, Matt Steiner, Zheng Sun, Nikhil Vinayak Supekar, Jim Tao, Chintan Thakkar, Tian Tong, Aleksandr Ulanov, Daksh Vasistha, Simha Venkataramaiah, Arunprasad Venkatraman, Abhishek Verma, Ruud Vinke, Vidhoon Viswanathan, Sasha Vorontsov, Eric Walden, Dong Wang, Feng Wang, Haole Wang, Jeff Wang, Senhong Wang, Ye Wang, Di Wu, Haocheng Wu, Shawn Wu, Jimmy Xiang, Nan Xiao, Ruichao Xiao, Chao Xie, Yudi Xie, Fangzhou Xu, Nathan Yan, Tak Yan, Hang Yang, Song Yang, Yuhan Yang, Yavuz Yetim, Bowen Yu, Li Yu, Qifan Yuan, Xiaodong Yuan, Lin Zeng, Siqi (Cindy) Zeng, Caijie Zhang, Joanna Zhang, Min Zhang, Qing Zhang, Zhengkai Zhang, Fangyu Zou, and the entire v-team behind the success of Meta Andromeda.

The post Meta Andromeda: Powering the Next Generation of Ads Retrieval Through Model-System Co-Design appeared first on Engineering at Meta .
