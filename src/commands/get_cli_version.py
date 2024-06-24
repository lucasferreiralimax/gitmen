from importlib.metadata import version

# Função para exibir a versão do programa
def get_cli_version():
    try:
        return version('gitman')
    except Exception:
        return "Versão desconhecida"