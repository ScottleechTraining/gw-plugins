#!/usr/bin/env python3
"""Package the Custom Carousel Machine engine into the buyer-facing release zip.

Reads the version from .claude-plugin/plugin.json and writes
dist/custom-carousel-machine-v{version}.zip, laid out as a single
top-level custom-carousel-machine/ folder matching what README.md and
UPDATING.md tell buyers to unzip and copy from.

stdlib only. Run: python tools/package_release.py
"""
import hashlib
import json
import sys
import zipfile
from pathlib import Path

ENGINE_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = ENGINE_ROOT / "dist"
ZIP_ROOT = "custom-carousel-machine"

# What a buyer receives. Everything else (qa/, tools/, dist/, vcs, secrets) is excluded.
TOP_LEVEL_INCLUDES = [
    "README.md",
    "UPDATING.md",
    "brand-profile.template.md",
    ".claude-plugin",
    "skills",
    "examples",
]
EXCLUDE_NAMES = {"qa", "tools", "dist", "__pycache__"}
EXCLUDE_PREFIXES = (".git", ".env")

REQUIRED_SKILLS = [
    "skills/carousel/SKILL.md",
    "skills/brand-setup/SKILL.md",
    "skills/pack-author/SKILL.md",
]
FIXED_DATE = (2020, 1, 1, 0, 0, 0)  # deterministic ZipInfo timestamp
FORBIDDEN_STRINGS = (b"service_role", b"sb_secret")
EM_DASH = "—"


def is_excluded(rel_path: Path) -> bool:
    return any(
        part in EXCLUDE_NAMES or part.startswith(EXCLUDE_PREFIXES)
        for part in rel_path.parts
    )


def collect_files():
    files = []
    for top in TOP_LEVEL_INCLUDES:
        top_path = ENGINE_ROOT / top
        if not top_path.exists():
            raise FileNotFoundError(f"expected engine file/dir missing: {top}")
        if top_path.is_file():
            files.append(top_path)
            continue
        for p in top_path.rglob("*"):
            if p.is_file() and not is_excluded(p.relative_to(ENGINE_ROOT)):
                files.append(p)
    return sorted(files, key=lambda p: p.relative_to(ENGINE_ROOT).as_posix())


def build_zip(version: str) -> Path:
    DIST_DIR.mkdir(exist_ok=True)
    zip_path = DIST_DIR / f"custom-carousel-machine-v{version}.zip"
    files = collect_files()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            arcname = f"{ZIP_ROOT}/{f.relative_to(ENGINE_ROOT).as_posix()}"
            info = zipfile.ZipInfo(arcname, date_time=FIXED_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, f.read_bytes())
    return zip_path


def validate(zip_path: Path):
    errors = []
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()

        for skill in REQUIRED_SKILLS:
            full = f"{ZIP_ROOT}/{skill}"
            if full not in names:
                errors.append(f"missing required skill file: {full}")

        if f"{ZIP_ROOT}/README.md" not in names:
            errors.append(f"missing {ZIP_ROOT}/README.md")

        for name in names:
            rel_parts = Path(name).parts[1:]  # drop the custom-carousel-machine/ root
            if any(part in EXCLUDE_NAMES or part.startswith(EXCLUDE_PREFIXES) for part in rel_parts):
                errors.append(f"excluded path leaked into zip: {name}")

        for name in names:
            data = zf.read(name)
            for bad in FORBIDDEN_STRINGS:
                if bad in data:
                    errors.append(f"forbidden string '{bad.decode()}' found in {name}")
            if name.endswith(".md") and EM_DASH in data.decode("utf-8", errors="replace"):
                errors.append(f"em dash (U+2014) found in {name}")

    return errors


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main():
    plugin_json = json.loads((ENGINE_ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    version = plugin_json["version"]

    zip_path = build_zip(version)
    errors = validate(zip_path)

    with zipfile.ZipFile(zip_path) as zf:
        infos = zf.infolist()
        file_count = len(infos)
        total_size = sum(i.file_size for i in infos)

    digest = sha256_of(zip_path)

    print("=" * 60)
    print("Custom Carousel Machine release")
    print(f"version:            {version}")
    print(f"zip:                {zip_path}")
    print(f"files:              {file_count}")
    print(f"uncompressed size:  {total_size:,} bytes")
    print(f"zip size:           {zip_path.stat().st_size:,} bytes")
    print(f"sha256:             {digest}")
    print("=" * 60)

    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("validation: OK")


if __name__ == "__main__":
    main()
