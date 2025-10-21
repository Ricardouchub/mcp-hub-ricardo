from __future__ import annotations
from typing import List, Dict
from mcp_hub.core import mcp
from ..auth.github_auth import get_github_client

@mcp.tool(name="github_list_repos", description="Lista tus repos (propios) básicos.")
def github_list_repos(limit: int = 20) -> List[Dict]:
    gh = get_github_client()
    user = gh.get_user()
    repos = []
    for r in user.get_repos()[:limit]:
        repos.append({"name": r.name, "private": r.private, "url": r.html_url, "default_branch": r.default_branch})
    return repos

@mcp.tool(name="github_create_issue", description="Crea un issue en repo 'owner/name'.")
def github_create_issue(repo_full_name: str, title: str, body: str = "") -> Dict:
    gh = get_github_client()
    repo = gh.get_repo(repo_full_name)
    issue = repo.create_issue(title=title, body=body)
    return {"number": issue.number, "url": issue.html_url}