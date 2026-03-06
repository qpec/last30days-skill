# Design: Authoritative Validation Layer for Research Reports

**Date:** 2026-03-06
**Status:** Approved
**Problem:** Research reports rely almost entirely on community sources (X, Reddit, YouTube, Podcasts). They lack authoritative data from government statistics, industry analysts, and quality journalism. Claims go unverified.

---

## Architecture: Two-Phase Research

### Current Flow
```
User request → 20 parallel narrative agents (X/Reddit/YouTube/Podcasts) → Synthesis → Report
```

### New Flow
```
User request
  → Phase 1: 15-20 narrative agents (X/Reddit/YouTube/Podcasts)
  → Theme extraction: Claude identifies 3-7 testable claims
  → Phase 2: 3-5 validation agents (WebSearch targeting authoritative domains)
  → Final synthesis: narrative + authority data merged
  → Report with Authority Check table
```

**Key principle:** X/Reddit/YouTube discover *what people are talking about*. Validation agents confirm *whether it's true*.

---

## Phase 1: Narrative Agents (No Changes)

Existing parallel Bash agents running `python3 scripts/last30days.py` with `--sources=x|reddit` and `--deep --emit=compact`. No code changes.

## Theme Extraction (New Step)

After Phase 1 returns, Claude extracts 3-7 **testable claims** from the raw data. Each claim must be:
- Specific (includes a number, trend direction, or named entity)
- Verifiable (can be checked against external data)

Example output:
```
1. "Software dev postings down 70% from 2022 peak" — from @aitoolshaven
2. "Junior developer roles down 20% since 2022" — from @neurawebtech
3. "AI/ML engineers command 56% salary premium" — from @grok
4. "India tech hiring up 9% MoM in March 2026" — from @moneycontrolcom
5. "550K+ tech layoffs since 2022" — from @glynch1234
```

## Phase 2: Validation Agents (New)

3-5 parallel validation agents, each using Claude's `WebSearch` and `WebFetch` tools (not the Python script). Each agent takes 1-2 themes and searches authoritative sources.

### Search Strategy Per Theme

For each claim, run 3-4 targeted web searches:
1. Government/statistical source (BLS, FRED, Eurostat, CBS)
2. Industry report (McKinsey, Gartner, Stack Overflow survey)
3. Quality journalism (Bloomberg, WSJ, TechCrunch)
4. Job market data platform (Indeed Hiring Lab, LinkedIn Economic Graph)

### Global Authoritative Source Priority

| Category | Sources |
|----------|---------|
| Government/Stats | BLS.gov, FRED (St. Louis Fed), Eurostat, OECD, Census.gov |
| Job Market Data | Indeed Hiring Lab, LinkedIn Economic Graph, Glassdoor, Levels.fyi |
| Industry Analysts | McKinsey, Gartner, Deloitte, Forrester, IDC |
| Industry Surveys | Stack Overflow Developer Survey, JetBrains State of Dev, GitHub Octoverse |
| Quality Journalism | Bloomberg, WSJ, Reuters, TechCrunch, The Information, Ars Technica |
| Academic/Think Tank | Brookings, Stanford HAI, MIT CSAIL, World Economic Forum |

### Netherlands Authoritative Sources (When NL-Relevant)

Activated when topic mentions: Netherlands, Dutch, Holland, NL, Amsterdam, Eindhoven, Rotterdam, etc.

| Category | Sources |
|----------|---------|
| Government/Stats | CBS.nl (Centraal Bureau voor de Statistiek), UWV Arbeidsmarktinformatie, Rijksoverheid.nl |
| Labor Market | UWV Barometer Arbeidsmarkt, CBS StatLine (ICT sector) |
| Industry Bodies | Nederland ICT, Dutch Digital, NLdigital, Brainport Eindhoven |
| Salary/Job Data | Glassdoor.nl, Intermediair Salarisgids, Nationale Vacaturebank, Indeed.nl |
| Industry Reports | ABN AMRO sectorrapport IT, ING Economisch Bureau ICT, Computable.nl |
| Journalism | FD (Financieele Dagblad), NRC, Tweakers.net, AG Connect, Computable.nl |
| Research | SER (Sociaal-Economische Raad), TNO, TU Delft, Rathenau Instituut |
| Recruitment | Randstad ICT, Yacht, Hays NL salary guide, Robert Half NL |

### Validation Agent Output Format

```
THEME: "Junior developer roles down 20% since 2022"
STATUS: PARTIALLY CONFIRMED
AUTHORITATIVE SOURCES:
- BLS: Software dev employment grew 2.1% in 2024 but QA roles declined 8% (bls.gov/ooh)
- Indeed Hiring Lab: Entry-level tech postings down 34% from 2022 peak (hiringlab.org)
- Stack Overflow 2025: 62% of respondents report fewer junior openings
NUANCE: The 20% figure appears US-specific and varies by sub-role
```

---

## Report Format Changes

### 1. Authority Check Table

Added after each major section or as a consolidated table:

```markdown
| # | Claim | Community Source | Authority Source | Status |
|---|-------|-----------------|------------------|--------|
| 1 | Dev postings -70% from peak | @aitoolshaven | FRED: -67% confirmed | ✅ Confirmed |
| 2 | Junior roles -20% | @neurawebtech | BLS: -15% entry SWE | ⚠️ Partially |
| 3 | AI/ML 56% premium | @grok | Levels.fyi: 42% premium | ⚠️ Overstated |
| 4 | India hiring +9% | @moneycontrolcom | No independent source | ❓ Unverified |
```

Status values:
- ✅ Confirmed — authoritative source corroborates
- ⚠️ Partially — directionally correct, numbers differ
- ❌ Contradicted — authoritative source disagrees
- ❓ Unverified — no authoritative source found

### 2. Source Tier System

Every source gets a tier label:
- **Tier 1** — Government data, peer-reviewed research
- **Tier 2** — Industry reports with methodology
- **Tier 3** — Quality journalism with editorial standards
- **Tier 4** — Community signal (X, Reddit, YouTube, Podcasts)

Source tables add a "Tier" column.

### 3. Section Confidence Ratings

Each thematic section gets a confidence badge based on source tier mix:
- **HIGH** — Backed by 2+ Tier 1-2 sources
- **MEDIUM** — Backed by 1 Tier 1-2 source or 3+ Tier 3 sources
- **LOW** — Community signal only (Tier 4)

---

## Implementation Scope

### What Changes

1. **CLAUDE.md** — Update Standard Research Method to include Phase 2 validation workflow
2. **CLAUDE.md** — Add authoritative source lists (global + NL)
3. **CLAUDE.md** — Update Report Writing Standards with authority check table, tiers, confidence ratings

### What Does NOT Change

- Python scripts (no code changes)
- Phase 1 agent workflow (same parallel Bash calls)
- Obsidian integration
- Output folder structure

### Cost Impact

- Phase 2 adds 3-5 `WebSearch` calls per research run (free, built into Claude)
- Phase 2 may add 2-5 `WebFetch` calls for full article retrieval (free)
- No additional external API costs
- Extra time: ~30-60 seconds for Phase 2

---

## Success Criteria

1. Every research report includes an Authority Check table
2. At least 50% of key claims are validated against Tier 1-2 sources
3. NL-relevant research includes CBS/UWV/FD data when available
4. Source tables show tier labels for all sources
5. Each section has a confidence rating
