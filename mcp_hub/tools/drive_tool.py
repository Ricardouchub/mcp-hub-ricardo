from __future__ import annotations
import io
from pathlib import Path
from typing import Any, Dict, List
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload
from mcp_hub.core import mcp
from ..auth.google_auth import get_google_creds

def _build_drive_service():
    creds = get_google_creds()
    return build("drive", "v3", credentials=creds)

@mcp.tool(name="drive_search", description="Busca archivos en Drive por texto y opcionalmente por mimeType.")
def drive_search(query_text: str, mime_type: str | None = None, page_size: int = 10) -> List[Dict[str, Any]]:
    """Ej: query_text='burnout', mime_type='application/vnd.google-apps.spreadsheet'"""
    service = _build_drive_service()

    def _escape_drive(s: str) -> str:
        return s.replace("'", r"\'")

    safe = _escape_drive(query_text)
    q = f"name contains '{safe}'"
    if mime_type:
        q += f" and mimeType = '{mime_type}'"
    resp = service.files().list(
        q=q,
        pageSize=page_size,
        fields="files(id, name, mimeType, modifiedTime, owners(displayName), webViewLink)",
    ).execute()
    return resp.get("files", [])

@mcp.tool(name="drive_create_file", description="Crea un archivo en Drive desde texto o desde un archivo local.")
def drive_create_file(
    name: str,
    mime_type: str | None = None,
    content: str | None = None,
    source_path: str | None = None,
    parent_id: str | None = None,
) -> Dict[str, Any]:
    if (content is None and source_path is None) or (content is not None and source_path is not None):
        raise ValueError("Debes indicar exactamente uno: content o source_path.")

    service = _build_drive_service()
    metadata: Dict[str, Any] = {"name": name}
    if mime_type:
        metadata["mimeType"] = mime_type
    if parent_id:
        metadata["parents"] = [parent_id]

    if source_path:
        path = Path(source_path).expanduser()
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"No encuentro el archivo local: {path}")
        media = MediaFileUpload(str(path), mimetype=mime_type, resumable=False)
    else:
        data = (content or "").encode("utf-8")
        media = MediaIoBaseUpload(io.BytesIO(data), mimetype=mime_type or "text/plain", resumable=False)

    created = service.files().create(body=metadata, media_body=media, fields="id, name, mimeType, webViewLink").execute()
    return created

@mcp.tool(name="drive_update_file", description="Actualiza el contenido o nombre de un archivo en Drive.")
def drive_update_file(
    file_id: str,
    new_name: str | None = None,
    content: str | None = None,
    source_path: str | None = None,
    mime_type: str | None = None,
) -> Dict[str, Any]:
    if content is not None and source_path is not None:
        raise ValueError("Usa content o source_path, no ambos.")

    service = _build_drive_service()
    metadata: Dict[str, Any] = {}
    if new_name:
        metadata["name"] = new_name

    media = None
    if source_path:
        path = Path(source_path).expanduser()
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"No encuentro el archivo local: {path}")
        media = MediaFileUpload(str(path), mimetype=mime_type, resumable=False)
    elif content is not None:
        data = (content or "").encode("utf-8")
        media = MediaIoBaseUpload(io.BytesIO(data), mimetype=mime_type or "text/plain", resumable=False)

    request = service.files().update(
        fileId=file_id,
        body=metadata or None,
        media_body=media,
        fields="id, name, mimeType, webViewLink",
    )
    updated = request.execute()
    return updated

@mcp.tool(name="drive_download_file", description="Descarga un archivo de Drive a una ruta local.")
def drive_download_file(file_id: str, destination_path: str) -> Dict[str, Any]:
    service = _build_drive_service()
    dest = Path(destination_path).expanduser()
    if dest.exists() and dest.is_dir():
        raise IsADirectoryError(f"La ruta destino es un directorio: {dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)

    request = service.files().get_media(fileId=file_id)
    with open(dest, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()

    info = service.files().get(fileId=file_id, fields="id, name, mimeType, size, webViewLink, webContentLink").execute()
    return {"saved_to": str(dest), "file": info}

@mcp.tool(name="drive_delete_file", description="Elimina o envia a la papelera un archivo en Drive.")
def drive_delete_file(file_id: str, permanent: bool = False) -> Dict[str, Any]:
    service = _build_drive_service()
    if permanent:
        service.files().delete(fileId=file_id).execute()
        return {"status": "deleted", "id": file_id}

    trashed = service.files().update(fileId=file_id, body={"trashed": True}, fields="id, trashed").execute()
    return {"status": "trashed", "id": trashed.get("id"), "trashed": trashed.get("trashed")}

@mcp.tool(name="drive_share_file", description="Comparte un archivo de Drive generando enlace o agregando usuarios.")
def drive_share_file(
    file_id: str,
    role: str = "reader",
    share_type: str = "anyone",
    allow_file_discovery: bool = False,
    email: str | None = None,
) -> Dict[str, Any]:
    service = _build_drive_service()
    body: Dict[str, Any] = {"role": role, "type": share_type, "allowFileDiscovery": allow_file_discovery}
    if share_type == "user":
        if not email:
            raise ValueError("Debes indicar email cuando share_type es 'user'.")
        body["emailAddress"] = email

    permission = service.permissions().create(fileId=file_id, body=body, fields="id").execute()
    file_info = service.files().get(fileId=file_id, fields="id, name, webViewLink, webContentLink").execute()
    return {"permissionId": permission.get("id"), "file": file_info}
