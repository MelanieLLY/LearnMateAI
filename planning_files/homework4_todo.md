> 🛑 **STATUS: SUBMITTED & DONE** 🛑
> Homework 4 has already been submitted on a separate branch. 
> All strict HW4 requirements (using Claude Code CLI, forced TDD commit history, etc.) can now be completely IGNORED. We are free to refactor and develop normally.

# 背景
是project 3的前置作业,侧重点不一样. 
homework4的各种要求请见: planning files/homework4_requirment.md
从Project3中选取的在homework4中实现的feature是Instructor Module Management API (Create/Edit/Delete)
我project3的整体架构文件:
- planning files/project3_proposal.md
- planning files/整体架构-从用户到数据的完整链路.png
- planning files/核心的 AI 处理流程-当学生请求生成学习内容时-系统内部发生了什么.png

## Author
我自己和AI一起写的 自用笔记

# 步骤
## Part 1: Claude Code Project Setup
### tasks 1 初始化 Claude Code 及环境配置
1.task的目的
满足 Part 1 核心要求。让 Claude Code 了解项目上下文，生成初始配置，演示 `/init` 命令和权限配置(`.claude/settings.json`)。

2.给claude发的指令
在终端中进入项目后输入：
> `Please run /init to set up the project. We already have a CLAUDE.md, but I need you to review it, ensure it covers Node.js + FastAPI architectures, TDD testing rules, and set up the allowed tools and directories in .claude/settings.json.`

3.task 的收尾工作 
为了符合规范，新开一个分支：`git checkout -b feature/2-instructor-module-api`
提交本次修改：`git commit -am "chore(#2): init claude code and permissions"`

4.需要得到的文字记录有哪些 
- [ ] 文本复制：复制 `/init` 命令执行后 Claude 输出的配置建议对话。(有截图更好)
- [ ] 文本复制：最终迭代定稿的 `.claude/settings.json` 日志或文件内容。


### tasks 2 演示上下文管理策略
1.task的目的
展示作业要求的 Context Management Strategy (`/clear`, `/compact`, `--continue`)。

2.给claude发的指令
直接在对话中发送：
> `/compact` 

3.task 的收尾工作 
无代码收尾。

4.需要得到的文字记录有哪些 
- [ ] 文本复制：复制 `/compact` 执行后，Claude 帮你总结精简的对话内容。(有截图更好)


## Part 2 & Part 3: Explore -> Plan -> Implement -> Commit 及 TDD 流程
💡 **老师说的“测试失败”是什么意思？如何记录？**
所谓 TDD (测试驱动开发)，第一步（RED 阶段）就是“代码还没写，先写测试用例”。这时候你去运行测试程序，终端一定会抛出**一大堆红色的错误日志 (FAILED)**。**这段包含 FAILED 的报错文本就是你的铁证**。你只需要从终端里全选复制这些红色报错，贴进你的 Log 记录里。写完业务代码后，运行转变为绿色的 PASSED 就是第二阶段 (GREEN 阶段) 的铁证，同样复制那段绿字即可。

### tasks 1 Explore & Plan (探索与规划)
1.task的目的
展示对 `Explore` 工具的使用，并规划出 TDD 测试步骤。

2.给claude发的指令
> `We are working on Issue #2: Instructor Module Management API.`
> `First, use your Explore tools (Glob, Grep, Read) to understand the current backend directory structure (specifically FastAPI routes, schemas, and tests).`
> `Then, switch to the planning phase. Provide a step-by-step TDD plan (Red-Green-Refactor) for implementing the Create Module API. Do NOT write the actual endpoint code yet.`

3.task 的收尾工作 
检查 Claude 的回复是否正确规划了目录。

4.需要得到的文字记录有哪些
- [ ] 文本复制：复制 Claude 使用 Glob/Grep 探索后端的返回结果文本。
- [ ] 文本复制：复制 Claude 给出的阶段性 TDD 步骤表。(有截图更好)


### tasks 2 Implement - 阶段一：失败的测试 (RED 阶段)
1.task的目的
只写出用来测 Create Module 的 Pytest 测试模块，然后让其在终端执行并报错。

2.给claude发的指令
> `Now we are entering the RED Phase.`
> `Do NOT write the actual endpoint code yet. I want you to FIRST write the FULL failing pytest suite for "Create Module".`
> `To ensure we cover the real business logic, please explicitly include tests for the following scenarios:`
> `1. Happy Path: Successfully create a module with valid payload -> Expect 201.`
> `2. Missing Title: Fail to create without a required field (e.g., empty or missing title) -> Expect 422.`
> `3. Duplicate Title: Fail to create if the same instructor tries to create a module with an already existing title -> Expect 409 Conflict.`
> `4. Unauthorized: Fail to create if the requester is not authenticated or not an instructor -> Expect 401/403.`
> `Write ONLY the failing tests first, executing them via terminal to strictly prove they fail.`

3.task 的收尾工作 
立刻执行 Commit：
`git add .`
`git commit -m "test(#2): RED - add failing test for create module API"`

4.需要得到的文字记录有哪些 
- [ ] 文本复制（高分点）：全选终端里爆出的包含 `FAILED` 和 `AssertionError` 之类报错的信息并复制留存。(必须截图) 
*(注：TDD 红了的这个瞬间非常关键，建议复制文本+截屏双重保险)*


### tasks 3 Implement - 阶段二：代码实现 (GREEN 阶段)
1.task的目的
让 Claude 写出 API 接口的逻辑代码，修好刚才的报错。

2.给claude发的指令
> `Now, implement the minimum code required in the backend API to make the 'Create Module' test pass (GREEN phase). After implementing, run the pytest again to verify it passes.`

3.task 的收尾工作 
立刻执行 Commit：
`git add .`
`git commit -m "feat(#2): GREEN - implement create module API to pass tests"`

4.需要得到的文字记录有哪些 
- [ ] 文本复制：复制终端中打印着 `PASSED` 或 `100%` 的成功日志。(有截图更好)


### tasks 4 Implement - 阶段三：代码重构 (REFACTOR 阶段)
1.task的目的
代码优化（加 Docstrings、提取路由），且保证还能 PASS。

2.给claude发的指令
> `Now, refactor the Create Module code. Strictly follow PEP 8, add high-quality docstrings. Run the tests again to ensure nothing broke (REFACTOR phase).`

3.task 的收尾工作 
再次成功后 Commit，并打印小结：
`git add .`
`git commit -m "refactor(#2): improve create module API structure"`
**执行 `git log --oneline -n 3` 以打印历史。**

4.需要得到的文字记录有哪些 
- [ ] 文本复制：复制你在终端运行 `git log` 后，显示的三个连续的历史记录 (`test RED` -> `feat GREEN` -> `refactor`)。(有截图更好)


### tasks 5 Edit API TDD - 阶段一：失败的测试 (RED 阶段)
1.task的目的
为 Edit Module 编写测试代码并执行，确保终端报错 (RED 阶段)。

2.给claude发的指令
> `Great. Now we move to the Edit Module API. Again, enter the RED Phase first.`
> `Write failing pytest tests for "Edit Module" to cover:`
> `1. Happy Path: Successfully edit a module title/description -> Expect 200.`
> `2. Not Found: Try to edit a non-existent module -> Expect 404.`
> `3. Unauthorized: Not the owner or not authenticated -> Expect 401/403.`
> `Write ONLY the tests first, run them in the terminal, and prove they FAIL.`

3.task 的收尾工作 
立刻执行 Commit：
`git add .`
`git commit -m "test(#2): RED - add failing tests for edit module API"`

4.需要得到的文字记录有哪些 
- [ ] 文本复制：再次复制终端爆出的包含 FAILED 报错的信息并留存。(必须截图)

### tasks 6 Edit API TDD - 阶段二：代码实现 (GREEN 阶段)
1.task的目的
实现 Edit 接口，使测试全部通过。

2.给claude发的指令
> `Now, implement the minimum code required in the backend API to make the 'Edit Module' tests pass (GREEN phase). Run pytest again to verify it passes.`

3.task 的收尾工作 
立刻执行 Commit：
`git add .`
`git commit -m "feat(#2): GREEN - implement edit module API to pass tests"`

4.需要得到的文字记录有哪些 
- [ ] 文本复制：复制终端中显示 PASSED 返回成功的日志。

### tasks 7 Edit API TDD - 阶段三：代码重构 (REFACTOR 阶段)
1.task的目的
优化 Edit 接口代码，确保依然测试通过。

2.给claude发的指令
> `Now, refactor the Edit Module code. Ensure strict PEP 8 compliance and add docstrings. Run tests again to ensure it remains GREEN (REFACTOR phase).`

3.task 的收尾工作 
立刻执行 Commit：
`git add .`
`git commit -m "refactor(#2): improve edit module API structure"`

4.需要得到的文字记录有哪些 
- [ ] 文本复制：此阶段如果有特别漂亮的重构总结，可复制留存。

### tasks 8.1 Delete API - 阶段零：Explore & Plan (探索与规划)
1.task的目的
让 Claude 先探索并输出针对 Delete API 的实现计划，满足作业里 Explore -> Plan 的打分要求。

2.给claude发的指令
> `Excellent. Now we move to the final API: Delete Module. `
> `Before we start writing tests, please use your Explore tools to check the current db schemas and routes. `
> `Then, output a brief TDD plan for implementing the Delete API. `
> `(Do not write any code yet.)`

3.task 的收尾工作 
等待输出一份包含 RED-GREEN-REFACTOR 的规划即可。

4.需要得到的文字记录有哪些 
- [ ] 文本复制：复制它的 Plan 规划。

### tasks 8.2 Delete API TDD - 阶段一：失败的测试 (RED 阶段)
1.task的目的
为 Delete Module 编写测试代码并报错 (RED 阶段)。

2.给claude发的指令
> `Great plan. Now enter the RED Phase for the Delete Module API.`
> `Write failing pytest tests for "Delete Module" covering:`
> `1. Happy Path: Successfully delete a module -> Expect 200/204.`
> `2. Not Found: Try to delete a non-existent module -> Expect 404.`
> `3. Unauthorized: Not the owner or not authenticated -> Expect 401/403.`
> `Write ONLY the tests first, run them, and prove they FAIL.`

3.task 的收尾工作 
立刻执行 Commit：
`git add .`
`git commit -m "test(#2): RED - add failing tests for delete module API"`

4.需要得到的文字记录有哪些 
- [ ] 文本复制：再次复制 Delete 阶段的 FAILED 错误文本。(必须截图)

### tasks 9 Delete API TDD - 阶段二：代码实现 (GREEN 阶段)
1.task的目的
实现 Delete 接口，使测试全部通过。

2.给claude发的指令
> `Now, implement the backend code to make the 'Delete Module' tests pass (GREEN phase). Run pytest to verify.`

3.task 的收尾工作 
立刻执行 Commit：
`git add .`
`git commit -m "feat(#2): GREEN - implement delete module API to pass tests"`

4.需要得到的文字记录有哪些 
- [ ] 文本复制：复制终端中显示 PASSED 返回成功的日志。

### tasks 10 Delete API TDD - 阶段三：代码重构 (REFACTOR 阶段)
1.task的目的
优化 Delete 接口代码并验证。

2.给claude发的指令
> `Finally, refactor the Delete Module code. Check for PEP 8 and docstrings. Run tests a final time to ensure the complete suite is GREEN (REFACTOR phase).`

3.task 的收尾工作 
立刻执行 Commit：
`git add .`
`git commit -m "refactor(#2): improve delete module API structure"`
**执行 `git log --oneline -n 10` 以打印整个 TDD 的华丽历史。**

4.需要得到的文字记录有哪些 
- [ ] 文本复制：复制展示刚才 Edit 和 Delete 全部流程的一连串 Git 历史供老师检阅。(有截图更好)


## Part 4: Reflection
### tasks 1 总结收尾与文档生成
1.task的目的
由 Claude 提炼反思报告 (Reflection) 和整理日志 (Annotated Log)。

2.给claude发的指令
> `We have finished the implementation. Use your transcript and compile today's annotated Claude Code session log into docs/HW4_SessionLog.md.`
> `Also, draft a 1-2 page reflection document in docs/HW4_Reflection.md answering:`
> `1. How does the Explore->Plan->Implement->Commit workflow compare to my previous approach?`
> `2. What context management strategies worked best during this session?`

3.task 的收尾工作 
推送代码并建 PR：
`git add .`
`git commit -m "docs(#2): add HW4 reflection and logs"`
`gh pr create --title "feat(#2): Instructor Module API" --body "Closes #2. Full TDD via Claude Code"`

4.需要得到的文字记录有哪些 
- [ ] 文本复制：复制使用 `gh pr create` 后生成的 PR 链接及日志。(有截图更好)
- 最终生成的两个 `.md` 文档。