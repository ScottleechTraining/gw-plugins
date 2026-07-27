---
name: gw-triage
model: claude-opus-5
description: "Walk the Deliverables inbox and decide Ready/Cold/Kill per topic. Terminal mirror of the dashboard's Inbox view. Decisions are batched and reviewed before any folder moves happen."
---

# GW Triage — Walk inbox, decide Ready/Cold/Kill per topic

Sit down with the inbox and triage each topic. Terminal mirror of the
dashboard's Inbox view. Decisions are batched and reviewed before any
folder moves happen.

## Paths

- **Inbox:** `C:/Claude Projects/Gridiron Warrior/Deliverables/_inbox/`
- **Ready:** `C:/Claude Projects/Gridiron Warrior/Deliverables/ready/`
- **Cold:** `C:/Claude Projects/Gridiron Warrior/Deliverables/cold-storage/`

## Promotion rubric (score each topic before you preview it)

Scott makes the final R/C/K/S call, but every preview must carry a suggested verdict so he can decide in seconds. Score each topic on four axes, then apply the verdict rule below. Read what is already in `ready/` and `archived/` first so novelty and duplication are judged against real inventory, not memory.

1. **Hook strength for the ICP**: does the first line stop a time-strapped HS football or S&C coach mid-scroll? Names a specific mistake, decision, or fear (letting athletes down, kids getting dominated), not a vague theme. Weak/generic hook is the most common reason a pack is not Ready.
2. **Teaching novelty**: does it teach something not already sitting in `ready/` or `archived/`? A near-duplicate of a shipped or queued topic is Cold at best, never Ready. Same angle already published = Cold. Genuinely new teaching = Ready-eligible.
3. **Seasonal timing**: is it on-calendar right now (August is coming, camp prep, in-season CNS, offseason build)? On-window and strong pushes toward Ready. On-window is a tie-breaker up, not a rescue for a weak hook. Off-season-but-evergreen is fine; off-season-and-dated leans Cold.
4. **Offer alignment**: does it feed a live offer: Insiders ($29/mo, primary MRR), the Schools funnel (Summer/Inseason in a Day → GW Schools), Summit (July 18), or a course (GW2.0 / Contact Prep / Scores and Stops / Second Brain)? A pack with a clear CTA into an offer beats one that teaches into a dead end.

**Verdict rule (suggested, Scott confirms):**
- **Ready**: strong hook AND novel teaching AND (on-window OR clean offer alignment). The pack earns a spot in the publish queue as-is.
- **Ready+ (needs carousel polish)**: meets the Ready bar on substance but the carousel asset is rough. Route R+ so the queue flags it, do not demote good teaching over a fixable asset.
- **Cold-storage**: solid teaching but off-window, a soft hook, thin offer tie-in, or too close to something already shipped. Not dead, just not now. Revisit when the season or the queue shifts.
- **Kill**: only for genuine junk: broken/empty pack, off-brand, off-voice, or a topic Scott has explicitly killed before. Kill is destructive and rare.

**Tie-breaks:** Ready vs Cold, and the hook is anything short of strong → Cold. Cold vs Kill → Cold. On-window but duplicative → Cold (timing does not beat novelty). Two Ready-eligible packs competing for attention → the one with the tighter offer CTA wins.

**Default when uncertain: Cold-storage. Never Kill on doubt.** Cold is reversible with one move back to `_inbox/`. Kill is a `git rm`. When you cannot decide, the answer is Cold.

## Step 1: Check the inbox

```bash
cd "C:/Claude Projects/Gridiron Warrior/Deliverables/_inbox"
ls -1 | grep -v "^\." | grep -v "^_"
```

If empty, print: "Inbox is empty. Nothing to triage." and stop.

## Step 2: For each topic in the inbox, build a preview

For each subfolder in `_inbox/`:
- Folder name (slug)
- First 5 lines of `*-content-pack.md` if present
- Whether `*-carousel.html` exists
- Whether `*-substack-article.md` exists
- Whether `*-research-brief.md` exists
- Date the folder was created (use `git log --format=%ad --date=short -- <folder>` first, fall back to file mtime)

Format the preview compactly:
```
[1/5] sample-topic-slug
  Created: 2026-06-01
  Assets: ✅ content-pack ✅ carousel ⬜ substack ⬜ research-brief
  Preview:
    > # Content Pack: Sample Topic
    > Voice: Scott Leech. Short sentences.
    > ## Twitter Thread 1
    > Hook line goes here.
```

## Step 3: Ask Scott to decide for each topic

For each topic in order, ask:

```
Decision for [N/total] <slug>?
  R     = Ready (move to ready/)
  R+    = Ready + carousel needs polish (move to ready/, flag in queue-state.json)
  C     = Cold (move to cold-storage/)
  K     = Kill (delete the folder)
  S     = Skip for now (leave in _inbox/)
```

Wait for an answer. Accept single letters (R/C/K/S) or R+ for ready-with-polish.

Collect all decisions into a list before executing anything:
```python
decisions = [
    ("sample-topic-slug", "R"),
    ("other-topic", "C"),
    ...
]
```

## Step 4: Show the planned moves before destruction

```
Planned moves:
  R   sample-topic-slug          → ready/
  R+  another-topic               → ready/ (carousel_needs_polish=true)
  C   stale-topic                → cold-storage/
  K   dead-on-arrival            → DELETED
  S   not-sure-yet               → stays in _inbox/

Proceed? (yes/no)
```

If no: print "Aborted. Nothing changed." and stop.

## Step 5: Execute the moves

```bash
cd "C:/Claude Projects/Gridiron Warrior/Deliverables"

# For each R or R+ decision:
git mv "_inbox/<slug>" "ready/<slug>"

# For each C decision:
git mv "_inbox/<slug>" "cold-storage/<slug>"

# For each K decision (CONFIRM AGAIN before running):
git rm -r "_inbox/<slug>"
```

For R+ decisions, also update `queue-state.json` to set `carousel_needs_polish: true` on those topics. Easiest way: do this AFTER running `/gw-queue` (Step 7) by directly patching the JSON:

```python
import json, pathlib
p = pathlib.Path("C:/Claude Projects/Gridiron Warrior/Deliverables/queue-state.json")
data = json.loads(p.read_text(encoding="utf-8"))
polish_slugs = ["slug-a", "slug-b"]
for t in data["topics"]:
    if t["slug"] in polish_slugs:
        t["carousel_needs_polish"] = True
p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
```

## Step 6: Refresh state

Invoke `/gw-queue` (or directly run `python -m scripts.gwqueue.scan_folders`) to pick up the new layout.

## Step 7: Commit

```bash
cd "C:/Claude Projects"
git add -A
git commit -m "triage: sort <N> topics from inbox"
```

Where `<N>` is the count of non-Skip decisions.

## Step 8: Print summary

```
Triaged <total> topics from inbox:
  → ready/:        <r_count> (incl. <polish_count> flagged for carousel polish)
  → cold-storage/: <c_count>
  → deleted:       <k_count>
  ↻ left in inbox: <s_count>

Run /gw-queue to see updated dashboard state.
```

## Voice

Direct. Short. No fluff. The triage decisions themselves are mechanical, but the previews should give Scott enough to decide quickly without opening files.
