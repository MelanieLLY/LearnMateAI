#!/usr/bin/env python3
"""PostToolUse hook: lint the file Claude just edited.

Claude Code pipes the tool call as JSON on stdin. This script reads
``tool_input.file_path`` and runs only the checker for that file:

- ``server/**/*.py``: ``ruff check`` and ``ruff format --check`` (config: server/ruff.toml)
- ``client/**/*.ts(x)``: ``eslint`` on the file, then ``tsc --noEmit`` on the app
  project when the file is under client/src and is not a test file

Exit codes follow the Claude Code hook contract: 0 means clean or not
applicable; 2 means the checker failed, and stderr is shown to Claude so it can
fix the file. The tool call has already run, so exit 2 does not undo the edit.

Uses only the standard library so it runs on the system python3.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

CHECK_TIMEOUT_SECONDS = 60
MAX_OUTPUT_CHARS = 4000
TS_SUFFIXES = (".ts", ".tsx")
TEST_MARKERS = (".test.", ".spec.")


def project_root() -> Path:
    env_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if env_dir:
        return Path(env_dir).resolve()
    return Path(__file__).resolve().parents[2]


def find_ruff(server_dir: Path) -> list[str] | None:
    for candidate in (server_dir / ".venv" / "bin" / "ruff", server_dir / "venv" / "bin" / "ruff"):
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return [str(candidate)]
    on_path = shutil.which("ruff")
    return [on_path] if on_path else None


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=CHECK_TIMEOUT_SECONDS
        )
    except subprocess.TimeoutExpired:
        return 1, f"{' '.join(cmd)} timed out after {CHECK_TIMEOUT_SECONDS}s"
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def lint_python(file_path: Path, server_dir: Path) -> list[str]:
    ruff = find_ruff(server_dir)
    if ruff is None:
        return [
            "ruff is not installed. Run: cd server && .venv/bin/pip install -r requirements-dev.txt"
        ]
    errors = []
    code, out = run([*ruff, "check", "--output-format", "concise", str(file_path)], server_dir)
    if code != 0:
        errors.append(f"ruff check failed:\n{out}")
    code, out = run([*ruff, "format", "--check", "--diff", str(file_path)], server_dir)
    if code != 0:
        errors.append(
            f"ruff format --check failed (fix with: cd server && ruff format {file_path}):\n{out}"
        )
    return errors


def lint_typescript(file_path: Path, client_dir: Path) -> list[str]:
    bin_dir = client_dir / "node_modules" / ".bin"
    eslint, tsc = bin_dir / "eslint", bin_dir / "tsc"
    if not eslint.is_file():
        return ["client/node_modules is missing. Run: cd client && npm ci"]
    errors = []
    code, out = run([str(eslint), str(file_path)], client_dir)
    if code != 0:
        errors.append(f"eslint failed:\n{out}")
    relative = file_path.relative_to(client_dir).as_posix()
    is_app_source = relative.startswith("src/") and not any(
        m in file_path.name for m in TEST_MARKERS
    )
    if is_app_source and tsc.is_file():
        code, out = run([str(tsc), "--noEmit", "-p", "tsconfig.app.json"], client_dir)
        if code != 0:
            errors.append(f"tsc --noEmit -p tsconfig.app.json failed:\n{out}")
    return errors


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    file_value = (payload.get("tool_input") or {}).get("file_path")
    if not file_value:
        return 0

    root = project_root()
    file_path = Path(file_value)
    if not file_path.is_absolute():
        file_path = Path(payload.get("cwd") or root) / file_path
    file_path = file_path.resolve()
    if not file_path.is_file():
        return 0

    server_dir, client_dir = root / "server", root / "client"
    skip_parts = {"node_modules", ".venv", "venv", "dist"}
    if skip_parts.intersection(file_path.parts):
        return 0

    if file_path.suffix == ".py" and is_under(file_path, server_dir):
        errors = lint_python(file_path, server_dir)
    elif file_path.suffix in TS_SUFFIXES and is_under(file_path, client_dir):
        errors = lint_typescript(file_path, client_dir)
    else:
        return 0

    if not errors:
        return 0
    report = "\n\n".join(errors)
    if len(report) > MAX_OUTPUT_CHARS:
        report = report[:MAX_OUTPUT_CHARS] + "\n... (output truncated)"
    print(f"[LINT HOOK] {file_path.relative_to(root)} has problems:\n{report}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
