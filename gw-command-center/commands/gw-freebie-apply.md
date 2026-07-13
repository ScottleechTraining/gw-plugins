---
name: gw-freebie-apply
model: sonnet
description: "Apply a pasted gw-freebie-result string from freebies.html. approve marks a freebie eligible for the Vault, edit flags it (with a note) for the fix batch, kill retires it: standalone .md files move to killed/_freebies/, PDFs inside topic folders just get marked killed in the sidecar. Mechanical parse and apply, no judgment."
---

# GW Freebie Apply - Apply pasted freebie-review decisions

Scott reviews every freebie candidate in `freebies.html`, picks APPROVE /
EDIT / KILL per item, and copies a `gw-freebie-result:` string. This command
parses it and writes decisions to the sidecar `freebie-state.json` and moves
killed standalone `.md` files. Page: `scripts.gwqueue.build_freebie_review_page`
(that is the contract this mirrors; the page only READS the sidecar, applying
is this command's job).

## Paths

- **Deliverables:** `C:/Claude Projects/Gridiron Warrior/Deliverables/`
- **Sidecar state:** `C:/Claude Projects/Gridiron Warrior/Deliverables/_system/review/freebie-state.json`
- **Freebies page:** `C:/Claude Projects/Gridiron Warrior/Deliverables/_system/review/freebies.html`
- **Killed freebies:** `C:/Claude Projects/Gridiron Warrior/Deliverables/killed/_freebies/`

## Input: the pasted string

```
gw-freebie-result: approve=[id1,id2] edit=[id3:"note",id4] kill=[id5]
```

Three buckets. `approve` and `kill` are plain comma-separated ids. `edit`
entries may carry an optional `:"note"` suffix (double-quoted, may contain
commas, so parse on the bracket structure, not naively on commas). Any bucket
may be empty. Each id is the freebie's stable id from the page: its path
relative to `Deliverables/`, extension dropped, slashes replaced with `__`
(e.g. `ready__hell-week__hell-week-freebie`). If the string is not prefixed
`gw-freebie-result:` or is missing any of the three buckets, report
"malformed freebie-result string" with what you got and STOP. Do not guess.

## Verdict semantics

- **approve**: sidecar `status = "approved"`. Eligible for Vault/delivery.
- **edit**: sidecar `status = "edit"` plus `note`. The fix batch picks it up
  with the note. If no note was given, still set status `edit` with empty note.
- **kill**: sidecar `status = "killed"`. If the freebie is a standalone `.md`
  (id contains no `lead-magnet` segment and the resolved file ends in `.md`),
  MOVE the file to `killed/_freebies/`. PDFs/XLSX inside topic folders are NOT
  moved (they live beside their pack); they are only marked killed in the
  sidecar so the page mutes them.

## Step 1: Parse and apply

Run once. Pass the whole pasted line as `$RESULT_STRING`.

```bash
python - "$RESULT_STRING" <<'PY'
import json, re, shutil, sys, pathlib
raw = sys.argv[1]

DELIV = pathlib.Path("C:/Claude Projects/Gridiron Warrior/Deliverables")
SIDECAR = DELIV / "_system" / "review" / "freebie-state.json"
KILLED = DELIV / "killed" / "_freebies"

def bucket(name):
    m = re.search(name + r"=\[(.*?)\](?=\s+\w+=\[|\s*$)", raw)
    return m.group(1).strip() if m else None

approve_b, edit_b, kill_b = bucket("approve"), bucket("edit"), bucket("kill")
if approve_b is None or edit_b is None or kill_b is None:
    sys.exit("MALFORMED: expected approve=[...] edit=[...] kill=[...], got: " + raw)

def plain_ids(s):
    return [x.strip() for x in s.split(",") if x.strip()]

approve = plain_ids(approve_b)
kill = plain_ids(kill_b)

# edit: id or id:"note", note may contain commas -> same regex gw-review uses for polish
edit = {}
for m in re.finditer(r'([^,\[\]]+?)(?::"((?:[^"\\]|\\.)*)")?(?=,|$)', edit_b):
    fid = m.group(1).strip()
    if not fid:
        continue
    edit[fid] = (m.group(2) or "").replace('\\"', '"')

state = {}
if SIDECAR.exists():
    try:
        state = json.loads(SIDECAR.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        state = {}

def resolve(fid):
    """id -> Path. id is rel path (ext dropped, '/'->'__'). Glob back the file."""
    rel = fid.replace("__", "/")
    matches = sorted((DELIV).glob(rel + ".*"))
    return matches[0] if matches else None

actions = []

for fid in approve:
    state[fid] = {"status": "approved"}
    actions.append(f"approve {fid}")

for fid, note in edit.items():
    state[fid] = {"status": "edit", "note": note}
    actions.append(f"edit {fid}" + (f' -> "{note}"' if note else ""))

KILLED.mkdir(parents=True, exist_ok=True)
for fid in kill:
    entry = {"status": "killed"}
    p = resolve(fid)
    is_standalone_md = p is not None and p.suffix.lower() == ".md" and "lead-magnet" not in fid
    if is_standalone_md:
        dst = KILLED / p.name
        if dst.exists():
            dst = KILLED / (p.stem + "__dup" + p.suffix)
        shutil.move(str(p), str(dst))
        entry["moved_to"] = str(dst.relative_to(DELIV)).replace("\\", "/")
        actions.append(f"kill {fid} -> {entry['moved_to']}")
    else:
        where = "file gone" if p is None else "marked killed (stays in place)"
        actions.append(f"kill {fid} ({where})")
    state[fid] = entry

SIDECAR.parent.mkdir(parents=True, exist_ok=True)
SIDECAR.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
print("\n".join(actions) if actions else "no decisions to apply")
PY
```

## Step 2: Rebuild the page

Decided items re-render muted with their status badge so Scott can change his
mind later.

```bash
cd "C:/Claude Projects/Gridiron Warrior"
python -m scripts.gwqueue.build_freebie_review_page
```

## Step 3: Report

One table, exactly what was applied:

| verdict | id | result |
|---|---|---|
| approve | ... | eligible for Vault |
| edit | ... | flagged for fix batch (note) |
| kill | ... | moved to killed/_freebies/ OR marked killed in place |

Note any `kill ... (file gone)` lines so a mistyped or already-moved id is
visible, not silent.

## Voice

Mechanical status output. Any recommendation stays in Scott's tone: short,
direct, no em-dashes.
