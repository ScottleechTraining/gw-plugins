# gw-command-center

Single source of truth for Gridiron Warrior skills and commands across Claude Code, Cowork, and claude.ai chat.

**Version:** 0.2.0-dev (latest tag: v0.1.0)
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
| `gw-youtube-takeaways` | YouTube/notebook → 8 takeaways + GW 10x insight + branded PDF + Drive upload |
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
| `gw-youtube-takeaways` | `reportlab` for PDF, `Claude in Chrome` MCP for video extraction | Already in stack |
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
| **0.2.0-dev** (in progress) | Frontmatter added to all 27 commands (validation now clean). `--dry-run` flag added to `gw-image-forge` for no-cost prompt iteration. README rewritten. |

Planned for **0.3.0**:
- Swap `gw-youtube-takeaways` from Chrome MCP extraction to native `notebooklm` MCP
- Fold `gw-content-forge` Cowork variant in if Scott decides he wants the parallel version killed
- Disable Cowork `anthropic-skills` GW bundle entirely

---

Keep the Fire Burning.

— Leech
