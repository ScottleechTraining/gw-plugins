# Film Room - Ship Notes (Scott only, not in the zip)

status: draft-pending-scott (2026-08-19)

## What this is

Generalized gw-youtube-takeaways, packaged like the Custom Carousel Machine: a skills zip that course buyers drop into `.claude/skills/`. Second Brain bonus chapter drafted at `coach-second-brain-course/modules/bonus-the-film-room.md`.

## What changed from your version

- NotebookLM and Google Drive dependencies removed from the core path. NotebookLM demoted to optional power path. No Drive upload; report saves to `film-room/reports/` in the coach's project.
- reportlab PDF builder dropped. Output is now one self-contained HTML report with click-to-edit text and a Print / Save as PDF button, same pattern that made the Carousel Machine land. Zero Python deps, zero installs.
- "10x Move for GW" is now "One Thing to Install Monday": one bolded action the coach runs with their team this week.
- GW palette and Leech sign-off replaced by the buyer's brand profile. Reads the same `carousel/brand-profile.md` the Carousel Machine writes, including voice notes and banned words. Neutral defaults when absent.
- Run log generalized to `film-room/watch-log.md` in the coach's project.
- Link-pile mode is now a first-class input: parses a pasted wall of URLs (YouTube Link Grabber workflow), cleans, dedupes, drops Shorts, confirms before processing.

## Before you ship

1. Test on a clean machine or fresh project WITHOUT a brand profile: neutral defaults should render and the one-line brand-setup nudge should appear.
2. Test WITH your Carousel Machine brand profile: report should come out in brand, signed correctly, never as Leech.
3. Run one link-pile test: YouTube search, Link Grabber, paste 15+ links, confirm the clean-and-confirm step fires.
4. Run one no-transcript video to check the thin-source flagging.
5. Print one report to PDF from Chrome and check page breaks (video sections should not split headers).
6. Decide version string and rezip if you touch anything: `cd plugins/film-room && zip -r dist/film-room-v0.1.1.zip README.md skills/`
7. Chapter says "free with your Second Brain" and references the Carousel Machine bonus. If you plan to also sell Film Room standalone like the Carousel Machine, the chapter already supports that framing ("I sell it on its own" line is NOT in this draft; add it if true).

## Open decisions for you

- Name: "The Film Room" assumed. Alternatives considered: Clinic Notes Machine, The Watch List Killer.
- Standalone product or course-bonus only.
- Whether to add a `pack-author` style expansion later (custom report layouts). Skipped for v1; one great layout beats options.
