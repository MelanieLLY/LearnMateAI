# Agent Memory (durable project decisions)

Imported into every Claude Code session through CLAUDE.md. It holds decisions and constraints that
the code alone doesn't explain. Session-by-session logs belong in `planning_files/chathistory_P3.md`,
not here.

## When to append
Add an entry when a change in this session:
- makes a decision that later work must follow (a model, a schema, a library, a UI rule),
- uncovers a constraint by debugging (a platform limit, an API quirk), or
- reverses or replaces an earlier entry. Mark the old entry `Superseded by YYYY-MM-DD` instead of
  deleting it.

Don't add routine bug fixes, anything already obvious from the code, or secrets.
Entry format: `### YYYY-MM-DD: title`, then **Decision**, **Why**, **Where** (paths, issue/PR).
Append in the same commit as the change it describes.

---

### 2026-04-14 (Issue #38, #40): agents use forced tool_choice for structured output
**Decision**: `flashcard_agent`, `summary_agent` and `quiz_agent` call `claude-sonnet-4-6` with a
single tool and `tool_choice={"type": "tool", ...}`, then validate the tool input in Python.
**Why**: free-text JSON came back wrapped in markdown fences and broke `json.loads` (#38). Forcing
the tool makes Claude return the schema every time. Claude still sometimes returns a nested field
as a JSON string, so the agents keep a fallback parser (`json.loads`, then `json_repair`) and
coerce SA `options: []` to `None` (#40). The quiz agent retries twice (`_MAX_RETRIES`).
**Constraint**: Claude Opus 5.5, Sonnet 5.5 and Fable 5.1 return a 400 for forced `tool_choice`.
Moving the agents to one of those models means switching to `output_config.format` (JSON schema)
or `tool_choice: auto` with `strict: true`. The eval harness and the AI PR review already use
`output_config.format`.
**Where**: `server/src/agents/*.py`, `server/tests/test_*_agent.py`.

### 2026-04-20 / 2026-09-25 (deb1f4e, 7784817): cold-start handling for Render free tier
**Decision**: treat a slow or failing first request as a backend cold start, not an outage.
**Why**: the Render free-tier service sleeps when idle, and its Postgres can drop connections
while the service boots.
**Where**:
- `client/src/pages/Login.tsx`: a 4-second timer shows a "server is waking up" hint; 502/503/504
  and network `TypeError`s map to the cold-start message. Register uses the same pattern.
- `server/src/database.py`: `init_db` retries 5 times with exponential backoff (2 s base);
  `pool_pre_ping=True`, `pool_recycle=300`, `sslmode=prefer`, TCP keepalives.
- Without a postgres `DATABASE_URL`, the backend falls back to local SQLite (`learnmate.db`).

### 2026-04-20 (Issue #64): English-only UI and seed data
**Decision**: all UI strings, error messages, mock/seed data and LLM prompts are in English.
Planning docs, reflections and chat logs may stay in Chinese.
**Why**: recorded in #64 / PR #65 as a full UI translation; the reason was not written down.
Ask the owner before adding another UI language.
**Where**: `client/src/**`, `server/mock_data.json`, `server/src/agents/prompts/`.

### 2026-04 (observed 2026-09-24): uploaded material files are not parsed
**Decision**: `module_content` passed to the agents is the module title plus description.
Uploaded files under `server/uploads/` are served for download only.
**Where**: `module_content = f"{module.title}\n\n{module.description or ''}"` in
`server/src/services/flashcard_service.py`, `quiz_service.py` and `summary_service.py`.

### 2026-10-01 (Issue #76): enforced guardrails
**Decision**: guardrails are hooks and permission rules, not reminders.
- PostToolUse `Edit|Write|MultiEdit` runs `.claude/hooks/lint_edited_file.py` (ruff for
  `server/**/*.py`, eslint + tsc for `client/**/*.ts(x)`), exit 2 on failure.
- PreToolUse `Bash` commit gate runs backend pytest before any `git commit` (inline in
  `.claude/settings.json`).
- Stop hook `.claude/hooks/stop_test_gate.py` runs pytest / vitest when `server/` or `client/`
  has uncommitted changes. One retry per turn (`stop_hook_active`).
- `permissions.deny` blocks force push, hard reset, `git clean`, recursive `rm`, vercel/render
  CLIs, `psql`/`pg_dump`, Postgres URLs, and reading `.env` / `.env.*`.
- `permissions.ask` covers edits to `.claude/settings.json` and `.claude/hooks/**`.
- File rules use `Edit(path)`. `Write(path)` rules are ignored by Claude Code (the CLI prints a
  warning), so the old `Write(...)` entries were removed.
**Why**: the 2026-10-01 audit found the old lint hook matched a tool name that doesn't exist
(`WriteFile`) and the docs called the commit gate a Stop hook.
**Constraint**: Bash deny rules match the command text Claude writes; they are not a sandbox
(`bash -c '...'` or `/bin/rm` are not covered). The leading-wildcard rules also match text inside
heredocs and `echo`, so write files that mention a Postgres URL or `DATABASE_URL=` with the
Write/Edit tool instead of a shell heredoc. The ruff baseline in `server/` had 246 findings
and 39 unformatted files on 2026-10-01, so editing an old file surfaces its existing issues.

### 2026-10-01 (Issue #76): eval harness
**Decision**: `python -m src.evals.run` (from `server/`) is the eval entry point. CI runs mock mode
(recorded tool outputs through the real agent code, stub judge). `--live` runs the real agents and
the LLM judge (`claude-opus-5-5`, override with `EVAL_JUDGE_MODEL`) and costs API credits.
**Where**: `server/src/evals/`, `server/tests/test_evals.py`, `.github/workflows/backend-ci.yml`.
When a prompt or agent rule changes, update `data/golden_set.json` / `data/mock_outputs.json` and
the thresholds in `quiz_agent.py` (the checks import them).

### 2026-10-02 (Issue #78): instructor audience guidelines go into the agents' system prompts
**Decision**: `generate_quiz`, `generate_flashcards` and `generate_summary` take
`audience_context` and append it to `SYSTEM_PROMPT` through
`with_audience_guidelines` (`server/src/agents/prompts/audience.py`). The services build it from
the course's and the module's `audience_context` (`services/audience_service.py`), course first,
each level capped at 1000 characters. Empty guidelines send the base prompt unchanged.
**Why**: since #15 the field was saved on courses and modules but no agent read it, while the
README said the prompt engine used it. It goes in the system prompt, not the user turn, so it reads
as an instruction from the instructor rather than course material. The header tells the model the
guidelines shape content and tone only, so they can't loosen the output-format rules.
**Where**: `server/src/agents/prompts/audience.py`, `server/tests/test_audience_guidelines.py`,
`client/src/components/AudienceContextField.tsx` (example guidelines in `audienceExamples.ts`).
