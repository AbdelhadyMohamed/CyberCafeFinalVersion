from tkinter import *
from tkinter import ttk


class MainMenu:

    def __init__(self, window):

        self.window = window
        self.window.minsize(350, 250)  # Defines minimum dimensions
        self.window.maxsize(400, 300)  # Defines maximum dimensions

        self.main_menu_page = ttk.Frame(self.window)
        self.main_menu_page.pack(fill='both', expand=True)

        self.main_menu_page.columnconfigure(0, weight=2)
        self.main_menu_page.columnconfigure(1, weight=1)
        self.main_menu_page.columnconfigure(2, weight=2)

        self.create_widgets()

    def create_widgets(self):
        
        title_label = ttk.Label(self.main_menu_page, text="Main Menu", font=('Arial', 16, 'bold'))
        title_label.grid(column=1, pady=20)

        master_entry_button = ttk.Button(self.main_menu_page, text='Master Entry',
                                         command=self.go_to_masterentry_screen)
        master_entry_button.grid(column=1, pady=10, ipady=5, sticky=(E, W))  # in the middle of the screen

        cafe_manag_button = ttk.Button(self.main_menu_page, text='Cafe Management',
                                       command=self.go_to_cafemanagement_screen)
        cafe_manag_button.grid(column=1, pady=10, ipady=5, sticky=(E, W))

        logout_button = ttk.Button(self.main_menu_page, text='Log Out', command=self.go_to_login_screen)
        logout_button.grid(column=1, pady=30, ipady=5, sticky=(E, W))


    def go_to_masterentry_screen(self):
        from _5_master_entry import MasterEntry
        MasterEntry(self.window)
        self.main_menu_page.destroy()

    def go_to_cafemanagement_screen(self):
        from _4_cafe_management import CafeManagement  # To avoid circular import (very important)
        self.main_menu_page.destroy()
        CafeManagement(self.window)

    def go_to_login_screen(self):
        from _2_login import Login
        Login(self.window)
        self.main_menu_page.destroy()
