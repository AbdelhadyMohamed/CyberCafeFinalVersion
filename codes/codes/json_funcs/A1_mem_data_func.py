import json

# Defines path of database file
members_json_path = "../json_files/members_data.json"

def get_members_data():
    """
    Opens database and returns dictionary
    """
    with open(members_json_path) as json_file:
        return json.load(json_file)  # returns a list of dictionaries


def push_members_data(my_json_dict):
    """
    Updates and closes database file
    """
    members_json = json.dumps(my_json_dict)
    jsonFile = open(members_json_path, "w")
    jsonFile.write(members_json)
    jsonFile.close()
    

def add_to_members_database(position, first_name, last_name, phone, address, email, username):  # converts the members_bd from list to json file to write new member
    """
    Adds dictionary in database
    """
    # creates dictionary of passed elements
    new_dict = {
        "id": position,
        "First Name": first_name,
        "Last Name": last_name,
        "Phone": phone,
        "Address": address,
        "E-mail": email
    }

    # fetches json dictionary
    my_json_dict = get_members_data()

    my_json_dict[username] = new_dict

    push_members_data(my_json_dict)



def delete_from_member_database(iid):
    """
    Deletes from database
    """
    my_json_dict = get_members_data()

    # deletes dictionary from json
    my_json_dict.pop(iid)  # removes index selected from treeview

    push_members_data(my_json_dict)



def update_members_data_base(username, position, first_name, last_name, phone, address, email):
    """
    Changes value from dictionary
    """
    # Gets new values to use for update
    updated_record = {"id": position,
                      "First Name": first_name,
                      "Last Name": last_name,
                      "Phone": phone,
                      "Address": address,
                      "E-mail": email
                      }

    my_json_dict = get_members_data()
    my_json_dict[username] = updated_record  # overwrites in the old position

    push_members_data(my_json_dict)
