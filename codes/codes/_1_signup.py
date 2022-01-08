from tkinter import *
from tkinter import ttk

from json_funcs import A0_manag_data_func as mdf


class Signup:
    """
    Builds sign up page on root window
    """
    def __init__(self, window):
        self.window = window

        self.window.minsize(420, 350)
        self.window.maxsize(500, 400)

        # Creates sign up frame to be displayed on the root window
        self.signup_page = ttk.Frame(self.window)
        self.signup_page.pack(fill='both', expand=True)

        # Defines attributes of columns in grids
        self.signup_page.grid_columnconfigure(0, weight=1)
        self.signup_page.grid_columnconfigure(1, weight=1)

        # Declares dynamic string variables 
        self.name = StringVar(self.signup_page)
        self.username = StringVar(self.signup_page)
        self.password = StringVar(self.signup_page)
        self.confirm_password = StringVar(self.signup_page)

        # Declares validation boolean variables
        self.validation1 = False
        self.validation2 = False
        self.validation3 = False
        self.validation4 = False

        # Calls functions which build each set of widgets on the frame
        self.build_labels()
        self.build_entries()
        self.build_buttons()
        self.build_error_labels()


    def build_labels(self):
        """
        Builds every static label on the page.
        Each label belongs to a cell in the grid layout
        """
        welcome_label = ttk.Label(self.signup_page, text="Sign Up Page", font=('Arial', 16, 'bold'))
        welcome_label.grid(row=0, column=0, pady=20, padx=15, sticky=W)

        name_label = ttk.Label(self.signup_page, text="Full Name")
        name_label.grid(row=1, column=0, padx=10, pady=(20, 5), sticky=W)

        username_label = ttk.Label(self.signup_page, text="Admin Username")
        username_label.grid(row=1, column=1, padx=10, pady=(20, 5), sticky=W)

        password_label = ttk.Label(self.signup_page, text="Password")
        password_label.grid(row=4, column=0, padx=10, pady=(20, 5), sticky=W)

        confirm_password_label = ttk.Label(self.signup_page, text="Confirm Password")
        confirm_password_label.grid(row=4, column=1, padx=10, pady=(20, 5), sticky=W)


    def build_entries(self):
        """
        Builds every entry box on the frame
        """
        # Passes the function check_name to another function handler through .register method
        name_vcmd = self.signup_page.register(self.check_name)

        # Evaluates name validation at each keystroke through function handler 
        name_entry = ttk.Entry(self.signup_page, textvariable=self.name, width=30, validate='key', validatecommand=(name_vcmd, '%P'))
        name_entry.grid(row=2, column=0, padx=(10, 30), sticky=W)


        username_vcmd = self.signup_page.register(self.check_username)
        username_entry = ttk.Entry(self.signup_page, textvariable=self.username, width=30, validate='key', validatecommand=(username_vcmd, '%P'))
        username_entry.grid(row=2, column=1, padx=(10, 30), sticky=W)


        password_vcmd = self.signup_page.register(self.check_password)
        password_entry = ttk.Entry(self.signup_page, show="*", textvariable=self.password, width=30, validate='key', validatecommand=(password_vcmd, '%P'))
        password_entry.grid(row=5, column=0, padx=(10, 30), sticky=W)


        password_confirm_vcmd = self.signup_page.register(self.check_password_confirm)
        confirm_password_entry = ttk.Entry(self.signup_page, show="*", textvariable=self.confirm_password, width=30, validate='focusout', validatecommand=(password_confirm_vcmd, '%P'))
        confirm_password_entry.grid(row=5, column=1, padx=(10, 30), sticky=W)


    def build_buttons(self):
        """
        Builds the 2 buttons: Ok and Back
        """
        ok_button = ttk.Button(self.signup_page, text="OK",command=self.open_confirmation_page)
        ok_button.grid(row=7, column=1, padx=(10, 30), pady=20, ipadx=53, ipady=5, sticky=W)

        back_button = ttk.Button(self.signup_page, text="Back", command=self.back_to_welcome_screen)
        back_button.grid(pady=20, ipady=5, ipadx=10, columnspan=2)


    def build_error_labels(self):
        """
        Builds error labels
        """
        self.name_err_label = ttk.Label(self.signup_page, foreground='red')
        self.username_err_label = ttk.Label(self.signup_page, foreground='red')
        self.password_err_label = ttk.Label(self.signup_page, foreground='red')
        self.password_confirm_err_label = ttk.Label(self.signup_page, foreground='red')


    def check_name(self, val):
        """
        This function holds all the conditional checks which evaluate the name entry
        """
        # Lists all special characters
        special_characters = "!@#$%^&*()-+?_=,<>/.,';:[]\{\}"
        # Fetches the managers data and puts them in a list
        names_list = list(di['Name'] for di in mdf.get_managers_data().values())

        # Ensures name does not contain a number
        if any(ch.isnumeric() for ch in val):
            self.name_err_label['text'] = "Numbers are not allowed"
            self.name_err_label.grid(row=3, column=0, padx=(10, 0), sticky=W)
            self.validation1 = False
            return False

        # Ensures name does not contain a special character
        elif any(ch in special_characters for ch in val):
            self.name_err_label['text'] = "Special characters are not allowed"
            self.name_err_label.grid(row=3, column=0, padx=(10, 0), sticky=W)
            self.validation1 = False
            return False

        # Ensures name size is greater than 5 characters
        elif len(val) < 5:
            self.name_err_label['text'] = "Name must be greater than 5 characters"
            self.name_err_label.grid(row=3, column=0, padx=(10, 0), sticky=W)
            self.validation1 = False
            return True

        # Ensures name size is less tha 15 characters
        elif len(val) > 15:
            self.name_err_label['text'] = "Name is limited to 15 characters"
            self.name_err_label.grid(row=3, column=0, padx=(10, 0), sticky=W)
            self.validation1 = False
            return False

        # Ensures name is not already existent in managers database using above list
        elif val in names_list:
            self.name_err_label['text'] = "This name has already an account"
            self.name_err_label.grid(row=3, column=0, padx=(10, 0), sticky=W)
            self.validation1 = False
            return True

        # Deletes any error label if entry is empty
        elif self.name_err_label != "":
            self.name_err_label.destroy()
            self.build_error_labels()

        # Is accessed only if all conditions are satisfied. Validation is made True.
        self.validation1 = True
        return True


    def check_username(self, val):
        """
        This function holds all the conditional checks which evaluate the username entry
        """
        special_characters = "!@#$%^&*()-+?_=,<>/.,';:[]\{\}"
        usernames_list = list(username for username in mdf.get_managers_data().keys())

        # Ensures username does not contain a space character
        if any(ch == " " for ch in val):
            self.username_err_label['text'] = "Userame cannot have a space character"
            self.username_err_label.grid(
                row=3, column=1, padx=(10, 0), sticky=W)
            self.validation2 = False
            return False

        # Ensures username does not exceed 15 characters
        elif len(val) > 15:
            self.username_err_label['text'] = "Userame is limited to 15 characters"
            self.username_err_label.grid(
                row=3, column=1, padx=(10, 0), sticky=W)
            self.validation2 = False
            return False

        # Ensures username size is greater than 5 characters
        elif len(val) < 5:
            self.username_err_label['text'] = "Name must be greater than 5 characters"
            self.username_err_label.grid(
                row=3, column=1, padx=(10, 0), sticky=W)
            self.validation2 = False
            return True

        # Ensures username does not contain any special character
        elif any(ch in special_characters for ch in val):
            self.username_err_label['text'] = "Special characters are not allowed"
            self.username_err_label.grid(
                row=3, column=1, padx=(10, 0), sticky=W)
            self.validation2 = False
            return False

        # Ensures username is not already existent in database
        elif val in usernames_list:
            self.username_err_label['text'] = "Username is already taken"
            self.username_err_label.grid(
                row=3, column=1, padx=(10, 0), sticky=W)
            self.validation2 = False
            return True

        # Deletes error label if entry is empty
        elif self.username_err_label != "":
            self.username_err_label.destroy()
            self.build_error_labels()

        # Validation is made True if every condition is checked
        self.validation2 = True
        return True


    def check_password(self, val):
        """
        This function holds all the conditional checks which evaluate the password entry
        """
        special_characters = "!@#$%^&*()-+?_=,<>/.,';:[]\{\}"

        # Ensures password is at least 7 characters
        if len(val) < 6:
            self.password_err_label['text'] = "Password must be 7 characters long"
            self.password_err_label.grid(
                row=6, column=0, padx=(10, 0), sticky=W)
            self.validation3 = False
            return True

        # Ensures password contains at least one number
        elif not any(ch.isnumeric() for ch in val):
            self.password_err_label['text'] = "Password must contain one number"
            self.password_err_label.grid(
                row=6, column=0, padx=(10, 0), sticky=W)
            self.validation3 = False
            return True

        # Ensures password contains at least one special character
        elif not any(ch in special_characters for ch in val):
            self.password_err_label['text'] = "Password must contain one special character"
            self.password_err_label.grid(
                row=6, column=0, padx=(10, 0), sticky=W)
            self.validation3 = False
            return True

        # Deletes error label if entry is empty
        elif self.password_err_label != "":
            self.password_err_label.destroy()
            self.build_error_labels()

        self.validation3 = True
        return True


    def check_password_confirm(self, val):
        """
        This function holds all the conditional checks which evaluate the password confirmation entry
        """
        # Checks that second password matches first one
        if val != self.password.get():
            self.password_confirm_err_label['text'] = "Passwords do not match"
            self.password_confirm_err_label.grid(
                row=6, column=1, padx=(10, 0), sticky=W)
            self.validation4 = False
            return True

        elif self.password_confirm_err_label != "":
            self.password_confirm_err_label.destroy()
            self.build_error_labels()

        self.validation4 = True
        return True


    def open_confirmation_page(self):
        """
        This function opens a confirmation page for a manager to authorize the new manager sign up.
        """
        # If all entries have been validated, the confirmation page is opened.
        if self.validation1 == self.validation2 == self.validation3 == self.validation4 == True:
            self.confirm_page = Tk()
            self.confirm_page.title("Manager Confirmation")

            confirm_frame = ttk.Frame(self.confirm_page)

            style = ttk.Style(self.confirm_page)  # add style to treeview
            style.theme_use("clam")

            message = ttk.Label(confirm_frame, text="Please introduce the password of one of the authorized managers to continue")
            message.pack(padx=10, pady=10)

            self.pswd_entry = ttk.Entry(confirm_frame, show="*")
            self.pswd_entry.pack(padx=10, pady=10)

            self.confirm_message = ttk.Label(confirm_frame)
            self.confirm_message.pack(padx=10, pady=10)

            ok_button = ttk.Button(
                confirm_frame, text="Ok", command=self.check_password_manager)
            ok_button.pack(padx=10, pady=10)

            confirm_frame.pack(fill='both', expand=True)


    def check_password_manager(self):
        """
        This function checks if the manager password is already existent in the managers database
        """

        passwords_list = list(di['Password'] for di in mdf.get_managers_data().values())
        if self.pswd_entry.get() in passwords_list:
            mdf.add_managers_data(
                self.name.get(), self.username.get(), self.confirm_password.get())

            self.pswd_entry.delete(0, END)
            self.confirm_message['text'] = "New Manager successfully added"
            self.confirm_message['foreground'] = 'green'

            self.confirm_page.destroy()
            self.signup_page.destroy()

            from _2_login import Login
            Login(self.window)

        else:
            self.pswd_entry.delete(0, END)
            self.confirm_message['text'] = "Password not recognized"
            self.confirm_message['foreground'] = 'red'


    def back_to_welcome_screen(self):
        """
        Destroys sign up page and builds login page
        """
        from _0_welcome import WelcomePage  # Local import to avoid circular import error
        WelcomePage(self.window)
        self.signup_page.destroy()
