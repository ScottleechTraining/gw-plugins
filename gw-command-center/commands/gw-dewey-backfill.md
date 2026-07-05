---
name: gw-dewey-backfill
model: sonnet
description: "One-time Dewey 2nd pass - re-classify backlog for Business + AI content"
---

# /gw-dewey-backfill — Dewey Second Pass (One-Time)

The first Dewey pass had an S&C lens and skipped a lot of Business + AI content. This one-time backfill re-runs the full Dewey sheet (2,677 rows) hunting specifically for Business + AI content that was filtered out.

## Steps

### 1. Identify candidates to re-classify

Pull all rows from Dewey sheet where:
- `Processed = TRUE` (we already saw them once)
- AND no corresponding note exists in `External Library\Twitter-Instagram Saves\` OR existing note's frontmatter has no `domain:` field

Save to a scratch file: `External Library\Twitter-Instagram Saves\_backfill-candidates.csv`.

### 2. Batch processing

Process in batches of 50 rows. For each row:

1. Read post URL + caption + author + media URL from Dewey sheet
2. Apply NEW classifier with **Business + AI bias**:
   - `business`: marketing, sales pages, email funnels, sponsorships, pricing, copywriting, branding, course launches, lead gen, social growth tactics, info-product business
   - `ai`: AI tools, prompts, Claude / GPT / Gemini, automation, agent design, MCP, no-code, AI-assisted content, computer use, RAG, prompt engineering
   - `s-and-c-already-captured`: skip (we got it on first pass)
   - `skip`: still off-topic
3. For `business` or `ai` classifications:
   - OCR media if needed (Tier 1 Dewey CDN)
   - Write note following standard `gw-dewey-ingest` schema with `domain: business` or `domain: ai`
4. After each batch of 50, append progress to `wiki\log.md` and commit

### 3. Resume support

Write cursor file `External Library\Twitter-Instagram Saves\.backfill-cursor.txt` with last-processed row. Re-running picks up where it left off.

### 4. Final report

After full run, write `External Library\Twitter-Instagram Saves\_backfill-report-YYYY-MM-DD.md`:

```markdown
---
title: Dewey Backfill Report
date: YYYY-MM-DD
total_rows_examined: <N>
business_notes_created: <N>
ai_notes_created: <N>
still_skipped: <N>
---

# Dewey Second-Pass Backfill Report

<summary stats, top 10 most-saved authors per domain, etc.>
```

### 5. Commit

```bash
cd "D:\Claude Projects\Gridiron Warrior" && git add -A && git commit -m "dewey: backfill complete — N business, M ai notes added"
```

## Cost guardrails

- Estimate: 2,677 rows × ~$0.005/row (OCR + classify) = ~$13.50 max
- If hitting unexpected costs (NotebookLM credits, API calls), pause and report
- This is a ONE-TIME job. Do not re-run unless backlog grows significantly.

## Tonight's plan

Run a 50-row sample. Write a validation report to `External Library\Twitter-Instagram Saves\_backfill-sample-report.md`. Leave the full 2,677-row run for Scott to kick off in the morning after reviewing the sample.
