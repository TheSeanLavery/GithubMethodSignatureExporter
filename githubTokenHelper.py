import os
import requests

CONFIG_FILENAME = "getsig.config"


def check_pat_expiration(pat):
    headers = {"Authorization": f"token {pat}"}
    response = requests.get("https://api.github.com/user", headers=headers)

    if response.status_code == 200:
        return True
    else:
        return False


def load_existing_pat():
    if os.path.exists(CONFIG_FILENAME):
        with open(CONFIG_FILENAME, "r") as config_file:
            return config_file.readline().strip()
    return None


def save_pat(pat):
    with open(CONFIG_FILENAME, "w") as config_file:
        config_file.write(pat)


def display_instructions():
    print("\nTo proceed, you will need a GitHub Personal Access Token (PAT) with the following permissions:")
    print("  - Read access to code")
    print("  - Read access to metadata")
    print("\nTo create a new PAT, follow these steps:")
    print("1. Visit https://github.com/settings/tokens?type=beta")
    print("2. Click the 'Generate new token' button")
    print("3. Enter a token description (e.g., 'getsig')")
    print("4. Under 'Select scopes', check the 'read:code' and 'read:metadata' permissions")
    print("5. Click 'Generate token'")
    print("6. Copy the generated token (Note: You won't be able to see it again)\n")


def get_new_pat():
    display_instructions()
    pat = input("Please enter your GitHub Personal Access Token (PAT): ")
    while not check_pat_expiration(pat):
        print("\nThe provided token is invalid or expired.")
        pat = input("Please enter a valid GitHub Personal Access Token (PAT): ")

    save_pat(pat)
    return pat


def get_token():
    existing_pat = load_existing_pat()

    if existing_pat and check_pat_expiration(existing_pat):
        return existing_pat
    else:
        return get_new_pat()


if __name__ == "__main__":
    pat = get_token()
    print("\nYour PAT is ready to use!")
