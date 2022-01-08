from tkinter import *
from tkinter import ttk


class CafeManagement:
    def __init__(self, window):
        self.window = window
        style = ttk.Style(self.window)  # add style to treeview
        style.theme_use("clam")
        self.cafe_management_page = ttk.Frame(window)
        self.cafe_management_page.pack(expand=True, fill='both')
        self.cafe_management_page.columnconfigure(0, weight=2)
        self.cafe_management_page.columnconfigure(1, weight=1)
        self.cafe_management_page.columnconfigure(2, weight=2)
        self.create_widgets()


    def create_widgets(self):
        # Page title
        title_label = ttk.Label(self.cafe_management_page, text="Cafe Management", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=1, pady=20)

        booking = ttk.Button(self.cafe_management_page, text='Booking', command=self.go_to_booking, width=20)
        booking.grid(column=1, pady=10, ipady=5)

        renewal = ttk.Button(self.cafe_management_page, text='Renewal',
                             command=self.go_to_renewal, width=20)  # command=lambda: self.go_to_charges()
        renewal.grid(column=1, pady=10, ipady=5)

        back = ttk.Button(self.cafe_management_page, text='Back to Main Menu', command=self.back_to_main_menu, width=20)
        back.grid(column=1, pady=30, ipady=5)


    def go_to_booking(self):
        from _4a_member_booking import MemberBooking
        MemberBooking()


    def go_to_renewal(self):
        from _4b_renewal import Renewal
        Renewal()


    def back_to_main_menu(self):
        from _3_main_menu import MainMenu  # To avoid circular import (very important)
        self.cafe_management_page.destroy()
        MainMenu(self.window)
