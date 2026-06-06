# GW Mark — One-shot channel state update

Update a topic's channel state from the terminal. Useful when you've
just posted something and want to record it without opening the dashboard.

## Usage: $ARGUMENTS

Format: `<topic-slug> <channel> <state> [date]`

Examples:
- `/gw-mark tri-set ig_carousel posted` (date defaults to today)
- `/gw-mark rfd-strength-alone-not-enough twitter_thread drafted`
- `/gw-mark jumps-by-force-vector substack skip`
- `/gw-mark gassers ig_carousel posted 2026-07-15` (explicit date)

## Valid channels

Standard: `ig_carousel`, `twitter_thread`, `ig_single`, `email`, `insiders`, `substack`
Optional: `twitter_single`, `reel`

## Valid states

`ready` | `drafted` | `posted` | `skip` | `n/a`

## Paths

- **State file:** `D:/Claude Projects/Gridiron Warrior/Deliverables/queue-state.json`
- **Dashboard copy:** `D:/Claude Projects/websites/scottleechtraining.com/tools/queue/queue-state.json` (sync if folder exists)

## Step 1: Parse $ARGUMENTS

Split on whitespace. Expect 3 or 4 tokens.

If fewer than 3 tokens or `--help`, print usage and stop:
```
Usage: /gw-mark <topic-slug> <channel> <state> [date]

Channels: ig_carousel | twitter_thread | ig_single | email | insiders | substack | twitter_single | reel
States:   ready | drafted | posted | skip | n/a

Example: /gw-mark tri-set ig_carousel posted
```

## Step 2: Validate channel and state

Reject and stop if `channel` is not in the valid list.
Reject and stop if `state` is not in the valid list.

## Step 3: Find the topic

Read `queue-state.json`. Find topics whose `slug` contains the input substring (case-insensitive).

- Zero matches: print "No topic matches '<slug>'. Run /gw-queue to refresh." and stop.
- Multiple matches: list them with last_activity and ask the user to disambiguate. Do NOT proceed until disambiguated.
- One match: continue.

## Step 4: Update the channel

Use this Python to do the actual write (run via `python -c` from the command):

```python
import json, sys, pathlib
from datetime import date

slug_input = "REPLACE_ME"          # the matched topic's actual slug
channel = "REPLACE_ME"
state = "REPLACE_ME"
explicit_date = None               # or "YYYY-MM-DD" if provided

p = pathlib.Path("D:/Claude Projects/Gridiron Warrior/Deliverables/queue-state.json")
data = json.loads(p.read_text(encoding="utf-8"))
topic = next(t for t in data["topics"] if t["slug"] == slug_input)

entry = {"state": state}
if state == "posted":
    entry["date"] = explicit_date or date.today().isoformat()

topic["channels"][channel] = entry
topic["last_activity"] = date.today().isoformat()

p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

# Also write to dashboard copy if it exists
dash = pathlib.Path("D:/Claude Projects/websites/scottleechtraining.com/tools/queue/queue-state.json")
if dash.parent.exists():
    dash.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

# Count squeeze
settled = sum(1 for c in topic["channels"].values() if c.get("state") in ("posted", "skip"))
total = len(topic["channels"])
print(f"Marked {slug_input} {channel} = {state}" + (f" ({entry['date']})" if "date" in entry else ""))
print(f"Status: {settled}/{total} channels settled")
```

When constructing the actual command to run, replace the REPLACE_ME placeholders with the parsed/validated values.

## Step 5: Squeeze check

If all channels are now `posted` or `skip`, ask the user:
```
All channels settled for <slug>. Move to archived/? (yes/no)
```

If yes: print the bash commands needed to `git mv` the topic folder from `ready/` (or wherever it currently lives) to `archived/`. Run them on confirmation. Then re-run `/gw-queue` to refresh state.

If no: leave it in place. The user can run `/gw-mark <slug> __retire__` later or use the dashboard.

## Step 6: Confirm

Print the final status line:
```
Marked <slug> <channel> = <state> (<date if posted>)
Status: <settled>/<total> channels settled
```

Optional: if 0 channels settled before this call (fresh topic), say "Nice. First channel out the door."

## Voice

Brief, direct. No em-dashes. No fluff. The output is mechanical confirmation.
