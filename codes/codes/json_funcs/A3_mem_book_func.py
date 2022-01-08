import json

# Defines paths of database files
members_book_json_path = "../json_files/members_book.json"


def get_members_booking():
    """
    Opens database and returns dictionary
    """
    with open(members_book_json_path) as json_file:
        return json.load(json_file)  # returns a list of dictionaries


def push_members_booking(members_book):
    """
    Updates and closes database file
    """
    members_json = json.dumps(members_book)  # converts from a list into  json file
    jsonFile = open(members_book_json_path, "w")
    jsonFile.write(members_json)  # writes a new(updated) list content into our json file
    jsonFile.close()


def add_guest_booking(iid):
    """
    Adds new guest user
    """
    members_book = get_members_booking()
    members_book[iid] = {"Status": "Inactive", "Login Time": "", "Logout Time": ""}

    push_members_booking(members_book)


def remove_guest_book(iid):
    """
    Removes guest user from database
    """
    members_book = get_members_booking()
    members_book.pop(iid)

    push_members_booking(members_book)


def reset_member_booking(iid):
    """
    Clears every field in record and set status to "Inactive"
    """
    members_book = get_members_booking()

    members_book[iid] = {"Status": "Inactive", "Login Time": "", "Logout Time": ""}

    push_members_booking(members_book)


def start_update(iid, start_time):
    """
    Starts session and takes start time
    """
    members_book = get_members_booking()
    members_book[iid] = {"Status": "Active", "Login Time": start_time, "Logout Time": ""}

    push_members_booking(members_book)


def end_update(iid, start_time, end_time):
    """
    Ends session and takes both start and end times
    """
    members_book = get_members_booking()
    members_book[iid] = {"Status": "Ended", "Login Time": start_time, "Logout Time": end_time}

    push_members_booking(members_book)
