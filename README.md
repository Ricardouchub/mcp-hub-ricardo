# MCP Hub Personal

**Servidor MCP personalizado** para integrar herramientas de uso cotidiano (Gmail, Google Calendar, Drive, VSCode y GitHub) directamente con entornos compatibles como **VSCode Copilot** y **Codex**.

---

##  Descripción general

Este proyecto implementa un **MCP Server multipropósito** que actúa como un hub local para interactuar con los siguientes servicios:

- 📧 **Gmail** → leer correos no leídos, obtener mensajes específicos.
- 📅 **Google Calendar** → listar próximos eventos.
- 📂 **Google Drive** → buscar archivos por nombre.
- 💻 **VSCode Local** → abrir carpetas, archivos y gestionar extensiones.
- 🐙 **GitHub** → listar repositorios y crear issues.

Todo el servidor está desarrollado con el framework **FastMCP**, sin dependencias de Docker ni servicios externos.

---

## 🧩 Arquitectura

mcp-hub-ricardo/
├── mcp_hub/
│   ├── auth/
│   │   └── google_auth.py          # Manejo de OAuth2 para APIs de Google
│   ├── tools/
│   │   ├── gmail_tool.py           # Endpoints de Gmail
│   │   ├── calendar_tool.py        # Endpoints de Calendar
│   │   ├── drive_tool.py           # Endpoints de Drive
│   │   ├── vscode_tool.py          # Acciones locales VSCode
│   │   └── github_tool.py          # Integración con GitHub API
│   ├── core/
│   │   └── mcp.py                  # Instancia central de FastMCP
│   └── server.py                   # Punto de entrada del servidor MCP
├── secrets/
│   └── credentials.google.json     # Credenciales OAuth2 (no se versionan)
├── data/
│   └── token.google.json           # Token generado tras autenticación
├── pyproject.toml
└── README.txt                      # Este archivo

---

## Requisitos

- Python **3.10+**
- Node.js **18+** (solo para Inspector MCP opcional)
- Cuenta Google Cloud con credenciales OAuth2
- Token personal de GitHub (solo lectura / issues)
- Visual Studio Code con **Copilot / Codex** instalados

---

## Instalación

git clone https://github.com/Ricardouchub/mcp-hub-ricardo.git
cd mcp-hub-ricardo
uv sync
uv pip install -e .

---

## Autenticación con Google

1. Crea credenciales OAuth2 desde Google Cloud Console.
2. Descarga el archivo `credentials.json`.
3. Guárdalo como `secrets/credentials.google.json`.
4. Ejecuta una tool por primera vez (por ejemplo `calendar_upcoming`) para iniciar el flujo de autorización.
5. Una vez completado, se guardará un token persistente en `data/token.google.json`.

---

## Ejecución local

uv run mcp dev mcp_hub/server.py

Esto abrirá el **Inspector MCP** para probar herramientas y verificar las respuestas.

O directamente por **STDIO** (modo producción):

uv run mcp run stdio mcp_hub/server.py

---

## Integración con VSCode Copilot

1. Abre **VSCode → Settings → Extensions → Copilot Labs → MCP Servers**.
2. Agrega la ruta de tu servidor.
3. Reinicia VSCode.
4. Usa prompts como:
   > “Léeme los últimos 5 correos no leídos y guárdalos en README.md.”

---

## Integración con Codex

Archivo de configuración `~/.codex/config.toml`:

model = "gpt-5-codex"
model_reasoning_effort = "medium"

[mcp_servers.mcp_hub_ricardo]
command = "C:/Users/fabri/Desktop/Portfolio/mcp-hub-ricardo/.venv/Scripts/mcp.exe"
args = ["run", "--transport", "stdio", "C:/Users/fabri/Desktop/Portfolio/mcp-hub-ricardo/mcp_hub/server.py"]
cwd = "C:/Users/fabri/Desktop/Portfolio/mcp-hub-ricardo"
startup_timeout_sec = 60

[mcp_servers.mcp_hub_ricardo.env]
GOOGLE_CREDENTIALS_PATH = "C:/Users/fabri/Desktop/Portfolio/mcp-hub-ricardo/secrets/credentials.google.json"
GOOGLE_TOKEN_PATH       = "C:/Users/fabri/Desktop/Portfolio/mcp-hub-ricardo/data/token.google.json"
GOOGLE_SCOPES           = "https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/calendar.readonly https://www.googleapis.com/auth/drive.metadata.readonly"
GITHUB_TOKEN            = "ghp_xxxxxxxxxxxxxxxxxxxxx"

---

## Ejemplo de uso (en VSCode / Codex)

> Lee los próximos 3 eventos de mi calendario y crea una nota con ellos.
> Lista mis últimos 5 correos no leídos.
> Abre la carpeta actual en VSCode.
> Crea un issue titulado “Optimizar autenticación de Google” en mi repo principal.

---

## Stack

| Componente | Uso |
|-------------|-----|
| **FastMCP** | Framework MCP Server |
| **uv** | Entorno Python ultrarrápido |
| **Google API Client** | Acceso a Gmail, Drive, Calendar |
| **PyGithub** | Conexión con API de GitHub |
| **VSCode CLI** | Acceso a entorno local de VSCode |

---

## Autor

**Ricardo Urdaneta**
_Data Analyst / Data Engineer / Data Scientist_
GitHub: https://github.com/Ricardouchub

---

## Licencia

MIT License © 2025 Ricardo Urdaneta