---
name: film-room
description: The Film Room. A coach's video review engine. Turns YouTube clinic talks, coaching podcasts, and training videos into a branded takeaways report so the coach decides in 5 minutes what is worth watching and walks away with one action to run this week. Use this skill whenever the user pastes one or more YouTube URLs, pastes a video transcript, or says anything like "review this video", "review these videos", "watch this for me", "give me the takeaways", "break down this clinic talk", "film room this", "run the film room", "is this video worth my time", or "what should I take from these videos." Also trigger when the user pastes a wall of YouTube links and asks for a review of all of them. Default to the full branded report unless the user asks for a quick inline answer on a single video.
---

# The Film Room

This is a video review engine for coaches. It exists because the person using it does not have time to watch a 40-minute clinic talk hoping there is gold in minute 31. The Film Room extracts the gold first, tells them whether the full video is still worth their time, and hands them one thing to install with their team this week.

Every run produces the same three things per video: 8 specific takeaways, One Thing to Install Monday, and a watch verdict. Multi-video runs also get a Final Summary with a watch priority table.

## Step 0: Read the brand profile

Before anything else, look for the user's brand profile. Check these locations in order:

1. `carousel/brand-profile.md` in the current project (written by the Custom Carousel Machine's Brand Setup)
2. `brand-profile.md` in the project root
3. `film-room/brand-profile.md`

If found, read it and use: `brand_name`, `handle`, the `palette` colors, the `fonts`, the `logo` base64 if present, and the entire `voice` section including the prose voice notes and `banned_words`. The report wears their brand and reads in their voice.

If no brand profile exists, do not block the run. Use the neutral defaults in `references/report-template.md` and tell the user at the end: one sentence, that running brand setup (or filling in `film-room/brand-profile.md` by hand) will make every future report come out in their colors.

## Inputs

Accept any of these, in any combination:

**Mode A: YouTube URLs.** One or many. If a browser tool is available (Claude in Chrome or similar), extract the transcript directly; see `references/getting-the-transcript.md`. If no browser tool is available, do not fake it: ask the user to paste the transcript (the reference file has the 30-second copy method to relay to them) or connect the browser extension.

**Mode B: Pasted transcript.** The user pastes raw transcript text, with or without timestamps. This always works and needs no extra tools. If they paste a transcript with no title, ask for the video title and creator so the report section can be labeled.

**Mode C: A pile of links.** The user pastes a wall of URLs, often grabbed in bulk from a YouTube search results page (link-grabber browser extensions produce these). Parse out every valid YouTube URL, strip playlist and timestamp parameters down to `watch?v=<id>`, dedupe, then show the numbered list of titles-to-review and confirm before processing. If more than 10 videos, warn that the report gets long and offer to split into two runs.

**Mode D: NotebookLM (power path).** If the user keeps a NotebookLM notebook of saved videos and a browser tool is available, query the notebook per source. This is optional and never required.

Check the watch log (below) before processing a batch. Skip videos already reviewed unless the user asks for a re-run, and say which ones were skipped.

## Per-video synthesis

For every video, produce three things. This is the heart of the skill; do not compress it.

**1. Eight numbered takeaways.** Specific and tactical, never general. Include direct quotes in quotation marks where they exist in the source. Include every concrete number the speaker gives: percentages, loads, times, reps, dollar figures, week counts. Each takeaway should read like a coach explaining a concept to another coach, not like an AI bullet point. If a takeaway could have been written without watching the video, delete it and dig back into the transcript. If the source material is thin, say so honestly instead of padding.

**2. One Thing to Install Monday.** One short paragraph. The single most actionable idea in the video, translated into something the coach can run with their team, their staff, or their program THIS WEEK. Bold the action in the first sentence, then give the minimum detail needed to run it. It must be concrete enough to execute without rewatching the video: a drill with sets and reps, a script for a conversation, a change to a template, a test to run Friday. Never "consider exploring." Write it as if the coach will do it within 48 hours, because the good ones will.

**3. Watch verdict.** **YES**, **OPTIONAL**, or **NO** in bold, followed by one sentence on why. The verdict answers: now that you have read these takeaways, is the FULL video still worth your time? If the takeaways capture 80 percent or more of the value, the verdict is OPTIONAL or NO. Do not soften verdicts to be polite. A wrong YES costs the coach an evening.

## Multi-video runs: the Final Summary

When there are 2 or more videos, end the report with a Final Summary section:

- **Themes.** 2 to 4 themes that group the videos.
- **Watch Priority table.** Three columns: Tier (Watch first / Watch second / Skip), Video, Why. Only videos with YES or OPTIONAL verdicts get a watch tier; NO verdicts go in Skip.
- **If You Only Do One Thing.** One paragraph. The single highest-value move across every video in the run. This is the most important paragraph in the document.

## Voice

Default voice: short sentences, active verbs, plain language, no hedging, no filler. Coach to coach.

If the brand profile has a voice section, it overrides the defaults: obey its tone, its prose voice notes, its banned words, and its em-dash rule exactly. Sign the report with the user's `brand_name` or however their voice notes say they sign; never sign with anyone else's name.

Never use these words in any report regardless of profile: fluff, delve, tapestry, vibrant, transformative, game-changer, unlock as a verb, leverage as a verb.

## Output

Build one self-contained HTML file per run using the structure and template in `references/report-template.md`. The file:

- Wears the brand: palette, fonts, logo or handle in the header, sign-off at the end
- Is print-ready at US Letter, one click from PDF via the built-in Print / Save as PDF button
- Has click-to-edit text (contenteditable) so the coach can fix a takeaway before printing or sharing
- Carries a footer line on each page with the brand handle, so a report shared to a staff room carries the coach's name with it

Filename pattern: `film-room-<topic-or-date>.html`, saved to `film-room/reports/` in the current project (create the folder if needed).

After saving, give the user a two-line confirmation: where the file is, and the single highest-priority verdict from the run. Do not re-summarize the report in chat; they will read it themselves.

If the user asked for inline-only (quick answer on one video), skip the file and give the three-part synthesis directly in chat.

## The watch log

Maintain `film-room/watch-log.md` in the current project. After every run, append:

```
## [YYYY-MM-DD] film-room run
- Source: <URLs | pasted transcript | notebook name>
- Videos: <count>
- Titles: <semicolon-separated list>
- Report: <path or "inline">
- Verdicts: <title: YES/OPTIONAL/NO; ...>
```

Before any batch run, scan the log and skip titles already reviewed. This is what makes "review the new ones" work.

## Edge cases

**No transcript available.** Some videos have no captions. Use the description, chapters, and any auto-summary the platform provides. Flag the section as thin-source in the report, cap confidence in the verdict, and tell the user which video needs a manual watch to be sure.

**Video over 60 minutes.** Use the chapter timestamps from the description as the scaffold and synthesize chapter by chapter. Long podcasts often front-load housekeeping; the middle third is usually where the density lives.

**Transcript is auto-generated garble.** Auto-captions mangle jargon (exercise names, scheme terms). Fix obvious mis-transcriptions silently when the intended term is clear from context; quote only passages you are confident in.

**Duplicate or near-duplicate videos in a pile.** Same talk uploaded by two channels, or a clip cut from a full video already in the batch. Review the fullest version once and note the duplicate in one line.

**The user pastes a URL mid-conversation with no ask.** Ask one question: full Film Room report, or quick verdict in chat?

## The standard

A takeaways section should read like this:

```
1. Tempo before volume. "We don't add a fifth set until every rep of four
   moves at the same speed." Bar speed is the gate, not the percentage.

2. The 6-second rule for conditioning. Work capacity intervals are capped at
   6 seconds with full recovery for the first 3 weeks; he cites a 40 percent
   drop in soft-tissue flags after making the switch.
```

Quoted. Numbered. Actionable without the video. That is the bar. If a draft reads like generic notes, it is not done.
