#!/usr/bin/env python3
import os
import sys
import subprocess
from importlib.metadata import version

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

# Função para exibir a versão do programa
def get_program_version():
    try:
        return version('gitman')
    except Exception:
        return "Versão desconhecida"

# Função para atualizar dependências de um projeto
def update_projects(projects, ignored_deps, commit_message, base_dir):
    project_list = projects.split(',')
    
    for project_dir in project_list:
        full_path = os.path.join(base_dir, project_dir)
        if not os.path.isdir(full_path):
            print(f"O diretório {full_path} não existe.")
            continue
        
        os.chdir(full_path)
        
        print(f"Verificando dependências desatualizadas em {full_path}")
        
        try:
            # Gera uma lista de dependências desatualizadas com nome e versão
            outdated_result = subprocess.run(
                ['npm', 'outdated', '--parseable', '--depth=0'], 
                capture_output=True, text=True
            )
            
            # Exibir a saída completa para depuração
            print(f"Saída do npm outdated:\n{outdated_result.stdout}")
            print(f"Erros do npm outdated:\n{outdated_result.stderr}")

            # Se houver dependências desatualizadas, outdated_result.returncode será 1
            if outdated_result.returncode not in [0, 1]:
                raise subprocess.CalledProcessError(outdated_result.returncode, outdated_result.args, output=outdated_result.stdout, stderr=outdated_result.stderr)
            
            outdated_packages = outdated_result.stdout.strip()
            
            if ignored_deps:
                ignored_array = ignored_deps.split(',')
                for ignored_dep in ignored_array:
                    outdated_packages = '\n'.join(
                        line for line in outdated_packages.split('\n') 
                        if not line.startswith(ignored_dep + ':')
                    )
            
            if outdated_packages:
                print("Dependências desatualizadas encontradas. Atualizando dependências:")
                for package in outdated_packages.split('\n'):
                    package_name = package.split(':')[1]
                    print(f"  - {package_name}")
                
                # Atualiza cada pacote individualmente
                for package in outdated_packages.split('\n'):
                    package_name = package.split(':')[1]
                    print(f"Atualizando {package_name}")
                    subprocess.run(['npm', 'install', package_name, '--legacy-peer-deps'], check=True)
                
                # Adiciona mudanças ao Git, cria um commit e faz push
                subprocess.run(['git', 'add', 'package.json', 'package-lock.json'], check=True)
                subprocess.run(['git', 'commit', '-m', commit_message], check=True)
                subprocess.run(['git', 'push'], check=True)
            else:
                print(f"Todas as dependências estão atualizadas em {full_path}")
        
        except subprocess.CalledProcessError as e:
            print(f"Erro ao verificar/atualizar dependências em {full_path}:")
            print(f"Comando: {e.cmd}")
            print(f"Retorno do comando: {e.returncode}")
            print(f"Saída: {e.output}")
            print(f"Erro: {e.stderr}")
        
        os.chdir('..')

# Função para rodar npx npm-check-updates e atualizar dependências
def ncu_update_projects(projects, commit_message, base_dir):
    project_list = projects.split(',')
    
    for project_dir in project_list:
        full_path = os.path.join(base_dir, project_dir)
        if not os.path.isdir(full_path):
            print(f"O diretório {full_path} não existe.")
            continue
        
        os.chdir(full_path)
        
        print(f"Atualizando todas as dependências em {full_path} com npm-check-updates")
        
        try:
            # Executa npx npm-check-updates
            ncu_result = subprocess.run(['npx', 'npm-check-updates', '-u'], capture_output=True, text=True)
            
            # Exibir a saída completa para depuração
            print(f"Saída do npx npm-check-updates:\n{ncu_result.stdout}")
            print(f"Erros do npx npm-check-updates:\n{ncu_result.stderr}")

            # Se houver atualizações, ncu_result.returncode será 1
            if ncu_result.returncode not in [0, 1]:
                raise subprocess.CalledProcessError(ncu_result.returncode, ncu_result.args, output=ncu_result.stdout, stderr=ncu_result.stderr)
            
            # Executa npm install
            install_result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
            
            # Exibir a saída completa para depuração
            print(f"Saída do npm install:\n{install_result.stdout}")
            print(f"Erros do npm install:\n{install_result.stderr}")
            
            if install_result.returncode != 0:
                raise subprocess.CalledProcessError(install_result.returncode, install_result.args, output=install_result.stdout, stderr=install_result.stderr)
            
            # Adiciona mudanças ao Git, cria um commit e faz push
            subprocess.run(['git', 'add', 'package.json', 'package-lock.json'], check=True)
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            subprocess.run(['git', 'push'], check=True)
        
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar npm-check-updates ou npm install em {full_path}:")
            print(f"Comando: {e.cmd}")
            print(f"Retorno do comando: {e.returncode}")
            print(f"Saída: {e.output}")
            print(f"Erro: {e.stderr}")
        
        os.chdir('..')

# Função para verificar dependências desatualizadas em todos os projetos
def check_outdated_in_all_projects(base_dir):
    for dir in os.listdir(base_dir):
        full_path = os.path.join(base_dir, dir)
        if os.path.isdir(full_path):
            print("Entrando no diretório:", full_path)
            os.chdir(full_path)
            
            try:
                print("Rodando 'outdated' em", full_path)
                subprocess.run(['npm', 'outdated'], check=True)
            
            except subprocess.CalledProcessError as e:
                print(f"Erro ao verificar dependências desatualizadas em {full_path}:")
                print(e.stderr)
            
            os.chdir('..')
    
    print("Verificação concluída.")

# Função para verificar o status do Git em todos os projetos
def check_git_status_in_all_projects(base_dir):
    for dir in os.listdir(base_dir):
        full_path = os.path.join(base_dir, dir)
        if os.path.isdir(full_path):
            print("Entrando no diretório:", full_path)
            os.chdir(full_path)
            
            try:
                print("Verificando o status do Git em", full_path)
                subprocess.run(['git', 'status'], check=True)
            
            except subprocess.CalledProcessError as e:
                print(f"Erro ao verificar o status do Git em {full_path}:")
                print(e.stderr)
            
            os.chdir('..')
    
    print("Verificação de status do Git concluída.")

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
                check_outdated_in_all_projects(base_directory)
            elif opt == '-g':
                check_git_status_in_all_projects(base_directory)
            elif opt == '-n':
                project_directory = args.pop(0)
                ncu_flag = True
            elif opt == '-m':
                commit_message = args.pop(0)
            elif opt in ('-v', '--version'):
                print(f"Versão do programa: {get_program_version()}")
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