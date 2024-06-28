import os
import subprocess
import i18n
from rich.console import Console
from rich.rule import Rule
from ..utils import logger_expection

console = Console()


# Função para atualizar dependências de um projeto Expo
def expo_fix(projects, base_dir):
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
            # Executa o comando npx expo install --fix
            result = subprocess.run(
                ["npx", "expo", "install", "--fix"],
                check=True,
            )
            console.print(result)
            console.print(
                f":fire: [bold yellow1]{i18n.t('update.up_outdated_found')}[/]"
            )
            console.print(Rule(style="grey11"))

            # Adiciona mudanças ao Git, cria um commit e faz push
            # subprocess.run(["git", "status"], check=True)
            # console.print(Rule(style="grey11"))
        except subprocess.CalledProcessError as e:
            logger_expection(e=e, full_path=full_path)

        os.chdir("..")
