from tkinter import *

from tkinter import ttk


class MasterEntry:
    """
    Builds Master Entry Menu
    """
    def __init__(self, window):
        self.window = window

        # Creates frame to be built on the window
        self.master_entry_page = ttk.Frame(window)
        self.master_entry_page.pack(fill='both', expand=True)

        # Configures grid such that there is a center column
        self.master_entry_page.columnconfigure(0, weight=2)
        self.master_entry_page.columnconfigure(1, weight=1)
        self.master_entry_page.columnconfigure(2, weight=2)

        self.window.minsize(350, 250)  # Defines minimum dimensions
        self.window.maxsize(400, 300)  # Defines maximum dimensions

        # Only a few widgets are built within a single function
        self.create_widgets()


    def create_widgets(self):
        # Builds title
        title_label = ttk.Label(self.master_entry_page, text="Master Entry", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=1, pady=20)

        # Builds buttons
        member_entry_button = ttk.Button(self.master_entry_page, text='Member Entry', command=self.go_to_member_entry)
        member_entry_button.grid(column=1, pady=10, ipady=5, sticky=(E, W))

        computer_entry_button = ttk.Button(self.master_entry_page, text='Computer Entry', command=self.go_to_computer_entry)
        computer_entry_button.grid(column=1, pady=10, ipady=5, sticky=(E, W))

        back_button = ttk.Button(self.master_entry_page, text='Back to Main Menu', command=self.back_to_main_menu)
        back_button.grid(column=1, pady=30, ipady=5, sticky=(E, W))


    def back_to_main_menu(self):
        """
        Opens main menu frame and destroys current page
        """
        from _3_main_menu import MainMenu  # To avoid circular import
        MainMenu(self.window)
        self.master_entry_page.destroy()


    def go_to_member_entry(self):
        """
        Opens member entry frame and destroys current page
        """
        from _5a_member_entry import MemberEntry    # To avoid circular import
        MemberEntry(self.window)
        self.master_entry_page.destroy()


    def go_to_computer_entry(self):
        """
        Opens computer entry frame and destroys current page
        """
        from _5b_computer_entry import ComputerEntry    # To avoid circular import
        ComputerEntry(self.window)
        self.master_entry_page.destroy()
