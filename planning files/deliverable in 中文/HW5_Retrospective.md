# Homework 5: LLM Coding Aids - 终极复盘与反思 (中文草稿)

## Part 1: Custom Skill 如何改变了我们的工作流？哪些任务变得更简单了？
引入 `/add-feature` 自定义技能彻底改变了我们从零开始构建特征（Feature）的习惯，将原本不可预测的摸索过程转化为标准化流水线。起初在构建第一个功能（Student Notes API）时，我们面临许多决策性摩擦。由于缺乏先验指导，我们在执行 RED 阶段（测试驱动）时常常猜测需要多少个测试用例，并在 GREEN 阶段（代码实现）时因为随意创建 Router 和 Service 导致频繁遭遇“循环导入报错 (circular import errors)”。虽然项目最终跑通了 23 个测试，耗时 19 分钟，但过程中充满了不确定性。

基于这些具体的痛点，我们将技能迭代至 **v2** 版本，固化了严格的 TDD 7步开发流（`EXPLORE → PLAN → RED → GREEN → REFACTOR → COMMIT → DOCUMENT`）。当在第二个任务（Flashcards 智能生成功能）中运用 v2 时，效率的飞跃非常显著。新技能在 EXPLORE 阶段强制了一套 4 步检查单（要求明确架构、命名、设计模式和测试结构）；在 RED 阶段锁定了一套 6 种场景的泛用测试模板（1个成功状态，外加 401未登录/403权限错误/404模块丢失/422无内容/空内容等 5 个失败状态）；最关键的是，它自上而下严格限制了后端文件的创建序列（`Model → Schema → Agent → Service → Router`）。

最直观的改变是：我们不再把时间浪费在调试代码层级和纠结测试覆盖面上。我们在零导入错误的情况下一次性通过了全部 29 个测试，且在 20 分钟内就完成了一个复杂的 AI 生成功能。正如我们在工作日志中所总结的，这套技能让我们完美实现了“从思考如何构建代码 (HOW to build) 到彻底聚焦于构建什么业务逻辑 (WHAT to build)”的根本性心智转变。

## Part 2: MCP 接入实现了哪些以前不可能完成的功能？
模型上下文协议 (MCP) 的接入成功打破了本地终端环境与云端项目管理平台之间的信息壁垒。在接入 GitHub MCP 之前，若让大模型辅助编程，我们必须跳出终端环境，用浏览器手动查阅代码库的 Sprint 画板，或者手动输入 `gh issue list` 命令后将文本复制给 Claude；AI 的工作语境存在严重的“盲区”。

在配置 MCP 的过程中，我们深刻体会到了“AI幻觉”与网络验证协议的冲突。起初，助手默认给出了面向企业用户的 `claude mcp add --transport http...` 配置方案，结果触发了 `Incompatible auth server (does not support dynamic client registration)` 报错。在查阅了课程资料和官方的 `install-claude.md` 源码文档后，我们发现对于标准版用户，必须要显式注入鉴权信息。我们最终重写了配置：通过 `add-json` 参数绕过了客户端动态注册，并手动挂载了带有严格格式（注意区分空格）的 HTTP PAT Header (`"Authorization":"Bearer 你的Token"`)。*([Click to view MCP Connection Verification Screenshot](../../docs/screenshot/10_mcp_connected.png))*

彻底连通后，MCP 赋能的作用很大，Claude Code 直接在命令行界面内获得了读取并介入我们整个项目的权限。例如，当我们发出指令时，它能够即时调用 `Queried github` 工具，精准抓取了仓库中最新的活动要求：#9 (Instructor Module Management 面板)、#8 (Production & Polish 架构完善) 以及 #7 (System Eval & MLOps)。更强大的是，它连带阅读了 Issue 内部的 Labels 及其具体文字细节。现在，大模型无需人类做搬运工，即可主动抓取云端的真实需求并生成匹配的代码，真正做到了需求上下文与开发上下文的高度同源。*([Click to view Issues Fetching Terminal Output Screenshot](../../docs/screenshot/11_mcp_fetch_issues.png))*

## Part 3: 下一步规划：继续开发什么工作流 (Hooks/Agents)？
在未来的开发中，我们希望进一步深化大模型的复合工具链整合能力。目前我们的 MCP 应用主要局限于简单的单向查询（如查阅 Issues）。既然已经证实 Claude Code 能够完美识别项目架构，我们计划探索一套更具连贯性的版本控制与工单管理自动化管线 (Collaboration Pipeline)。

我们不打算引入高复杂度的外部测试管线，而是希望就在当下的 GitHub 体系内，构建一个稳定触发的一条龙工作流。具体设想是：当一个 Feature 标记开发完毕并通过所有测试后，我们可以命令 Claude 执行这一组合指令流：
1. 提取刚才变更的代码，自动生成符合 Conventional Commits 标准的 Git Commit 消息并提交。
2. 借用 GitHub MCP，自动根据刚才提交的内容起草一份 Pull Request (PR) 的详细描述。
3. 自动为主分支里对应的源 Issue 更新标签状态（例如从 `in-progress` 改为 `in-review`）。
4. 最后协助完成代码 Merge 并连带 Close 掉该 Issue。

在这个设想的闭环中，我们将 AI 的定位从单纯的“代码生成器”升级为了“项目流程秘书”。整个管线将严格采取基于 Human-in-the-loop 的确认机制——即每一步操作都需要等待开发者手动确认 `Y` 后再进行下一步。这不仅能在我们的 Project 3 冲刺期极大地降低代码维护的运维成本，而且将非常安全、可靠地让 AI 在固定工作流中发挥最大价值。
