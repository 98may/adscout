---
title: Becoming an AI Team
source_url: https://medium.com/pinterest-engineering/becoming-an-ai-team-866d6b567803
company: pinterest
date: '2026-09-01'
evidence_tier: 2
language: en
track: modeling
full_text: complete
---

# Becoming an AI Team

Listen

Share

John Grass | Sr. Manager, Engineering

## A Fundamental Transformation

An AI team is fundamentally more than just a group whose members incorporate AI tools into their existing workflows. The journey to becoming an AI team necessitates a fundamental and comprehensive paradigm shift in how the team defines ownership, engages in strategic planning, and, most critically, executes on its core goals and objectives. This transformation is not merely an addition of new technology; it is a restructuring of the team’s operating model, philosophy, and individual roles.

In an AI-centric environment, every single member is significantly empowered, not only through access to cutting-edge AI tools and sophisticated models but through an expanded scope of responsibility and influence . These new capabilities allow individuals to automate routine tasks, accelerate data analysis, and rapidly prototype solutions, freeing up cognitive resources for higher-level, more strategic thinking. The expectation shifts from simply completing tasks to orchestrating intelligent systems and focusing on solving problems that were previously intractable.

Consequently, the very nature of the work for both individual contributors and managers will be fundamentally different from anything that has come before.

At Pinterest, this isn’t theoretical. Our infrastructure teams sit at the core of a product that serves billions of Pins, boards, ads, and real-time signals. That reality has forced us to treat “becoming an AI team” as an operational necessity, not a side project as we cannot keep scaling reliability, cost efficiency, and developer productivity using only traditional playbooks.

## AI Team Capabilities

The advent of accessible Artificial Intelligence (AI) tools has fundamentally raised the performance ceiling for what development teams can accomplish. To illustrate this profound shift, consider a normally challenging project — for example, refactoring an entire legacy codebase to replace a widespread used process named “foo” with a more modern one named “bar.” This type of undertaking, which can be critical for long-term maintainability but often low on the priority list due to its sheer scale, would have previously required a dedicated team of several engineers and a timeline spanning many months, potentially a year or more.

With the seamless integration of modern AI tools, projects once considered infeasible or prohibitively expensive in terms of human capital and time can now be completed with incredible speed and accuracy. The very refactoring example mentioned above, utilizing sophisticated code-generation and transformation models, can now be executed and verified in a matter of a week or less.

This new capability changes far more than just project timelines; it fundamentally reshapes how organizations and teams must approach prioritization. The set of “possible projects” that are technically within reach has grown dramatically, multiplying the complexity of deciding where to focus energy. Consequently, the act of prioritization has become even more critical. Teams must internalize a new maxim: Just because something is feasible does not mean it is strategic. The ability to accomplish a task quickly with AI does not inherently align it with the core goals of the business or product.

By offloading repetitive, high-effort engineering tasks to AI, teams will fundamentally shift their focus. Engineers, product managers, and designers must dedicate more time and energy to high-level strategic thinking, in-depth problem definition, and validating genuine user needs, rather than getting caught up in execution details. Consequently, the core value of an engineering team moves from being expert coders to becoming expert strategists and problem-solvers, using AI as a powerful force multiplier for execution.

## The Manager’s Evolving Role

As the daily work of individual contributors, particularly engineers, becomes increasingly elevated and augmented by AI, the role of the manager undergoes a profound transformation. Managers are systematically freed from the time-consuming, routine tasks traditionally associated with project management and oversight such as the meticulous tracking, status updates, resource allocation for predictable tasks, and micro-managing process adherence.

This liberation allows managers to pivot from being primarily process enforcers and administrative overseers to becoming true strategic guides and visionary leaders. Their focus shifts dramatically toward:

- Strategic Direction and Vision Setting: The primary responsibility evolves to identifying which ambitious challenges and emerging technologies merit the team’s concentrated pursuit. This involves a higher-level view of the product roadmap, understanding market shifts, and translating the organization’s overarching goals into clear, actionable, and inspiring technical objectives for the team.

- Maximizing Collective Impact: Instead of simply ensuring projects are completed on time, the manager’s role is to steer collective efforts toward the points of maximum strategic impact . This requires deep critical thinking, understanding the leverage points within the architecture or product, and making difficult trade-off decisions that align the team’s output directly with the most significant business outcomes.

- Talent Development and Mentorship: With AI handling much of the repetitive code generation and debugging, the value of the human engineer shifts to creativity, complex problem-solving, and system-level architecture. Managers must therefore focus intensely on coaching and mentoring team members, helping them develop higher-order skills, navigate ambiguity, and define career paths that capitalize on advanced technical and strategic competencies.

## AI work at Pinterest

Across Pinterest, we’re seeing similar patterns. Data and platform teams are building agents that write and validate Spark jobs, triage alerts, and help product teams explore data without deep query expertise. Our design, PM, and support functions are using AI for brainstorming, content drafting, and faster decision-making. Initiatives like our AI Acceleration Learning Sessions and GenAI productivity working groups are making these wins visible and repeatable, so teams don’t have to rediscover the same patterns in isolation.

For infrastructure teams, this has a very concrete flavor: agents that surface distressed databases before they page an engineer, tools that propose safer rollout plans, and coding assistants that make large-scale refactors on our storage platforms possible in days instead of quarters. Those are the kinds of capabilities that make an “AI team” feel less like a slogan and more like an everyday operating model.

## Future Teams Are AI Teams

The integration of Artificial Intelligence into the modern workplace is not merely an incremental technological upgrade; it represents a fundamental shift in how work is conceived, executed, and managed. For every professional, from the newest individual contributor to the most seasoned manager, adapting to this new paradigm isn’t optional, it’s imperative for survival and success. The era of the “traditional” high-performing team is rapidly giving way to the AI-enabled team , and the difference in capability is staggering.

The core reality is that the capacity, efficiency, and innovative potential of AI-enabled teams will be an order of magnitude greater than their predecessors. AI tools will automate routine, repetitive tasks, freeing up human talent to focus on complex problem-solving, strategic thinking, and creative endeavors that require uniquely human judgment and emotional intelligence. This shift doesn’t eliminate roles; it elevates them, demanding a new set of skills centered around prompt engineering, data interpretation, critical thinking, and collaborative interaction with intelligent systems.

To remain effective, competitive, and truly innovative, teams and organizations must fully embrace this transformation. This involves more than just adopting new AI tools; it requires a deep cultural change.

The future of high-performance is intrinsically linked to this symbiotic relationship between human expertise and machine intelligence. Teams that hesitate will quickly find themselves outpaced by competitors who have successfully made the leap, highlighting that embracing this AI-driven evolution is not just a strategic advantage but is rapidly becoming the foundational requirement for sustainable innovation and effectiveness.

## Previous Capacity & Commitments Model

Teams would assess available capacity for a work cycle and commit to specific deliverables. The expectation was to meet all commitments. In reality, factors like underestimated effort or reduced resource availability typically led to falling short (e.g., achieving 70% of commitments).

## Initial Impact of AI Tools

AI tools (for documentation, coding, etc.) have been available and used by some individuals, leading to a modest increase in overall team efficiency. This early, non-uniform adoption has yielded minor capacity gains (e.g., an estimated 20% increase). Consequently, teams are performing better against commitments, but still slightly missing the mark (e.g., hitting 90% ), meaning the team is still operating at 100% capacity (fully busy).

On our Storage Foundations team at Pinterest, we’ve already started to see this shift in very real terms. For example, work such as investigating distressed database clusters could previously require several days of effort is increasingly being front-loaded by AI agents that sift through logs, generate candidate hypotheses, and even draft remediation commands

We’re also starting to see this show up at the portfolio level. AI-assisted tooling around MySQL, TiDB and Cache Infrastructure has let us move from “only what’s absolutely urgent” to clearing whole classes of maintenance work that used to sit in the backlog indefinitely. That doesn’t mean we’ve “saved X engineers”; it means the same engineers are now spending much more of their time on roadmap-level questions instead of chronic firefighting and manual KTLO.

## The Need to Pass the Tipping Point

To fully realize the benefits of AI, the team needs dedicated time for skill development and deeper integration of the technology. AI adoption increases team capacity. The crucial hurdle is reaching a point where the team’s increased capacity exceeds its commitments . This surplus time is essential for developing AI proficiency. The current challenge for most teams is this transitional phase: simultaneously learning and using new tools while struggling to meet existing deliverable expectations.

## Navigating the Chaos: The Role of Leadership in the AI Transition

The transition to an AI-powered work environment is inherently complex and often turbulent. Teams are confronted with an overwhelming deluge of information, including a proliferation of AI tools, new academic research, industry blogs, online courses, and detailed demos. This sheer volume can quickly lead to paralysis and confusion: Which specific tools offer the best return on investment? What are the foundational concepts or practical skills I absolutely need to acquire? How do I strike a sustainable and productive balance between the necessary phase of exploration and real-world execution and delivery? The difficult truth is that no universal, one-size-fits-all answer exists to these critical questions.

In this phase of uncertainty, managers assume a role that is not merely supervisory, but truly critical. They must become the primary navigators, charting a course through the technological uncertainty. This guidance involves several key responsibilities:

- Guiding Through Uncertainty: Leaders must acknowledge and validate the team’s confusion and anxiety, providing a clear vision of the destination even when the immediate path is obscured. They filter the noise, helping the team prioritize a manageable set of tools or learning tracks that align directly with organizational goals.

- Encouraging Information Sharing and Experimentation: Managers should actively dismantle silos, creating structured and informal forums such as brown bag sessions, dedicated Slack channels, or internal demo days where team members can share their discoveries, successes, and, crucially, their failures. Furthermore, they must allocate dedicated time and resources for experimentation, framing it not as a diversion from work, but as an essential part of the new workflow.

- Creating a Culture of Psychological Safety: Perhaps the most important leadership function is establishing an environment where it is genuinely “okay to learn and adapt.” This means normalizing the fact that competence in AI will be a journey, not an instant state. Leaders must replace the fear of failure with an appetite for fast, informed learning , celebrating the insights gained from an unsuccessful experiment as much as a successful deployment. This psychological safety accelerates the learning curve and transforms fear into proactive engagement with the new technology.

## Guiding Your Team Through the AI Transition

The integration of Artificial Intelligence represents not just an incremental technological update, but a fundamental shift in the landscape of daily work. While it may unfold more gradually than a traditional corporate reorganization, the transition to an AI-augmented environment will prove to be an even more profound, systemic transformation, altering core processes, roles, and skill requirements. It is crucial for leadership to acknowledge that change, even when promising vast positive outcomes, is an inherently stressful process for employees. Proactive and empathetic guidance is essential to navigate this period successfully.

For individual contributors, the core of their professional identity and daily tasks will evolve significantly, shifting the focus from execution to strategy, guidance, and unique human insights.

Prior professional experience remains absolutely essential. However, the application of that experience will fundamentally change. Instead of primarily using experience to execute tasks manually, team members will leverage it for guiding, critiquing, and collaborating with advanced AI agents and tools. Their role shifts to one of a skilled orchestrator, using their deep understanding of the problem space, customer needs, and business context to ensure the AI’s output is accurate, relevant, and fully aligned with strategic goals.

As AI takes on an increasing share of repetitive, data-intensive, and complex implementation work (“the how”), the demand for a strategic mindset within individual roles will escalate. Team members must become much more strategic partners, actively participating in and driving decisions about what work is most valuable to pursue, why it matters, and how to define success. This requires moving beyond merely fulfilling assigned tasks to critically analyzing the business problem, prioritizing initiatives, and defining clear, high-leverage prompts and guardrails for the AI to follow. This strategic contribution elevates the value and scope of every role.

## Conclusion

Embracing this holistic shift thoughtfully, strategically, and together is not optional. It is essential for engineering teams aiming to thrive, innovate, and lead in this new era where intelligence is the core layer of the product. The successful team will be one that is centered around the continuous optimization of the AI-driven system.
