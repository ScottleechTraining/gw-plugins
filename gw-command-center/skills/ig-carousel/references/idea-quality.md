# Idea Quality: gw-idea-quality-v1

Feeder F3, 2026-09-10. One grading sheet for every content idea, whatever door it came in. The seed writer applies it in the same pass that writes the angle. Code (`scripts/gwqueue/idea_quality.py`) validates ranges, arithmetic, and required reasons; it cannot check that a reason is true. Calibration record: `docs/superpowers/2026-09-10-feeder-f3-calibration.md`.

The problem it replaces: the old seed rubric scored revenue tie-in, voice fit, urgency, and ease. Daily-report rows got a default 14/20. Idea-mine rows mapped a discovery score onto /20 with a floor of 12. All three landed in one ranked queue as if they measured the same thing. A useful post with no offer under it lost to a catchy claim with a product name.

## Gates before scores

An idea is scored only after it passes every gate. A gate failure is recorded, never outscored.

| Gate | Pass means |
|---|---|
| audience+lesson | One intended coach and one coherent lesson are identifiable. |
| claims | The F2 claim boundary check leaves no unresolved central claim and no safety issue. |
| sources | Permitted material exists for the actual proposed teaching. External Library is provenance only; Scott's words are attributed as his. |
| duplicate | Not a confirmed duplicate. Token overlap alone is a warning for the semantic review, not a fail. |
| route | `forge`, `leech-letter`, `film-study`, or `manual`. Only `forge` enters the automatic queue. Leech Letter material never enters Forge because it scored well. |

Failure names: `needs-repair` (audience, claims, or sources), `duplicate`, `route-elsewhere`. These are assessment statuses, not queue statuses.

## Five dimensions, 0 to 4 each

Integers only. A 1 or a 3 is the explained middle between two anchors.

| Dimension | 0 | 2 | 4 |
|---|---|---|---|
| Coach relevance | No clear intended coach or need | A plausible problem for the named coach | A precisely described situation and its consequence for that coach |
| Decision specificity | Broad theme or slogan | Clear issue, choice still broad | One concrete choice or mistake the post can resolve |
| Reader payoff | Nothing usable beyond agreement | A clear takeaway that still needs explaining | A concrete next step, question, comparison, or reference the reader can use |
| Source support | Central teaching unsupported | Permitted material supports a narrower version | Locatable, permitted material supports the proposed lesson and its example |
| Moment of use | No credible use occasion | A recurring relevant need | A specific current or recurring decision point when this help lands |

Every score carries one reason tied to the actual idea. No invented customer quotes. A need the model inferred is labeled inferred, not demonstrated demand (F5 owns observed demand). A recurring planning problem can earn a 4 on moment of use; evergreen is not filler.

## Qualification and tie-breaks

- 15 to 20 with every dimension at least 2 and every gate passed: eligible for production selection.
- 11 to 14, or any dimension below 2: repair candidate. It is written up in the seed with what is missing and gets no Forge command, so it never becomes filler on an empty night.
- 0 to 10: not ready. Cut it.

Among qualifying ideas: total, then reader payoff, then source support, then oldest added. Scott's explicit picks keep their existing authority and still pass the source-safety checks. No action or topic quotas here; F7 owns the portfolio.

## Kept outside the total

- **Action proposal**: save, share, conversation, conversion, or unresolved. A proposal until Forge verifies feasibility.
- **Business connection**: a verified relevant offer, general trust or community relevance, or none. An excellent idea can carry none.
- **Effort**: low, medium, high. Operational information, never a reason to rank weak teaching above strong.
- **Voice**: a writing requirement, not points for a sensational hook.

A conversion request still needs a verified offer and a response path. Removing revenue from the score removes nothing from the offer checks.

## Seed block, exactly

Inside the angle block, replacing the old Scores lines. The harvester reads `**Rubric**`, `**Gates**`, the five score bullets, and `**Total: N/20**`; the legacy `score` field on the backlog row keeps working.

```markdown
**Rubric**: gw-idea-quality-v1
**Gates**: audience+lesson: pass | claims: pass | sources: pass | duplicate: pass | route: forge
**Scores** (0-4 each):
- Coach relevance: 4, <one reason tied to this idea>
- Decision specificity: 3, <reason>
- Reader payoff: 4, <reason>
- Source support: 2, <reason>
- Moment of use: 4, <reason>
- **Total: 17/20**
**Action proposal**: save
**Business connection**: none
**Effort**: low
```

The total must equal the sum. A block whose total, ranges, or reasons fail validation keeps its plain score on the row and records no assessment; the warning is visible in the idea context.

## Score provenance

Every /20 on the backlog is labeled by where it came from:

- `v1`: a valid `idea_assessment` under this rubric, tied to the idea context revision it scored.
- `legacy`: the old four-dimension seed total, a daily-report default 14/20 (the F1 context warns `score defaulted`), or an idea-mine discovery score mapped onto /20. These stay as history. They are never rescored, and they are never compared with a v1 total as if they meant the same thing.

## Shadow, then cutover

Switch: `Deliverables/_system/idea-quality-settings.json`, `{"ranking": "legacy"}` or `{"ranking": "gw-idea-quality-v1"}`. Scott's file. Absent means legacy. No command creates, edits, or deletes it.

- **Shadow (default now):** the picker ranks by legacy score. When any eligible row carries an assessment, the picks file and the job log print a `shadow v1` line with coverage and the v1 order of the assessed rows. Nothing selected changes.
- **Cutover:** the picker ranks by v1 only when every eligible pending row carries a valid, current assessment. One gap, one stale record, or one unknown rubric version and the entire run uses legacy order with a `v1 fallback` note. Never a mixed comparison. Known evidence or safety failures stay blocked either way.

Freebie rule: the nightly forge triggers a freebie at 18/20 under the legacy meaning. A v1 18 does not mean that. Until Scott approves a v1 freebie rule, every pick carrying a v1 assessment prints `freebie: hold` and gets no freebie; legacy picks keep the 18/20 rule. Proposed rule for approval: v1 total 17 or higher with reader payoff 4 and source support 3 or higher.

## Not in F3

No new idea generator, no portfolio quotas, no performance weights, no rescoring of the historical queue, no change to novelty thresholds or route rules.
