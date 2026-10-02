---
trigger: always_on
description: Writing and naming conventions for agent-written text in this repo (commits, PRs, comments, docs)
---

# Writing Style for Agent Output

Applies to anything an agent writes into the repo or onto GitHub: commit messages, PR titles and
descriptions, issue text, code comments, docstrings and docs. Code naming rules live in CLAUDE.md
(TypeScript / Python Conventions) and are not repeated here.

## General
- Say what changed and why. Lead with the fact, skip the preamble.
- Use concrete nouns: file paths, function names, issue numbers, test counts, timings.
- Only state results you checked. "Tests pass" means you ran them in this change; otherwise write
  "not run".
- Plain English in code, commits and PRs. Docs written in Chinese stay in Chinese.
- No emoji in commit messages or code comments.

## Commit messages
- Format: `type(#issue): summary`. Types: feat, fix, refactor, docs, test, chore, perf, ci.
- Summary: imperative mood, lowercase after the colon, no trailing period, at most 72 characters.
  Good: `fix(#40): parse stringified questions before validation`.
  Bad: `Fixed some bugs and improved things.`
- Body (optional): bullets on what changed and why. Wrap at 72 characters.
- End with the attribution line the harness requires, if any.

## PR descriptions
Use these sections, in this order:
1. **Summary**: 1–3 bullets on what the PR does and why.
2. **Changes**: grouped by area (backend, frontend, CI, docs).
3. **Test plan**: commands run and their result, plus checkboxes for anything left to check by hand.
4. **Security checklist**: the "Security Acceptance Criteria" from CLAUDE.md, ticked honestly.
Link the issue with `Closes #N`. Title follows the commit summary format.

## Code comments and docstrings
- Comments explain why or a non-obvious constraint. Don't restate what the next line does.
- Point to the source of a rule when there is one: an issue number, a prompt file, a doc.
- Python: Google-style docstrings on public functions and agent modules. TypeScript: JSDoc only
  on exported functions whose behavior isn't obvious from the signature.
- No commented-out code, no `TODO` without an issue number (`TODO(#76): ...`).

## Banned filler
Don't use these words or phrases in commits, PRs, comments or docs. Replace them with the specific
fact, or delete them.

| Avoid | Write instead |
|---|---|
| comprehensive, robust, seamless, powerful, cutting-edge, state-of-the-art | what it covers or handles, with numbers |
| leverage, utilize | use |
| enhance, improve (with no detail) | the measurable change |
| best practices, industry standard (unnamed) | the specific rule |
| it's worth noting, note that, importantly, in order to | (delete) / to |
| simply, just, easily, obviously | (delete) |
| various, a number of, several (when you know the count) | the count |
| delve, dive into, journey, game-changer, elevate | (delete) |
| I hope this helps, Great question, Let me know if | (delete) |
