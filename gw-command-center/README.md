# gw-command-center

Single source of truth for Gridiron Warrior skills across Claude Code, Cowork, and chat.

**Version:** 0.1.0
**Status:** v0.1 — skills only. Command migration is a follow-up.

## What's in here

Ten skills under `skills/`:

| Skill | Purpose |
|---|---|
| `leech-letter-editor` | Edit/ghostwrite the weekly Saturday Leech Letter in Scott's voice |
| `gw-substack-forge` | Long-form Substack article engine in Scott's voice |
| `gw-content-forge` | Short-form social content from transcripts (planned — copied in command migration) |
| `gw-youtube-takeaways` | YouTube/notebook → 8 takeaways + GW 10x insight + PDF + Drive |
| `gw-image-forge` | OpenAI Images API image generation, SI 1987 / Tri-X 400 aesthetic |
| `ig-carousel` | Editable HTML Instagram carousels with PNG/PDF export |
| `jedi-council` | 5-advisor multi-agent council for strategic decisions |
| `pdf` | Read, edit, form-fill, convert PDFs |
| `pptx` | Create, edit, validate PowerPoint decks |
| `skill-creator` | Build, evaluate, and benchmark new skills |
| `kit-guardrails` | Safety rails on every Kit MCP call — never send / schedule / delete / bulk-mutate without confirmation |

## External dependencies

These skills rely on tooling outside the plugin:

- **`gw-image-forge`** — requires `OPENAI_API_KEY` in `D:\Claude Projects\Gridiron Warrior\scripts\.env`
- **`pdf`** — requires Python packages `pypdf` and `reportlab` (installed)
- **`pptx`** — requires `soffice` (LibreOffice) on PATH for `.pptx → .pdf` conversion. Install LibreOffice if PDF export is needed; everything else works without it.
- **`gw-youtube-takeaways`** — `scripts/build_pdf.py` uses `reportlab` (installed). YouTube extraction relies on the `Claude in Chrome` MCP.

## Install (v0.1 — dev mode)

Skills are symlinked into `~/.claude/skills/` for dogfood verification. Once verified, the plugin is installed via the local-folder marketplace pattern:

```powershell
# Add the parent folder as a local marketplace, then install
/plugin install gw-command-center
```

## Versioning

- `0.1.0` — initial 10-skill adoption + new gw-image-forge build
- `0.2.0` — command migration (`gw-*` commands)
- `0.3.0` — swap `gw-youtube-takeaways` to use the native `notebooklm` MCP
