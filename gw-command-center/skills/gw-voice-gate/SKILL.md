---
name: gw-voice-gate
description: PASS/FAIL QA gate for any draft written as Scott Leech. Runs a mechanical checklist against a draft (em-dashes, banned words, sign-off, sentence length, AI-slop tells, bullet abuse, ICP fit) and applies the fixes. Use this skill whenever Scott says "voice gate", "voice check", "check this draft against Scott's voice", or "run the gate". Also run this automatically as the final step of any GW skill that produces Scott-voice content (Leech Letter, Substack, Content Forge, freebie, seed writer) before the draft is presented or saved. A draft never ships with a FAIL.
---

# GW Voice Gate

A mechanical, verifiable QA gate. It runs on any draft written as Scott and returns PASS or FAIL. It edits mechanically to fix the listed violations. It never rewrites voice, restructures content, or invents ideas beyond the fixes below.

The reference voice rules live in `D:\Claude Projects\CLAUDE.md` (VOICE RULES, BANNED WORDS, SIGNATURE PHRASES, EMAIL VOICE EXAMPLES). This gate is the executable version of those rules.

## Input

A draft as text (pasted, or a file path to read). Note the content type: email / letter / long-form post, or short social (tweet, IG caption, carousel slide). Some checks only apply to the long forms.

## Run these checks in order. Each is a concrete step.

### Check 1: Em-dash scan
Search the draft for the em-dash character and for the double-hyphen used as one dash. Any hit is a FAIL.
- List the line number of each hit.
- Rewrite each offending sentence without it: split into two sentences, or replace with a period. Never swap in a semicolon-heavy construction.

### Check 2: Banned words scan
Case-insensitive, word-boundary match against this list:
fluff, delve, tapestry, vibrant, transformative, unlock, leverage (verb use only), game-changer, revolutionary, groundbreaking, seamless, robust, utilize, synergy, holistic, empower, journey, curated, cutting-edge, innovative, best-in-class, dive into, unpack, explore, elevate, reimagine, supercharge.
- Any hit is a FAIL. List the line number and the word.
- "leverage" only fails when used as a verb (leverage this, leveraging that). "Leverage" as a noun (the leverage in a squat) passes.
- Give a plain-language replacement for each hit (utilize to use, elevate to raise, dive into to get into, unlock to open up, etc.).

### Check 3: Sign-off
Applies only to email, letter, or long-form post. Skip for tweets, IG captions, carousel slides.
- The content must end with "Keep the Fire Burning," then "Leech" on its own line.
- Signing "Scott" anywhere is a FAIL. Change it to "Leech."
- A missing or malformed sign-off on a long-form piece is a FAIL. Add the correct sign-off.
- Exception: a personal letter addressed to a family member may sign off "Dad."

### Check 4: Sentence and paragraph length
- Flag any sentence over 30 words. List the line number and suggest a split point.
- Flag any paragraph over 5 sentences. List it and suggest where to break it.
- These are flags, not hard fails on their own. Apply the split when it is clean and does not change meaning.

### Check 5: AI-slop tells
Flag and fix each:
- "It's not just X, it's Y" (and "not only X but Y") constructions. Rewrite as a plain statement.
- Rule-of-three adjective stacks used as padding ("faster, stronger, and more explosive"). Cut to the one that carries weight.
- Rhetorical-question openers stacked more than once. Keep at most one; turn the rest into statements.
- Hedging: "might", "could potentially", "it's worth noting", "perhaps", "in some cases". Cut the hedge and state it straight.

### Check 6: Bullet abuse
Applies to emails and social posts, which should be conversational paragraphs.
- More than one short bullet list in an email is a flag. Convert the weaker list to prose.

### Check 7: ICP sanity
The draft speaks to a time-strapped high school football and S&C coach.
- Flag anything addressed to athletes ("get your reps in", "coach put you through") or to marketers ("your funnel", "your audience", "conversion rate").
- Note the line and rewrite it to speak to the coach.

## Output format

No em-dashes anywhere in your own output.

1. First line: **PASS** or **FAIL**.
2. A numbered list of violations. Each entry: the check, the line reference, the offending text, and the concrete fix.
3. If FAIL: the corrected draft in full, with every fix applied.

If PASS, say so and stop. Do not rewrite a clean draft.

## Scope discipline

The gate edits mechanically. It fixes only the listed violations. It does not rewrite voice, restructure the piece, retitle it, change the argument, or add ideas. If a draft reads weak but breaks no rule, it PASSES. Voice work belongs to the skill that wrote the draft, not to the gate.
