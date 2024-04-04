import json


def read_users():
    with open("data/usernames_passwords.json", "r") as file:
        data = json.load(file)
        return data


def write_users(username, password):
    data = read_users()
    # if isinstance(password, bytes):
    #     password = password.decode('utf-8')
    detail = {
        "username": username,
        "password": password
    }
    data.append(detail)  # Append the new user detail to the existing data
    with open("data/usernames_passwords.json", "w") as file:  # Open in write mode
        json.dump(data, file, indent=2)
