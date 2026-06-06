# YouTube Extraction (Direct URL Mode)

How to pull title, metadata, and transcript from a YouTube video URL using the Claude in Chrome MCP. The transcript is the gold — it's where every direct quote and number in the takeaways comes from.

## Setup

1. Get a tab via `tabs_context_mcp` with `createIfEmpty: true`.
2. Navigate to the bare URL: strip `?t=` and `&t=` parameters first. Use `watch?v=<id>` only.
3. Wait 5 seconds for the page to settle.

## Get title, channel, length, view count

After the page loads, take a screenshot. The title appears below the player, the channel name and subscriber count are below the title, and the duration shows in the player as `0:00 / MM:SS`. View count and post date are in the metadata strip just below the title.

If you need these programmatically, the title is in `<h1 class="ytd-watch-metadata">`, the channel is the first `<a>` inside `ytd-channel-name`, and the view count is in `#info-container` text. But the screenshot read is faster and more reliable.

## Get the description

Scroll down 5 ticks. The description is collapsed by default with a `...more` link. Click `...more` to expand it. The expanded description often contains:

- Chapter timestamps (`00:00 - Introduction`, `01:10 - Single Graphic Page`, etc.)
- Links to related resources
- An AI-generated summary at the bottom labeled "AI-generated video summary"

For videos with a chapter list, the chapter timestamps ARE the structural outline of the content. Pull them. They're more reliable than guessing the structure from the transcript.

If the AI-generated summary is present, click its expand chevron to see the full text. It's a useful backup if the transcript is unavailable or thin.

## Get the transcript

The transcript is the main goal of this mode. Steps:

1. Use `find` with query `Show transcript button`. There are usually two refs returned (one in the description, one elsewhere). Try the description ref first.
2. Click it. Wait 3 seconds.
3. Extract via JavaScript:

```javascript
const segs = document.querySelectorAll('ytd-transcript-segment-renderer');
let texts = [];
segs.forEach(s => {
  const text = s.querySelector('.segment-text, yt-formatted-string.segment-text');
  if (text) texts.push(text.innerText.trim());
});
const full = texts.join(' ');
```

The result is one continuous string of transcript text without timestamps. Length varies — a 9-minute video produces ~8,000 characters, a 35-minute video can hit 30,000+.

For longer transcripts, slice the string in 2,000-3,000 character chunks for synthesis. Don't try to read 30K characters at once.

## When the transcript panel doesn't open

If the JavaScript returns 0 segments after the click:

1. Take a screenshot. Verify whether the transcript panel is visible on the right side of the player.
2. If not visible, the click missed. Try the second `Show transcript` ref from the find result.
3. If still not visible, scroll up so the player is in view (the transcript button is part of the player chrome).
4. As a last resort, click the `...` menu in the description and select "Show transcript" from the menu items.

## When the video has no transcript

Some videos lack auto-captions and have no manually uploaded transcript. The transcript button won't appear. In that case:

- Pull the description and chapters
- Pull the AI-generated summary if present
- Note in the takeaways section that the source material was thin
- Recommend Scott manually watch the video if the title and description suggest high value

## Title text patterns

Numbered list videos (e.g., "17 BEST Niches For X" or "5 Steps To Y") almost always have chapters in the description matching the list. Pull the chapter list as your scaffold and use the transcript to fill in details for each chapter.

How-to videos usually don't have chapters. Read the full transcript and identify the structural pivots yourself.

Long-form interview/podcast videos (60+ min) usually have chapters. Use them as the scaffold and synthesize per-chapter rather than trying to summarize the whole video.

## URL format

Always use the canonical form:
- `https://www.youtube.com/watch?v=<id>`

Avoid:
- `https://youtu.be/<id>` (sometimes redirects with extra params)
- `https://www.youtube.com/watch?v=<id>&t=120s` (autoplays at timestamp)
- `https://www.youtube.com/embed/<id>` (no description, no transcript UI)
