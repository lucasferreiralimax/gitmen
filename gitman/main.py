#!/usr/bin/env python3
import os
import sys
import i18n
from rich.console import Console
from .config import i18nConfig, select_language
from .commands import projects_update, ncu_update, angular_update, get_cli_version, check_outdated, check_status, check_github
from .codeArt import gitmanArt

console = Console()

# Função para exibir o uso correto do script
def usage():
    console.print(f"[bold red]{gitmanArt}[/bold red]")
    print(i18n.t('main.usage.description'))
    for i in range(1, 10):
        new_line = 'line' + str(i)
        print(i18n.t('main.usage.'+ new_line))
    sys.exit(1)

# Função principal do programa
def app():
    try:
        i18nConfig()    

        # Verifica os parâmetros do script
        if len(sys.argv) == 1:
            usage()

        project_directory = ""
        ignored_dependencies = ""
        type_update = ""
        commit_message = "update: deps of project"
        base_directory = os.path.expanduser("~/Documents")

        # Processa os argumentos de linha de comando
        args = sys.argv[1:]
        while args:
            opt = args.pop(0)
            if opt == '-b':
                base_directory = os.path.expanduser(args.pop(0))
            elif opt == '-u':
                project_directory = args.pop(0)
            elif opt == '-i':
                ignored_dependencies = args.pop(0)
            elif opt == '-a':
                check_outdated(base_directory)
            elif opt == '-g':
                check_status(base_directory)
            elif opt == '-n':
                type_update = "ncu"
                project_directory = args.pop(0)
            elif opt == 'ng':
                type_update = "angular"
            elif opt == '-m':
                commit_message = args.pop(0)
            elif opt == 'github':
                check_github()
                sys.exit(0)
            elif opt == 'language':
                select_language()
                sys.exit(0)
            elif opt in ('-v', '--version'):
                get_cli_version()
                sys.exit(0)
            else:
                usage()

        # Executa o comando apropriado baseado nos parâmetros fornecidos
        if type_update == "ncu":
            ncu_update(project_directory, commit_message, base_directory)
        if type_update == "angular":
            angular_update(project_directory, ignored_dependencies, commit_message, base_directory)
        elif project_directory:
            projects_update(project_directory, ignored_dependencies, commit_message, base_directory)

    except KeyboardInterrupt:                            
        console.print(f"[bold red]{gitmanArt}[/bold red]")                     
        console.print(':skull: [bold red3]GitmanArt execution interrupted; exiting.[/bold red3]')
        sys.exit(0)

    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    app()
