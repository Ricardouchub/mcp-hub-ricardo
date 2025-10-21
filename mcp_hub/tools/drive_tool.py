from __future__ import annotations
from typing import List, Dict
from googleapiclient.discovery import build
from mcp_hub.core import mcp
from ..auth.google_auth import get_google_creds

@mcp.tool(name="drive_search", description="Busca archivos en Drive por texto y opcionalmente por mimeType.")
def drive_search(query_text: str, mime_type: str | None = None, page_size: int = 10) -> List[Dict]:
    """Ej: query_text='burnout', mime_type='application/vnd.google-apps.spreadsheet'"""
    creds = get_google_creds()
    service = build("drive", "v3", credentials=creds)
    def _escape_drive(s: str) -> str:
        return s.replace("'", r"\'")
    safe = _escape_drive(query_text)
    q = f"name contains '{safe}'"
    if mime_type:
        q += f" and mimeType = '{mime_type}'"
    resp = service.files().list(q=q, pageSize=page_size, fields="files(id, name, mimeType, modifiedTime, owners(displayName))").execute()
    files = resp.get("files", [])
    return files