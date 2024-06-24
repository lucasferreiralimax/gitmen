import os
import subprocess
import i18n

# Função para verificar dependências desatualizadas em todos os projetos
def check_outdated(base_dir):
    for dir in os.listdir(base_dir):
        full_path = os.path.join(base_dir, dir)
        if os.path.isdir(full_path):
            print(i18n.t('check_outdated.entering_directory', fullpath=full_path))
            os.chdir(full_path)
            
            try:
                print(i18n.t('check_outdated.running_outdated', fullpath=full_path))
                subprocess.run(['npm', 'outdated'], check=True)
            
            except subprocess.CalledProcessError as e:
                print(i18n.t('check_outdated.error', fullpath=full_path))
                print(e.stderr)
            
            os.chdir('..')
    
    print(i18n.t('check_status.complete_status'))