import os
import subprocess
import i18n
from rich.console import Console
from rich.rule import Rule
from ..codeArt import gitmenArt

console = Console()


# Função para instalar dependências em todos os projetos
def script(base_dir, script_run):
    for dir in os.listdir(base_dir):
        full_path = os.path.join(base_dir, dir)
        if os.path.isdir(full_path):
            package_json_path = os.path.join(full_path, "package.json")
            if os.path.exists(package_json_path):
                os.chdir(full_path)
                try:
                    console.print(
                        f":sparkles: {i18n.t('script.installing', fullpath=f'[bold white]{dir}[/bold white]')}"
                    )

                    command = script_run.split()

                    result = subprocess.run(
                        command, stdout=subprocess.PIPE, text=True
                    )

                    console.print(result.stdout)

                except subprocess.CalledProcessError as e:
                    console.print(
                        f":exclamation: {i18n.t('script.install_error', fullpath=f'[bold red]{full_path}[/bold red]')}"
                    )
                    console.print(e.stderr)

                os.chdir("..")
                console.print(Rule(style="grey11"))

    console.print(f"[bold red]{gitmenArt}[/bold red]")
    console.print(f":white_check_mark: {i18n.t('script.complete_status')}")
