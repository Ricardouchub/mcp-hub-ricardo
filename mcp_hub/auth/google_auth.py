from __future__ import annotations
import os, json, pathlib
from typing import Sequence
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

CREDS_PATH = pathlib.Path(os.getenv("GOOGLE_CREDENTIALS_PATH", "secrets/credentials.google.json"))
TOKEN_PATH = pathlib.Path(os.getenv("GOOGLE_TOKEN_PATH", "data/token.google.json"))
SCOPES: Sequence[str] = os.getenv("GOOGLE_SCOPES", "").split()

def get_google_creds() -> Credentials:
    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    creds: Credentials | None = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Intentará refrescar automáticamente cuando uses el cliente
            pass
        else:
            if not CREDS_PATH.exists():
                raise FileNotFoundError(
                    f"No encuentro tu credentials.json en {CREDS_PATH}. Descárgalo de Google Cloud Console (OAuth Client)."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)  # abre navegador para login
        TOKEN_PATH.write_text(creds.to_json())
    return creds