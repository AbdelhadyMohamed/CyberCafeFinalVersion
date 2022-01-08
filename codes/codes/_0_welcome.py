from tkinter import *
from tkinter import ttk


class WelcomePage:
    """
    Builds welcome page on window
    """
    def __init__(self, window):
        self.window = window

        # Defines dimensions of window
        self.window.minsize(400, 250)
        self.window.maxsize(450, 300)

        # Creates a frame to be displayed on the root window
        self.welcome_frame = ttk.Frame(self.window)

        # Organizes frame in a grid layout where each widget belongs in a cell (row, column)
        welcome_label = ttk.Label(self.welcome_frame, text="Welcome to the Cybercafe Management System", font=('Arial', 12, 'bold'))
        welcome_label.grid(row=0, column=2, pady=20, padx=15)

        signup_button = ttk.Button(self.welcome_frame, text="Sign Up", command=self.go_to_signup)
        signup_button.grid(row=1, column=2, pady=20, ipadx=15, ipady=5)

        login_button = ttk.Button(self.welcome_frame, text="Log In", command=self.go_to_login)
        login_button.grid(row=2, column=2, pady=20, ipadx=15, ipady=5)

        # Displays the frame on the window
        self.welcome_frame.pack(fill='both', expand=True)


    def go_to_signup(self):
        """
        Opens Sign Up page when clicking on Sign Up button
        """
        from _1_signup import Signup
        self.welcome_frame.destroy()
        Signup(self.window)


    def go_to_login(self):
        """
        Opens Log In page when clicking on Log In button
        """
        from _2_login import Login     # Local import to avoid circular import error
        self.welcome_frame.destroy()
        Login(self.window)
