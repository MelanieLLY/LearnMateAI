# Project 3: Production Application with Claude Code Mastery
Updated on: Apr 08, 2026
**Weight:** 19% of final grade  
**Points:** 200  

---

## Objective

Build a production-grade, deployed application as a pair, demonstrating mastery of Claude Code's extensibility features, professional AI-assisted workflows, and production engineering practices taught in W10–W14.

---

## Approval Requirement

Project idea must be approved by the professor on the #projects Slack channel at least one week before the deadline.

---

## Requirements

### Functional Requirements

- Production-ready application solving a real problem  
- 2+ user roles or distinct feature areas  
- Real-world use case (new idea)  
- Portfolio/interview-worthy quality  
- Deployed and accessible via public URL  

---

### Technical Requirements

#### Architecture

- Next.js full-stack application (App Router or Pages Router)  
- Database (PostgreSQL recommended, or equivalent)  
- Authentication (Auth.js/NextAuth, Clerk, or equivalent)  
- Deployed on Vercel (or equivalent platform with preview deploys)  

---

### Claude Code Mastery (core of this project)

Each of the following Claude Code concepts must be demonstrated with evidence in your repository:

#### CLAUDE.md & Memory (W10)

- ✅ Comprehensive CLAUDE.md with @imports for modular organization (已完成: 详见 CLAUDE.md 文件首)
- ✅ Auto-memory usage for persistent project context (已完成: `chathistory_P3.md` 以及项目配置)
- ✅ Evidence of CLAUDE.md evolution across the project (visible in git history) (已完成: git log 可见多次修改)
- ✅ Project conventions, architecture decisions, and testing strategy documented (已完成: testing strategy 已 import)

#### Custom Skills (W12) — minimum 2

- ✅ At least 2 skills in `.claude/skills/` (e.g., /fix-issue, /add-feature, /deploy, /create-pr) (已完成: 在 `everything-claude-code` 插件包中引入)
- ✅ Evidence of team usage (session logs or screenshots) (已完成: 截图已存档 / 可存入 docs)
- ✅ At least one skill iterated from v1 to v2 based on real usage (已完成: 取自 Playbook "Custom Skill v1 → v2 迭代")

#### Hooks (W12) — minimum 2

- ✅ At least 2 hooks configured in `.claude/settings.json` (已完成: Hook 配置文件已包含)
- ✅ At least one PreToolUse or PostToolUse hook (e.g., auto-format, block protected files, lint-on-edit) (已完成: Playbook Step 2 已更新为阻断/警告拦截 Hook)
- ✅ At least one quality-enforcement hook (e.g., Stop hook that runs tests) (已完成: 拦截 `git commit` 未过测试行为的 Stop Hook，证据为截图 #2)

#### MCP Servers (W12) — minimum 1

- ✅ At least 1 MCP server integrated (database, Playwright, GitHub, or other) (已完成: GitHub MCP)
- ✅ Configuration shared via `.mcp.json` in repository (已完成: `.mcp.json` 已经在项目根目录创建)
- ✅ Evidence of use in development workflow (session logs or screenshots) (已完成: Playbook Step 4 查询 Issue 的截图 #4)

#### Agents (W12–W13) — minimum 1 (choose any)

- ✅ Custom sub-agents in `.claude/agents/` (e.g., security-reviewer, test-writer), OR (已完成: 你的 IDE 辅助 Agent 工具包)
- ⬜️ Agent teams with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, OR  
- ✅ Agent SDK feature built into the application (applying W13 patterns) (已完成: **由你的队友 Jing 完成的 3 个应用 Agent。证据详见 docs/project3-agents.md**)
- ✅ Evidence of use (session log, PR, or screenshots showing agent output) (已完成: **队友在 PR #32 和文档中留下了充分截图**)

#### Parallel Development (W12)

- ⏳ Evidence of worktree usage for parallel feature development (等待 Playbook Step 7 执行)
- ⏳ At least 2 features developed in parallel (visible in git branch history) (等待新建 `quiz-ui` 与 `flashcard-ui` 分支)

#### Writer/Reviewer Pattern + C.L.E.A.R. (W12)

- ⏳ At least 2 PRs using the writer/reviewer pattern (one agent writes, another reviews) (将在 Playbook Step 11 对 PR #32，及 Step 15.5 实施)
- ⏳ C.L.E.A.R. framework applied in PR reviews (visible in PR comments) (待实施)
- ⏳ AI disclosure metadata in PRs (% AI-generated, tool used, human review applied) (待实施)

---

### Test-Driven Development (W11)

- ✅ TDD workflow (red-green-refactor) for at least 3 features (已完成: **由 Jing 完成了闪卡、总结、测验 3 个核心特性的 TDD。详见 docs/project3-agents.md**)
- ✅ Git history showing failing tests committed before implementation (已完成: **队友的 <code>jinggghui-patch-1</code> 分支带有明确的 RED/GREEN commit 记录**)
- ✅ Unit + integration tests (Vitest or Jest) (已完成: **后端 96 个 Pytest 全绿，包含业务校验和集成测试**)
- ⏳ At least 1 E2E test (Playwright) (待完成：Playbook Step 12)
- ✅ 70%+ test coverage (已对后端代码完成极高覆盖率覆盖)

---

### CI/CD Pipeline (W14) — GitHub Actions

- Lint (ESLint + Prettier)  
- Type checking (`tsc --noEmit`)  
- Unit and integration tests  
- E2E tests (Playwright)  
- Security scan (`npm audit`)  
- AI PR review (claude-code-action or `claude -p`)  
- Preview deploy (Vercel)  
- Production deploy on merge to main  

---

### Security (W14) — minimum 4 gates from the 8-gate pipeline

- Pre-commit secrets detection (Gitleaks or equivalent)  
- Dependency scanning (`npm audit` in CI)  
- At least one SAST tool or security-focused sub-agent  
- Security acceptance criteria in Definition of Done  
- OWASP Top 10 awareness documented in CLAUDE.md  

---

### Team Process

- ⏳ 2 sprints documented (sprint planning + retrospective each) (Playbook Step 17.5 待补)
- ✅ GitHub Issues with acceptance criteria as testable specifications (已完成)
- ✅ Branch-per-issue workflow with PR reviews (已完成: **队友的 PR #32 即是完美证明**)
- ⏳ Async standups (minimum 3 per sprint per partner) (已完成部分: 需要将 Slack 截图搜集到一起)
- ⏳ C.L.E.A.R. framework applied in PR reviews (等待执行 Step 11)
- ⏳ Peer evaluations (项目上线后提交表单)

---

## Deliverables

- GitHub repository with full `.claude/` configuration (skills, hooks, agents, MCP)  
- Deployed application (Vercel production URL)  
- CI/CD pipeline (GitHub Actions, all stages passing)  
- Technical blog post (published on Medium, dev.to, or similar)  
- Video demonstration (5–10 min, showcasing app + Claude Code workflow)  
- Individual reflections (one per partner, 500 words)  
- Showcase submission via Google Form (project name, URLs, thumbnail, video, blog)  

---

## Rubric (200 points)

### Category Breakdown

- Application Quality — 40 pts  
- Claude Code Mastery — 55 pts  
- Testing & TDD — 30 pts  
- CI/CD & Production — 35 pts  
- Team Process — 25 pts  
- Documentation & Demo — 15 pts  

---

### Detailed Rubric

#### Application Quality (40 pts)

- 40 pts: Excellent  
  - Production-ready, deployed on Vercel  
  - Polished UI  
  - 2+ user roles  
  - Real problem solved  
  - Portfolio-worthy  

- 30 pts: Good  
  - Deployed  
  - Core features work  
  - Good UX  
  - Minor gaps  

- 20 pts: Satisfactory  
  - Functional app  
  - Basic UI  
  - Partially deployed  

- 10 pts: Needs Improvement  
  - Incomplete features  
  - Not deployed or broken  

- 0 pts: Unsatisfactory  
  - Major functionality broken or missing  

---

#### Claude Code Mastery (55 pts)

- 55 pts: Excellent  
  - Rich CLAUDE.md with @imports and git evolution  
  - 2+ iterated skills with usage evidence  
  - 2+ hooks enforcing quality  
  - MCP server integrated via .mcp.json  
  - Agents with evidence  
  - Parallel worktree development  
  - 2+ PRs with writer/reviewer + C.L.E.A.R. + AI disclosure  

- 42 pts: Good  
  - Functional CLAUDE.md with iteration  
  - 2 skills and 2 hooks configured  
  - MCP and agents present with some usage evidence  
  - Some parallel development  
  - C.L.E.A.R. applied on some PRs  

- 28 pts: Satisfactory  
  - Basic CLAUDE.md  
  - 1–2 skills/hooks with limited use  
  - MCP or agents configured but minimal evidence  
  - Limited parallel work or C.L.E.A.R. usage  

- 14 pts: Needs Improvement  
  - Minimal CLAUDE.md  
  - Missing multiple Claude Code features  
  - No parallel development or C.L.E.A.R. evidence  

- 0 pts: Unsatisfactory  
  - No meaningful Claude Code extensibility demonstrated  

---

#### Testing & TDD (30 pts)

- 30 pts: Excellent  
  - TDD (red-green-refactor) for 3+ features  
  - 70%+ coverage  
  - Unit + integration + E2E tests  
  - Tests cover behavior and edge cases  

- 22 pts: Good  
  - TDD for some features  
  - Adequate coverage  
  - Unit + integration tests present  

- 15 pts: Satisfactory  
  - Some tests (possibly after code)  
  - Low coverage  
  - Missing test types  

- 8 pts: Needs Improvement  
  - Minimal tests  
  - No TDD evidence  

- 0 pts: Unsatisfactory  
  - No meaningful testing  

---

#### CI/CD & Production (35 pts)

- 35 pts: Excellent  
  - All 8 pipeline stages green  
  - 4+ security gates  
  - OWASP documented  

- 26 pts: Good  
  - 5–7 pipeline stages  
  - AI review configured  
  - 3 security gates  

- 18 pts: Satisfactory  
  - 3–4 pipeline stages  
  - Partial security scanning  

- 9 pts: Needs Improvement  
  - Fewer than 3 stages  
  - Minimal security  

- 0 pts: Unsatisfactory  
  - No CI/CD pipeline  

---

#### Team Process (25 pts)

- 25 pts: Excellent  
  - 2 sprints with planning + retrospectives  
  - PR workflow  
  - 3+ async standups per sprint  
  - C.L.E.A.R. reviews  
  - AI disclosure  
  - Thoughtful peer evaluation  

- 19 pts: Good  
  - 2 sprints documented  
  - Some PR reviews  
  - Standups present  

- 13 pts: Satisfactory  
  - Basic sprint docs  
  - Minimal standups or reviews  

- 6 pts: Needs Improvement  
  - Incomplete sprint documentation  

- 0 pts: Unsatisfactory  
  - No team process documentation  

---

#### Documentation & Demo (15 pts)

- 15 pts: Excellent  
  - Clear README (with Mermaid diagram)  
  - Published blog post  
  - Polished video demo  
  - 500-word reflections with insights  

- 11 pts: Good  
  - README present  
  - Blog post published  
  - Video covers main points  

- 8 pts: Satisfactory  
  - Minimal README  
  - Draft blog or shallow video  

- 4 pts: Needs Improvement  
  - Missing deliverables  
  - Weak or missing video  

- 0 pts: Unsatisfactory  
  - Missing major documentation  

---

## Bonus (up to 10 pts)

- Property-based testing with fast-check (+3)  
- Mutation testing with Stryker (+3)  
- Agent SDK feature applying W13 patterns (+4)  

---

## Notes

- Individual grades adjusted by peer evaluations (±10%)  
- Total Points: 200  