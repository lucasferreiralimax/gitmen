#!/usr/bin/env python3
import os
import sys
import i18n
import platform
from commands import projects_update
from commands import ncu_update
from commands import get_cli_version
from commands import check_outdated
from commands import check_status

# Obter informações do sistema
system_info = platform.system()

if system_info == 'Windows':
    # Para Windows, usando o módulo winreg para obter o idioma
    import winreg

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Control Panel\\International", 0, winreg.KEY_READ)
    system_lang, _ = winreg.QueryValueEx(key, "LocaleName")
    winreg.CloseKey(key)
    
elif system_info == 'Darwin':
    # Para macOS, usando o comando 'defaults' para obter o idioma
    import subprocess

    proc = subprocess.Popen(['defaults', 'read', '-g', 'AppleLocale'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = proc.communicate()
    system_lang = out.strip().decode('utf-8')

else:
    # Para Linux e outros sistemas baseados em Unix, usando 'locale' para obter o idioma
    import subprocess

    proc = subprocess.Popen(['locale'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = proc.communicate()
    system_lang = out.split()[0].decode('utf-8').split('=')[1]

if system_lang:
    system_lang = system_lang[:2]

i18n.load_path.append('translations')
i18n.set('fallback', 'en')
i18n.set('locale', system_lang)

# Função para exibir o uso correto do script
def usage():
    print(i18n.t('main.usage.description', name=sys.argv[0]))
    for i in range(1, 9):
        new_line = 'line' + str(i)
        print(i18n.t('main.usage.'+ new_line))
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
        print(i18n.t('main.interrupted'))
        sys.exit(0)

if __name__ == "__main__":
    app()
