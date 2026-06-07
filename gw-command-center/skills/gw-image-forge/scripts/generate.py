#!/usr/bin/env python3
"""GW Image Forge — OpenAI Images backend (gpt-image-1).

Mirrors the fal.ai pattern from D:\\Claude Projects\\_archive\\2026-05-12\\misc\\
GW-Design-Studio\\scripts\\generate_images.py. Lifts the .env loader pattern
from D:\\Claude Projects\\Gridiron Warrior\\scripts\\send_lint_email.py.

Stdlib only. No pip install.

Usage:
    python generate.py --config config.json
    python generate.py --config -   # read from stdin

Config schema:
    {
        "name": "kebab-case-slug",
        "prompt": "full constructed prompt as a single string",
        "size": "1024x1024" | "1024x1536" | "1536x1024" | "auto",
        "quality": "low" | "medium" | "high",
        "n": 1                        # optional, defaults to 1
    }

Output:
    PNG files written to D:\\Claude Projects\\Gridiron Warrior\\Images\\
    Filename pattern: {name}_{i}.png  (1-indexed when n > 1; just {name}.png when n == 1)

On success, stdout receives:
    {"paths": ["D:\\\\...\\\\foo_1.png", ...]}
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ENV_FILE = Path(r"D:\Claude Projects\Gridiron Warrior\scripts\.env")
OUT_DIR = Path(r"D:\Claude Projects\Gridiron Warrior\Images")
API_URL = "https://api.openai.com/v1/images/generations"
MODEL = "gpt-image-1"

VALID_SIZES = {"1024x1024", "1024x1536", "1536x1024", "auto"}
VALID_QUALITY = {"low", "medium", "high", "auto"}


def load_env_file(path: Path = ENV_FILE) -> None:
    """Read KEY=VALUE lines from .env and inject into os.environ.

    Live env vars take precedence; .env only fills gaps. Missing file is OK.
    Pattern lifted verbatim from send_lint_email.py.
    """
    if not path.is_file():
        return
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def validate_config(cfg: dict) -> dict:
    """Normalize and validate a config dict. Returns the normalized dict."""
    required = {"name", "prompt"}
    missing = required - set(cfg)
    if missing:
        raise ValueError(f"Missing required config keys: {sorted(missing)}")

    name = str(cfg["name"]).strip()
    if not name or "/" in name or "\\" in name:
        raise ValueError(f"Invalid name (must be a kebab-case slug, no path separators): {name!r}")

    prompt = str(cfg["prompt"]).strip()
    if not prompt:
        raise ValueError("Prompt is empty")

    size = cfg.get("size", "1024x1024")
    if size not in VALID_SIZES:
        raise ValueError(f"Invalid size {size!r}; must be one of {sorted(VALID_SIZES)}")

    quality = cfg.get("quality", "high")
    if quality not in VALID_QUALITY:
        raise ValueError(f"Invalid quality {quality!r}; must be one of {sorted(VALID_QUALITY)}")

    n = int(cfg.get("n", 1))
    if not 1 <= n <= 4:
        raise ValueError(f"Invalid n={n}; must be between 1 and 4")

    return {
        "name": name,
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "n": n,
    }


def call_openai(cfg: dict, api_key: str) -> list[bytes]:
    """POST to the Images API and return a list of PNG byte strings."""
    payload = {
        "model": MODEL,
        "prompt": cfg["prompt"],
        "size": cfg["size"],
        "quality": cfg["quality"],
        "n": cfg["n"],
    }
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    last_err: Exception | None = None
    for attempt in (1, 2):
        try:
            req = urllib.request.Request(API_URL, data=body, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                images = []
                for item in data.get("data", []):
                    b64 = item.get("b64_json")
                    if not b64:
                        raise RuntimeError(f"Image item missing b64_json: {item}")
                    images.append(base64.b64decode(b64))
                if not images:
                    raise RuntimeError(f"OpenAI returned no images: {data}")
                return images
        except urllib.error.HTTPError as e:
            err_body = ""
            try:
                err_body = e.read().decode("utf-8", errors="replace")
            except Exception:
                pass
            last_err = RuntimeError(f"HTTP {e.code} from OpenAI: {err_body}")
            if e.code == 429 and attempt == 1:
                # Single retry with 5s backoff on rate limit
                time.sleep(5)
                continue
            raise last_err from e
        except urllib.error.URLError as e:
            last_err = RuntimeError(f"Network error: {e.reason}")
            raise last_err from e

    # Unreachable in practice but keeps mypy quiet.
    raise last_err or RuntimeError("Unknown failure")


def write_pngs(cfg: dict, images: list[bytes]) -> list[Path]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    if cfg["n"] == 1:
        # Single image: no index suffix
        target = OUT_DIR / f"{cfg['name']}.png"
        target.write_bytes(images[0])
        paths.append(target)
    else:
        for i, img in enumerate(images, start=1):
            target = OUT_DIR / f"{cfg['name']}_{i}.png"
            target.write_bytes(img)
            paths.append(target)
    return paths


def main() -> int:
    p = argparse.ArgumentParser(description="GW Image Forge — OpenAI gpt-image-1 backend")
    p.add_argument(
        "--config",
        required=True,
        help="Path to JSON config file, or '-' to read JSON from stdin",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate config and print the constructed prompt without calling the OpenAI API. Costs nothing. Useful for iterating on prompt construction.",
    )
    args = p.parse_args()

    if args.config == "-":
        raw = sys.stdin.read()
    else:
        raw = Path(args.config).read_text(encoding="utf-8")

    try:
        cfg = validate_config(json.loads(raw))
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Config error: {e}", file=sys.stderr)
        return 2

    if args.dry_run:
        # Print what would be sent without calling the API.
        preview = {
            "mode": "dry-run",
            "name": cfg["name"],
            "size": cfg["size"],
            "quality": cfg["quality"],
            "n": cfg["n"],
            "prompt_length": len(cfg["prompt"]),
            "prompt": cfg["prompt"],
            "would_write_to": str(
                OUT_DIR / f"{cfg['name']}.png" if cfg["n"] == 1
                else OUT_DIR / f"{cfg['name']}_1.png"
            ),
            "api_url": API_URL,
            "model": MODEL,
        }
        print(json.dumps(preview, indent=2))
        return 0

    load_env_file()
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        print(
            "OPENAI_API_KEY missing. Add it to "
            + str(ENV_FILE)
            + " as `OPENAI_API_KEY=sk-...`",
            file=sys.stderr,
        )
        return 3

    try:
        images = call_openai(cfg, api_key)
    except Exception as e:
        print(f"Image generation failed: {e}", file=sys.stderr)
        return 4

    paths = write_pngs(cfg, images)
    print(json.dumps({"paths": [str(p) for p in paths]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
