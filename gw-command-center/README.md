# gw-command-center

Single source of truth for Gridiron Warrior skills and commands across Claude Code, Cowork, and claude.ai chat.

**Version:** 0.6.0
**Owner:** Scott Leech / Scott Leech Training LLC
**Marketplace:** [`ScottleechTraining/gw-plugins`](https://github.com/ScottleechTraining/gw-plugins) (public)

---

## What's in here

**11 skills** + **33 commands** = 44 components, all owned by this plugin.

### Skills

| Skill | Purpose |
|---|---|
| `leech-letter-editor` | Edit/ghostwrite the weekly Saturday Leech Letter in Scott's voice |
| `gw-substack-forge` | Long-form Substack article engine in Scott's voice |
| `gw-youtube-takeaways` | YouTube/notebook → 8 takeaways + GW 10x insight + branded PDF + Drive upload. Native `notebooklm` MCP (v0.3.0+); Chrome MCP archived as fallback. |
| `gw-image-forge` | OpenAI Images (`gpt-image-1`) image generation, SI 1987 / Tri-X 400 aesthetic, B&W default + cinematic color mode |
| `ig-carousel` | Editable HTML Instagram carousels with PNG/PDF export, 6 style packs, Vitesse Bold embedded |
| `jedi-council` | 5-advisor multi-agent council for strategic decisions (Karpathy LLM Council pattern) |
| `pdf` | Read, edit, form-fill, convert PDFs |
| `pptx` | Create, edit, validate PowerPoint decks |
| `skill-creator` | Build, evaluate, and benchmark new skills |
| `kit-guardrails` | Safety rails on every Kit MCP call — never send / schedule / delete / bulk-mutate without explicit confirmation |
| `gw-voice-gate` | Mechanical PASS/FAIL Scott-voice QA gate (banned words, em-dashes, sign-off, slop tells). Mandatory final step in every voice skill |

### Commands

All 27 `gw-*` slash commands from the daily GW operating pipeline. Highlights:

- `/gw-daily`, `/gw-morning-readiness`, `/gw-morning-digest` — daily ritual
- `/gw-research`, `/gw-ai-research`, `/gw-business-research`, `/gw-sc-research`, `/gw-everything-on` — research pipelines
- `/gw-content-forge`, `/gw-film-study-brief`, `/gw-freebie-forge`, `/gw-extract-quotes` — content production
- `/gw-queue`, `/gw-triage`, `/gw-mark`, `/gw-ship`, `/gw-unship`, `/gw-publish` — Deliverables queue management
- `/gw-dewey-ingest`, `/gw-dewey-daily`, `/gw-dewey-backfill`, `/gw-x-bookmarks`, `/gw-screenshot-ingest`, `/gw-voice-ingest` — ingest pipelines
- `/gw-seed-writer`, `/gw-stage`, `/gw-weekly-synthesis` — content shaping
- `/gw-carousel-batch` — parallel carousel builds with central photo assignment + render-and-eyeball verification
- `/gw-pipeline-doctor`, `/gw-plugin-ship` — ops runbooks (overnight failure triage, plugin release ritual)

Every command carries `model:` frontmatter (opus for judgment/voice/synthesis, sonnet for mechanical work) per the MODEL POLICY in the root CLAUDE.md. New commands must include one.

---

## Install

### Claude Code (CLI)

```bash
claude plugin marketplace add ScottleechTraining/gw-plugins
claude plugin install gw-command-center@gw-plugins
```

Restart Code. The 37 components are now active at user scope.

### Cowork

1. Open Cowork → **Settings → Plugins → Add marketplace**
2. URL: `ScottleechTraining/gw-plugins`
3. Click **Sync** → click **Install** on `gw-command-center`

### claude.ai chat

1. https://claude.ai/customize → **Skills**
2. Personal plugins → **+** → **Add marketplace**
3. URL: `ScottleechTraining/gw-plugins`
4. Click **Sync** → click **Install** on `gw-command-center`

---

## External dependencies

These skills rely on tooling outside the plugin:

| Skill | Dependency | Install |
|---|---|---|
| `gw-image-forge` | `OPENAI_API_KEY` in `D:\Claude Projects\Gridiron Warrior\scripts\.env` | Get key from https://platform.openai.com/api-keys, add billing |
| `pdf` | `pypdf`, `reportlab` | `pip install pypdf reportlab` |
| `pptx` | `soffice` (LibreOffice) for PDF conversion | Install LibreOffice; everything else works without it |
| `gw-youtube-takeaways` | `reportlab` for PDF, native `notebooklm` MCP (`mcp__notebooklm__*`) for extraction, `Claude in Chrome` MCP as legacy fallback | Already in stack — run `nlm login` once if auth expires |
| `gw-research` and friends | `nlm` CLI, `yt-dlp` | Already in stack — see CLAUDE.md "Active Intelligence Pipeline" section |

---

## Edit flow (code is truth)

```
1. Edit the file in D:\Claude Projects\plugins\gw-command-center\
2. Validate:        claude plugin validate gw-command-center
3. Refresh local:   claude plugin marketplace update gw-plugins
                    claude plugin uninstall gw-command-center
                    claude plugin install gw-command-center@gw-plugins
4. Commit + push:   git -C "D:\Claude Projects\plugins" add -A
                    git -C "D:\Claude Projects\plugins" commit -m "..."
                    git -C "D:\Claude Projects\plugins" push
5. Cowork + chat refresh themselves from github on next session.
```

Bump `version` in `gw-command-center/.claude-plugin/plugin.json` on any non-trivial change.

---

## Smoke tests

After install, run any of these to confirm the plugin is hot:

- "make me a carousel about offseason structure" → `ig-carousel`
- "ask the council if I should kill DFY" → `jedi-council`
- "generate an image of a chalk-dusted barbell" → `gw-image-forge` (~$0.10, ~30s for high quality)
- "generate an image of X, dry run only" → `gw-image-forge --dry-run` (no cost, prints prompt only)

The image-forge smoke test image (locker room at 5am, SI '87 B&W) lives at:
`D:\Claude Projects\Gridiron Warrior\Images\locker-room-5am.png`

---

## Why this plugin exists

Before v0.1, the same skill lived in three places: Code user-level `~/.claude/skills/`, Code project-level `.claude/skills/`, and the Cowork `anthropic-skills` plugin bundle. The same trigger phrase produced different output on different surfaces because each copy drifted independently. Edits in Code never reached Cowork.

This plugin ends that. One file, one git history, three surfaces. If you find a loose `gw-*.md` outside this folder, the plugin install is broken — fix the install, don't recreate the loose file.

The non-negotiable rule lives in `D:\Claude Projects\CLAUDE.md` under "PLUGIN & SKILL DISTRIBUTION (CODE IS TRUTH)".

---

## Disabling the old Cowork bundle

After installing this plugin in Cowork or claude.ai chat, the parallel `anthropic-skills` GW bundle is still active and will compete with the plugin for natural-language routing. To restore single-source-of-truth, disable the duplicates:

**In claude.ai chat:**
1. https://claude.ai/customize → **Skills**
2. In the middle column, find each duplicate GW skill (those that exist both as Personal skill AND in `gw-command-center` plugin)
3. Click into each duplicate → top-right three-dot menu (⋮) → **Delete**
4. Targets to delete (each is a Personal-skill copy that the plugin now owns):
   - `gw-content-forge`, `gw-image-forge`, `gw-substack-forge`, `gw-youtube-takeaways`
   - `ig-carousel`, `jedi-council`, `leech-letter-editor`, `skill-creator`
   - `pdf`, `pptx` (only if you have parallel copies; sometimes claude.ai keeps these scoped to the anthropic-skills plugin)
5. Also remove the standalone **Gw kit** plugin entirely (the plugin's `kit-guardrails` owns this surface now)
6. **KEEP** `grill-me` and `notebooklm-bridge` if they exist — `grill-me` is canonical local, `notebooklm-bridge` we intentionally skipped folding in (the native MCP is direct)

**In Cowork:**
1. Open Cowork → **Settings → Plugins**
2. Find the `anthropic-skills` plugin in the list
3. For each GW skill inside it (`gw-content-forge`, `gw-image-forge`, `gw-substack-forge`, `gw-youtube-takeaways`, `ig-carousel`, `jedi-council`, `leech-letter-editor`, `skill-creator`), toggle OFF
4. Find the `gw-kit` plugin and disable it entirely

After this, the router has exactly one source for every GW skill — the plugin. The "code is truth" loop is closed across all three surfaces.

---

## Versioning

| Version | What changed |
|---|---|
| **0.1.0** (2026-06-06) | Initial. 10 skills + 27 commands. `gw-image-forge` rebuilt against OpenAI Images API. Voice-writing guardrails on `leech-letter-editor` + `gw-substack-forge`. |
| **0.2.1** (2026-06-07) | Frontmatter added to all 27 commands (validation now clean). `--dry-run` flag added to `gw-image-forge` for no-cost prompt iteration. README rewritten. `gw-image-forge` prompt methodology rewritten to documentary photo-editor framing: 5-block prompt structure (Subject/Environment/Camera/Medium/Exclusions), 4 era presets (1980s SI default, 1990s NCAA media guide, 2000s ESPN Magazine, modern D1 athletic comms), 15-item imperfection variable list, verbatim Reality Layer paragraph, banned-word enforcement (no "cinematic", "ultra detailed", "volumetric lighting", "dramatic lighting", etc.). |
| **0.3.0** (2026-06-07) | `gw-youtube-takeaways` swapped from Chrome MCP DOM-scraping to native `mcp__notebooklm__*` MCP server. SKILL.md and `references/notebooklm-extraction.md` rewritten around `notebook_list`, `notebook_get`, `source_add(wait=True)`, `source_get_content`, `notebook_query(source_ids=[…])`, and `source_describe`. No more click coordinates, no more JavaScript injection to scrape `chat-message-pair`, no more 60-second waits. Source titles return untruncated. AI queries are cleanly scoped to a single source via `source_ids` parameter rather than prompt-engineering trick. Mode B (raw URLs) now adds to the "Youtube Videos" notebook seamlessly via `source_add(urls=[…], wait=True)`. Chrome MCP path documented as legacy fallback for sessions where the MCP server is unavailable. End-to-end notebook review time drops from 4-6 minutes to 60-90 seconds. |
| **0.4.0** (2026-06-07) | `gw-content-forge` Cowork variant folded into the plugin command. Single source of truth restored. The merged command now handles TWO MODES: **TRANSCRIPT MODE** (paste a transcript → get the correct asset set for podcast / Film Study / Wildcat Webinar) and **CONTENT PACK MODE** (give a topic or file → get 3 Twitter threads + 2 IG carousels + 3 reel ideas + email). Per-content-type asset variations come from the Cowork SKILL: podcast = 6 assets (YT desc, HelloAudio desc, email, thread, IG caption, show notes), Film Study = 5 assets, Wildcat Webinar = 6 assets (adds guest share message). Plugin-side richness preserved: wiki-first integration, NotebookLM depth check, External Library cross-domain sweep (Dewey saves / Business briefs / AI briefs / Voice corpus / Daily seeds), wiki ingest pipeline, queue-system save-to-`_inbox/`, forge backlog mark step. Validation clean. |

| **0.5.x** (2026-06/07) | Incremental fixes shipped without README rows (novelty-gate collision review in `gw-nightly-forge`, queue/idea-page integration, misc). Table drifted from `plugin.json`; closed at 0.6.0. |
| **0.6.0** (2026-07-05) | **Opus/Sonnet handoff release.** Every command now carries `model:` frontmatter (17 opus, 16 sonnet) so nothing inherits the Fable session model; Fable is planning-only per the new MODEL POLICY in root CLAUDE.md. New skill `gw-voice-gate` (mechanical Scott-voice PASS/FAIL checklist) wired as mandatory final step into `leech-letter-editor`, `gw-substack-forge`, `gw-content-forge`. New commands: `gw-carousel-batch` (parallel carousel builds, central photo assignment, render-and-eyeball verification), `gw-pipeline-doctor` (overnight failure runbook: D: drive check, health JSONs, 401/token expiry, rerun_failed_jobs.py, git divergence rules), `gw-plugin-ship` (release ritual). `ig-carousel` v3.5 gains a "Known traps" section (hero JPEG-not-PNG, pack--case selector, headless quirks, kill-your-servers, mandatory visual verification). Explicit rubrics added to `gw-triage` (promotion rubric, default Cold never Kill), `gw-seed-writer` (angle-quality gate, zero-is-ok), `gw-weekly-synthesis` (wiki promotion criteria, under-promote default). `jedi-council` advisor/peer-review spawns pinned to `model: opus`. |

Still pending (Scott action required):
- Disable the parallel Cowork `anthropic-skills` GW bundle (must be done in the Cowork UI; see README "Disabling the old Cowork bundle" section). With v0.4.0, the plugin owns every GW skill and command. Once disabled, the router never sees the parallel copies. Target: do it next time you open Cowork.

---

Keep the Fire Burning.

— Leech
