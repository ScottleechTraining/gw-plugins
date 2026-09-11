---
name: gw-ai-research
model: claude-opus-5
description: "Daily AI research - pull top topic from queue, NotebookLM -> brief"
---

# /gw-ai-research — Daily AI Research Brief

Mirror of `/gw-business-research` but for AI topics.

Scope: one topic, one brief, plus the queue, index, and log updates the steps below name. Do not research a second topic, do not add sections the brief template does not have, and do not write files outside the paths this command names. Finish every step through the wiki log line before you report.

## Steps

### 1. Read the queue

Open `C:\Claude Projects\Gridiron Warrior\External Library\AI\_topic-queue.md`. Find first topic under `## Active Queue`.

If empty: auto-pick a trending AI topic relevant to a small-business AI user (Claude, Anthropic SDK, Obsidian + AI, prompting, automation, MCP, agent design). Flag `auto_picked: true`.

### 1b. Frame the question (D5, 2026-09-10)

Same topic, same order: the first active bullet stays the pick. Before any NotebookLM call, write four lines for it. They go into the brief frontmatter and they lead the structured prompt.

- `question`: one specific question Scott as the operator of this pipeline is deciding this week, in plain words. Not the topic restated. Shape: "With 15 minutes left after practice, what recovery work is worth keeping?" (that is an example of shape, not a training recommendation).
- `decision`: a workflow or tool decision (build, adopt, change, or skip), in one clause.
- `audience`: who is asking and their real constraint (season, staff, budget, tools). Unknown stays unknown: write `constraints unknown`, never invent one.
- `question_source`: `queue`, or `ds-<slug>` when a record in `wiki/business/coach-demand-signals.md` supplied the question, or `scott` when the queue line marks it as his request.

Scan `C:\Claude Projects\Gridiron Warrior\External Library\AI\_index.md` for a brief that already answers this exact question (same decision, same audience, not just the same nouns). If one exists, research today anyway (reuse is not enabled yet), name that brief in `## Already Decided` with its date, and make the new brief add to it rather than repeat it.

### 1c. Decide the outcome (D5 Task 4, 2026-09-10)

A run ends one of six ways. Pick one now, with the framed question from 1b in hand, before any NotebookLM call.

Run these checks first and remember exactly which ones you ran, because the receipt records them:

1. `C:\Claude Projects\Gridiron Warrior\External Library\AI\_index.md`, every brief title and date.
2. The `## Completed` section of this lane's `_topic-queue.md`.
3. `C:\Claude Projects\Gridiron Warrior\wiki\system\decisions.md`.
4. The topic's own wiki pages.

Compare the decision, the audience and the constraint, not the nouns. A shared topic word is not coverage. Open the candidate brief and read it before you call anything a duplicate. One failed lookup does not prove nothing is worth researching.

| Outcome | When | Today's output |
|---|---|---|
| NEW | No brief answers this question. This is the default. | A dated brief |
| UPDATE | A brief answers it for a different population, season or constraint, or its evidence is stale. | A dated brief that names the old one in `supersedes` and adds to it |
| REUSE | An existing brief already answers this exact decision for this exact audience. | A receipt, no brief |
| SCOTT ANSWER NEEDED | The missing source is Scott's own judgment or experience, not anything external. | A receipt carrying ONE specific question for him, no brief |
| NO NEW RESEARCH | After the four checks, no eligible question is worth a run. | A receipt naming the reason, no brief |
| BLOCKED / FAILED | A NotebookLM or source failure. Unchanged, see the HARD RULE in step 2. | A `status: blocked` stub and a red gate |

Hard rules on the choice:

- A technical failure is NEVER one of the three quiet outcomes. Blocked stays blocked. Do not use a quiet outcome to make a broken night look green.
- Scott's own request is always NEW or UPDATE. If the queue line names him (`per Scott`, `scott`, a pinned note) or `question_source` is `scott`, reuse and the quiet outcomes are off the board.
- An auto-picked topic (the queue was empty) is a NEW.
- REUSE must name the brief it reuses. SCOTT ANSWER NEEDED must carry one specific question and must never invent an answer in his voice.

**NEW and UPDATE:** continue with step 2 exactly as before. Add two keys to the brief frontmatter: `disposition: new` or `disposition: update`, and on an update `supersedes: <the older brief filename>`.

**REUSE, SCOTT ANSWER NEEDED, NO NEW RESEARCH:** skip step 2 and the brief entirely and run the no-brief close-out below.

#### No-brief close-out

Four steps, in order, then stop. Write no brief, add no `_index.md` line, and never move the line to `## Completed`. Completed means researched, and nothing here was researched.

**1. Write the receipt.** Never hand-write the JSON file; the CLI validates it.

```
python "C:\Claude Projects\Gridiron Warrior\scripts\research_receipt.py" write --lane ai --date YYYY-MM-DD --file <fields.json>
```

Quoting a JSON object on the PowerShell command line is fragile, so write the fields to a temp `.json` file and pass `--file`. The `--json '<fields>'` form works where the shell allows it.

Fields:

| Field | Required | Value |
|---|---|---|
| `queue_entry` | yes | The active queue line, verbatim, before your suffix |
| `topic_slug` | yes | The slug in the brackets |
| `question`, `decision`, `audience`, `question_source` | yes | The four lines from 1b |
| `disposition` | yes | `reuse`, `scott-answer-needed`, or `no-new-research` |
| `reason` | yes | One plain sentence saying why |
| `checks_performed` | yes | List of the checks you actually ran |
| `queue_action` | yes | `left-active` |
| `related_briefs` | REUSE | List with the reused brief filename |
| `scott_question` | SCOTT ANSWER NEEDED | One specific question for Scott |

The CLI exits non-zero and writes nothing if a field is missing, the disposition is unknown, a reuse names no brief, or a Scott question is absent. Fix the fields and run it again. It also never overwrites an earlier receipt for the same lane and date; a second run lands at `ai-2.json` and says so.

**2. Append the suffix to the queue line, in place.** Same byte pattern the blocked path already writes: one existing line gets a suffix, every other byte of the file stays as it is. Never rewrite another line.

- REUSE: ` *(reuse YYYY-MM-DD -> <existing-brief-filename>)*`
- SCOTT ANSWER NEEDED: ` *(awaiting Scott YYYY-MM-DD)*`
- NO NEW RESEARCH: ` *(no new research YYYY-MM-DD - <short reason>)*`

The line stays under `## Active Queue` with its `[topic-slug]` intact. That keeps `scripts/queue_status.py` counting it as active (honest: the work is not done), keeps it first in line tomorrow, and lets `/gw-weekly-synthesis` Step 3 find the slug so it does not requeue the topic. Encoding: the AI queue is UTF-16LE with a BOM and CRLF line endings, so read and write it with explicit encoding (a naive write has already truncated a sibling queue to 2 bytes).

**3. Append the wiki log line.**

```
YYYY-MM-DD /gw-ai-research: [topic-slug] (disposition: reuse|scott-answer-needed|no-new-research)
```

**4. Print one line, then exit 0.**

```
GW-RESEARCH: ai <disposition> - no brief today, receipt written
```

The `ai-research` gate has no log-marker validator, so this line is for Scott and the sched-log, not for the gate. The gate reads the receipt: `job-contracts.json` now validates this lane with `receipt_or_brief`, which passes on a dated non-blocked brief OR a receipt whose disposition is one of the three above. No brief and no receipt still fails. A receipt carrying `blocked` or `failed` still fails.

**5. Do NOT commit.** Same rule as a normal run.

### 2. Run NotebookLM research

Use the `mcp__notebooklm__*` MCP server. Same explicit flow as `/gw-business-research`, with AI-relevant sources (Anthropic docs, AI Twitter, dev YouTube, Claude release notes):

1. `notebook_create` with title "AI Research: [topic name] — [date]" → capture the returned `notebook_id`
2. Use yt-dlp or web search to find 4-6 high-signal sources on the topic
3. Add sources via `source_add`
4. Query with `notebook_query` (notebook_id from step 1) using the structured prompt below. Lead the prompt with the framed `question` and `decision` from step 1b; every field answers that question, not the topic in general.

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

**DECISIONS GATE (HARD RULE — identical across gw-sc/ai/business-research).** Before you write a single recommendation, read two things:

1. `C:\Claude Projects\Gridiron Warrior\wiki\system\decisions.md`, in full. Every `KILLED`, `DECLINED`, `DE-SCOPED`, `RETIRED`, `REJECTED`, and `RULE` heading is off the board.
2. The topic's own wiki pages. Grep `wiki\index.md` for the topic's keywords to find them, then read only those pages — index.md is 337KB, never read it whole. Where a page marks a number or a prescription as the GW standard (a dated "Scott's ruling", "per Scott", or "Scott's call" note), that ruling outranks anything a source told you. The source's number keeps its attribution to its author; it never becomes the recommendation.

For AI topics the live constraints matter as much as the kills: `wiki/business/tech-stack.md` is the record of what Scott actually runs, and the model policy in the root `CLAUDE.md` (Opus and Sonnet execute, Fable plans) is not negotiable by a source that likes a different model. Do not recommend a tool as new when the stack page already lists it.

Nothing that collides gets recommended. Write one line in `## Already Decided` instead, naming the entry, its date, and its reopen condition, then move on. A brief that says "declined 2026-08-07, reopen if Scott raises it" is worth more than one that re-pitches it.

Judgment, not keyword match. A shared noun is not a collision: `decisions.md` kills the member-facing answer bot, not every mention of a bot. Confirm the recommendation IS the dead thing before cutting it. If it genuinely differs, keep it and say in one clause how it differs.

Why this gate exists: in the week ending 2026-08-17 two briefs re-pitched settled calls — the $37 Second Brain order bump (declined 2026-08-07) and the Balis 75-79 percent in-season lower-body cap (overruled to 85-88 on 2026-08-10). Both were caught by hand during the Sunday weave. The pipeline catches them now, not Scott.

Save to `C:\Claude Projects\Gridiron Warrior\External Library\AI\YYYY-MM-DD-[topic-slug]-brief.md`:

The `: AI Research Brief` title suffix is a parsed contract: `/gw-weekly-synthesis` Step 3 strips it to recover the topic name. Keep the colon delimiter exactly. The em-dash form was retired 2026-07-27 (voice rule); it survives only in legacy briefs, which synthesis still accepts.

Density: cover only findings that materially affect how Scott would act on this topic. Keep each numbered item to one or two sentences, stay inside the counts the template gives, and expand an item only when a distinct source changes the recommendation. Every template section still gets real content.

```markdown
---
title: "[Topic Name]: AI Research Brief"
tags: [ai, research, daily-brief, [topic-slug]]
date: YYYY-MM-DD
notebook_id: <notebook-id>
topic: [topic-slug]
question: "<the framed question, one sentence>"
decision: <one clause>
audience: <who is asking and their constraint>
question_source: queue|ds-<slug>|scott
disposition: new|update
supersedes: <older brief filename, UPDATE only, omit the key on NEW>
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

## Already Decided
- <thing the sources recommended> — <KILLED|DECLINED|DE-SCOPED|RETIRED|REJECTED|RULED> YYYY-MM-DD: <the call in one clause>. Reopen if: <condition>.

## Sources
- ...
```

`## Already Decided` is the only conditional section in the template. Include it only when the decisions gate actually fired; omit the heading entirely when nothing collided.

### 4. Update queue + index

In `_topic-queue.md`:
- Remove the topic from `## Active Queue`
- Add to `## Completed` as `- YYYY-MM-DD - topic name [topic-slug]`

Note this is NOT byte-identical to the business queue line: the AI queue uses a dash after the date and carries no wikilink, while business uses a colon and links the brief. Match the format already in the file you are editing. What both share is the mandatory trailing `[topic-slug]`, which is what `/gw-weekly-synthesis` Step 3 greps for to avoid re-queueing a researched topic.

**Encoding warning:** the AI queue is UTF-16LE with a BOM and **CRLF** line endings (the old "LF-only" note here was wrong; frozen and corrected by the D5 audit, 2026-09-10). Read and write with explicit encoding. A naive write has already truncated a sibling queue to 2 bytes.

In `_index.md`:
- Add link under `## Daily Research Briefs`: `- YYYY-MM-DD: [[YYYY-MM-DD-topic-slug-brief|topic name]]`

### 5. Append to wiki log

```
2026-MM-DD /gw-ai-research: [topic-slug] (auto_picked: false|true)
```

Do NOT run `git commit`. The `gw-daily-closeout` job commits all approved daily-output paths once, after the morning digest, via `scripts/git_safe_commit.py`. This skill's job ends at writing the brief and the wiki/log.md line.
