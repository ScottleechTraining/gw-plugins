# gw-command-center

Single source of truth for Gridiron Warrior skills and commands across Claude Code, Cowork, and claude.ai chat.

**Version:** 0.3.0 (latest tag: gw-command-center--v0.3.0)
**Owner:** Scott Leech / Scott Leech Training LLC
**Marketplace:** [`ScottleechTraining/gw-plugins`](https://github.com/ScottleechTraining/gw-plugins) (public)

---

## What's in here

**10 skills** + **27 commands** = 37 components, all owned by this plugin.

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

### Commands

All 27 `gw-*` slash commands from the daily GW operating pipeline. Highlights:

- `/gw-daily`, `/gw-morning-readiness`, `/gw-morning-digest` — daily ritual
- `/gw-research`, `/gw-ai-research`, `/gw-business-research`, `/gw-sc-research`, `/gw-everything-on` — research pipelines
- `/gw-content-forge`, `/gw-film-study-brief`, `/gw-freebie-forge`, `/gw-extract-quotes` — content production
- `/gw-queue`, `/gw-triage`, `/gw-mark`, `/gw-ship`, `/gw-unship`, `/gw-publish` — Deliverables queue management
- `/gw-dewey-ingest`, `/gw-dewey-daily`, `/gw-dewey-backfill`, `/gw-x-bookmarks`, `/gw-screenshot-ingest`, `/gw-voice-ingest` — ingest pipelines
- `/gw-seed-writer`, `/gw-stage`, `/gw-weekly-synthesis` — content shaping

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

## Versioning

| Version | What changed |
|---|---|
| **0.1.0** (2026-06-06) | Initial. 10 skills + 27 commands. `gw-image-forge` rebuilt against OpenAI Images API. Voice-writing guardrails on `leech-letter-editor` + `gw-substack-forge`. |
| **0.2.1** (2026-06-07) | Frontmatter added to all 27 commands (validation now clean). `--dry-run` flag added to `gw-image-forge` for no-cost prompt iteration. README rewritten. `gw-image-forge` prompt methodology rewritten to documentary photo-editor framing: 5-block prompt structure (Subject/Environment/Camera/Medium/Exclusions), 4 era presets (1980s SI default, 1990s NCAA media guide, 2000s ESPN Magazine, modern D1 athletic comms), 15-item imperfection variable list, verbatim Reality Layer paragraph, banned-word enforcement (no "cinematic", "ultra detailed", "volumetric lighting", "dramatic lighting", etc.). |
| **0.3.0** (2026-06-07) | `gw-youtube-takeaways` swapped from Chrome MCP DOM-scraping to native `mcp__notebooklm__*` MCP server. SKILL.md and `references/notebooklm-extraction.md` rewritten around `notebook_list`, `notebook_get`, `source_add(wait=True)`, `source_get_content`, `notebook_query(source_ids=[…])`, and `source_describe`. No more click coordinates, no more JavaScript injection to scrape `chat-message-pair`, no more 60-second waits. Source titles return untruncated. AI queries are cleanly scoped to a single source via `source_ids` parameter rather than prompt-engineering trick. Mode B (raw URLs) now adds to the "Youtube Videos" notebook seamlessly via `source_add(urls=[…], wait=True)`. Chrome MCP path documented as legacy fallback for sessions where the MCP server is unavailable. End-to-end notebook review time drops from 4-6 minutes to 60-90 seconds. |

Planned for **0.4.0** (defer until Scott calls them):
- Fold `gw-content-forge` Cowork variant in if Scott decides he wants the parallel version killed (currently the plugin command handles natural-language triggers via its description, so this may be moot)
- Disable Cowork `anthropic-skills` GW bundle entirely (target: 2026-06-13, one week after v0.1 ship)

---

Keep the Fire Burning.

— Leech
