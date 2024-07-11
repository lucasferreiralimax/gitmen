import os
import i18n
import platform
import subprocess
import inquirer
import json

CONFIG_FILE = os.path.expanduser("~/.gitmen_config.json")


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def set_language(language):
    config = load_config()
    config["language"] = language
    save_config(config)


def get_language():
    config = load_config()
    return config.get("language", None)


def select_language():
    languages = ["en", "pt"]
    questions = [
        inquirer.List(
            "language",
            message=i18n.t("comman.select_language"),
            choices=languages,
        ),
    ]
    answers = inquirer.prompt(questions)
    set_language(answers["language"])
    i18n.set("locale", answers["language"])  # Atualizar o idioma no i18n
    print(i18n.t("comman.language_set", language=answers["language"]))


def i18nConfig():
    # Obter informações do sistema
    system_info = platform.system()
    system_lang = get_language()

    if not system_lang:
        if system_info == "Windows":
            # Para Windows, usando o módulo winreg para obter o idioma
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                "Control Panel\\International",
                0,
                winreg.KEY_READ,
            )
            system_lang, _ = winreg.QueryValueEx(key, "LocaleName")
            winreg.CloseKey(key)

        elif system_info == "Darwin":
            # Para macOS, usando o comando 'defaults' para obter o idioma
            proc = subprocess.Popen(
                ["defaults", "read", "-g", "AppleLocale"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            out, _ = proc.communicate()
            system_lang = out.strip().decode("utf-8")

        else:
            # Para Linux e outros sistemas baseados em Unix, usando 'locale' para obter o idioma
            proc = subprocess.Popen(
                ["locale"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            out, _ = proc.communicate()
            system_lang = out.split()[0].decode("utf-8").split("=")[1]

        if system_lang:
            system_lang = system_lang[:2]

    # Determina o caminho absoluto para a pasta translations
    package_dir = os.path.dirname(os.path.abspath(__file__))
    translations_path = os.path.join(package_dir, "translations")

    # print(f"Translations path: {translations_path}")
    # print(f"System language: {system_lang}")

    i18n.load_path.append(translations_path)
    i18n.set("fallback", "en")
    i18n.set("locale", system_lang)

    # print(f"i18n load_path: {i18n.load_path}")
    # print(f"i18n locale: {i18n.get('locale')}")
    # print(f"i18n fallback: {i18n.get('fallback')}")