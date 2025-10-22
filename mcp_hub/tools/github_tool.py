from __future__ import annotations
from typing import Any, Dict, List
from mcp_hub.core import mcp
from ..auth.github_auth import get_github_client

@mcp.tool(name="github_list_repos", description="Lista repos propios (nombre, privacidad, url).")
def github_list_repos(limit: int = 20) -> List[Dict[str, Any]]:
    gh = get_github_client()
    user = gh.get_user()
    repos = []
    for r in user.get_repos()[:limit]:
        repos.append(
            {
                "name": r.name,
                "private": r.private,
                "url": r.html_url,
                "default_branch": r.default_branch,
            }
        )
    return repos

@mcp.tool(name="github_create_issue", description="Crea un issue en repo 'owner/name'.")
def github_create_issue(repo_full_name: str, title: str, body: str = "") -> Dict[str, Any]:
    gh = get_github_client()
    repo = gh.get_repo(repo_full_name)
    issue = repo.create_issue(title=title, body=body)
    return {"number": issue.number, "url": issue.html_url}

@mcp.tool(name="github_list_pull_requests", description="Lista pull requests abiertos de un repositorio.")
def github_list_pull_requests(repo_full_name: str, state: str = "open", limit: int = 20) -> List[Dict[str, Any]]:
    gh = get_github_client()
    repo = gh.get_repo(repo_full_name)
    pulls = []
    for pr in repo.get_pulls(state=state)[:limit]:
        pulls.append(
            {
                "number": pr.number,
                "title": pr.title,
                "state": pr.state,
                "head": pr.head.ref,
                "base": pr.base.ref,
                "url": pr.html_url,
            }
        )
    return pulls

@mcp.tool(name="github_create_pull_request", description="Crea un pull request nuevo.")
def github_create_pull_request(
    repo_full_name: str,
    title: str,
    head: str,
    base: str,
    body: str = "",
    draft: bool = False,
) -> Dict[str, Any]:
    gh = get_github_client()
    repo = gh.get_repo(repo_full_name)
    pr = repo.create_pull(title=title, body=body, head=head, base=base, draft=draft)
    return {"number": pr.number, "url": pr.html_url, "state": pr.state}

@mcp.tool(name="github_merge_pull_request", description="Fusiona un pull request.")
def github_merge_pull_request(
    repo_full_name: str,
    number: int,
    commit_title: str | None = None,
    commit_message: str | None = None,
    merge_method: str = "merge",
) -> Dict[str, Any]:
    gh = get_github_client()
    repo = gh.get_repo(repo_full_name)
    pr = repo.get_pull(number)
    result = pr.merge(commit_title=commit_title, commit_message=commit_message, merge_method=merge_method)
    return {"merged": result.merged, "message": result.message, "sha": result.sha}

@mcp.tool(name="github_create_branch", description="Crea una rama nueva a partir de otra referencia.")
def github_create_branch(repo_full_name: str, new_branch: str, from_ref: str = "main") -> Dict[str, Any]:
    gh = get_github_client()
    repo = gh.get_repo(repo_full_name)
    source_ref = repo.get_git_ref(f"heads/{from_ref}")
    ref = repo.create_git_ref(ref=f"refs/heads/{new_branch}", sha=source_ref.object.sha)
    return {"ref": ref.ref, "sha": ref.object.sha}

@mcp.tool(name="github_commit_file", description="Sube un archivo nuevo o actualiza uno existente en un repositorio.")
def github_commit_file(
    repo_full_name: str,
    path: str,
    content: str,
    message: str,
    branch: str | None = None,
) -> Dict[str, Any]:
    gh = get_github_client()
    repo = gh.get_repo(repo_full_name)
    encoded_content = content.encode("utf-8")
    try:
        existing = repo.get_contents(path, ref=branch)
        updated = repo.update_file(existing.path, message, encoded_content, existing.sha, branch=branch)
        return {"content": {"path": updated["content"].path, "sha": updated["content"].sha}, "commit": {"sha": updated["commit"].sha}}
    except Exception:
        created = repo.create_file(path, message, encoded_content, branch=branch)
        return {"content": {"path": created["content"].path, "sha": created["content"].sha}, "commit": {"sha": created["commit"].sha}}

@mcp.tool(name="github_list_releases", description="Lista releases mas recientes de un repositorio.")
def github_list_releases(repo_full_name: str, limit: int = 10) -> List[Dict[str, Any]]:
    gh = get_github_client()
    repo = gh.get_repo(repo_full_name)
    releases = []
    for rel in repo.get_releases()[:limit]:
        releases.append(
            {
                "tag": rel.tag_name,
                "name": rel.title,
                "draft": rel.draft,
                "prerelease": rel.prerelease,
                "url": rel.html_url,
            }
        )
    return releases

@mcp.tool(name="github_create_release", description="Crea un release con tag y notas.")
def github_create_release(
    repo_full_name: str,
    tag: str,
    name: str,
    body: str = "",
    draft: bool = False,
    prerelease: bool = False,
) -> Dict[str, Any]:
    gh = get_github_client()
    repo = gh.get_repo(repo_full_name)
    release = repo.create_git_release(tag=tag, name=name, message=body, draft=draft, prerelease=prerelease)
    return {"id": release.id, "url": release.html_url}
