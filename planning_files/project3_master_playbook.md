# 🏆 Project 3: 满分起飞终极操作手册 (The Master Playbook)

> **最终修订版 (Apr 8)**
> 本手册经过对照 Apr 8 最新 Requirement 的全面 Gap 审查。覆盖老师所有要求，按步骤无脑执行即可。
>
> **格式说明：**
> - 发给 **Antigravity (AG)** 的 prompt → 中文
> - 发给 **Claude Code 终端** 的 prompt → 英文
> - 📸 标记处需要截图或文字证据，编号连续
>
> **已完成项（HW4/HW5）：**
> - ✅ TDD 红绿灯 — 3 个 feature（Issue #2 Module CRUD, Student Notes, Flashcard）
> - ✅ Custom Skill v1 → v2 迭代（add-feature-skill）
> - ✅ MCP 连接 GitHub（有截图证据）
> - ✅ Agents 配置（30 个 agent 文件）
> - ✅ CLAUDE.md 多次 git evolution
>
> **独自完成策略：**
> 所有需要两人协作的证据（standup、PR review），由我 + AI 工具完成。
> AI PR review (Copilot / claude-code-action) 同时满足 writer/reviewer pattern 和 AI disclosure 要求。

---

## 🗂️ 核心 Issue 消化路线图 (Execution Roadmap)

### 【Phase 0: 前期修补 (Day 0)】
0. 修复坏掉的配置和路径，让后续步骤能正常运行。

### 【Phase 1: 拿满 Claude Code Mastery 证据 (Day 1-2)】
1. **Issue #22**: `docs: Claude Code Mastery artifacts` —— Hook截图、Agent调用截图、MCP截图。

### 【Phase 2: 收尾基础核心 (Day 2-3)】
2. **Issue #9, #16**: 收尾前置 UI 任务。

### 【Phase 3: TDD 炫技与 Worktree 并行开发核心 AI 功能 (Day 3-7)】
~~3. **Issue #23**: `feat(backend): Quiz generation & storage API` —— TDD 流程。~~ (已由 Jing 完成，截图拿现成的)
~~4. **Issue #24**: `feat(frontend): Quiz taking UI and feedback loop`。~~
~~5. **Issue #4**: `Agentic Content Generation` —— 闪卡、总结等。~~
3. **Issue #24**: `feat(frontend): Quiz taking UI` (并行特性 A)
4. **Issue #33**: `feat(frontend): Flashcard & Summary UI` (并行特性 B)

### 【Phase 4: QA 保障 (Day 7-8)】
6. **Issue #21**: `test: Set up Playwright for E2E tests`。
7. **Issue #6 & #7**: `Instructor report` + `System Eval`。

### 【Phase 5: DevSecOps + CI/CD + 部署 (Day 8-10)】
8. **Issue #20**: `chore: CI/CD Pipeline & Security Gates` —— 8 个 stage + 4 安全门。
9. **Issue #8**: `Feature: Production & Polish` —— Render DB + Vercel 部署。

### 【Phase 6: 交付打包 (Day 10-12)】
10. Readme、博客、视频、Reflection、Google Form。

---

## 📜 详细步骤执行与 Prompt 复制清单

---

### 【Phase 0：一次性修补】

**🎯 Step 0-1: Commit 文件夹重命名** ✅
- **操作**: 把 `planning files` → `planning_files` 的改名正式 commit，否则 GitHub 上引用全部断裂。

<details>
<summary>👉 点击查看指令详情</summary><br>
发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，请帮我把 <code>planning files</code> 改名为 <code>planning_files</code> 的变更 commit 到 Git。commit message 用 <code>chore: rename planning files to planning_files for path compatibility</code>。</blockquote>
</details>

**🎯 Step 0-2: 修复 CLAUDE.md 路径 + 增加 @import**  ✅
- **操作**: 修复坏掉的 `@import` 引用，增加 testing strategy 引用。

<details>
<summary>👉 点击查看指令详情</summary><br>
发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，请修复 CLAUDE.md 中的 @import 路径：
1. <code>@import project_proposal.md</code> 改为 <code>@import planning_files/project3_proposal.md</code>
2. <code>@import "planning files/learnmate-sprint-plan.md"</code> 改为 <code>@import planning_files/learnmate-sprint-plan.md</code>
3. 新增 <code>@import .claude/rules/common/testing.md</code>（这是我们的 testing strategy 文档）
4. 在 CLAUDE.md 中新增一个 <code>## Security — OWASP Top 10</code> 段落，简要列出 OWASP Top 10 及我们的对应防护措施（如 SQL injection → ORM 参数化查询, XSS → React 自动转义 等）。
不要改动 CLAUDE.md 中其他已有内容。
</blockquote>
</details>

---

### 【Phase 1：拿满 "Claude Code Mastery" 证据】

**🎯 Step 1: 高频团队站会 (Async Standups)** （持续进行）
- **操作**: 每天在群里发消息汇报。

<details>
<summary>👉 点击查看指令详情</summary><br>
此步骤无需发送给 AI。<br>
你复制给队友的 Slack 消息：<br>
<blockquote><em>Team, today I worked on Issue 22. Claude Hooks are configured. No blockers.</em></blockquote>
📸 截好这段对话的图 (证据 #1)。<br>
</details>

**🎯 Step 1.5: 引入 everything-claude-code 插件环境与工作流 (遵循 Scrum Flow)** ✅
- **操作**: 严格按照项目研发规范（开 Issue -> 切分支 -> 部署工具 -> 记录日志 -> 提 PR）来部署自动化组件。
- **状态**: PR #26 已 merge（插件文件已导入），但 chat history hook 和 PR 流程可能未完成。

<details>
<summary>👉 点击展开行动指令 (与执行流程)</summary>
标准化建档 (不跳过任何规则):
    <ul>
    <li>建立专属 Issue，例如：<code>gh issue create --title "chore: Setup everything-claude-code plugins and hooks" ...</code></li>
    <li>根据 Issue 编号切出分支：<code>git checkout -b chore/XX-setup-plugins</code></li>
    </ul>
安装与配置插件 (避坑手动模式):
    <ul>
    <li>开启 <code>claude</code> 终端输入命令获取作业必需的生态调用截图（只需一条即可证明）：<br>
        <code>/plugin marketplace add affaan-m/everything-claude-code</code></li>
    <li>（由于官方下载器 Bug）请直接前往 Github 下载 <code>everything-claude-code</code> 源码压缩包。</li>
    <li>提取并手动将以下精选组件复制粘贴至本项目的 <code>.claude/</code> 目录下：<br>
        <ul>
        <li><strong>Rules (规则):</strong> <code>rules/common/</code>, <code>rules/typescript/</code>, <code>rules/python/</code></li>
        <li><strong>Agents (人设分身):</strong> <code>agents/tdd-guide.md</code>, <code>agents/e2e-runner.md</code>, <code>agents/code-reviewer.md</code>, <code>agents/doc-updater.md</code>, <code>agents/database-reviewer.md</code></li>
        <li><strong>Skills (加强光盘):</strong> <code>skills/tdd-workflow/</code>, <code>skills/frontend-patterns/</code>, <code>skills/backend-patterns/</code></li>
        <li><strong>Commands (快捷指令):</strong> <code>commands/tdd.md</code>, <code>commands/e2e.md</code>, <code>commands/plan.md</code>, <code>commands/eval.md</code></li>
        </ul>
    </li>
    </ul>
配置自动写入 chathistory 的 Hook:
    <ul>
    <li>在 <code>settings.json</code> 中配置一个钩子，使得每次退出 <code>claude</code> 终端时，由 Hook 提醒用户运行 <code>/chat-history-log</code> 来保存日志到 <code>planning_files/chathistory_P3.md</code>。</li>
    </ul>
沟通历史存档与 PR 交接:
    <ul>
    <li>结束对话时，确保大模型更新了 <code>chathistory_P3.md</code>。</li>
    <li>通过常规流程 Commit 代码并在 GitHub 提交 PR，标记 <code>Closes #XXX</code>。</li>
    </ul>
</details>

**🎯 Step 2: Hooks 修复 + MCP 迁移 + CLAUDE.md 更新 (Issue #22)** ✅ （已完成）
- **操作**: 修改 Stop Hook 为真正的拦截、将 MCP 配置迁移到项目级、触发 hook 截图。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>
<strong>Step 2a — 修复 Stop Hook（发给 Claude Code 终端，英文）：</strong> ✅ 已完成<br>
<blockquote><em>Please update our <code>.claude/settings.json</code>. Change the PreToolUse hook for "Bash" so that when the command contains "git commit", it prints a warning "🛑 [STOP HOOK] Tests must pass before commit! Run: cd server && pytest" and exits with code 1 (blocking the commit). Keep the existing PostToolUse hooks unchanged. This is a quality-enforcement Stop hook.</em></blockquote>
<strong>Step 2b — 触发 Stop Hook 截图（发给 Claude Code 终端，英文）：</strong> ✅ 已完成<br>
<blockquote><em>Now try to run <code>git commit -m "test hook"</code> so I can see the Stop hook blocking it.</em></blockquote>
📸 截取终端里 hook 拦截成功并显示 "🛑 [STOP HOOK]" 的画面 (证据 #2)。<br>
<strong>Step 2c — 迁移 MCP 到项目级（在你自己的终端执行）：</strong><br>
<blockquote><code>claude mcp add-json --scope=project github '{"type":"http","url":"https://api.githubcopilot.com/mcp","headers":{"Authorization":"Bearer PLACEHOLDER_TOKEN"}}'</code></blockquote>
这会在项目根目录生成 <code>.mcp.json</code> 文件。确保它被 git add 并 commit。Token 留 placeholder，实际值通过环境变量注入。<br>
</details>

**🎯 Step 3: 调用 Doc Review Agent (Issue #22)** ✅
- **操作**: 召唤代理检查文档，截图证据。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>
发送给 [Claude Code 终端] (英文):<br>
<blockquote><em>Act as the agent defined in <code>.claude/agents/doc-reviewer.md</code>. Read my <code>README.md</code> and check if it has formatting issues or missing sections.</em></blockquote>
📸 截图它以专家口吻回复的画面 (证据 #3)。<br>
</details>

**🎯 Step 4: MCP 连接抓取外部数据 (Issue #22)** ✅
- **操作**: 用 MCP 工具查看 GitHub 状态。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>
发送给 [Claude Code 终端] (英文):<br>
<blockquote><em>Use github MCP tool to list top 3 open issues for this repo.</em></blockquote>
📸 截图带有 Tool Use 标志的终端交互画面 (证据 #4)。<br>
</details>

---

### 【Phase 2：收尾基础模块与视觉体系 (Sprint 1 遗留项落成)】

**🎯 Step 5: 学生端模块浏览与笔记骨架 (Issue #16)** ✅ （已完成）
> 💡 **NOTE (开发纪要)**: 在进行本阶段 (Phase 2 - Step 5) 开发时，我们发现当前全栈系统中并未建立 `Student` 加入 `Course` 的 `Enrollment` 从属关系表，且获取模块数据的后端接口严格锁定了讲师权限。故此处我们仅完成了前端接入 UI 骨架。此“将学生连入新建班级”的动态权限与模型连接逻辑，留待之后的环节（如 Phase 4）再行彻底搭建。
- **操作**: 对接前后端的数据。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>
发送给 [Antigravity] (中文):<br>
<blockquote>嘿 Antigravity，开始执行 Playbook Step 5。请对接学生端前台的 <code>/notes</code> 模块，写好 <code>StudentModuleView.tsx</code> 组件，并保证无 <code>any</code> TS 类型错误，顺利完成功能即可。</blockquote>
</details>

**🎯 Step 6: 全局 UI 动态润色与过渡 (Issue #16)** ✅ （已完成）
- **操作**: 搞定面试/作品集质量要求。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>
发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，执行 Step 6。请为所有组件做交互增强：引入毛玻璃效果 (backdrop-blur)，加载时的骨架屏 (Loading skeleton) 及响应状态。保证达到 "portfolio-worthy" 的视觉标准。</blockquote>
</details>

---

### 【Phase 3：实际 AI 开发期 (TDD + Worktree)】

**🎯 Step 7: 展现 Parallel Development (Git Worktrees)** ✅ （已完成）
~~- **操作**: 拆分工程物理文件夹。~~
~~<details>~~
~~<summary>👉 点击展开行动指令 (Prompt)</summary><br>~~
~~发送给 [Antigravity] (中文):<br>~~
~~<blockquote>Antigravity，为了完成 Worktree 要求，请通过命令行跑 <code>git worktree add</code> 帮我分出 <code>../LearnMateAI-quiz-backend</code> (Issue 23) 和前端 (Issue 24) 两个并行目录。跑完后用命令打印出列表。</blockquote>~~
~~📸 截取 <code>git worktree list</code> 输出 (证据 #5)。<br>~~
~~</details>~~

- **操作 (New)**: 因为后端被做完了，我们需要开两个纯前端的 Issue 分支来证明“并行开发 (Parallel Development)”，这就完全满足“2 features developed in parallel”这一得分点！

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>
发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，我的队友把后端全做完啦！为了满足得分点 "At least 2 features developed in parallel (visible in git branch history)"，请帮我通过 <code>git worktree add</code> 分出 <code>../LearnMateAI-quiz-ui</code> 和 <code>../LearnMateAI-flashcard-ui</code> 两个前端并行开发目录。跑完后打印出列表。</blockquote>
📸 截取 <code>git worktree list</code> 输出 (证据 #5)。<br>
</details>

**🎯 Step 7.5: 安装前端测试框架 (前置依赖)** ✅ （已完成）
- **操作**: 安装 vitest + testing-library + playwright，为后续所有测试步骤做准备。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>
发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，在开始 TDD 之前，请先帮我安装前端测试框架依赖：
1. 在 <code>client/</code> 下安装 vitest、@testing-library/react、@testing-library/jest-dom、@testing-library/user-event、jsdom
2. 安装 @playwright/test 并运行 <code>npx playwright install chromium</code>
3. 创建 <code>client/vitest.config.ts</code> 基础配置（使用 jsdom environment）
4. 在 <code>client/package.json</code> 的 scripts 中加上 <code>"test": "vitest"</code> 和 <code>"test:e2e": "playwright test"</code>
5. 确认 <code>npm test</code> 可以正常运行（即使还没有测试文件也不应报错）</blockquote>
</details>

**🎯 Step 8: TDD 提交流程 - Quiz API (Issue #23)** （✅ 已由 Jing 完成）
~~- **操作**: 写代码，但要卡两次截图。~~
~~> 💡 TDD 红绿灯我们已经有 3 个 feature 达标了（Module CRUD + Student Notes + Flashcard）。Quiz 这次 TDD 是额外保险，但流程上走一遍不费力。~~

~~<details>~~
~~<summary>👉 点击展开行动指令 (Prompt)</summary><br>~~
~~<em>(分为红绿两步)</em><br>~~
~~【红灯步】发送给 [Antigravity] (中文):<br>~~
~~<blockquote>Antigravity，执行 Step 8 前半段。故意只写一个名为 <code>test_quiz.py</code> 会失败的 Pytest 用例，然后执行红字 commit。</blockquote>~~
~~📸 截图终端的红字 (证据 #6)<br>~~
~~【绿灯步】发送给 [Antigravity] (中文):<br>~~
~~<blockquote>Antigravity，执行 Step 8 后半段。写出带 <code>hints</code> 字段的真 Quiz 以及测评结果保存接口，将测试通过。提交绿灯 commit。</blockquote>~~
~~📸 截图 pytest 全绿画面 (证据 #7)<br>~~
~~</details>~~

- **操作 (New)**: 直接去 `docs/project3-agents.md` 里拿队友已经截好的图！躺赢：
📸 取用队友的 TDD RED 报错截图 (证据 #6)
📸 取用队友的 TDD GREEN 和 96 Tests Paasing 全绿截图 (证据 #7)

**🎯 Step 9 & 10: 展现 Parallel Development (双开终端进行 UI 开发)**
> *这是核心大招！请同时打开两个终端进行以下操作来向教授展示绝对的并行拉拔！*

| 🟩 终端 A (Feature: Quiz UI)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | 🟦 终端 B (Feature: Flashcards & Summary UI)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **对应 Issue**: #24<br>**工作区**: `../LearnMateAI-quiz-ui`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | **对应 Issue**: #33<br>**工作区**: `../LearnMateAI-flashcard-ui`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **对应 Issue**: #24<br>**工作区**: `../LearnMateAI-quiz-ui` | **对应 Issue**: #33<br>**工作区**: `../LearnMateAI-flashcard-ui` |
| **目标**: 配合后端建立单题翻页并带有趣味反馈的学生答题卡。 | **目标**: 对接基于大模型的学习资料总结，并搭建精美的记忆卡翻转 3D 界面。 |
| **启动**: `cd ../LearnMateAI-quiz-ui && claude` | **启动**: `cd ../LearnMateAI-flashcard-ui && claude` |
| **发给终端的 Prompt**:<br><blockquote>**[Context Initializer]**<br>We are executing an academic rubric: "2 features developed in parallel, visible in git history". You are currently operating inside a physical Git Worktree folder (`LearnMateAI-quiz-ui`) linked to the main repository.<br><br>**[Your Tasks]**<br>1. Run `git rebase main` first to sync the testing frameworks I just installed on the main branch.<br>2. Implement the interactive Quiz UI (`QuizTakingView.tsx`) over the ready `/quizzes` backend API. Show one question at a time, and display an animated LLM feedback & score badge upon submission!</blockquote> | **发给终端的 Prompt**:<br><blockquote>**[Context Initializer]**<br>We are executing an academic rubric: "2 features developed in parallel, visible in git history". You are currently operating inside a physical Git Worktree folder (`LearnMateAI-flashcard-ui`) linked to the main repository.<br><br>**[Your Tasks]**<br>1. Run `git rebase main` first to sync the testing frameworks I just installed on the main branch.<br>2. Build a premium 3D flippable card UI to display flashcards, and a section for module summaries (`StudentModuleView.tsx`) over the ready backend APIs. Ensure dynamic, smooth animations!</blockquote> |
| 待代码跑通后，发送：<br><blockquote>Great! Now stage all files and commit them with message: `feat(#24): implement interactive Quiz UI`. Then run `git push origin HEAD` to push this parallel branch!</blockquote> | 待代码跑通后，发送：<br><blockquote>Great! Now stage all files and commit them with message: `feat(#33): implement 3D flashcards and summary UI`. Then run `git push origin HEAD` to push this parallel branch!</blockquote> |
| **📸 最终需截取的证据** | **📸 最终需截取的证据** |
| 截取这个终端正在生成 Quiz UI 代码的画面。 | 截取生成 Flashcard 过程；以及并排展现这俩终端正在跑代码的画面 (证据 #7b) |

> 🌟 **Bonus (可选): 丰富的 PR Description**
> 如果你想把这两个并行分支也当做 "C.L.E.A.R." 评分点的防备选项，可以在提 PR 时直接把下面的文案分别复制进它们的 Description 里：
> 
> **For Quiz UI (Issue #24):**
> ```markdown
> ## Implementation Summary
> Closes #24. Introduces interactive Quiz UI over the backend API.
> 
> ## C.L.E.A.R. Description
> - **C**ontext: Adds frontend React view to match the Quiz API.
> - **L**ogic: Handles loading states, progression, and LLM explanation parsing.
> - **E**vidence: Vitest UI interaction tests are written and passing.
> - **A**rchitecture: Follows established component composition.
> - **R**isk: Low. Defensive UI checks applied.
> 
> **AI Disclosure:** UI Code ~90% generated by Antigravity (Writer).
> ```
>
> **For Flashcard UI (Issue #33):**
> ```markdown
> ## Implementation Summary
> Closes #33. Builds premium 3D flippable card UI to display LLM flashcards.
> 
> ## C.L.E.A.R. Description
> - **C**ontext: Addresses the Flashcards requirement for parallel development.
> - **L**ogic: Implements smooth 3D CSS rotate transforms.
> - **E**vidence: Local unit tests verify initial rendering.
> - **A**rchitecture: Components extracted logically (FlashCard3D, FlashcardSection).
> - **R**isk: Low risk. Localized CSS scoping.
> 
> **AI Disclosure:** UI Code ~90% generated by Antigravity (Writer).
> ```

**🎯 Step 11: 提交 PR 并做第一次 C.L.E.A.R. 审查 ⭐** （未开始）
~~提交 PR 后，在 GitHub PR 页面留下以下 comment：<br>~~
~~<blockquote>~~
~~<strong>C.L.E.A.R. Review</strong><br><br>~~
~~C: Follows existing FastAPI module pattern (router → service → model) ✅<br>~~
~~L: Edge cases handled — empty quiz, unauthorized access, module not found ✅<br>~~
~~E: 6 pytest tests passing, TDD red→green visible in git history ✅<br>~~
~~A: Consistent with established Model→Schema→Service→Router pattern ✅<br>~~
~~R: No hardcoded secrets, input validated via Pydantic schemas ✅<br><br>~~
~~<strong>AI Disclosure:</strong> ~85% AI-generated using Antigravity + Claude CLI. Human reviewed all test logic and security checks.~~
~~</blockquote>~~
~~📸 截图 GitHub PR 页面上的这段 comment (证据 #8)。<br>~~
~~</details>~~

- **操作 (New)**: 我们需要满足 "one agent writes, another reviews" 这一得分点！由于代码是 AI 写的 (Writer)，你需要召唤专属的智能审查分身 (Reviewer) 来自动生成 Review 内容。去队友被 Merge 的 **PR #32** 底下留言。
<details>
<summary>👉 点击展开行动指令 (必须使用终端执行)</summary><br>
打开一个新的终端，输入 <code>claude</code> 唤起对话后，发送以下指令让其扮演 Reviewer 查阅代码差距：
<blockquote><em>Please act as the expert agent defined in <code>.claude/agents/code-reviewer.md</code>. I need you to review PR #32 which merges the branch 'jinggghui-patch-1'. Please provide your review comment strictly structured using the C.L.E.A.R framework (Context, Logic, Evidence, Architecture, Risk). Ensure to append this exact disclosure at the bottom of your output: "AI Disclosure: PR Code ~90% generated by Antigravity (Writer). Review autonomously generated by Code-Reviewer Agent (Reviewer)."</em></blockquote>
将终端吐出的大长串英文评价，完整粘贴复制到 Github PR #32 的评论区。
📸 截图这段包含 AI Disclosure 标语的 Github 评论 (证据 #8)。<br>
</details>

---

### 【Phase 4：测试保障与报告看板】

**🎯 Step 12: Playwright 浏览器模拟测试 (Issue #21)** （未开始）
> 💡 **TODO (补漏提醒 + 撤除调试代码)**: 之前在 Phase 2 (Step 5) 时已记录，目前学生还不能主动看到班级和拉取模块。做到这里时**记得务必先把后端学生选课/关系绑定的接口（并在路由开放 GET 权限给学生）补全**！否则该脚本里让学生“浏览模块列表”的行为将因为拿不到数据（或 403）而失败。
> 🧹 **清理任务**：一旦后端真实权限开通，必须删除 `App.tsx` 左上角的“🐞 调试入口”按钮，以及 `module.py` 和 `StudentModuleView.tsx` 中相关的 `x-debug-student` 绕过代码。
- **操作**: 自动化 E2E 测试脚本。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>
发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，配置 E2E (Playwright) 环境，手敲一段模拟真实学生行为"自动打开首页、点击登录、浏览模块列表"的测试脚本验证流，并能在我的本地跑通且全绿。</blockquote>
</details>

**🎯 Step 13: Instructor 报告仪表盘 (Issue #6)** （未开始）
- **操作**: 班级报告数据可视化。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>
发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，为 Instructor 建立聚合报告仪表盘，显示班级匿名统计数据（如平均分、易错知识点分布）。保持简洁实用，不需要花哨的图表库。</blockquote>
</details>

---

### 【Phase 5：CI/CD 安全防线与部署】

**🎯 Step 14: 四大安全门 + OWASP (Issue #20)** （未开始）
- **操作**: 配置安全检测机制。老师要求至少 4 个安全门。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>
发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，请帮我配置以下 4 个安全门：
1. <strong>Gitleaks</strong>：在 GitHub Actions 中添加 gitleaks-action 防秘钥泄漏
2. <strong>npm audit</strong>：在 CI 中加 <code>npm audit --audit-level=high</code> 步骤
3. <strong>Bandit (SAST)</strong>：已有 bandit.yml，确认它正常工作
4. <strong>Security acceptance criteria</strong>：在每个 Issue 的 acceptance criteria 里加安全条款（如"不得硬编码 secret"）
<br>
另外，确认 CLAUDE.md 中已有 OWASP Top 10 段落（Step 0-2 已加）。
</blockquote>
</details>

**🎯 Step 14.5: 配置 AI PR Review（为后续 C.L.E.A.R. PR 做准备）** （未开始）
- **操作**: 在 GitHub Actions 中添加 AI PR review，确保 Issue #20 的 PR 能触发自动 review。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>
发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，请帮我在 GitHub Actions 中配置 AI PR review。可以选择以下方案之一（选最容易配通的）：
- 方案 A：添加 <code>claude-code-action</code> GitHub Action
- 方案 B：使用 GitHub Copilot 自动 review（如果我有权限）
- 方案 C：在 CI workflow 中加一个 step 用 <code>claude -p</code> 对 diff 做 review

目的是让后续的 PR 能被 AI 自动 review，留下截图证据。
</blockquote>
</details>

**🎯 Step 15: GitHub Actions 完整流水线 (Issue #20) ⭐** （未开始）
- **操作**: 创建覆盖老师要求的全部 8 个 stage 的 CI/CD workflow。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>
发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，帮我配置最终的 <code>.github/workflows/production.yml</code>。必须包含以下 8 个 stage（每个是一个独立 job 或 step）：

1. **Lint** — ESLint + Prettier 检查前端代码
2. **Type check** — <code>tsc --noEmit</code> 检查 TypeScript
3. **Unit + Integration tests** — Pytest (后端) + Vitest (前端)
4. **E2E tests** — Playwright
5. **Security scan** — <code>npm audit</code>
6. **AI PR review** — Step 14.5 中配好的 AI review action
7. **Preview deploy** — Vercel preview 部署（PR 触发）
8. **Production deploy** — Vercel production 部署（merge to main 触发）

确保所有 stage 都能 pass（至少不 block PR merge）。
</blockquote>
Push 代码后，去 GitHub Actions 页面抓取 All Green 截图。<br>
📸 截图 (证据 #9)。<br>
</details>

**🎯 Step 15.5: 提交 C.L.E.A.R. PR #2 (Issue #20) ⭐** （未开始）
- **操作**: Issue #20 (CI/CD + Security) 的 PR 是我们选定的 **C.L.E.A.R. PR #2**。这里我们同样使用 Reviewer Agent 来完成第二个 PR 点评，稳拿 Writer/Reviewer 满分！

<details>
<summary>👉 点击展开行动指令 (必须使用终端执行)</summary><br>
在提交 Issue #20 的 PR 之后，前往终端输入 <code>claude</code> 并发送：
<blockquote><em>Act as the expert agent from <code>.claude/agents/code-reviewer.md</code>. Review my open PR for Issue #20 (CI/CD Pipeline). Output your response strictly using the C.L.E.A.R framework. Conclude with: "AI Disclosure: Workflow generated by Antigravity (Writer). Review generated by Code-Reviewer Agent (Reviewer)."</em></blockquote>
照旧，将生成的英文点评全文粘贴至 GitHub PR 评论区。
📸 截图这段 Github 评论，确保截出 AI Disclosure 声明 (证据 #10)。<br>
</details>

**🎯 Step 16: 部署 (Issue #8)** （未开始）
- **操作**: Render 部署 PostgreSQL 数据库，Vercel 部署前端应用。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>
发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，帮我做两件部署事项：
1. **Render**: 配置 PostgreSQL 数据库实例，获取连接字符串填入 <code>.env</code>
2. **Vercel**: 将 Vite 前端打包部署到 Vercel，获取公网 URL (<code>xxx.vercel.app</code>)

指导我完成部署流程或者生成相应的配置脚本。
</blockquote>
</details>

---

### 【Phase 6：交付打包材料】

**🎯 Step 17: Readme 与架构图** （未开始）
- **操作**: 补全所有的门面文档。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>
发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，重写终稿 README。在里面添加：
1. 一套 Mermaid 数据流与前后端分离的架构示意图
2. 项目功能列表
3. 本地开发和部署说明
4. 最新版本的 API Docs 链接或概要</blockquote>
</details>

**🎯 Step 17.5: Sprint Retrospective (× 2)** （未开始）
- **操作**: 为 Sprint 1 和 Sprint 2 各补一份 Retrospective，写到 sprint plan 文件里。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>
发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，请在 <code>planning_files/learnmate-sprint-plan.md</code> 中，为 Sprint 1 和 Sprint 2 各添加一段 Retrospective，格式为：
- **What went well**: ...
- **What to improve**: ...
- **Action items**: ...

参考我们的实际经历来写（Sprint 1 搭建了基础架构和 Auth，Sprint 2 做了 AI 功能和 CI/CD）。</blockquote>
</details>

**🎯 Step 18a: 发技术博客** （未开始）
- **操作**: 在 Medium 或 Dev.to 发布一篇技术博客。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>
发送给 [Claude Code 终端或 Antigravity] (英文):<br>
<blockquote><em>Please act as a tech blogger and write a 500-word Dev.to post titled 'How Claude Code Accelerated our Agile Sprint for LearnMateAI.' Highlight our C.L.E.A.R. reviews, security pipeline, TDD workflow, and MCP usage.</em></blockquote>
</details>

**🎯 Step 18b: 个人 Reflection (500字)** （未开始）
- **操作**: 写一篇 500 字的个人反思，关于 Claude Code 在项目中的使用体验。
> 注意: HW4 的 `REFLECTION by Liuyi.md` 是关于 TDD workflow 的。这次要写一篇**新的**，侧重 Project 3 整体的 Claude Code 使用经验（skills、hooks、MCP、agents 等）。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>
发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，帮我写一篇 500 字左右的英文个人 reflection，主题是 "Claude Code 在 Project 3 中的实践体验"。内容应涵盖：
1. Custom Skills (v1→v2) 的迭代过程
2. Hooks 如何保障代码质量
3. MCP 如何打通 GitHub 工作流
4. C.L.E.A.R. review 的实践心得
5. 最大的收获和教训
请参考 <code>docs/HW5_Retrospective.md</code> 的写作风格。</blockquote>
</details>

**🎯 Step 19: 录制 视频 Demo (5-10 分钟)** （未开始）
- **操作**: 录制一段 5-10 分钟的 screencast，展示 App 功能 + Claude Code 工作流。

<details>
<summary>👉 点击查看指引</summary><br>
视频应包含：<br>
<ol>
<li>App 功能演示：登录 → 浏览模块 → 学生答题 → Instructor 看报告</li>
<li>Claude Code 工作流展示：TDD 红绿、Hook 拦截、MCP 查 Issue、Agent 调用</li>
<li>CI/CD Pipeline All Green 画面</li>
<li>部署后的公网 URL 访问</li>
</ol>
用 QuickTime 或 OBS 录制。<br>
</details>

**🎯 Step 20: Google Form 提交 + Peer Evaluation** （未开始）
- **操作**: 最终提交。

<details>
<summary>👉 点击查看指引</summary><br>
<ol>
<li><strong>Google Form Showcase</strong>: 填入 project name, GitHub URL, Vercel URL, thumbnail, video link, blog link</li>
<li><strong>Peer Evaluation</strong>: 在课程系统中完成 peer evaluation 表格</li>
</ol>
</details>

---

## 📋 C.L.E.A.R. 框架速查（老师版本）

| 维度 | 全称 | 检查内容 |
|------|------|---------|
| **C** | Context | Does this code fit the project's architecture and conventions? |
| **L** | Logic | Is the business logic correct? Are edge cases handled? |
| **E** | Evidence | Are there tests? Do they actually verify the behavior? |
| **A** | Architecture | Does it follow established patterns? Any new dependencies? |
| **R** | Risk | Security issues? Performance concerns? Data exposure? |

**选定的 2 个 C.L.E.A.R. PR：**
~~1. Issue #23 (Quiz Backend API) → Step 11~~
1. PR #32 (Teammate's Agent Backend) → Step 11 这是我 Review 别人的！
2. Issue #20 (CI/CD + Security) → Step 15.5

---

## 📸 证据清单汇总

| 编号 | 内容 | 产出 Step |
|------|------|----------|
| #1 | Slack 站会消息截图 | Step 1 |
| #2 | Stop Hook 拦截成功终端截图 | Step 2b |
| #3 | Agent 以专家口吻 review 文档截图 | Step 3 |
| #4 | MCP Tool Use 查 PR 的终端截图 | Step 4 |
| #5 | `git worktree list` 输出截图 | Step 7 |
| #6 | Pytest 红灯失败截图 | Step 8 |
| #7 | Pytest 全绿通过截图 | Step 8 |
| #7b | 两个终端同时（或交替）跑在不同分支写UI (`17_evidence_7b_parallel_terminals.png`) | Step 9 & 10 |
| #8 | C.L.E.A.R. PR #1 的 GitHub comment 截图 | Step 11 |
| #9 | GitHub Actions All Green 截图 | Step 15 |
| #10 | C.L.E.A.R. PR #2 的 GitHub comment 截图 | Step 15.5 |
