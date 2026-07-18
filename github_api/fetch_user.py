import requests

def get_user(username):
    url = f"https://api.github.com/users/{username}"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

    return None