---
name: gw-ai-research
model: opus
description: "Daily AI research - pull top topic from queue, NotebookLM -> brief"
---

# /gw-ai-research — Daily AI Research Brief

Mirror of `/gw-business-research` but for AI topics.

## Steps

### 1. Read the queue

Open `C:\Claude Projects\Gridiron Warrior\External Library\AI\_topic-queue.md`. Find first topic under `## Active Queue`.

If empty: auto-pick a trending AI topic relevant to a small-business AI user (Claude, Anthropic SDK, Obsidian + AI, prompting, automation, MCP, agent design). Flag `auto_picked: true`.

### 2. Run NotebookLM research

Use the `mcp__notebooklm__*` MCP server. Same explicit flow as `/gw-business-research`, with AI-relevant sources (Anthropic docs, AI Twitter, dev YouTube, Claude release notes):

1. `notebook_create` with title "AI Research: [topic name] — [date]" → capture the returned `notebook_id`
2. Use yt-dlp or web search to find 4-6 high-signal sources on the topic
3. Add sources via `source_add`
4. Query with `notebook_query` (notebook_id from step 1) using the structured prompt below

**Never call `research_start` without a `notebook_id`.** The MCP advertises "creates new notebook if not provided," but that auto-create path is NOT implemented (verified in `notebooklm_tools/core/research.py`): a null notebook_id builds a request to `/notebook/None` and NotebookLM rejects it with `INVALID_ARGUMENT` (Google API error code 3). This presents as a fake "transient" block and silently kills the day's AI brief. If you want `research_start`'s web auto-crawl, `notebook_create` FIRST, then `research_start(notebook_id=<that id>)` → poll → import → query. The numbered `source_add` flow above avoids it entirely and is the default.

**HARD RULE — NotebookLM errors (identical across gw-sc/ai/business-research):** Never fall back to web-search-only or memory-only synthesis and never present a fallback as a normal brief. But before blocking, classify the error correctly — a transient blip is NOT an auth failure, and the two get different fixes:

1. **Transient error — RETRY first.** A gRPC `INTERNAL` (code 13), `UNAVAILABLE` (14), `DEADLINE_EXCEEDED` (4), a timeout, or any 5xx is a Google-side blip, not a dead token. Retry the failing call up to **3 times** with a short backoff (~15s between attempts). A single transient error must never cost the day's brief. If `notebook_list` already succeeded this run, the session IS valid — a later failure is transient by definition; retry it, do not call it auth.
2. **True auth failure — block with the nlm login fix.** Only when `notebook_list` ITSELF returns an auth/permission error (gRPC `UNAUTHENTICATED` code 16, `PERMISSION_DENIED` code 7, or an explicit expired-session message) is the Google session actually dead. (A genuinely missing Chrome/CDP in a headless run also blocks here, with that cause named.)
3. **Block only after the right trigger:** auth failure, OR transient retries exhausted. Write a STUB brief with `status: blocked`, `notebook_id: null`, `source_count: 0`, and a `block_reason:` of either `auth` or `transient`. The one-line body names the cause and the matching fix — `auth` → "run `nlm login`, then re-invoke"; `transient` → "NotebookLM/Google had a server-side blip after N retries; the token is fine — do NOT run nlm login. Re-invoke or let tonight's run retry." Leave the topic in `## Active Queue` (append ` *(blocked YYYY-MM-DD — <reason>)*`), append the wiki/log line, and exit. Do NOT raw-commit (gw-daily-closeout commits).

A blocked stub now **fails** the job gate (the `not_contains: "status: blocked"` validator in job-contracts.json), so the status grid shows the lane RED and `/gw-morning-readiness` flags YELLOW — two honest signals instead of a fake-fresh green. Scott would rather see one honest "blocked" than a fabricated brief, and he should never be told to `nlm login` when the token works.

Structured query:
- **Core concept** (the big idea, 2-3 sentences)
- **How it works** (3-5 mechanics)
- **Best practices** (3-5 patterns)
- **Pitfalls** (2-3 things to avoid)
- **Best quote** or example
- **GW application** — how this connects to the Command Center, Content Forge, Dewey ingest, daily seeds, etc.

### 3. Write brief

Save to `C:\Claude Projects\Gridiron Warrior\External Library\AI\YYYY-MM-DD-[topic-slug]-brief.md`:

```markdown
---
title: "[Topic Name] — AI Research Brief"
tags: [ai, research, daily-brief, [topic-slug]]
date: YYYY-MM-DD
notebook_id: <notebook-id>
topic: [topic-slug]
source_count: <N>
auto_picked: false|true
pipeline: gw-ai-research
---

# [Topic Name]

## Core Concept
...

## How It Works
1. ...
2. ...

## Best Practices
1. ...
2. ...

## Pitfalls
1. ...
2. ...

## Best Quote / Example
...

## GW Application
- **Vault ingest**: ...
- **Content Forge**: ...
- **Daily seeds**: ...
- **Other**: ...

## Sources
- ...
```

### 4. Update queue + index

Same pattern as business research.

### 5. Append to wiki log

```
2026-MM-DD /gw-ai-research: [topic-slug] (auto_picked: false|true)
```

Do NOT run `git commit`. The `gw-daily-closeout` job commits all approved daily-output paths once, after the morning digest, via `scripts/git_safe_commit.py`. This skill's job ends at writing the brief and the wiki/log.md line.
