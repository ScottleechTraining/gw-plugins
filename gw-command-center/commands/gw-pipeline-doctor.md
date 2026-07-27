---
name: gw-pipeline-doctor
model: claude-opus-5
description: "Diagnose and repair overnight GW pipeline failures. Ordered runbook: drive check, health status files, sched logs, auth expiry, rerun, known traps."
---

# /gw-pipeline-doctor — Pipeline Repair Runbook

When the overnight pipeline broke and Scott needs it fixed. Work the steps IN ORDER. Cheapest and most-likely cause first. Stop at the first step that explains the failure and act on it. Do not skip ahead.

`/gw-morning-readiness` tells you IF it broke. This tells you WHY and fixes it.

Paths (all real, confirmed against the code):
- Health status files: `C:\Claude Projects\Gridiron Warrior\scripts\health\<gate>-<YYYY-MM-DD>.status.json`
- Sched logs: `C:\Users\scott\.claude\sched-logs\gw-<gate>.log`
- Token marker: `C:\Users\scott\.claude\sched-state\setup-token-created.json`

## Step 1 — Drive check FIRST

The D: drive (GW_Har) intermittently dismounts and takes the whole vault and repo with it. Every gate reads from D:. If the drive dropped, nothing else is diagnosable and every downstream symptom is a lie.

```bash
test -d "C:\Claude Projects\Gridiron Warrior" && echo "VAULT PRESENT" || echo "VAULT MISSING"
```

If MISSING: report **"D: drive (GW_Har) dropped — reconnect it, then re-run the pipeline."** and STOP. Do not diagnose code, do not read logs, do not rerun. Nothing else matters until the drive is back.

If PRESENT: continue.

## Step 2 — Read the health status files

Every gate writes a terminal status JSON. Read today's (and yesterday's, in case the run straddled midnight) and list every gate whose `status` is not `complete`.

```bash
cd "C:\Claude Projects" && "C:\Python314\python.exe" -c "import json,glob,datetime; d=datetime.date.today().strftime('%Y-%m-%d'); [print(g, json.load(open(g)).get('status'), '|', json.load(open(g)).get('root_cause')) for g in sorted(glob.glob(rf'Gridiron Warrior\scripts\health\*-{d}.status.json'))]"
```

Terminal statuses that mean trouble: `failed`, `blocked`, `running` (stuck — killed mid-run), or a missing file entirely (gate never fired). `complete` is the only clean one.

The status JSON carries `root_cause` and `next_action` fields written by the pipeline itself. Read them — they often name the fix. Note each non-`complete` gate for Step 3.

## Step 3 — Read the failing gate's log and classify

For each failed gate, read the tail of its log:

```bash
tail -60 "C:\Users\scott\.claude\sched-logs\gw-<gate>.log"
```

Classify the failure into one of these buckets:

- **auth** — `API Error: 401`, `Failed to authenticate`, `Invalid authentication credentials`. Go to Step 4.
- **drive / path** — file-not-found on a D: path, `vault missing`. Almost always a drive drop that recovered between the run and now — but Step 1 already ruled out a current drop, so this is a transient. Rerun (Step 5).
- **upstream-dependency skip** — `RUNJOB BLOCKED ... required upstream not complete`. This gate is fine; a gate it `needs` failed. Fix the upstream gate first, then this one. The rerunner handles the ordering for you (Step 5).
- **claude runtime error** — non-zero exit from a `claude -p` step that is not a 401 (crash, timeout, tool error). Rerun once (Step 5); if it repeats, read the full step output.
- **validator failure** — `payload exited 0 but produced no valid artifact`, or a `[INVALID]` line. The command ran but the expected artifact (a dated brief, a marker line, a Netlify deploy) never landed. Rerun; if it repeats, the payload logic itself is broken, not the infra.

## Step 4 — Auth failures

Scheduled tasks do NOT use interactive `/login`. They authenticate with a `claude setup-token` OAuth token exposed as the `CLAUDE_CODE_OAUTH_TOKEN` env var. That token lasts roughly one year. Its issue date is recorded in the marker file:

```bash
cat "C:\Users\scott\.claude\sched-state\setup-token-created.json"
```

A 401 in the logs means one of two things:
1. The token expired (compare `created_at` + ~365 days to today).
2. The env var is not reaching the scheduled process.

Report it plainly and tell Scott:
> **Run `claude setup-token` again, then `setx CLAUDE_CODE_OAUTH_TOKEN <new-token>`, then rewrite `C:\Users\scott\.claude\sched-state\setup-token-created.json` with today's date.**

Do NOT attempt an interactive `/login` from a script — it will hang forever with no TTY. Do NOT tell Scott to run `nlm login` for a Claude 401 (that is a NotebookLM auth fix, a different failure surfaced by `/gw-morning-readiness` as a blocked brief).

Note: preflight already ignores stale 401s from before the last `=== GW-CLAUDE-OK <gate> ===` marker in the log, so if you see a 401 ABOVE a more recent OK marker, it is already-healed — not the current failure.

## Step 5 — Rerun through the rerunner, never by hand

Do NOT invoke gates by hand or re-run schtasks one at a time. Use the rerunner — it reads each status file, reruns only the non-complete gates, respects dependency order (upstream producers before the digest), and labels the run `GW_RUN_TYPE=recovery` so it does not masquerade as the scheduled run. Validators still run.

Dry run first, always:

```bash
cd "C:\Claude Projects" && "C:\Python314\python.exe" "Gridiron Warrior/scripts/rerun_failed_jobs.py" --date today --dry-run
```

Then drop `--dry-run` to actually rerun:

```bash
cd "C:\Claude Projects" && "C:\Python314\python.exe" "Gridiron Warrior/scripts/rerun_failed_jobs.py" --date today
```

One stubborn gate only:

```bash
cd "C:\Claude Projects" && "C:\Python314\python.exe" "Gridiron Warrior/scripts/rerun_failed_jobs.py" --gate <gate>
```

A `complete` gate is never rerun. Weekly gates read on a grace day are reported but not auto-rerun (rerun them on their fire day). After the rerun, go back to Step 2 and confirm the gates went `complete`.

## Step 6 — Known traps

Consult before improvising. Each of these has bitten before.

**(a) Delete-pending file locks.** Orphaned `http.server` processes or hung headless Edge/Chrome leave files in a delete-pending state. An `Access is denied` on delete is an OPEN HANDLE, not an ACL problem. Do not chase permissions. Find and kill the orphaned process:

```bash
tasklist | grep -i -E "python|msedge|chrome"
```

Kill the strays, then the delete succeeds.

**(b) `PUSH REJECTED` in the closeout log.** The daily-closeout gate pushes master fast-forward ONLY. A `[git_safe_commit] PUSH REJECTED (origin moved?)` line means a cloud PR merged to `origin/master` while local work was in flight. The local commits are intact and safe. Reconcile INTERACTIVELY — pull, inspect, merge by hand. NEVER blind-merge and NEVER force-push. The two histories diverged for a reason; look before you reconcile.

**(c) A gate that wrote nothing.** A `running` status with no artifact, or an empty log tail, means the gate was killed mid-run — a credit outage or a crash, not a clean failure. The gate may have written partial state or nothing at all. Before rerunning, verify what actually landed on disk (the expected brief / carousel / marker). When you rerun, spell out the verified starting state so the gate does not double-write or resume from a half-finished artifact.

## Step 7 — Output

Report tight and dense. One line per gate:

- **GREEN / YELLOW / RED** verdict per gate.
- What was fixed (and how).
- What still needs Scott (auth re-token, drive reconnect, interactive git reconcile — the things a script cannot do).
- **ONE next action.** Lead with it if anything is still broken.

No throat-clearing. Do not soften RED. If the drive is down or the token expired, that is the headline.
