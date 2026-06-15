---
name: gw-business-research
description: "Daily business research - pull top topic from queue, NotebookLM -> brief"
---

# /gw-business-research — Daily Business Research Brief

Fires daily. Pulls the top topic from `External Library\BusinessDocuments\_topic-queue.md`. If queue is empty, auto-picks a trending business topic.

## Steps

### 1. Read the queue

Open `D:\Claude Projects\Gridiron Warrior\External Library\BusinessDocuments\_topic-queue.md`.

Find the first topic under `## Active Queue`. Extract topic name + slug from format `- topic name [topic-slug]`.

If queue is empty (no topics under Active Queue):
- Auto-pick a trending business topic relevant to Scott's ICP (high school football + S&C coaches, course launches, Insiders growth, sponsor outreach)
- Set frontmatter flag `auto_picked: true`

### 2. Run NotebookLM research

Use the `mcp__notebooklm__*` MCP server:

1. `notebook_create` with title "Business Research: [topic name]"
2. Use yt-dlp or web search to find 4-6 high-signal sources on the topic (YouTube videos, blog posts, expert tweets)
3. Add sources via `source_add`
4. Query with structured prompt to extract:
   - **Core principles** (3-5 key ideas)
   - **Tactical recommendations** (3-5 specific actions)
   - **Common mistakes** (2-3 anti-patterns)
   - **Best quote** (one memorable line)
   - **GW application** (how this connects to Insiders / Courses / Summit / DFY)

**HARD RULE — NotebookLM auth/availability (identical across gw-sc/ai/business-research):** If the `mcp__notebooklm__*` server is unavailable or any call errors (commonly an expired Google session — `notebook_create` / `source_add` / `notebook_query` return an auth error), do NOT write the brief from the web-search sources alone and do NOT present it as a normal brief. The web sources gathered in step 2 are NOT a substitute for the notebook synthesis. Instead write a STUB brief with `status: blocked`, `notebook_id: null`, `source_count: 0`, and a one-line body naming the cause and the fix (`run nlm login`, then re-invoke). Leave the topic in `## Active Queue` (append ` *(blocked YYYY-MM-DD — NotebookLM auth; retry after nlm login)*`), append the wiki/log line, and exit. Do NOT raw-commit (gw-daily-closeout commits). The blocked stub keeps the `file_today` gate green, but `/gw-morning-readiness` detects `status: blocked` and surfaces it YELLOW with the `nlm login` next action. Scott would rather see one honest "blocked" than a fake-fresh brief.

### 3. Write brief

Save to `D:\Claude Projects\Gridiron Warrior\External Library\BusinessDocuments\YYYY-MM-DD-[topic-slug]-brief.md`:

```markdown
---
title: "[Topic Name] — Business Research Brief"
tags: [business, research, daily-brief, [topic-slug]]
date: YYYY-MM-DD
notebook_id: <notebook-id>
topic: [topic-slug]
source_count: <N>
auto_picked: false|true
pipeline: gw-business-research
---

# [Topic Name]

## Core Principles
1. ...
2. ...
3. ...

## Tactical Recommendations
1. ...
2. ...

## Common Mistakes
1. ...
2. ...

## Best Quote
> "..."

## GW Application
- **Insiders**: ...
- **Courses**: ...
- **Summit**: ...
- **DFY**: ...

## Sources
- <source 1>
- <source 2>
```

### 4. Update queue + index

In `_topic-queue.md`:
- Remove the topic from `## Active Queue`
- Add to `## Completed` as `- YYYY-MM-DD: topic name → [[YYYY-MM-DD-topic-slug-brief|brief]]`

In `_index.md`:
- Add link under `## Daily Research Briefs`: `- YYYY-MM-DD: [[YYYY-MM-DD-topic-slug-brief|topic name]]`

### 5. Append to wiki log

```
2026-MM-DD /gw-business-research: [topic-slug] (auto_picked: false|true)
```

### 6. Do NOT commit

The `gw-daily-closeout` job commits all approved daily-output paths once, after the morning digest, via `scripts/git_safe_commit.py`. This skill's job ends at writing the brief and the wiki/log.md line.

## Notes

- Budget per run: ~$0.10-0.30 in NotebookLM credits
- If NotebookLM is unavailable: see the HARD RULE in step 2 — write a `status: blocked` stub, never a web-only brief.
