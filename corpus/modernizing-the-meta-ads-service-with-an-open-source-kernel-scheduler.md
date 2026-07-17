---
title: Modernizing the Meta Ads Service With an Open-Source Kernel Scheduler
source_url: https://engineering.fb.com/2026/07/13/ml-applications/modernizing-the-meta-ads-service-with-an-open-source-kernel-scheduler
company: meta
date: '2026-07-13'
evidence_tier: 2
language: en
track: infra
full_text: complete
---

# TL; DR

- At Meta’s scale, a few milliseconds of latency degradation can have a significant negative impact on ads performance.

- When a Linux kernel upgrade risked regressing latency across Meta’s ad serving fleet, we turned to sched_ext — the upstream, BPF-based extensible scheduling framework — to build a scheduling policy customized to the Ads delivery workload.

- The result: a 28% reduction in ads retrieval stage tail(99th percentile) latency, 3.28 megawatts(MW) power saving, and a 1.1% increase in the number of ads ranked, proving that workload-specific scheduling optimization can directly drive business value.

# Why Ads Latency Matters

Meta’s ads serving fleet handles more than 5 million requests per second on average at the serving platform entry point, which is over 400 billion per day across all monetized surfaces 1 . Every millisecond shaved off the p99 latency makes the ads more relevant for people on our platforms, and better matches mean stronger ROI for advertisers.

This provides a real opportunity to reduce latency through workload-specific scheduling. That is why our Ads and Linux Kernel teams have been working together to build a scheduling policy customized to the ads delivery workload using sched_ext, the upstream, BPF-based extensible scheduling framework. Until now, we have been using the general-purpose schedulers typically integrated in the Linux kernel (CFS and EEVDF) that balance threads across CPUs with no understanding of the workload. However, here we know the purpose and importance of each thread. With sched_ext, we can encode this knowledge directly into the scheduler. Work that improves the p99 request latency is scheduled first, and everything else takes a back seat.

## sched_ext at Meta

s ched_ext is an open-source, BPF-based scheduler framework that officially entered kernel v6.12. We developed it by partnering with the authors of Google’s ghOS t to design a scheduler suitable for upstream Linux integration. It has already been deployed in several services at Meta, delivering meaningful reductions in scheduling latency.

While upgrading our fleet to the latest stable version of Linux ( kernel v6.9 ) we observed that the new Earliest Eligible Virtual Deadline First (EEVDF) scheduler introduced in Linux kernel v6.6 was causing a latency regression which reduced the number of ads ranked in response. As a result, a subset of ads hosts were forced to remain on the older v6.4 kernel, creating technical debt and operational fragmentation.

Given its already strong performance, sched_ext was a great candidate to address these scheduling regressions.

## Custom Scheduling with sched_ext

Sched_ext lets scheduler developers implement their preferred scheduling policy as a BPF program. When a host starts running the ads workload, an ads-optimized policy is applied. From that point on, the kernel calls into the BPF scheduler through a set of event-driven callbacks to handle common scheduling events, such as:

- Thread wake-up : choose a CPU when a thread becomes runnable.

- Enqueue : place a thread in a run queue.

- Dispatch : select the next thread when a CPU becomes idle.

- Idle transitions : respond to CPUs entering/leaving idle states.

At a high level, the policy soft-partitions CPUs into two pools , one for threads on the latency-critical request path and one for less latency-sensitive work. Which thread goes into which pool is part of the domain-specific knowledge encoded inside the policy. The size of each pool is adjusted dynamically using load-based heuristics. This approach tends to keep related work on the same CPUs over time, improving last-level cache (L3) locality and reducing costly DRAM access.

The policy is packaged as a user-space binary that loads the BPF program. That design makes experimentation and performance optimization much faster. To roll out a change, we can simply restart the scheduler process to unload the old policy and load the new one, without rebuilding or reinstalling the kernel.

# Results and Impact

The initial launch took place to switch from kernel 6.4 with the CFS scheduler to kernel 6.9 with sched_ext on the largest ads serving server type. Based on the backtest experiment, the launch delivered:

- +1.1% on weighted-ads-ranked (metric for number of ads retrieved and ranked).

- 3.28 megawatts of power savings across the fleet.

- 28% reduction in service p99 latency on the ads retrieval path 2 .

Compounding improvements. Two follow-on scheduler-policy updates, delivered as purely user-space changes, extended the win:

- Additional 60% reduction in service p99 latency.

- 18% reduction in timeout errors on the critical path.

This is a non-trivial win delivered with no dependency on kernel releases. Each follow-on iteration above shipped in days rather than months because the scheduler policy lives in user space as a BPF program. That cadence is what turned sched_ext from a “kernel upgrade unblocker” to a continuous-optimization platform for ads serving.

# From Short-Term Fix to Strategic Asset

What started out as a targeted response to a very specific operational issue has turned out to be much more strategic, and widely applicable, than we originally anticipated. sched_ext delivers some key benefits to Meta:

A parallel and decoupled scheduler optimization path. Upstream Linux scheduling naturally evolves over time, sometimes in larger steps (such as the CFS-to-EEVDF transition), which can be disruptive to downstream consumers. sched_ext gives Meta the flexibility to continuously improve these custom schedulers alongside that evolution. We run and refine our own BPF-based scheduling logic, tailored to the unique demands of our production workloads, so our critical services stay optimized regardless of what happens upstream.

Independent deployment and reduced overheads. Scheduler improvements ship as BPF program updates, shipped in days rather than months. The resulting reduction in the cost of experimentation is transformative. Ideas that previously required a kernel patch and months of validation — local-cache-aware placement, ROI-based executor routing, NUMA-aware steering — become tractable iterations rather than major projects.

A shared industry asset. sched_ext was upstreamed into Linux v6.12, so the same mechanism Meta used here is now available to the entire Linux ecosystem. Any operator with a workload that doesn’t fit the general-purpose model — hyperscaler, cloud provider, embedded systems team — can ship workload-specific scheduling policies without forking the kernel.

# Future Plans

sched_ext is already allowing us to see opportunities for further improvements in ads performance, by giving the application more fine-grained control over the behavior of the scheduler. For example, the ads services have important context about the relative importance of service requests, and are potentially able to signal to the scheduler when a thread starts working on an important request. When the scheduler receives this hint, it can take appropriate steps like increasing this thread’s scheduling slice or ensuring it’s always at the top of the queue.

# Acknowledgments

Special thanks to Samuel Nair , Usama Arif , GP Musumeci , Praveen Alevoor , Ye Wang , and the broader Ads capacity efficiency and kernel team for their contributions and collaboration.

Ads Infra Leadership Team: Uladzimir Pashkevich, Varna Puvvada, Prabhakar Goyal, Neeraj Agrawal, Tak Yan , Liz Shepherd , Drew Lackman

The post Modernizing the Meta Ads Service With an Open-Source Kernel Scheduler appeared first on Engineering at Meta .
