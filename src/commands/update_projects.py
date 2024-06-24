import os
import subprocess

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