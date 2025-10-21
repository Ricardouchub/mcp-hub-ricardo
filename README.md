# MCP Hub Personal

**MCP Server personal** para integrar herramientas de uso cotidiano (Gmail, Google Calendar, Drive, VSCode y GitHub) con clientes compatibles como **VSCode Copilot**, **Codex** y **Claude for Desktop**.

---

## Descripcion general

Este proyecto implementa un **MCP Server multiproposito** que actua como hub local para interactuar con los siguientes servicios:

- Gmail: leer correos no leidos y obtener mensajes especificos.
- Google Calendar: listar proximos eventos.
- Google Drive: buscar archivos por nombre.
- VSCode Local: abrir carpetas, archivos y gestionar extensiones.
- GitHub: listar repositorios y crear issues.

Todo el servidor esta construido con el framework **FastMCP**, sin depender de Docker ni de servicios externos adicionales.

---

## Arquitectura

```
mcp-hub-ricardo/
├── mcp_hub/
│   ├── auth/
│   │   └── google_auth.py          # Manejo de OAuth2 para las APIs de Google
│   ├── tools/
│   │   ├── calendar_tool.py        # Endpoints de Calendar
│   │   ├── drive_tool.py           # Endpoints de Drive
│   │   ├── gmail_tool.py           # Endpoints de Gmail
│   │   ├── github_tool.py          # Integracion con la API de GitHub
│   │   └── vscode_tool.py          # Acciones locales sobre VSCode
│   ├── core/
│   │   └── mcp.py                  # Instancia central de FastMCP
│   └── server.py                   # Punto de entrada del servidor MCP
├── secrets/
│   └── credentials.google.json     # Credenciales OAuth2 (crear manualmente)
├── data/
│   └── token.google.json           # Token generado tras la autenticacion inicial
├── pyproject.toml
└── .env.example
```

---

## Requisitos

- Python **3.10+**
- Node.js **18+** (solo para el Inspector MCP opcional)
- Cuenta de Google Cloud con credenciales OAuth2
- Token personal de GitHub (lectura / issues)
- Visual Studio Code con **Copilot / Codex** instalados

---

## Instalacion

```bash
git clone https://github.com/Ricardouchub/mcp-hub-ricardo.git
cd mcp-hub-ricardo
uv sync
uv pip install -e .
```

---

## Autenticacion con Google

1. Crea credenciales OAuth2 desde Google Cloud Console.
2. Descarga el archivo `credentials.json`.
3. Guardalo como `secrets/credentials.google.json`.
4. Ejecuta una tool por primera vez (por ejemplo `calendar_upcoming`) para iniciar el flujo de autorizacion.
5. Al finalizar, se guardara un token persistente en `data/token.google.json`.

---

## Ejecucion local

```
uv run mcp dev mcp_hub/server.py
```

Esto abre el **Inspector MCP** para probar herramientas y validar respuestas.

Modo produccion (STDIO):

```
uv run mcp run stdio mcp_hub/server.py
```


---

## Ejemplo de uso (VSCode / Codex)

<img width="700" src="img/Prueba 5 leer correos.png" alt="Main"/>

## MCP Inspector

<img width="700" src="img/MPC Inspector.png" alt="Main"/>

---

## Autor

**Ricardo Urdaneta**

[LinkedIn](https://www.linkedin.com/in/ricardourdanetacastro/) | [GitHub](https://github.com/Ricardouchub)
