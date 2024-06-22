#!/usr/bin/env python3
import os
import sys
import subprocess

# Caminho para a pasta Documents
DOCS_DIR = os.path.expanduser("~/Documents")

# Função para exibir o uso correto do script
def usage():
    print("Uso: {} [-u <project_directory>] [-i <ignored_dependencies>] [-a] [-g] [-n <project_directory>]".format(sys.argv[0]))
    print("  -u <project_directory>          Atualiza as dependências do diretório de projeto especificado.")
    print("                                  Se múltiplos projetos forem fornecidos, separe-os por vírgula.")
    print("  -i <ignored_dependencies>       Lista de dependências a serem ignoradas, separadas por vírgula.")
    print("  -a                              Verifica dependências desatualizadas em todos os projetos.")
    print("  -g                              Verifica o status do Git em todos os projetos.")
    print("  -n <project_directory>          Roda npx npm-check-updates -u && npm install seguido de um commit.")
    sys.exit(1)

# Função para atualizar dependências de um projeto
def update_projects(projects, ignored_deps):
    project_list = projects.split(',')
    
    for project_dir in project_list:
        if not os.path.isdir(project_dir):
            print("O diretório {} não existe.".format(project_dir))
            continue
        
        os.chdir(project_dir)
        
        print("Verificando dependências desatualizadas em", project_dir)
        
        # Gera uma lista de dependências desatualizadas com nome e versão
        outdated_packages = subprocess.run(['npm', 'outdated', '--parseable', '--depth=0'], capture_output=True, text=True).stdout
        
        # Filtra as dependências ignoradas
        if ignored_deps:
            ignored_array = ignored_deps.split(',')
            for ignored_dep in ignored_array:
                outdated_packages = '\n'.join(line for line in outdated_packages.split('\n') if not line.startswith(ignored_dep + '@'))
        
        if outdated_packages.strip():
            print("Atualizando dependências:", outdated_packages.strip())
            subprocess.run(['npm', 'install'] + outdated_packages.split(), check=True)
            
            # Adiciona mudanças ao Git, cria um commit e faz push
            subprocess.run(['git', 'add', 'package.json', 'package-lock.json'])
            subprocess.run(['git', 'commit', '-m', 'update: deps of project'])
            subprocess.run(['git', 'push'])
        else:
            print("Todas as dependências estão atualizadas em", project_dir)
        
        os.chdir('..')

# Função para rodar npx npm-check-updates e atualizar dependências
def ncu_update_projects(projects):
    project_list = projects.split(',')
    
    for project_dir in project_list:
        if not os.path.isdir(project_dir):
            print("O diretório {} não existe.".format(project_dir))
            continue
        
        os.chdir(project_dir)
        
        print("Atualizando todas as dependências em", project_dir, "com npm-check-updates")
        subprocess.run(['npx', 'npm-check-updates', '-u'], check=True)
        subprocess.run(['npm', 'install'], check=True)
        
        # Adiciona mudanças ao Git, cria um commit e faz push
        subprocess.run(['git', 'add', 'package.json', 'package-lock.json'])
        subprocess.run(['git', 'commit', '-m', 'update: all deps with npm-check-updates'])
        subprocess.run(['git', 'push'])
        
        os.chdir('..')

# Função para verificar dependências desatualizadas em todos os projetos
def check_outdated_in_all_projects():
    for dir in os.listdir(DOCS_DIR):
        full_path = os.path.join(DOCS_DIR, dir)
        if os.path.isdir(full_path):
            print("Entrando no diretório:", full_path)
            os.chdir(full_path)
            print("Rodando 'outdated' em", full_path)
            subprocess.run(['npm', 'outdated'])
            os.chdir('..')
    
    print("Verificação concluída.")

# Função para verificar o status do Git em todos os projetos
def check_git_status_in_all_projects():
    for dir in os.listdir(DOCS_DIR):
        full_path = os.path.join(DOCS_DIR, dir)
        if os.path.isdir(full_path):
            print("Entrando no diretório:", full_path)
            os.chdir(full_path)
            print("Verificando o status do Git em", full_path)
            subprocess.run(['git', 'status'])
            os.chdir('..')
    
    print("Verificação de status do Git concluída.")

# Verifica os parâmetros do script
if len(sys.argv) == 1:
    usage()

project_directory = ""
ignored_dependencies = ""
ncu_flag = False

# Processa os argumentos de linha de comando
args = sys.argv[1:]
while args:
    opt = args.pop(0)
    if opt == '-u':
        project_directory = args.pop(0)
    elif opt == '-i':
        ignored_dependencies = args.pop(0)
    elif opt == '-a':
        check_outdated_in_all_projects()
    elif opt == '-g':
        check_git_status_in_all_projects()
    elif opt == '-n':
        project_directory = args.pop(0)
        ncu_flag = True
    else:
        usage()

# Executa o comando apropriado baseado nos parâmetros fornecidos
if ncu_flag:
    ncu_update_projects(project_directory)
elif project_directory:
    update_projects(project_directory, ignored_dependencies)
