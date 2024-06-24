#!/usr/bin/env python3
import os
import sys
import i18n
from .config import i18nConfig, select_language
from .commands import projects_update
from .commands import ncu_update
from .commands import get_cli_version
from .commands import check_outdated
from .commands import check_status

gitman = """
  _______  __  .___________..___  ___.      ___      .__   __. 
 /  _____||  | |           ||   \/   |     /   \     |  \ |  | 
|  |  __  |  | `---|  |----`|  \  /  |    /  ^  \    |   \|  | 
|  | |_ | |  |     |  |     |  |\/|  |   /  /_\  \   |  . `  | 
|  |__| | |  |     |  |     |  |  |  |  /  _____  \  |  |\   | 
 \______| |__|     |__|     |__|  |__| /__/     \__\ |__| \__| 
                                                               
"""

# Função para exibir o uso correto do script
def usage():
    print(gitman)
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
        ncu_flag = False
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
                project_directory = args.pop(0)
                ncu_flag = True
            elif opt == '-m':
                commit_message = args.pop(0)
            elif opt == 'language':
                select_language()
                sys.exit(0)
            elif opt in ('-v', '--version'):
                get_cli_version()
                sys.exit(0)
            else:
                usage()

        # Executa o comando apropriado baseado nos parâmetros fornecidos
        if ncu_flag:
            ncu_update(project_directory, commit_message, base_directory)
        elif project_directory:
            projects_update(project_directory, ignored_dependencies, commit_message, base_directory)

    except KeyboardInterrupt:                            
        print(gitman)                              
        print('\nGitman execution interrupted; exiting.')
        sys.exit(0)

    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    app()
