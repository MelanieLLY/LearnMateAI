# Claude Code + GitHub MCP Server 配置指南 (中文草稿)

本指南记录了如何在 Claude Code CLI 环境中配置官方的 GitHub Model Context Protocol (MCP) 服务器。完成配置后，Claude 将被授予直接访问指定 GitHub 仓库数据的权限（如读取 issue、分析提交记录等）。如果将来有更新的话，导致部分操作步骤更新，请 以官方文档(https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md)为准。 

## 1. 准备工作：生成私人访问令牌 (PAT)
为了让 Claude 以编程方式访问 GitHub 数据，需要配置个人访问令牌。
1. 在浏览器中访问 **GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)**。
2. 点击 **Generate new token**。
3. 添加易于识别的备注（例如：`Claude Code MCP Setup`）。
4. 在权限 (scopes) 列表中，勾选合适的权限。
5. 点击底部的 **Generate token**，并在页面刷新前将生成的令牌字符串随时保存（格式通常为 `ghp_...` 或 `github_pat_...`）。

## 2. 清理历史配置
在正式配置前，如果曾经尝试通过标准引导流程使用了受限的 OAuth 企业接口（包含 `api.githubcopilot.com/mcp/`），需要首先清理原有配置，因为该接口通常不支持标准账号和免费组织的动态客户端注册 (dynamic client registration)。

在终端输入以下命令移除无效配置：
```bash
claude mcp remove github
```

## 3. 通过 add-json 注入配置
使用带有环境变量的 `add-json` 参数配置是能够稳定通过鉴权的标准做法。此操作通过 HTTP 请求头 (Headers) 将生成的令牌作为鉴权信息传递给服务器。

在终端中执行以下代码（请将末尾的中文内容替换为实际的 Token 字符串）：
```bash
claude mcp add-json github '{"type":"http","url":"https://api.githubcopilot.com/mcp","headers":{"Authorization":"Bearer 替换为你的真实Token"}}'
```

> **⚠️ 注意事项：**
> 在构建 `Authorization` 字段时，关键字 `Bearer` 与后续的 Token 字符串之间**必须保留一个半角空格**（如 `"Bearer github_pat_..."`）。格式错误（如带有连字符 `Bearer-` 或缺少空格）都可能会导致请求被 GitHub 服务器拒绝 (401 Unauthorized)。

如果你把 token 放在 .env 里，官方文档还给了这一版:

```bash
claude mcp add-json github '{"type":"http","url":"https://api.githubcopilot.com/mcp","headers":{"Authorization":"Bearer '"$(grep GITHUB_PAT .env | cut -d '=' -f2)"'"}}'
```

## 4. 连接验证与功能测试
配置完成后，重新启动 Claude CLI 并验证连接。

1. 在终端中启动助手：
   ```bash
   claude
   ```
2. 输入命令调用 MCP 管理控制台：
   ```
   /mcp
   ```
   *控制台应返回綠色的 `✔ connected` 和 `✔ authenticated` 状态，确认 HTTP 请求头鉴权成功。*

   **配置验证结果展示：**

   ![MCP Connection Verification](../../docs/screenshot/10_mcp_connected.png)

3. 下发实际任务指令以测试工具调用能力：
   > `Use the GitHub MCP to list the open issues in this repository and summarize the latest 3.`
   
   测试成功时，终端日志将显示其已调用 `Queried github` 等对应 MCP 工具，并成功获取仓库详情，无需依赖本地及常规命令。

   **功能测试记录展示：**

   ![Fetching Issues Command](../../docs/screenshot/11_mcp_fetch_issues.png)
