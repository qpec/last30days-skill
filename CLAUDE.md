# CLAUDE.md — last30days-skill

## What This Project Is

A Claude Code skill that researches any topic across Reddit, X/Twitter, YouTube, Podcasts, and the web from the last 30 days. Surfaces real community discussions ranked by engagement (upvotes, likes, views) and generates actionable prompts.

**Version:** 3.0
**License:** MIT
**Repo:** https://github.com/mvanhorn/last30days-skill

---

## Quick Reference

### Invoking the Skill

```
/last30days [topic]
/last30 [topic]                          # alias
/last30days AI video tools for ChatGPT   # with target tool
```

### Running the Research Script Directly

```bash
python3 scripts/last30days.py "topic" [flags]
```

### Common Flag Combinations

```bash
# Quick X-only scan
python3 scripts/last30days.py "topic" --sources=x --quick --emit=compact

# Deep Reddit research
python3 scripts/last30days.py "topic" --sources=reddit --deep --emit=compact

# Full research, all sources, JSON output
python3 scripts/last30days.py "topic" --deep --emit=json

# Check which APIs are available
python3 scripts/last30days.py "test" --diagnose

# Use fixture data (no API calls)
python3 scripts/last30days.py "topic" --mock
```

---

## Standard Research Method

When the user asks to research a topic, follow this workflow:

### 1. Determine Scope

| User Says | Agents | Depth | Sources |
|-----------|--------|-------|---------|
| "research X" | 3-5 | `--deep` | `--sources=auto` |
| "deep research X" | 5-10 | `--deep` | multiple angles |
| "deep research X with N agents" | N (max 20) | `--deep` | parallel, different angles |

**Default depth is always `--deep`.** Only use `--quick` if the user explicitly asks for a quick/fast scan.

**Max 20 parallel Bash calls per message.** Use all 20 when the user asks for thorough research.

### 2. Launch Parallel Research

Split the topic into distinct angles and launch them **in parallel using multiple Bash tool calls in a single message**. All calls run directly from Claude Code (Opus) — no subagents, no Task tool.

Each parallel Bash call runs:
```bash
cd /c/Users/ynhan/Desktop/Repositories/last30days-skill && python3 scripts/last30days.py "angle" --sources=x|reddit --quick|--deep --emit=compact 2>&1
```

**Splitting strategy:**
- Mix X/Twitter (`--sources=x`) with Reddit (`--sources=reddit`) across the parallel calls
- Cover the topic from multiple angles (e.g., "AI adoption enterprise", "AI adoption healthcare", "AI adoption challenges")
- Each call targets one source to avoid redundant API calls
- Aim for ~70% X agents / ~30% Reddit agents (X has more real-time signal, Reddit has deeper discussion)

**Example — 10 agents on "AI adoption":**
```
Bash 1:  "AI adoption enterprise"         --sources=x      --deep
Bash 2:  "AI adoption challenges barriers" --sources=x      --deep
Bash 3:  "AI adoption startups"           --sources=x      --deep
Bash 4:  "AI adoption healthcare"         --sources=x      --deep
Bash 5:  "AI adoption education"          --sources=x      --deep
Bash 6:  "AI replacing jobs workforce"    --sources=x      --deep
Bash 7:  "AI regulation policy"           --sources=x      --deep
Bash 8:  "AI adoption trends"             --sources=reddit  --deep
Bash 9:  "AI coding agents adoption"      --sources=reddit  --deep
Bash 10: "AI tools ROI adoption"          --sources=reddit  --deep
```

### 3. Synthesize Results

Claude Code synthesizes directly in the same session. After all parallel Bash calls return:
- Identify recurring themes across results
- Rank by engagement (likes, upvotes, RTs)
- Extract direct quotes with attribution
- Build a narrative structure with clear sections
- **Always include a Source Success Table** showing which sources succeeded/failed across all agents:

```
### Source Success Rate
| Source   | Succeeded | Failed | Success % | Notes                    |
|----------|-----------|--------|-----------|--------------------------|
| X        | 7/7       | 0      | 100%      |                          |
| Reddit   | 3/3       | 0      | 100%      | via Tavily               |
| YouTube  | 10/10     | 0      | 100%      | 72 transcripts extracted |
| Podcast  | 5/5       | 0      | 100%      | via Tavily + Listen Notes |
| Web      | 3/3       | 0      | 100%      | via Tavily               |
```

**Cost model:** Only external API costs apply (~$0.02/call for OpenAI normalization). Bird/X search is free. Tavily has a free tier. Everything runs in the Claude Code Opus session.

### 4. Extract Testable Claims

After synthesis, identify **3-7 testable claims** from the Phase 1 data. Each claim must be:
- **Specific** — includes a number, trend direction, or named entity
- **Verifiable** — can be checked against external data

Example:
```
1. "Software dev postings down 70% from 2022 peak" — @aitoolshaven
2. "Junior developer roles down 20% since 2022" — @neurawebtech
3. "AI/ML engineers command 56% salary premium" — @grok
4. "India tech hiring up 9% MoM in March 2026" — @moneycontrolcom
5. "550K+ tech layoffs since 2022" — @glynch1234
```

### 5. Validate Against Authoritative Sources (Phase 2)

Launch **3-5 parallel validation searches** using Claude's `WebSearch` tool (not the Python script). Each search targets 1-2 claims from Step 4.

**Search strategy per claim — run 3-4 targeted searches:**
1. Government/statistical source (BLS, FRED, Eurostat, CBS)
2. Industry report (McKinsey, Gartner, Stack Overflow survey)
3. Quality journalism (Bloomberg, WSJ, TechCrunch)
4. Job market data platform (Indeed Hiring Lab, LinkedIn Economic Graph)

Use `WebFetch` to retrieve full data when a search result looks promising.

**Validation output format per claim:**
```
THEME: "Junior developer roles down 20% since 2022"
STATUS: PARTIALLY CONFIRMED
AUTHORITATIVE SOURCES:
- BLS: Software dev employment grew 2.1% in 2024 but QA roles declined 8% (bls.gov/ooh)
- Indeed Hiring Lab: Entry-level tech postings down 34% from 2022 peak (hiringlab.org)
- Stack Overflow 2025: 62% of respondents report fewer junior openings
NUANCE: The 20% figure appears US-specific and varies by sub-role
```

**Status values:**
- ✅ Confirmed — authoritative source corroborates
- ⚠️ Partially — directionally correct, numbers differ
- ❌ Contradicted — authoritative source disagrees
- ❓ Unverified — no authoritative source found

### 6. Merge Validation into Report

Incorporate Phase 2 findings into the final report:
- Add an **Authority Check table** (see Report Writing Standards)
- Assign **source tiers** to all sources
- Add **confidence ratings** to each thematic section
- Weave authoritative data into the narrative alongside community signal

### 7. Write Report to File

When the user asks for a report/rapportage:
- Write to a date-prefixed `.md` file in the project root (e.g., `2026-02-28-topic.md`)
- Include ALL sources with URLs in a table at the bottom
- Always provide the full file path back to the user

---

## Flags Reference

| Flag | Values | Default | Purpose |
|------|--------|---------|---------|
| `--emit` | `compact`, `json`, `md`, `context`, `path` | `compact` | Output format |
| `--sources` | `auto`, `reddit`, `x`, `both` | `auto` | Source selection |
| `--quick` | flag | OFF | Fast mode: 8-12 items/source, 90s timeout |
| `--deep` | flag | OFF | Deep mode: 40-70 items/source, 300s timeout |
| `--mock` | flag | OFF | Use fixture data, no API calls |
| `--debug` | flag | OFF | Verbose logging to stderr |
| `--days=N` | integer | 30 | Custom lookback period |
| `--store` | flag | OFF | Persist to SQLite |
| `--diagnose` | flag | OFF | Show API availability and exit |
| `--timeout=N` | seconds | varies | Override global timeout |
| `--include-web` | flag | OFF | Force web search |
| `--refresh` | flag | OFF | Bypass 24-hour cache |

---

## Environment & API Keys

**Config file:** `~/.config/last30days/.env`

```bash
# Required for Reddit (via OpenAI Responses API fallback)
OPENAI_API_KEY=sk-...

# X/Twitter — Bird (free, preferred)
AUTH_TOKEN=...                # X auth token (browser cookie)
CT0=...                       # X CSRF token (browser cookie)

# X/Twitter — xAI (paid alternative)
XAI_API_KEY=xai-...

# Tavily Search (preferred for Reddit discovery, web search, and podcast discovery)
TAVILY_API_KEY=tvly-...       # Tavily (free tier available)

# Podcast transcript enrichment (optional)
LISTEN_NOTES_API_KEY=...      # Listen Notes (free tier: 300 req/month)

# Web search backends (Tavily preferred, others as fallback)
BRAVE_API_KEY=...             # Brave Search (free tier: 2K/month, fallback)
PARALLEL_API_KEY=...          # Parallel AI
OPENROUTER_API_KEY=...        # OpenRouter (Sonar Pro)
```

**Check availability:** `python3 scripts/last30days.py "test" --diagnose`

---

## Project Structure

```
scripts/
├── last30days.py              # Main orchestrator
├── watchlist.py               # Topic watchlist CLI
├── store.py                   # SQLite persistence
├── briefing.py                # Morning briefing generator
└── lib/
    ├── bird_x.py              # X via Bird (free, GraphQL)
    ├── xai_x.py               # X via xAI API
    ├── tavily_reddit.py        # Reddit via Tavily (preferred)
    ├── brave_reddit.py         # Reddit via Brave Search (fallback)
    ├── openai_reddit.py        # Reddit via OpenAI API (last resort)
    ├── tavily_search.py        # Web search via Tavily (preferred)
    ├── brave_search.py         # Web search via Brave (fallback)
    ├── podcast_search.py       # Podcast discovery + transcript enrichment
    ├── youtube_yt.py           # YouTube via yt-dlp
    ├── websearch.py            # Web search normalization
    ├── reddit_enrich.py        # Reddit engagement enrichment
    ├── env.py                  # Config & API key loading
    ├── models.py               # Model auto-selection
    ├── cache.py                # 24-hour TTL cache
    ├── http.py                 # Stdlib-only HTTP client
    ├── dates.py                # Date range helpers
    ├── score.py                # Engagement-aware scoring
    ├── normalize.py            # API response → canonical schema
    ├── dedupe.py               # Near-duplicate detection
    ├── schema.py               # Dataclass definitions
    ├── entity_extract.py       # Entity extraction
    ├── render.py               # Output formatting (folder-based)
    └── vendor/bird-search/     # Vendored Bird v0.8.0
```

**Output directory:** `~/.local/share/last30days/out/`
**Per-run output:** `~/.local/share/last30days/out/{topic}_{timestamp}/`
  - `01-raw-data-full.json` — Complete data with full YouTube transcripts
  - `02-raw-data-compact.json` — Truncated transcripts for compact output
  - `03-report.md` — Full markdown report
  - `04-summary.md` — Context snippet for reuse

**Cache directory:** `~/.cache/last30days/`
**Database:** `~/.local/share/last30days/research.db` (watchlist mode)

---

## Coding Conventions

### Python

- **Python 3.9+**, type hints throughout
- **Stdlib-only HTTP** — no `requests` library, uses `urllib`
- **Dataclasses** for all data models (see `schema.py`)
- **Logging to stderr** — stdout is reserved for output (consumed by Claude)
- **Internal functions** prefixed with `_` (e.g., `_log_info`)
- **Error handling:** retry with exponential backoff on 429/5xx, no retry on 4xx

### Logging Pattern

```python
def _log_error(msg: str):
    sys.stderr.write(f"[MODULE ERROR] {msg}\n")
    sys.stderr.flush()
```

### API Client Pattern

Each source module follows:
1. Prompt template at module level
2. Depth config dict (`quick`/`default`/`deep`)
3. `search()` function as entry point
4. Return list of normalized dicts

### Tests

```bash
python3 -m pytest tests/
```

Test files follow: `tests/test_{module}.py`
Fixtures in: `fixtures/`

### Commits

```
feat: new feature
fix: bug fix
docs: documentation
refactor: code refactoring
```

---

## Scoring System

Three-factor scoring (0-100):

| Factor | Weight | Source |
|--------|--------|--------|
| Relevance | 45% | Semantic match to topic |
| Recency | 25% | How recent within lookback window |
| Engagement | 30% | log-normalized upvotes/likes/views |

**Reddit engagement:** `0.55*log(score) + 0.40*log(comments) + 0.05*(upvote_ratio*10)`
**X engagement:** `0.55*log(likes) + 0.25*log(reposts) + 0.15*log(replies) + 0.05*log(quotes)`
**Podcast scoring:** `0.60*relevance + 0.25*recency + 0.15*engagement_bonus`
**Web (no engagement):** Relevance 55%, Recency 45%, -15 penalty

---

## Search Backend Priority

### Reddit Discovery
1. **Tavily** (preferred) — domain-filtered search, reliable, good date parsing
2. **Brave Search** (fallback) — has been returning 422 errors
3. **OpenAI Responses API** (last resort) — more expensive, LLM dependency

### Web Search
1. **Parallel AI** (if configured)
2. **Tavily** (preferred default)
3. **Brave Search** (fallback)
4. **OpenRouter/Sonar Pro** (fallback)

### Podcast Discovery
1. **Tavily** — domain-filtered to podcast platforms (Apple, Spotify, etc.)
2. **Listen Notes API** — direct search + transcript enrichment (optional)

---

## Report Writing Standards

When writing research reports to file:

1. **Header:** Title, date, method, data sources, period
2. **Executive summary:** 2-3 sentences capturing the main insight
3. **Thematic sections:** Organized by theme, not by source
4. **Direct quotes:** Use `>` blockquotes with `@handle` or `r/subreddit` attribution
5. **Source tables:** ALL sources with URLs at the bottom, organized by category
6. **Footer:** Generation method and date

**File naming:** `YYYY-MM-DD-{topic-slug}.md` in project root (date-prefixed for chronological sorting)

**Example:** `2026-02-28-pm-po-role-change-ai.md`

---

## Known Issues (Windows)

- Bird (X search) may throw `UnicodeDecodeError` on Windows due to cp1252 encoding — the search still completes, results are valid
- Bird handle drilldown may fail with `UV_HANDLE_CLOSING` assertion — Phase 2 enrichment is best-effort, Phase 1 results are always available
- **YouTube:** `yt-dlp` is installed but its Scripts dir is not in PATH by default. Run this at session start:
  ```
  export PATH="$PATH:/c/Users/ynhan/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0/LocalCache/local-packages/Python312/Scripts"
  ```
