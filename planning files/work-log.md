# Day 1
1. [后端] 步骤 1：S3 后端上传 API (纯逻辑开发) ✅ 已完成 (合并入 main, PR #15)

任务：使用 TDD（红绿测试重构）在 server/src/routers/modules.py 里新增上传到 S3 的 API (POST /modules/{module_id}/materials)。
特殊准备：在此步骤中，为 Module 数据表新增两个重要字段：Learning Objectives(学习目标) 和 Audience Context / Sensitivity(受众敏感度)（这是为了接下来第二阶段中约束 AI 的生成底线做关键的数据层支撑）。

1.5. [全栈] 步骤 1.5：用户注册与登录认证 (Auth Flow) 👉 当前任务 (Tracking in #17)

任务：实现后端的 /auth/register 和 /auth/login 接口，提供真实的 JWT Token 分发逻辑。并在此基础上重构前端，废弃之前的“免密后门”，引入真实的登录/注册界面。

2. [前端] 步骤 2：教师端模块管理 UI (极简骨架版) ✅ 已完成 (合并入 main, PR #15)

任务：创建 InstructorModuleDashboard.tsx，对接 GET 等接口实现渲染和创建模块、上传资料表单。此外还引入了 Course 上下文架构及 concurrently 全局依赖脚本，大幅提升开发体验。

3. [前端] 步骤 3：学生端模块浏览与笔记上传 UI (极简骨架版)

任务：创建 StudentModuleView.tsx，让学生端可以查看列表、下载资料，并实现上传学习笔记对接我们之前做好的 /notes API。同样不要在乎样式，先让数据能在库里跑通。

4. [前端] 步骤 4：全局 UI 润色 (Tailwind CSS)

任务：等到数据双向跑通后，一次性为教师端和学生端加上所有优美的 Tailwind CSS、毛玻璃组件、骨架屏加载以及平滑的过渡动画，提供高级的视觉体验。