from __future__ import annotations
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Sequence
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

def _run(args: Sequence[str], capture: bool = True) -> Dict[str, Any]:
    code = _resolve_code_exe()
    try:
        completed = subprocess.run(
            [code, *args],
            capture_output=capture,
            text=True,
            check=False,
        )
        return {
            "args": [code, *args],
            "returncode": completed.returncode,
            "stdout": completed.stdout if capture else "",
            "stderr": completed.stderr if capture else "",
        }
    except Exception as exc:
        return {"args": [code, *args], "error": str(exc)}

@mcp.tool(name="vscode_open", description="Abre VSCode en una carpeta (equivale a: code -r <path>).")
def vscode_open(path: str) -> Dict[str, Any]:
    result = _run(["-r", path], capture=False)
    return result

@mcp.tool(name="vscode_open_file", description="Abre un archivo especifico en VSCode (acepta :linea:columna).")
def vscode_open_file(file_path: str) -> Dict[str, Any]:
    return _run(["-r", "-g", file_path], capture=False)

@mcp.tool(name="vscode_install_ext", description="Instala una extension de VSCode por id (publisher.ext).")
def vscode_install_ext(extension_id: str) -> Dict[str, Any]:
    return _run(["--install-extension", extension_id])

@mcp.tool(name="vscode_list_extensions", description="Lista extensiones instaladas en VSCode.")
def vscode_list_extensions() -> Dict[str, Any]:
    result = _run(["--list-extensions"])
    if "stdout" in result and result["stdout"]:
        extensions = [line.strip() for line in result["stdout"].splitlines() if line.strip()]
        result["extensions"] = extensions
    return result

@mcp.tool(name="vscode_search_text", description="Busca texto en archivos usando ripgrep integrado de VSCode.")
def vscode_search_text(pattern: str, folder: str | None = None, files_include: str | None = None, files_exclude: str | None = None) -> Dict[str, Any]:
    args: List[str] = ["--search", pattern]
    if folder:
        args.extend(["--folder-uri", Path(folder).resolve().as_uri()])
    if files_include:
        args.extend(["--include", files_include])
    if files_exclude:
        args.extend(["--exclude", files_exclude])
    return _run(args)

@mcp.tool(name="vscode_run_command", description="Ejecuta un comando de VSCode (--command).")
def vscode_run_command(command_id: str, args_json: str | None = None) -> Dict[str, Any]:
    args: List[str] = ["--command", command_id]
    if args_json:
        try:
            _ = json.loads(args_json)
            args.extend(["--command-args", args_json])
        except json.JSONDecodeError as exc:
            raise ValueError(f"args_json debe ser JSON valido: {exc}")
    return _run(args)

@mcp.tool(name="vscode_git_status", description="Ejecuta git status desde la CLI de VSCode (code --git).")
def vscode_git_status(folder: str | None = None) -> Dict[str, Any]:
    args: List[str] = ["--git", "status"]
    if folder:
        args.append(Path(folder).resolve().as_posix())
    return _run(args)
