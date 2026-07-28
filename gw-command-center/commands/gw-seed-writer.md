---
name: gw-seed-writer
model: claude-opus-5
description: "Daily content seed - yesterday's vault deltas -> 1-3 content angles in Scott's voice"
---

# /gw-seed-writer: Daily Content Seed

Fires daily. Reads everything new in the vault from the last 24h. Writes 1-3 specific content angles in Scott Leech's voice. Output is the daily idea fuel for Scott's content production.

## HARD RULE: zero em-dashes in the seed file

The seed file must contain **zero** em-dash characters (U+2014). Not in the frontmatter, not in the title, not in the delta bullets, not in the score justifications. This is the root CLAUDE.md voice rule and it is absolute.

The templates further down this file are written em-dash free on purpose. **Copy their punctuation exactly.** The 2026-07-26 regression happened because a run reproduced an older template that still carried em-dashes, which put 13 of them into the seed while the six prior days had zero. If you are ever unsure what punctuation to use, the house style is:

- Title and heading: `Daily Content Seed, YYYY-MM-DD` (comma, never a dash)
- Delta bullet: `` `path/to/file.md`: one-line summary `` (colon)
- Score line: `- Revenue tie-in: 4, the justification` (comma)

Use periods, commas, or colons. Never an em-dash. An en-dash (U+2013) is not a workaround either.

## Steps

### 1. Identify what's new in last 24h

Use git log to find files changed in the last 24 hours:

```bash
cd "C:\Claude Projects\Gridiron Warrior" && git log --since="24 hours ago" --name-only --pretty=format: | sort -u
```

Plus any files modified but not committed (git status). Filter to relevant additions:
- `External Library\Twitter-Instagram Saves\` (new Dewey notes)
- `External Library\Screenshots\processed\` (new screenshots)
- `External Library\BusinessDocuments\YYYY-MM-DD-*-brief.md` (new business research)
- `External Library\AI\YYYY-MM-DD-*-brief.md` (new AI research)
- `Voice Corpus\Voice Notes\YYYY-MM-DD-*.md` (Scott's voice notes, HIGH PRIORITY)
- `Research\NotebookLM\*-research-brief.md` (S&C research briefs)

### 2. Read CLAUDE.md voice rules first

Read `C:\Claude Projects\CLAUDE.md` and internalize:
- Voice rules: short sentences, active verbs, plain language
- No em-dashes ever
- Banned words list
- Signature phrases
- Sign-off: "Keep the Fire Burning, / Leech"

### 3. Synthesize 1-3 angles

**Angle-quality gate (every angle must clear all four before it gets scored, this is pass/fail, not a tally):**

1. **Names a specific mistake or decision.** The angle points at one concrete coaching error or fork-in-the-road choice ("you're squatting Thursday and killing Friday", "you count reps instead of load"), NOT a vague theme ("conditioning matters", "toughness"). If you can't state the mistake in one sentence, the angle isn't ready.
2. **Passes the ICP filter.** Would a time-strapped HS football or S&C coach stop scrolling? It has to hit a real pain (kids getting dominated, no time to program, letting athletes down), not just be interesting to you.
3. **Teachable in one pack.** It fits a thread, a carousel, or one email. If it needs a course outline or three sessions to land, it's too big, split it or send it to `/gw-film-study-brief` instead of forcing it into a seed.
4. **Not a duplicate.** Before writing, check `queue-state.json`'s `forge_backlog` and the last few days in `_daily-seeds/` for the same angle. If it's already queued or was seeded this week, skip it. A fresh spin on a shipped topic is fine; a re-run of a pending one is noise.

An angle that fails any gate gets cut, not scored. Only survivors go through the scoring block below.

**When the day's deltas are thin:** fewer good angles beats padded weak ones. One angle that clears the gate is a better output than three that limp through. **Zero angles is an acceptable output**: when nothing in the 24h delta clears the gate, write the seed file with zero angles and a one-line reason (e.g. "only new material was 2 competitor Dewey saves, no Scott-original hook"). Do not manufacture an angle to hit a count.

**Read budget (HARD CAPS, do not exceed):**

- **Max 10 individual Read tool calls total for this entire step.** This is a synthesis task, not an archival pass.
- **Do NOT Glob or Grep the whole vault.** Use the git log output from Step 1 as the sole source of "what's new."
- **Voice notes: read all** (HIGH PRIORITY. Scott's own words, usually 1-3 files max).
- **Research briefs (business + AI): read both fully** if they exist (1-2 files max).
- **Dewey notes: do NOT read individually.** The new-Dewey-row summary is already in `wiki/log.md` from `/gw-dewey-daily`'s log entry. Read THAT line to get domain counts, top authors, and one-line takeaways. Only open an individual Dewey note if a specific row is mentioned by name and you genuinely need the body.
- **Screenshots: do NOT read processed notes individually.** Count from the git log file list. If a specific screenshot looks critical for an angle (rare), open one.
- **CLAUDE.md: already in your project context, do NOT re-Read it.** Just internalize the voice rules from your existing context.

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

**CTA**: <which product to point to: Insiders / GW 2.0 / Contact Prep / Scores and Stops / Summit / GW Schools / Summer in a Day>

**Scores** (1=low, 5=high):
- Revenue tie-in: N, <1-line justification linking to a specific offer>
- Voice fit: N, <how naturally this lands in Scott's voice>
- Urgency: N, <why today/this week vs evergreen>
- Ease of production: N, <draft-to-publish friction>
- **Total: N/20**

**Next command** (pick exactly one):
- `/gw-content-forge "<this angle's hook>"`: when the angle is ready to expand into a full content pack (3 threads, 2 carousels, 3 reel ideas, 1 email)
- `/gw-film-study-brief "<topic>"`: when the angle is really a Film Study research question, not a publish-ready angle
- **Manual: leech-letter-editor skill**: when the angle is Saturday Leech Letter material (Scott writes these himself; do not auto-route)
- **Manual: gw-substack-forge skill**: when the angle deserves a long-form Substack article
- **Manual: ig-carousel skill**: when the angle is single-purpose carousel content
- **Manual: Kit broadcast draft**: when the angle is a one-off promo email (kit-guardrails: draft only, never auto-send)

**Confidence**: high | medium | low
```

### 3a. Pick today's TOP MOVE

After all angles are scored, pick the single angle with the highest **Total** score and mark it `**TOP MOVE**` at the top of the angles section. Ties: break in favor of higher Revenue, then higher Urgency, then highest Ease.

### 4. Final em-dash self-check, THEN write the seed file

**Do this before the file is saved, not after.** Read back the full draft you are about to write and scan it character by character for em-dashes (U+2014) and en-dashes (U+2013). Check every one of these, because they are where the regression landed:

1. The `title:` frontmatter line
2. The `# Daily Content Seed` H1
3. Every bullet in "What landed in the vault yesterday"
4. Every one of the four score lines in every angle
5. Every hook and every body-sketch bullet

If you find even one, rewrite that sentence with a period, comma, or colon and scan again. Repeat until the count is zero. Only then write the file.

State the result explicitly in your output before saving, so the check is visible and cannot be silently skipped:

```
Em-dash self-check: 0 found in draft. Writing file.
```

If the count is not zero, you have not finished. Do not save a draft with a known em-dash in it and plan to clean it up afterwards.

Then save to `C:\Claude Projects\Gridiron Warrior\Deliverables\_daily-seeds\YYYY-MM-DD.md`:

```markdown
---
title: Daily Content Seed, YYYY-MM-DD
tags: [daily-seed, content-pipeline]
date: YYYY-MM-DD
sources_scanned: <N>
angles_generated: <1-3>
top_move_angle: <angle number, 1-3>
top_move_score: <N/20>
pipeline: gw-seed-writer
---

# Daily Content Seed, YYYY-MM-DD

## TOP MOVE

**Angle [N]: [the winner's hook]** (score: N/20)

Run: `<the winner's next_command from Step 3>`

## What landed in the vault yesterday (24h delta)

<bullet list of new files with one-line summary each>

## Today's content angles

<the 1-3 angles, scored per Step 3. The TOP MOVE angle gets a `**TOP MOVE**` label inline>

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

After writing the seed file, run the voice-check guard against the output. **`--strict` is mandatory here**: without it the guard scores em-dashes as a warning you are allowed to accept, which is exactly how 13 of them shipped on 2026-07-26. With it, an em-dash is a hard blocker.

```bash
python "C:\Claude Projects\Gridiron Warrior\scripts\voice_check.py" "C:\Claude Projects\Gridiron Warrior\Deliverables\_daily-seeds\YYYY-MM-DD.md" --strict
```

Exit codes:
- `0` clean, proceed to commit.
- `1` warnings (possible offer-stack drift), review and decide whether to fix or accept.
- `2` blockers (banned words OR em-dashes, because `--strict` is on), fix the seed file before committing. Then re-run the check.

The guard parses the canonical banned-words list from CLAUDE.md, so it stays in sync if Scott updates the list. The check is mandatory before the commit step.

---

## After writing the daily seed: append forge ideas to backlog

For each angle in today's seed that has a `/gw-content-forge "..."` recommendation, append a new entry to `queue-state.json`'s `forge_backlog` array. Skip duplicates (same slug already present).

```bash
python -c "
import json, pathlib, re
new_entries = [
    # FILL THIS IN per today's angles. Example:
    # {'title': '...', 'format': 'Twitter thread', 'score': '19/20'},
]
p = pathlib.Path('C:/Claude Projects/Gridiron Warrior/Deliverables/queue-state.json')
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
