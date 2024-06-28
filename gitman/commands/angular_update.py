import os
import subprocess
import i18n
import re
from rich.console import Console
from rich.rule import Rule
from ..utils import deps_logs, logger_expection

console = Console()


# Função para atualizar dependências de um projeto angular
def angular_update(projects, ignored_dependencies, commit_message, base_dir):
    project_list = projects.split(",")

    for project in project_list:
        full_path = os.path.join(base_dir, project)

        if not os.path.isdir(full_path):
            console.print(
                i18n.t("update.up_directory_not_exist").format(fullpath=full_path)
            )
            continue

        os.chdir(full_path)

        console.print(
            f":sparkles: {i18n.t('update.up_checking_outdated', fullpath=f'[bold white]{project}[/bold white]')}"
        )
        console.print(Rule(style="grey11"))

        try:
            # Regex to find 'ng update' commands
            pattern = r"ng update (@angular/[^\s]+)"
            patternDep = r"@angular/([^\s]+)"
            text_result = subprocess.run(
                ["ng", "update"], check=True, text=True, stdout=subprocess.PIPE
            )
            packages = re.findall(pattern, text_result.stdout)

            if commit_message == "update: deps of project":
                package_names = [
                    re.search(patternDep, package).group(1) for package in packages
                ]
                commit_message = "update angular: " + ", ".join(package_names)

            deps_logs(deps_up=packages)
            console.print(
                f":fire: [bold yellow1]{i18n.t('update.up_outdated_found')}[/]"
            )
            console.print(Rule(style="grey11"))

            # Atualiza todos os pacotes desatualizados de uma vez
            subprocess.run(
                ["ng", "update"] + packages,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            )

            # Adiciona mudanças ao Git, cria um commit e faz push
            subprocess.run(["git", "status"], check=True)
            subprocess.run(
                ["git", "add", "package.json", "package-lock.json"], check=True
            )
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            subprocess.run(["git", "push"], check=True)
            console.print(Rule(style="grey11"))

            console.print(
                f":fire: [bright_cyan]{i18n.t('update.up_git_commit_message')}[/] [bold white]{commit_message}[/]"
            )
            console.print(Rule(style="grey11"))
            console.print(f":fire: [bright_cyan]{i18n.t('update.up_git_push')}[/]")
            console.print(Rule(style="grey11"))
        except subprocess.CalledProcessError as e:
            logger_expection(e=e, full_path=full_path)

        os.chdir("..")