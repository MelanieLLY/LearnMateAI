# LearnMate AI

LearnMate AI 是一款针对现代教育场景打造的智能助学平台。我们通过提供多端独立的角色体验，探索和演示了如何通过高阶的 AI 编码助手（Claude Code Mastery）、Agent 工作流和全套自动化部署来加速产品级 SaaS 平台的落地方案。

## 📍 在线体验说明

> [!IMPORTANT]
> **关于网络延迟 (Cold Start) 的重要提示**  
> 为了控制成本，我们的后端部署在 Render 的免费服务层上。如果一段时间没有活跃访问，服务器会自动休眠。因此，**您的首次登录或进行请求操作时，可能会遇到大约 3 分钟的延迟加载**。这属于休眠唤醒的正常现象，请耐心等待服务器“唤醒”，启动完成后即可恢复极速响应。

* **前端环境 (Vercel)**: [https://learn-mate-ai-zeta.vercel.app](https://learn-mate-ai-zeta.vercel.app)
* **后端环境 (Render)**: [https://learnmate-api.onrender.com](https://learnmate-api.onrender.com)

### 🔑 测试演示账号

为方便教师/TA快速体验不同角色权限，建议使用系统预置的测试账号直接登录：

**👨‍🏫 教师角色 (Instructor)**
* **账号**: `robert.smith@university.edu`
* **密码**: `owEuWEmcl2Xx`

**🎓 学生角色 (Student)**
* **账号 (学生 A)**: `alex.johnson@student.edu`
* **密码**: `dUfkhVsX8vJQ`
* **账号 (学生 B)**: `emily.davis@student.edu`
* **密码**: `OKmjlTF25O2r`

---

## 🚀 核心功能与设计巧思

我们在功能设计上拒绝了简单的 CRUD，而是通过对 Issues 及核心用户故事的梳理，落地了一系列解决师生痛点的独特交互与工程巧思：

### 1. Instructor 教师模块
* **AI 伤害感知与受众自定义 (Harm-Aware Audience Customization)**
  * **设计巧思**：为了最大限度地减少 AI 生成内容（测验、闪卡等）可能带来的文化或心理偏见伤害，我们赋予了教师高度自定义课程“受众画像”的权限。系统在生成辅助资料时，其底层的 Prompt 引擎会主动结合教师预设的课堂受众敏感度，从根源上降低 AI 输出的不良倾向对学生造成的潜在负面影响，实现了业界前沿的“伤害感知（Harm-Aware）”内容把控。
* **实时学情全景看板 (Instructor Report Dashboard)** 
  * **设计巧思**：放弃了死板的扁平表格，我们在后端打通了 `QuizSubmission` 的全域数据连通。看板不仅能实时计算全班动态均分，还能无感收集学生数据，进行“班级匿名测验分析”和“易错知识点聚合”，让教师在不侵犯学生隐私的前提下，一眼看穿“全班都没搞懂的知识盲区”并及时调整授课策略。

### 2. Student 学生模块
* **3D 沉浸式知识闪卡 (Interactive Flashcards)**
  * **设计巧思**：针对密集阅读带来的疲惫感，我们在前端运用 CSS3 构建了带真实景深动画的 **3D 双面翻转闪卡 UI**。配合大模型的内容提炼接口，将晦涩的课程摘要直接幻化为一套套可以手动“把玩”的口袋卡片，顺滑的物理交互极大地增强了随时随地进行碎片化记忆的临场感。
* **渐进式测验与真人级解卷反馈 (Quiz Taking UI)**
  * **设计巧思**：摈弃了枯燥的一卷到底长表单，采用专注感极强的“单题目步进式卡片”。更重要的是，学生提交试卷的瞬间不仅仅是为了拿个分数，系统会调用 LLM API 即刻渲染一个动态计分的智能徽章 (Score Badge)，并结合学生的具体提交给出详细到逻辑层的纠正分析。由于是在动态过程中返回，这提供了一种宛如“私人助教面对面给你批卷子”的爽快感。

### 3. 底层架构与安全控权
* **身份隔离与动态数据路由引擎**
  * **设计巧思**：彻底抛弃了前端硬编码管理用户的传统做法，利用 JSON 数据底座作为单一数据源支撑，配合 React Context 和严格的路由守卫 (404 / Unauthorized Redirects)。任何身份一经登录便在毫秒级被隔离至他专属的数据维度视图下，杜绝跨角色的非法数据探嗅。

---

## 🏗 系统架构图 (System Architecture)

基于对高并发、解耦合开发与安全性多维度的考量，本平台采用客户端-服务器 (Client-Server) 分离架构：

```mermaid
graph TD
    %% 客户端与界面层
    subgraph Client [前端应用层: Vite / React]
        UI[UI Components<br/>Tailwind CSS] --> Router[React Router]
        Router --> APIStore[API Queries & State]
    end

    %% 后端与 API 层
    subgraph Server [后端核心服务: FastAPI / Python]
        Security[JWT Auth & Validator] --> API[FastAPI Endpoints]
        API --> Handlers[Business Logic & Handlers]
        Handlers --> Prompt[Local Prompt Engine]
    end

    %% 数据库与大语言模型集成
    subgraph Infrastructure [云基础设施层]
        DB[(PostgreSQL Cloud)]
        LLM[OpenAI / Anthropic APIs]
    end

    %% 连接关系与数据流向
    Client -- "Axios HTTP (API Request)" --> Security
    Handlers -- "SQLAlchemy ORM (pool_pre_ping)" --> DB
    Prompt -- "LLM Reasoning / Tool calls" --> LLM
```

---

## 🛠 技术栈 (Tech Stack)

* **Frontend**: React.js 18, Vite, React Router DOM, Tailwind CSS (全套 A11y 骨架屏降级支持)
* **Backend**: Python 3.10+, FastAPI (ASGI), Pydantic, SQLAlchemy ORM
* **Database**: PostgreSQL Cloud (Neon/Render DB)
* **CI/CD Pipeline**: GitHub Actions
* **Quality Gates**: ESLint, Flake8, Gitleaks, NPM Audit, Bandit

---

## 🤖 Claude Code 工具链与工程规范 (Mastery & Workflow)

本项目全方位贴合 Project 3 的极客开发要求，深度贯彻了 AI 配合敏捷开发的最新流水线：

1. **基于 TDD 的 LLM 管控防线 (Red-Green-Refactor)**
   * 对于测验生成这种容易出现幻觉的高危 API，我们将生成的 prompt 验证全程覆盖为 TDD 测试链条。通过撰写高强度的 Pytest 测试用例，强制模型回应必须命中 Pydantic Schema 的要求标准，彻底把控了内容输出的有效性。
2. **系统级 `.claude` 智能伴生环境**
   * 我们精心调和了系统级的工作流 (`CLAUDE.md`) 与智能 Hook。引入严苛的代码防劣化策略，如果在带有未跑通状态的代码上执行 commit 时，Git 会直接唤起拦截警告将其阻断终止。
3. **DevSecOps 与九段式 CI 流水线**
   * 从利用 Worktree 铺开并行 UI 探索起步，我们还在 GitHub 主干上注入了全面的自动化 Action 执行步骤——囊括密文泄露检查到并行部署再到借助 Agent 进行全自动代码 C.L.E.A.R Review——呈现真正的产品级交付链路。

---

## 💻 快速本地部署 (Local Development Setup)

如果需要在本地运行或体验：

```bash
# 1. 获取代码库 (环境配置文件可参考根目录 .env.example)
git clone <repository-url>
cd LearnMateAI

# 2. 启动客户端 (端口 5200)
cd client
npm install
npm run dev

# 3. 启动服务端环境 (端口 8200)
cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8200
```

---

## 版权与开发素材档案 (License & Assets)

**Copyright © 2026 LearnMate Team. All Rights Reserved.**

本应用包含其衍生模型、UI 重塑组件受限于教育版权管理。相关核心代码目前只对审核课程(Project 3)对应的工作室教授及助教开放评价权限，杜绝外部复制、倒卖或是剥离做进一步商用。

> **影像记录区**：
> 早期 `/init` 工程创建时的基础脚手架截图纪实：
> [脚手架视图 1](https://github.com/user-attachments/assets/cd358470-668c-4226-8a37-af7739b2b528) | [脚手架视图 2](https://github.com/user-attachments/assets/502f65f4-c737-4121-a22c-42fa8c3fd00e)
