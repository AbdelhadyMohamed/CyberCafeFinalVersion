import string
from string import punctuation
from tkinter import ttk


def check_entries(page, E1, E2, E3, E4, E5, E6):
    """
    Contains all error checks on every entry in edit members page
    """
    # Creates error label without initial text
    error_label =  ttk.Label(page,foreground='red')

    # Prevents 4 first labels to be null
    if E1 == '' and E2 == '' and E3 == '' and E4 == '':
        error_label['text'] = "All entities are empty pls fill it in or select one to process"
        error_label.pack()
        error_label.after(3000, error_label.destroy)
        return False

    # Checks if first name is null value
    if E1 == '':
        error_label['text'] = "First name entry is empty please write it"
        error_label.pack()
        error_label.after(3000, error_label.destroy)
        return False

    # Checks if first name is other than characters
    if any(item in E1 for item in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']) == True or any(
            item in E1 for item in
            punctuation) == True:
        error_label['text'] = "First name can not be a number or a special character"
        error_label.pack()
        error_label.after(3000, error_label.destroy)
        return False

    # First name must be less than 20 characters
    if len(E1) >= 20:
        error_label['text'] = "First name must be less than 20 character"
        error_label.pack()
        error_label.after(3000, error_label.destroy)

    # Last name cannot be empty
    if E2 == '':
        error_label['text'] = "Last name entry is empty please write it"
        error_label.pack()
        error_label.after(3000, error_label.destroy)
        return False

    # Check if last name is other than characters
    if any(item in E2 for item in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']) == True or any(
            item in E2 for item in
            punctuation) == True:
        "last name can not start with number or special character"
        error_label.pack()
        error_label.after(3000, error_label.destroy)
        return False

    # Last name must be less than 20 characters
    if len(E2) >= 20:
        error_label['text'] = "second name must be less than 20 character"
        error_label.pack()
        error_label.after(3000, error_label.destroy)

    # Check if phone number is not char or special char
    if any(item in E3 for item in list(string.ascii_letters)) == True or any(
            item in E3 for item in punctuation) == True:
        error_label['text'] = "Phone number can not be character or special number "
        error_label.pack()
        error_label.after(3000, error_label.destroy)
        return False

    # Check size of phone number
    if len(E3) >= 14 or len(E3) < 6:
        error_label['text'] = "Phone number must be between 6 to 14 number "
        error_label.pack()
        error_label.after(3000, error_label.destroy)
        return False

    # Checks if address entry is empty
    if E4 == '':
        error_label['text'] = "Address can not be empty"
        error_label.pack()
        error_label.after(3000, error_label.destroy)
        return False

    # Checks size of address
    if len(E4) >= 25:
        error_label['text'] = "Address can not be more than 25 characters"
        error_label.pack()
        error_label.after(3000, error_label.destroy)
        return False

    # Checks if email address contains @ symbol
    if '@' not in E5:
        error_label['text'] = "Email format is not recognized"
        error_label.pack()
        error_label.after(3000, error_label.destroy)
        return False

    # Checks if username is null
    if E6 == "":
        error_label['text'] = "Username can not be null"
        error_label.pack()
        error_label.after(3000, error_label.destroy)
        return False

    return True
