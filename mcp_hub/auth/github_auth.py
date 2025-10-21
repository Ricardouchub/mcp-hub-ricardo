import os
from dotenv import load_dotenv
from github import Github

load_dotenv()

def get_github_client() -> Github:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("Falta GITHUB_TOKEN en tu .env")
    return Github(token)