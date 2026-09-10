# Rhetorical Approaches (roadmap idea 5)

Installed in plugin 0.24.0 (2026-09-09). Editorial reference for opted-in decks: Forge chooses one of six teaching progressions after the action and before drafting, and records it in `brief.reason`. This changes how a new draft teaches, not its visual style, the canonical archetype taxonomy in [content-archetypes.md](content-archetypes.md), or the schema. Style-only rebuilds and legacy decks never apply it.

## Six Approaches

| Approach | Use when the source contains | Body progression | Avoid |
|---|---|---|---|
| Observation | A specific recurring situation | Scene, overlooked detail, significance, practical response | Inventing a witnessed scene |
| Demonstration | A process that can be shown | Inputs, worked steps, output, usable rule | Unsupported numbers or outcomes |
| Decision guide | A real choice with meaningful conditions | Choice, distinguishing question, conditions, next step | Universal prescriptions from one example |
| Correction | A documented misconception or explicit limitation | State the assumption fairly, show its limit, replace it with a better rule | Inventing an opponent or declaring everyone wrong |
| Comparison | Two source-supported alternatives | Hold context constant, compare one dimension, explain the trade-off | Straw-man before/after stories |
| Personal lesson | Scott's own attributable experience and reflection | What happened, what he noticed, what changed, lesson | Fabricated first-person memories or admissions |

## Automatic Selection

After selecting the primary action and before drafting, choose the approach best supported by the actual source. Action determines the desired reader behavior; archetype determines the broad content structure; this approach determines how the argument unfolds. Style remains a separate visual decision.

Keep the existing archetype and output contracts. Do not create six new archetypes or force every approach into every archetype. If the selected structure and approach conflict, choose another compatible approach rather than silently overriding the agreed brief.

Use at most the six most recent available new-format drafts as a variety tie-break, not as a mandatory quota or performance score. Compare the body progression, not just hook words. If recent history is unavailable, choose on source fit and continue without an extra question. Do not scan the whole archive just to choose a rhetorical approach. In GW terms: read the `brief.reason` of at most six managed decks found by `python -m scripts.gwqueue.carousel_copy validate` on recent `Deliverables/_inbox` and `ready` topics, or skip the tie-break entirely if that takes more than a minute. The two variants of one content pack should use different approaches when the source supports two; they are alternatives, never two queue entries.

Record the choice and source reason in the existing brief.reason field, in the form `approach: <name>; <why the source supports it>` followed by the action reason. No schema extension or duplicate metadata store is needed. Explicit Scott direction wins. Style-only rebuilds preserve saved copy and never retrofit this module. Explicit action rewrites may change the approach when needed and still require fresh review.

## Rewrite Test

Changing 'Stop doing X' to 'Here are three ways to do X' while keeping the same accusation and body is not meaningful variety. At least the teaching progression must change: showing instead of asserting, asking a decision question instead of listing rules, or reporting an observation instead of manufacturing a correction.

## Personal-Voice Boundary

A concept summary mentioning Scott does not license new first-person dialogue, emotions, or a confession. Use third-person attribution when only a summary supports the event. First-person lessons require checking Scott's original words and preserving their meaning. If unavailable, choose another approach without asking an overnight question. Never invent vulnerability to satisfy variety. Every evidence boundary below is an instance of the shared rule in [claim-boundaries.md](claim-boundaries.md); when they differ, the shared rule wins.

---

## Appendix: one teaching, six ways to deliver it (outlines, not drafts)

Source: C:/Claude Projects/Gridiron Warrior/wiki/concepts/weekly-load-ownership.md

These are alternative editorial outlines demonstrating rhetorical variety, not six posts to enqueue. Hooks are new adaptations, not Scott quotes. They reuse the load-ownership topic from the save/share packets deliberately; run the normal novelty gate before any production use.

### 1. Observation

Hook: Each coach can explain his addition. Who can explain the whole week?
Body: describe each role's partial view; identify the missing combined picture; show the source's named-owner and shared-sheet response.
Payoff: the staff knows which information is missing and who will gather it.
Action fit: share with the coach coordinating practice.
Evidence boundary: describe the pattern, not an invented incident Scott supposedly witnessed.

### 2. Demonstration

Hook: Put the additions on one sheet before you add them to the week.
Body: show an illustrative blank row with proposed work, duration, affected group, and reporting owner; fill the work/group fields with a clearly labeled example; leave unknown duration for the staff to supply; show how the row joins the shared discussion.
Payoff: a usable reporting structure, not another abstract argument for communication.
Action fit: save for the staff meeting.
Evidence boundary: no invented load totals, safe thresholds, or claimed improvement. Example fields are an editorial adaptation of the source, not a named proprietary system.

### 3. Decision Guide

Hook: Before you add work, who has seen the rest of the week?
Body: ask whether an owner is named; if not, assign the information-gathering role; if yes, record the addition and affected group; bring the combined picture to the people making the decision.
Payoff: a next-step decision about information ownership.
Action fit: save for planning.
Evidence boundary: this is not a decision tree for safe training dosage. The owner does not automatically gain veto authority.

### 4. Correction

Hook: A small addition is not the whole picture.
Body: acknowledge why one coach's added work may look reasonable; show that other coaches can also be adding work; replace the isolated view with the source's shared picture before the addition.
Payoff: judge the proposal in context rather than treating its small size as sufficient information.
Action fit: share with the staff member reviewing additions.
Evidence boundary: do not claim that every small addition is harmful or that coaches are careless. The source describes an ownership gap, not a universal causal rule.

### 5. Comparison

Hook: Same staff. Two ways to handle an addition.
Body: compare reporting after the work with writing the proposed addition before it happens; hold the staff and proposed work constant; show what information can enter the decision in each case.
Payoff: the difference is when the information becomes available, not who is the better coach.
Action fit: share to agree on the reporting process.
Evidence boundary: label the comparison illustrative. Do not invent before/after injury rates, improved performance, or a real client outcome.

### 6. Personal Lesson: Conditional Use

Supported outline: the wiki describes Scott bringing a report to staff meetings and having one-on-one conversations with position coaches. A third-person case can contrast presenting the overall week with only discussing one coach's period.
Potential hook, attributed rather than autobiographical: How Scott brings the whole week into the staff conversation.
Payoff: demonstrate the communication practice without pretending that information gives him control of the practice script.
Action fit: share with the person presenting the weekly report.
Evidence gate: check the original voice source before writing any first-person account, quoted dialogue, emotional claim, or statement about what Scott learned. That check was not performed here. Until then, use attributed case framing or select another approach.

### QA Performed

Each outline changes the teaching progression, identifies a reader payoff, and names its evidence boundary. Five are ready for source-grounded drafting through normal gates; the autobiographical treatment remains conditional on original-source verification. None is a rendered or approved carousel.

Novelty check on 2026-09-09: the source (`weekly-load-ownership`) already has shipped packs in `Deliverables/ready/`; these outlines are format examples only.
