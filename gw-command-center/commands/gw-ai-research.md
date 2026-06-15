---
name: gw-ai-research
description: "Daily AI research - pull top topic from queue, NotebookLM -> brief"
---

# /gw-ai-research — Daily AI Research Brief

Mirror of `/gw-business-research` but for AI topics.

## Steps

### 1. Read the queue

Open `D:\Claude Projects\Gridiron Warrior\External Library\AI\_topic-queue.md`. Find first topic under `## Active Queue`.

If empty: auto-pick a trending AI topic relevant to a small-business AI user (Claude, Anthropic SDK, Obsidian + AI, prompting, automation, MCP, agent design). Flag `auto_picked: true`.

### 2. Run NotebookLM research

Same flow as business research but with AI-relevant sources (Anthropic docs, AI Twitter, dev YouTube, Claude release notes).

**HARD RULE — NotebookLM auth/availability (identical across gw-sc/ai/business-research):** If the `mcp__notebooklm__*` server is unavailable or any call errors (commonly an expired Google session — `notebook_list` returns an auth error, or Chrome/CDP is missing in a headless run), do NOT fall back to web-search-only or memory-only synthesis, and do NOT present the result as a normal brief. Instead write a STUB brief with `status: blocked`, `notebook_id: null`, `source_count: 0`, and a one-line body naming the cause and the fix (`run nlm login`, then re-invoke). Leave the topic in `## Active Queue` (append ` *(blocked YYYY-MM-DD — NotebookLM auth; retry after nlm login)*`), append the wiki/log line, and exit. Do NOT raw-commit (gw-daily-closeout commits). The blocked stub keeps the `file_today` gate green, but `/gw-morning-readiness` detects `status: blocked` and surfaces it YELLOW with the `nlm login` next action. Scott would rather see one honest "blocked" than a fake-fresh brief.

Structured query:
- **Core concept** (the big idea, 2-3 sentences)
- **How it works** (3-5 mechanics)
- **Best practices** (3-5 patterns)
- **Pitfalls** (2-3 things to avoid)
- **Best quote** or example
- **GW application** — how this connects to the Command Center, Content Forge, Dewey ingest, daily seeds, etc.

### 3. Write brief

Save to `D:\Claude Projects\Gridiron Warrior\External Library\AI\YYYY-MM-DD-[topic-slug]-brief.md`:

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
