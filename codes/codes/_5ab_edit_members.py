from tkinter import *
from tkinter import ttk
from tkinter.constants import W, VERTICAL, END

import _5aba_check_entries_functions as check
from json_funcs import A1_mem_data_func as js


class EditMembers:
    """
    This class builds the edit members page.
    """
    # Class variable: keeps track of how many instances of this class have been called. 
    # 0 -> False, 1 -> True
    _instance = False

    def __init__(self):
        # Executes constructor only if no other instances have been called
        if EditMembers._instance == False:
            # Initializes an ID for members
            self.id = 1

            # Builds new window
            page = Tk()  # Creates instance of the whole app
            page.title("Edit Members Page")
            page.minsize(900, 700)
            page.maxsize(950, 750)

            self.page = page

            # Defines style of page
            style = ttk.Style(self.page)  # add style to treeview
            style.theme_use("clam")

            # Changes value of instance to one, which means an instance has been executed
            EditMembers._instance = True
            # Calls function on_closing when window is closed
            self.page.protocol("WM_DELETE_WINDOW", self.on_closing)

            # Builds frame of widgets on page
            self.edit_members_frame = ttk.Frame(self.page)
            self.edit_members_frame.pack(fill="both", expand=True)

            # Builds all widgets
            self.build_tree()
            self.build_entries()
            self.build_buttons()

            page.mainloop()


    def find_startID(self):
        """
        This function finds the last ID used for members and defines the starting ID
        """
        member_data = js.get_members_data()
        if member_data.items():
            for value in member_data.values():
                self.id = value['id']
        else:
            self.id = 1000  # Arbitrary value

        return self.id


    def build_tree(self):
        """
        This function builds the treeview
        """
        # Treeview frame
        tree_frame = ttk.Frame(self.edit_members_frame)

        # Column configuration
        self.edit_members_frame.columnconfigure(0, weight=10)
        self.edit_members_frame.columnconfigure(1, weight=1)

        # Create Treeview
        self.tree = ttk.Treeview(tree_frame)

        # Define our columns
        self.tree['columns'] = ('ID', 'First Name', 'Last Name', 'Phone', 'Address', 'E-mail', 'Username')

        # Only shows headings and hides first empty column
        self.tree['show'] = 'headings'

        # Displays headers
        for column in self.tree[
            "columns"]:  # cycles through headers and uses internal identifiers as names for columns (text = column)
            self.tree.heading(column, text=column, anchor=W)

        # Define columns attributes
        for column in self.tree["columns"]:
            self.tree.column(column, width=120, minwidth=120, anchor=W)

        # Shows data in tree
        members_data = js.get_members_data()

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

        # Binding event of double click with triggering sekect_records function
        self.tree.bind("<Double-1>", self.select_record)

        # Creates scrollbar object
        s = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree['yscrollcommand'] = s.set

        # Grids the tree and scrollbar
        self.tree.grid(row=0, column=0)
        s.grid(row=0, column=1, sticky=NSEW)

        # Packs the frame
        tree_frame.pack(pady=20)


    def build_entries(self):
        """
        This function builds the 6 labels and entries
        """
        # Creates a frame for the buttons
        labels_entries_frame = ttk.Frame(self.edit_members_frame)

        # Create labels of entry boxes
        l1 = ttk.Label(labels_entries_frame, text='First Name')
        l2 = ttk.Label(labels_entries_frame, text='Last Name')
        l3 = ttk.Label(labels_entries_frame, text='Phone')
        l4 = ttk.Label(labels_entries_frame, text='Address')
        l5 = ttk.Label(labels_entries_frame, text='E-mail')
        l6 = ttk.Label(labels_entries_frame, text='Username')

        # Places labels on screen
        col = 0
        for label in [l1, l2, l3, l4, l5, l6]:
            label.grid(row=0, column=col, padx=5, sticky=W)
            col += 1

        # Create entry boxes
        self.E1 = ttk.Entry(labels_entries_frame)
        self.E2 = ttk.Entry(labels_entries_frame)
        self.E3 = ttk.Entry(labels_entries_frame)
        self.E4 = ttk.Entry(labels_entries_frame)
        self.E5 = ttk.Entry(labels_entries_frame)
        self.E6 = ttk.Entry(labels_entries_frame)

        self.entries = [self.E1, self.E2, self.E3, self.E4, self.E5, self.E6]

        # Places entry boxes on screen
        col = 0
        for entry in self.entries:
            entry.grid(row=1, column=col, padx=5, pady=5)
            col += 1

        # Packs the frame
        labels_entries_frame.pack(pady=20)


    def build_buttons(self):
        """
        This function builds the buttons
        """
        add_record = ttk.Button(self.edit_members_frame, text='Add Record', width=15, command=self.add_record)
        add_record.pack(pady=15)

        update_record = ttk.Button(self.edit_members_frame, text='Update Record', width=15, command=self.update_selected)
        update_record.pack(pady=15)

        remove_selected = ttk.Button(self.edit_members_frame, text='Remove Record', width=15, command=self.remove_selected)
        remove_selected.pack(pady=15)


    def add_record(self):
        """
        This function adds member in database and tree
        """
        # Adds one to the last found member ID
        id = self.find_startID() + 1

        # Calls check function and passes all entries to it
        if check.check_entries(self.edit_members_frame, self.E1.get(), self.E2.get(), self.E3.get(), self.E4.get(), self.E5.get(), self.E6.get()) is True:  # if test cases is true
            # Try and except to check if username is already taken
            try:
                self.tree.insert("", index="end", iid=self.E6.get(), values=(
                    id,  # start from last index in the list
                    self.E1.get(),
                    self.E2.get(),
                    self.E3.get(),
                    self.E4.get(),
                    self.E5.get(),
                    self.E6.get()
                    )
                )
                # update record
                js.add_to_members_database(
                    id,
                    self.E1.get(),
                    self.E2.get(),
                    self.E3.get(),
                    self.E4.get(),
                    self.E5.get(),
                    self.E6.get()
                )

                self.reset_entries()  # clear the boxes after insertion

            except:
                mess_label = ttk.Label(self.edit_members_frame, text="Your username is already taken", foreground='red')
                mess_label.pack(pady=5)
                mess_label.after(3000, mess_label.destroy)


    def remove_selected(self):
        """
        Remove selected item from database and treeview
        """
        iid_selected = self.tree.selection()
        for iid in iid_selected:
            self.tree.delete(iid)  # deletes from ui by key
            js.delete_from_member_database(iid)  # deletes from json


    def select_record(self, event=None):
        """
        This function selects element in treeview
        """
        selected = self.tree.selection()
        if selected != ():
            # Deletes entries before inserting selected item
            self.reset_entries()
            # Return the selected row's index
            focused = self.tree.focus()

            # Returns tuple with values in row
            values = self.tree.item(focused, 'values')

            ind = 1
            for entry in self.entries:  # loops through selected row
                entry.insert(0, values[ind])
                ind += 1


    def update_selected(self):
        """
        This function updates the content of the treeview and database
        """
        members_data = js.get_members_data()
        selected = self.tree.selection()  # save selected data to (selected) variable
        if check.check_entries(self.edit_members_frame, self.E1.get(), self.E2.get(), self.E3.get(), self.E4.get(), self.E5.get(),
                               self.E6.get()) is True:  # checks test cases
            if self.E6.get() == selected[
                0]:  # makes sure that username is not changed(it can not be changed because it is a key )
                # save new data into our tree
                focused = self.tree.focus()
                self.tree.item(focused, values=(
                    members_data[selected[0]]['id'],
                    self.E1.get(),
                    self.E2.get(),
                    self.E3.get(),
                    self.E4.get(),
                    self.E5.get(),
                    selected[0]
                )
                               )
                # saves the list to our database (to be saved even after pausing the program
                js.update_members_data_base(selected[0], members_data[selected[0]]['id'],
                                            self.E1.get(),
                                            self.E2.get(),
                                            self.E3.get(),
                                            self.E4.get(),
                                            self.E5.get(),
                                            )

                self.reset_entries()  # reset entries

            elif self.E6.get() != selected[0]:  # checks if username is changed
                msg_label = ttk.Label(self.edit_members_frame,
                                      text="You can not change your username because it is a primary key",
                                      foreground='red')
                msg_label.pack(pady=5)
                msg_label.after(3000, msg_label.destroy)

    def reset_entries(self):
        """
        This function deletes the entries content
        """
        for entry in self.entries:
            entry.delete(0, END)

    def on_closing(self):
        """
        This function redefines protocol of button upon closing
        """
        EditMembers._instance = False
        self.page.destroy()
        