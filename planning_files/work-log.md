# Day 1
1. [后端] 步骤 1：S3 后端上传 API (纯逻辑开发) ✅ 已完成 (合并入 main, PR #15)

任务：使用 TDD（红绿测试重构）在 server/src/routers/modules.py 里新增上传到 S3 的 API (POST /modules/{module_id}/materials)。
特殊准备：在此步骤中，为 Module 数据表新增两个重要字段：Learning Objectives(学习目标) 和 Audience Context / Sensitivity(受众敏感度)（这是为了接下来第二阶段中约束 AI 的生成底线做关键的数据层支撑）。

1.5. [全栈] 步骤 1.5：用户注册与登录认证 (Auth Flow) ✅ 已完成 (合并入 main, PR #19, 关闭 Issue #17)

任务：实现后端的 /auth/register 和 /auth/login 接口，提供真实的 JWT Token 分发逻辑。重构前端废弃了“免密后门”，引入真实的登录/注册界面。后端端口也实现了彻底的随机动态分配和前后台热共享机制。

2.5. [全栈] 步骤 2.5：完善看板资料显示与模块全量 CRUD (待办/Bug Fix)

任务：当前前端教师端看板虽然能够成功调用 API 创建课程/模块和上传文件，但遇到两处功能缺失需要后续填补：
- 上传成功的关联学习资料没有在前端界面任何地方展示（阅读接口未对接）。
- 模块/课程只有创建（Create）功能，缺失“读取具体材料”、“修改记录（Update）”和“删除（Delete）”的功能闭环。需要在之后进行补充开发。

2. [前端] 步骤 2：教师端模块管理 UI (极简骨架版) ✅ 已完成 (合并入 main, PR #15)

任务：创建 InstructorModuleDashboard.tsx，对接 GET 等接口实现渲染和创建模块、上传资料表单。此外还引入了 Course 上下文架构及 concurrently 全局依赖脚本，大幅提升开发体验。

3. [前端] 步骤 3：学生端模块浏览与笔记上传 UI (极简骨架版)

任务：创建 StudentModuleView.tsx，让学生端可以查看列表、下载资料，并实现上传学习笔记对接我们之前做好的 /notes API。同样不要在乎样式，先让数据能在库里跑通。

4. [前端] 步骤 4：全局 UI 润色 (Tailwind CSS)

任务：等到数据双向跑通后，一次性为教师端和学生端加上所有优美的 Tailwind CSS、毛玻璃组件、骨架屏加载以及平滑的过渡动画，提供高级的视觉体验。

---

# Day 2 (今日规划)

**今日核心目标：收尾 Sprint 1 遗留基础模块，并进行全局视觉大升级（对接 Issue #16 与遗留 Bug）**

- **[修复] 遗留的步骤 2.5**：完善教师看板（展示已上传资料、补全修改与删除闭环）。
- **[开发] 步骤 3 / Playbook Step 5**：开发前台 `StudentModuleView.tsx`，对接数据让学生能看到课程并上传笔记。
- **[重构] 步骤 4 / Playbook Step 6**：引入企业级高阶响应式交互（Tailwind 毛玻璃、Loading 骨架屏），让全站真正达到 Portfolio-worthy（作品集级别）的惊艳视觉！