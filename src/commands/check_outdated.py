import os
import subprocess

# Função para verificar dependências desatualizadas em todos os projetos
def check_outdated(base_dir):
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