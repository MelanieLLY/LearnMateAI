# 背景
这是 HW5 的实操攻略指南。与以往强迫 TDD 的重点不同，本次 HW5 侧重于针对你的 P3 项目（如后端 API 或各种重构任务）打造自用的 **Claude Custom Skill**，以及接入 **MCP Server**（Model Context Protocol）以增强 AI 能力，最后完成反思报告。
具体作业要求请见：`planning files/ homework5_requirment.md`

## Author
我自己和AI一起写的 自用笔记

# 步骤
## Part 1: Custom Skill (自定义技能)
### tasks 1 Explore & Define - 规划并创建初版 Skill (v1)
1.task的目的
在 `.claude/skills/` 下定义一个能够协助你 P3 开发的重用工作流技能（Slash command）。例如 `/fix-issue`, `/create-api`, 或者 `/code-review`。并要求包含明确的 name, description 以及指令。

2.给claude发的指令
在终端中进入项目并在对话中输入：
> `I am working on HW5. Please help me create a custom Claude Code skill in the '.claude/skills/' directory for my Project 3 workflow. Let's create a skill called 'code-review.md' (or any other appropriate name for our workflow). Please include proper metadata (name, description) and clear step-by-step instructions for the skill.`

3.task 的收尾工作 
为了规范代码，开一个新分支：`git checkout -b feature/hw5-skills-mcp`
提交代码：`git add .claude/skills/` -> `git commit -m "feat: create initial custom skill v1"`

4.需要得到的文字记录有哪些 
- [ ] 截图：新创建的 `v1` 技能文件的内容。
- [ ] 截图：终端使用刚才生成的 slash command（比如输入 `/code-review --help` 等等）的响应证明。

### tasks 2 Test Skill - 在两个真实任务上测试技能
1.task的目的
验证刚才创建的 v1 技能，并在**至少两个真实的任务**上执行它，以此展现技能的实际效果并发现潜在不足。

2.给claude发的指令
> `Now, let's test our new skill on a real task. [Task 1]: Please run the slash command we just created to review/process the file 'server/api/routers/XXX.py' (or any relevant file).`
> `Great, now let's do [Task 2]: Please use the skill again on 'server/tests/XXX.py'.`

3.task 的收尾工作 
仔细检查 Claude 使用技能时的表现，如果代码有修改，执行对应的 `git commit`。

4.需要得到的文字记录有哪些 
- [ ] 截图：执行 Task 1 时的对话与执行日志。
- [ ] 截图：执行 Task 2 时的对话与执行日志。

### tasks 3 Iterate Skill - 发现问题并迭代至 v2 (核心得分点)
1.task的目的
基于在 Task 2 测试中观察到的结果（例如指令太过刻板、某些特殊情况未能覆盖），修改 `.claude/skills/` 内的文件，完成 v1 到 v2 的进化。

2.给claude发的指令
> `Based on the two tests we just ran, I noticed the skill could be improved by [mentioning 1-2 specific issues, e.g., missing specific type checking or needing better summary formatting]. Please modify the skill file to iterate it to version 2 (v2), fixing these issues and making the instructions more robust.`

3.task 的收尾工作 
提交代码：`git commit -am "feat: iterate custom skill to v2 based on test results"`

4.需要得到的文字记录有哪些 
- [ ] 截图：v1 到 v2 代码的具体改变（Diff 内容）以及为什么要修改的理由（迭代依据）。
- [ ] 说明文本：简单写下 "What changed and why" 备用。

---

## Part 2: MCP Integration (MCP 接入)
### tasks 4 Setup MCP - 连接并配置 MCP 服务器 (保姆级拆解)
1. **[准备环节] 决定要连什么？**
   *强烈推荐连接 GitHub MCP，因为最容易配置且不容易因为本地环境报错。*
   - 去浏览器打开 GitHub -> Settings -> Developer Settings -> Personal Access Tokens (Classic)。
   - 点击 `Generate new token (classic)`，勾选 `repo` 这一项权限，生成。
   - 把生成的一长串 Token 暂时复制到电脑自带的备忘录里备用。

2. **[第一步] 在终端问 Claude 怎么连**
   在项目终端里输入 `claude` 回车启动。发给它：
   > `I need to complete the MCP Integration part of my homework. Let's use 'claude mcp' to connect a GitHub MCP server. Please give me the exact 'claude mcp add' command I should type in my terminal to set it up.`

3. **[第二步] 退出来，真正执行配置**
   - 看到 Claude 后，输入 `/exit` 退出 Claude 聊天状态。
   - 在裸机终端里，粘贴并执行最新官方文档要求的语句（🚨一定要把最后中文替换成你的 Token 并保留双引号）：
     `claude mcp add-json github '{"type":"http","url":"https://api.githubcopilot.com/mcp","headers":{"Authorization":"Bearer 你的TOKEN放这里"}}'`
   - 回车执行！ 

4. **[收尾与证明] (⚠️非常重要)**
   - **截图 1 (得分点)：** 屏幕上显示成功连接 (Successfully added...) 或者类似的运行日志时，**立刻截图**！这就是交作业的证据。
   - 提交你的代码更新：`git commit -am "chore: add mcp server configuration"`
   - **关于写文档：** 打开你的备忘录，用最乱的大白话流水账记下刚才你是怎么点、怎么拿到 Token、怎么退出来的。**不要自己排版！** 发给我。

5. **交给 Anti-Gravity 处理的 Prompt 👇 (当你搞定连接，就直接发给我)**
   > `[Send to Anti-Gravity]: 我刚刚配置了 MCP，这是我配置过程中的一堆流水账笔记：[贴上你混乱的记录]。请帮我整理成一篇专业的英文 Setup Documentation，符合 HW5 要求的“别人如何复现你的连接”的标准。` 

### tasks 5 Demonstrate - 演示完整 MCP 工作流 (手把手跑任务)
1. **[第一步] 重新喊出 Claude**
   在终端重新运行 `claude` 唤醒它。

2. **[第二步] 让 Claude 干活证明 MCP 在生效**
   给它发以下指令（对应 GitHub）：
   > `Now that the MCP server is configured, please demonstrate a complete task that leverages this connection. Use the GitHub MCP to list my open issues and summarize the latest 3.`

3. **[收尾与证明] (⚠️非常重要)**
   - 看着它调取工具 (你会看到类似 Using tool get_issues 的框框)。
   - **截图 2 (得分点)：** 等它完整回答完内容后，把整个问答过程以及它弹出的**工具调用日志全部截屏**！

---

## Part 3: Retrospective (15%)
### tasks 6 反思文档撰写与收尾 (让 Anti-Gravity 代笔)
1.任务目的
撰写 1-2 页（约 400-600 词左右）的 Retrospective 报告。我们不用自己从零写，让 Anti-Gravity 直接根据你的真实感受扩写。

2. **交给 Anti-Gravity 处理的 Prompt 👇 (快结束时发给我)**
   > `[Send to Anti-Gravity]: 我已经做完了 Part 1 的 Custom Skill 和 Part 2 的 MCP Integration。现在需要写反思，我真实的中文感受如下：`
   > `1. skill 改变了我的...每次它都能...我觉得变简单了。`
   > `2. MCP 让我直接在终端里就能...以前我还得去网页上，现在...`
   > `3. 下一步我想做一个...的工具，因为...`
   > `请帮我把上面的碎碎念扩写成一篇 400-600 词左右、排版精美专业的全英文 Retrospective 报告，命名为 'docs/HW5_Retrospective.md'，以满足 HW5 提交要求。`

3. **[最后一步] 检查并发车提交：**
   - 把我给你的最终英文文档保存进 `docs/HW5_Retrospective.md` 文件里。
   - 在终端里提交本次作业生成的所有代码：
     `git add .`
     `git commit -m "docs: add HW5 retrospective document"`
     `gh pr create --title "feat: HW5 Custom Skill and MCP" --body "Included custom skill v1 & v2 iteration, MCP integration, and Retrospective."`
   - **截图 3 (得分点)：** 跑去 GitHub 网页端找 Pull Request，给刚才建的这把 PR **截个图**。

4. **[胜利清点] 你交差最后要打包/上传的所有东西：**
   - [ ] Part 1: V1 技能文件和跑命令的成功**截图**
   - [ ] Part 1: v1 跑到 v2 的具体改变 (Diff) 以及文字理由的**截图或文档**
   - [ ] Part 1: V2 找两个文件使用的过程**截图**
   - [ ] Part 2: `claude mcp add` 终端顺利执行配置成功的**截图**
   - [ ] Part 2: 利用 MCP 做成一件事并包含工具调用记录的**交互截图**
   - [ ] Part 2: Setup Documentation 文档 (`MCP_Setup.md`，发给我帮你写的)
   - [ ] Part 3: 反思文档 (`docs/HW5_Retrospective.md`，发给我帮你写的)
   - [ ] Part 3: 最终 GitHub 上的 PR **截图**
