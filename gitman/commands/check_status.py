import os
import subprocess
import i18n
from rich.console import Console
from rich.rule import Rule
from ..codeArt import gitmanArt

console = Console()

# Função para verificar o status do Git em todos os projetos
def check_status(base_dir):
    for dir in os.listdir(base_dir):
        full_path = os.path.join(base_dir, dir)
        if os.path.isdir(full_path):
            git_folder = os.path.join(full_path, '.git')
            if os.path.exists(git_folder):
                os.chdir(full_path)
                try:
                    console.print(f":sparkles: {i18n.t('check_status.checking_git_status', fullpath=f'[bold white]{dir}[/bold white]')}")
                    result = subprocess.run(['git', 'status'], stdout=subprocess.PIPE, text=True)
                    if "nothing to commit, working tree clean" in result.stdout:
                        if "On branch" in result.stdout:
                            first_line = result.stdout.splitlines()[0]
                            console.print(f":gem: [bold cyan]{first_line}[/bold cyan]")
                        console.print(f":white_check_mark: [bold green]{i18n.t('check_status.clean_working_tree')}[/bold green]")
                    else:
                        subprocess.run(['git', 'status'], check=True)
                
                except subprocess.CalledProcessError as e:
                    console.print(f":exclamation: {i18n.t('check_status.git_error', fullpath=f'[bold red]{full_path}[/bold red]')}")
                    console.print(e.stderr)
                
                os.chdir('..')
                console.print(Rule(style="grey11"))

    console.print(f"[bold red]{gitmanArt}[/bold red]")
    console.print(f":white_check_mark: {i18n.t('check_status.complete_status')}")