---
title: 'Intelligent Delivery: Making Every Unit of Compute Serve Better Ads'
source_url: https://engineering.fb.com/2026/11/11/ml-applications/intelligent-delivery-serve-better-ads
company: meta
date: '2026-11-11'
evidence_tier: 2
language: en
track: modeling
full_text: complete
---

- Ads ranking models are growing toward LLM scale faster than the hardware to run them can keep up. An extra unit of compute has more impact on some ad requests, models, and chips than on others. The challenge is deciding where to allocate it to get the best outcome for the entire system.

- We built Intelligent Delivery, an ML-driven system that allocates resources across the serving stack toward the system-wide optimum. It has delivered ~10% incremental ranking performance on top of model and system advancements since 2017.

- We’re sharing a few of Intelligent Delivery’s capabilities: how we build ML models to predict the marginal utility of compute, multi-layered mechanisms to move resources across the system, and how we increasingly leverage agentic AI to continuously detect and respond to system shifts.

As frontier ads ranking systems advance toward larger models, broader candidate sets, and richer delivery architectures, they also place greater demands on serving efficiency. Compute resources do not scale at the rate that models and system complexity do. The challenge is not just how to build more powerful models, but how to operate them efficiently across a heterogeneous system, with finite serving capacity, and under a tight latency budget. We recently shared how we put idle inference capacity to work . This post covers how we decide where each unit of compute goes to achieve globally optimal system efficiency.

Intelligent Delivery is our approach to the problem, and it has contributed an additional ~10% improvement in ads ranking performance on top of model and system advancements across major surfaces, from 2017 through the first half of 2026. It introduces an ML-driven, increasingly AI-operated adaptive optimization layer that continuously directs resources toward the requests, models, hardware fleets, and ranking stages with the highest marginal utility. This helps us run advanced ads ranking models efficiently in production, getting more out of every unit of compute to serve better ads for people who use our apps and services.

## The Goal and What Makes It Difficult

One of our goals is to create a delivery system that continuously converges on its global optimum, regardless of how user behavior changes, models evolve, and the serving stack grows more complex.

Three fundamental properties of ads delivery systems make this challenging:

The marginal impact of compute is highly heterogeneous and context-dependent: The same additional unit of compute can generate very different returns depending on the product surface, user intent, candidate quality, and system state. Request-aware signals alone are not sufficient; allocating well means estimating, for every request, the return on every available tunable system parameter, where each knob behaves differently at each stage of the funnel. We need to produce a per-request result calculation across a vast decision space within milliseconds.

Local optimality does not translate to global optimality: Result estimation is just the start; the serving stack must also be dynamically controllable. Ads delivery spans multi-stage ranking , hundreds of models, generations of hardware, and many data centers. Resources cannot be shifted freely and reliably across these boundaries without adaptive controls that account for complex dependencies throughout the stack.

The global optimum is a moving target: The optimization landscape is continuously shifting. Every new model, hardware generation, or new architecture changes the landscape and can invalidate previously optimal allocation decisions. The system needs to adapt quickly enough to retain its optimality.

Intelligent Delivery includes three capabilities, each designed to address one of these fundamental system challenges.

## Capabilities of Intelligent Delivery

### 1. Request Understanding: A Shared ML Intelligence Layer for Compute

Some ad requests benefit more from additional computation than others. Initially, we captured these differences through coarse segments: Requests were grouped by attributes such as surface, context, and ad creative representation, with engineers creating policies to allocate resources for each group. This approach delivered improvements but did not scale. Every new signal multiplied the rules, making the effort unsustainable, and independent segments could not capture the nonlinear interactions among thousands of signals, which limited accuracy.

We achieved about a 20% improvement in identifying the highest-impact ad requests in offline benchmarks on major surfaces, relative to our previous production model, after reframing this into two ML problems: Which ad requests are most likely to benefit from additional compute? And how will different resource settings affect their outcomes and serving performance?

To answer the first question, we built the Resource Core Model , deep learning models with 6B sparse parameters and 20M dense parameters that run once before candidate retrieval and are shared across the delivery funnel. Learned embeddings and deep feature interactions capture nuanced request patterns that manually defined segments cannot.

We then fine-tune the Resource Core Model into a set of specialized models, each generating incremental signals about outcome, compute consumption, and latency impact. Together this forms a shared ML intelligence layer for resource allocation: The Resource Core Model understands each request and its serving behavior, while individual mechanisms determine how to translate those predictions into actions.

### 2. Allocation Mechanisms: A Hierarchy of Decision Engines

Ads serving runs on a globally distributed, heterogeneous fleet with many data center regions, several hardware generations, and millions of hosts, all shared by a multi-tier serving stack. A single allocation mechanism cannot control the complex resource distribution end to end. So we decomposed the problem into a hierarchy of layers and built a dedicated decision engine for each. The easiest way to see the hierarchy is to follow a single request through it.

Someone opens their feed. An ad request is created, and over the next few hundred milliseconds it passes through a chain of resource allocation decisions. This leads us to three important questions and answers.

Which region serves it? Traffic and capacity are not colocated, and each region carries a different hardware mix and a different amount of headroom — so the same unit of compute is more efficient in some places than in others. We built real-time infrastructure to dynamically shift traffic between regions in a cycle of minutes, driving toward the point where every region achieves the same level of efficiency on its marginal unit of capacity.

What hardware does it land on? Our fleet spans CPUs from Intel, AMD, and Arm and accelerators from NVIDIA, AMD, and our own Meta Training and Inference Accelerator (MTIA) , across several generations of each. The hard part isn’t the variety; it’s that capacity isn’t interchangeable. Our stages are bound by different resources — retrieval by memory capacity, ranking by compute, and model inference by accelerator throughput — so there is no single fastest SKU, only a best match per workload. We benchmark measured efficiency for every workload-SKU pair, then solve the assignment so that scarce hardware goes to the workloads that convert it into the most useful work.

Inside the host, how much of this machine does the request get? Concurrent requests differ in latency budget and impact, under a hard tail-latency SLO. We predict each request’s expected outcome and its compute and latency cost in real time using our advanced deep learning models, and solve a constrained optimization that maximizes impact delivered within the host’s latency budget — as the host load increases, the performance trade-off rises and resource-intensive low-impact work is trimmed first. Enforcing those decisions takes control across the whole stack, so the framework spans from kernel-level scheduler up to application-level thread pools.

These three steps are just a subset of the allocation decisions we make during a request’s lifecycle. Following this, we optimize the number of ads to rank for each request in each ranking stage, what ad candidates enter the pool, and much more.

These allocation decisions are tightly coupled, so a resource change in any one of them ripples across the whole system. Shifting traffic between regions changes per-host load, which drives the feedback controller that sets how much work each request gets. We validate these changes in an end-to-end, closed-loop hardware testing environment to make sure we are optimizing for the global optimum instead of a local optimum.

### 3. Optimization Loop: Self-Optimizing Serving with Agentic AI

As our ad system advances, productionizing a new model, a new mechanism, or new hardware into the system requires a lot of effort to achieve seamless integration. We can’t brute-force every single configuration across millions of tunable dimensions built in our system for a new change. That would require too much time and far more hardware resources than we have.

We relied heavily on human expertise and engineers’ prior knowledge to identify promising configurations. But this approach didn’t scale, because every new model, mechanism, and hardware generation expanded the search space faster than engineers could explore it. We tried automating this with a constrained optimization approach, which delivered improvements but remained inflexible and slow. We found that it lacked the ability to generalize (it could only cover a few key knobs) and couldn’t effectively incorporate human intuition from prior experience.

Instead of doing a blind search, AI agents continuously monitor the entire system landscape, identifying changes and inefficiencies to address. In a long context window, an agent reads mechanism source code, design documents, and a decade of experiment logs and narrows that to a handful of changes worth testing. Engineers review and approve the final change before it ships.

Today, agents can already propose well-reasoned changes and design and run rigorous experiments. In the first half of 2026, agents contributed to about 20% of Intelligent Delivery optimizations. On our most automated mechanism, they now contribute to about 80% of the engineering effort, from understanding the system landscape and forming hypotheses to running experiments and converging on the final change. This shortens the optimization loop from months to weeks while keeping people firmly in control. And it steadily captures the expertise engineers have built over the years.

## The Next Frontiers for Intelligent Delivery

End-to-end real-time optimization: Today, understanding a request and deciding how to serve it are still two separate steps. We’re building toward fusing them into a single model that reads a request and serves it in real time, without months of experiments. There’s established work in varying compute per request with learning-based methods. However, doing it jointly across every serving stage at once — under shifting traffic, hard capacity limits, and tight inter-stage dependencies — is the part that’s still open, and it’s what we’re pushing on.

Serving state-of-the-art models on GPUs: Large ranking models, like Meta’s Generative Ads Model (GEM) , are growing toward LLM scale and increasingly run on GPUs, which opens a different optimization space. GPU capacity doesn’t divide the way CPU time does — it comes in whole, fixed blocks, and throughput, batching, and memory all behave differently. The levers we built for a CPU world have to be reimagined, and much of our work now goes into understanding those mechanisms and turning them into new levers. The more useful work we get out of each accelerator, the more people we can serve with strong models under the same capacity.

## Acknowledgements

Sowji Adavi, Karthik Alle, Tao Cai, Olivier Chaine, Jianhao Du, Antonio Frigo, Gayatree Ganu, Chao Li, Chao Ma, Bennet Matazzoni, Riddhi Mehta, Saurabh Pohnerkar, Sudhir Pokhrel, Yuehui Qian, Liang Qiao, Yitao Qiu, Rob Schwartzberg, Sanketh Shetty, Ganlin Song, Samuel Tatipamula, Xueqi Wang, Ye Wang, Wei Wei, Jing Xu, Haomin Yu, Jiayi Yu, Jay Zang, Caijie Zhang, Shengjie Zhang, Tong Zhang, and Wei Zheng.

The post Intelligent Delivery: Making Every Unit of Compute Serve Better Ads appeared first on Engineering at Meta .
