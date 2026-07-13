---
name: gw-youtube-takeaways
description: "Scott Leech's video review and takeaway engine for Gridiron Warrior. Extracts content from YouTube videos or NotebookLM notebooks via the native notebooklm MCP, generates 8 specific takeaways per video plus one 10x business insight tied to GW (Insiders, DFY, Courses, Summit), gives a watch verdict per video, and produces a GW-branded PDF saved to C:\\Claude Projects\\Gridiron Warrior AND uploaded to Google Drive. Use this skill aggressively whenever Scott pastes one or more YouTube URLs, says 'review this video', 'review these videos', 'watch this for me', 'give me the takeaways', 'review my notebook', 'review the new videos in my notebook', 'build a video PDF', 'summarize these videos for the business', or asks any variant of 'what should I take from these videos.' Also trigger on 'review the youtube videos notebook' or any reference to a NotebookLM notebook full of video sources. Default to the full PDF + Drive upload workflow unless Scott explicitly asks for inline-only review."
---

# GW Video Takeaways

Scott's video review engine. Turns YouTube content into per-video takeaways, business-applied 10x insights, and a GW-branded PDF saved locally and to Google Drive.

Scott uses this for two reasons. One: he runs a NotebookLM notebook called "Youtube Videos" where he stockpiles videos he hasn't watched yet, and he needs them filtered through a coach-and-business lens before deciding which to actually watch. Two: he sometimes pastes raw YouTube URLs and wants the same treatment on the spot.

The skill exists because Scott's working window is 8pm to sleep, and he doesn't have time to watch 30+ minute videos hoping for the gold. He needs Claude to extract the gold first.

**v0.3.0 change:** This skill now uses the native `mcp__notebooklm__*` MCP server. The previous Chrome-MCP DOM-scraping flow is archived as a fallback only.

## Triggers

Run this skill when Scott:
- Pastes one or more YouTube URLs and asks anything that implies "review" or "summarize"
- Says "review my notebook," "review the youtube videos notebook," "do the video review thing again"
- Says "review the new videos" (means: pull the notebook, skip videos already in the log, review the rest)
- Asks for "takeaways," "8 takeaways," "what should I take from this," "watch verdict"
- Mentions a NotebookLM notebook by name in a context that implies content extraction

If Scott pastes 1 or 2 URLs and seems to want a quick answer in chat, ask whether he wants the full PDF treatment or inline-only. Default to PDF if there are 3+ videos or if the source is a full notebook.

## Inputs (3 modes)

**Mode A — NotebookLM notebook.** Scott references a notebook (usually "Youtube Videos"). Use `mcp__notebooklm__notebook_list` to find it by title, get its sources via `mcp__notebooklm__notebook_get`, filter out titles already in the run log, then extract content for each remaining source.

**Mode B — Raw YouTube URLs.** Scott pastes one or more URLs. Add them to the "Youtube Videos" notebook via `mcp__notebooklm__source_add` with `source_type="url"` and `wait=True`. NotebookLM handles the YouTube transcript extraction natively — no DOM scraping. Then proceed exactly as Mode A.

**Mode C — Mixed.** Scott pastes URLs AND mentions a notebook. Add the new URLs to the notebook (Mode B path), then extract all relevant sources (Mode A path). Each video becomes a separate entry in the final PDF.

Each video gets the same synthesis treatment regardless of source mode.

## Per-video extraction (native MCP path)

This replaces the old Chrome-MCP click sequences. The full extraction guide lives in `references/notebooklm-extraction.md`.

The short version:

```
1. notebook_list()                                          → find "Youtube Videos" by title match
2. notebook_get(notebook_id)                                → list of sources with IDs + titles
3. (Mode B/C only) source_add(notebook_id, source_type="url", urls=[...], wait=True)
                                                            → wait for NotebookLM to process the YouTube transcript
4. For each source to review:
   a. source_get_content(source_id)                         → raw transcript text (fast, no AI)
   b. notebook_query(notebook_id, query="8 tactical takeaways from this video...", source_ids=[source_id])
                                                            → quote-rich, source-scoped takeaways
   c. (Optional) source_describe(source_id)                 → keyword chips for theme grouping
```

Per-video synthesis input: combine raw transcript (from `source_get_content`) + AI takeaways (from `notebook_query`). The transcript gives you exact quotes and numbers; the AI query gives you structure. Don't skip either.

For the per-source `notebook_query`, use this prompt template verbatim:

```
For the source titled "<exact source title>" ONLY, give me the 8 most important takeaways for a strength and conditioning coach who is also a business owner. Be specific and tactical, not general. Number them 1-8. Include direct quotes in quotation marks where they exist. Include numbers (dollar amounts, follower counts, percentages, time costs) where they appear. Do not pull from any other source.
```

The `source_ids=[source_id]` parameter scopes the query to one source — far more reliable than the old "Be careful not to pull from other sources" prompt-engineering trick.

## Per-video synthesis

For every video, produce three things:

**1. 8 numbered takeaways.** Specific and tactical, not general. Include direct quotes in quotation marks where they exist. Include numbers (dollar figures, follower counts, time costs, percentages) where they appear in the source. Each takeaway should read like a coach explaining a concept, not like a generic AI bullet point. If you find yourself writing "leverage AI to optimize content workflows," delete it and write what the speaker actually said.

**2. The 10x Move for GW.** One paragraph. Tie the video's content directly to one of Scott's revenue priorities, in this order: (a) Gridiron Warrior Insiders community ($29/mo, target 30→100+), (b) DFY team programming ($500/mo, target 5+ clients), (c) Course sales volume, (d) GW Summer Summit (July 18, 2026 at URI, target 75-100 registrations). Bold the headline action at the start. The 10x must be specific enough to act on tonight — not "you could explore X." Write it as if Scott will execute it within 48 hours.

**3. Watch verdict.** "YES," "OPTIONAL," or "NO" in bold, followed by a single sentence on why. The verdict measures whether the FULL video is worth Scott's time given that he just read your takeaways. If the takeaways capture 80%+ of the value, the verdict is OPTIONAL or NO.

## Voice

Write in Scott's external voice. Short sentences. Active verbs. Plain language. Tough love. Coach in the trenches.

Banned words: fluff, delve, tapestry, vibrant, transformative, unlock as a verb, leverage as a verb, game-changer.

No em-dashes, ever. Use periods, semicolons, or colons.

## PDF structure

Build the PDF with `scripts/build_pdf.py` (a parameterized reportlab template). Don't write a custom builder per run — feed the script a JSON payload of videos and it produces the PDF.

The structure:

1. **Cover page.** Title in GW Black, subtitle in GW Gray with date and source. One short intro paragraph explaining what's in the report.

2. **Per-video sections.** For each video: red header with "Video N: <title>", italic gray subheader with creator name, a Takeaways section with 8 numbered items, a "10x Move for GW" section with the insight in a cream-colored callout box, and a "Watch the full video?" section with the verdict.

3. **Final Summary page.** Always on a new page. Includes:
   - **Themes.** 2-4 themes that group the videos. Use keyword chips from `source_describe` to seed these.
   - **Watch Priority table.** Three columns: Tier ("Watch first," "Watch second," "Optional"), Video, Why. Black header row, alternating cream and white rows.
   - **Highest-Leverage Move Across All Videos.** One paragraph synthesizing the cross-video play. This is the most important section in the document — it's the answer to "if Scott can only do one thing from all this, what's the move?"

4. **Sign-off.** "Keep the Fire Burning, / Leech"

## Brand palette

Hard-coded colors:
- GW Red `#9E1B1B` for video headers
- GW Black `#111111` for title text and table header
- GW Gray `#3A3A3A` for subtitles and metadata
- GW Light Cream `#F2EFEA` for the 10x callout box and alternating table rows

Helvetica family throughout. No Unicode subscripts/superscripts — those render as black boxes in reportlab. Use `<sub>` and `<super>` tags inside Paragraph objects instead.

## Output files

Two outputs every run, no exceptions unless Scott explicitly asks for inline-only:

1. **Local file** at `C:\Claude Projects\Gridiron Warrior\<filename>.pdf`. Filename pattern: `Youtube_Videos_Notebook_Takeaways_<descriptor>.pdf` where descriptor is either a version (`v1`, `v2`, etc.) or a date (`2026-05-02`) or a topic if Scott specified one.

2. **Google Drive root.** Use `mcp__e432adf7-cb86-45a0-a515-5c44c49c2b8d__create_file` with `contentMimeType: application/pdf` and the file content as `base64Content`. To produce the base64 string from the local PDF, run `base64 -w 0 <path>` in bash. Don't include `parentId` — that puts the file in My Drive root.

After both saves, give Scott a short confirmation message with two links:
- A `computer://` link to the local file
- A `https://drive.google.com/file/d/<id>/view` link from the create_file response

Keep the post-amble short. Scott reads the PDF himself.

## Run log

To support the "review the new videos" pattern (skip what we've already done), maintain a log at `C:\Claude Projects\Gridiron Warrior\wiki\log.md` per the project CLAUDE.md convention.

After every run, append an entry:

```
## [YYYY-MM-DD] ingest | youtube-takeaways v<N>
- Source: <notebook name or "direct URLs">
- Videos reviewed: <count>
- Titles: <semicolon-separated list>
- PDF: <local path>
- Drive: <drive URL>
```

Before a notebook run, scan recent log entries to identify titles already covered. Skip those, review only the new ones, and mention in the cover-page subtitle which previous run this builds on.

## Edge cases

**Notebook not found by title.** If `notebook_list()` returns no notebook matching "Youtube Videos" (case-insensitive), tell Scott the notebook name. Don't auto-create — Scott manages his notebook layout deliberately.

**`source_add` with `wait=True` times out.** Default timeout is 120s. For very long videos NotebookLM can take longer to index the transcript. Retry once with `wait_timeout=300`. If it still times out, add without waiting and tell Scott to come back in a few minutes; the source will be ready on the next run.

**`notebook_query` returns an empty or refusing answer.** Some videos break the query layer (very long videos, code-heavy content, or sparse transcripts). Fall back to using `source_get_content` raw text and synthesize the takeaways directly from the transcript yourself. Note "synthesized from raw transcript" in the takeaway intro line so Scott knows the difference.

**Source has no extractable transcript.** YouTube videos without captions return short or empty content from `source_get_content`. Note this in the takeaways section ("transcript unavailable; based on title and source guide"), use `source_describe` for the AI summary, and rate the video 5/10 confidence in the watch verdict. Recommend manual watch if the title suggests high value.

**Scott pasted a URL with `?t=` or other tracking parameters.** Strip query params before passing to `source_add` — use the bare `watch?v=<id>` form. NotebookLM handles canonicalization but cleaner URLs in the source list make Scott's notebook easier to browse.

**More than 15 videos in a single run.** Ask Scott if he wants to split into two PDFs (videos 1-N and N-end) for readability. Otherwise the priority table at the end gets cramped.

**Scott wants raw URLs reviewed without adding to his notebook.** Default behavior is to add them to "Youtube Videos" since that's his stockpile and it keeps the workflow seamless. If Scott explicitly says "don't add it to my notebook," create a one-shot temporary notebook via `notebook_create(name="GW Review Scratch <date>")`, do the extraction there, and `notebook_delete(notebook_id)` it after the PDF ships. Confirm with Scott before deleting.

## Format example

For a video on coaching offer pricing, the Takeaways section should read like this — not generic motivational filler:

```
Takeaways

1. Hybrid pricing model. Charges "$4k onboarding + $900/month for 5 months" = $8.5K total. Front-loaded cash AND "juicy 900 a month from the back end."

2. Regional exclusivity drives retention. "One videographer per area" (towns of 150K-250K). Result: 85% continuation rate.

3. Close high-ticket via DMs, no sales calls. Generated "$120K in 60 days with less than $1,000 ad spend and no sales calls" using voice notes plus a Stripe link.
```

Specific. Quoted. Numbered. The reader can act on these. That's the standard.

## Why this matters

Scott's working time is 30-60 minutes per night. The wrong video eats two of those nights. This skill exists so he can decide in 5 minutes what's worth watching and what's not, and walk away with at least one move he can ship before bed regardless.

Don't soften the watch verdicts to be polite. If a video isn't worth his time given what's already in the takeaways, say NO.

## Legacy fallback

If the `mcp__notebooklm__*` MCP server is unavailable in a session (auth expired, server disconnected, or transient failure), the Chrome-MCP DOM-scraping path documented in `references/youtube-extraction.md` still works as a fallback. It's brittle (click coordinates, JavaScript injection, 60s waits) but functional.

Default path is always native MCP. Only fall through if MCP is hard down.
