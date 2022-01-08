from tkinter import *
from tkinter import ttk


class MemberEntry:
    """
    Builds Member Entry Menu
    """
    def __init__(self, window):
        self.window = window

        # Creates frame to be built on the window
        self.member_entry_page = ttk.Frame(window)
        self.member_entry_page.pack(fill='both', expand=True)

        # Configures grid such that there is a center column
        self.member_entry_page.columnconfigure(0, weight=2)
        self.member_entry_page.columnconfigure(1, weight=1)
        self.member_entry_page.columnconfigure(2, weight=2)

        self.window.minsize(350, 250)  # Defines minimum dimensions
        self.window.maxsize(400, 300)  # Defines maximum dimensions

        # Only a few widgets are built within a single function
        self.create_widgets()


    def create_widgets(self):
        # Builds title
        title_label = ttk.Label(self.member_entry_page, text="Member Entry", font=('Arial', 16, 'bold'))
        title_label.grid(column=1, pady=20)

        # Builds buttons
        edit_members_button = ttk.Button(self.member_entry_page, text='Show Member', command=self.go_to_show_members)
        edit_members_button.grid(column=1, padx=10, pady=10, ipady=5, sticky=(N, S, E, W))

        show_members_button = ttk.Button(self.member_entry_page, text='Edit Members', command=self.go_to_edit_members)
        show_members_button.grid(column=1, padx=10, pady=10, ipady=5, sticky=(N, S, E, W))

        back = ttk.Button(self.member_entry_page, text='Back to Master Entry', command=self.back_to_master_entry)
        back.grid(column=1, padx=10, pady=30, ipady=5, sticky=(N, S, E, W))


    def back_to_master_entry(self):
        """
        Opens master entry frame and destroys current page
        """
        from _5_master_entry import MasterEntry
        self.member_entry_page.destroy()
        MasterEntry(self.window)


    def go_to_edit_members(self):
        """
        Opens edit members page and destroys current page
        """
        from _5ab_edit_members import EditMembers
        EditMembers()


    def go_to_show_members(self):
        """
        Opens show members page and destroys current page
        """
        from _5aa_c_show_members import ShowMembers
        ShowMembers()
