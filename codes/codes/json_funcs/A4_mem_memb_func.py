import json

# Defines path of database file
members_memb_json_path = "../json_files/members_membership.json"


def get_membership():
    """
    Opens database and returns dictionary
    """
    with open(members_memb_json_path) as json_file:
        return json.load(json_file)  # returns a list of dictionaries


def push_members_membership(membership):
    """
    Updates and closes database file
    """
    members_json = json.dumps(membership)  # converts from a list into  json file
    jsonFile = open(members_memb_json_path, "w")
    jsonFile.write(members_json)  # writes a new(updated) list content into our json file
    jsonFile.close()


def activate_membership(iid, start_date, end_date, plan_type):
    """
    Starts membership with variable plan
    """
    members_book = get_membership()
    members_book[iid] = {"Status": "Running", "Start Date": start_date, "End Date": end_date, "Plan Type": plan_type}

    push_members_membership(members_book)


def deactivate_membership(iid):
    """
    Cancels membership
    """
    members_book = get_membership()

    members_book[iid] = {"Status": "Inactive", "Start Date": "", "End Date": "", "Plan Type": ""}
    
    push_members_membership(members_book)


def remove_membership(iid):
    """
    Removes membership from database
    """
    members_book = get_membership()

    members_book.pop(iid)

    push_members_membership(members_book)
