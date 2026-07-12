"""Render carousel QA fixtures to PNGs and build a contact sheet."""

from __future__ import annotations

import html
import http.server
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import threading
from dataclasses import dataclass
from datetime import datetime
from functools import partial
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, urlencode


SCRIPT_DIR = Path(__file__).resolve().parent
FIXTURES_DIR = SCRIPT_DIR / "fixtures"
RENDERS_DIR = SCRIPT_DIR / "renders"

EDGE_CANDIDATES = (
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
)
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_WIDTH = 1080
EXPECTED_HEIGHT = 1350
MIN_PNG_SIZE = 2000
EDGE_TIMEOUT_SECONDS = 60
SLUG_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")

WorkItem = tuple[str, str, str]


@dataclass(frozen=True)
class RenderResult:
    fixture_filename: str
    pack: str
    template: str
    ok: bool
    detail: str


class FixtureParser(HTMLParser):
    """Collect the body pack and data-template attributes in source order."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.pack: str | None = None
        self.templates: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = dict(attrs)
        if tag == "body" and self.pack is None:
            self.pack = attributes.get("data-pack")

        template = attributes.get("data-template")
        if template is not None:
            self.templates.append(template)


def require_slug(value: str, label: str, fixture_path: Path) -> str:
    """Reject empty or path-like slugs before using them as output names."""

    if not SLUG_PATTERN.fullmatch(value):
        raise ValueError(
            f'{fixture_path.name}: invalid {label} slug {value!r}; '
            "expected letters, digits, dots, underscores, or hyphens"
        )
    return value


def discover_work() -> list[WorkItem]:
    """Return fixture, pack, and template tuples in deterministic source order."""

    fixture_paths = sorted(
        FIXTURES_DIR.glob("*.html"), key=lambda path: path.name.casefold()
    )
    if not fixture_paths:
        raise FileNotFoundError(f"No HTML fixtures found in {FIXTURES_DIR}")

    work: list[WorkItem] = []
    for fixture_path in fixture_paths:
        parser = FixtureParser()
        parser.feed(fixture_path.read_text(encoding="utf-8"))
        parser.close()

        if parser.pack is None:
            raise ValueError(
                f'{fixture_path.name}: <body> is missing data-pack="..."'
            )
        pack = require_slug(parser.pack, "pack", fixture_path)

        if not parser.templates:
            raise ValueError(
                f'{fixture_path.name}: no data-template="..." values found'
            )
        for raw_template in parser.templates:
            template = require_slug(raw_template, "template", fixture_path)
            work.append((fixture_path.name, pack, template))

    return work


def reset_renders_dir() -> None:
    """Start every run with a clean renders directory."""

    if RENDERS_DIR.exists():
        shutil.rmtree(RENDERS_DIR)
    RENDERS_DIR.mkdir(parents=True)


def locate_edge() -> tuple[Path | None, list[Path]]:
    """Find Edge from EDGE_PATH first, then the standard install locations."""

    candidates: list[Path] = []
    override = os.environ.get("EDGE_PATH")
    if override and override.strip():
        override_path = os.path.expandvars(override.strip().strip('"'))
        candidates.append(Path(override_path).expanduser())
    candidates.extend(EDGE_CANDIDATES)

    for candidate in candidates:
        try:
            if candidate.is_file():
                return candidate, candidates
        except OSError:
            continue
    return None, candidates


def validate_png(path: Path) -> str | None:
    """Return an error message, or None for a valid 1080x1350 PNG."""

    try:
        size = path.stat().st_size
    except FileNotFoundError:
        return "screenshot file was not created"
    except OSError as exc:
        return f"could not stat screenshot: {exc}"

    if size <= MIN_PNG_SIZE:
        return f"screenshot is only {size} bytes (must be > {MIN_PNG_SIZE})"

    try:
        with path.open("rb") as png_file:
            header = png_file.read(24)
    except OSError as exc:
        return f"could not read screenshot: {exc}"

    if len(header) < 24:
        return "screenshot is too short to contain a PNG IHDR"
    if header[:8] != PNG_SIGNATURE:
        return "screenshot does not begin with the PNG signature"
    if header[12:16] != b"IHDR":
        return "screenshot does not contain IHDR as its first PNG chunk"

    width, height = struct.unpack(">II", header[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        return (
            f"screenshot dimensions are {width}x{height}; "
            f"expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )
    return None


def concise_process_error(stderr: str, stdout: str) -> str:
    """Keep Edge diagnostics useful without flooding the terminal or gallery."""

    message = stderr.strip() or stdout.strip() or "no diagnostic output"
    message = " ".join(message.split())
    if len(message) > 500:
        return message[:497] + "..."
    return message


def render_one(
    edge_path: Path, port: int, fixture_filename: str, pack: str, template: str
) -> RenderResult:
    """Render and validate one isolated fixture slide."""

    out_path = RENDERS_DIR / pack / f"{template}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    user_data_dir = Path(tempfile.mkdtemp(prefix="carousel-qa-edge-"))
    url = (
        f"http://127.0.0.1:{port}/{quote(fixture_filename)}?"
        f"{urlencode({'qa': template})}"
    )
    command = [
        str(edge_path),
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        "--window-size=1080,1350",
        f"--user-data-dir={user_data_dir}",
        "--virtual-time-budget=5000",
        f"--screenshot={out_path}",
        url,
    ]

    try:
        try:
            # subprocess.run kills and waits for its child if the timeout expires
            # or another exception interrupts communication with the process.
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=EDGE_TIMEOUT_SECONDS,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return RenderResult(
                fixture_filename,
                pack,
                template,
                False,
                f"Edge timed out after {EDGE_TIMEOUT_SECONDS} seconds",
            )
        except OSError as exc:
            return RenderResult(
                fixture_filename,
                pack,
                template,
                False,
                f"could not start Edge: {exc}",
            )

        validation_error = validate_png(out_path)
        if completed.returncode != 0:
            process_error = concise_process_error(completed.stderr, completed.stdout)
            detail = f"Edge exited {completed.returncode}: {process_error}"
            if validation_error:
                detail = f"{detail}; {validation_error}"
            return RenderResult(
                fixture_filename, pack, template, False, detail
            )
        if validation_error:
            return RenderResult(
                fixture_filename,
                pack,
                template,
                False,
                validation_error,
            )
        return RenderResult(
            fixture_filename,
            pack,
            template,
            True,
            f"valid {EXPECTED_WIDTH}x{EXPECTED_HEIGHT} PNG",
        )
    finally:
        shutil.rmtree(user_data_dir, ignore_errors=True)


def start_fixture_server() -> tuple[http.server.ThreadingHTTPServer, threading.Thread]:
    """Serve fixtures on loopback using an OS-assigned free port."""

    handler = partial(
        http.server.SimpleHTTPRequestHandler, directory=str(FIXTURES_DIR)
    )
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    server.daemon_threads = True
    thread = threading.Thread(
        target=server.serve_forever,
        name="carousel-qa-http-server",
        daemon=True,
    )
    try:
        thread.start()
    except BaseException:
        server.server_close()
        raise
    return server, thread


def render_card(result: RenderResult) -> str:
    """Build one escaped contact-sheet card."""

    label = html.escape(result.template)
    fixture = html.escape(result.fixture_filename)
    if result.ok:
        relative_png = f"{result.pack}/{result.template}.png"
        escaped_png = html.escape(relative_png, quote=True)
        preview = (
            f'<a href="{escaped_png}">'
            f'<img src="{escaped_png}" alt="{label} rendered slide" loading="lazy">'
            "</a>"
        )
        card_class = "card"
        status = '<span class="status ok">OK</span>'
    else:
        detail = html.escape(result.detail)
        preview = (
            '<div class="failed-preview">'
            '<strong>FAILED</strong>'
            f"<small>{detail}</small>"
            "</div>"
        )
        card_class = "card failed"
        status = '<span class="status bad">FAILED</span>'

    return f"""
      <article class="{card_class}">
        {preview}
        <div class="meta">
          <code>{label}</code>
          {status}
        </div>
        <div class="fixture">{fixture}</div>
      </article>"""


def write_index(results: list[RenderResult], generated_at: str) -> None:
    """Write a self-contained contact sheet grouped by pack."""

    grouped: dict[str, list[RenderResult]] = {}
    for result in results:
        grouped.setdefault(result.pack, []).append(result)

    sections: list[str] = []
    for pack, pack_results in grouped.items():
        cards = "\n".join(render_card(result) for result in pack_results)
        sections.append(
            f"""
    <section>
      <h2>{html.escape(pack)}</h2>
      <div class="grid">
{cards}
      </div>
    </section>"""
        )

    body = "\n".join(sections)
    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Instagram Carousel QA Renders</title>
  <style>
    :root {{ color-scheme: dark; font-family: system-ui, sans-serif; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; padding: 32px; background: #151515; color: #f4f4f4; }}
    header {{ margin: 0 auto 36px; max-width: 1600px; }}
    h1 {{ margin: 0 0 8px; font-size: clamp(1.8rem, 4vw, 3rem); }}
    header p {{ margin: 0; color: #aaa; }}
    section {{ margin: 0 auto 48px; max-width: 1600px; }}
    h2 {{ border-bottom: 1px solid #3a3a3a; padding-bottom: 10px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 22px; }}
    .card {{ overflow: hidden; border: 2px solid #353535; border-radius: 10px; background: #222; }}
    .card.failed {{ border-color: #e34b4b; }}
    .card a {{ display: block; background: #0d0d0d; }}
    .card img {{ display: block; width: 100%; height: auto; aspect-ratio: 4 / 5; object-fit: cover; }}
    .failed-preview {{ display: grid; min-height: 325px; place-content: center; gap: 12px; padding: 24px; background: #3a1717; color: #ffb3b3; text-align: center; }}
    .failed-preview strong {{ font-size: 1.5rem; }}
    .failed-preview small {{ max-width: 36ch; overflow-wrap: anywhere; }}
    .meta {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 12px 14px 6px; }}
    code {{ overflow-wrap: anywhere; font-size: .95rem; }}
    .fixture {{ padding: 0 14px 12px; color: #999; font-size: .78rem; overflow-wrap: anywhere; }}
    .status {{ flex: none; border-radius: 999px; padding: 3px 8px; font-size: .7rem; font-weight: 800; }}
    .status.ok {{ background: #173b25; color: #8de0a8; }}
    .status.bad {{ background: #6b2020; color: #ffd1d1; }}
  </style>
</head>
<body>
  <header>
    <h1>Instagram Carousel QA Renders</h1>
    <p>Generated at {html.escape(generated_at)}.</p>
  </header>
{body}
</body>
</html>
"""
    with (RENDERS_DIR / "index.html").open(
        "w", encoding="utf-8", newline="\n"
    ) as index_file:
        index_file.write(document)


def failed_results(work: list[WorkItem], detail: str) -> list[RenderResult]:
    """Create failure records for work that could not be attempted."""

    return [
        RenderResult(fixture, pack, template, False, detail)
        for fixture, pack, template in work
    ]


def print_summary(results: list[RenderResult], total_expected: int) -> None:
    """Print the required one-line render totals and failed identifiers."""

    ok_count = sum(result.ok for result in results)
    failures = [
        f"{result.pack}/{result.template}" for result in results if not result.ok
    ]
    failure_list = ", ".join(failures) if failures else "none"
    print(
        f"Summary: total expected={total_expected}, rendered OK={ok_count}, "
        f"failed={len(failures)}; failures={failure_list}"
    )


def finish(results: list[RenderResult], total_expected: int, generated_at: str) -> int:
    """Write the gallery, print totals, and choose the process exit code."""

    index_ok = True
    try:
        write_index(results, generated_at)
    except Exception as exc:
        index_ok = False
        print(f"ERROR: Could not write render index: {exc}", file=sys.stderr)

    print_summary(results, total_expected)
    renders_ok = len(results) == total_expected and all(
        result.ok for result in results
    )
    return 0 if index_ok and renders_ok else 1


def main() -> int:
    """Discover, render, validate, index, summarize, and clean up."""

    try:
        reset_renders_dir()
        work = discover_work()
    except (OSError, ValueError) as exc:
        print(f"ERROR: Could not prepare QA renders: {exc}", file=sys.stderr)
        print("Summary: total expected=0, rendered OK=0, failed=0; failures=none")
        return 1

    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")
    edge_path, checked_paths = locate_edge()
    if edge_path is None:
        checked = ", ".join(str(path) for path in checked_paths)
        detail = "Microsoft Edge was not found"
        print(
            "ERROR: Microsoft Edge was not found. Set EDGE_PATH to msedge.exe. "
            f"Checked: {checked}",
            file=sys.stderr,
        )
        results = failed_results(work, detail)
        return finish(results, len(work), generated_at)

    results: list[RenderResult] = []
    server: http.server.ThreadingHTTPServer | None = None
    server_thread: threading.Thread | None = None
    server_started = False
    fatal_error: Exception | None = None

    try:
        server, server_thread = start_fixture_server()
        server_started = True
        port = server.server_address[1]

        for fixture_filename, pack, template in work:
            try:
                result = render_one(
                    edge_path, port, fixture_filename, pack, template
                )
            except Exception as exc:
                result = RenderResult(
                    fixture_filename,
                    pack,
                    template,
                    False,
                    f"unexpected render error: {exc}",
                )
            results.append(result)
            marker = "OK" if result.ok else "FAIL"
            print(f"[{marker}] {pack}/{template}: {result.detail}")
    except Exception as exc:
        fatal_error = exc
    finally:
        # Each synchronous subprocess.run owns, kills on failure, and waits for
        # its Edge process before returning. The server is the only live child
        # resource that can remain at this point.
        if server is not None:
            try:
                if server_started:
                    server.shutdown()
            finally:
                server.server_close()
        if server_thread is not None:
            server_thread.join(timeout=5)

    if fatal_error is not None:
        print(f"ERROR: QA rendering stopped: {fatal_error}", file=sys.stderr)
        attempted = len(results)
        results.extend(
            failed_results(work[attempted:], f"not attempted: {fatal_error}")
        )

    return finish(results, len(work), generated_at)


if __name__ == "__main__":
    raise SystemExit(main())
