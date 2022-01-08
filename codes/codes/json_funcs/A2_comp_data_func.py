import json

# Defines path of database file
computers_json_path = "../json_files/computers_data.json"


def get_computers_data():
    """
    Opens database and returns dictionary
    """
    with open(computers_json_path) as json_file:
        return json.load(json_file)  # returns a list of dictionaries


def push_computer_data(my_json_dict):
    """
    Updates and closes database file
    """
    computers_json = json.dumps(my_json_dict)
    jsonFile = open(computers_json_path, "w")
    jsonFile.write(computers_json)
    jsonFile.close()


def add_to_computer_database(computer_id, computer_name):  # converts the members_bd from list to json file to write new member
    """
    Adds element in database
    """
    # fetches json dictionary
    my_json_dict = get_computers_data()

    my_json_dict[computer_id] = computer_name

    push_computer_data(my_json_dict)



def delete_from_computer_database(iid):
    """
    Deletes element from database
    """
    my_json_dict = get_computers_data()

    # Deletes dictionary from json
    my_json_dict.pop(iid)

    push_computer_data(my_json_dict)


def update_computers_data_base(id, Name):
    """
    Change already existant values
    """
    my_json_dict = get_computers_data()
    my_json_dict[id] = Name
    push_computer_data(my_json_dict)
