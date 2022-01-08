from datetime import *
from tkinter import *
from tkinter import ttk

from dateutil.relativedelta import *

from json_funcs import A1_mem_data_func as A1
from json_funcs import A4_mem_memb_func as js


class Renewal:
    """
    This class opens a new page for the manager to enter renewal details for members
    """
    # Class variable: keeps track of how many instances of this class have been called. 
    # 0 -> False, 1 -> True
    _instance = False

    def __init__(self):
        # Executes constructor only if no other instances have been called
        if Renewal._instance == False:
            # Builds new window
            page = Tk()
            page.title("Renew Membership Page")
            page.minsize(925, 350)
            page.maxsize(975, 400)
            self.page = page

            # Defines style of new window
            style = ttk.Style(self.page)
            style.theme_use("clam")

            # Changes value of instance to one, which means an instance has been executed
            Renewal._instance = True
            # Calls function on_closing when window is closed
            self.page.protocol("WM_DELETE_WINDOW", self.on_closing)

            # Builds frame of widgets on page
            self.renewal_frame = ttk.Frame(self.page)
            self.renewal_frame.pack(fill='both', expand=True)

            # Defines column attributes of grid
            self.renewal_frame.grid_columnconfigure(0, weight=4)
            self.renewal_frame.grid_columnconfigure(1, weight=1)

            # Initializes members_membership database with members_data
            for key in A1.get_members_data():
                if key not in js.get_membership().keys():
                    js.deactivate_membership(key)

            # If a member has been removed from database, it can no longer remain in members_membership
            for member in js.get_membership():
                if member not in A1.get_members_data():
                    js.remove_membership(member)

            # Builds all widgets
            self.build_tree()
            self.build_buttons()
            self.build_label()
            self.check_membership()

            # Binds treeview with the even of Button Release
            self.tree.bind("<ButtonRelease-1>", self.scan_selection)

            page.mainloop()

    def build_tree(self):
        """
        This function builds the treeview and its scrollbar
        """
        # Treeview frame
        tree_frame = ttk.Frame(self.renewal_frame)

        # Create Treeview
        self.tree = ttk.Treeview(tree_frame)

        # Define our columns
        self.tree['columns'] = ('Username', 'Status', 'Start Date', 'End Date', 'Plan Type')

        # Only shows headings and hides first empty column
        self.tree['show'] = 'headings'

        # Displays headers
        for column in self.tree[
            "columns"]:  # cycles through headers and uses internal identifiers as names for columns (text = column)
            self.tree.heading(column, text=column, anchor=CENTER)

        # Define columns attributes
        for column in self.tree["columns"]:
            self.tree.column(column, width=150, minwidth=120, anchor=CENTER)

        # Shows data in tree
        members_book = js.get_membership()

        # Displays each members renewal data in tree
        for key, value in members_book.items():  # values are themselves dictionaries
            self.tree.insert("", "end", iid=key, values=(  # most important line
                key,
                value['Status'],
                value['Start Date'],
                value['End Date'],
                value['Plan Type']
                )
            )

        # Creates instance of scrollbar object
        s = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree['yscrollcommand'] = s.set

        # Grids the tree and scrollbar
        self.tree.grid(row=0, column=0)
        s.grid(row=0, column=1, sticky=(N, S, E, W))

        # Grids the frame
        tree_frame.grid(row=0, column=0, sticky=(N, S, E, W))


    def build_label(self):
        """
        Builds label of confirmation message
        """
        self.confirm_label = ttk.Label(self.renewal_frame)

    def build_buttons(self):
        """
        Builds buttons in a frame and initializes their status to disabled.
        """
        button_column = ttk.Frame(self.renewal_frame)

        self.renew_one_week_button = ttk.Button(button_column, text="Renew 1-Week", state="disabled", command=self.renew_one_week)
        self.renew_one_month_button = ttk.Button(button_column, text="Renew 1-Month", state="disabled", command=self.renew_one_month)
        self.renew_one_year_button = ttk.Button(button_column, text="Renew 1-Year", state="disabled", command=self.renew_one_year)

        self.cancel_membership_button = ttk.Button(self.renewal_frame, text="Cancel Subscription", state="disabled", command=self.cancel)

        self.renew_one_week_button.pack(padx=10, pady=20)
        self.renew_one_month_button.pack(padx=10, pady=20)
        self.renew_one_year_button.pack(padx=10, pady=20)

        self.cancel_membership_button.grid(row=1, column=1, padx=10, pady=30)

        button_column.grid(row=0, column=1, sticky=(N, S, E, W))

    def renew_one_week(self):
        """
        Function which executes when the button 1-week is pressed. It renews the membership to one week.
        """
        # Fetches selection
        iid = self.tree.focus()
        
        # Looks for the date of today
        start_date = datetime.today()
        # Adds one week relative to today's date
        end_date = start_date + relativedelta(weeks=+1)

        # Formats the date
        start_date_str = start_date.strftime("%d %b %Y")
        end_date_str = end_date.strftime("%d %b %Y")

        # Activates membership and stores new state in database
        js.activate_membership(iid, start_date_str, end_date_str, "Weekly")

        # Updates treeview
        self.tree.item(iid, values=(iid, "Running", start_date_str, end_date_str, "Weekly"))

        # If the label was grided or packed, it is destroyed before rebuild
        self.confirm_label.destroy()
        self.build_label()

        # Defines message and color of label
        self.confirm_label["text"] = 'Subscription has been successfully renewed.\nIt will expire on ' + end_date_str
        self.confirm_label["foreground"] = 'green'
        self.confirm_label.grid(row=1, column=0)

        # Updates status of button
        self.state_buttons(iid)


    def renew_one_month(self):
        """
        Function which executes when the button 1-month is pressed. It renews the membership to one month.
        """
        iid = self.tree.focus()

        start_date = datetime.today()
        end_date = start_date + relativedelta(months=+1)

        start_date_str = start_date.strftime("%d %b %Y")
        end_date_str = end_date.strftime("%d %b %Y")

        js.activate_membership(iid, start_date_str, end_date_str, "Monthly")

        self.tree.item(iid, values=(iid, "Running", start_date_str, end_date_str, "Monthly"))

        self.confirm_label.destroy()
        self.build_label()

        self.confirm_label["text"] = 'Subscription has been successfully renewed.\nIt will expire on ' + end_date_str
        self.confirm_label["foreground"] = 'green'
        self.confirm_label.grid(row=1, column=0)

        self.state_buttons(iid)


    def renew_one_year(self):
        """
        Function which executes when the button 1-year is pressed. It renews the membership to one year.
        """
        iid = self.tree.focus()

        start_date = datetime.today()
        end_date = start_date + relativedelta(years=+1)

        start_date_str = start_date.strftime("%d %b %Y")
        end_date_str = end_date.strftime("%d %b %Y")

        js.activate_membership(iid, start_date_str, end_date_str, "Yearly")

        self.tree.item(iid, values=(iid, "Running", start_date_str, end_date_str, "Yearly"))

        self.confirm_label.destroy()
        self.build_label()

        self.confirm_label["text"] = 'Subscription has been successfully renewed.\nIt will expire on ' + end_date_str
        self.confirm_label["foreground"] = 'green'
        self.confirm_label.grid(row=1, column=0)

        self.state_buttons(iid)


    def cancel(self):
        """
        Function which executes when the cancel button is pressed. It cancels any membership.
        """
        iid = self.tree.focus()

        # Updates database
        js.deactivate_membership(iid)

        # Fetches start date of membership
        start_date = js.get_membership()[iid]["Start Date"]

        # Updates treeview
        self.tree.item(iid, values=(iid, "Inactive", start_date, "", "Canceled"))

        # If the label was grided or packed, it is destroyed before rebuild
        self.confirm_label.destroy()
        self.build_label()

        # Defines new message and font color to label
        self.confirm_label["text"] = 'Subscription has been cancelled'
        self.confirm_label["foreground"] = 'red'
        self.confirm_label.grid(row=1, column=0)

        # Updates buttons state
        self.state_buttons(iid)


    def check_membership(self):
        """
        Checks if membership is finished or not yet and cancels it automatically.
        """
        # Fetches membership details
        membership = js.get_membership()

        for iid in membership.keys():
            end = membership[iid]['End Date']
            # If end is not null, this means member has an active membership
            if end != '':
                # Converts end from string to datetime object
                end_date = datetime.strptime(end, "%d %b %Y")
                # Fetches today's date
                current_date = datetime.today()

                # Updates membership details in database and treeview
                if current_date >= end_date:
                    membership[iid]["Status"] = "Ended"
                    self.tree.item(iid, values=(iid, "Ended", js.get_membership()[iid]["Start Date"], 
                                                              js.get_membership()[iid]["End Date"],
                                                              js.get_membership()[iid]["Plan Type"]
                                                            )
                                                )


    def scan_selection(self, event=None):   # Passed event from bind function. Not used so made None by default
        """
        Important function which scans selection in treeview
        """
        self.confirm_label.destroy()
        self.build_label()

        selected = self.tree.focus()

        self.state_buttons(selected)


    def state_buttons(self, selected):
        """
        Important function which updates the state of the buttons according
        to the selection in the treeview.
        """
        status = js.get_membership()[selected]["Status"]

        if status == "Running":
            self.renew_one_week_button['state'] = "disabled"
            self.renew_one_month_button['state'] = "disabled"
            self.renew_one_year_button['state'] = "disabled"

            self.cancel_membership_button['state'] = "normal"

        elif status == "Inactive" or status == 'Ended':
            self.renew_one_week_button["state"] = "normal"
            self.renew_one_month_button['state'] = "normal"
            self.renew_one_year_button['state'] = "normal"

            self.cancel_membership_button['state'] = "disabled"


    def on_closing(self):
        """
        Called upon closing of the window
        """
        # When window is closed, the class variable _instance is reset to False
        Renewal._instance = False
        self.page.destroy()