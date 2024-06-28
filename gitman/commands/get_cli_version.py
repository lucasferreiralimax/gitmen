from importlib.metadata import version
import i18n


# Função para exibir a versão do programa
def get_cli_version():
    try:
        print(i18n.t("comman.version", version=version("gitman")))
    except Exception:
        print(i18n.t("comman.version_not_found"))
