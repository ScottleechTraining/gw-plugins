# Portfolio Selection

Feeder F7, 2026-09-10. Three good drills do not make a good practice if they all train the same thing. Among similarly strong ideas, the nightly picker can prefer ones that help coaches with different decisions. This is a small preference after every existing gate: not a quota, not a score, not a content strategy. Code: `scripts/gwqueue/portfolio_select.py`, policy id `gw-portfolio-v1`.

## Mode

Scott's switch, key `portfolio` in `Deliverables/_system/idea-quality-settings.json`: `shadow` (default, also when the file is absent), `active`, or `off`. No command edits that file.

- **Shadow.** The picker computes the recommendation and writes a receipt to `Deliverables/_system/portfolio-shadow-<date>.md`. The picks file does not change. That receipt is never a pick list; the nightly agent forges only what the picks file lists.
- **Active.** The recommendation becomes the pick order, but only on a run where the v1 ranking actually ran (every eligible row assessed and current). Under legacy ranking or a v1 fallback the picker says `portfolio: unavailable` and uses baseline order, because unlike scores cannot be compared.
- **Pilot.** The twelve-post pilot is in Block A and B planning. F7 stays in shadow while that selection policy is frozen. Activation waits for the next approved comparison batch or Scott's explicit prospective amendment that names the slots it affects. No pilot post is relabeled as an F7 selection.

## Family vocabulary

A coaching-decision family is recorded by the seed writer in the v1 block as `**Family**:` from this list, and only this list: in-season load, conditioning, session design, monitoring and standards, practice planning, staff coordination, speed and acceleration, strength technique, nutrition and recovery, culture and leadership, contact prep, business and fundraising. Anything else is recorded as unknown with a warning. Unknown never earns a preference. Families are not inferred from title words.

## Policy

1. Explicit Scott picks (source `scott-pick ...`) keep their place first. Quality and safety gates still apply to them.
2. Candidates are the rows the picker already found eligible, ranked, and qualifying under gw-idea-quality-v1, in that order.
3. For each slot the best remaining total sets the bar. Alternatives within one point of it are the band. The band is recomputed every slot, so the tolerance never compounds.
4. Within the band, prefer a family not yet selected in this run.
5. Still tied: prefer the family least represented in recent production history (at most the six most recent forged rows that carry a family, one row per topic; variants and rerolls are one identity), then higher total, then older added, then slug.
6. Repeat up to the existing maximum. The output ceiling never grows for variety.

If only one family has qualifying ideas, selection proceeds normally. Nothing is invented, relabeled, or reached for below the band. An unselected idea stays pending with no status change. Novelty gating and the nightly semantic rescue run exactly as before, on whichever order is in force; the receipt records the actual picks after the gate beside the recommendation.

## Receipt

Production notes only, in the `_system` file: mode and policy, baseline order, recommended order, explicit picks kept first, rows with unknown family, the history families used (labeled production history, never audience history) or the disclosure that only within-batch diversity was considered, and each swap with both slugs, both families, both scores, and a plain reason. Nothing from it goes on a slide or into the queue.

## Calibration

The one-point band, the family list, and the reasons are a proposal for Scott to review in shadow. Change them in this reference and in the code together; do not tune them in one command.
