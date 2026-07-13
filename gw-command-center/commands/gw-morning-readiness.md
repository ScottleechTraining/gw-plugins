---
name: gw-morning-readiness
model: sonnet
description: "One-glance GREEN / YELLOW / RED verdict on the overnight GW pipeline + one next action"
---

# /gw-morning-readiness — Pipeline Verdict

Answers one question: did the overnight pipeline do its job, and if not, what is the ONE thing to do about it.

## Step 1 — Run the deterministic check

```bash
cd "C:\Claude Projects" && "C:\Python314\python.exe" "Gridiron Warrior/scripts/morning_readiness.py"
```

This reads the same sources of truth the health check uses — per-gate status JSON, schtasks Last Result — plus live topic-queue counts, and prints a verdict:

- **GREEN** — every expected gate complete, schtasks clean, queues sane. Nothing to do.
- **YELLOW** — the briefing ran, but a degradable gate (research / seed / ingest) is missing or a topic queue is empty. Thinner than it should be.
- **RED** — a core gate (morning-digest, daily-closeout) did not complete, or a GW scheduled task returned non-zero. Act now.

## Step 2 — Present it

Relay the verdict and the single `next action` line verbatim. Do NOT soften RED into "mostly fine." If RED, the recommended recovery is almost always:

```bash
cd "C:\Claude Projects" && "C:\Python314\python.exe" "Gridiron Warrior/scripts/rerun_failed_jobs.py" --date today --dry-run
```

then drop `--dry-run` to actually rerun the failed/missing gates (run_type=recovery).

Keep the report short and dense. Lead with the verdict. No throat-clearing.
