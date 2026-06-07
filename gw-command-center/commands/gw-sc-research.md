---
description: "Daily S&C research — pull top topic from queue, NotebookLM → brief"
---

# /gw-sc-research — Daily Strength & Conditioning Research Brief

Mirror of `/gw-ai-research` and `/gw-business-research` but for strength & conditioning topics drawn from Scott's actual coaching territory. Sources lean on Scott's NotebookLM **S&C Master Resource** notebook plus the Dewey S&C bucket from the daily ingest.

## WIKI CONTAMINATION GUARD (HARD RULE)

This pipeline writes ONLY to `External Library\S-and-C\`. It NEVER writes to `wiki/`. It NEVER adds or modifies wiki concept pages. Promotion of an S&C insight into the wiki happens exclusively through Scott's Sunday `/gw-weekly-synthesis` review. Do not break this wall.

## Steps

### 1. Read the queue

Open `D:\Claude Projects\Gridiron Warrior\External Library\S-and-C\_topic-queue.md`. Find the first topic under `## Active Queue`.

If empty: auto-pick a relevant S&C topic informed by the wiki's coaching themes (in-season programming, contact prep, deceleration, energy systems, recovery, high-school constraints). Flag `auto_picked: true`.

### 2. Run NotebookLM research

Use the `mcp__notebooklm__*` MCP server. This skill uses an **existing** notebook (unlike business research which creates a new one per topic), so the flow is query-against-existing, not create-new.

**Required calls in order:**

1. **Resolve the master notebook ID.** Call `mcp__notebooklm__notebook_list` and find the notebook titled exactly `S&C Master Resource`. Save its `id` as `master_id`. As of 2026-05-18 this is `f4704629-7eab-4d23-ac95-7f8a2d9e826c` with 102 sources — verify it's still present via the list call before using.

2. **Query the master notebook.** Call `mcp__notebooklm__notebook_query` with `notebook_id=master_id` and a structured prompt that asks for the six fields listed below. Capture `notebook_id` in the brief frontmatter.

3. **(Optional, only if master returns thin results)** Create a fresh topic-scoped notebook to supplement: `mcp__notebooklm__notebook_create` with title `S&C Research: [topic name]`, add 3-5 sources via `mcp__notebooklm__source_add` (yt-dlp + web search for high-signal sources), then query. Cross-reference its results with the master via `mcp__notebooklm__cross_notebook_query` if helpful.

4. **Cross-reference the local Dewey S&C bucket** at `External Library\Twitter-Instagram Saves\_by-domain\strength-conditioning\` for anchor authors / recent reels relevant to the topic.

**HARD RULE:** If the MCP server isn't available or `notebook_list` errors, do NOT silently fall back to memory-only synthesis. Write a stub brief with frontmatter `status: blocked` and `notebook_id: null`, append `(blocked)` to the queue + index entries, commit, and exit. Scott would rather see "blocked" and re-run later than get a fake brief that looks fresh but isn't.

**Structured query prompt fields:**
- **Core concept** (the big idea, 2-3 sentences in Scott's plain-language coaching voice)
- **How it works** (3-5 mechanics — physiology, biomechanics, or programming logic)
- **Best practices** (3-5 patterns Scott can use this week)
- **Pitfalls** (2-3 things to avoid, especially for high-school constraints)
- **Best quote** or example
- **GW application** — how this connects to a Film Study, Insiders post, Leech Letter angle, Contact Prep / GW 2.0 / Scores and Stops course, or DFY programming

### 3. Write brief

Save to `D:\Claude Projects\Gridiron Warrior\External Library\S-and-C\YYYY-MM-DD-[topic-slug]-brief.md`:

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
