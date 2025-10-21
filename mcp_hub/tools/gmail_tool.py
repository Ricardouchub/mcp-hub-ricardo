from __future__ import annotations
from typing import List, Dict, Any
from googleapiclient.discovery import build
from mcp_hub.core import mcp
from ..auth.google_auth import get_google_creds

@mcp.tool(name="gmail_list_unread", description="Lista correos no leídos (INBOX).")
def gmail_list_unread(max_results: int = 10) -> List[Dict[str, Any]]:
    """Retorna remitente, asunto, fecha y el id del mensaje."""
    creds = get_google_creds()
    service = build("gmail", "v1", credentials=creds)
    resp = service.users().messages().list(userId="me", labelIds=["INBOX", "UNREAD"], maxResults=max_results).execute()
    messages = resp.get("messages", [])
    out: List[Dict[str, Any]] = []
    for m in messages:
        msg = service.users().messages().get(userId="me", id=m["id"], format="metadata", metadataHeaders=["From","Subject","Date"]).execute()
        headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
        out.append({"id": m["id"], "from": headers.get("From"), "subject": headers.get("Subject"), "date": headers.get("Date")})
    return out

@mcp.tool(name="gmail_get_message", description="Obtiene el cuerpo (texto) de un correo por id.")
def gmail_get_message(message_id: str) -> Dict[str, Any]:
    creds = get_google_creds()
    service = build("gmail", "v1", credentials=creds)
    msg = service.users().messages().get(userId="me", id=message_id, format="full").execute()
    # simplificado: extrae solo part text/plain si existe
    def _walk(parts):
        for p in parts or []:
            if p.get("mimeType") == "text/plain" and p.get("body", {}).get("data"):
                from base64 import urlsafe_b64decode
                return urlsafe_b64decode(p["body"]["data"]).decode("utf-8", errors="ignore")
            if p.get("parts"):
                t = _walk(p["parts"])
                if t: return t
        return ""
    payload = msg.get("payload", {})
    body_text = _walk(payload.get("parts")) or ""
    return {"snippet": msg.get("snippet"), "text": body_text[:10000]}