import os
import json
import requests
import inquirer
from rich.console import Console
from rich.table import Table
import i18n
from ..codeArt import gitmenArt

console = Console()
CONFIG_GITHUB = os.path.expanduser("~/.gitmen_github.json")


def save_config(username, token):
    config = {"username": username, "token": token}
    with open(CONFIG_GITHUB, "w") as f:
        json.dump(config, f)
    console.print(
        f":white_check_mark: {i18n.t('check_github.saved_credentials', username=f'[bold cyan]{username}[/bold cyan]')}"
    )


def load_config():
    if os.path.exists(CONFIG_GITHUB):
        with open(CONFIG_GITHUB, "r") as f:
            config = json.load(f)
        username = config.get("username")
        console.print(
            f":information_source: {i18n.t('check_github.loaded_username', username=f'[bold cyan]{username}[/bold cyan]')}"
        )
        return config.get("username"), config.get("token")
    return None, None


def check_github():
    saved_username, saved_token = load_config()

    if saved_username and saved_token:
        console.print(
            f":key: {i18n.t('check_github.using_saved_credentials', username=f'[bold cyan]{saved_username}[/bold cyan]')}"
        )
        username = saved_username
        token = saved_token
    else:
        console.print(f":warning: {i18n.t('check_github.no_saved_credentials')}")
        username = saved_username  # Use saved username if available

        questions = [
            inquirer.Text(
                "username", message=i18n.t("check_github.prompt_username"), default=username
            ),
            inquirer.Password(
                "token",
                message=i18n.t("check_github.prompt_token"),
                default=None,
            ),
        ]
        answers = inquirer.prompt(questions)

        username = answers["username"]
        token = answers["token"] if answers["token"] else None

        save_config(username, token)

    # Obter seguidores e seguidos
    followers = get_all_github_data(username, "followers", token)
    following = get_all_github_data(username, "following", token)

    if followers is None:
        console.print(
            f":x: {i18n.t('check_github.followers_none', username=f'[bold cyan]{username}[/bold cyan]')}"
        )
    elif followers == []:
        console.print(
            f":x: {i18n.t('check_github.followers_failed', username=f'[bold cyan]{username}[/bold cyan]')}"
        )
    else:
        console.print(
            f":white_check_mark: {i18n.t('check_github.followers_fetched', count=len(followers), username=f'[bold cyan]{username}[/bold cyan]')}"
        )

    if following is None:
        console.print(
            f":x: {i18n.t('check_github.following_none', username=f'[bold cyan]{username}[/bold cyan]')}"
        )
    elif following == []:
        console.print(
            f":x: {i18n.t('check_github.following_failed', username=f'[bold cyan]{username}[/bold cyan]')}"
        )
    else:
        console.print(
            f":white_check_mark: {i18n.t('check_github.following_fetched', count=len(following), username=f'[bold cyan]{username}[/bold cyan]')}"
        )

    if followers and following:
        display_comparison_table(username, followers, following)
        # display_comparison_table_back(username, followers, following)
        

    console.print(f"[bold red]{gitmenArt}[/bold red]")
    console.print(f":white_check_mark: {i18n.t('check_status.complete_status')}")


def get_all_github_data(username, endpoint, token=None):
    all_data = []
    page = 1
    while True:
        data = get_github_data(username, endpoint, token, page)
        if not data:
            break
        if isinstance(data, list) and not data:
            break
        all_data.extend(data)
        page += 1
    return all_data


def get_github_data(username, endpoint, token=None, page=1):
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"

    url = f"https://api.github.com/users/{username}/{endpoint}?page={page}&per_page=100"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 403:
        console.print(
            f":x: {i18n.t('check_github.rate_limit', endpoint=endpoint, username=f'[bold cyan]{username}[/bold cyan]')}"
        )
        return []
    else:
        console.print(
            f":x: {i18n.t('check_github.fetch_failed_status', endpoint=endpoint, username=f'[bold cyan]{username}[/bold cyan]', status=response.status_code)}"
        )
        return []


def display_comparison_table(username, followers, following):
    followers_logins = {follower["login"]: follower for follower in followers}
    following_logins = {followed["login"]: followed for followed in following}

    followers_table = Table(
        title=i18n.t("check_github.table_title", username=f"{username}")
    )
    followers_table.add_column(i18n.t("check_github.column_user"), style="cyan")
    followers_table.add_column(
        i18n.t("check_github.column_follows_back"), style="green"
    )

    for follower in following_logins:
        follows_back = (
            i18n.t("check_github.yes_label")
            if follower in followers_logins
            else i18n.t("check_github.no_label")
        )
        followers_table.add_row(follower, follows_back)

    console.print(followers_table)

    console.print(i18n.t("check_github.total_followers", count=len(followers)))
    console.print(i18n.t("check_github.total_following", count=len(following)))
    
# def display_comparison_table_back(username, followers, following):
#     followers_logins = {follower["login"]: follower for follower in followers}
#     following_logins = {followed["login"]: followed for followed in following}

#     followers_table = Table(title=f"Comparison if I'm follow  back of {username}")
#     followers_table.add_column("User", style="cyan")
#     followers_table.add_column("Follows Back?", style="green")

#     for follower in followers_logins:
#         follows_back = "Yes" if follower in following_logins else "No"
#         followers_table.add_row(follower, follows_back)

#     console.print(followers_table)

#     console.print(f"Total followers: {len(followers)}")
#     console.print(f"Total following: {len(following)}")
