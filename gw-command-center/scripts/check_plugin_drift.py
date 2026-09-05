#!/usr/bin/env python3
"""SessionStart hook: warn when any installed copy of gw-command-center lags the source.

Three copies exist on this machine:
  1. Source of truth  C:\\Claude Projects\\plugins\\gw-command-center\\.claude-plugin\\plugin.json
  2. CLI install      ~/.claude/plugins/installed_plugins.json (refreshed by gw-plugin-ship Step 4)
  3. Cowork snapshot  %APPDATA%\\Claude\\local-agent-mode-sessions\\*\\*\\rpm\\plugin_*\\  (refreshed
                      only when Scott clicks Sync in Cowork Settings -> Plugins)

The desktop app injects copy 3 into Claude Code sessions, so a stale snapshot can shadow
a fresh CLI install. Found 2026-09-05: the snapshot sat at v0.1.0 for three months.

Prints nothing when everything matches. Always exits 0 (advisory only).
Stdlib only.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

PLUGIN = "gw-command-center"
SOURCE = Path(r"C:\Claude Projects\plugins") / PLUGIN / ".claude-plugin" / "plugin.json"
CLI_REGISTRY = Path.home() / ".claude" / "plugins" / "installed_plugins.json"
RPM_ROOT = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / "Claude" / "local-agent-mode-sessions"
SUPERSEDED = {"gw-kit": "kit-guardrails now ships inside gw-command-center"}


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def rpm_plugins() -> list[tuple[str, str]]:
    """(name, version) for every plugin the desktop app has snapshotted."""
    out = []
    for pj in RPM_ROOT.glob("*/*/rpm/plugin_*/.claude-plugin/plugin.json"):
        data = read_json(pj)
        if data.get("name"):
            out.append((data["name"], str(data.get("version", "?"))))
    return out


def main() -> int:
    truth = read_json(SOURCE).get("version")
    if not truth:
        return 0  # source folder missing (other machine, D: era); nothing to compare

    warnings = []

    cli = read_json(CLI_REGISTRY).get("plugins", {}).get(f"{PLUGIN}@gw-plugins", [{}])
    cli_ver = cli[0].get("version") if cli else None
    if cli_ver != truth:
        warnings.append(
            f"CLI install is {cli_ver or 'missing'}, source is {truth}. "
            "Run gw-plugin-ship Step 4 (marketplace update / uninstall / install)."
        )

    for name, ver in rpm_plugins():
        if name == PLUGIN and ver != truth:
            warnings.append(
                f"Cowork snapshot is {ver}, source is {truth}. It shadows the CLI install in Code sessions. "
                "Scott: Cowork -> Settings -> Plugins -> gw-plugins -> Sync -> Update. Same at claude.ai/customize -> Skills."
            )
        elif name in SUPERSEDED:
            warnings.append(f"Cowork still has plugin '{name}' ({SUPERSEDED[name]}). Scott: uninstall it in Cowork Settings -> Plugins.")

    if warnings:
        print("PLUGIN DRIFT (gw-command-center):")
        for w in warnings:
            print(f"  - {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
