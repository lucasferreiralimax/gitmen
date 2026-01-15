import os
import requests
import subprocess
import i18n
import sys
from rich.console import Console
from rich.rule import Rule
from ..codeArt import gitmenArt

console = Console()

def get_github_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"
    repos = []
    page = 1

    while True:
        response = requests.get(url, params={"page": page, "per_page": 100})
        if response.status_code != 200:
            console.print(
                f":exclamation: {i18n.t('clone_repos.github_error', error=f'[bold red]{response.status_code}[/bold red]')}"
            )
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
        console.print(
            f":exclamation: {i18n.t('clone_repos.repo_error', error=f'[bold red]{repo_url}: {e}[/bold red]')}"
        )

def clone_repos(username, base_directory, selected_repos=None):
    """
    Clona todos os repositórios do usuário ou apenas os nomes em selected_repos (lista de nomes).
    """
    console.print(
        f":empty: {i18n.t('clone_repos.cloning', user=f'[bold cyan]{username}[/bold cyan]')}"
    )
    repos = get_github_repositories(username)

    if not repos:
        console.print(
            f":empty: {i18n.t('clone_repos.empty_user', user=f'[bold red]{username}[/bold red]')}"
        )
        return

    # garante que o diretório base exista
    os.makedirs(base_directory, exist_ok=True)

    console.print(
        f":note: {i18n.t('clone_repos.repo_find', repos_size=f'[bold cyan]{len(repos)}[/bold cyan]')}"
    )

    selected_set = set(selected_repos) if selected_repos else None
    found_selected = set()

    for repo in repos:
        repo_name = repo["name"]

        # se foi passada uma lista, pule repos não solicitados
        if selected_set is not None and repo_name not in selected_set:
            continue

        repo_url = repo["clone_url"]
        dest_dir = os.path.join(base_directory, repo_name)

        console.print(
            f":white_check_mark: {i18n.t('clone_repos.repo_clone', repo_name=f'[bold cyan]{repo_name}[/bold cyan]', dest_dir=f'[bold cyan]{dest_dir}[/bold cyan]')}"
        )
        clone_repository(repo_url, base_directory)

        if selected_set is not None:
            found_selected.add(repo_name)

    # se o usuário pediu uma lista, informe se houve nomes não encontrados
    if selected_set is not None:
        not_found = selected_set - found_selected
        if not_found:
            console.print(f":exclamation: Repositórios não encontrados: [bold red]{', '.join(sorted(not_found))}[/bold red]")

    console.print(f"[bold red]{gitmenArt}[/bold red]")
    console.print(f":white_check_mark: {i18n.t('clone_repos.complete_clone')}")
