# Feeder Evaluation

Feeder F8, 2026-09-10. After practice you review the film. Each week the synthesis run reviews what the feeder selected, what production had to fix, and what readers actually did, kept as three separate questions. It recommends at most one bounded change with the evidence behind it. Scott approves changes; one popular post never rewrites the playbook. Code: `scripts/gwqueue/feeder_eval.py`, read-only.

## What it reads

- Backlog rows: F1 idea context (id, revision), F3 assessment (total, family, assessed date), status and skip reasons.
- Packs dated inside the window: the `Idea origin:` and `Claim check:` receipt lines, the F4 `Teaching readiness:` lines, the F2 `claim-check.json` dispositions, and whether an approved package exists.
- The pilot ledger: planning slots (URL means published) and the collector's observation blocks.
- The settings file, to label which ranking and portfolio mode ran.

It never joins a post to an idea by title similarity. A pack joins to a row by the receipt's idea id, else by exact slug, else it is reported unmatched.

## Measures

Every measure shows numerator, denominator, and what was missing. Traceable handoffs, material-claim repair (over claim-checked packs only), missing-material and claim blocks, teaching-readiness outcomes, review revision burden (count of polish notes; minutes are not measured), selection coverage by lane and family, cohorts (legacy, v1-shadow, v1-active by the F3 cutover date), and delivery (selected, drafted, review-approved, verified published from ledger URLs). A folder is not a publication.

Audience measures use one primary-eligible observation per slot (inside the 156 to 180 hour window with reach observed; the latest such one). Rates are medians per 100 reached and are NA with fewer than two posts per action. Thread counts are the collector's heuristic. Qualified inquiries, completed actions, and production minutes stay hand-filled in the ledger and are not aggregated.

## The weekly section

Four lines in the synthesis report: what ran, what needed fixing, what readers did, and the coach's call. The call is one of keep, watch, repair, or one bounded proposed test with target, evidence, expected benefit, risk, review date, and reversal criterion. A week with no proposal is valid. Proposals need the skill-tune weight rule (two independent occurrences, or one now plus distinct earlier evidence); the same post in two reports is one occurrence. A serious correctness or privacy issue escalates for repair without waiting.

Proposals that touch score weights, source permissions, selector rules, or the pilot design follow their own gates. Skill-tune APPLY covers its allowlist only.

## Limits

Newly installed detectors find more; that is coverage, not deterioration. Missing edit history is not zero revisions. Shadow selections have no audience result. Several feeder changes launched in the same week are evaluated as one process. Withdrawn evidence is dropped and any recommendation built on it is flagged, never silently rewritten.
