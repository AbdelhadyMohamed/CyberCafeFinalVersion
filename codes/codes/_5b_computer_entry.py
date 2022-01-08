from tkinter import *
from tkinter import ttk


class ComputerEntry:
    def __init__(self, window):
        self.window = window
        self.computer_entry_frame = ttk.Frame(window)
        self.computer_entry_frame.pack(fill="both", expand=True)
        self.window.minsize(350, 250)  # Defines minimum dimensions
        self.window.maxsize(400, 300)  # Defines maximum dimensions

        self.computer_entry_frame.columnconfigure(0, weight=2)
        self.computer_entry_frame.columnconfigure(1, weight=1)
        self.computer_entry_frame.columnconfigure(2, weight=2)

        self.create_widgets()

    def create_widgets(self):
        # Page title
        title_label = ttk.Label(self.computer_entry_frame, text="Computer Entry", font=('Arial', 16, 'bold'))
        title_label.grid(column=1, pady=20)

        search_record_button = ttk.Button(self.computer_entry_frame, text='Show Computers',
                                          command=self.go_to_search_computer)
        search_record_button.grid(column=1, pady=10, sticky=(N, S, E, W), ipady=5)

        show_members_button = ttk.Button(self.computer_entry_frame, text='Edit Computers',
                                         command=self.go_to_edit_computers)
        show_members_button.grid(column=1, pady=10, sticky=(N, S, E, W), ipady=5)

        back = ttk.Button(self.computer_entry_frame, text='Back to Master Entry', command=self.back_to_master_entry)
        back.grid(column=1, sticky=(N, S, E, W), pady=30, ipady=5)

    def back_to_master_entry(self):
        from _5_master_entry import MasterEntry
        self.computer_entry_frame.destroy()
        MasterEntry(self.window)

    def go_to_edit_computers(self):
        from _5bb_edit_computers import EditComputers
        EditComputers()

    def go_to_search_computer(self):
        from _5ba_show_computer import ShowComputers
        ShowComputers()
