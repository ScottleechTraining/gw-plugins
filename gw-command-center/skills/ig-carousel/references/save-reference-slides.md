# Save-Led Reference Slides

Status: installed in plugin 0.22.0 (2026-09-09), roadmap idea 8. Editorial reference for save-led opted-in decks only; loaded by Forge after the brief and before copy, and by the carousel skill and batch for new save-led builds and explicit action rewrites to save. It adds no schedule, dependency, app, schema field, or publishing permission. Style-only rebuilds and legacy decks never apply it.

## The Job

A save-led carousel must contain one compact tool that a coach can use later without rereading the entire post. A summary of the argument is not automatically a tool.

Before writing, finish this sentence internally: "At [specific future moment], this coach will reopen the post to [specific task] using [named reference slide]." If that sentence is vague, the save angle is not ready.

## Automatic Selection

Run only when the existing brief.action is save and the deck is newly written or explicitly undergoing an action rewrite. Do not alter legacy decks, already-approved decks, or style-only rebuilds.

Choose the smallest useful form supported by the source:

| Reader's later task | Reference form | Required contents |
|---|---|---|
| Remember what to check before a decision | Checklist | 3-5 concrete checks plus what to do when one fails |
| Choose between options | Decision card | Context, distinguishing question, conditional next step |
| Fill in a plan or staff report | Fill-in card | Named fields, one worked example elsewhere in the carousel |
| Follow a sequence | Sequence card | Ordered steps and the condition that changes the sequence |

Tie-break: use the form that answers one recurring coaching question with the fewest assumptions. Do not force numbers, dosage, thresholds, named proprietary methods, or a medical decision into a source that lacks them.

If no supported reference fits, revise the angle within save first. If it still cannot work, the failure path depends on who chose save:

- Forge chose save automatically: choose the next feasible action from the brief policy instead and draft that. Record the rejected save angle and why in the brief's reason line. This is not a silent switch; nobody requested save.
- Scott requested save (an `action: save` reroll note, or an explicit instruction): stop that draft for editorial repair. Leave the saved master and the polish note untouched, report the slug as REPAIR NEEDED with the missing source material named, and continue other topics. Do not ask Scott a nightly question, invent material to fill a card, or mark the failed draft complete. The morning review surfaces the repair.

## Placement and Structure

Use the existing archetype and slide budget. Normally place the reference slide after a short worked example and before the final CTA. Reuse or replace a summary/body slide; do not automatically add another slide. Keep the final CTA separate.

The reference slide must stand alone when screenshotted: a literal title naming the task, any essential context, and the usable tool. "The framework" or "Remember this" is not a sufficient title. Keep the normal GW attribution/footer. Do not add a fake download button, QR code, resource URL, or gated version.

Editorial starting budget, not a platform rule: title up to 9 words, no more than 5 items, and roughly 35-65 words total excluding the standard footer. Prefer fewer words. If readability fails on a phone, narrow the task or simplify the tool instead of shrinking below the existing design system's readable text size. Existing photo requirements and style rules still apply; this module does not replace them.

## Copy and CTA Contract

The reference is an ordinary body slide in schema 1. Its title and rows live inside that slide's existing fields object, each bound once with data-gw-copy. Do not add a new role, action, archetype, schema version, or second master. Initial build JSON remains an input; saved HTML remains authoritative afterward.

Use existing brief fields: payoff names the tool, reason names the future use, and takeaway names the decision. No schema extension is needed.

The final slide and caption name the same later use. For example: "Save the checklist for your next staff meeting." Avoid stacking save, share, comment, follow, and buy requests on one post. Useful content is available in the carousel itself, not contingent on a DM. This does not prevent a separately chosen conversation or conversion post later.

A save-to-share reroll rewrites the argument and CTA under the existing action-rewrite rules; the reference may remain only if it still serves the new intent. A style reroll must preserve saved wording exactly, even when this new editorial module would have written something else.

## Preflight: All Must Pass

1. Future-use test: name the moment and the job, not "later" or "get better."
2. Screenshot test: the card makes sense without the hook or caption.
3. Decision test: each item tells the coach what to check, record, choose, or change.
4. Source test: each coaching claim has a source; invented illustrations are explicitly labeled illustrative in production notes and on-slide when they could be mistaken for a real case. Categories and the repair ladder: [claim-boundaries.md](claim-boundaries.md).
5. Completeness test: the promised tool is visible and usable in the post. A blank with no field labels fails.
6. Pairing test: brief action, reference payoff, final CTA, and caption agree.
7. Layout test: inspect the rendered card at phone size; no clipped labels or tiny table text.
8. Compatibility test: existing voice/message gates, asset counts, photo floors, saved-copy rules, review tokens, and approval requirements remain intact.

These are editorial checks, not a predictive save-rate score. No claim about platform ranking or revenue lift is established by adding this module.

## Business Boundary

The free card should solve a small real problem. A future paid engagement can solve the larger implementation problem, but do not withhold the card's answer or force a sales CTA into a save-led deck. Product fit must be checked against current offer decisions before any later conversion post.

---

## Appendix: three worked save-led drafts (unrendered, unapproved)

Status: source-grounded copy drafts from the 2026-09-09 Codex packet. Not published, rendered, approved, or queued. Novelty check on 2026-09-09: every one of the three sources already has a shipped pack in `Deliverables/ready/` (weekly-load-ownership: three-coaches-each-added-a-reasonable-amount; ego-proof-exercise-selection: your-camp-lift-is-built-on-barbells; resource-reality-hs-programs: cheap-monitoring-battery and others). Treat these as format examples only; do not forge them as topics without a new angle that passes the novelty gate. These are new adaptations, not verbatim Scott quotes or new claims of results. Run the normal novelty and voice gates before putting any into the queue; existing sources may already have produced posts.

### 1. Who Owns the Whole Week?

Audience: high school football staff. Action: save. Archetype: System.
Future use: before the next staff meeting, reopen a checklist for reviewing extra work across coaches.
Payoff: a staff-meeting check that captures additions before they happen.
Source: C:/Claude Projects/Gridiron Warrior/wiki/concepts/weekly-load-ownership.md, especially "The Fix" and "Boundaries." Source identifies this as Scott's practice. This is an ownership tool, not a physiological load score.

#### Slide 1: Cover
Three coaches added a little.
Who owns the total?

#### Slide 2: Problem
The position coach adds Indy.
The head coach adds a finisher.
The JV kid picks up varsity reps.
Each coach sees his piece. Somebody needs to see the week.

#### Slide 3: Worked Example
ILLUSTRATIVE STAFF NOTE
Added work: extended Indy
Affected group: varsity receivers
Duration: record before the add
Cross-roster athletes: name them
Owner: bring the whole week to the room

#### Slide 4: Reference Card
BEFORE THE NEXT STAFF MEETING
1. Name the person who tracks the whole week.
2. Record each proposed addition, duration, and group.
3. List JV athletes also taking varsity reps.
4. Put those additions beside the week's existing work.
5. If nobody owns the total, name an owner before the next add.

#### Slide 5: CTA
Save the checklist for your next staff meeting.
Bring the whole week, not just your part.

#### Paired Caption
A reasonable addition can still be an addition nobody else knows about. One person needs the whole picture before the work gets added. Save the checklist for your next staff meeting.

Production boundary: do not import the external shared 1-10 scale; the source explicitly says it is not Scott's staff language. No injury-prevention promise, universal contact-hour limit, or claim that the owner has veto authority.
Future paid-fit hypothesis, not post copy: a school may need recurring help turning the shared picture into an annual system. Verify the current GW Schools offer before using this as a conversion angle.

### 2. Stop Turning Camp Into a PR Comparison

Audience: coaches selecting camp accessory work. Action: save. Archetype: Teardown.
Future use: when selecting camp B/C-block movements, reopen a decision card about comparison and familiarity.
Payoff: distinguish a useful training choice from an unhelpful comparison with summer numbers.
Source: C:/Claude Projects/Gridiron Warrior/wiki/concepts/ego-proof-exercise-selection.md, "The teaching" and "How Scott uses this in GW." This is Scott's context-specific camp practice, not a universal ban on familiar lifts.

#### Slide 1: Cover
The exercise can be fine.
The comparison can be the problem.

#### Slide 2: Before
A camp athlete looks at a familiar lift and sees what he cannot do today.
Now the session is being judged against a summer number.
That is not the only way to choose the work.

#### Slide 3: Worked Example
FROM SCOTT'S CAMP APPROACH
Alternating dumbbell bench instead of using flat bench as another comparison with an established number.
Different movement. Different reference point.
This is a selection example, not a load prescription.

#### Slide 4: Reference Card
CAMP ACCESSORY SELECTION CHECK
1. Name the job this movement needs to do.
2. Ask whether an old PR is becoming the comparison.
3. Consider a suitable variation without that established baseline.
4. Choose work your athletes can execute well today.
Use this for context, not novelty for its own sake.

#### Slide 5: CTA
Save this for your next camp accessory block.
Choose the job before you choose the comparison.

#### Paired Caption
Not every camp session needs another reminder of what an athlete lifted when he was fresh. Sometimes the useful change is the exercise and the reference point that comes with it. Save the selection check for your next camp accessory block.

Production boundary: never describe this as rehabilitation, permission to train through pain, or a guaranteed motivation effect. Do not turn the source's example weight into a prescription. Appropriateness remains a coaching decision.
Future paid-fit hypothesis, not post copy: contextual exercise-selection decisions could support a seasonal consulting case. Verify current offer availability before pitching it.

### 3. Does This Program Fit Your Room?

Audience: high school coaches adapting a program to staffing, equipment, and time. Action: save. Archetype: Template.
Future use: before importing a session from another program, reopen a room-fit audit.
Payoff: expose logistical assumptions before writing the day's exercise list.
Source: C:/Claude Projects/Gridiron Warrior/wiki/concepts/resource-reality-hs-programs.md, opening sections and "Why this makes GW programming the rational choice." The audit below is a new editorial adaptation of the constraints principle, not a documented named Scott framework.

#### Slide 1: Cover
A college program can fail before the first set.
It does not fit your room.

#### Slide 2: Problem
The exercise list is only part of the plan.
Who coaches it?
Where does everybody go?
What happens when the period ends?
Borrow the ideas. Check the assumptions.

#### Slide 3: Worked Example
ILLUSTRATIVE ROOM CHECK
30 athletes. 3 racks. One class period.
Before importing the session, sketch who occupies each station and who coaches each group.
If that picture does not work, the exercise list is not finished.

#### Slide 4: Reference Card
BEFORE YOU BORROW THE PROGRAM
Athletes: who trains together?
Equipment: what is actually available?
Staff: who supervises each station?
Time: when must the room be clear?
Bottleneck: where will athletes wait?
If the plan depends on resources you do not have, simplify it before assigning exercises.

#### Slide 5: CTA
Save the room-fit check before you borrow another program.
Write for the room you have.

#### Paired Caption
A program built around a different staff, room, and schedule brings those assumptions with it. Check them before you copy the exercises. Save the room-fit card for the next time you adapt somebody else's session.

Production boundary: the 30-athlete/3-rack example is illustrative, not a prescribed supervision ratio or a capacity/safety standard. Do not invent rack rotations or guarantee completion time from this example.
Future paid-fit hypothesis, not post copy: an implementation service can customize around the actual school constraints. The save-led post still gives away the complete small audit.

### Editorial QA Performed

All three drafts include a specific future use, a source location, an example, a standalone reference card, a matching single-action CTA, and a paired caption. None promises a download, manual DM fulfillment, medical result, or performance uplift. All use ordinary body slides; no foundations schema changes are required.

Not performed: live queue deduplication, source transcript re-listening, the installed voice checker, visual rendering, or publication. Those remain the normal production gates. This pack is an editorial module and drafts, not three approved finished carousels.
