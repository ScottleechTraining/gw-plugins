---
name: gw-seed-writer
description: "Daily content seed - yesterday's vault deltas -> 1-3 content angles in Scott's voice"
---

# /gw-seed-writer — Daily Content Seed

Fires daily. Reads everything new in the vault from the last 24h. Writes 1-3 specific content angles in Scott Leech's voice. Output is the daily idea fuel for Scott's content production.

## Steps

### 1. Identify what's new in last 24h

Use git log to find files changed in the last 24 hours:

```bash
cd "D:\Claude Projects\Gridiron Warrior" && git log --since="24 hours ago" --name-only --pretty=format: | sort -u
```

Plus any files modified but not committed (git status). Filter to relevant additions:
- `External Library\Twitter-Instagram Saves\` (new Dewey notes)
- `External Library\Screenshots\processed\` (new screenshots)
- `External Library\BusinessDocuments\YYYY-MM-DD-*-brief.md` (new business research)
- `External Library\AI\YYYY-MM-DD-*-brief.md` (new AI research)
- `Voice Corpus\Voice Notes\YYYY-MM-DD-*.md` (Scott's voice notes — HIGH PRIORITY)
- `Research\NotebookLM\*-research-brief.md` (S&C research briefs)

### 2. Read CLAUDE.md voice rules first

Read `D:\Claude Projects\CLAUDE.md` — internalize:
- Voice rules: short sentences, active verbs, plain language
- No em-dashes ever
- Banned words list
- Signature phrases
- Sign-off: "Keep the Fire Burning, / Leech"

### 3. Synthesize 1-3 angles

**Read budget (HARD CAPS — do not exceed):**

- **Max 10 individual Read tool calls total for this entire step.** This is a synthesis task, not an archival pass.
- **Do NOT Glob or Grep the whole vault.** Use the git log output from Step 1 as the sole source of "what's new."
- **Voice notes: read all** (HIGH PRIORITY — Scott's own words, usually 1-3 files max).
- **Research briefs (business + AI): read both fully** if they exist (1-2 files max).
- **Dewey notes: do NOT read individually.** The new-Dewey-row summary is already in `wiki/log.md` from `/gw-dewey-daily`'s log entry — read THAT line to get domain counts, top authors, and one-line takeaways. Only open an individual Dewey note if a specific row is mentioned by name and you genuinely need the body.
- **Screenshots: do NOT read processed notes individually.** Count from the git log file list. If a specific screenshot looks critical for an angle (rare), open one.
- **CLAUDE.md: already in your project context — do NOT re-Read it.** Just internalize the voice rules from your existing context.

If your read count hits 10 mid-pass, STOP reading and synthesize with what you have. The output quality plateaus after the top ~5 sources anyway.

Look for:
- **Cross-domain mashups** (Dewey save + business framework + GW concept = a thread)
- **Scott's own voice notes amplified** (a Pocket voice note becomes the seed for an email)
- **Counter-intuitive takes** (research finding + Scott's typical viewpoint = a "myth-bust" angle)
- **Timely tie-ins** (Summit is approaching, August is coming, recent podcast episode)

For each angle, output:

```markdown
### Angle [N]: [one-line hook]

**Format**: Twitter thread | IG carousel | Email | Reel
**Source material**: <wikilink to new vault item(s)>
**Hook (first line in Scott's voice)**:
> ...

**Body sketch** (3-5 bullet points of the teaching points, in Scott's voice):
- ...
- ...

**CTA**: <which product to point to — Insiders / GW 2.0 / Contact Prep / Scores and Stops / Summit / GW Schools / Summer in a Day>

**Scores** (1=low, 5=high):
- Revenue tie-in: N — <1-line justification linking to a specific offer>
- Voice fit: N — <how naturally this lands in Scott's voice>
- Urgency: N — <why today/this week vs evergreen>
- Ease of production: N — <draft-to-publish friction>
- **Total: N/20**

**Next command** (pick exactly one):
- `/gw-content-forge "<this angle's hook>"` — when the angle is ready to expand into a full content pack (3 threads, 2 carousels, 3 reel ideas, 1 email)
- `/gw-film-study-brief "<topic>"` — when the angle is really a Film Study research question, not a publish-ready angle
- **Manual: leech-letter-editor skill** — when the angle is Saturday Leech Letter material (Scott writes these himself; do not auto-route)
- **Manual: gw-substack-forge skill** — when the angle deserves a long-form Substack article
- **Manual: ig-carousel skill** — when the angle is single-purpose carousel content
- **Manual: Kit broadcast draft** — when the angle is a one-off promo email (kit-guardrails: draft only, never auto-send)

**Confidence**: high | medium | low
```

### 3a. Pick today's TOP MOVE

After all angles are scored, pick the single angle with the highest **Total** score and mark it `**TOP MOVE**` at the top of the angles section. Ties: break in favor of higher Revenue, then higher Urgency, then highest Ease.

### 4. Write the seed file

Save to `D:\Claude Projects\Gridiron Warrior\Deliverables\_daily-seeds\YYYY-MM-DD.md`:

```markdown
---
title: Daily Content Seed — YYYY-MM-DD
tags: [daily-seed, content-pipeline]
date: YYYY-MM-DD
sources_scanned: <N>
angles_generated: <1-3>
top_move_angle: <angle number, 1-3>
top_move_score: <N/20>
pipeline: gw-seed-writer
---

# Daily Content Seed — YYYY-MM-DD

## TOP MOVE

**Angle [N]: [the winner's hook]** (score: N/20)

Run: `<the winner's next_command from Step 3>`

## What landed in the vault yesterday (24h delta)

<bullet list of new files with one-line summary each>

## Today's content angles

<the 1-3 angles, scored per Step 3 — the TOP MOVE angle gets a `**TOP MOVE**` label inline>

## Queue health

- Business queue: <N topics remaining>
- AI queue: <N topics remaining>
- (warn here if either is below 5)

## Next move

The TOP MOVE above is today's recommendation. Other angles are backup if the top one doesn't land or Scott vetoes.
```

### 5. Append to wiki log

```
2026-MM-DD /gw-seed-writer: N angles generated from M sources
```

Do NOT run `git commit`. The `gw-daily-closeout` job commits all approved daily-output paths once, after the morning digest, via `scripts/git_safe_commit.py`. This skill's job ends at writing the seed file and the wiki/log.md line.

## Voice gut-check before writing

Every angle's hook and body MUST pass this check:
- No em-dashes
- No banned words (fluff, delve, leverage as verb, unlock, etc.)
- Sounds like a coach in the trenches, not a marketer
- Could plausibly be the first line of a Leech Letter

If an angle doesn't pass, kill it and try another. Better to produce 1 strong angle than 3 weak ones.

## Voice check (runtime enforcement)

After writing the seed file, run the voice-check guard against the output:

```bash
python "D:\Claude Projects\Gridiron Warrior\scripts\voice_check.py" "D:\Claude Projects\Gridiron Warrior\Deliverables\_daily-seeds\YYYY-MM-DD.md"
```

Exit codes:
- `0` clean — proceed to commit.
- `1` warnings (em-dashes, possible offer-stack drift) — review and decide whether to fix or accept.
- `2` blockers (banned words present) — fix the seed file before committing. Then re-run the check.

The guard parses the canonical banned-words list from CLAUDE.md, so it stays in sync if Scott updates the list. The check is mandatory before the commit step.

---

## After writing the daily seed — append forge ideas to backlog

For each angle in today's seed that has a `/gw-content-forge "..."` recommendation, append a new entry to `queue-state.json`'s `forge_backlog` array. Skip duplicates (same slug already present).

```bash
python -c "
import json, pathlib, re
new_entries = [
    # FILL THIS IN per today's angles. Example:
    # {'title': '...', 'format': 'Twitter thread', 'score': '19/20'},
]
p = pathlib.Path('D:/Claude Projects/Gridiron Warrior/Deliverables/queue-state.json')
data = json.loads(p.read_text(encoding='utf-8'))
backlog = data.setdefault('forge_backlog', [])
existing_slugs = {e['slug'] for e in backlog}

def slugify(title):
    head = title.split(',')[0].strip().lower()
    s = re.sub(r'[^a-z0-9]+', '-', head)
    return re.sub(r'-+', '-', s).strip('-')[:80]

from datetime import date
today = date.today().isoformat()
seed_file = f'_daily-seeds/{today}.md'
added = 0
for entry in new_entries:
    slug = slugify(entry['title'])
    if slug in existing_slugs:
        continue
    backlog.append({
        'slug': slug,
        'title': entry['title'],
        'format': entry.get('format'),
        'score': entry.get('score'),
        'source': seed_file,
        'added': today,
        'status': 'pending',
    })
    added += 1
p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'Added {added} new backlog entries')
"
```
