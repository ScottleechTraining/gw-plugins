# Banned words and phrases: the one list every voice skill reads

Created 2026-11-18 (Scott ruling R9: "Absolutely. One shared file."). Every command or skill that writes as Scott, or checks a draft written as Scott, reads this file. When Scott bans a word or a phrase, add it here with the date and his reason, then bump the plugin version. Nothing else in the plugin should restate this list.

The root `C:\Claude Projects\CLAUDE.md` keeps its own BANNED WORDS section because it loads every session, and `Gridiron Warrior/scripts/voice_check.py` parses that section. When a word is added here, add it there too.

Insiders offer phrases ($29, any trial, "Weekly Film Study" and the rest) are a separate list: the "Never write" section of `plugins/gw-command-center/references/insiders-offer.md`.

## Punctuation

- **No em-dashes. Ever.** Not one, in any output. The double hyphen used as a dash counts as one. Rewrite the sentence: split it in two or use a period. Do not swap in a string of semicolons.

## Banned words

Case-insensitive, whole-word match. Any use fails unless an exception is listed.

fluff, delve, tapestry, vibrant, transformative, unlock, leverage (as a verb), game-changer, revolutionary, groundbreaking, seamless, robust, utilize, synergy, holistic, empower, journey, curated, cutting-edge, innovative, best-in-class, dive into, unpack, explore, elevate, reimagine, supercharge, lane (as a training track or path).

Exceptions on record:
- **leverage**: fails only as a verb ("leverage this", "leveraging that"). The noun passes ("the leverage in a squat").
- **lane**: Scott 2026-10-13, "I hate the term Lane. It feels very AI." "Strength lane", "speed lane", "pick his lane", "the lane decides" all fail. Name the work ("more bar", "sprints, jumps, throws") or say track, path, or plan. A literal sprint lane on a field passes.

Plain replacements: utilize to use, elevate to raise, dive into to get into, unlock to open up.

## Banned phrases and terms

- **Contrast titles.** "You do not need X. You need Y." and every variant: "You don't need X, you need Y", "Not X. Y.", "X, not Y.", a one-line "Not four weeks." beat, "you think X, it starts with Y". Banned everywhere: hooks, titles, covers, captions, threads, reels, emails, bodies. Scott 2026-11-03: "it definitely does feel very AI oriented." State the one claim that matters instead. Search each piece for a sentence that opens or closes on "not" and rewrite any that sets up a contrast. Packs already shipped to Drive stay as shipped; never re-render one for this.
- **"card" for a carousel slide.** Scott 2026-09-15, again 2026-09-22 after decks shipped with "Save the card" and "the card on slide 4". Fails in slide copy, CTAs, and captions, and in reports and review notes written to Scott. Write "Save this for..." or "slide 4". The reference slide is a slide. Internal file and CSS names (`card_title`, `.card`) stay as they are.
- **"match" for a Contact Prep drill.** Scott 2026-09-22. Write "drill". A wrestling match or a matching pair of numbers passes.
- **"mat drills" and "mat block" in public content.** Scott 2026-09-19: "Call them Contact Prep drills not mat drills." and "I would never say mat block." In carousels, threads, captions, and emails, call mat-drill-style contact station work "Contact Prep drills". Historic Leech Letters and the wiki page `concepts/mat-drill-microcycle.md` keep "mat drills"; do not rewrite history. Ask Scott before applying this outside drill talk (for example "Mat Drills season" as an era name).

## Flagged, not banned

- **sorting**: Scott flagged it as AI-ish on 2026-09-19. Name the mistake, or use split, separate, or group.
