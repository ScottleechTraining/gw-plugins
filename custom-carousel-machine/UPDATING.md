# Updating The Custom Carousel Machine

Your brand and your custom packs are **safe** during an update. They live in your project (`carousel/brand-profile.md` and `carousel/packs/`), not inside this engine. An update only replaces the engine.

## How to update
1. Download the newest zip from where you got this one.
2. Delete the old skill folders under `~/.claude/skills/`: `carousel`, `brand-setup`, `pack-author`.
3. Unzip the new version anywhere, then copy the three folders **inside** its `skills/` folder (`carousel`, `brand-setup`, `pack-author`) into `~/.claude/skills/`.
4. Restart Claude Code. Your `carousel/` folder in your project is untouched.

## How to tell what changed
Check `version` in `.claude-plugin/plugin.json` and the changelog at the top of `skills/carousel/SKILL.md`.

## The one rule that keeps updates safe
Never put your real `brand-profile.md` or your authored packs *inside* the engine folder. Keep them in your project's `carousel/` folder. If you ever see them inside the engine, move them out before updating.
