# Carousel Copy Record

Released in 0.21.0 on 2026-09-08; creation enabled the same night with Scott's approval. This is the single schema and copy-lifecycle contract for opted-in carousels. Archetype structures remain in [content-archetypes.md](content-archetypes.md); visual rules remain in [style-packs.md](style-packs.md).

## Opt-In and Capability Gate

From the Gridiron Warrior vault directory, check before opting in:

```bash
python -m scripts.gwqueue.carousel_copy --capabilities
```

Require support for schema 1, copy validation/export, copy-aware save/build/restyle/rewrite, and the managed package workflow before using them. Check installed helpers' help/capability output; a plugin version alone is not proof.

Capabilities report `enabled: false` by default. Creation is controlled by runtime `Deliverables/_system/carousel-copy-settings.json` with `{"enabled":true}`; an absent file means false. Scott enabled creation once on 2026-09-08. Never create, delete, or edit that settings file from a command; enabling or disabling is Scott's rollout decision. Once enabled, existing unattended Forge automatically creates copy records for NEW decks and passes them through `--copy`; no per-post opt-in question or nightly `--managed` argument.

The assembler's explicit `--copy` input or an existing embedded schema marker identifies new-format work; a brief or plugin update alone does not. Old unbuilt source packs without explicit new schema remain legacy, even after creation is enabled; discovery must not backfill copy records for that backlog. Disabling creation later does not disable validation, editing, restyles, or action rerolls for already-managed decks. No bulk migration and no changes to legacy decks. If helpers are missing, leave a managed topic pending with a clear capability error; never strip its marker or ship it unmanaged. Continue unrelated legacy overnight work through the existing path without failing the whole job or adding an unattended question.

## Schema 1

The saved HTML is the master. Embed exactly one `script#gw-carousel-copy[type=application/json]` record:

```json
{
  "schema_version": 1,
  "deck_id": "sample-carousel-1",
  "variant_id": "carousel-1",
  "source_pack": "sample-content-pack.md",
  "brief": {
    "audience": "High school football coach",
    "action": "save",
    "archetype": "System",
    "promise": "Build next week's plan",
    "takeaway": "Coordinate practice and lifting",
    "payoff": "A usable weekly checklist",
    "reason": "The reader needs this during weekly planning"
  },
  "slides": [
    {"id": "s01", "role": "cover", "fields": {"headline": "Plan the whole week"}},
    {"id": "s02", "role": "body", "fields": {"body": "Start with the practice schedule"}},
    {"id": "s03", "role": "cta", "fields": {}}
  ],
  "caption": "Build the plan around the week. Save this for Sunday.",
  "cta": {"action": "save", "text": "Save this for Sunday"}
}
```

This abbreviated example specifies the data shape, not a three-slide production template. All shown properties are required. Copy values are text strings, not HTML. `source_pack` is a basename, not a path, and must exist under the topic folder for caption splitting. Slide IDs are unique and stable; each `fields` object maps field names to text. Roles are `cover`, `body`, and `cta`; only the final slide has role `cta`. An empty final CTA slide fields object is valid because its ask lives in `cta.text`. Caption must be nonempty.

Allowed actions: `save`, `share`, `conversation`, `conversion`. `brief.action` and `cta.action` must match. Allowed archetype values: `System`, `Formula`, `Teardown`, `Vault`, `Template`, `Confession` (without "The"). Unknown schema versions, actions, archetypes, duplicate IDs, missing fields, invalid paths, extra bindings, or master/DOM disagreement fail validation.

Each physical `.slide` must carry `data-gw-slide` matching its record ID, in the same order as `slides`. Bind each slide copy field exactly once with a stable path such as `data-gw-copy="s01.headline"`. Bind the visible final ask with `data-gw-copy="cta.text"`; it is required, not a second slide-field copy of the CTA. The assembler appends the editable `caption` binding outside all `.slide` elements, so it never exports as a slide. Do not include a caption binding/editor in the skeleton. Keep copy bindings independent of style classes and preserve exact text and explicit newlines through edit/save/reopen.

## Brief Before Copy

For an opted-in Forge run, choose the action automatically before drafting any slides, including overnight. Explicit Scott instructions win. Otherwise choose by the feasible reader payoff:

- A usable artifact the coach will return to favors save. When save is chosen for a new deck or an explicit rewrite, [save-reference-slides.md](save-reference-slides.md) governs the reference body slide; it adds no schema field.
- Recipient-specific staff coordination favors share; name who needs it and why.
- A relevant response Scott can actually fulfill favors conversation. Do not promise an unavailable resource or impossible follow-up.
- A valid current offer plus buying intent favors conversion. Check the offer and current decisions; never force a sale because a default CTA names a product.

When more than one action fits, use recent new-format records only as a variety tie-break. No invented performance scores or rigid quotas. Record the audience, action, archetype, promise, takeaway, practical payoff, and reason before slide drafts. The builder honors this brief instead of selecting a different action or archetype. Use the archetype reference for teaching structure, but this action policy supersedes its legacy outcome ranking, conversation tie-break, and default CTA for opted-in decks. The chosen archetype shapes the body, caption, and CTA together; generic Forge seven-slide structure is fallback only. Unattended selection needs no confirmation gate.

## Build, Save, and Rebuild

### Initial handoff

For newly opted-in Forge output, finish both source-pack carousel variants and their voice/message gates, preserving the full asset set. Then automatically select the strongest variant without a question: prefer the one with the clearer fulfilled promise and usable payoff, stronger source support, and better audience/action fit. Explicit Scott selection wins; if both are equally strong, choose Carousel #1 as the deterministic tie-break. A variant failing a gate must be fixed before selection, not hidden by selecting the other.

Write exactly one `carousel-build.json` in the topic folder using schema 1 above. Its `variant_id` is `carousel-1` or `carousel-2`, matching the selected source-pack heading; its brief, ordered slides, caption, and CTA all come from that same variant. Set a stable `deck_id` and the existing `source_pack` basename. Do not combine one variant's slides with the other's caption or silently reselect during assembly. The JSON handoff freezes the initial choice for the builder.

Pass that file through `--copy` and produce only one selected HTML master for the topic. Both variants remain in the source pack, but the unselected variant does not become a second managed HTML master or posting caption. Once the HTML exists, its embedded record is authoritative: `carousel-build.json` is initial build input only, not a live master and not permission to overwrite saved HTML edits. Restyle/export/review use the saved HTML; action rewrites preserve its selected identity.

Run from the Gridiron Warrior vault directory, where the scripts module lives, not the checkout root. Positional skeleton/output/optional hero inputs remain compatible:

```bash
python -m scripts.gwqueue.carousel_copy validate PATH
python -m scripts.gwqueue.carousel_copy export PATH --output JSON
python -m scripts.gwqueue.build_carousel SKELETON OUT [HERO] [HERO2] --copy JSON
python -m scripts.gwqueue.build_carousel SKELETON OUT [HERO] [HERO2] --restyle-from EXISTING_HTML
python -m scripts.gwqueue.build_carousel SKELETON OUT [HERO] [HERO2] --rewrite-from EXISTING_HTML --copy NEW_JSON
```

Square brackets indicate optional positional inputs, not literal arguments. `--copy` creates the first new-format build. Export reads the explicit saved HTML PATH and refuses conflicting DOM; it does not select a deck or resolve topic ambiguity. The topic resolver handles ambiguous selection before a path is passed to export; never guess from the content pack. Exported JSON is a rebuild input, not a second live master.

The runtime assembler injects its copy-aware browser helper and Save Changes integration. Save captures bound slide text, caption, and CTA into escaped JSON before serializing. Use the helper, not a duplicated JavaScript implementation in a prompt. Validate, edit, save, reopen, then validate again before claiming persistence works.

Style-only changes use `--restyle-from`, preserving the complete saved record and exact wording, including caption and CTA. Reflow or resize text; do not shorten it to fit. Never reconstruct a restyle from the pack. An action POLISH note (`action: save`, `action: share`, `action: conversation`, or `action: conversion`, optionally followed by `. user note`) requires a new brief and a coordinated body/caption/CTA rewrite via `--rewrite-from ... --copy ...`. Retain `deck_id`, `variant_id`, and `source_pack`; this is the same deck, not a new identity. Run voice/message gates and require re-review. Never clear approval/polish state yourself or publish a reroll automatically.

For in-place replacements, the assembler renders and verifies the candidate before swapping it into the destination and backs up the old HTML by content hash. Use that replacement path rather than overwriting the live file yourself. A failed render or verification leaves the prior HTML in place; a successful replacement still requires a fresh review snapshot and approval before managed shipping. The backup is recovery history, not another selected master.

## Managed Posting Package

For new-format topics, prepare render + caption split before approval. Resolve the explicitly selected variant consistently across render, review, and split; show its actual paired caption, not both pack captions. Other channels stay unchanged.

The renderer writes `slides/.carousel-render.json` with the source HTML hash and PNG hashes. Package preflight requires that provenance to match the saved master and exact slide set, checks 1080x1350 dimensions and rejects blank slides, and checks the paired caption. File timestamps alone are not proof that PNGs came from the current master. Missing or stale provenance requires a fresh render, never a hand-edited proof. Render provenance is neither a review snapshot nor approval.

```bash
python -m scripts.gwqueue.carousel_package validate TOPIC
python -m scripts.gwqueue.carousel_package review TOPIC
```

`validate` checks current outputs read-only; it neither stages review nor approves. The `stage_review` operation, exposed by the `review TOPIC` CLI, snapshots exact current outputs to `carousel-review.json` and prints a Review token, NOT approval. Preserve that SHA256 token with the paired outputs shown to Scott. `build_review_page` generates the snapshot and binds its token to the managed deck and paired caption shown on that page.

Approval happens only through `apply_review`. Managed SHIP requires the emitted `review=[slug:SHA256TOKEN]` bucket alongside unchanged ship/polish/kill buckets. Preserve it exactly from the reviewed page; a stale browser tab's decision must not approve a newer snapshot. The applier passes the expected token to `approve_package(topic, expected_review_token)`, which requires a matching token for managed approval and rejects changed source HTML, ordered PNGs, or caption. Only then is approved `carousel-package.json` written. Relative paths survive the move to ready. Legacy paste format remains unchanged and does not require a token.

Direct `/gw-ship` must render/split, run `review TOPIC`, retain its printed Review token, and SHOW the paired outputs with that token to Scott. After approval (or his explicit approval of those exact unchanged outputs and their retained token), call `apply_review` with `ship=[slug] polish=[] kill=[] review=[slug:SHA256TOKEN]`. Substitute the original emitted token, never a token regenerated after the review. A general ship request is not approval of newly generated or changed outputs.

Do not create/edit either receipt by hand, replace a reviewed token with the latest token, or silently refresh a stale snapshot to reuse an old approval. Missing or mismatched tokens block managed SHIP. On a stale-review block, prepare and snapshot current outputs, show them again with their new token, and obtain renewed approval. State POLISH invalidates managed approvals and sets `ready_to_ship=false`; the builder cannot restore approval. Sync refuses missing or stale approval before uploading. Copy edits, action rerolls, or render changes require current outputs and renewed review/approval, not an unmanaged fallback. Legacy discovery and shipping remain unchanged.

Managed sync preflights the approved package before remote calls; a blocked topic must not trigger remote lookup, upload, or cleanup for that topic. After uploading the approved slide set, sync reconciles surplus remote PNGs only inside that managed topic's slide folder so an older, longer deck cannot leave extra posting slides. Non-PNG files and legacy slide folders are not part of this cleanup. Use the managed sync helper, not a manual or broad Drive cleanup; report any failure without claiming the topic shipped.
