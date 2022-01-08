from datetime import datetime
from tkinter import *
from tkinter import ttk

from json_funcs import A1_mem_data_func as A1
from json_funcs import A3_mem_book_func as js
from json_funcs import A4_mem_memb_func as A4


class MemberBooking:
    """
    This class opens a new page for the manager to enter booking details for members
    """
    # Class variable: keeps track of how many instances of this class have been called. 
    # 0 -> False, 1 -> True
    _instance = False

    def __init__(self):
        
        # Executes constructor only if no other instances have been called
        if MemberBooking._instance == False:
            # Builds new window
            page = Tk()
            page.title("Members Booking Page")
            page.minsize(725, 350)
            page.maxsize(775, 400)
            self.page = page

            # Defines style of new window
            style = ttk.Style(self.page)  # add style to treeview
            style.theme_use("clam")

            # Changes value of instance to one, which means an instance has been executed
            MemberBooking._instance = True
            # Calls function on_closing when window is closed
            self.page.protocol("WM_DELETE_WINDOW", self.on_closing)

            # Builds frame of widgets on page
            self.member_booking_frame = ttk.Frame(self.page)
            self.member_booking_frame.pack(fill='both', expand=True)

            # Defines column attributes of grid
            self.member_booking_frame.grid_columnconfigure(0, weight=4)
            self.member_booking_frame.grid_columnconfigure(1, weight=1)

            # Initializes members_book database with members_data
            for member in A1.get_members_data():
                if member not in js.get_members_booking().keys():
                    js.reset_member_booking(member)   #sets/adds new member in booking
                    A4.deactivate_membership(member)  #sets new member in renewal
            
            # If a member has been removed from database, it can no longer remain in members book
            for member in js.get_members_booking():
                if member[:5] != "Guest" and member not in A1.get_members_data():
                    js.remove_guest_book(member)
            
            # Builds all widgets
            self.find_startID()
            self.build_tree()
            self.build_buttons()
            self.build_label()

            # Binds treeview with the even of Button Release
            self.tree.bind("<ButtonRelease-1>", self.scan_selection)

            page.mainloop()


    def build_tree(self):
        """
        This function builds the treeview and its scrollbar
        """
        # Treeview frame
        tree_frame = ttk.Frame(self.member_booking_frame)

        # Create Treeview
        self.tree = ttk.Treeview(tree_frame)

        # Define internal identifiers of columns
        self.tree['columns'] = ('Username', 'Status', 'Login Time', 'Logout Time')

        # Only shows headings and hides first empty root column
        self.tree['show'] = 'headings'

        # Displays headers
        for column in self.tree[
            "columns"]:  # cycles through headers and uses internal identifiers as names for columns (text = column)
            self.tree.heading(column, text=column, anchor=CENTER)

        # Define columns attributes
        for column in self.tree["columns"]:
            self.tree.column(column, width=150, minwidth=120, anchor=CENTER)

        # Fetches data from members_book
        members_book = js.get_members_booking()

        # Displays each members booking data in tree
        for key, value in members_book.items():  # values are themselves dictionaries
            self.tree.insert("", "end", iid=key, values=(  # most important line
                key,
                value['Status'],
                value['Login Time'],
                value['Logout Time'],
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


    def build_buttons(self):
        """
        Builds buttons in a frame and initializes their status to disabled.
        """
        button_column = ttk.Frame(self.member_booking_frame)

        self.start_session_button = ttk.Button(button_column, text="Start Session", state="disabled", command=self.start_session)
        self.end_session_button = ttk.Button(button_column, text="End Session", state="disabled", command=self.end_session)
        self.take_charges_button = ttk.Button(button_column, text="Take Charges", state="disabled", command=self.take_charges)
        guest_button = ttk.Button(self.member_booking_frame, text="Add", command=self.add_guest)

        self.start_session_button.pack(padx=10, pady=20)
        self.end_session_button.pack(padx=10, pady=20)
        self.take_charges_button.pack(padx=10, pady=20)

        button_column.grid(row=0, column=1, sticky=(N, S, E, W))
        guest_button.grid(row=2, column=0, padx=10, sticky=W)


    def build_label(self):
        """
        Builds static labels
        """
        self.guest_label = ttk.Label(self.member_booking_frame, text="Add Guest User: ")
        self.charge_label = ttk.Label(self.member_booking_frame)

        self.guest_label.grid(row=1, column=0, padx=10, pady=(25, 10), sticky=W)


    def find_startID(self):
        """
        This function finds the starting guest ID by looking in members_book
        """
        member_data = js.get_members_booking()

        # Initialized value
        guest = "Guest1000"

        for guest_id in member_data.keys():
            if guest_id[:5] == "Guest":
                guest = guest_id
                guest = guest[0:5] + str(int(guest[5:9]) + 1)

        return guest


    def add_guest(self):
        """
        This function adds guest when button is clicked
        """
        # Saves guest name in guest variable
        guest = self.find_startID()

        # Adds guest username in members_book database
        js.add_guest_booking(guest)

        # Fetches members_book
        members_book = js.get_members_booking()

        # Inserts guest details in treeview
        self.tree.insert("", "end", iid=guest, values=(
            guest,
            members_book[guest]['Status'],
            members_book[guest]['Login Time'],
            members_book[guest]['Logout Time']
            )
        )

        # Sets focuc on new guest in treeview
        self.tree.focus(guest)
        self.tree.selection_set(guest)

        # Automatically starts a new session for guest user
        self.start_session()


    def start_session(self):
        """
        This function starts a new session and fetches start time
        """
        # Scans user selection
        selected = self.tree.focus()

        # Fetches current time at selection
        self.start_time = datetime.now()
        # Casts start_time to string type with special format
        formatted_start_time = self.start_time.strftime("%H:%M:%S")

        # Updates member book with Login time
        js.start_update(selected, formatted_start_time)

        # Modifies value of item in tree
        self.tree.item(selected, values=(selected, "Active", formatted_start_time))

        # Redefines state of buttons
        self.state_buttons(selected)


    def end_session(self):
        """
        This function closes session and fetches end time 
        """
        # Checks selected item in tree
        selected = self.tree.focus()

        # Feteches current time at logout
        self.end_time = datetime.now()
        # Formats logout time
        formatted_end_time = self.end_time.strftime("%H:%M:%S")

        # Fetches Login time
        start_time = js.get_members_booking()[selected]["Login Time"]

        # Updates member book upon login
        js.end_update(selected, start_time, self.end_time.strftime("%H:%M:%S"))

        # Updates treeview
        self.tree.item(selected, values=(selected, "Ended", start_time, formatted_end_time))

        # Updates state of buttons
        self.state_buttons(selected)


    def take_charges(self):
        """
        This function takes the charges and displays it to the user
        """
        # Checks selected item and returns iid (internal identifier)
        selected = self.tree.focus()

        # Fetches login and logout times and reformates them to datetime objects
        start_time = datetime.strptime(js.get_members_booking()[selected]['Login Time'], "%H:%M:%S")
        end_time = datetime.strptime(js.get_members_booking()[selected]["Logout Time"], "%H:%M:%S")
        time_spent = (end_time - start_time).total_seconds()  # Calculates the time spent in seconds

        # Fetches information of membership to know how much the charge should be
        members_membership = A4.get_membership()

        # If user is a not a guest and has an active membership 
        if selected[:5] != "Guest" and members_membership[selected]["Status"] == "Running":
            charge = 0.02
        else:
            charge = 0.1

        # Calculates total price
        price = charge * time_spent

        # Deletes times from json book
        js.reset_member_booking(selected)
        # Updates values in treeview
        self.tree.item(selected, values=(selected, "Inactive", "", ""))  # deletes from ui

        # Displays label with charge
        self.charge_label['text'] = "Please proceed to pay {:.2f}$, charged at {}$ per minute".format(price, charge * 60)
        self.charge_label.grid(row=1, column=0, pady=(25, 10))

        # If it is a guest, deletes it from database and tree
        if selected[0:5] == "Guest":
            self.tree.delete(selected)  # deletes from ui
            js.remove_guest_book(selected)  #deletes from database
            
            # Disables buttons state
            self.start_session_button["state"] = "disabled"
            self.end_session_button["state"] = "disabled"
            self.take_charges_button["state"] = "disabled"
        else:
            # Updates buttons state 
            self.state_buttons(selected)


    def scan_selection(self, event=None):   # Passed event from bind function. Not used so made None by default
        """
        Important function which scans selection in treeview
        """
        selected = self.tree.focus()

        # Each time the selection is changed, the label is reset
        self.charge_label.destroy()
        self.build_label()

        # Each time the selection is changed, the buttons state is changed
        self.state_buttons(selected)


    def state_buttons(self, selected):
        """
        Important function which updates the state of the buttons according
        to the selection in the treeview.
        """
        # Fetches status of selected member
        status = js.get_members_booking()[selected]["Status"]

        if status == "Inactive" and selected !=  "":
            self.start_session_button["state"] = "normal"
            self.end_session_button["state"] = "disabled"
            self.take_charges_button["state"] = "disabled"

        elif status == "Active" and selected !=  "":
            self.start_session_button["state"] = "disabled"
            self.end_session_button["state"] = "normal"
            self.take_charges_button["state"] = "disabled"

        elif status == "Ended" and selected !=  "":
            self.start_session_button["state"] = "disabled"
            self.end_session_button["state"] = "disabled"
            self.take_charges_button["state"] = "normal"


    def on_closing(self):
        """
        Called upon closing of the window
        """
        # When window is closed, the class variable _instance is reset to False
        MemberBooking._instance = False
        self.page.destroy()