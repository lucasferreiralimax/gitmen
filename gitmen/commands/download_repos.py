import os
import requests
import subprocess
import sys
from rich.console import Console

console = Console()

def get_github_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"
    repos = []
    page = 1

    while True:
        response = requests.get(url, params={"page": page, "per_page": 100})
        if response.status_code != 200:
            console.print(f"Erro ao acessar a API do GitHub: {response.status_code}")
            sys.exit(1)
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1

    return repos

def clone_repository(repo_url, dest_dir):
    try:
        subprocess.run(["git", "clone", repo_url], cwd=dest_dir, check=True)
    except subprocess.CalledProcessError as e:
        console.print(f"Erro ao clonar o repositório {repo_url}: {e}")

def download_repos(username, base_directory):
    console.print(f"Obtendo repositórios para o usuário {username}...")
    repos = get_github_repositories(username)

    if not repos:
        console.print(f"Nenhum repositório encontrado para o usuário {username}.")
        return

    console.print(f"Encontrados {len(repos)} repositórios. Iniciando o download...")

    for repo in repos:
        repo_name = repo["name"]
        repo_url = repo["clone_url"]
        dest_dir = os.path.join(base_directory, repo_name)

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        console.print(f"Clonando {repo_name} para {dest_dir}...")
        clone_repository(repo_url, base_directory)

    console.print("Download de todos os repositórios concluído.")
