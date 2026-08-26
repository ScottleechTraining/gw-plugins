# The Film Room

A video review engine for coaches. Paste a YouTube link, a transcript, or a whole pile of links. Get back a branded, print-ready report: 8 specific takeaways per video, One Thing to Install Monday, and a straight watch-or-skip verdict. Decide in 5 minutes what deserves your evening.

Works with the brand profile from the Custom Carousel Machine. If you already ran brand setup, every Film Room report comes out in your colors, your fonts, your name, automatically.

## Install

1. Unzip this anywhere. Your Downloads folder is fine.
2. Open the `skills` folder inside it. You will see one folder: `film-room`.
3. Copy the `film-room` folder into your Claude skills folder.
   - Windows: `C:\Users\YOURNAME\.claude\skills\`
   - Mac: `~/.claude/skills/`
4. Restart Claude Code.

The `film-room` folder goes DIRECTLY into `skills`. When you are done you should have `.claude/skills/film-room/SKILL.md`. Do not drop this whole unzipped folder in there with `film-room` buried inside it. Claude Code only finds a skill at `.claude/skills/<name>/SKILL.md`.

## Use

Open Claude Code in your project and say:

```
film room this: <paste a YouTube link, several links, or a transcript>
```

That is the whole interface. First run in a project, Claude also creates `film-room/reports/` for your reports and `film-room/watch-log.md` so it never reviews the same video twice.

## No browser extension?

No problem. Open the video on YouTube, click `...more` under the video, click **Show transcript**, select the transcript text, copy, and paste it to Claude with the title. Thirty seconds. Claude will walk you through it the first time.

## What's in the box

```
skills/
  film-room/
    SKILL.md                          The engine
    references/
      getting-the-transcript.md      Three ways to get the source material
      report-template.md             The branded report your coaches will see
```
