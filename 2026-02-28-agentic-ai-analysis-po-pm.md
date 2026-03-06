# Agentic AI for Analysis: Product Owners & Managers

**Date:** 2026-02-28
**Period:** January 29 – February 28, 2026
**Method:** 23 parallel research agents across 3 runs (X, Reddit, YouTube, Web)
**Sources:** X/Twitter (Bird GraphQL), Reddit (Brave Search + OpenAI), YouTube (yt-dlp + transcripts), Web (Brave Search)

---

## Executive Summary

The product management profession is undergoing its most significant transformation since Agile. Agentic AI is not replacing POs/PMs — it is **redefining what the role produces**. The PM of 2026 no longer writes tickets; they design the system where AI produces product. The community consensus across X, Reddit, and YouTube is clear: PMs who can define agent constraints, metrics, and guardrails will thrive. Those who can't will be replaced — not by AI, but by PMs who can.

---

## 1. The PM Role Is Being Redefined

The strongest signal across all sources: the PM role is shifting from **backlog administrator to AI system designer**.

> "El Product Manager ha muerto. El nuevo PM no gestiona backlog. Diseña el sistema donde la IA produce producto. Tokens = presupuesto. Git no es opcional. agents.md = constitución"
> — @CarlosBeneyto (21 likes, 2 RT)

> "AI in product management is not about replacing the human touch. It's about scaling it. How many user interviews can you personally conduct in a week? Maybe 10-15 if you're really pushing it."
> — @rangelovbor

> "Higher probability that it's role shift than AI replacing jobs. Layoff old product staff, hire new product staff. Same story, as old as time."
> — @TraderSmith09, replying to @aakashgupta

> "I think AI will replace essentially everything that software engineers do today, and it already has for the things they did 3 yrs ago =/= replacing the people. I think software engineers will continue to exist, doing new things."
> — @ArthurMacwaters (10 likes)

> "There is so much of what Gokul says about product management that can be applied at a totally different level with agentic engineering and AI. I am writing about it."
> — @aprateem

**Reddit confirms the shift is real and happening now:**

> **"How did AI change the Product Manager role in your company?"** — r/prodmgmt (Feb 21)
> Direct discussion from working PMs describing changes already in effect.

> **"Keeping up with the new skills required in the PM role"** — r/ProductManagement (Feb 21)
> PMs discussing the scramble to learn AI-native skills.

> **"My devs are on AI steroids and Scrum is officially too slow. Now what?"** — r/scrum (Feb 14)
> Developers shipping so fast with AI agents that traditional sprint cadences become the bottleneck. POs must adapt.

---

## 2. Where Agents Are Actually Being Used for PM/PO Analysis

Concrete use cases emerging from the research, ranked by maturity:

### Production-Ready

| Use Case | Evidence | Source |
|----------|----------|--------|
| **PRD generation** | @grok: "Here's PRD for agentic AI load board disruptor (feed to Claude/Cursor)" | X |
| **Support triage & ticket analysis** | @PromptSmithAI: "Feed ticket logs, get structured summaries + action plans. Before: manual backlog sprints." | X |
| **User story generation from requirements** | Azure DevOps AI, Jira Atlassian Intelligence, ChatGPT for user stories | YouTube (multiple tutorials) |
| **Competitive intelligence platforms** | r/aiagents: "Best Customer Intelligence Platforms for 2026" | Reddit |

### Early Adopters

| Use Case | Evidence | Source |
|----------|----------|--------|
| **Backlog grooming & stale item cleanup** | @AragornRuns: "that backlog of annoyances-not-worth-a-morning is just Tuesday" running 24/7 on OpenClaw | X |
| **AI-powered project planning** | n8n + Asana automation: "plan an entire two-week development project complete with epics, user stories, dependencies, and realistic timelines" | YouTube (Shab Noor) |
| **Scrum ceremony automation** | @MatthewRideout: "standups throughout the day, retrospectives to write new docs and guardrails, creating definitions of done for self-validation, writing specs from shorthand" | X |
| **Solo product engineering** | Adam Wynne: "I built a production analytics platform in seven weeks by myself — competitive analysis, domain learning, coding" using AI agents | YouTube |

### Emerging / Experimental

| Use Case | Evidence | Source |
|----------|----------|--------|
| **Agentic user research** | Aakash Gupta: "AI for user research is a mess. It's unreliable. But if you do it the right way, then AI actually isn't going to hallucinate" | YouTube |
| **Agentic demos replacing sales decks** | @Ronald_vanLoon: "An AI agent sits behind your site... it walks the product through" | X |
| **Autonomous Q&A agents** | @cyntro_py: "Notion + Anthropic announced business agents — autonomous Q&A across Slack, email, calendar, Notion; onboarding agents" | X |
| **AI Scrum Master** | Multiple YouTube channels exploring the concept; r/agile: "Scrum Master roles are shrinking" | YouTube, Reddit |

---

## 3. The Metrics & Governance Problem

A critical concern surfaced consistently for POs:

> **"Agentic yes, but is the underlying metric the correct one"** — r/BusinessIntelligence (Feb 23)

Agents optimize at scale — but **if the metric is wrong, they optimize the wrong thing faster**. This makes the PO's metric-definition work exponentially more important.

> "74% of enterprises plan to deploy agentic AI in 2 years. Most will underestimate the hard part." — r/AI_Agents (Feb 23)

The "hard part" is process quality and governance, not technology. For POs this means:

1. **Defining success metrics** becomes the highest-leverage PM activity
2. **Guardrails and constraints** (the "constitution" @CarlosBeneyto references) are now core PM artifacts
3. **Agent accountability** is an open question: @_dannybenson asks "how could we actually hold agents accountable and make them hold up properly in roles and responsibility?"

---

## 4. The Enterprise Reality Check

Reddit's signal is consistently more skeptical than X's enthusiasm:

> **"Our 'AI transformation' cost seven figures and delivered a ChatGPT wrapper"** — r/sysadmin

> **"AI making my job so much harder and fighting every decision I make"** — r/sysadmin

> **"We're shipping an AI product and I'm not sure our security posture covers what it actually needs"** — r/sysadmin (Feb 25)

> **"Why is everyone lying about AI agents"** — r/aiagents (Feb 24) — demanding real case studies over hype

> **"Confused how to use the AI agent within the company"** — r/WorkAdvice (Jan 29) — tensions around PO-style process vs self-serve agent building

**Counter-signal from a real deployment:**
> **"We built an AI agent for our operations team — 6 months later here's what actually happened (the good, bad, unexpected)"** — r/AI_Agents (Feb 25) — genuine retrospective useful for POs evaluating agent ROI

---

## 5. YouTube Transcript Insights

Deep transcript analysis (5,000 tokens/video in deep mode) surfaced nuanced takes not visible from titles alone:

### Aakash Gupta — AI User Research Method (Feb 12, 3.6K views)
> "AI for user research is a mess. It's unreliable. But what if I told you I know how to fix it? There's a real art to doing this right. But if you do it the right way, then AI actually isn't going to hallucinate."

Key insight: AI user research requires **structured prompting with domain constraints**, not open-ended queries. POs need to learn prompt architecture for research, not just for code.

### Career Growth Show — PM in the AI Era (Feb 16)
> "If you're a product manager in 2026, you've probably asked yourself this question at least once. Will AI replace me? And if you haven't asked it yet, your company definitely has."

### Dexter Kuan — The Brutal Truth (Feb 22)
> "Will AI replace product managers? AI can now write PRDs. It can analyze user data. It can generate road maps. So let me ask you something uncomfortable. If AI can already do 70% of what product managers do, what's the 30% that makes you irreplaceable?"

### Product-Led Alliance — What AI Can and Can't Do (Feb 4)
> "When product teams at Airtable started using AI to build prototypes, something unexpected happened. Engineers could suddenly mock up interfaces. Designers could generate backend logic."

Implication: role boundaries are dissolving. The PO doesn't just define requirements — they become the integrator across blurred disciplines.

### The Ezra Klein Show — How Fast Will AI Agents Rip Through the Economy? (Feb 24, 250K views)
> "The thing about covering AI over the past few years is that we're typically talking about the future. Every new model, impressive as it was, seemed like proof of concept for the models that would come next."

High-signal macro discussion on economic impact of agents entering the workforce.

### Azure DevOps AI for Backlog Management (10K views)
> "Imagine if Azure DevOps could help you write better user stories, spot duplicates, and even turn meeting notes into product backlog items."

Practical tutorial showing AI agents integrated directly into PO workflows in Jira and Azure DevOps.

---

## 6. Tools & Platforms for PM/PO Agents

| Tool/Platform | What It Does | Signal Source |
|---------------|-------------|---------------|
| **Microsoft Copilot + Agent 365** | Cross-product data integration, memory across apps, task automation | @MSTCommunity, @Microsoft365Dev, YouTube (multiple) |
| **Copilot Workflows Agent** | Automates Outlook/Teams/SharePoint workflows without code | YouTube (Collaboration Simplified, 342K views) |
| **Jira Atlassian Intelligence** | Backlog grooming, sprint planning, duplicate detection, user story generation | YouTube (Ed Morel, Just Ask Jake) |
| **Azure DevOps AI** | Meeting notes → backlog items, user story writing, duplicate spotting | YouTube (Dani Kahil, 10K views) |
| **n8n + Asana AI Agent** | Automated sprint planning with epics, dependencies, timelines | YouTube (Shab Noor) |
| **OpenClaw agents** | Always-on agents for backlog cleanup, monitoring, outreach | @AragornRuns, @madzadev |
| **OpenAI Agent Builder** | Visual no-code agent building | YouTube (OpenAI, 1.6M views) |
| **Tongyi Lab Personal AI Assistant** | MCP + Ollama, bridges messaging platforms, vector search | @wildmindai (47 likes) |
| **Apollo Agentic GTM Platform** | Sales/marketing stack with agentic positioning | @asteris_ai |
| **Dynamics 365 AI Next Best Action** | Real-time recommendations for leads, opportunities, cases | @inogic |

---

## 7. The Emerging PM Toolkit

Based on all signals, the 2026 PM/PO toolkit is shifting to:

1. **Agent orchestration files** (`agents.md`, `BRAIN.md`, `MEMORY.md`) — defining constraints, permissions, goals, and context for autonomous agents. @johann_sath: "5 files that turn OpenClaw from a chatbot into an employee"
2. **Metric governance frameworks** — what agents can and cannot optimize, with human checkpoints
3. **Agentic user research** — agents conducting continuous discovery across Reddit, X, support tickets, with structured prompting
4. **Backlog automation** — agents doing triage, prioritization, and stale-item cleanup under PM-defined rules
5. **AI prototyping** — PMs building working prototypes directly, blurring the line between PM and engineer
6. **Interactive agentic demos** — replacing slide decks with agents that walk stakeholders through the product

---

## 8. Key Quotes & Voices

| Who | Quote | Platform |
|-----|-------|----------|
| @CarlosBeneyto | "El nuevo PM no gestiona backlog. Diseña el sistema donde la IA produce producto." | X |
| @rangelovbor | "AI in PM is not about replacing the human touch. It's about scaling it." | X |
| @MoodiSadi | "You're not replacing creative judgment with prompts — you're building constraints around specific outputs." | X |
| @twlvone | "AI is already replacing real labor at real companies. Different kind of spend." | X (29 likes) |
| @Foumalin1 | "When everyone is laid off, who is gonna be the customer to buy their product?" | X |
| @_dannybenson | "How could we actually hold agents accountable in a product-oriented, economic context?" | X |
| @johann_sath | "5 files that turn OpenClaw from a chatbot into an employee" | X (34 likes) |
| @PromptSmithAI | "Support triage agents: feed ticket logs, get structured summaries + action plans." | X |
| r/scrum | "My devs are on AI steroids and Scrum is officially too slow. Now what?" | Reddit |
| r/sysadmin | "Our 'AI transformation' cost seven figures and delivered a ChatGPT wrapper" | Reddit |
| Aakash Gupta | "AI for user research is a mess... but if you do it the right way, AI actually isn't going to hallucinate" | YouTube |
| Dexter Kuan | "If AI can already do 70% of what PMs do, what's the 30% that makes you irreplaceable?" | YouTube |

---

## Source Table

### X/Twitter Posts

| Score | Author | Date | Engagement | URL |
|-------|--------|------|------------|-----|
| 86 | @snsf | 2026-02-28 | 151 likes, 9 RT | https://x.com/snsf/status/2027571404745715911 |
| 86 | @DefiCompass | 2026-02-28 | 80 likes, 6 RT | https://x.com/DefiCompass/status/2027753699649462370 |
| 86 | @ZenomTrader | 2026-02-28 | 186 likes, 4 RT | https://x.com/ZenomTrader/status/2027803849780597014 |
| 86 | @DmytroSverba | 2026-02-28 | 18 likes, 1 RT | https://x.com/DmytroSverba/status/2027635266303783138 |
| 84 | @0xreso1ute | 2026-02-25 | 40 likes, 1 RT | https://x.com/0xreso1ute/status/2026538504738713949 |
| 83 | @twlvone | 2026-02-24 | 29 likes | https://x.com/twlvone/status/2026412633495097731 |
| 81 | @threepointone | 2026-02-22 | 61 likes, 1 RT | https://x.com/threepointone/status/2025677924158816479 |
| 79 | @wildmindai | 2026-02-28 | 47 likes, 4 RT | https://x.com/wildmindai/status/2027655500909658534 |
| 79 | @circle | 2026-02-28 | 44 likes, 8 RT | https://x.com/circle/status/2027836202750013543 |
| 78 | @Subit_Crypto | 2026-02-28 | 23 likes, 5 RT | https://x.com/Subit_Crypto/status/2027711007280316590 |
| 76 | @CarlosBeneyto | 2026-02-23 | 21 likes, 2 RT | https://x.com/CarlosBeneyto/status/2025887764189712521 |
| 76 | @RalliesNews | 2026-02-27 | 8 likes, 1 RT | https://x.com/RalliesNews/status/2027337100249465315 |
| 76 | @johann_sath | 2026-02-28 | 34 likes, 3 RT | https://x.com/johann_sath/status/2027819951751594115 |
| 75 | @ArthurMacwaters | 2026-02-26 | 10 likes | https://x.com/ArthurMacwaters/status/2027100767338070296 |
| 74 | @MSTCommunity | 2026-02-27 | 12 likes, 4 RT | https://x.com/MSTCommunity/status/2027451164984221902 |
| 74 | @Microsoft365Dev | 2026-02-26 | 16 likes, 2 RT | https://x.com/Microsoft365Dev/status/2026948100581982353 |
| 72 | @TechByMobolaji_ | 2026-02-27 | 13 likes | https://x.com/TechByMobolaji_/status/2027355884335088123 |
| 70 | @Foumalin1 | 2026-02-27 | 6 likes | https://x.com/Foumalin1/status/2027177917533360172 |
| 69 | @cyntro_py | 2026-02-24 | 26 likes, 1 RT | https://x.com/cyntro_py/status/2026381382113722375 |
| 68 | @elvissun | 2026-02-28 | 12 likes | https://x.com/elvissun/status/2027794704725839968 |
| 67 | @rangelovbor | 2026-02-27 | — | https://x.com/rangelovbor/status/2027428646315524525 |
| 66 | @lexispawn | 2026-02-25 | 7 likes | https://x.com/lexispawn/status/2026790854002876567 |
| 66 | @ivanrvpereira | 2026-02-26 | 3 likes | https://x.com/ivanrvpereira/status/2027021871036641426 |
| 65 | @MatthewRideout | 2026-02-27 | 6 likes | https://x.com/MatthewRideout/status/2027203165263716379 |
| 64 | @aprateem | 2026-02-28 | — | https://x.com/aprateem/status/2027559457639587941 |
| 64 | @asteris_ai | 2026-02-28 | — | https://x.com/asteris_ai/status/2027787945294385193 |
| 64 | @grok | 2026-02-28 | — | https://x.com/grok/status/2027834597229125971 |
| 64 | @bencium | 2026-02-28 | — | https://x.com/bencium/status/2027659349342945319 |
| 64 | @Ronald_vanLoon | 2026-02-28 | — | https://x.com/Ronald_vanLoon/status/2027677867107029013 |
| 64 | @PromptSmithAI | 2026-02-28 | — | https://x.com/PromptSmithAI/status/2027539390734709164 |
| 64 | @_dannybenson | 2026-02-28 | — | https://x.com/_dannybenson/status/2027846376768385441 |
| 64 | @MoodiSadi | 2026-02-28 | — | https://x.com/MoodiSadi/status/2027632801064046726 |
| 64 | @aerezk | 2026-02-28 | — | https://x.com/aerezk/status/2027663906043302060 |
| 64 | @opendallas2023 | 2026-02-28 | — | https://x.com/opendallas2023/status/2027845637769707920 |
| 64 | @TradingTitan108 | 2026-02-28 | — | https://x.com/TradingTitan108/status/2027801482037473620 |
| 63 | @TraderSmith09 | 2026-02-27 | — | https://x.com/TraderSmith09/status/2027181602300940518 |
| 63 | @pantheonsceo | 2026-02-27 | — | https://x.com/pantheonsceo/status/2027279180644422007 |
| 63 | @Adsroidapp | 2026-02-27 | — | https://x.com/Adsroidapp/status/2027388910742192326 |
| 63 | @inogic | 2026-02-27 | — | https://x.com/inogic/status/2027366854386442272 |

### Reddit Threads

| Score | Subreddit | Date | Title | URL |
|-------|-----------|------|-------|-----|
| 73 | r/prodmgmt | 2026-02-21 | How did AI change the Product Manager role in your company? | https://www.reddit.com/r/prodmgmt/comments/1rb1fl1/ |
| 69 | r/BusinessIntelligence | 2026-02-23 | Agentic yes, but is the underlying metric the correct one | https://www.reddit.com/r/BusinessIntelligence/comments/1rcc4ra/ |
| 67 | r/AI_Agents | 2026-02-20 | Want to learn Agentic AI but where? | https://www.reddit.com/r/AI_Agents/comments/1ra029q/ |
| 66 | r/ProductManagement | 2026-02-21 | Keeping up with the new skills required in the PM role | https://www.reddit.com/r/ProductManagement/comments/1ramopf/ |
| 64 | r/vibecoding | 2026-02-26 | Stop "coding" and start orchestrating. The 10x developer is just an AI conductor now | https://www.reddit.com/r/cursor/comments/1rfgtl5/ |
| 62 | r/scrum | 2026-02-14 | My devs are on AI steroids and Scrum is officially too slow. Now what? | https://www.reddit.com/r/scrum/comments/1r4jbys/ |
| 62 | r/careerguidance | 2026-02-23 | I am so confused on the AI jobs takeover. Don't know what is real? | https://www.reddit.com/r/careerguidance/comments/1rcdvzx/ |
| 58 | r/u_James-Robert-543 | 2026-02-13 | How is an AI Agent PM different from a traditional PM? | https://www.reddit.com/r/u_James-Robert-543/comments/1r3o7za/ |
| 58 | r/AI_Agents | 2026-02-21 | AI agents aren't replacing jobs, they're replacing task layers inside jobs | https://www.reddit.com/r/AI_Agents/comments/1raqm5f/ |
| 57 | r/agile | 2026-02-28 | Scrum Master roles are shrinking — where did you move next? | https://www.reddit.com/r/agile/comments/1r8ys5r/ |
| 57 | r/AI_Agents | 2026-02-25 | We built an AI agent for our ops team — 6 months later | https://www.reddit.com/r/AI_Agents/comments/1rebqp8/ |
| 57 | r/AI_Agents | 2026-02-23 | 74% of enterprises plan to deploy agentic AI in 2 years | https://www.reddit.com/r/AI_Agents/comments/1rclhd3/ |
| 56 | r/aiagents | 2026-02-24 | Why is everyone lying about AI agents | https://www.reddit.com/r/aiagents/comments/1rdn5hq/ |
| 54 | r/sysadmin | 2026-02-14 | Our 'AI transformation' cost seven figures and delivered a ChatGPT wrapper | https://www.reddit.com/r/sysadmin/comments/1r3wgjt/ |
| 47 | r/ProductOwner | 2026-01-30 | What do you use AI for as a product owner | https://www.reddit.com/r/ProductOwner/comments/1qr5r1b/ |
| 43 | r/AI_Agents | 2026-02-20 | PM return to work | https://www.reddit.com/r/AI_Agents/comments/1r9ut19/ |
| 39 | r/WorkAdvice | 2026-01-29 | Confused how to use the AI agent within the company | https://www.reddit.com/r/WorkAdvice/comments/1qpxb6j/ |

### YouTube Videos

| Score | Channel | Date | Views | Title | URL |
|-------|---------|------|-------|-------|-----|
| 85 | Aakash Gupta | 2026-02-27 | 1,385 | I Should Be Charging $999 for This AI Prototyping Masterclass | https://www.youtube.com/watch?v=rW4MZEwGYY0 |
| 83 | The Ezra Klein Show | 2026-02-24 | 250,691 | How Fast Will A.I. Agents Rip Through the Economy? | https://www.youtube.com/watch?v=lIJelwO8yHQ |
| 75 | Biotecnika | 2026-02-27 | 614 | Beginner's Guide to Agentic AI | https://www.youtube.com/watch?v=jZ6S-X1RBAY |
| 74 | PML SCHOOL | 2026-02-13 | 38 | Augmented Intelligence in PM: Why AI Won't Replace PMs | https://www.youtube.com/watch?v=gp-G7FV0ZkI |
| 73 | Aakash Gupta | 2026-02-12 | 3,632 | This AI Expert's Method Will Change How You Do Customer Research | https://www.youtube.com/watch?v=rzAGo_XML1U |
| 67 | Aakash Gupta Learnings | 2026-02-28 | 115 | The New PM Superpower Nobody Talks About | https://www.youtube.com/watch?v=2EFiV1ggeEc |
| 64 | Career Growth Show | 2026-02-16 | 16 | PM in the AI Era: Why Your Role Just Changed Forever | https://www.youtube.com/watch?v=e0svoV0VlZI |
| 62 | Product-Led Alliance | 2026-02-04 | 45 | What AI can (and can't) do in product management | https://www.youtube.com/watch?v=sa5FiyCdMBM |
| 61 | TheProfessor | 2026-02-09 | 24 | AI Is Replacing the Entire Product Development Process | https://www.youtube.com/watch?v=d-hwlWmvGdU |
| 61 | Scott Brant | 2025-03-10 | 83,196 | How to Use the NEW Microsoft Planner Copilot Agent for PM | https://www.youtube.com/watch?v=TvaiI69MEGI |
| 61 | Jeff Su | 2025-04-08 | 3,841,838 | AI Agents, Clearly Explained | https://www.youtube.com/watch?v=FwOTs4UxQS4 |
| 61 | Liam Ottley | 2025-03-27 | 2,147,287 | How to Build & Sell AI Agents | https://www.youtube.com/watch?v=w0H1-b044KY |
| 60 | Futurepedia | 2025-05-21 | 3,267,231 | From Zero to Your First AI Agent in 25 Minutes | https://www.youtube.com/watch?v=EH5jx5qPabU |
| 60 | OpenAI | 2025-10-06 | 1,638,177 | Intro to Agent Builder | https://www.youtube.com/watch?v=44eFf-tRiSg |
| 57 | Adam Wynne | 2026-02-18 | 38 | I Replaced a Full Product Engineering Team with AI Agents | https://www.youtube.com/watch?v=h7wdwvlN6PY |
| 55 | Dani Kahil | 2025-08-13 | 10,128 | AI in Azure DevOps — Smarter Product Backlog Management | https://www.youtube.com/watch?v=7apIcZCkd_s |
| 55 | Collaboration Simplified | 2025-11-15 | 342,092 | NEW Copilot Workflows Agent Will Automate Your Job | https://www.youtube.com/watch?v=_w-jVw8Uhc0 |
| 53 | Lenny's Podcast | 2024-10-31 | 175,081 | Product Management Is Dead, So What Are We Doing Instead? | https://www.youtube.com/watch?v=93fCvFkY1Lg |
| 53 | Ed Morel | 2025-04-26 | 9,703 | Jira AI: Top 5 Examples of Using Atlassian Intelligence | https://www.youtube.com/watch?v=zeskGJaihcs |
| 52 | Shab Noor | 2025-08-04 | 3,791 | How I Use n8n to Build an AI Project Manager | https://www.youtube.com/watch?v=hdeBm4r-IOk |
| 51 | Dexter Kuan | 2026-02-22 | 3 | AI Replacing Product Managers — The Brutal Truth | https://www.youtube.com/watch?v=hQp0oQn2Va4 |
| 51 | GeekyBaller | 2025-08-08 | 65,986 | The COMPLETE AI Product Manager Roadmap [2026] | https://www.youtube.com/watch?v=wDBraae1Bjw |
| 50 | McKinsey & Company | 2025-05-07 | 956,587 | The Future of Customer Experience: Embracing Agentic AI | https://www.youtube.com/watch?v=3FN_pC7Sy4I |
| 50 | Aakash Gupta | 2025-07-27 | 56,203 | If This 81 Min Video Doesn't Make You an AI PM, I'll Delete My Channel | https://www.youtube.com/watch?v=MZlKnSJ_gaA |
| 48 | Sustained Agility | 2024-09-26 | 7,800 | AI for Product Owners: Automate Themes, Epics, and User Stories | https://www.youtube.com/watch?v=HydrTL_tPFk |
| 47 | hackajob HQ | 2026-02-04 | 43 | AI can't replace knowing your users | https://www.youtube.com/watch?v=7lN_QwZ9ZxI |
| 46 | Agilemania | 2025-07-21 | 3,962 | What is AI Scrum Master and How You Can Benefit? | https://www.youtube.com/watch?v=UqQ_7vT7tDE |

---

### Source Success Rate

| Source   | Succeeded | Failed | Success % | Notes |
|----------|-----------|--------|-----------|-------|
| X        | 14/14     | 0      | 100%      | ~500+ posts scanned across 23 agents |
| Reddit   | 12/12     | 0      | 100%      | Brave 422 → fell back to OpenAI on all queries |
| YouTube  | 16/16     | 0      | 100%      | ~296 videos found, 63 transcripts extracted (deep mode) |
| Web      | 0/6       | 6      | 0%        | Brave 422 on all queries — `brave_search.py` needs sanitization fix |

---

*Generated by /last30days v2.1 — 23 parallel research agents across 3 sessions*
*2026-02-28*
