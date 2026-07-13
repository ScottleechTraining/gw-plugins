---
name: gw-ideas-apply
model: sonnet
description: "Apply a pasted gw-ideas-result string from ideas.html to the forge backlog. forge queues /gw-content-forge on the slug now, top bumps its score so the nightly picker takes it first, skip retires it with a recorded skip_reason. Mechanical parse and apply, no judgment."
---

# GW Ideas Apply - Apply pasted ideas-queue decisions

Scott reviews the forge backlog in `ideas.html`, picks FORGE NOW / TOP / SKIP
per idea, and copies a `gw-ideas-result:` string. This command parses that
string and mutates `queue-state.json`'s `forge_backlog`. Page:
`scripts.gwqueue.build_ideas_page` (that is the contract this mirrors).

## Paths

- **Deliverables:** `C:/Claude Projects/Gridiron Warrior/Deliverables/`
- **State file:** `C:/Claude Projects/Gridiron Warrior/Deliverables/queue-state.json`
- **Ideas page:** `C:/Claude Projects/Gridiron Warrior/Deliverables/_system/review/ideas.html`

## Input: the pasted string

```
gw-ideas-result: forge=[slug1,slug2] top=[slug3] skip=[slug4,slug5]
```

Three buckets, each a plain comma-separated list of backlog slugs. Any bucket
may be empty (`forge=[]`). Slugs never carry a note here (unlike gw-review's
polish). If the string does not contain all three `name=[...]` buckets, or is
not prefixed `gw-ideas-result:`, report "malformed ideas-result string" with
what you got and STOP. Do not guess.

## Verdict semantics

- **forge**: run `/gw-content-forge` on the slug immediately. This does NOT
  change the backlog entry's status; the next scan auto-marks it `forged` once
  the topic folder exists (see `scan_folders._process_forge_backlog`).
- **top**: bump the entry so tonight's picker takes it first. Set
  `score` to `"N/20"` where N = max(current N, 18). Leave status `pending`.
- **skip**: set `status = "skipped"` and record a `skip_reason`. House rule:
  every skip carries a reason (the ideas page lists skipped-with-reason entries
  for a human override). For a manual SKIP, use the reason Scott gives; if none,
  write `skip_reason = "manual skip from ideas review"`.

## Step 1: Apply the top and skip buckets to state

Run this once. Pass the whole pasted line as `$RESULT_STRING` (the regex
ignores the `gw-ideas-result:` prefix). If Scott gave a spoken skip reason,
also pass it as `$SKIP_REASON`; otherwise leave it empty.

```bash
python - "$RESULT_STRING" "${SKIP_REASON:-}" <<'PY'
import json, re, sys, pathlib
raw = sys.argv[1]
manual_reason = (sys.argv[2].strip() if len(sys.argv) > 2 else "") or "manual skip from ideas review"

STATE = pathlib.Path("C:/Claude Projects/Gridiron Warrior/Deliverables/queue-state.json")

def bucket(name):
    m = re.search(name + r"=\[(.*?)\](?=\s+\w+=\[|\s*$)", raw)
    return m.group(1).strip() if m else None

forge_b, top_b, skip_b = bucket("forge"), bucket("top"), bucket("skip")
if forge_b is None or top_b is None or skip_b is None:
    sys.exit("MALFORMED: expected forge=[...] top=[...] skip=[...], got: " + raw)

def slugs(s):
    return [x.strip() for x in s.split(",") if x.strip()]

forge = slugs(forge_b)
top = slugs(top_b)
skip = slugs(skip_b)

data = json.loads(STATE.read_text(encoding="utf-8"))
backlog = {e.get("slug"): e for e in data.get("forge_backlog", []) if isinstance(e, dict)}
actions = []

def score_n(entry):
    head = str(entry.get("score") or "").split("/")[0].strip()
    return int(head) if head.isdigit() else 0

for slug in top:
    e = backlog.get(slug)
    if not e:
        actions.append(f"SKIP top {slug} (not in backlog)"); continue
    new_n = max(score_n(e), 18)
    e["score"] = f"{new_n}/20"
    e["status"] = "pending"
    actions.append(f"top {slug} -> score {e['score']}")

for slug in skip:
    e = backlog.get(slug)
    if not e:
        actions.append(f"SKIP skip {slug} (not in backlog)"); continue
    e["status"] = "skipped"
    e["skip_reason"] = manual_reason
    actions.append(f"skip {slug} -> skipped ({manual_reason})")

# forge entries are only echoed here; forging happens in Step 2 outside this script.
for slug in forge:
    actions.append(f"forge {slug} (run /gw-content-forge - see Step 2)"
                   if slug in backlog else f"SKIP forge {slug} (not in backlog)")

STATE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print("\n".join(actions) if actions else "no decisions to apply")
PY
```

## Step 2: Forge the forge bucket

For EACH slug in `forge=[...]` that exists in the backlog, run
`/gw-content-forge` on it now (one invocation per slug, using the backlog
entry's title/angle as the topic). If the bucket is empty, skip this step.

## Step 3: Re-scan

The scan auto-marks any freshly forged slug as `forged` and refreshes the
ideas page.

```bash
cd "C:/Claude Projects/Gridiron Warrior"
python -m scripts.gwqueue.scan_folders
python -m scripts.gwqueue.build_ideas_page
```

## Step 4: Report

One table, exactly what was applied:

| verdict | slug | result |
|---|---|---|
| forge | ... | forged now via /gw-content-forge |
| top | ... | score raised to N/20 |
| skip | ... | skipped, reason recorded |

Note any `SKIP ... (not in backlog)` lines the script emitted so a mistyped
slug is visible, not silent.

## Voice

Mechanical status output. Any recommendation stays in Scott's tone: short,
direct, no em-dashes.
