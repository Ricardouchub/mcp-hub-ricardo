from __future__ import annotations
import os, subprocess, shlex, shutil, sys
from mcp_hub.core import mcp

def _resolve_code_exe() -> str:
    v = os.getenv("VSCODE_CLI")
    if v and os.path.exists(v):
        return v

    exe = shutil.which("code")
    if exe:
        return exe

    if os.name == "nt":
        candidates = [
            os.path.join(os.getenv("LOCALAPPDATA", ""), r"Programs\Microsoft VS Code\bin\code.cmd"),
            os.path.join(os.getenv("ProgramFiles", ""), r"Microsoft VS Code\bin\code.cmd"),
            os.path.join(os.getenv("ProgramFiles(x86)", ""), r"Microsoft VS Code\bin\code.cmd"),
        ]
        for c in candidates:
            if c and os.path.exists(c):
                return c

    return "code"

def _run(args: list[str]) -> str:
    code = _resolve_code_exe()
    try:
        p = subprocess.run([code, *args], capture_output=True, text=True)
        return (p.stdout or "") + (p.stderr or "")
    except Exception as e:
        return f"Error ejecutando {code} {' '.join(args)}: {e}"

@mcp.tool(name="vscode_open", description="Abre VSCode en una carpeta (equivale a: code -r <path>).")
def vscode_open(path: str) -> str:
    return _run(["-r", path])

@mcp.tool(name="vscode_open_file", description="Abre un archivo específico en VSCode (acepta :linea:columna).")
def vscode_open_file(file_path: str) -> str:
    return _run(["-r", "-g", file_path])

@mcp.tool(name="vscode_install_ext", description="Instala una extensión de VSCode por id (publisher.ext).")
def vscode_install_ext(extension_id: str) -> str:
    return _run(["--install-extension", extension_id])