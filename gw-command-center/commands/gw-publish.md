---
name: gw-publish
description: "Mark a campaign as published. Generates a 1-page wiki summary (the campaign's permanent record in the second brain), archives the topic folder to Deliverables/USED ALREADY/YYYY-MM/, and logs the publish event. Run AFTER scheduling or shipping a campaign's social, email, and Substack assets."
---

# GW Publish — Deliverable Archive + Summary Auto-Flow

Mark a campaign as published. This command:
1. Generates a 1-page wiki summary (the campaign's permanent record in the second brain)
2. Moves the topic folder to `Deliverables\USED ALREADY\YYYY-MM\`
3. Logs the publish event

Run this AFTER you've scheduled or shipped a campaign's social/email/Substack assets.

## Topic: $ARGUMENTS

The user provides one of:
- A topic slug matching a Deliverables folder name (e.g., `jumps-by-force-vector`)
- A full folder path (e.g., `D:/Claude Projects/Gridiron Warrior/Deliverables/2026-05-07-jumps-by-force-vector`)
- Nothing — in which case, list the topic folders in `Deliverables/` (excluding `USED ALREADY/`, `_templates/`) and ask which to publish

## Vault Paths

- **Deliverables source:** `D:/Claude Projects/Gridiron Warrior/Deliverables/`
- **Archive destination:** `D:/Claude Projects/Gridiron Warrior/Deliverables/USED ALREADY/[YYYY-MM]/`
- **Wiki summaries:** `D:/Claude Projects/Gridiron Warrior/wiki/summaries/`
- **Wiki index:** `D:/Claude Projects/Gridiron Warrior/wiki/index.md`
- **Wiki log:** `D:/Claude Projects/Gridiron Warrior/wiki/log.md`

## Step 1: Resolve the Topic Folder

Find the folder. If multiple folders match (e.g., `2026-05-07-jumps-by-force-vector` and `2026-04-12-jumps-by-force-vector`), list them with last-modified dates and ask Scott which to publish.

Read the folder contents. Expected assets (some optional):
- `*-research-brief.md`
- `*-content-pack.md`
- `*-substack-article.md`
- `*-ig-caption.md`
- `*-carousel.html`
- `*-social-pack.html`

## Step 2: Check for Existing Summary

Look in `wiki/summaries/` for an existing page on this topic (filename match or frontmatter `source:` pointing to this Deliverables folder).

If found, ask: "A summary page already exists at [path]. Update the existing page, or create a new dated version?"

## Step 3: Generate the Wiki Summary

Read each deliverable file in the topic folder. Extract:
- **Core teaching** — what is the one thing a coach should walk away knowing
- **Key quote** — the most quotable Scott-voice line in the pack
- **Concepts touched** — wiki concept pages this campaign references or should reference
- **Entities touched** — people, programs, products mentioned (cross-link wiki entity pages)
- **CTAs** — which products/offers the campaign pushes

Write to `wiki/summaries/[topic-slug].md`:

```markdown
---
title: [Topic Title]
type: summary
source: Deliverables/USED ALREADY/[YYYY-MM]/[folder-name]/
date_published: [YYYY-MM-DD]
status: published
tags: [infer 2-3 relevant tags from topic + content type]
pipeline: gw-publish
---

# [Topic Title]

**Source folder:** `Deliverables/USED ALREADY/[YYYY-MM]/[folder-name]/`
**Published:** [YYYY-MM-DD]
**Asset count:** [N] files

## Core Teaching

[2-3 sentences. The one thing this campaign teaches. Coach lens.]

## Key Quote

> [Best Scott-voice line from the pack — usable as a reshare-worthy quote card]

## Assets Shipped

- [Asset type] — [filename]
- (one line per asset)

## Concepts Touched

- [[concepts/[slug]]] (stub or full)
- (link existing concept pages, flag missing ones to back-fill)

## Entities Touched

- [[entities/[slug]]]
- (people, products, programs)

## CTAs Pushed

- [Product/offer] — [why this campaign points there]

## Performance Notes

[Empty section for Scott to fill in later with engagement metrics, conversions, lessons learned.]
```

## Step 4: Move the Folder to Archive

Target path: `Deliverables/USED ALREADY/[YYYY-MM]/[original-folder-name]/`

Where `[YYYY-MM]` is the publish date's year-month. Create the dated month folder if it doesn't exist.

Use PowerShell:
```powershell
$src = 'D:/Claude Projects/Gridiron Warrior/Deliverables/[folder-name]'
$dst = 'D:/Claude Projects/Gridiron Warrior/Deliverables/USED ALREADY/[YYYY-MM]/[folder-name]'
New-Item -ItemType Directory -Force -Path (Split-Path $dst -Parent) | Out-Null
Move-Item $src $dst
```

## Step 5: Update Wiki Index + Log

- Add the summary link to `wiki/index.md` under Summaries → Published Campaigns (create section if missing)
- Append to `wiki/log.md`: `## [YYYY-MM-DD] publish | [topic] — moved to USED ALREADY/[YYYY-MM]/ via gw-publish`

## Step 6: Flag Missing Concept Stubs

If the campaign touched a coaching concept that doesn't have a wiki concept page yet, create a stub using the same format as `/gw-research` Step 7.5.

## Step 7: Report

Tell Scott:
1. Folder moved to: [archive path]
2. Wiki summary created at: [path]
3. Concept stubs created (if any)
4. Anything missing from the campaign (e.g., "no Substack article was found — was this intentional?")
5. The Key Quote pulled — verify it's the right one

## Error Handling

- If topic folder not found, list all candidate folders and ask.
- If destination month folder collides with an existing folder of the same name (unlikely but possible — same topic shipped twice in one month), append `-v2` suffix.
- If wiki summary creation fails partway, don't move the folder yet. Folder move is the LAST step so a failed run leaves Deliverables intact.
