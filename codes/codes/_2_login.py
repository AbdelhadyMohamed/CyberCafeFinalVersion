from tkinter import *
from tkinter import ttk

from json_funcs import A0_manag_data_func as mdf


class Login:

    def __init__(self, window):
        self.window = window

        self.window.minsize(400, 325)
        self.window.maxsize(450, 375)

        self.login_page = ttk.Frame(window)
        self.login_page.pack(fill='both', expand=True)

        self.username = StringVar(self.login_page)
        self.password = StringVar(self.login_page)

        # Grid configuration
        self.login_page.columnconfigure(0, weight=1)
        self.login_page.columnconfigure(1, weight=3)

        self.managers_db = mdf.get_managers_data()

        self.build_labels()
        self.build_entries()
        self.build_buttons()
        self.build_err_labels()


    def build_labels(self):

        # Page title
        title_label = ttk.Label(self.login_page, text="Login Page", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, sticky=W, columnspan=2, padx=10, pady=20)

        # Username Label
        username_label = ttk.Label(self.login_page, text="username:", font=('Arial', 12))
        username_label.grid(column=0, row=1, padx=10, pady=10)

        # Password Label
        password_label = ttk.Label(self.login_page, text="password:", font=('Arial', 12))
        password_label.grid(column=0, row=3, padx=10, pady=10)


    def build_err_labels(self):

        # Username error label
        self.error_user_label = ttk.Label(self.login_page)

        # Password error label
        self.error_pass_label = ttk.Label(self.login_page)


    def delete_err_labels(self):
        """
        This function resets the error labels by destroying the widget and recreating it without its text parameter
        """
        self.error_user_label.destroy()
        self.build_err_labels()


    def build_entries(self):
        # username entry
        username_entry = ttk.Entry(self.login_page, textvariable=self.username, validate='focusin', validatecommand=self.delete_err_labels)
        username_entry.grid(column=1, row=1, sticky=(N, S, E, W), padx=10, pady=10)
        username_entry.focus()

        # password entry
        password_entry = ttk.Entry(self.login_page, show="*", textvariable=self.password, validate='focusin', validatecommand=self.check_username)
        password_entry.grid(column=1, row=3, sticky=(N, S, E, W), padx=10, pady=10)


    def build_buttons(self):
        # button
        self.ok_button = ttk.Button(self.login_page, text='Ok', command=self.check_password)
        self.ok_button.grid(column=1, row=5, sticky=(N, W, E, S), padx=10, pady=15, ipadx=10, ipady=5)

        self.back_button = ttk.Button(self.login_page, text='Back', command=self.back_to_welcome_screen)
        self.back_button.grid(column=0, pady=15, ipadx=10, ipady=5)


    def check_username(self):
        """
        This function checks if username is existent in database
        """
        user_input = self.username.get()

        # If username is recognized, executes this condition
        if user_input in self.managers_db.keys():
            self.error_user_label['foreground'] = "green"
            self.error_user_label['text'] = "Valid Username"
            self.error_user_label.grid(column=1, row=2, sticky=W, padx=10)
            return True

        # 
        elif user_input == '':
            self.error_user_label['foreground'] = "red"
            self.error_user_label['text'] = "Please enter a valid username"
            self.error_user_label.grid(column=1, row=2, sticky=W, padx=10)
            return False

        # 
        elif user_input != self.managers_db.keys():
            self.error_user_label['foreground'] = "red"
            self.error_user_label['text'] = "This user does not exist!"
            self.error_user_label.grid(column=1, row=2, sticky=W, padx=10)
            return False


    def check_password(self):
        """
        Checks password attributes
        """
        user_input = self.username.get()
        passw_input = self.password.get()

        try:  # if there is no input and pressed ok
            if passw_input == self.managers_db[user_input]['Password']:
                from _3_main_menu import MainMenu
                self.login_page.destroy()
                MainMenu(self.window)  # builds the new main menu screen
                return True
            else:
                self.error_pass_label['foreground'] = 'red'
                self.error_pass_label['text'] = "Invalid Password!"  # Used set() instead of '=' because of Strvar()
                self.error_pass_label.grid(column=1, row=4, sticky=W, padx=10)
                return False
        except:
            return False


    def back_to_welcome_screen(self):
        from _0_welcome import WelcomePage
        WelcomePage(self.window)
        self.login_page.destroy()
