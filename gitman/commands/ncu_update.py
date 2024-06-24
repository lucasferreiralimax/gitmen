import os
import subprocess
import i18n

# Função para rodar npx npm-check-updates e atualizar
def ncu_update(projects, commit_message, base_dir):
    project_list = projects.split(',')
    
    for project_dir in project_list:
        full_path = os.path.join(base_dir, project_dir)
        if not os.path.isdir(full_path):
            print(i18n.t('ncu_update.ncu_directory_not_exist').format(fullpath=full_path))
            continue
        
        print(i18n.t('ncu_update.ncu_entering_directory').format(fullpath=full_path))
        os.chdir(full_path)
        
        try:
            print(i18n.t('ncu_update.ncu_running').format(fullpath=full_path))
            # Executa npx npm-check-updates
            ncu_result = subprocess.run(['npx', 'npm-check-updates', '-u'], capture_output=True, text=True)
            
            # Exibir a saída completa para depuração
            print(i18n.t('ncu_update.ncu_output').format(output=ncu_result.stdout))
            print(i18n.t('ncu_update.ncu_errors').format(errors=ncu_result.stderr))

            # Se houver atualizações, ncu_result.returncode será 1
            if ncu_result.returncode not in [0, 1]:
                raise subprocess.CalledProcessError(ncu_result.returncode, ncu_result.args, output=ncu_result.stdout, stderr=ncu_result.stderr)
            
            # Executa npm install
            install_result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
            
            # Exibir a saída completa para depuração
            print(i18n.t('ncu_update.ncu_npm_install_output').format(output=install_result.stdout))
            print(i18n.t('ncu_update.ncu_npm_install_errors').format(errors=install_result.stderr))
            
            if install_result.returncode != 0:
                raise subprocess.CalledProcessError(install_result.returncode, install_result.args, output=install_result.stdout, stderr=install_result.stderr)
            
            # Adiciona mudanças ao Git, cria um commit e faz push
            subprocess.run(['git', 'add', 'package.json', 'package-lock.json'], check=True)
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            subprocess.run(['git', 'push'], check=True)
            
            print(i18n.t('ncu_update.ncu_git_commit_message').format(message=commit_message))
            print(i18n.t('ncu_update.ncu_git_push'))
        
        except subprocess.CalledProcessError as e:
            print(i18n.t('ncu_update.ncu_error').format(fullpath=full_path))
            print(i18n.t('ncu_update.ncu_command').format(command=e.cmd))
            print(i18n.t('ncu_update.ncu_return_code').format(returncode=e.returncode))
            print(i18n.t('ncu_update.ncu_output').format(output=e.output.decode()))
            print(i18n.t('ncu_update.ncu_error_details').format(errors=e.stderr.decode()))
        
        os.chdir('..')
    
    print(i18n.t('ncu_update.ncu_complete'))