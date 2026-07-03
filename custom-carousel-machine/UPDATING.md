# Updating The Custom Carousel Machine

Your brand and your custom packs are **safe** during an update. They live in your project (`carousel/brand-profile.md` and `carousel/packs/`), not inside this engine. An update only replaces the engine.

## If you installed via marketplace
```
claude plugin marketplace update <your-marketplace>
claude plugin uninstall custom-carousel-machine
claude plugin install custom-carousel-machine@<your-marketplace>
```

## If you installed via zip
1. Delete the old engine folder (the `custom-carousel-machine` skill folder under `~/.claude/skills/`).
2. Unzip the new version in its place.
3. That's it. Your `carousel/` folder in your project is untouched.

## How to tell what changed
Check `version` in `.claude-plugin/plugin.json` and the changelog at the top of `skills/carousel/SKILL.md`.

## The one rule that keeps updates safe
Never put your real `brand-profile.md` or your authored packs *inside* the engine folder. Keep them in your project's `carousel/` folder. If you ever see them inside the engine, move them out before updating.
