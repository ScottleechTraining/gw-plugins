---
name: gw-plugin-ship
model: sonnet
description: "Ship a gw-command-center plugin change: validate, version bump, local refresh, commit and push the plugins repo."
---

# /gw-plugin-ship — Ship a Plugin Change

The exact "code is truth" edit flow, turned into ordered steps. Run it after editing any skill or command in the plugin so the change reaches all three surfaces (Code, Cowork, claude.ai chat) without drift.

Single source of truth: `C:\Claude Projects\plugins\gw-command-center\`. If the same file lives anywhere else, the plugin is broken — see Step 1.

## Step 1 — Confirm edits live ONLY in the plugin folder

The change must be in `C:\Claude Projects\plugins\gw-command-center\` and nowhere else. Loose copies are the drift source the plugin exists to kill. Verify no shadow copies exist for the files you touched:

- NEVER `~/.claude/commands/gw-*.md` or `~/.claude/skills/gw-*` (deleted in v0.1 migration).
- NEVER `C:\Claude Projects\.claude\commands\gw-*.md` (the old project-level shadow).

If you find a loose `gw-*` file outside the plugin folder, the install is broken. Delete the loose file and fix the install — do not edit it, and do not let it survive this ship.

## Step 2 — Bump the version and log it

For any non-trivial change, bump `version` in:

```
C:\Claude Projects\plugins\gw-command-center\.claude-plugin\plugin.json
```

Then add a row to the **Versioning** table at the bottom of `C:\Claude Projects\plugins\gw-command-center\README.md` describing what changed. Keep the description concrete (which skill/command, what behavior moved).

## Step 3 — Validate

From the plugins directory:

```bash
cd "C:\Claude Projects\plugins" && claude plugin validate gw-command-center
```

Fix anything it flags before going further. A dirty validation does not ship.

## Step 4 — Refresh the local cache

Three commands, in order. This is how Code picks up the edit locally:

```bash
claude plugin marketplace update gw-plugins
claude plugin uninstall gw-command-center
claude plugin install gw-command-center@gw-plugins
```

Note: the refreshed plugin takes effect NEXT session, not the current one. Do not expect the new behavior in the session you shipped from.

## Step 5 — Commit and push the plugins repo

Cowork and claude.ai chat install from the GitHub copy, so the change cannot reach them until it is pushed:

```bash
git -C "C:\Claude Projects\plugins" add -A
git -C "C:\Claude Projects\plugins" commit -m "<what changed>"
git -C "C:\Claude Projects\plugins" push
```

This repo pushes clean. It is a SEPARATE repo from the main GW vault repo — the main-repo local/origin divergence and fast-forward-only rules do NOT apply here. A plain `push` is correct.

## Step 6 — Tell Scott to click Sync (Cowork + claude.ai do NOT auto-refresh)

The Cowork and claude.ai copies are snapshots taken the last time Scott clicked **Sync** on the gw-plugins marketplace. They never update on their own. Worse, the Cowork desktop app injects its snapshot into Claude Code sessions, where a stale copy can shadow the fresh CLI install (found 2026-09-05: Cowork had sat at v0.1.0 since June 6).

Put this in the report, verbatim, as the single next action:

> Sync now: Cowork → Settings → Plugins → gw-plugins → **Sync** → **Update** gw-command-center. Then https://claude.ai/customize → Skills → gw-plugins → **Sync** → **Update**.

The SessionStart hook in `C:\Claude Projects\.claude\settings.json` runs `scripts/check_plugin_drift.py` and prints a PLUGIN DRIFT warning until the Cowork snapshot matches `plugin.json`.

## Step 7 — Report

- Version shipped (old to new).
- Files changed.
- Validation result (clean / what was fixed).
- Confirm: local refreshed (live next session), repo pushed.
- The Sync instruction from Step 6 as the last line.
