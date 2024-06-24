import os
import subprocess
import i18n

# Função para verificar o status do Git em todos os projetos
def check_status(base_dir):
    for dir in os.listdir(base_dir):
        full_path = os.path.join(base_dir, dir)
        if os.path.isdir(full_path):
            print(i18n.t('check_status.entering_directory', fullpath=full_path))
            os.chdir(full_path)
            
            try:
                print(i18n.t('check_status.checking_git_status', fullpath=full_path))
                subprocess.run(['git', 'status'], check=True)
            
            except subprocess.CalledProcessError as e:
                print(i18n.t('check_status.git_error', fullpath=full_path))
                print(e.stderr)
            
            os.chdir('..')

    print(i18n.t('check_status.complete_status'))