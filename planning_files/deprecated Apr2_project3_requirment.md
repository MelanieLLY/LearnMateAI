> [!WARNING]
> **DEPRECATED**: Due to April 8th update, this requirement is deprecated. Please refer to `Apr8_project3_requirement.md`.
Updated on Apr 08,2026.

Weight: 19% of final grade | Points: 200

## Objective
Build a production-grade, deployed application as a pair, demonstrating mastery of Claude Code's extensibility features, professional AI-assisted workflows, and production engineering practices taught in W10-W14.

## Approval Requirement
Project idea must be approved by the professor on the #projects Slack channel at least one week before the deadline.

## Requirements

### Functional Requirements
- Production-ready application solving a real problem
- 2+ user roles or distinct feature areas
- Real-world use case (new idea)
- Portfolio/interview-worthy quality
- Deployed and accessible via public URL

### Technical Requirements
- Next.js full-stack application (App Router or Pages Router)
- Database (PostgreSQL recommended, or equivalent)
- Authentication (Auth.js/NextAuth, Clerk, or equivalent)
- Deployed on Vercel (or equivalent platform with preview deploys)

### Claude Code Mastery (core of this project)
Each of the following Claude Code concepts must be demonstrated with evidence in your repository:

- **CLAUDE.md & Memory (W10):**
  - Comprehensive CLAUDE.md with @imports for modular organization
  - Auto-memory usage for persistent project context
  - Evidence of CLAUDE.md evolution across the project (visible in git history)
  - Project conventions, architecture decisions, and testing strategy documented

- **Custom Skills (W12) — minimum 2:**
  - At least 2 skills in `.claude/skills/` (e.g., /fix-issue, /add-feature, /deploy, /create-pr)
  - Evidence of team usage (session logs or screenshots)
  - At least one skill iterated from v1 to v2 based on real usage

- **Hooks (W12) — minimum 2:**
  - At least 2 hooks configured in `.claude/settings.json`
  - At least one PreToolUse or PostToolUse hook (e.g., auto-format, block protected files, lint-on-edit)
  - At least one quality-enforcement hook (e.g., Stop hook that runs tests)

- **MCP Servers (W12) — minimum 1:**
  - At least 1 MCP server integrated (database, Playwright, GitHub, or other)
  - Configuration shared via `.mcp.json` in repository
  - Evidence of use in development workflow (session logs or screenshots)

- **Agents (W12-W13) — minimum 1 (choose any):**
  - Custom sub-agents in `.claude/agents/` (e.g., security-reviewer, test-writer), OR
  - Agent teams with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, OR
  - Agent SDK feature built into the application (applying W13 patterns)
  - Evidence of use (session log, PR, or screenshots showing agent output)

- **Parallel Development (W12):**
  - Evidence of worktree usage for parallel feature development
  - At least 2 features developed in parallel (visible in git branch history)

- **Writer/Reviewer Pattern + C.L.E.A.R. (W12):**
  - At least 2 PRs using the writer/reviewer pattern (one agent writes, another reviews)
  - C.L.E.A.R. framework applied in PR reviews (visible in PR comments)
  - AI disclosure metadata in PRs (% AI-generated, tool used, human review applied)

### Test-Driven Development (W11)
- TDD workflow (red-green-refactor) for at least 3 features
- Git history showing failing tests committed before implementation
- Unit + integration tests (Vitest or Jest)
- At least 1 E2E test (Playwright)
- 70%+ test coverage

### CI/CD Pipeline (W14) — GitHub Actions
- Lint (ESLint + Prettier)
- Type checking (`tsc --noEmit`)
- Unit and integration tests
- E2E tests (Playwright)
- Security scan (npm audit)
- AI PR review (claude-code-action or claude -p)
- Preview deploy (Vercel)
- Production deploy on merge to main

### Security (W14) — minimum 4 gates from the 8-gate pipeline
- Pre-commit secrets detection (Gitleaks or equivalent)
- Dependency scanning (npm audit in CI)
- At least one SAST tool or security-focused sub-agent
- Security acceptance criteria in Definition of Done
- OWASP top 10 awareness documented in CLAUDE.md

### Team Process
- 2 sprints documented (sprint planning + retrospective each)
- GitHub Issues with acceptance criteria as testable specifications
- Branch-per-issue workflow with PR reviews
- Async standups (minimum 3 per sprint per partner)
- C.L.E.A.R. framework applied in PR reviews
- Peer evaluations

## Deliverables
- GitHub repository with full `.claude/` configuration (skills, hooks, agents, MCP)
- Deployed application (Vercel production URL)
- CI/CD pipeline (GitHub Actions, all stages passing)
- Technical blog post (published on Medium, dev.to, or similar)
- Video demonstration (5-10 min, showcasing app + Claude Code workflow)
- Individual reflections (one per partner, 500 words)
- Showcase submission via Google FormLinks to an external site. (project name, URLs, thumbnail, video, blog)

## Rubric (200 points)

### Category | Points | Description
- **Application Quality** | 40 | Production-ready, deployed, polished, real use case
- **Claude Code Mastery** | 55 | Skills, hooks, MCP, agents, CLAUDE.md/memory, worktrees, C.L.E.A.R.
- **Testing & TDD** | 30 | TDD workflow, coverage, test pyramid
- **CI/CD & Production** | 35 | Pipeline stages, AI review, Vercel deploy, security gates
- **Team Process** | 25 | Sprints, PRs, C.L.E.A.R. reviews, async standups, peer evals
- **Documentation & Demo** | 15 | README, blog post, video demo, reflections

### Bonus (up to 10 extra points)
- Property-based testing with fast-check (+3)
- Mutation testing with Stryker (+3)
- Agent SDK feature applying W13 patterns (+4)

## Note
Individual grades adjusted by peer evaluations (±10%)

## Rubric Details

### Project 3: Production Application with Claude Code Mastery Rubric

### Application Quality
**40 pts**

- **Excellent - 40 pts**
  - Production-ready, deployed on Vercel, polished UI, 2+ user roles, real problem solved, portfolio-worthy

- **Good - 30 pts**
  - Deployed, core features work, good UX, minor gaps

- **Satisfactory - 20 pts**
  - Functional app, basic UI, partially deployed

- **Needs Improvement - 10 pts**
  - Incomplete features, not deployed or broken

- **Unsatisfactory - 0 pts**
  - Major functionality broken or missing

### Claude Code Mastery
**55 pts**

- **Excellent - 55 pts**
  - Rich CLAUDE.md with @imports and git evolution; 2+ iterated skills with usage evidence; 2+ hooks enforcing quality; MCP server integrated via .mcp.json; agents (sub-agents/teams/SDK) with evidence; parallel worktree development; 2+ PRs with writer/reviewer + C.L.E.A.R. + AI disclosure

- **Good - 42 pts**
  - Functional CLAUDE.md with iteration; 2 skills and 2 hooks configured; MCP and agents present with some usage evidence; some parallel development; C.L.E.A.R. applied on some PRs

- **Satisfactory - 28 pts**
  - Basic CLAUDE.md; 1-2 skills/hooks with limited use; MCP or agents configured but minimal evidence; limited parallel work or C.L.E.A.R. usage

- **Needs Improvement - 14 pts**
  - Minimal CLAUDE.md; missing multiple Claude Code features (skills, hooks, MCP, or agents); no parallel development or C.L.E.A.R. evidence

- **Unsatisfactory - 0 pts**
  - No meaningful Claude Code extensibility demonstrated

### Testing & TDD
**30 pts**

- **Excellent - 30 pts**
  - TDD red-green-refactor for 3+ features visible in git; 70%+ coverage; unit + integration + E2E (Playwright); tests verify behavior and edge cases

- **Good - 22 pts**
  - TDD for some features; adequate coverage; unit + integration tests present; functional test quality

- **Satisfactory - 15 pts**
  - Some tests written (may be after code); low coverage; missing test types

- **Needs Improvement - 8 pts**
  - Minimal tests, no TDD evidence, trivial assertions

- **Unsatisfactory - 0 pts**
  - No meaningful testing

### CI/CD & Production
**35 pts**

- **Excellent - 35 pts**
  - All 8 pipeline stages green (lint, typecheck, tests, E2E, security, AI review, preview, prod deploy); 4+ security gates; Sentry with source maps + structured logging; issue diagnosed via monitoring

- **Good - 26 pts**
  - 5-7 pipeline stages; AI review configured; 3 security gates; Sentry configured with some logging

- **Satisfactory - 18 pts**
  - 3-4 pipeline stages; partial security scanning; basic error tracking

- **Needs Improvement - 9 pts**
  - Fewer than 3 stages; minimal security; no monitoring

- **Unsatisfactory - 0 pts**
  - No CI/CD pipeline or production infrastructure

### Team Process
**25 pts**

- **Excellent - 25 pts**
  - 2 sprints with planning + retrospectives; branch-per-issue with PR reviews; 3+ async standups/sprint/partner; C.L.E.A.R. in reviews; AI disclosure; thoughtful peer evaluation

- **Good - 19 pts**
  - 2 sprints documented; branch workflow with some PR reviews; standups present; peer evaluation completed

- **Satisfactory - 13 pts**
  - Basic sprint docs; some branching; minimal standups or reviews

- **Needs Improvement - 6 pts**
  - Incomplete sprint documentation; no structured workflow

- **Unsatisfactory - 0 pts**
  - No team process documentation

### Documentation & Demo
**15 pts**

- **Excellent - 15 pts**
  - Clear README with Mermaid architecture diagram; published blog post with AI workflow insights; polished 5-10 min screencast; 500-word reflections with specific Claude Code insights; smooth 8-10 min live demo following W14 structure

- **Good - 11 pts**
  - README present; blog post published; screencast covers main points; adequate reflections; demo mostly follows structure

- **Satisfactory - 8 pts**
  - Minimal README; draft blog or shallow screencast; short reflections; demo over/under time

- **Needs Improvement - 4 pts**
  - Missing multiple deliverables; weak demo

- **Unsatisfactory - 0 pts**
  - Missing major documentation or no demo

### Total Points
**200**