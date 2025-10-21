# mcp_hub/server.py
from mcp_hub.core import mcp  # instancia compartida

# Importa las tools; al importarse, sus @mcp.tool() ya quedan registradas
from mcp_hub.tools.gmail_tool import gmail_list_unread, gmail_get_message
from mcp_hub.tools.calendar_tool import calendar_upcoming
from mcp_hub.tools.drive_tool import drive_search
from mcp_hub.tools.vscode_tool import vscode_open, vscode_open_file, vscode_install_ext
from mcp_hub.tools.github_tool import github_list_repos, github_create_issue