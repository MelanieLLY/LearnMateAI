# LearnMateAI 工程亮点与技术履历沉淀 (Portfolio Highlights)

本文档记录 LearnMateAI 项目在全栈与 AI 工程化演进中的核心技术亮点、架构设计、防御性反序列化流水线、AI Harness 治理与 CI/CD 安全扫描实践，供履历构建与技术面试参考。

---

## 📅 2026-03-17 ~ 2026-04-21: 结构化输出加固、云端部署冷启动提示与班级报告 (Sprint 1–2 & Post-HW Hardening)

> 本条目于 2026-09-24 依据 git 记录（repo commit b72460e）事后整理，日期区间为首个与最后一个 commit 的日期。两人团队项目：闪卡、摘要、测验三个生成 Agent 的初版、双源 Prompt 与布鲁姆分级、Gitleaks、前端 CI 与 AI PR Review 工作流由队友 Jing 实现；其余标注"本人"的内容为 MelanieLLY 的提交。

### 1. 业务背景与问题挑战 (Context & Problem)
- **多源学习数据割裂**：常见 AI 教学工具只依赖课程材料生成内容，没有把学生自己的笔记纳入生成，且生成内容缺乏认知层级上的梯度区分。
- **大模型反序列化脆弱性**：Claude 在 Tool Calling 时偶发返回 Stringified JSON、代码块围栏包裹或空数组缺陷（简答题返回 `options: []`），会触发 Pydantic 校验失败导致 HTTP 500。
- **AI 协作盲目提交隐患**：团队使用 Claude Code 编码时，Agent 可以不跑测试直接执行 git commit；初版 hook 读取的是不存在的 `$COMMAND` 环境变量且总是 `exit 0`，只能提醒、无法拦截，而 `exit 1` 只会被记为 hook 报错、命令照常执行。
- **云端冷启动与多端并行冲突**：Render 免费层后端服务闲置后休眠，首次请求需要等待唤醒（页面文案写"闲置 15 分钟休眠、2-3 分钟唤醒"，来自 Render 免费层说明，非本项目实测），前端易被误判为宕机；多前端交互模块并发开发时分支频繁冲突。

### 2. 核心架构与数据结构设计 (Data Structure & Architecture)
- **双源 Prompt 解耦架构（队友 Jing 实现）**：Prompt 模板集中于 `server/src/agents/prompts/`（`b1ff144`、`53bef1e`）；`module_content` 为模块标题加描述（上传的材料文件不会被解析），与学生最新一条笔记 `student_notes` 一起放进 user message；闪卡 prompt 要求约一半卡片来自各来源；设置 `MAX_INPUT_CHARS = 10,000`，超长时两个来源各截一半。
- **布鲁姆认知分级模型 (Bloom's Taxonomy，队友 Jing 实现)**：闪卡绑定 Bloom 6 大认知层级（Remember, Understand, Apply, Analyze, Evaluate, Create）和 1-5 难度分级；测验使用 Easy/Medium/Hard 难度，强制约束多选题（每题 4 个选项）占比 >= 60% 且至少 1 道简答题。
- **班级报告模型（本人）**：`QuizSubmission` 记录学生每次测验得分；`GET /courses/{course_id}/report` 用 `require_instructor` 鉴权并校验课程归属，用 SQL `AVG(score)` 计算课程平均分并统计选课人数；报告中的 common gaps 与模块统计目前按课程标题读取 `mock_data.json` 的演示数据。

### 3. 领域算法与性能/成本优化 (Domain Algorithm & Cost/Performance Optimization)
- **冷启动提示与数据库回退（本人）**：
  - 登录页设置 4 秒慢请求计时器，提前提示后端正在冷启动，并把 502/503/504 与网络 TypeError 映射为冷启动说明，避免用户误判服务崩溃（`client/src/pages/Login.tsx:24-66`）；
  - `server/src/database.py` 在 `DATABASE_URL` 为 postgres 连接串时连接云端 PostgreSQL，否则回退到本地 SQLite；针对 Render Postgres 断开空闲连接，开启 `pool_pre_ping` 与 `pool_recycle=3600`。
- **Vercel 反向代理与路由重写（本人）**：`client/vercel.json` 把 `/api/*` 与 `/uploads/*` 反向代理到 Render 上的 FastAPI 后端，其余路径回退到 `index.html`；前端以同源相对路径调用 API 并携带 HttpOnly cookie，无需跨域请求。

### 4. AI 系统工程与结构化输出 (LLM Engineering & Structured Outputs)
- **级联防御性反序列化流水线（本人，#38 `8719f4c` 迁移到 tool use，#40 `e7b8d49`、#6 `0fde5e4`/`97fb8c8` 加固）**：
  1. *Markdown 剥离*：正则过滤 ````json ... ```` 代码块围栏；
  2. *标准加载*：优先使用 Python 标准库 `json.loads`；
  3. *容错自修复*：捕获 `JSONDecodeError` 后降级至 `json_repair.repair_json`；
  4. *In-place Schema 变通 (Coercion)*：拦截并纠正简答题 `options: []` ➔ `None`，同时支持 `±1` 题目数量漂移容差与 2 次自动重试机制 (`_MAX_RETRIES = 2`)；重试用尽后接口返回带原因的 500。

### 5. 深度根因排查与健壮性边界设计 (Root-Cause Debugging & Defensive Architecture)
- **Claude Code PreToolUse 提交守卫（本人，`542368d`）**：
  - 排查发现旧版 hook 读取不存在的 `$COMMAND` 环境变量且总是 `exit 0`，同时确认 `exit 1` 只会被 Claude Code 记为 hook 报错、命令照常执行；
  - 改为从 stdin 读取工具调用 JSON（`INPUT=$(cat)`），命中 `git commit` 时把提示写到 `stderr` 并返回 `exit 2`，拦截经 Claude Bash 工具发出的提交并提示先运行 pytest（截图 `docs/screenshot/13_evidence_2_stop_hook.png`）。hook 本身不运行测试，定位是提交守卫。
- **Git Worktrees 并行解耦（本人）**：将仓库隔离为 `LearnMateAI-quiz-ui`（`feat/24-quiz-ui`）与 `LearnMateAI-flashcard-ui`（`feat/33-flashcard-ui`）两个独立工作区，在多终端并发开发测验状态机与 3D 翻转动画；另有一次已推送的提交被 amend 后又 pull 产生分叉，用 `git reset --hard` 回到 amend 点并 force push 恢复线性历史。
- **9 阶段 CI/CD 骨架与安全扫描**：`production.yml`（本人，`d65ec7c`）划分 Lint、Typecheck、Vitest、Pytest、Playwright E2E、npm audit + Bandit、AI PR Review、Preview Deploy、Prod Deploy 九个阶段，但各阶段之间没有依赖，命令均为软失败，后三个阶段目前是 echo 占位；真正阻断的是 `backend-ci.yml`（pytest）、队友写的 `frontend-ci.yml`（npm audit、tsc、ESLint、Vitest）与 `gitleaks.yml`，另有本人添加的 CodeQL、Bandit、Dependency Review 工作流。本人修复 CI 时把后端 CI 从预发布的 Python 3.14 固定为 3.12，在 Vitest 中排除 Playwright 的 `e2e/**`，并把 E2E 测试与种子脚本里的 mock 账号密码改为环境变量注入，配置 `.gitleaks.toml` 白名单。

### 6. 简历技术描述素材 (Ready-to-Use Resume Bullet Points)
- **English**:
  - (Teammate Jing's work, not for use as a personal bullet) Dual-source prompts blending module content and student notes, with flashcards tagged across Bloom's taxonomy levels (Remember through Create).
  - Migrated three Claude-powered generation agents to schema-enforced tool use and built a defensive JSON deserialization layer with staged recovery, in-place schema normalization, question-count tolerance, and bounded retries, so malformed model output is repaired or rejected cleanly instead of crashing quiz creation.
  - Built a Claude Code PreToolUse guard that parses tool-call input and blocks agent-issued git commits until tests are run, keeping AI-assisted commits behind an explicit test step.
  - Set up GitHub Actions workflows for linting, type checks, Vitest, Pytest, Playwright E2E, and CodeQL, Bandit, and dependency scanning; fixed recurring CI failures by pinning Python 3.12, moving test credentials into environment variables with a scoped Gitleaks allowlist, and isolating E2E specs from the unit-test runner.
- **中文**:
  - （队友 Jing 的工作，不作为本人 bullet 使用）双源 Prompt 融合模块内容与学生笔记，闪卡按布鲁姆六级认知层级与 1-5 难度生成，测验约束题型配比。
  - 将三个生成 Agent 迁移到 Claude tool use，并构建级联防御性反序列化流水线，结合正则剥离、容错自修复、简答题 Schema 规范化与题目容差重试，让格式偏差的输出能被修复入库或以明确原因返回错误。
  - 为 Claude Code 配置 PreToolUse 提交守卫，从 stdin 解析工具调用，用 `exit 2` 拦截 Agent 发起的 git commit 并提示先跑测试。
  - 搭建 9 阶段 CI/CD 骨架与 CodeQL、Bandit、Dependency Review 安全扫描，修复 Python 版本、硬编码测试凭据与 Vitest/Playwright 混跑导致的 CI 失败，并实现 Render 冷启动提示与 PostgreSQL/SQLite 环境回退。
