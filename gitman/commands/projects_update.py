import os
import subprocess
import i18n

# Função para atualizar dependências de um projeto
def projects_update(projects, ignored_deps, commit_message, base_dir):
    project_list = projects.split(',')
    
    for project_dir in project_list:
        full_path = os.path.join(base_dir, project_dir)
        if not os.path.isdir(full_path):
            print(i18n.t('update.up_directory_not_exist').format(fullpath=full_path))
            continue
        
        os.chdir(full_path)
        
        print(i18n.t('update.up_checking_outdated').format(fullpath=full_path))
        
        try:
            # Gera uma lista de dependências desatualizadas com nome e versão
            outdated_result = subprocess.run(
                ['npm', 'outdated', '--parseable', '--depth=0'], 
                capture_output=True, text=True
            )
            
            # Exibir a saída completa para depuração
            print(i18n.t('update.up_outdated_output').format(output=outdated_result.stdout))
            print(i18n.t('update.up_outdated_errors').format(errors=outdated_result.stderr))

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
                print(i18n.t('update.up_outdated_found'))
                for package in outdated_packages.split('\n'):
                    package_name = package.split(':')[1]
                    print(f"  - {package_name}")
                
                # Atualiza cada pacote individualmente
                for package in outdated_packages.split('\n'):
                    package_name = package.split(':')[1]
                    print(i18n.t('update.up_updating_package').format(package_name=package_name))
                    subprocess.run(['npm', 'install', package_name, '--legacy-peer-deps'], check=True)
                
                # Adiciona mudanças ao Git, cria um commit e faz push
                subprocess.run(['git', 'add', 'package.json', 'package-lock.json'], check=True)
                subprocess.run(['git', 'commit', '-m', commit_message], check=True)
                subprocess.run(['git', 'push'], check=True)
                
                print(i18n.t('update.up_git_commit_message').format(message=commit_message))
                print(i18n.t('update.up_git_push'))
            else:
                print(i18n.t('update.up_all_to_date').format(fullpath=full_path))
        
        except subprocess.CalledProcessError as e:
            print(i18n.t('update.up_error').format(fullpath=full_path))
            print(i18n.t('update.up_command').format(command=e.cmd))
            print(i18n.t('update.up_return_code').format(returncode=e.returncode))
            print(i18n.t('update.up_output').format(output=e.output.decode()))
            print(i18n.t('update.up_error_details').format(errors=e.stderr.decode()))
        
        os.chdir('..')