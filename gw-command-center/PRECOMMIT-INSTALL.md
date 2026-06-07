# Pre-commit hook install (one-time)

This plugin ships a `check_commands.py` validator that catches the exact
regression class that took the GW pipeline red on 2026-06-07: a plugin
command file missing its `name:` frontmatter field, or with Unicode
em-dash (`—`) / arrow (`→`) in its description. Both cause Claude Code's
plugin loader to silently fail to register the slash command, so
`claude -p "/gw-foo"` returns `Unknown command` even though the file
exists.

To install the pre-commit hook in your local clone:

```bash
cp gw-command-center/scripts/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

The hook only fires when `gw-command-center/commands/*.md` is staged, so
non-command commits are unaffected. Bypass intentionally with
`git commit --no-verify`.

If the hook ever blocks you legitimately, run the auto-fixer:

```bash
python gw-command-center/fix_commands.py
git add gw-command-center/commands/
git commit ...
```
