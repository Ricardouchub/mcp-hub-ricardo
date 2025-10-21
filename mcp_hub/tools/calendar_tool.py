from __future__ import annotations
from datetime import datetime, timezone
from typing import List, Dict, Any
from googleapiclient.discovery import build
from mcp_hub.core import mcp
from ..auth.google_auth import get_google_creds

@mcp.tool(name="calendar_upcoming", description="Lista próximos eventos del calendario principal.")
def calendar_upcoming(max_events: int = 10) -> List[Dict[str, Any]]:
    creds = get_google_creds()
    service = build("calendar", "v3", credentials=creds)
    now = datetime.now(timezone.utc).isoformat()
    events_result = service.events().list(calendarId="primary", timeMin=now, maxResults=max_events, singleEvents=True, orderBy="startTime").execute()
    items = events_result.get("items", [])
    out = []
    for e in items:
        out.append({
            "id": e.get("id"),
            "summary": e.get("summary"),
            "start": e.get("start"),
            "end": e.get("end"),
            "location": e.get("location"),
        })
    return out