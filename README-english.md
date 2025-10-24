# Personal MCP Hub

![Status](https://img.shields.io/badge/Status-Active-22C55E?logo=statuspage&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![uv](https://img.shields.io/badge/uv-Python%20env-3E4B9E?logo=python&logoColor=white)
![FastMCP](https://img.shields.io/badge/MCP-FastMCP-0C7D9D?logo=protocol&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-PyGithub-181717?logo=github&logoColor=white)
![VSCode](https://img.shields.io/badge/VSCode-Client-007ACC?logo=visualstudiocode&logoColor=white)
![Codex](https://img.shields.io/badge/Codex-Client-6B7280?logo=apachespark&logoColor=white)
![Claude](https://img.shields.io/badge/Claude-Client-8A2BE2?logo=anthropic&logoColor=white)

**Personal MCP Server** to integrate everyday tools (Gmail, Google Calendar, Drive, VSCode, and GitHub) with clients such as **VSCode Copilot**, **Codex**, and **Claude for Desktop**.

---

## Overview

This project implements a **multi-purpose MCP Server** that acts as a local hub to interact with:

- Gmail: list messages, read content, send emails, manage labels, and attach files.
- Google Calendar: list events, create/update/delete meetings, and export them to `.ics`.
- Google Drive: search, create, update, download, delete, and share files.
- Local VSCode: open files/folders, manage extensions, search text, and run commands or git actions through the VSCode CLI.
- GitHub: list repositories, create issues, manage pull requests, branches, commits, and releases.

The entire server is built on **FastMCP**, without Docker or additional external services.

---

## Tool List

| Service | Tools | API/CLI |
|---------|-------|---------|
| Gmail | `gmail_list_unread`, `gmail_search_messages`, `gmail_get_message`, `gmail_modify_message`, `gmail_mark_as_read`, `gmail_send_message` | Gmail API v1 |
| Calendar | `calendar_upcoming`, `calendar_create_event`, `calendar_update_event`, `calendar_delete_event`, `calendar_export_event` | Calendar API v3 |
| Drive | `drive_search`, `drive_create_file`, `drive_update_file`, `drive_download_file`, `drive_delete_file`, `drive_share_file` | Drive API v3 |
| GitHub | `github_list_repos`, `github_create_issue`, `github_list_pull_requests`, `github_create_pull_request`, `github_merge_pull_request`, `github_create_branch`, `github_commit_file`, `github_list_releases`, `github_create_release` | PyGithub |
| VSCode | `vscode_open`, `vscode_open_file`, `vscode_install_ext`, `vscode_list_extensions`, `vscode_search_text`, `vscode_run_command`, `vscode_git_status` | VSCode CLI (`code`) |

---

## Architecture

```
mcp-hub-ricardo/
├── mcp_hub/
│   ├── auth/
│   │   └── google_auth.py          # OAuth2 handling for Google APIs
│   ├── tools/
│   │   ├── calendar_tool.py        # Calendar endpoints
│   │   ├── drive_tool.py           # Drive endpoints
│   │   ├── gmail_tool.py           # Gmail endpoints
│   │   ├── github_tool.py          # GitHub API integration
│   │   └── vscode_tool.py          # Local VSCode actions
│   ├── core/
│   │   └── mcp.py                  # Shared FastMCP instance
│   └── server.py                   # MCP server entrypoint
├── secrets/
│   └── credentials.google.json     # OAuth2 credentials (create manually)
├── data/
│   └── token.google.json           # Token generated after the first auth flow
├── pyproject.toml
└── .env.example
```

---

## Requirements

- Python **3.10+**
- Node.js **18+** (only for the optional MCP Inspector)
- Google Cloud account with OAuth2 credentials
- Personal GitHub token with `repo` scope
- Visual Studio Code with **Copilot / Codex** enabled

---

## Installation

```bash
git clone https://github.com/Ricardouchub/mcp-hub-ricardo.git
cd mcp-hub-ricardo
uv sync
uv pip install -e .
```

---

## Google Authentication

1. Create OAuth2 credentials in Google Cloud Console.
2. Download the `credentials.json` file.
3. Save it as `secrets/credentials.google.json`.
4. Run any Google tool for the first time (for example `calendar_upcoming`) to trigger the authorization flow.
5. Once completed, a persistent token is stored in `data/token.google.json` (if you change scopes, delete this file and repeat the flow).

---

## Local Execution

```
uv run mcp dev mcp_hub/server.py
```

This opens the **MCP Inspector** to test tools and verify responses.

Production / STDIO mode:

```
uv run mcp run stdio mcp_hub/server.py
```

---

## Client Integration

### 1) Codex

Codex reads the MCP configuration from `~/.codex/config.toml` 

#### `~/.codex/config.toml`
```toml
[mcp_servers.mcp_hub_ricardo]
# Adjust the executable depending on your OS
# Windows:
command = "PROJECT_ROOT/.venv/Scripts/mcp.exe"
# macOS/Linux:
# command = "PROJECT_ROOT/.venv/bin/mcp"

args = ["run", "--transport", "stdio", "PROJECT_ROOT/mcp_hub/server.py"]
cwd  = "PROJECT_ROOT"

[mcp_servers.mcp_hub_ricardo.env]
GOOGLE_CREDENTIALS_PATH = "PROJECT_ROOT/secrets/credentials.google.json"
GOOGLE_TOKEN_PATH       = "PROJECT_ROOT/data/token.google.json"
GOOGLE_SCOPES           = "https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.modify https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.metadata.readonly"
GITHUB_TOKEN            = "YOUR_GITHUB_TOKEN"
```

### 2) Claude Desktop

Claude Desktop uses `%APPDATA%/Claude/claude_desktop_config.json` (Windows) or `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS). After editing, **restart** Claude Desktop.

#### `claude_desktop_config.json`
```json
{
  "mcpServers": {
    "mcp-hub-ricardo": {
      "command": "PROJECT_ROOT/.venv/Scripts/mcp.exe",
      "args": [
        "run",
        "--transport",
        "stdio",
        "PROJECT_ROOT/mcp_hub/server.py"
      ],
      "cwd": "PROJECT_ROOT",
      "env": {
        "GOOGLE_CREDENTIALS_PATH": "PROJECT_ROOT/secrets/credentials.google.json",
        "GOOGLE_TOKEN_PATH": "PROJECT_ROOT/data/token.google.json",
        "GOOGLE_SCOPES": "https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.modify https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.metadata.readonly",
        "GITHUB_TOKEN": "YOUR_GITHUB_TOKEN"
      }
    }
  }
}
```

### 3) VS Code + Copilot

Open the Command Palette and run **MCP: Open User Configuration**.

#### `mcp.json`
```json
{
  "servers": {
    "mcp-hub-ricardo": {
      "type": "stdio",
      "command": "PROJECT_ROOT/.venv/Scripts/mcp.exe",
      "args": ["run", "--transport", "stdio", "PROJECT_ROOT/mcp_hub/server.py"],
      "cwd": "PROJECT_ROOT",
      "env": {
        "GOOGLE_CREDENTIALS_PATH": "PROJECT_ROOT/secrets/credentials.google.json",
        "GOOGLE_TOKEN_PATH": "PROJECT_ROOT/data/token.google.json",
        "GOOGLE_SCOPES": "https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.modify https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.metadata.readonly",
        "GITHUB_TOKEN": "YOUR_GITHUB_TOKEN"
      }
    }
  }
}
```

**Steps in VS Code**:
1. Make sure VS Code is up to date and you have access to Copilot.  
2. In **Copilot Chat**, open the **tool selection** pane and enable the tools exposed by **mcp-hub-ricardo**.  

---

## Examples 

### Copilot (VSCode)
<img width="700" src="img/Copilot_example.png" alt="Main"/>

### Claude (desktop)
<img width="400" src="img/Claude_example.png" alt="Main"/> 

### Codex (VSCode)
<img width="400" src="img/Codex_example.png" alt="Main"/>

## MCP Inspector
<img width="700" src="img/Mpc_inspector.png" alt="Main"/>


---

## Author

**Ricardo Urdaneta**

[LinkedIn](https://www.linkedin.com/in/ricardourdanetacastro/) | [GitHub](https://github.com/Ricardouchub)
