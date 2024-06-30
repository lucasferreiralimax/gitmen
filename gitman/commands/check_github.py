import os
import json
import requests
import inquirer
from rich.console import Console
from rich.table import Table
import i18n
from ..codeArt import gitmanArt

console = Console()
CONFIG_GITHUB = os.path.expanduser("~/.gitman_github.json")


def save_config(username, token):
    config = {"username": username, "token": token}
    with open(CONFIG_GITHUB, "w") as f:
        json.dump(config, f)
    console.print(f"Saved GitHub credentials: {username}")


def load_config():
    if os.path.exists(CONFIG_GITHUB):
        with open(CONFIG_GITHUB, "r") as f:
            config = json.load(f)
        username = config.get("username")
        console.print(f"Loaded GitHub username: {username}")
        return config.get("username"), config.get("token")
    return None, None


def check_github():
    saved_username, saved_token = load_config()

    if saved_username and saved_token:
        console.print(f"Using saved GitHub credentials for user: {saved_username}")
        username = saved_username
        token = saved_token
    else:
        console.print("No saved GitHub credentials found.")
        username = saved_username  # Use saved username if available

        questions = [
            inquirer.Text(
                "username", message="Enter GitHub username", default=username
            ),
            inquirer.Password(
                "token",
                message="Enter GitHub token (leave blank for unauthenticated requests)",
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
        console.print(f"❌ No followers found for user {username}")
    elif followers == []:
        console.print(f"❌ Failed to fetch followers for user {username}")
    else:
        console.print(f"✅ Fetched {len(followers)} followers for user {username}")

    if following is None:
        console.print(f"❌ No users followed by {username}")
    elif following == []:
        console.print(f"❌ Failed to fetch following for user {username}")
    else:
        console.print(f"✅ Fetched {len(following)} users followed by {username}")

    if followers and following:
        display_comparison_table(username, followers, following)
        # display_comparison_table_back(username, followers, following)
        

    console.print(f"[bold red]{gitmanArt}[/bold red]")
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
            f":x: Rate limit exceeded or authentication required for fetching {endpoint} for user {username}"
        )
        return []
    else:
        console.print(
            f":x: Failed to fetch {endpoint} for user {username}. Status code: {response.status_code}"
        )
        return []


def display_comparison_table(username, followers, following):
    followers_logins = {follower["login"]: follower for follower in followers}
    following_logins = {followed["login"]: followed for followed in following}

    followers_table = Table(title=f"Followers and Following Comparison for {username}")
    followers_table.add_column("User", style="cyan")
    followers_table.add_column("Follows Back?", style="green")

    for follower in following_logins:
        follows_back = "Yes" if follower in followers_logins else "No"
        followers_table.add_row(follower, follows_back)

    console.print(followers_table)

    console.print(f"Total followers: {len(followers)}")
    console.print(f"Total following: {len(following)}")
    
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
