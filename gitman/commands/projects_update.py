import os
import subprocess
import i18n
import re
from rich.console import Console
from rich.rule import Rule
from ..utils import deps_logs, logger_expection

console = Console()


# Função para atualizar dependências de um projeto
def projects_update(projects, ignored_deps, commit_message, base_dir):
    project_list = projects.split(",")

    for project_dir in project_list:
        full_path = os.path.join(base_dir, project_dir)
        if not os.path.isdir(full_path):
            console.print(
                i18n.t("update.up_directory_not_exist").format(fullpath=full_path)
            )
            continue

        os.chdir(full_path)

        console.print(
            f":sparkles: {i18n.t('update.up_checking_outdated', fullpath=f'[bold white]{project_dir}[/bold white]')}"
        )
        console.print(Rule(style="grey11"))

        try:
            # Gera uma lista de dependências desatualizadas com nome e versão
            outdated_result = subprocess.run(
                ["npm", "outdated", "--parseable", "--depth=0"],
                capture_output=True,
                text=True,
            )

            # Exibir a saída completa para depuração
            # if outdated_result.stdout:
            #     console.print(i18n.t('update.up_outdated_output').format(output=outdated_result.stdout))
            #     console.print(Rule(style="grey11"))
            # if outdated_result.stderr:
            #     console.print(i18n.t('update.up_outdated_errors').format(errors=outdated_result.stderr))
            #     console.print(Rule(style="grey11"))

            # Se houver dependências desatualizadas, outdated_result.returncode será 1
            if outdated_result.returncode not in [0, 1]:
                raise subprocess.CalledProcessError(
                    outdated_result.returncode,
                    outdated_result.args,
                    output=outdated_result.stdout,
                    stderr=outdated_result.stderr,
                )

            outdated_packages = outdated_result.stdout.strip()
            outdated_packagesUpdate = set()
            packages_names = []

            if ignored_deps:
                ignored_array = [dep.strip() for dep in ignored_deps.split(",")]
                pattern = r"@\d+\.\d+\.\d+$"
                for package in outdated_packages.split("\n"):
                    package_name = package.split(":")[3]
                    package_name_clean = re.sub(pattern, "", package_name)
                    if not any(
                        package_name_clean.strip() == ignored_dep
                        for ignored_dep in ignored_array
                    ):
                        outdated_packagesUpdate.add(package_name)

                packages_names = list(outdated_packagesUpdate)
                deps_logs(deps_up=packages_names, deps_off=ignored_array)
            else:
                for package in outdated_packages.split("\n"):
                    package_name = package.split(":")[3]
                    packages_names.append(package_name.strip())

            if outdated_packages:
                update_and_commit(
                    packages_names=packages_names, commit_message=commit_message
                )
            else:
                console.print(
                    f":white_check_mark: [bold]{i18n.t('update.up_all_to_date', fullpath=f'[bold white]{project_dir}[/bold white]')}[/bold]"
                )
                console.print(Rule(style="grey11"))

        except subprocess.CalledProcessError as e:
            logger_expection(e=e, full_path=full_path)

        os.chdir("..")


def projects_update_from_check(projects, commit_message, base_dir):
    for project in projects:
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
            deps_logs(deps_up=projects[project][0], deps_off=projects[project][1])
            update_and_commit(
                packages_names=projects[project][0], commit_message=commit_message
            )
        except subprocess.CalledProcessError as e:
            logger_expection(e=e, full_path=full_path)

        os.chdir("..")


def update_and_commit(packages_names, commit_message):
    console.print(f":fire: [bold yellow1]{i18n.t('update.up_outdated_found')}[/]")
    console.print(Rule(style="grey11"))

    # Atualiza todos os pacotes desatualizados de uma vez
    subprocess.run(
        ["npm", "install"] + packages_names + ["--legacy-peer-deps"], check=True
    )
    console.print(Rule(style="grey11"))

    # Adiciona mudanças ao Git, cria um commit e faz push
    subprocess.run(["git", "status"], check=True)
    subprocess.run(["git", "add", "package.json", "package-lock.json"], check=True)
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "push"], check=True)
    console.print(Rule(style="grey11"))

    console.print(
        f":fire: [bright_cyan]{i18n.t('update.up_git_commit_message')}[/] [bold white]{commit_message}[/]"
    )
    console.print(Rule(style="grey11"))
    console.print(f":fire: [bright_cyan]{i18n.t('update.up_git_push')}[/]")
    console.print(Rule(style="grey11"))
