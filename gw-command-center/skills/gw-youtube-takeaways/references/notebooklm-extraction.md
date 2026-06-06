# NotebookLM Extraction

How to pull video content from a NotebookLM notebook using the Claude in Chrome MCP. Two methods — chat queries and source guides — and the right one depends on the video.

## Setup

1. Navigate to `https://notebooklm.google.com`. Wait 3 seconds.
2. Click the notebook tile (usually "Youtube Videos" — confirm the title in the screenshot).
3. The notebook opens with three panels: Sources (left), Chat (middle), Studio (right).
4. The source list shows truncated titles. Use `find` with the query "all source list buttons in left sources panel" to get full titles and refs.

## Method 1: Chat query (preferred for tactical, quote-rich output)

This produces the best takeaways because the chat extracts specific numbers and direct quotes. Use it first.

1. Find the chat input via `find` with query "chat input textarea query box". Usually returns a textarea ref like `ref_171`.
2. Set the value to a targeted query:

```
For the source titled "<exact source title>" ONLY, give me the 8 most important takeaways. Be specific and tactical, not general. Number them 1-8. Include direct quotes or specific numbers where possible. Do not pull from any other source.
```

3. Find the submit button via `find` with query "submit send button for chat query". Usually `ref_173`.
4. Click submit.
5. Wait 30-45 seconds. NotebookLM streams the response. Long videos take longer.
6. Extract the response via JavaScript:

```javascript
const pairs = document.querySelectorAll('.chat-message-pair');
const last = pairs[pairs.length - 1];
last.innerText.replace(/\n+/g, ' || ');
```

The response will start with the prompt text, then the takeaways separated by `||`. Citations appear as numbers in pipes. Strip them when synthesizing the takeaways.

## When chat fails

If after 60 seconds the response is the same length as the prompt (chat didn't run) OR you see "The system was unable to answer," fall back to the source guide method below.

Chat fails most often on:
- Videos longer than 60 minutes
- Videos with technical/code-heavy content (NotebookLM struggles to extract structured info)
- Videos with very long titles (sometimes the title match fails)

## Method 2: Source guide (reliable fallback)

The source guide is a per-source AI-generated summary that lives in the right panel when you click a source title. Less quote-rich than chat output but always works.

The click pattern is finicky:

1. Navigate fresh to the notebook URL (resets state).
2. Find the source button via `find` with query "<short title fragment> source button" — get the ref.
3. Click the ref. This sometimes deselects the checkbox.
4. Click the ref again. This sometimes re-selects.
5. Click on the title text coordinates (usually around `(196, <row-y>)` based on the source list scroll position) — THIS is what opens the source detail panel.

Confirm the panel opened by taking a screenshot. The right panel should now show:
- The source title at top
- A "Source guide" section with a paragraph summary
- Topic chips below the summary
- A video thumbnail at the bottom

Extract the paragraph summary via JavaScript:

```javascript
const els = document.querySelectorAll('p');
let result = '';
for (const e of els) {
  if (e.innerText && e.innerText.length > 300 && e.innerText.length < 5000 &&
      !e.innerText.startsWith('For the source') &&
      !e.innerText.startsWith('These sources') &&
      !e.innerText.startsWith('Looking at')) {
    result = e.innerText;
    break;
  }
}
result;
```

The filters skip past the chat prompts and any notebook-wide overviews to land on the source-specific summary.

## When the source guide is generic

If the extracted paragraph starts with "These sources..." instead of being source-specific (e.g., "Tom Youngs argues that..." or "In this transcript, the speaker..."), the click sequence didn't fully open the detail panel. Take a screenshot to verify. If the source list is showing instead of the detail panel, the click missed.

Recover by:
1. Clicking the source title text again at the highlighted row coordinates
2. Or clicking on a topic chip (e.g., "AI infrastructure systems") below the source guide summary, which expands a focused query in the chat that returns source-specific content

## Skipping already-reviewed videos

For "review the new videos in my notebook" requests:

1. Read `D:\Claude Projects\Gridiron Warrior\wiki\log.md` (or similar log if the project structure differs).
2. Scan the most recent ingest entries for video titles already covered.
3. After listing all current sources in the notebook, filter out the matches.
4. Review only the remaining new ones.

If the notebook has 21 sources and 8 are already in the log, you should review 13. Mention this in the cover-page subtitle: "13 NEW videos beyond the original 8."

## Source ordering

NotebookLM displays sources alphabetically by default. The `find` tool returns them in DOM order which matches the alphabetical list. Don't reorder them in the PDF — Scott navigates the notebook alphabetically too.

## Resetting between extractions

Some click sequences leave the source detail panel open. Before extracting the next video, navigate fresh to the notebook URL:

```javascript
navigate(url='https://notebooklm.google.com/notebook/<notebook-id>')
```

Then wait 4 seconds for the source list to repopulate. Trying to switch between sources without resetting often fails because the click handlers are inconsistent.
