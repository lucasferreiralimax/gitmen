#!/usr/bin/env python3
import os
import sys

from commands import update_projects
from commands import ncu_update_projects
from commands import get_cli_version
from commands import check_outdated
from commands import check_status

# Função para exibir o uso correto do script
def usage():
    print("Uso: {} [-b <base_directory>] [-u <project_directory>] [-i <ignored_dependencies>] [-a] [-g] [-n <project_directory>] [-m <commit_message>]".format(sys.argv[0]))
    print("  -b <base_directory>             Diretório base onde os projetos estão localizados. (padrão: ~/Documents)")
    print("  -u <project_directory>          Atualiza as dependências do diretório de projeto especificado.")
    print("                                  Se múltiplos projetos forem fornecidos, separe-os por vírgula.")
    print("  -i <ignored_dependencies>       Lista de dependências a serem ignoradas, separadas por vírgula.")
    print("  -a                              Verifica dependências desatualizadas em todos os projetos.")
    print("  -g                              Verifica o status do Git em todos os projetos.")
    print("  -n <project_directory>          Roda npx npm-check-updates -u && npm install seguido de um commit.")
    print("  -m <commit_message>             Mensagem de commit a ser usada nas atualizações. (opcional)")
    print("  -v, --version                   Mostra a versão do programa.")
    sys.exit(1)

# Função principal do programa
def app():
    try:
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
            elif opt in ('-v', '--version'):
                print(f"Versão do programa: {get_cli_version()}")
                sys.exit(0)
            else:
                usage()

        # Executa o comando apropriado baseado nos parâmetros fornecidos
        if ncu_flag:
            ncu_update_projects(project_directory, commit_message, base_directory)
        elif project_directory:
            update_projects(project_directory, ignored_dependencies, commit_message, base_directory)

    except KeyboardInterrupt:
        print("\nExecução do script interrompida.")
        sys.exit(0)

if __name__ == "__main__":
    app()