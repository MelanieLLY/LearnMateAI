#!/usr/bin/env python3
"""Stop hook: run the test suites before Claude ends a turn with uncommitted code.

When Claude finishes a turn, Claude Code pipes a JSON object on stdin. This
script checks ``git status`` for uncommitted changes (including untracked
files) and runs:

- backend pytest when files under server/ changed
- frontend vitest when files under client/ changed

If a suite fails, it exits 2 with the failing output on stderr. Claude Code
then keeps the turn going and shows that output to Claude.

Loop guard: when ``stop_hook_active`` is true, Claude is already continuing
because of an earlier block from this hook, so the script lets it stop instead
of blocking again. That gives the agent one retry per turn, not an endless loop.

Uses only the standard library so it runs on the system python3.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

SUITE_TIMEOUT_SECONDS = 240
TAIL_LINES = 60
BACKEND_SUFFIXES = (".py", ".txt", ".ini", ".toml", ".json")
FRONTEND_SUFFIXES = (".ts", ".tsx", ".js", ".mjs", ".jsx", ".json", ".css")


def project_root() -> Path:
    env_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if env_dir:
        return Path(env_dir).resolve()
    return Path(__file__).resolve().parents[2]


def changed_paths(root: Path) -> list[str]:
    proc = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all", "--", "server", "client"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    paths = []
    for line in proc.stdout.splitlines():
        # Porcelain v1: "XY path" or "XY old -> new" for renames.
        entry = line[3:].split(" -> ")[-1].strip().strip('"')
        if entry:
            paths.append(entry)
    return paths


def needs_suite(paths: list[str], prefix: str, suffixes: tuple[str, ...]) -> bool:
    ignored = (
        "server/uploads/",
        "client/dist/",
        "client/test-results/",
        "client/playwright-report/",
    )
    return any(
        p.startswith(prefix) and p.endswith(suffixes) and not p.startswith(ignored) for p in paths
    )


def python_for(server_dir: Path) -> str:
    for candidate in (
        server_dir / ".venv" / "bin" / "python",
        server_dir / "venv" / "bin" / "python",
    ):
        if candidate.is_file():
            return str(candidate)
    return "python3"


def run_suite(name: str, cmd: list[str], cwd: Path) -> str | None:
    """Run one suite. Returns None on success, or a failure report."""
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=SUITE_TIMEOUT_SECONDS
        )
    except subprocess.TimeoutExpired:
        return f"{name}: `{' '.join(cmd)}` timed out after {SUITE_TIMEOUT_SECONDS}s"
    except FileNotFoundError as exc:
        return f"{name}: could not start `{cmd[0]}` ({exc})"
    if proc.returncode == 0:
        return None
    tail = "\n".join((proc.stdout + proc.stderr).strip().splitlines()[-TAIL_LINES:])
    return f"{name} failed (`{' '.join(cmd)}` in {cwd.name}/, exit {proc.returncode}):\n{tail}"


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        payload = {}
    if payload.get("stop_hook_active"):
        return 0

    root = project_root()
    paths = changed_paths(root)
    failures = []
    if needs_suite(paths, "server/", BACKEND_SUFFIXES):
        server_dir = root / "server"
        failures.append(
            run_suite(
                "Backend pytest",
                [python_for(server_dir), "-m", "pytest", "-q", "--disable-warnings"],
                server_dir,
            )
        )
    if needs_suite(paths, "client/", FRONTEND_SUFFIXES):
        failures.append(run_suite("Frontend vitest", ["npm", "test", "--silent"], root / "client"))

    failures = [f for f in failures if f]
    if not failures:
        return 0
    print(
        "[STOP HOOK] Uncommitted changes break the tests. Fix them before ending the turn.\n\n"
        + "\n\n".join(failures),
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
