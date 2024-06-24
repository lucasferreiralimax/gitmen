import os
import i18n
import platform
import subprocess

def i18nConfig():
    # Obter informações do sistema
    system_info = platform.system()

    if system_info == 'Windows':
        # Para Windows, usando o módulo winreg para obter o idioma
        import winreg

        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Control Panel\\International", 0, winreg.KEY_READ)
        system_lang, _ = winreg.QueryValueEx(key, "LocaleName")
        winreg.CloseKey(key)
        
    elif system_info == 'Darwin':
        # Para macOS, usando o comando 'defaults' para obter o idioma
        proc = subprocess.Popen(['defaults', 'read', '-g', 'AppleLocale'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = proc.communicate()
        system_lang = out.strip().decode('utf-8')

    else:
        # Para Linux e outros sistemas baseados em Unix, usando 'locale' para obter o idioma
        proc = subprocess.Popen(['locale'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = proc.communicate()
        system_lang = out.split()[0].decode('utf-8').split('=')[1]

    if system_lang:
        system_lang = system_lang[:2]

     # Determina o caminho absoluto para a pasta translations
    package_dir = os.path.dirname(os.path.abspath(__file__))
    translations_path = os.path.join(package_dir, 'translations')

    i18n.load_path.append(translations_path)
    i18n.set('fallback', 'en')
    i18n.set('locale', system_lang)