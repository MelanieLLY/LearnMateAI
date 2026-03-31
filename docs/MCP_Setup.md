# Claude Code + GitHub MCP Server Setup Guide

This guide documents how to configure the official GitHub Model Context Protocol (MCP) server within the Claude Code CLI environment. After configuration, Claude will be granted permission to directly access specific GitHub repository data (such as reading issues, analyzing commit history, etc.). If there are future updates that result in operational changes, please refer to the official documentation (https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md) as the source of truth.

## 1. Preparation: Generate a Personal Access Token (PAT)
To allow Claude programmatic access to GitHub data, you need to configure a personal access token.
1. In your browser, go to **GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)**.
2. Click **Generate new token**.
3. Add an easily identifiable note (e.g., `Claude Code MCP Setup`).
4. In the scopes list, check the appropriate permissions.
5. Click **Generate token** at the bottom, and save the generated token string immediately before refreshing the page (usually starting with `ghp_...` or `github_pat_...`).

## 2. Clear Historical Configurations
Before the formal configuration, if you have previously tried using the standard setup process that points to the restricted OAuth enterprise interface (containing `api.githubcopilot.com/mcp/`), you must first clear the old configuration. This is because that interface generally does not support dynamic client registration for standard accounts and free organizations.

Run the following command in the terminal to remove the invalid configuration:
```bash
claude mcp remove github
```

## 3. Inject Configuration via add-json
Using the `add-json` parameter configuration is the standard way to reliably pass authentication. This passes the generated token as authentication info to the server via HTTP Headers.

Run the following code in the terminal (replace the placeholder at the end with your actual Token string):
```bash
claude mcp add-json github '{"type":"http","url":"https://api.githubcopilot.com/mcp","headers":{"Authorization":"Bearer REPLACE_WITH_YOUR_ACTUAL_TOKEN"}}'
```

> **⚠️ Warning:**
> When building the `Authorization` field, there **must be a half-width space** between the `Bearer` keyword and the Token string that follows (e.g., `"Bearer github_pat_..."`). Formatting errors (like adding a hyphen `Bearer-` or missing the space) may cause the request to be rejected by the GitHub server (401 Unauthorized).

If you put the token in a `.env` file, the official documentation also provides this version:

```bash
claude mcp add-json github '{"type":"http","url":"https://api.githubcopilot.com/mcp","headers":{"Authorization":"Bearer '"$(grep GITHUB_PAT .env | cut -d '=' -f2)"'"}}'
```

## 4. Connection Verification and Functional Testing
After configuration, restart the Claude CLI and verify the connection.

1. Start the assistant in the terminal:
   ```bash
   claude
   ```
2. Enter the command to open the MCP management console:
   ```
   /mcp
   ```
   *The console should return green `✔ connected` and `✔ authenticated` statuses, confirming successful HTTP header authentication.*

   **Configuration Verification Result:**

   ![MCP Connection Verification](screenshot/10_mcp_connected.png)

3. Issue a real task command to test the tool capabilities:
   > `Use the GitHub MCP to list the open issues in this repository and summarize the latest 3.`
   
   If the test is successful, the terminal log will show that it called MCP tools like `Queried github` and successfully retrieved repository details without relying on local or normal bash commands.

   **Functional Testing Result:**

   ![Fetching Issues Command](screenshot/11_mcp_fetch_issues.png)
