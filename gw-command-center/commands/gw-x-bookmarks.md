---
name: gw-x-bookmarks
model: sonnet
description: "Convert X (Twitter) bookmarks into richly connected Obsidian notes with full threads, extracted articles, GW football/S&C tags, and wikilinks. Pipeline runs from D:/Claude Projects/GW-X-Bookmarks/ and writes to D:/Claude Projects/Gridiron Warrior/X-Bookmarks/ in the vault."
---

# GW X Bookmarks Pipeline

Converts X bookmarks into richly connected Obsidian notes with full threads, extracted articles, GW football/S&C tags, and wikilinks.

**Project:** `D:/Claude Projects/GW-X-Bookmarks/`
**Output:** `D:/Claude Projects/Gridiron Warrior/X-Bookmarks/` in vault

---

## First-Time Setup

1. Go to developer.twitter.com — create a Project + App
2. App type: Web App. Callback URL: `http://localhost:3000/callback`
3. Scopes: `tweet.read  bookmark.read  users.read  offline.access`
4. Copy CLIENT_ID + CLIENT_SECRET into `.env` (copy from `.env.example`)
5. Run auth: `npm run auth` — opens browser, saves token automatically

---

## Run the Pipeline

```bash
cd "D:/Claude Projects/GW-X-Bookmarks"

# Full pipeline (runs all 5 stages in sequence)
npm run pipeline

# Or run stages individually (each is resumable)
node src/01-fetch.js      # ~5 min   — pulls bookmarks from X API into SQLite
node src/02-threads.js    # ~10 min  — expands full conversation threads
node src/03-articles.js   # ~30 min  — fetches linked articles via Defuddle
node src/04-tag.js        # ~1 min   — applies GW football/S&C tags + entities
node src/05-notes.js      # ~2 min   — writes .md files + hub pages to vault
```

---

## Check Progress

```bash
npm run stats
```

---

## Re-Run for New Bookmarks

Run monthly. Each stage is idempotent — only processes records not yet handled.
SQLite tracks all state. Re-running any stage skips already-completed records.

---

## Output Structure

```
Gridiron Warrior/X-Bookmarks/
  tweets/
    [tweet-id].md       ← one note per bookmark
  index/
    _X Bookmarks.md     ← master hub
    @author.md          ← per-author pages
    2024-03.md          ← month index pages
    strength-training.md  ← tag hub pages
    Dante Scarnecchia.md  ← entity hub pages
```

---

## Troubleshooting

**403 on fetch:** Bookmarks endpoint needs Basic tier ($100/mo) at developer.twitter.com
**Token expired:** Run `npm run auth` again to refresh
**Article stage slow:** Normal — 1.2s delay per URL to be polite to servers
**node:sqlite warning:** "Experimental feature" — safe to ignore, works fine in Node 24
