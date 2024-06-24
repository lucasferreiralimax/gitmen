import os
import subprocess

# Função para verificar o status do Git em todos os projetos
def check_status(base_dir):
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