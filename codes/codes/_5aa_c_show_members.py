from tkinter import *
from tkinter import ttk
from tkinter.constants import W, VERTICAL, END

from json_funcs import A1_mem_data_func as js


class ShowMembers:
    """
    This class opens a new page to show members of the database
    """
    # Class variable: keeps track of how many instances of this class have been called. 
    # 0 -> False, 1 -> True
    _instance = False

    def __init__(self):
        # Executes constructor only if no other instances have been called
        if ShowMembers._instance == False:
            # Builds new window
            page = Tk()
            page.title("Show Members Page")
            page.minsize(900, 600)
            page.minsize(950, 650)

            self.page = page

            # Defines style of new window
            style = ttk.Style(self.page)  # add style to treeview
            style.theme_use("clam")

            # Changes value of instance to one, which means an instance has been executed
            ShowMembers._instance = True
            # Calls function on_closing when window is closed
            self.page.protocol("WM_DELETE_WINDOW", self.on_closing)

            # Builds frame of widgets on page
            self.search_members_frame = ttk.Frame(self.page)
            self.search_members_frame.pack(fill="both", expand=True)

            # Builds all widgets
            self.build_tree()
            self.build_search_widgets()

            page.mainloop()

    def build_tree(self):
        """
        This function builds the treeview and its scrollbar
        """
        # Builds frame for treeview
        tree_frame = ttk.Frame(self.search_members_frame)

        # Column configuration
        self.search_members_frame.columnconfigure(0, weight=10)
        self.search_members_frame.columnconfigure(1, weight=1)

        # Create Treeview
        self.tree = ttk.Treeview(tree_frame)

        # Define our columns
        self.tree['columns'] = ('ID', 'First Name', 'Last Name', 'Phone', 'Address', 'E-mail', 'Username')

        # Only shows headings and hides first empty column
        self.tree['show'] = 'headings'

        # Displays headers
        for column in self.tree["columns"]:  # cycles through headers and uses internal identifiers as names for columns (text = column)
            self.tree.heading(column, text=column, anchor=W)

        # Define columns attributes
        for column in self.tree["columns"]:
            self.tree.column(column, width=120, minwidth=120, anchor=W)

        # Shows data in tree
        members_data = js.get_members_data()

        # Displays each members booking data in tree
        for key, value in members_data.items():  # values are themselves dictionaries
            self.tree.insert("", "end", iid=key, values=(  # most important line
                value['id'],
                value['First Name'],
                value['Last Name'],
                value['Phone'],
                value['Address'],
                value['E-mail'],
                key  # fetches username key
                )
            )

        # Creates object of scrollbar
        s = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree['yscrollcommand'] = s.set

        # Grids the tree and scrollbar
        self.tree.grid(row=0, column=0)
        s.grid(row=0, column=1, sticky=NSEW)

        # Packs the frame
        tree_frame.grid(row=0, column=0, pady=20)


    def build_search_widgets(self):
        """
        Builds label, entry and button for searching in database
        """
        # Create and grids widgets directly
        search_frame = ttk.Frame(self.search_members_frame)
        search_frame.grid(row=1, column=0, pady=20, padx=5)
        search_label = ttk.Label(search_frame, text='Search Username')
        search_label.grid(row=0, column=0, pady=5, padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.grid(row=0, column=1, pady=5, padx=5)

        search_record = ttk.Button(search_frame, text='Search', width=15, command=self.search_by_username)
        search_record.grid(row=0, column=2, pady=5, padx=10)

        # Creates a frame which will show the report of the search
        self.result_screen = ttk.Frame(self.search_members_frame)


    def reset_entries(self):
        """
        Resets the content of entry
        """
        self.search_entry.delete(0, END)


    def search_by_username(self):
        """
        This function searches for a username in the database
        """
        # Flag turns True if username is found
        flag = False

        # Gets member data dictionary
        members_data = js.get_members_data()
        # Gets username which is to be searched for
        username = self.search_entry.get()
        for key in list(members_data.keys()):
            # Checks if username is correct (flag is true and break)
            if username == key:

                self.search_entry.delete(0, END)
                self.search_result(username, members_data[key]['id'],
                                   members_data[key]['First Name'],
                                   members_data[key]['Last Name'],
                                   members_data[key]['Phone'],
                                   members_data[key]['Address'],
                                   members_data[key]['E-mail'],
                                   )
                # User is found and flag is True
                flag = True
                break
            elif username != key:
                flag = False
                self.search_entry.delete(0, END)

        if not flag:  # checks if username is not in usernames(if flag is false)
            error_msg = Label(self.search_members_frame, text="Username Is Not Valid", fg='red')  # show error message
            error_msg.grid(row=2, column=0, sticky=(E, W))
            error_msg.after(3000, error_msg.destroy)
            

    def search_result(self, username, id, first_name, last_name, phone, address, email):
        """
        Displays member report upon search
        """
        self.result_screen.destroy()
        self.result_screen = ttk.Frame(self.search_members_frame)
        self.result_screen.grid(row=2, column=0)
        ttk.Label(self.result_screen, text='Username : ' + username)
        ttk.Label(self.result_screen, text='ID : ' + str(id))
        ttk.Label(self.result_screen, text='Full Name : ' + first_name + ' ' + last_name)
        ttk.Label(self.result_screen, text='Phone Number : ' + phone)
        ttk.Label(self.result_screen, text='Address : ' + address)
        ttk.Label(self.result_screen, text='E-mail : ' + email)

        for child in self.result_screen.winfo_children():  # adds padding all previous children
            child.grid(padx=10, pady=10, sticky=W)
        self.tree.selection_set(
            username)  # a function in tree manages you to focus on searched item (by username(key=iid))


    def on_closing(self):
        """
        Called upon closing of the window
        """
        ShowMembers._instance = False
        self.page.destroy()