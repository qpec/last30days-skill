# Agent-First Flow: How Teams Build When Everyone Has AI Agents

**A simple process for teams where every role — engineer, PM, designer, data — uses agentic AI to ship.**

---

## The Core Idea

Traditional Scrum assumes humans are the bottleneck. In an agent-first team, **the human's job shifts from implementing to specifying, reviewing, and deciding**. The bottleneck moves from "writing code" to "deciding what to build" and "verifying it's correct."

This process is **continuous flow (Kanban), not sprints**. Fixed two-week cycles make no sense when a single person ships 10-30 PRs per day. Work flows continuously from idea to production.

---

## The Process: Specify → Execute → Review → Ship

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌──────────┐
│   SPECIFY    │───>│   EXECUTE    │───>│   REVIEW     │───>│   SHIP   │
│              │    │              │    │              │    │          │
│ Human decides│    │ Agents work  │    │ AI + Human   │    │ Merge &  │
│ what to build│    │ in parallel  │    │ verify work  │    │ deploy   │
└─────────────┘    └─────────────┘    └─────────────┘    └──────────┘
     ▲                                                         │
     └─────────────── feedback loop (minutes, not weeks) ──────┘
```

### 1. SPECIFY (Human decides what)
- Write a clear intent: what should change, why, what "done" looks like
- Use **plan mode** — go back and forth with the agent until the plan is right
- Larger scope is fine: agents handle more work per story than humans did
- Pull from: user feedback, telemetry, bug reports, agent-suggested ideas

### 2. EXECUTE (Agents do the work)
- Switch to auto-accept once the plan looks good — agents one-shot it
- **Run multiple agents in parallel** (5-10+ at a time is normal)
- Each agent gets its own branch/worktree to avoid conflicts
- Agents handle: code, tests, docs, migrations, config — everything

### 3. REVIEW (AI first, then human)
- AI reviews 100% of PRs automatically (style, correctness, security)
- Human reviews the intent: "Does this solve the right problem?"
- Agents can self-verify by running tests, browser checks, build commands
- If it fails review → goes back to Execute with feedback, not back to Specify

### 4. SHIP (Merge and deploy)
- Trunk-based development — merge to main continuously
- Small, frequent merges (10-30 PRs/day per person is the norm at Anthropic)
- Monitor post-deploy; agents can watch telemetry and flag regressions

---

## Team Structure: Everyone Is a Builder

There are no pure "coders" and no pure "managers." Roles blur by design.

| Old Role | New Reality | What Changes |
|----------|------------|--------------|
| Engineer | Still architects systems, but agents write 100% of code | Focuses on system design, verification, hard judgment calls |
| Product Manager | Codes prototypes, runs agents, does stakeholder alignment | ~50% overlap with engineering; writes specs *and* ships them |
| Designer | Codes UI directly with agents, no more throwing designs over a wall | Unblocks themselves; implements their own vision |
| Data Scientist | Runs analysis agents, builds dashboards, writes SQL via agents | No longer waits for engineering support |
| Everyone | Shares a single **CLAUDE.md** in the repo with team conventions | Common knowledge base that agents and humans both reference |

**Key principle from Anthropic:** Under-fund teams slightly (1-2 people per project). This forces people to leverage agents fully instead of falling back to manual work.

---

## The Board: Kanban, Not Scrum

Use a simple Kanban board with WIP limits. No sprints. No sprint planning. No velocity tracking.

```
| Backlog    | Specifying (WIP: 3) | Agents Working | In Review (WIP: 5) | Shipped |
|------------|---------------------|----------------|---------------------|---------|
| Idea A     | Task D [Boris]      | Task F ▶▶▶     | Task H [AI ✓]       | Task K  |
| Idea B     | Task E [Kat]        | Task G ▶▶▶     | Task I [Human ◻]    | Task L  |
| Idea C     |                     | Task J ▶▶▶     |                     | Task M  |
```

**Why not Scrum?**
- Sprint planning becomes obsolete when agents execute in hours, not weeks
- Story points are meaningless when effort ≠ human hours
- Standups become "what did my agents ship overnight, what's blocked"
- Retros still useful — but for improving prompts, CLAUDE.md, and agent setups

**Why Kanban works:**
- Continuous flow matches the speed of agent execution
- WIP limits on "Specifying" prevent the real bottleneck: unclear intent
- WIP limits on "Review" prevent unreviewed code from piling up
- Visual board shows where work is stuck (usually: waiting for human decision)

---

## Rituals (Keep It Minimal)

| Ritual | Frequency | Purpose | Duration |
|--------|-----------|---------|----------|
| **Sync** | Daily, async | "What shipped, what's blocked, what's next" — via Slack/status sheet (agent-generated) | 5 min read |
| **Review queue** | Continuous | AI flags PRs for human review; humans process queue throughout day | Ongoing |
| **Feedback triage** | 2-3x/week | Scan user feedback channels; agents can suggest fixes and open PRs automatically | 30 min |
| **Retro** | Biweekly | What agent patterns worked, what CLAUDE.md rules to add/remove, what tooling to improve | 30 min |

No sprint planning. No estimation. No grooming. The agents don't need it.

---

## Seven Principles (Distilled from Anthropic + Industry)

1. **Speed over process.** If you can ship it today, ship it today. Don't wait for a ceremony.
2. **Under-fund, over-empower.** Small teams + unlimited tokens = forced innovation. 1-2 people per project.
3. **Plan first, then auto-accept.** 80% of tasks start in plan mode. Once the plan is solid, let the agent execute uninterrupted.
4. **Parallel by default.** Always have multiple agents running. Dead time = wasted capacity.
5. **Don't box the model.** Give it tools and a goal. Don't micromanage steps. The agent figures out the how.
6. **Shared knowledge in code.** CLAUDE.md in every repo: conventions, mistakes learned, style rules. Agents and humans both read it.
7. **Everyone builds.** PM codes. Designer codes. Data codes. The title "software engineer" is being replaced by "builder."

---

## How This Compares

| Aspect | Scrum | Kanban | **Agent-First Flow** |
|--------|-------|--------|----------------------|
| Cadence | Fixed sprints (2 weeks) | Continuous | **Continuous** |
| Planning | Sprint planning meeting | Just-in-time | **Plan mode per task** |
| Roles | PO, SM, Dev Team | Flexible | **Everyone is a builder** |
| Estimation | Story points | None | **None — agents execute in minutes** |
| Bottleneck | Development capacity | WIP limits | **Human decision-making & review** |
| Board | Sprint board | Kanban board | **Kanban board (4 columns)** |
| Feedback loop | End of sprint | Continuous | **Minutes (agent → PR → review → ship)** |
| Throughput | 5-15 stories/sprint/team | Varies | **10-30 PRs/day/person** |

---

## Getting Started: Three Steps

1. **Give everyone agents and tokens.** Don't gate access. PM, design, data — everyone gets Claude Code / Cowork. Optimize cost later.
2. **Create your CLAUDE.md.** Document your conventions, your mistakes, your style. This is your team's shared brain — agents read it on every task.
3. **Kill your sprint ceremonies.** Replace with: async daily sync, continuous review queue, biweekly retro. Let work flow.

---

---

## Validated by Community Research (Last 30 Days)

Deep research across 250+ posts on X/Twitter and Reddit (Feb-Mar 2026) confirms this process reflects a **real, converging trend** — not just one company's practice. Six core claims were validated, with important nuances.

### Claim 1: Continuous Flow Replaces Sprints (**STRONGLY VALIDATED**)

> *"We replaced user stories with structured specs for AI coding assistants... grooming became redundant, estimation stopped making sense, and sprint planning became just prioritization. We didn't decide to stop doing Scrum. The ceremonies just dissolved."*
> — r/agile (8 comments, active debate)

> *"My backlog is basically just a history book now. Does AI kill the 2-week sprint? My team is heavy on AI agents and the velocity is actually scary. I feel like a historian documenting what already happened rather than a PM planning what will happen."*
> — r/agile (40 upvotes, 59 comments)

**Industry signal:** Cox Automotive is transitioning 100 of 680 scrum teams to an agentic model, targeting 100% by end of 2026. Thoughtworks' AI/works platform frames this as "one continuous flow" that collapses multi-year modernization cycles into months.

**Nuance:** Multiple Redditors warned that dropping ceremonies entirely can cause drift — *"Customer feedback has always been the bottleneck and still is"* and *"One of the biggest killers of software companies is feature bloat."* The retro survives because it prevents unchecked acceleration.

### Claim 2: Everyone Becomes a Builder (**STRONGLY VALIDATED**)

Boris Cherny's quote — *"By end of year, everyone is a product manager, and everyone codes"* — went viral and was the single most-quoted statement across the dataset.

> *"On the Claude Code team, every position already codes. Designers. PMs. Managers. Finance. Data scientists."*
> — @MTanguma on X (summarizing Lenny's Podcast)

> *"'AI Product Engineer' is becoming a thing. PMs who can prompt their way to a prototype. Not no-code. Not vibe coding. Actually understanding what they're building."*
> — @madsviktor on X

> *"So PM's are required to AI develop now?"*
> — r/ProductManagement (63 upvotes, 155 comments — massive debate)

**Podcast signal:** The "Product Engineers: Create Fiercely" podcast is entirely dedicated to this convergence: *"Engineering, product, and design are collapsing."*

**Nuance:** Reddit PMs are split. Some embrace it (*"I built a full app solo"*), others resist (*"Hard to say if PMs will go deeper towards shipping, or if Engineering will go deeper towards steering"*). The convergence is real but uncomfortable.

### Claim 3: Parallel Agent Execution Is the Standard (**STRONGLY VALIDATED**)

> *"pi-side-agents: build in parallel with automated tmux + git worktree workflow. Completely changed my velocity and style of AI coding."*
> — @xpasky on X (156 likes)

> *"agent orchestrator lets one person manage 30+ parallel coding agents. 2,700+ GitHub stars and 1M+ impressions since we open sourced it 8 days ago."*
> — @agent_wrapper on X (148 likes)

> *"Kanban board for managing AI coding agents"*
> — @tom_doerr on X (382 likes, 42 RT — highest engagement in dataset)

**Tools emerging:** Vibe Kanban (2,700+ stars), ao-agents, Superset, Capy, Conductor, pi-side-agents — all solving the same problem: orchestrating parallel agents with isolated worktrees and visual tracking.

**Key insight from Chinese dev community:** *"The main problem with parallel coding agents isn't parallel and isn't coding agent, it's..."* (merge conflicts and context coordination — the unsolved hard problem).

### Claim 4: Review Is the New Bottleneck (**STRONGLY VALIDATED**)

> *"Why does code review take forever once teams hit 15-20 engineers?"*
> — r/ExperiencedDevs (170 upvotes, 119 comments)

> *"Writing code was never the bottleneck, and AI proved it."*
> — r/cursor (84 upvotes, 21 comments)

> *"AI-accelerated coding is creating massive downstream bottlenecks in code reviews, security..."*
> — Bill Staples, CEO of GitLab (CXOTalk podcast)

> *"Developers produce more code, but features don't ship any faster. The bottleneck just shifted."*
> — DevOps Paradox podcast

**Industry pattern:** The consistent finding is that AI shifted the bottleneck from "writing code" to "reviewing code" to "deciding what to build." Teams that solve review (via AI-first review + human intent check) unlock the full throughput.

### Claim 5: Plan-First Execution Works (**VALIDATED**)

> *"The biggest difference between AI coding assistants isn't the model — it's whether they force you to plan first."*
> — @santekotturi on X

> *"My Full Stack for AI-Assisted Shipping: ChatGPT → Planning and PRD, Cursor Plan Mode → Task breakdown, Cursor Agent → Execution, CodeRabbit → Review."*
> — @PrajwalTomar_ on X (5 likes)

> *"We Tested How Planning Impacts AI Coding. The Results Were Clear."*
> — r/cursor (comprehensive experiment comparing planned vs. unplanned agent work)

> *"Changed how I use Claude Code: Old way: Plan 50 features → ship 50 things → fix 200 bugs. New way: Plan 10 features → ship 3 of them, using 3 parallel agents → review → next batch."*
> — @Brandonius_813 on X

**Convergence:** Whether using Claude Code's plan mode, Cursor's composer mode, or structured specs, the pattern is identical: **plan → approve plan → auto-execute → review output.** The planning step is "non-negotiable" per multiple practitioners.

### Claim 6: Shared Knowledge Files (CLAUDE.md) (**VALIDATED**)

> *"Having a shared CLAUDE.md with team conventions saves so much time vs everyone configuring their own thing."*
> — @rv_RAJvishnu on X

> *"Skills are the most underrated Claude Code feature. We have 14 repos with custom CLAUDE.md files that encode team conventions — formatting, testing, deployment."*
> — @GGMTars on X

> *"The most effective rules in a CLAUDE.md aren't code problems to fix, they're workflow decisions, team conventions, communication patterns."*
> — @ejae_dev on X

> *"TIL Claude, Cursor, VS Code Copilot, and Codex all share the same 'Skills' format now."*
> — r/ClaudeAI

**Cross-tool convergence:** The CLAUDE.md pattern has become a de facto standard across Claude Code, Cursor, Copilot, and Codex. It functions as the team's institutional memory that both humans and agents reference.

### Key Risk: Comprehension Debt (**IMPORTANT CAVEAT**)

> *"AI wrote half my code and now I regret everything. Absolute mess. Huge files, unused functions everywhere, duplicate logic, random helpers, zero structure."*
> — r/vibecoding (427 upvotes, 254 comments — highest-engagement cautionary post)

> *"Teams adopt AI coding tools, velocity looks great for a few months, and then on-call engineers can't debug code they've never seen."*
> — r/artificial (21 comments)

> *"The comprehension debt is real and it sneaks up on you."*
> — r/artificial comment

**Mitigation:** This risk is why the Review step and CLAUDE.md conventions are non-negotiable. Teams that skip review or don't maintain shared conventions accumulate "comprehension debt" that eventually crashes their velocity.

---

### Source Success Rate

| Source   | Succeeded | Failed | Total Items | Notes                              |
|----------|-----------|--------|-------------|------------------------------------|
| X        | 9/9       | 0      | 198 posts   | Strong signal on all claims        |
| Reddit   | 5/5       | 0      | 102 threads | Deeper discussion, more nuance     |
| Podcast  | 14/14     | 0      | 142 episodes| Industry leaders confirming trends  |
| Web      | 8/8       | 0      | N/A         | CIO, Forrester, McKinsey coverage  |

---

*Synthesized from: Boris Cherny (Head of Claude Code, Anthropic) on Lenny's Podcast (2026), deep research across 250+ community posts on X/Twitter and Reddit (Feb-Mar 2026), industry analysis from CIO, Forrester, GitLab, McKinsey/QuantumBlack, and practitioner podcasts.*

**Primary Sources:**
- [Boris Cherny on Lenny's Podcast](https://www.lennysnewsletter.com/) — Anthropic's internal workflow
- [Inside the Development Workflow of Claude Code's Creator — InfoQ](https://www.infoq.com/news/2026/01/claude-code-creator-workflow/)
- [How Boris Cherny Uses Claude Code — Substack](https://karozieminski.substack.com/p/boris-cherny-claude-code-workflow)

**Industry Research:**
- [5 Ways Agentic Engineering Transforms Agile Practices — CIO](https://www.cio.com/article/4086747/5-ways-agentic-engineering-transforms-agile-practices.html)
- [How Agentic AI Will Reshape Engineering Workflows in 2026 — CIO](https://www.cio.com/article/4134741/how-agentic-ai-will-reshape-engineering-workflows-in-2026.html)
- [Anthropic 2026 Agentic Coding Trends Report](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf)
- [Agentic Workflows for Software Development — McKinsey/QuantumBlack](https://medium.com/quantumblack/agentic-workflows-for-software-development-dc8e64f4a79d)

**Community Voices (Highest Engagement):**
- [r/agile — "Does AI kill the 2-week sprint?"](https://www.reddit.com/r/agile/comments/1r4jemj/) (40pts, 59cmt)
- [r/vibecoding — "AI wrote half my code and now I regret everything"](https://www.reddit.com/r/vibecoding/comments/1r6zm8x/) (427pts, 254cmt)
- [r/ExperiencedDevs — "Why does code review take forever"](https://www.reddit.com/r/ExperiencedDevs/comments/1rjfo06/) (170pts, 119cmt)
- [r/ProductManagement — "So PM's are required to AI develop now?"](https://www.reddit.com/r/ProductManagement/comments/1rgpxql/) (63pts, 155cmt)
- [r/singularity — "Programming Changed More in 2 Months Than in Years" (Karpathy)](https://www.reddit.com/r/singularity/comments/1remuz1/) (1,214pts, 286cmt)

**Tools & Platforms:**
- [Vibe Kanban — Orchestrate AI Coding Agents](https://www.vibekanban.com/) (2,700+ GitHub stars)
- [ao-agents — Agent Orchestrator](https://github.com/aoagents) (2,700+ stars, 1M+ impressions)
- [Claude Code for Product Managers](https://ccforpms.com/fundamentals/agents)

**Podcasts:**
- [The New Bottleneck: AI That Codes Faster Than Humans Can Review — New Stack](https://podcasts.apple.com/md/podcast/the-new-bottleneck-ai-that-codes-faster-than-humans/id915443155?i=1000710091433)
- [Is Scrum Fast Enough? — Dave West, CEO of Scrum.org](https://open.spotify.com/episode/5b4qay5O5hFzBJlCZN4i1x)
- [Product Engineers: Create Fiercely — Role Convergence](https://podcasts.apple.com/no/podcast/product-engineers-create-fiercely/id1836853484)
