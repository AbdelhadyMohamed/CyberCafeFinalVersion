import json

# Defines path of database file
managers_json_path = "../json_files/managers_data.json"


def get_managers_data():
    """
    Opens database and returns dictionary
    """
    with open(managers_json_path) as json_file:
        return json.load(json_file)  # returns a list of dictionaries


def push_managers_data(my_json_dict):
    """
    Updates and closes database file
    """
    members_json = json.dumps(my_json_dict)
    jsonFile = open(managers_json_path, "w")
    jsonFile.write(members_json)
    jsonFile.close()


def add_managers_data(name, username, password):
    """
    Add new manager in database
    """
    my_json_dict = get_managers_data()

    my_json_dict[username] = {"Name": name, "Password": password}

    push_managers_data(my_json_dict)
