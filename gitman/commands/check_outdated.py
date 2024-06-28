import os
import sys
import subprocess
import i18n
import pyperclip
from rich.console import Console
from rich.rule import Rule

from ..codeArt import gitmanArt
from ..commands import projects_update_from_check
import inquirer
from inquirer import Checkbox, Text, Confirm

console = Console()
projects_to_update = []
all_dependencies = {}


# Função para verificar dependências desatualizadas em todos os projetos
def check_outdated(base_dir):
    for dir in os.listdir(base_dir):
        full_path = os.path.join(base_dir, dir)
        if os.path.isdir(full_path):
            package_json_path = os.path.join(full_path, "package.json")
            if os.path.exists(package_json_path):
                console.print(
                    f":file_folder: {i18n.t('check_outdated.entering_directory', fullpath=f'[bold cyan]{full_path}[/bold cyan]')}"
                )
                os.chdir(full_path)

                try:
                    default_result = subprocess.run(["npm", "outdated"])
                    if default_result.returncode == 0:
                        console.print(
                            f":white_check_mark: [bold]{i18n.t('check_outdated.no_outdated_dependencies', fullpath=f'[bold white]{dir}[/bold white]')}[/bold]"
                        )
                    else:
                        text_result = subprocess.run(
                            ["npm", "outdated"], text=True, stdout=subprocess.PIPE
                        )
                        projects_to_update.append(dir)
                        dependencies = parse_outdated_output(text_result.stdout)
                        all_dependencies[dir] = dependencies

                except subprocess.CalledProcessError as e:
                    if e.stderr:
                        console.print(
                            i18n.t("check_outdated.error", fullpath=full_path)
                        )
                        console.print(e.stderr)

                os.chdir("..")
                console.print(Rule(style="grey11"))

    # Verifica se há projetos para atualizar
    if projects_to_update:
        # Perguntar se deseja criar o update
        if confirm_update():
            selected_projects = select_projects_to_update()
            console.print(Rule(style="grey11"))

            # Coletar todas as dependências dos projetos selecionados
            all_selected_dependencies = []
            projects = {}

            for project in selected_projects:
                dependencies = all_dependencies.get(project, [])
                all_selected_dependencies.extend(dependencies)
                projects[project] = dependencies

            if not all_selected_dependencies:
                console.print(
                    ":x: No dependencies selected to ignore. Exiting application."
                )
                sys.exit(0)
                return

            # Remover duplicatas e ordenar as dependências
            all_selected_dependencies = sorted(set(all_selected_dependencies))

            # Exibir as dependências e permitir seleção para ignorar
            ignored_dependencies = select_dependencies_to_ignore(
                all_selected_dependencies
            )
            console.print(Rule(style="grey11"))

            for project, dependencies in projects.items():
                projects[project] = [
                    [dep for dep in dependencies if dep not in ignored_dependencies],
                    [dep for dep in dependencies if dep in ignored_dependencies],
                ]

            # Formatar e exibir a lista final de dependências para ignorar
            ignore_list = ",".join(ignored_dependencies)

            # Capturar a mensagem do commit
            commit_message = capture_commit_message()

            # Montar o comando gitman -u com as dependências ignoradas e a mensagem do commit
            projects_list = ",".join(selected_projects)
            command_parts = ["gitman", "-u", f'"{projects_list}"']

            if ignore_list:
                command_parts.extend(["-i", f'"{ignore_list}"'])

            if commit_message:
                command_parts.extend(["-m", f'"{commit_message}"'])

            command = " ".join(command_parts)
            console.print(Rule(style="grey11"))

            console.print(f"[bash]{command}[/bash]", style="turquoise2")
            console.print(Rule(style="grey11"))

            # Perguntar se deseja executar o comando
            if confirm_execution():
                # execute_command(command)
                console.print(
                    f":white_check_mark: {i18n.t('check_outdated.command_executed_successfully')}"
                )
                projects_update_from_check(projects, commit_message, base_dir)
            else:
                pyperclip.copy(command)

        console.print(Rule(style="grey11"))
    else:
        console.print(f":warning: {i18n.t('check_outdated.no_projects_update')}")
        console.print(Rule(style="grey11"))

    console.print(f"[bold red]{gitmanArt}[/bold red]")
    console.print(f":white_check_mark: {i18n.t('check_outdated.complete_check')}")


# Função para capturar a mensagem do commit
def capture_commit_message():
    questions_commit = [
        Text(
            "commit_message",
            message=i18n.t("check_outdated.commit_message_prompt"),
            validate=lambda _, x: True,  # Aceita qualquer entrada
        )
    ]
    commit_answers = inquirer.prompt(questions_commit)
    return commit_answers.get("commit_message", "").strip()


# Função para selecionar projetos que precisam ser atualizados
def select_projects_to_update():
    questions = [
        Checkbox(
            "projects",
            message=i18n.t("check_outdated.select_projects_message"),
            choices=projects_to_update,
        )
    ]
    answers = inquirer.prompt(questions)
    return answers.get("projects", [])


# Função para exibir as dependências e permitir a seleção para ignorar
def select_dependencies_to_ignore(dependencies):
    questions_ignore = [
        Checkbox(
            "ignore_dependencies",
            message=i18n.t("check_outdated.select_ignore_dependencies"),
            choices=dependencies,
        )
    ]
    answers_ignore = inquirer.prompt(questions_ignore)
    return answers_ignore.get("ignore_dependencies", [])


# Função para analisar a saída do comando npm outdated e extrair as dependências
def parse_outdated_output(output):
    dependencies = []
    if output:
        lines = output.splitlines()
        for line in lines[1:]:
            if line.strip():
                parts = line.split()
                dependency_name = parts[0]
                dependencies.append(dependency_name)
    return dependencies


# Função para perguntar se o usuário deseja executar o comando
def confirm_execution():
    questions = [
        Confirm(
            "execute",
            message=i18n.t("check_outdated.confirm_execute_command"),
            default=True,
        )
    ]
    answers = inquirer.prompt(questions)
    return answers.get("execute", False)


# Função para perguntar se o usuário deseja criar o update
def confirm_update():
    questions = [
        Confirm("update", message=i18n.t("check_outdated.confirm_update"), default=True)
    ]
    answers = inquirer.prompt(questions)
    return answers.get("update", False)
