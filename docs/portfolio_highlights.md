# LearnMateAI 工程亮点与技术履历沉淀 (Portfolio Highlights)

本文档记录 LearnMateAI 项目在全栈与 AI 工程化演进中的核心技术亮点、架构设计、防御性反序列化流水线、AI Harness 治理与 CI/CD 安全扫描实践，供履历构建与技术面试参考。

---

## 📅 2026-10-01: Agent 护栏从"提醒"改为可验证的强制执行 (Issue #76)

> 本人独立完成（MelanieLLY，AI 协作编写）。分支 `feat/76-enforced-agent-guardrails`，commit `65ea59e`、`ded48ae`、`319706c`、`61333cf`、`df08b71`。`.claude/agents`、`.claude/commands`、`.claude/rules/**`、`.claude/skills/*/SKILL.md` 来自第三方 everything-claude-code 插件（`3ab92d5`），本次未改动；下面的 hook、脚本、规则文件都是新写的。

### 1. 业务背景与问题挑战 (Context & Problem)
- 2026-10-01 的只读审计发现护栏大多只是提醒：PostToolUse hook 匹配的是 `WriteFile`（Claude Code 没有这个工具名，所以从未触发），而且只 echo 一句"记得跑 linter"；文档把 PreToolUse 提交守卫叫作 "Stop hook"，实际并没有 Stop hook。
- AI PR Review 工作流只把 Claude 的回复打印到日志，不发评论、不影响检查结果，还写死了模型 ID。
- Sprint plan 列了 LLM-as-judge 评测引擎，但仓库里没有任何评测代码。
- 权限放行了 `Bash(python:*)` 这类宽前缀，没有针对 force push、递归删除、部署 CLI、生产数据库的 deny 规则，也没有禁止读取 `.env`。

### 2. 核心架构与数据结构设计 (Data Structure & Architecture)
- **三类 hook 各管一个时机**（`.claude/settings.json`）：
  - PostToolUse `Edit|Write|MultiEdit` → `.claude/hooks/lint_edited_file.py`：从 stdin 读 `tool_input.file_path`，只检查这一个文件。`server/**/*.py` 跑 `ruff check` + `ruff format --check`（新加 `server/ruff.toml`，优先用 `server/.venv` 里的 ruff）；`client/**/*.ts(x)` 跑 eslint，文件在 `client/src` 且不是测试文件时再跑 `tsc --noEmit -p tsconfig.app.json`。失败时错误写 stderr 并 exit 2。
  - PreToolUse `Bash` 提交守卫：保留原样，命令含 `git commit` 时先跑 pytest，失败 exit 2。
  - Stop → `.claude/hooks/stop_test_gate.py`：`git status --porcelain` 发现 `server/` 或 `client/` 有未提交改动时分别跑 pytest / vitest，失败 exit 2 让回合继续；`stop_hook_active` 为 true 时直接放行，避免死循环（每回合最多重试一次）。
- **权限三层**：allow 收窄为 24 条具体命令（`python -m pytest *`、`npx tsc *` 等）；ask 覆盖 `.claude/settings.json` 和 `.claude/hooks/**`，agent 改护栏必须经过本人确认；deny 45 条，覆盖 force push（含 `+refspec`）、`git reset --hard`、`git clean`、递归 `rm`、vercel/render CLI、`psql`/`pg_dump`、Postgres 连接串、`DATABASE_URL=`，以及 `Read`/`Edit` 的 `.env`、`.env.*`（用 gitignore 取反 `Read(!.env.example)` 保留示例文件可读）。
- **Eval harness**（`server/src/evals/`）：`golden_set.json` 放 3 个模块（神经网络、SQL JOIN、光合作用），每个带 key terms、forbidden terms 和要求的 quiz/summary 设置；`checks.py` 是确定性检查；`judge.py` 是 LLM-as-judge 与 stub judge；`run.py` 是 CLI，输出 `eval-report.md` / `eval-report.json`。

### 3. 领域算法与性能/成本优化 (Domain Algorithm & Cost/Performance Optimization)
- **只 lint 被改的文件**：实测 Python 文件 0.14–0.17 秒，TS 文件（eslint + 全项目 tsc）1.31 秒。Stop hook 在工作区干净时 0.13 秒返回，不跑任何测试。
- **确定性检查与 agent 共用阈值**：把 `quiz_agent` 里写死的 `±1`、`0.6`、`1`、`4` 提成 `QUESTION_COUNT_TOLERANCE`、`MIN_MC_RATIO`、`MIN_SHORT_ANSWER`、`MC_OPTION_COUNT` 常量，`checks.py` 直接 import，改一处两边同步。另加了 agent 本身没有的检查：多选题正确答案必须在选项里、4 个选项不能重复、题目 id 唯一、摘要自报字数与实际字数误差 ≤15%、闪卡至少覆盖 3 个 Bloom 层级。每个模块 22 项检查（quiz 11、flashcards 6、summary 5），3 个模块共 66 项。
- **CI 零 API 成本**：mock 模式把 agent 模块里的 `anthropic.Anthropic` 替换成回放录制 tool 输出的假客户端，真实的 agent 代码（prompt 拼装、tool 输出解析、校验与重试）照常执行，所以 CI 不需要 API key。

### 4. AI 系统工程与结构化输出 (LLM Engineering & Structured Outputs)
- **按当前文档选模型和输出方式**：查了 Anthropic 当前文档，默认用 `claude-opus-5-5`。这个模型对强制 `tool_choice`（`any`/`tool`）直接返回 400，所以 PR review 和 judge 都改用 `output_config.format` 的 JSON schema 结构化输出，并开启 `fallbacks: "default"`（beta `server-side-fallback-2026-07-01`）处理拒答。模型可通过仓库变量 `AI_REVIEW_MODEL` / 环境变量 `EVAL_JUDGE_MODEL` 覆盖。
- **PR review 结构化判定**：schema 要求 `verdict`（`pass`/`block`）、`summary`、`findings[]`（severity 为 critical/high/medium/low）。`verdict` 为 block 或存在 critical 时 exit 1 让检查失败；用隐藏标记 `<!-- learnmate-ai-pr-review -->` 找到机器人已有评论并 PATCH，不会每次 push 堆一条新评论。权限只给 `contents: read` + `pull-requests: write`；fork PR 拿不到 secret 时输出 notice 后跳过。拒答、`max_tokens` 截断、输出不合法时也会更新评论说明原因并让检查失败。
- **LLM-as-judge rubric**：relevance、accuracy（以源材料为准，列出 unsupported claims）、difficulty match 三维各打 1–5 分。structured outputs 不支持数值范围约束，所以分数范围在 `parse_judge_output` 里校验，任一维低于 3 判为不通过。judge 的 client 可注入，测试里用假 client 和 httpx MockTransport 替代网络。
- **项目记忆与写作规范**：新增 `docs/agent-memory.md`（为什么强制 `tool_choice`、冷启动处理、英文 UI、上传文件不解析等决策，附"何时追加"的规则）和 `.agents/rules/writing-style.md`（commit、PR、注释格式与禁用填充词表），都从 CLAUDE.md 用 `@path` 导入。

### 5. 深度根因排查与健壮性边界设计 (Root-Cause Debugging & Defensive Architecture)
- **CLAUDE.md 的 import 一直没生效**：原文件写的是 `@import docs/learnmate-sprint-plan.md`，而文档规定的语法是 `@path`，这一行会被当成导入一个叫 `import` 的文件。已改成 `@docs/...`，并去掉了重复导入的 `testing.md`（`.claude/rules/` 本来就会自动加载）。
- **`Write(path)` 权限规则从未生效**：用 Claude Code 2.1.286 CLI 启动时它报告 7 条 `Write(...)` 规则（3 条历史遗留的 allow、4 条 deny）"is not matched by file permission checks — only Edit(path) rules are"。全部删除（每条都已有对应的 `Edit(...)`）后 CLI 不再报警；再用 Write 工具写 `client/.env.denyprobe2`，仍被 `Edit(.env.*)` 拦下。
- **hook 用自己检查自己**：写 `server/src/evals/run.py` 时 lint hook 当场报出 10 条 ruff 问题和格式 diff，按提示修完才继续，说明 hook 在真实会话里生效，不只是离线脚本能跑。
- **deny 规则的边界**：官方文档说明 Bash 规则只匹配 Claude 写出的命令文本，`/bin/rm`、`bash -c '...'` 这类写法不在覆盖范围内，已写进 CLAUDE.md 和记忆文件。反方向也有误伤：写这份文档时，一条 heredoc 命令因为正文里出现了连接串字样就被 `Bash(*postgres://*)` 整条拒绝，只能改用 Edit 工具写文件。
- **已知遗留**：按新 ruff 配置，`server/` 现有代码有 246 条问题、39 个文件未格式化（`quiz_agent.py` 因本次改动已修好）。hook 只查被编辑的文件，以后改到旧文件会先看到它原有的问题。

### 6. 验证记录 (Evidence: commands + output)
以下命令均在 2026-10-01 本地执行，输出为原样摘录（`<repo>` 代表仓库根目录）。

**Lint hook（stdin 喂样例 JSON）**
```text
$ printf '{"hook_event_name":"PostToolUse","tool_name":"Edit","tool_input":{"file_path":"<repo>/server/src/_probe_bad.py"}}' | python3 .claude/hooks/lint_edited_file.py
LINT server/src/_probe_bad.py -> exit 2 (0.17s)
src/_probe_bad.py:1:8: F401 [*] `os` imported but unused
LINT server/src/_probe_good.py -> exit 0 (0.14s)
LINT client/src/_probeBad.ts -> exit 2 (1.31s)
  1:15  error  Unexpected any. Specify a different type     @typescript-eslint/no-explicit-any
LINT docs/learnmate-sprint-plan.md -> exit 0 (0.12s)
LINT malformed stdin -> exit 0
```
首轮测试中同一类 TS 坏文件的 tsc 输出：`src/_hookProbeBad.ts(2,14): error TS2322: Type 'string' is not assignable to type 'number'.`
真实会话：用 Edit 工具改坏文件后，Claude Code 显示 `PostToolUse:Edit hook blocking error ... [LINT HOOK] server/src/_hook_probe_bad.py has problems: ruff check failed ...`。

**Stop hook 与 PreToolUse 提交守卫**
```text
STOP failing pytest -> exit 2
  [STOP HOOK] Uncommitted changes break the tests. Fix them before ending the turn.
  1 failed, 128 passed, 3 warnings in 0.60s
STOP failing vitest -> exit 2
  Tests  1 failed | 61 passed (62)
STOP stop_hook_active=true -> exit 0
STOP clean tree -> exit 0 (0.13s)
GATE git commit, failing test -> exit 2
  [TDD GATE] Tests failed or pytest is not installed. Commit blocked.
GATE git commit, passing -> exit 0   (128 passed)
GATE non-commit -> exit 0
```

**权限规则（本会话内实测，命令均无副作用）**
```text
psql --version                                                          -> denied
vercel --version                                                        -> denied
git push --force --dry-run origin HEAD:refs/heads/zz-nonexistent-probe  -> denied
git push --dry-run origin +HEAD:refs/heads/zz-nonexistent-probe         -> denied
echo <postgres URL pointing at a dpg-*.render.com host>                 -> denied
recursive rm of a nonexistent scratchpad dir                            -> denied
echo FAKE_PROBE=1 > client/.env.denyprobe                               -> denied (redirect target)
Read / cat client/.env.denyprobe (fake file)                            -> denied
Write client/.env.denyprobe2                                            -> denied
Read server/.env.example                                                -> allowed (negation rule)
对照：git push --dry-run origin HEAD:refs/heads/zz-nonexistent-probe  -> allowed
      git ls-remote origin 'refs/heads/zz-*' | wc -l                   -> 0（dry run 没有推送）
```

**AI PR review**
```text
$ node --test .github/scripts/ai-pr-review.test.mjs
ℹ tests 11
ℹ pass 11
ℹ fail 0
$ npx --yes @action-validator/cli@0.6.0 .github/workflows/ai-pr-review.yml   -> OK
# 用 @anthropic-ai/sdk@0.131.0 + 假 fetch 截获真实请求：
url: https://api.anthropic.com/v1/messages?beta=true
anthropic-beta: server-side-fallback-2026-07-01
body keys: fallbacks,max_tokens,messages,model,output_config,system
model: claude-opus-5-5 | fallbacks: default | effort: high | format: json_schema
# 本地按顺序执行 workflow 的 shell 步骤（secret 为空）：
::notice::ANTHROPIC_API_KEY is not available (fork PR or unset secret). Skipping AI review.
ANTHROPIC_API_KEY is not set (fork PR or missing secret). Skipping AI review.   exit=0
```

**Eval harness**
```text
$ cd server && python -m src.evals.run
Eval mock/stub: 9/9 artifacts, 66/66 checks passed. Report: eval_reports/eval-report.md (eval-report.json)
$ python -m pytest -q tests/test_evals.py --cov=src/evals
17 passed; src/evals TOTAL 93%
变异 1（数量容差 <= 改成 <）           -> 1 failed, 16 passed
变异 2（跳过"答案在选项中"检查）        -> 1 failed, 16 passed
# 与 CI 相同的 python:3.12-slim 容器：
128 passed, 3 warnings in 0.62s
Eval mock/stub: 9/9 artifacts, 66/66 checks passed.   eval_exit=0
```

**没有验证的部分**
- 本机没有 `act`，没有在 act 里跑完整 workflow；只用 action-validator 校验了 YAML，并在本地按顺序执行了各 shell 步骤。
- 没有用真实 API key 跑过 PR review 和 `--live` 评测（会产生费用）；GitHub 上的评论发布与检查失败要等第一个 PR 触发才能看到。
- 新的 `@path` import 是否加载，没有在新会话里确认（本机 headless CLI 未登录），需要在新会话里用 `/context` 查看。
- `ask` 规则（编辑 `.claude/settings.json` / `.claude/hooks/**` 时弹确认）按文档配置，没有在会话里触发测试。

### 7. 简历技术描述素材 (Ready-to-Use Resume Bullet Points)
- **English**:
  - Replaced reminder-only Claude Code hooks with enforced checks: a PostToolUse hook that lints only the edited file (ruff, or eslint + tsc) in 0.1–1.3 s and returns errors to the agent, plus a Stop hook that runs pytest/vitest before a turn ends with uncommitted changes.
  - Rebuilt the AI PR review around a JSON-schema structured output with a pass/block verdict: it upserts one PR comment and fails the check on critical findings, runs with least-privilege `pull-requests: write`, and skips fork PRs; covered by 11 node:test cases.
  - Built an LLM-as-judge eval harness for 3 generation agents: a 3-module golden set, 22 deterministic checks per module that share thresholds with the quiz agent, and a mockable judge, so the eval runs in CI with zero API calls.
  - Added 45 deny rules (force push, hard reset, recursive rm, deploy CLIs, production Postgres, `.env` reads) and tested each class live; found and removed 7 `Write()` permission rules that Claude Code ignored.
- **中文**:
  - 把只会提醒的 Claude Code hook 改成强制检查：PostToolUse hook 只 lint 被编辑的文件（ruff 或 eslint + tsc），耗时 0.1–1.3 秒，错误直接回传给 agent；Stop hook 在回合结束且有未提交代码时跑 pytest/vitest，失败就不让结束。
  - 重做 AI PR Review：用 JSON schema 结构化输出 pass/block 判定，只维护一条 PR 评论，有 critical 问题时让检查失败；权限只给 `pull-requests: write`，fork PR 自动跳过；11 个 node:test 用例覆盖。
  - 为 3 个生成 agent 搭建 LLM-as-judge 评测：3 个模块的 golden set、每个模块 22 项与 quiz agent 共用阈值的确定性检查、可 mock 的 judge，CI 中零 API 调用即可运行。
  - 新增 45 条 deny 规则（force push、hard reset、递归删除、部署 CLI、生产 Postgres、读取 `.env`）并逐类实测；排查出 7 条被 Claude Code 忽略的 `Write()` 权限规则并删除。

---

## 📅 2026-09-28: 关键前端流程的组件测试补齐 (Issue #72, PR #73)

> 本人独立完成（MelanieLLY，AI 协作编写）。commit `9d55326`，分支 `test/72-frontend-critical-flow-tests`。

### 1. 业务背景与问题挑战 (Context & Problem)
- 前端此前只有 `StudentModuleView`、`QuizTakingView` 两个测试文件（20 个用例），路由守卫、注册、登录、教师仪表盘这四个每个用户都会走到的流程都没有测试。
- 登录和注册的冷启动提示靠一个 4 秒的 `setTimeout` 实现，要验证"慢请求才提示、快请求不提示、慢请求失败后提示被真实错误替换"，靠手动点击基本测不到。

### 2. 核心架构与数据结构设计 (Data Structure & Architecture)
- **按路由隔离测试守卫**：用 `vi.mock` 替换 `useAuth`，在 `MemoryRouter` 里挂上 `/login`、`/404` 两个桩页面，断言最终渲染的是哪一页，而不是断言内部调用。覆盖未登录、`isAuthenticated` 为真但 `user` 为空、角色不符、角色符合、不限角色 5 种状态，外加加载中状态。
- **按 URL 分发的 fetch 桩**：仪表盘挂载时会并发请求 modules、courses，再对每个模块请求 materials 和 quizzes；测试用一个按 URL 返回不同数据的 `mockImplementation`，一份配置就能组合出空数据、空班级、请求失败等场景。
- **可访问性小改动**：仪表盘的加载骨架屏原来只是几个没有文字的 `div`，测试和屏幕阅读器都找不到。加上 `role="status"` 与 `aria-label="Loading dashboard"`，测试改用 `getByRole('status')` 查询。

### 3. 领域算法与性能/成本优化 (Domain Algorithm & Cost/Performance Optimization)
- 本次不涉及算法改动。测试全部用桩替代网络请求，0 次真实 API 调用，61 个前端用例本地约 1.4 秒跑完。

### 4. AI 系统工程与结构化输出 (LLM Engineering & Structured Outputs)
- 本次不涉及 LLM 调用。

### 5. 深度根因排查与健壮性边界设计 (Root-Cause Debugging & Defensive Architecture)
- **假时钟测试冷启动计时器**：用 `vi.useFakeTimers()` 精确推进时间，断言 3999ms 时没有提示、4000ms 时出现提示；快请求在计时器触发前返回时提示不会出现；慢请求最后返回 401 时，冷启动提示会被真实错误替换，按钮也恢复可点击。
- **错误分支全覆盖**：登录和注册都覆盖了后端 `detail` 错误、没有 detail 时的通用提示、返回 HTML（非 JSON）的 500、502/503/504 网关错误、`TypeError` 网络错误 5 类情况；注册还覆盖了密码长度边界（5 位拦截且不发请求，6 位放行）。
- **变异验证测试有效性**：分别把角色不符的跳转改成 `/login`、慢请求阈值 4 秒改成 8 秒、密码最短长度 6 改成 5、仪表盘加载状态永不结束，每次都有对应测试失败（1/2/1/5 个），确认测试真的在检查行为，而不是只把代码跑一遍。

### 6. 简历技术描述素材 (Ready-to-Use Resume Bullet Points)
- **English**:
  - Added 41 Vitest + React Testing Library tests covering route guarding, registration validation, login cold-start handling, and instructor dashboard loading/empty/error states, tripling frontend test count from 20 to 61.
  - Tested a 4-second cold-start warning timer with fake timers, asserting no hint at 3,999 ms, a hint at 4,000 ms, and replacement by the real error when a slow request fails.
  - Checked the tests with manual mutations (wrong-role redirect, timer threshold, password minimum, stuck loading state); each broken behavior failed its tests.
- **中文**:
  - 用 Vitest + React Testing Library 新增 41 个组件测试，覆盖路由守卫、注册校验、登录冷启动提示与教师仪表盘的加载/空/错误状态，前端用例从 20 个增加到 61 个。
  - 用假时钟测试 4 秒冷启动提示计时器，精确断言 3999ms 无提示、4000ms 出现提示、慢请求失败后提示被真实错误替换。
  - 通过手动变异（改错跳转目标、计时阈值、密码下限、加载状态）检验测试有效性，每处改坏都有对应用例失败。

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
