"""Validate every gw-command-center plugin command.

Catches the regression class introduced by commit dfb2241 "Add YAML
frontmatter to all 27 gw-* commands": some commands got `name:` and some
didn't, and some descriptions kept Unicode em-dashes (U+2014) that the
v2.1.158 plugin loader can't register.

Symptom of a broken command: `claude -p "/gw-foo"` returns "Unknown command".

Rules enforced:
  R1. Every commands/*.md MUST have a YAML frontmatter block.
  R2. The frontmatter MUST contain a `name:` field equal to the filename stem.
  R3. The frontmatter description (if present) MUST be ASCII-safe — no
      em-dash (—), no en-dash (–), no Unicode arrow (→). Use - and -> instead.
  R4. The frontmatter MUST contain `model: opus` or `model: sonnet`
      (CLAUDE.md MODEL POLICY: Fable is pay-per-use; no command may silently
      inherit the session model). Added per audit 2026-07-14 finding P2.

Exit codes:
  0 = all green
  1 = at least one violation
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMMANDS_DIR = HERE / "commands"
if not COMMANDS_DIR.exists():
    # fallback if script ever moves
    COMMANDS_DIR = HERE / "gw-command-center" / "commands"

UNSAFE_CHARS = {
    "—": "em-dash (—)",
    "–": "en-dash (–)",
    "→": "Unicode arrow (→)",
}


def parse_frontmatter(text: str) -> dict | None:
    """Return frontmatter dict, or None if no frontmatter block found.

    Tiny YAML-ish parser sufficient for `key: value` and `key: "value"`.
    Doesn't handle multi-line or nested — none of our commands need it."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    fm = {}
    for i in range(1, len(lines)):
        line = lines[i]
        if line.strip() == "---":
            return fm
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*?)\s*$", line)
        if m:
            key, val = m.group(1), m.group(2)
            # Strip surrounding quotes
            if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
                val = val[1:-1]
            fm[key] = val
    return fm  # missing closing ---, but treat what we have as frontmatter


def check_file(path: Path) -> list[str]:
    violations = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"could not read: {exc}"]

    fm = parse_frontmatter(text)
    if fm is None:
        violations.append("R1: missing YAML frontmatter block")
        return violations

    expected_name = path.stem
    actual_name = fm.get("name")
    if not actual_name:
        violations.append(f"R2: missing `name:` field (expected `name: {expected_name}`)")
    elif actual_name != expected_name:
        violations.append(
            f"R2: name mismatch (got '{actual_name}', expected '{expected_name}')"
        )

    desc = fm.get("description", "")
    for ch, label in UNSAFE_CHARS.items():
        if ch in desc:
            violations.append(f"R3: description contains {label} — use ASCII")

    model = fm.get("model")
    if not model:
        violations.append("R4: missing `model:` field (must be `model: opus` or `model: sonnet`)")
    elif model not in ("opus", "sonnet"):
        violations.append(f"R4: model '{model}' not allowed (must be opus or sonnet)")
    return violations


def main() -> int:
    if not COMMANDS_DIR.exists():
        print(f"FATAL: commands dir not found at {COMMANDS_DIR}", file=sys.stderr)
        return 1
    files = sorted(COMMANDS_DIR.glob("*.md"))
    if not files:
        print(f"FATAL: no .md commands in {COMMANDS_DIR}", file=sys.stderr)
        return 1

    bad = []
    for f in files:
        v = check_file(f)
        if v:
            bad.append((f.name, v))

    print(f"check_commands: {len(files)} files scanned, {len(bad)} with violations")
    for name, v in bad:
        print(f"\n  {name}")
        for line in v:
            print(f"    - {line}")

    if bad:
        return 1
    print("\nALL GREEN — every command has a valid frontmatter + ASCII-safe description.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
