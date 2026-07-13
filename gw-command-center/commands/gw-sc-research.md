---
name: gw-sc-research
model: opus
description: "Daily S&C research - pull top topic from queue, NotebookLM -> brief"
---

# /gw-sc-research — Daily Strength & Conditioning Research Brief

Mirror of `/gw-ai-research` and `/gw-business-research` but for strength & conditioning topics drawn from Scott's actual coaching territory. Sources lean on Scott's NotebookLM **S&C Master Resource** notebook plus the Dewey S&C bucket from the daily ingest.

## WIKI CONTAMINATION GUARD (HARD RULE)

This pipeline writes ONLY to `External Library\S-and-C\`. It NEVER writes to `wiki/`. It NEVER adds or modifies wiki concept pages. Promotion of an S&C insight into the wiki happens exclusively through Scott's Sunday `/gw-weekly-synthesis` review. Do not break this wall.

## Steps

### 1. Read the queue

Open `C:\Claude Projects\Gridiron Warrior\External Library\S-and-C\_topic-queue.md`. Find the first topic under `## Active Queue`.

If empty: auto-pick a relevant S&C topic informed by the wiki's coaching themes (in-season programming, contact prep, deceleration, energy systems, recovery, high-school constraints). Flag `auto_picked: true`.

### 2. Run NotebookLM research

Use the `mcp__notebooklm__*` MCP server. This skill uses an **existing** notebook (unlike business research which creates a new one per topic), so the flow is query-against-existing, not create-new.

**Required calls in order:**

1. **Resolve the master notebook ID.** Call `mcp__notebooklm__notebook_list` and find the notebook titled exactly `S&C Master Resource`. Save its `id` as `master_id`. As of 2026-05-18 this is `f4704629-7eab-4d23-ac95-7f8a2d9e826c` with 102 sources — verify it's still present via the list call before using.

2. **Query the master notebook.** Call `mcp__notebooklm__notebook_query` with `notebook_id=master_id` and a structured prompt that asks for the six fields listed below. Capture `notebook_id` in the brief frontmatter.

3. **(Optional, only if master returns thin results)** Create a fresh topic-scoped notebook to supplement: `mcp__notebooklm__notebook_create` with title `S&C Research: [topic name]`, add 3-5 sources via `mcp__notebooklm__source_add` (yt-dlp + web search for high-signal sources), then query. Cross-reference its results with the master via `mcp__notebooklm__cross_notebook_query` if helpful.

4. **Cross-reference the local Dewey S&C bucket** at `External Library\Twitter-Instagram Saves\_by-domain\strength-conditioning\` for anchor authors / recent reels relevant to the topic.

**HARD RULE — NotebookLM errors (identical across gw-sc/ai/business-research):** Never fall back to web-search-only or memory-only synthesis and never present a fallback as a normal brief. But before blocking, classify the error correctly — a transient blip is NOT an auth failure, and the two get different fixes:

1. **Transient error — RETRY first.** A gRPC `INTERNAL` (code 13), `UNAVAILABLE` (14), `DEADLINE_EXCEEDED` (4), a timeout, or any 5xx is a Google-side blip, not a dead token. Retry the failing `notebook_query` up to **3 times** with a short backoff (~15s between attempts). A single transient error must never cost the day's brief. If `notebook_list` already succeeded this run, the session IS valid — a `notebook_query` failure is transient by definition; retry it, do not call it auth.
2. **True auth failure — block with the nlm login fix.** Only when `notebook_list` ITSELF returns an auth/permission error (gRPC `UNAUTHENTICATED` code 16, `PERMISSION_DENIED` code 7, or an explicit expired-session message) is the Google session actually dead.
3. **Block only after the right trigger:** auth failure, OR transient retries exhausted. Write a STUB brief with `status: blocked`, `notebook_id: null`, `source_count: 0`, and a `block_reason:` of either `auth` or `transient`. The one-line body names the cause and the matching fix — `auth` → "run `nlm login`, then re-invoke"; `transient` → "NotebookLM/Google had a server-side blip after N retries; the token is fine — do NOT run nlm login. Re-invoke `/gw-sc-research` or let tonight's run retry." Leave the topic in `## Active Queue` (append ` *(blocked YYYY-MM-DD — <reason>)*`), append the wiki/log line, and exit. Do NOT raw-commit (gw-daily-closeout commits).

A blocked stub now **fails** the job gate (the `not_contains: "status: blocked"` validator in job-contracts.json), so the status grid shows the lane RED and `/gw-morning-readiness` flags YELLOW — two honest signals instead of a fake-fresh green. Scott would rather see one honest "blocked" than a fabricated brief, and he should never be told to `nlm login` when the token works.

**Structured query prompt fields:**
- **Core concept** (the big idea, 2-3 sentences in Scott's plain-language coaching voice)
- **How it works** (3-5 mechanics — physiology, biomechanics, or programming logic)
- **Best practices** (3-5 patterns Scott can use this week)
- **Pitfalls** (2-3 things to avoid, especially for high-school constraints)
- **Best quote** or example
- **GW application** — how this connects to a Film Study, Insiders post, Leech Letter angle, Contact Prep / GW 2.0 / Scores and Stops course, or DFY programming

### 3. Write brief

Save to `C:\Claude Projects\Gridiron Warrior\External Library\S-and-C\YYYY-MM-DD-[topic-slug]-brief.md`:

```markdown
---
title: "[Topic Name] — S&C Research Brief"
tags: [s-and-c, research, daily-brief, [topic-slug]]
date: YYYY-MM-DD
notebook_id: <notebook-id>
topic: [topic-slug]
source_count: <N>
auto_picked: false|true
pipeline: gw-sc-research
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
- **Film Study angle**: ...
- **Insiders post**: ...
- **Leech Letter hook**: ...
- **Course / DFY tie-in**: ...

## Sources
- ...
```

### 4. Update queue + index

Move the researched topic from `## Active Queue` to `## Completed` with `- YYYY-MM-DD - [topic name] [topic-slug]` (and `*(auto-picked)*` if applicable). Preserve all other queue entries unchanged.

### 5. Append to wiki log

```
YYYY-MM-DD /gw-sc-research: [topic-slug] (auto_picked: false|true)
```

### 6. Do NOT commit

The `gw-daily-closeout` job commits all approved daily-output paths once, after the morning digest, via `scripts/git_safe_commit.py`. This skill's job ends at writing the brief and the wiki/log.md line.

## Voice rules (apply to brief body)

- Plain-language coaching tone. Short sentences. Active verbs.
- No em-dashes. No banned words (see CLAUDE.md).
- This is a research brief, not a Leech Letter — present findings cleanly. Scott translates to voice during weekly synthesis or content forge.
