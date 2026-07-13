# NotebookLM Extraction (Native MCP, v0.3.0+)

How to pull video content from a NotebookLM notebook using the native `mcp__notebooklm__*` MCP server. This replaced the Chrome-MCP DOM-scraping approach in plugin v0.3.0.

The old approach used click coordinates around `(196, <row-y>)`, JavaScript injection to scrape `chat-message-pair` elements, and a 60-second wait per query. It was brittle and slow. This is neither.

## Setup

No browser navigation needed. The MCP server talks to NotebookLM via its API directly.

If you get an auth error from any tool, run `nlm login` in a terminal first (per the notebooklm MCP server instructions). Tokens last a long time; you shouldn't hit this often.

## Step 1: Find the notebook

```
notebooks = mcp__notebooklm__notebook_list(max_results=100)
```

Filter `notebooks` for a case-insensitive title match against the notebook Scott named. The usual target is "Youtube Videos" but Scott may reference a different one — match the title he gave you, not a hardcoded value.

If no match, tell Scott which notebooks were found and ask which one. Do NOT create a new notebook for him — he manages his layout deliberately.

## Step 2: List sources

```
notebook = mcp__notebooklm__notebook_get(notebook_id=<id>)
```

The returned notebook object includes a `sources` list. Each source has at minimum:
- `source_id` (UUID, used for all per-source operations)
- `title` (full title, no truncation — unlike the DOM-scraped version)
- `source_type` (you want `youtube` or `url` entries)

For "review the new videos" runs, read `C:\Claude Projects\Gridiron Warrior\wiki\log.md` and filter out source titles that appear in recent `ingest | youtube-takeaways` entries.

## Step 3: Extract raw transcript

For each source you want to review:

```
content = mcp__notebooklm__source_get_content(source_id=<id>)
```

Returns:
- `content` (raw transcript text as a string)
- `title`
- `source_type`
- `char_count`

This is the YouTube transcript as NotebookLM indexed it. Length varies — a 9-min video is ~8K chars, a 35-min video can hit 30K+. No AI processing, no summarization. Pure source.

For long transcripts (>20K chars), chunk for synthesis. The middle third is usually the most quote-rich on long interviews.

## Step 4: Get AI takeaways scoped to the source

```
result = mcp__notebooklm__notebook_query(
    notebook_id=<notebook_id>,
    query="For the source titled \"<exact source title>\" ONLY, give me the 8 most important takeaways for a strength and conditioning coach who is also a business owner. Be specific and tactical, not general. Number them 1-8. Include direct quotes in quotation marks where they exist. Include numbers (dollar amounts, follower counts, percentages, time costs) where they appear. Do not pull from any other source.",
    source_ids=[<source_id>],
    timeout=180
)
```

The `source_ids=[<id>]` parameter scopes the AI query to one source — far more reliable than the old "Be careful not to pull from other sources" prompt trick.

Timeout default is 120s; bump to 180 for long videos. The query is synchronous, so once it returns you have your structured takeaways.

## Step 5 (optional): Get keyword chips for theme grouping

```
described = mcp__notebooklm__source_describe(source_id=<id>)
```

Returns:
- `summary` (markdown with `**bold**` keywords)
- `keywords` (list of strings)

Use the `keywords` to seed the "Themes" section on the PDF's final summary page when grouping multiple videos.

## Step 6: Synthesize per-video

For each video, you now have three inputs:
1. Raw transcript (`source_get_content`)
2. Structured takeaways from the AI (`notebook_query`)
3. Optional keywords (`source_describe`)

Combine these into the per-video synthesis output (8 takeaways + 10x Move + Watch verdict) per the parent SKILL.md.

The raw transcript is the source of truth for direct quotes and numbers. The AI takeaways give you structure. If they conflict on a quote, use the raw transcript verbatim.

## Adding YouTube URLs (Mode B/C)

When Scott pastes raw URLs:

```
result = mcp__notebooklm__source_add(
    notebook_id=<youtube-videos-notebook-id>,
    source_type="url",
    urls=[<list of YouTube URLs>],
    wait=True,
    wait_timeout=120
)
```

`wait=True` blocks until NotebookLM finishes pulling the transcript. For typical videos this is 20-60 seconds. For 60+ minute videos, bump `wait_timeout` to 300.

After this returns, refresh the source list via `notebook_get(notebook_id)` and find the new sources by matching titles or by source IDs in the `source_add` result.

If `wait=True` times out, the source is still being processed in the background. You can:
1. Retry `source_add` with the same URL (it's idempotent on URL match)
2. Or `notebook_get` periodically until the source appears in the list
3. Or tell Scott to come back in a few minutes

## Error patterns

| What you see | What it means | Recovery |
|---|---|---|
| `notebook_list` returns `[]` | Auth expired | Run `nlm login` in terminal; retry |
| `notebook_get` returns 404 | Stale notebook ID | Re-list and re-match by title |
| `notebook_query` returns empty or refusing | Source content broke the query layer (long videos, code-heavy, sparse transcripts) | Fall back to `source_get_content` raw text + synthesize directly |
| `source_get_content` returns very short content | Video has no captions / no transcript | Use `source_describe` AI summary instead; note thin material in takeaways |
| `source_add(wait=True)` times out | Processing is slow | Retry with `wait_timeout=300`, or defer and revisit |

## Why this is better than the old Chrome path

- **No click coordinates.** No `(196, <row-y>)` guesses.
- **No DOM scraping.** No `document.querySelectorAll('.chat-message-pair')`.
- **Full titles.** The MCP returns untruncated source titles. The old `find` tool gave you truncated DOM text.
- **Scoped queries.** `source_ids=[<id>]` cleanly restricts the AI query. The old approach relied on prompt engineering and broke on similar source titles.
- **Synchronous API.** No "wait 30-45 seconds, then check the DOM."
- **Idempotent adds.** Re-running with the same URL doesn't duplicate the source.
- **Survives UI redesigns.** NotebookLM's web UI evolves; the API surface is stable.

A "review my notebook" run that took 4-6 minutes on Chrome MCP now runs in 60-90 seconds on native MCP. End-to-end with PDF + Drive upload usually under 3 minutes for a 5-video batch.
