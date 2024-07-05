import i18n
from rich.console import Console
from rich.rule import Rule

console = Console()


def deps_logs(deps_up, deps_off=None):
    for item_ignore in deps_off:
        console.print(
            f":stop_sign: [bright_red]{i18n.t('update.up_ignore_package')}[/] [bold orange4]{item_ignore}[/]"
        )
        console.print(Rule(style="grey11"))
    for item_install in deps_up:
        console.print(
            f":rocket: [cyan]{i18n.t('update.up_update_package')}[/] [bold white]{item_install}[/]"
        )
        console.print(Rule(style="grey11"))

def logger_expection(e, full_path):
    console.print(i18n.t("update.up_error").format(fullpath=full_path))
    console.print(i18n.t("update.up_command").format(command=e.cmd))
    console.print(i18n.t("update.up_return_code").format(returncode=e.returncode))
    console.print(i18n.t("update.up_output").format(output=e.output.decode()))
    console.print(i18n.t("update.up_error_details").format(errors=e.stderr.decode()))