# Report Template

One self-contained HTML file per run. No external requests except Google Fonts (and skip even that when the brand profile bakes fonts as base64). Everything below the substitution table is the template; fill the `{{TOKENS}}`, repeat the video section block per video, and delete the summary block on single-video runs.

## Substitutions

| Token | Source |
|---|---|
| `{{BRAND_NAME}}` | brand profile `brand_name`, else "Film Room" |
| `{{HANDLE}}` | brand profile `handle`, else empty |
| `{{INK}}` `{{PAPER}}` `{{DARK}}` `{{ACCENT}}` `{{ACCENT2}}` | brand profile palette: ink, paper, dark, accent_primary, accent_secondary. Neutral defaults: `#222222`, `#FAFAF7`, `#222222`, `#4A7A96`, `#555555` |
| `{{DISPLAY_FONT}}` `{{BODY_FONT}}` | brand profile fonts. Defaults: Roboto Slab, Barlow |
| `{{FONT_LINK}}` | Google Fonts `<link>` for the two families, or empty + `@font-face` blocks when fonts are baked |
| `{{LOGO_BLOCK}}` | `<img class="logo" src="data:image/png;base64,..." alt="...">` when the profile has a logo, else `<div class="handle-mark">{{HANDLE}}</div>` |
| `{{TITLE}}` | Report title, e.g. "Film Room: Tempo Conditioning" |
| `{{DATE_SOURCE}}` | e.g. "August 19, 2026 · 6 videos · reviewed from transcripts" |
| `{{INTRO}}` | 2-3 sentence cover paragraph: what was reviewed and what the reader gets |
| `{{SIGNOFF}}` | Per brand voice notes; else "— {{BRAND_NAME}}" |

Verdict badge classes: `v-yes`, `v-opt`, `v-no`.

## Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{TITLE}}</title>
{{FONT_LINK}}
<style>
  :root{
    --ink:{{INK}}; --paper:{{PAPER}}; --dark:{{DARK}};
    --accent:{{ACCENT}}; --accent2:{{ACCENT2}};
    --display:'{{DISPLAY_FONT}}',serif; --body:'{{BODY_FONT}}',sans-serif;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:#e8e8e6;font-family:var(--body);color:var(--ink)}
  .toolbar{position:sticky;top:0;z-index:10;background:var(--dark);color:#fff;
    display:flex;gap:12px;align-items:center;padding:10px 18px;font-size:14px}
  .toolbar button{background:var(--accent);color:#fff;border:none;padding:8px 16px;
    border-radius:4px;font-family:var(--body);font-size:14px;cursor:pointer}
  .toolbar .hint{opacity:.7}
  .page{background:var(--paper);max-width:8.5in;margin:24px auto;padding:.9in .8in;
    box-shadow:0 2px 14px rgba(0,0,0,.18)}
  .brandbar{display:flex;justify-content:space-between;align-items:center;
    border-bottom:3px solid var(--ink);padding-bottom:14px;margin-bottom:28px}
  .logo{max-height:44px}
  .handle-mark{font-family:var(--display);font-weight:700;font-size:18px}
  .brandbar .tag{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent2)}
  h1{font-family:var(--display);font-size:34px;line-height:1.15;margin-bottom:6px}
  .meta{color:var(--accent2);font-size:13px;margin-bottom:18px}
  .intro{font-size:15px;line-height:1.5;max-width:60ch}
  .video{margin-top:34px;padding-top:6px;border-top:1px solid rgba(0,0,0,.12)}
  .video h2{font-family:var(--display);font-size:20px;color:var(--accent);margin-bottom:2px}
  .creator{font-size:12.5px;font-style:italic;color:var(--accent2);margin-bottom:12px}
  .label{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
    color:var(--ink);margin:14px 0 6px}
  ol.takes{padding-left:22px;font-size:14px;line-height:1.5}
  ol.takes li{margin-bottom:7px}
  .monday{background:color-mix(in srgb,var(--accent) 9%,var(--paper));
    border-left:4px solid var(--accent);padding:12px 14px;font-size:14px;line-height:1.5}
  .verdict{font-size:14px;display:flex;gap:10px;align-items:baseline}
  .badge{font-weight:800;font-size:12px;letter-spacing:.08em;padding:3px 10px;border-radius:3px;color:#fff}
  .v-yes{background:#1f7a33}.v-opt{background:#b07d10}.v-no{background:#9e2020}
  .summary h2{font-family:var(--display);font-size:26px;margin-bottom:14px}
  table{width:100%;border-collapse:collapse;font-size:13.5px;margin:8px 0 18px}
  th{background:var(--dark);color:#fff;text-align:left;padding:8px 10px;font-size:12px;
    letter-spacing:.08em;text-transform:uppercase}
  td{padding:8px 10px;vertical-align:top;border-bottom:1px solid rgba(0,0,0,.1)}
  tr:nth-child(even) td{background:rgba(0,0,0,.03)}
  .onething{border:2px solid var(--ink);padding:16px 18px;font-size:15px;line-height:1.55}
  .onething .label{margin-top:0}
  .signoff{margin-top:30px;font-family:var(--display);font-size:16px;white-space:pre-line}
  .foot{margin-top:26px;padding-top:10px;border-top:1px solid rgba(0,0,0,.15);
    font-size:11px;color:var(--accent2);display:flex;justify-content:space-between}
  [contenteditable]:hover{outline:1px dashed var(--accent);outline-offset:2px}
  [contenteditable]:focus{outline:2px solid var(--accent);outline-offset:2px;background:rgba(255,255,255,.6)}
  @media print{
    .toolbar{display:none}
    body{background:#fff}
    .page{box-shadow:none;margin:0;max-width:none;padding:.6in .7in}
    .video{break-inside:avoid}
    .summary{break-before:page}
    @page{size:letter;margin:0}
  }
</style>
</head>
<body>
<div class="toolbar">
  <button onclick="window.print()">Print / Save as PDF</button>
  <span class="hint">Click any text in the report to edit it before you print or share.</span>
</div>

<div class="page">
  <div class="brandbar">
    {{LOGO_BLOCK}}
    <div class="tag">Film Room Report</div>
  </div>

  <h1 contenteditable="true">{{TITLE}}</h1>
  <div class="meta" contenteditable="true">{{DATE_SOURCE}}</div>
  <p class="intro" contenteditable="true">{{INTRO}}</p>

  <!-- REPEAT PER VIDEO -->
  <section class="video">
    <h2 contenteditable="true">Video 1: {{VIDEO_TITLE}}</h2>
    <div class="creator" contenteditable="true">{{CREATOR}} · {{DURATION}}</div>
    <div class="label">Takeaways</div>
    <ol class="takes" contenteditable="true">
      <li>{{TAKEAWAY_1}}</li>
      <!-- ... 8 total -->
    </ol>
    <div class="label">One Thing to Install Monday</div>
    <div class="monday" contenteditable="true"><strong>{{ACTION}}.</strong> {{DETAIL}}</div>
    <div class="label">Watch the full video?</div>
    <div class="verdict"><span class="badge v-yes">YES</span>
      <span contenteditable="true">{{ONE_SENTENCE_WHY}}</span></div>
  </section>
  <!-- END REPEAT -->

  <!-- MULTI-VIDEO RUNS ONLY -->
  <section class="summary">
    <h2>Final Summary</h2>
    <div class="label">Themes</div>
    <p class="intro" contenteditable="true">{{THEMES}}</p>
    <div class="label">Watch Priority</div>
    <table>
      <tr><th>Tier</th><th>Video</th><th>Why</th></tr>
      <tr><td>Watch first</td><td contenteditable="true">{{V}}</td><td contenteditable="true">{{WHY}}</td></tr>
    </table>
    <div class="onething">
      <div class="label">If You Only Do One Thing</div>
      <span contenteditable="true">{{CROSS_VIDEO_MOVE}}</span>
    </div>
  </section>
  <!-- END MULTI-VIDEO -->

  <div class="signoff" contenteditable="true">{{SIGNOFF}}</div>
  <div class="foot"><span>{{BRAND_NAME}}</span><span>{{HANDLE}}</span></div>
</div>
</body>
</html>
```

## Rules

- Keep every `contenteditable` attribute; click-to-edit before printing is a core feature, same as the Carousel Machine.
- One `.page` div total; the print stylesheet handles pagination. `break-inside:avoid` on `.video` keeps a video's header from orphaning at a page bottom.
- `color-mix` needs a modern browser; if the accent is very dark, verify the `.monday` box still reads. When in doubt hardcode a light tint of the accent.
- No Unicode sub/superscripts anywhere; spell them out.
- On thin-source videos, add `(thin source: no transcript available)` in the creator line so the reader knows the confidence level.
- Never put anyone else's brand, name, or sign-off in the output. The report belongs to the user.
