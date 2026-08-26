# Getting the Transcript

The transcript is where every quote and number in the takeaways comes from. No transcript, no gold. There are three ways to get one, in order of preference for the situation.

## Path 1: The manual copy (always works, zero installs)

This is the path to teach any user who does not have a browser tool connected. It takes about 30 seconds per video. Relay these exact steps:

1. Open the video on YouTube in your normal browser.
2. Below the video, click `...more` to expand the description.
3. Click **Show transcript**. A panel opens on the right.
4. Click the three-dot menu at the top of that panel and choose **Toggle timestamps** to turn timestamps off (optional, but makes a cleaner paste).
5. Click at the top of the transcript, scroll to the bottom, shift-click the end to select it all. Ctrl+A does NOT work here; it selects the whole page. Click the first line, then Shift+End or shift-click the last line.
6. Copy, come back to Claude, and paste it with the video title and creator name.

If the transcript panel is missing entirely, the video has no captions. See "No transcript" in the SKILL edge cases.

## Path 2: Browser tool extraction (when Claude in Chrome or similar is connected)

1. Navigate to the canonical URL only: `https://www.youtube.com/watch?v=<id>`. Strip `?t=`, `&t=`, `&list=`, and `&index=` parameters first; timestamps cause autoplay mid-video and playlist params load the wrong context.
2. Wait for the page to settle, then capture title, channel, duration, and view count from the page (a screenshot read is faster and more reliable than DOM selectors, which YouTube changes often).
3. Expand the description (`...more`). Pull chapter timestamps if present; for numbered-list videos ("5 Drills For X"), the chapters ARE the outline. Use them as the scaffold.
4. Find and click the **Show transcript** button. If two matches exist, try the one in the description area first.
5. Extract segments via JavaScript:

```javascript
const segs = document.querySelectorAll('ytd-transcript-segment-renderer');
let texts = [];
segs.forEach(s => {
  const t = s.querySelector('.segment-text, yt-formatted-string.segment-text');
  if (t) texts.push(t.innerText.trim());
});
texts.join(' ');
```

6. If zero segments come back: screenshot to check whether the panel opened; try the second Show transcript match; scroll the player into view; last resort, the three-dot menu in the description has a Show transcript item.

A 10-minute video yields roughly 8,000 characters; a 35-minute video can pass 30,000. Read long transcripts in 2,000 to 3,000 character chunks; never try to hold 30K characters in one pass.

## Path 3: NotebookLM (optional power path)

For users who stockpile videos as sources in a NotebookLM notebook. Requires a browser tool.

1. Open `https://notebooklm.google.com` and the named notebook.
2. For each video source, run a targeted chat query first: ask for the speaker's specific claims, numbers, and quotes on the video's topic. Chat output is quote-rich when it works.
3. If chat returns "The system was unable to answer" (common on 60+ minute videos), click the source title to open the source guide and pull the summary paragraph, then click the topic chips below the summary; each chip expands a focused, source-specific query.

## Handling a pasted pile of links

Users doing batch research often grab every link off a YouTube search results page at once with a link-grabber browser extension, then paste the whole pile. Expect noise: playlist URLs, channel URLs, Shorts, duplicates.

- Keep only `watch?v=` and `youtu.be/` URLs; normalize both to `https://www.youtube.com/watch?v=<id>`.
- Drop Shorts unless the user says otherwise; a 40-second clip rarely survives the 8-takeaway standard. Mention how many were dropped.
- Dedupe by video id.
- Present the cleaned, numbered list for confirmation before extracting anything. Extraction is the slow part; never spend it on videos the user did not mean to include.
