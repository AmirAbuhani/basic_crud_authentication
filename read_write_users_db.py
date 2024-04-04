import json


def read_users():
    with open("data/usernames_passwords.json", "r") as file:
        data = json.load(file)
        return data


def write_users(username, password):
    data = read_users()
    detail = {
        "username": username,
        "password": password
    }
    # Append the new user detail to the existing data
    data.append(detail)
    with open("data/usernames_passwords.json", "w") as file:
        json.dump(data, file, indent=2)
