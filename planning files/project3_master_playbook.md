# 🏆 Project 3: 满分起飞终极操作手册 (The Master Playbook)

> **修订版最终说明：** 在这个最终版本里，不仅不仅包含了老师新打分点的路线图，还融合了原业务核心逻辑（包含闪卡、看板等）。并且针对你的要求，我在每一步下方加入了**可折叠的 Prompt 发送参考清单（中文发给AG，英文发给Claude）**，让你在实操时真正做到无脑复制！

---

## 🗂️ 核心 Issue 消化路线图 (Execution Roadmap)

**【Phase 1: 收尾基础核心与抢拿 Claude 配置分 (Day 1-2)】**
1. **Issue #22**: `docs: Claude Code Mastery artifacts` —— 最简单，配完 Hooks 和 Agents 就截图拿分。
2. **Issue #9, #16**: 收尾烂尾前置任务（师生操作看版与 UI 全局毛玻璃润色）。

**【Phase 2: TDD 炫技与 Worktree 并行开发核心 AI 功能 (Day 3-6)】**
3. **Issue #23**: `feat(backend): Quiz generation & storage API` —— 由 AG 严格遵循 TDD 红绿法则完成。
4. **Issue #24**: `feat(frontend): Quiz taking UI and feedback loop` —— 物理隔离的并行开发。
5. **Issue #4**: `Agentic Content Generation` —— 闪卡、总结等生成逻辑节点。

**【Phase 3: QA 保障与 MLOps 基座 (Day 7-9)】**
6. **Issue #21**: `test: Set up Playwright for E2E tests` —— E2E 浏览器脚本测试。
7. **Issue #7 & #6**: `System Eval & MLOps` / `Instructor report` —— LLM-as-judge打分看版。

**【Phase 4: DevSecOps 满分收官与发版 (Day 10-12)】**
8. **Issue #20**: `chore: CI/CD Pipeline & 4 Security Gates` —— 防御漏洞与 GitHub Actions。
9. **Issue #8**: `Feature: Production & Polish` —— 部署 Vercel 静态，录制演示视频。

---

## 📜 详细步骤执行与 Prompt 复制清单

### 【阶段一：前期准备与拿满 "Claude Code Mastery" 证据】

**🎯 Step 1: 高频团队站会 (Async Standups)**
- **操作**: 每天在群里发消息汇报。

<details>
<summary>👉 点击查看指令详情</summary><br>

此步骤无需发送给 AI。<br>
你复制给队友的 Slack 消息：<br>
<blockquote><em>Team, today I worked on Issue 22. Claude Hooks are configured. No blockers.</em></blockquote>
截好这段对话的图 (证据 #1)。<br>

</details>

**🎯 Step 1.5: 引入 everything-claude-code 插件环境与工作流 (遵循 Scrum Flow)**
- **操作**: 严格按照项目研发规范（开 Issue -> 切分支 -> 部署工具 -> 记录日志 -> 提 PR）来部署自动化组件。

<details>
<summary>👉 点击查看行动指令 (与执行流程)</summary><br>

<ol>
<li>标准化建档 (不跳过任何规则):
  <ul>
  <li>建立专属 Issue，例如：<code>gh issue create --title "chore: Setup everything-claude-code plugins and hooks" ...</code></li>
  <li>根据 Issue 编号切出分支：<code>git checkout -b chore/XX-setup-plugins</code></li>
  </ul>
</li>

<li>安装与配置插件 (避坑手动模式):
  <ul>
  <li>开启 <code>claude</code> 终端输入命令获取作业必需的生态调用截图（只需一条即可证明）：<br>
      <code>/plugin marketplace add affaan-m/everything-claude-code</code></li>
  <li>（由于官方下载器 Bug）请直接前往 Github 下载 <code>everything-claude-code</code> 源码压缩包。</li>
  <li>提取并手动将以下精选组件复制粘贴至本项目的 <code>.claude/</code> 目录下：<br>
    <ul>
      <li><strong>Rules (规则):</strong> <code>rules/common/</code>, <code>rules/typescript/</code>, <code>rules/python/</code></li>
      <li><strong>Agents (人设分身):</strong> <code>agents/tdd-guide.md</code>, <code>agents/e2e-runner.md</code>, <code>agents/code-reviewer.md</code>, <code>agents/doc-updater.md</code>, <code>agents/database-reviewer.md</code></li>
      <li><strong>Skills (加强光盘):</strong> <code>skills/tdd-workflow/</code>, <code>skills/frontend-patterns/</code>, <code>skills/backend-patterns/</code>, <code>skills/eval-harness/</code>, <code>skills/verification-loop/</code>, <code>skills/e2e-testing/</code>, <code>skills/deployment-patterns/</code>, <code>skills/api-design/</code>, <code>skills/database-migrations/</code>, <code>skills/security-scan/</code></li>
      <li><strong>Commands (快捷指令):</strong> <code>commands/tdd.md</code>, <code>commands/e2e.md</code>, <code>commands/plan.md</code>, <code>commands/eval.md</code></li>
    </ul>
  </li>
  </ul>
</li>

<li>配置自动写入 chathistory 的 Hook:
  <ul>
  <li>在 <code>settings.json</code> 中配置一个钩子，使得每次退出 <code>claude</code> 终端时，自动将最近的沟通总结追加进 <code>planning files/chathistory_P3.md</code>。</li>
  </ul>
</li>

<li>沟通历史存档与 PR 交接:
  <ul>
  <li>结束对话时，确保大模型更新了 <code>chathistory_P3.md</code> （记录下：我们评估了 repo 并引入了 playbook 中）。</li>
  <li>通过常规流程 Commit 代码并在 GitHub 提交 PR，标记 <code>Closes #XXX</code>。</li>
  </ul>
</li>
</ol>

</details>

**🎯 Step 2: Hooks 与 CLAUDE.md 更新 (Issue #22)**
- **操作**: 验证 Hook 配置并在本地触发一次。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>

发送给 [Claude Code 终端] (英文):<br>
<blockquote><em>Please review our <code>.claude/settings.json</code>. Trigger the pre-commit Stop hook to show me it warns about tests. Update <code>CLAUDE.md</code> to use <code>@import planning_files/testing_strategy.md</code>.</em></blockquote>

截取终端里它提示 Hook 拦截成功的图 (证据 #2)。<br>

</details>

**🎯 Step 3: 调用 Doc Review Agent (Issue #22)**
- **操作**: 召唤后台建好的代理检查文档。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>

发送给 [Claude Code 终端] (英文):<br>
<blockquote><em>Act as the agent defined in <code>.claude/agents/doc-reviewer.md</code>. Read my <code>README.md</code> and check if it has formatting issues.</em></blockquote>

截图它以专家口吻回你的画面 (证据 #3)。<br>

</details>

**🎯 Step 4: MCP 连接抓取外部数据 (Issue #22)**
- **操作**: 用工具查看 GitHub 状态。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>

发送给 [Claude Code 终端] (英文):<br>
<blockquote><em>Use github MCP tool to list top 3 open Pull Requests for this repo.</em></blockquote>

截图带有 Tool Use 标志的终端交互画面 (证据 #4)。<br>

</details>

---

### 【阶段二：收尾基础模块与视觉体系 (Sprint 1 遗留项落成)】

**🎯 Step 5: 学生端模块浏览与笔记骨架 (Issue #16)**
- **操作**: 对接前后端的数据。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>

发送给 [Antigravity] (中文):<br>
<blockquote>嘿 Antigravity，开始执行 Playbook Step 5。请对接学生端前台的 <code>/notes</code> 模块，写好 <code>StudentModuleView.tsx</code> 组件，并保证无 <code>any</code> TS 类型错误，顺利完成功能即可。</blockquote>

</details>

**🎯 Step 6: 全局 UI 动态润色与过渡 (Issue #16)**
- **操作**: Tailwind 升级，搞定面试/作品集质量要求。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>

发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，执行 Step 6。请为所有组件写高阶交互：全部替换为 Tailwind CSS，引入毛玻璃效果 (backdrop-blur)，加载时的骨架屏 (Loading skeleton) 及响应状态。保证达到 "portfolio-worthy" 的视觉标准。</blockquote>

</details>

---

### 【阶段三：实际 AI 开发期 (TDD 红绿 + Worktree)】

**🎯 Step 7: 展现 Parallel Development (Git Worktrees)**
- **操作**: 拆分工程物理文件夹。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>

发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，为了完成 Worktree 要求，请通过命令行跑 <code>git worktree add</code> 帮我分出 <code>../LearnMateAI-quiz-backend</code> (Issue 23) 和前端 (Issue 24) 两个并行目录。跑完后用命令打印出列表。</blockquote>

完成后请截图截取 <code>git worktree list</code> (证据 #5)。<br>

</details>

**🎯 Step 8: Strict TDD 提交流程 - 后端 Quiz API (Issue #23)**
- **操作**: 写代码，但要卡两次截图拿考核分。
> 💡 **新工作流强化 (Pro Tip)**: 安装了插件后，这里你也可以直接在 Claude 终端输入 `/tdd test_quiz.py` 让内置专业测试代理帮你跑通以下红绿流程！

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>

<em>(分为红绿两步)</em><br>
【红灯步】发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，执行 Step 8 前半段。故意只写一个名为 <code>test_quiz.py</code> 会失败的 Pytest 用例，然后执行红字 commit。</blockquote>

(截图终端的红字，这是证据 #6)<br>

【绿灯步】发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，执行 Step 8 后半段。写出带 <code>hints</code> 字段的真 Quiz 以及测评结果保存接口，将测试通过。提交绿灯 commit。</blockquote>

(截图 pytest 全绿画面，这是证据 #7)<br>

</details>

**🎯 Step 9: 交互式 Quiz UI 开发 (Issue #24)**
- **操作**: 配合后端接口搞个漂亮的学生答题卡。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>

发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，请实现交互式 Quiz UI (<code>QuizTakingView.tsx</code>)，一次出现一道题，提交后立即显示带动画的模型反馈及打分徽章。注意动效美观。</blockquote>

</details>

**🎯 Step 10: 闪卡引擎与学习总结 Agent (Issue #4)**
- **操作**: 调用 LLM Prompt 进行真正的高级业务应用。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>

发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，处理 Issue #4 内容。由于我们此前已经写过一部分 Agent 逻辑，请完成所有的闪卡、总结路由，并在向 LLM 构建 context 时，务必将系统此前保存的 <code>受众背景敏感度(Audience Sensitivity)</code> 传递给大模型作为护栏，并在前端建立精美的卡片翻转 UI。</blockquote>

</details>

**🎯 Step 11: C.L.E.A.R. 审查并合并 PR**
- **操作**: Github 上审查代码。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>

提交 PR 时发给 [队友 / 也可以在 Github 找 Antigravity]:<br>
<blockquote>C: architecture met. L: edge cases passed. E: tests confirmed. A: pattern adhered. R: No SQL injection. AI Generated: ~85%, primarily using Antigravity and Claude CLI。</blockquote>

截图这段 Github 的评论面板 (证据 #8)。<br>

</details>

---

### 【阶段四：测试保障机制与 MLOps 看板】

**🎯 Step 12: Playwright 浏览器模拟测试 (Issue #21)**
- **操作**: 自动化填表与点击脚本。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>

发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，配置 E2E (Playwright) 环境，手敲一段模拟真实学生行为“自动打开首页、点击登录、浏览模块列表”的测试脚本验证流，并能在我的本地跑通且全绿。</blockquote>

</details>

**🎯 Step 13: 图表引入与大模型打分板 (Issue #6, #7)**
- **操作**: 数据可视化与看板建设。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>

发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，利用 Recharts 库，为 Instructor 建立聚合报告仪表盘，加入班级易错知识盲点分布图。还必须在 MLOps 专门加一张记录大模型 LLM-as-judge 的质量折线图。</blockquote>

</details>

---

### 【阶段五：CI/CD 安全防线与发版】

**🎯 Step 14: 四大安全哨兵初始化 (Issue #20)**
- **操作**: Git hooks 与漏扫机制配置。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>

发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，配置并初始化 <code>gitleaks</code> 防秘钥泄漏、配置 <code>npm audit</code> 和 <code>eslint/tsc</code>，此外在 CLAUDE.md 追加 OWASP 防止顶尖漏洞的安全标准声明充数。</blockquote>

</details>

**🎯 Step 15: GitHub Actions 八门金锁流水线 (Issue #20)**
- **操作**: 在云端触发校验任务。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>

发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，帮我配置最终的 <code>.github/workflows/production.yml</code>。每次 push 必须联动跑起 Pytest, Playwright 以及前面的所有四大安全护盾。</blockquote>

Push 代码后，网页端抓取过审的 All Green 页面图 (证据 #9)。<br>

</details>

**🎯 Step 16: Vercel 发布 (Issue #8)**
- **操作**: 给外面的看客一个能访问的网络。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>

发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，帮我把后半拉应用用部署脚本怼到 Render 上去。指引我或通过脚本将 Vite 打包连上传至 Vercel (<code>xxx.vercel.app</code>) 使得其公网可用。</blockquote>

</details>

---

### 【阶段六：交付打包材料】

**🎯 Step 17: Readme 与架构图**
- **操作**: 补全所有的门面文档。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>

发送给 [Antigravity] (中文):<br>
<blockquote>Antigravity，重写终稿 README。在里面添加详尽的一套 Mermaid 数据流与前后端分离部署的高级全栈通信架构示意图，并帮我导出最新版本的 API Docs。</blockquote>

</details>

**🎯 Step 18: 发技术博客与反思小记**
- **操作**: 输出心得。

<details>
<summary>👉 点击展开行动指令 (Prompt)</summary><br>

发送给 [Claude 终端或 Antigravity] (英文):<br>
<blockquote><em>Please act as a tech blogger and write a 500-word Dev.to post titled 'How Claude Code Accelerated our Agile Sprint for LearnMateAI.' Highlight our C.L.E.A.R. reviews, security pipeline, and MCP usage.</em></blockquote>

</details>
