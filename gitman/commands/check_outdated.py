import os
import subprocess
import i18n
import pyperclip
from rich.console import Console
from rich.rule import Rule
from gitman.main import gitman

console = Console()

# Lista para armazenar as dependências desatualizadas
dependencies_to_update = []

# Função para verificar dependências desatualizadas em todos os projetos
def check_outdated(base_dir):
    for dir in os.listdir(base_dir):
        full_path = os.path.join(base_dir, dir)
        if os.path.isdir(full_path):
            package_json_path = os.path.join(full_path, 'package.json')
            if os.path.exists(package_json_path):
                console.print(f":file_folder: {i18n.t('check_outdated.entering_directory', fullpath=f'[bold cyan]{full_path}[/bold cyan]')}")
                os.chdir(full_path)
                
                try:
                    result = subprocess.run(['npm', 'outdated'])
                    if result.returncode == 0:
                        console.print(f":white_check_mark: [bold]{i18n.t('check_outdated.no_outdated_dependencies', fullpath=f'[bold white]{dir}[/bold white]')}[/bold]")
                    else:
                        dependencies_to_update.append(dir)
                        # console.print(f":fire: [bold bright_yellow]{i18n.t('check_outdated.need_update', fullpath=f'[bold white]{dir}[/bold white]')}[/bold bright_yellow]")
                
                except subprocess.CalledProcessError as e:
                    if e.stderr:
                        console.print(i18n.t('check_outdated.error', fullpath=full_path))
                        console.print(e.stderr)
                
                os.chdir('..')
                console.print(Rule(style="grey11"))
    
    # Imprimir o log com as dependências que precisam ser atualizadas

    if dependencies_to_update:
        dependencies_list = ", ".join(dependencies_to_update)
        console.print(f":gem: [turquoise2]gitman -u \"{dependencies_list}\"[/turquoise2]")
        console.print(Rule(style="grey11"))
        pyperclip.copy(f"gitman -u \"{dependencies_list}\"")

    console.print(f"[bold red]{gitman}[/bold red]")
    console.print(f":white_check_mark: {i18n.t('check_outdated.complete_check')}")