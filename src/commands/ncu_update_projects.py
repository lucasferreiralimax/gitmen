import os
import subprocess

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
