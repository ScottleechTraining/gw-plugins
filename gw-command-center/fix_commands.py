"""Fix every command file that fails check_commands.py.

Two fixes applied, idempotently:
  F1. If `name:` is missing from frontmatter, insert it right after the
      opening `---`, with value = filename stem.
  F2. Replace Unicode em-dashes (—), en-dashes (–), and Unicode arrows (→)
      in the `description:` line only with ASCII (` - `, ` -> `).
      Body content is NEVER touched — only the description field in
      frontmatter.

Why this matters: Claude Code 2.1.158 plugin loader silently fails to
register commands whose frontmatter is missing `name:` or contains
certain Unicode in `description`. Symptom: `claude -p "/gw-foo"` returns
"Unknown command".

Usage:
    python fix_commands.py            # apply fixes in place
    python fix_commands.py --dry-run  # show what would change

Re-run check_commands.py after to confirm 0 violations.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMMANDS_DIR = HERE / "commands"
if not COMMANDS_DIR.exists():
    COMMANDS_DIR = HERE / "gw-command-center" / "commands"

UNSAFE_REPLACEMENTS = {
    "—": " - ",   # em-dash -> hyphen with spaces
    "–": " - ",   # en-dash -> hyphen with spaces
    "→": " -> ",  # Unicode arrow -> ASCII arrow
}


def scrub_unicode_description(line: str) -> str:
    """Replace unsafe Unicode in description value only. Idempotent."""
    if not line.lstrip().startswith("description:"):
        return line
    out = line
    for src, dst in UNSAFE_REPLACEMENTS.items():
        out = out.replace(src, dst)
    # Collapse any accidental double spaces we created.
    out = re.sub(r"  +", " ", out)
    return out


def fix_file(path: Path, dry_run: bool = False) -> tuple[bool, list[str]]:
    """Return (changed, summary_of_changes)."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return False, [f"SKIP {path.name}: no frontmatter block, leaving alone"]

    # Find end of frontmatter
    fm_end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm_end = i
            break
    if fm_end is None:
        return False, [f"SKIP {path.name}: unterminated frontmatter"]

    changes = []

    # F1: ensure `name:` field is present in frontmatter
    has_name = False
    for i in range(1, fm_end):
        if re.match(r"^name\s*:", lines[i]):
            has_name = True
            break
    if not has_name:
        expected = path.stem
        # Insert as new line at position 1 (right after opening ---)
        lines.insert(1, f"name: {expected}\n")
        fm_end += 1  # we shifted the closing --- down by one
        changes.append(f"F1: inserted `name: {expected}` into frontmatter")

    # F2: scrub Unicode in description line
    for i in range(1, fm_end):
        original = lines[i]
        scrubbed = scrub_unicode_description(original)
        if scrubbed != original:
            lines[i] = scrubbed
            chars = []
            for src in UNSAFE_REPLACEMENTS:
                if src in original:
                    chars.append(repr(src))
            changes.append(f"F2: scrubbed {', '.join(chars)} from description")

    if not changes:
        return False, []
    new_text = "".join(lines)
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return True, changes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not COMMANDS_DIR.exists():
        print(f"FATAL: commands dir not found at {COMMANDS_DIR}", file=sys.stderr)
        return 1

    files = sorted(COMMANDS_DIR.glob("*.md"))
    n_changed = 0
    for f in files:
        changed, summary = fix_file(f, dry_run=args.dry_run)
        if changed:
            n_changed += 1
            print(f"\n{f.name}:")
            for s in summary:
                print(f"  - {s}")
        elif summary:
            for s in summary:
                print(s)

    label = "would change" if args.dry_run else "changed"
    print(f"\n{n_changed} of {len(files)} files {label}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
