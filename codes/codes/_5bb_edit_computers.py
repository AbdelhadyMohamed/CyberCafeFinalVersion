import tkinter as tk
from tkinter import ttk
from tkinter.constants import N, S, E, W, VERTICAL, END

from json_funcs import A2_comp_data_func as js


class EditComputers:
    """
    This class builds the edit computers page.
    """
    # Class variable: keeps track of how many instances of this class have been called. 
    # 0 -> False, 1 -> True
    _instance = False

    def __init__(self):
        # Executes constructor only if no other instances have been called
        if EditComputers._instance == False:
            # Builds new window
            page = tk.Tk()
            page.title("Edit Computers Page")
            page.minsize(500, 650)
            page.maxsize(550, 700)

            self.page = page
            
            # Defines style of page
            style = ttk.Style(self.page)  # add style to treeview
            style.theme_use("clam")

            # Changes value of instance to one, which means an instance has been executed
            EditComputers._instance = True
            # Calls function on_closing when window is closed
            self.page.protocol("WM_DELETE_WINDOW", self.on_closing)

            # Builds frame of widgets on page
            self.edit_computers_frame = ttk.Frame(self.page)
            self.edit_computers_frame.pack(fill="both", expand=True)

            # Builds all widgets
            self.build_tree()
            self.build_entry()
            self.build_buttons()

            page.mainloop()


    def build_tree(self):
        """
        This function builds the treeview
        """
        # Treeview frame
        tree_frame = ttk.Frame(self.edit_computers_frame)

        # Column configuration
        self.edit_computers_frame.columnconfigure(0, weight=10)
        self.edit_computers_frame.columnconfigure(1, weight=1)

        # Create Treeview
        self.tree = ttk.Treeview(tree_frame)

        # Define our columns
        self.tree['columns'] = ('ID', 'Name')

        # Only shows headings and hides first empty column
        self.tree['show'] = 'headings'

        # Displays headers
        for column in self.tree[
            "columns"]:  # cycles through headers and uses internal identifiers as names for columns (text = column)
            self.tree.heading(column, text=column, anchor=W)

        # Define columns attributes
        for column in self.tree["columns"]:
            self.tree.column(column, width=140, minwidth=140, anchor=W)

        # Shows data in tree
        computers_data = js.get_computers_data()

        for key, value in computers_data.items():  # values are themselves dictionaries
            self.tree.insert("", "end", iid=key, values=(
                key, value
                )
            )

        # Creates scrollbar object
        s = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree['yscrollcommand'] = s.set

        # Grids the tree and scrollbar
        self.tree.grid(row=0, column=0)
        s.grid(row=0, column=1, sticky=(N, S, E, W))

        # Packs the frame
        tree_frame.pack(pady=10)

        # Binding events
        self.tree.bind("<Double-1>", self.select_record)


    def build_entry(self):
        """
        This function builds the label and entry of editing
        """
        label_entry_frame = ttk.Frame(self.edit_computers_frame)
        label_entry_frame.pack(pady=(10, 50))
        search_label = ttk.Label(label_entry_frame, text='Computer Name: ')
        search_label.grid(row=0, column=0, pady=5, padx=5)
        self.add_entry = ttk.Entry(label_entry_frame)
        self.add_entry.grid(row=0, column=1, pady=5, padx=5)

    def build_buttons(self):
        """
        This function builds the buttons
        """
        add_record = ttk.Button(self.edit_computers_frame, text='Add Record', width=15, command=self.add_record)
        add_record.pack(pady=20)

        update_record = ttk.Button(self.edit_computers_frame, text='Update Record', width=15,
                                   command=self.update_selected)
        update_record.pack(pady=20)

        remove_selected = ttk.Button(self.edit_computers_frame, text='Remove Selected Records', width=15,
                                     command=self.remove_selected)
        remove_selected.pack(pady=20)

    def add_record(self):  # add a record to members_db list
        """
        This function adds computer in database and tree
        """
        # Finds the last id 
        computers_data = js.get_computers_data()  # dictionary of computer data
        for key in computers_data.keys():
            id = int(key)

        id += 1
        if self.add_entry.get() != '' and self.add_entry.get() not in list(computers_data.values()) and len(self.add_entry.get()) > 8 and self.add_entry.get()[0:8] == "Computer":
            self.tree.insert("", index="end", iid=str(id), values=(
                id,  # start from last index in the list
                self.add_entry.get(),
                )
            )
            # update record
            js.add_to_computer_database(
                id,
                self.add_entry.get(),
            )
            self.reset_entries()  # reset entries after adding new record
        elif self.add_entry.get() == '':  # if no entered computer name
            mess_label = ttk.Label(self.edit_computers_frame, text="Computer Name can not be empty", foreground='red')
            mess_label.pack(pady=5)
            mess_label.after(3000, mess_label.destroy)

        elif len(
                self.add_entry.get()) <= 8:  # if computer name is less or greater than 8 charcaters(8 is very hard to test)
            mess_label3 = ttk.Label(self.edit_computers_frame, text="Computer Name must be at least 9 characters !!",
                                    foreground='red')
            mess_label3.pack(pady=5)
            mess_label3.after(3000, mess_label3.destroy)

        elif self.add_entry.get() in list(computers_data.values()):  # if computer name is already in the list
            mess_label2 = ttk.Label(self.edit_computers_frame, text="Computer Name is already taken", foreground='red')
            mess_label2.pack(pady=5)
            mess_label2.after(3000, mess_label2.destroy)
        
        elif self.add_entry.get() != "Computer":
            mess_label2 = ttk.Label(self.edit_computers_frame, text='Name not starting with "Computer"', foreground='red')
            mess_label2.pack(pady=5)
            mess_label2.after(3000, mess_label2.destroy)


    def reset_entries(self):
        """
        This function deletes the entries content
        """
        self.add_entry.delete(0, END)  # delete add entry


    def remove_selected(self):
        """
        Remove selected item from database and treeview
        """
        iid_selected = self.tree.selection()  # tuple of selected items
        for iid in iid_selected:
            self.tree.delete(iid)  # deletes from ui
            js.delete_from_computer_database(iid)  # deletes from json


    def select_record(self, event=None):
        """
        This function selects element in treeview
        """
        selected = self.tree.selection()
        if selected != ():
            self.reset_entries()  # deletes entries before inserting selected item
            focused = self.tree.focus()  # return the selected row's index

            values = self.tree.item(focused, 'values')  # returns tuple with values in row

            self.add_entry.insert(0, values[1])


    def update_selected(self):
        """
        This function updates the content of the treeview and database
        """
        computers_data = js.get_computers_data()
        if self.add_entry.get() != '' and self.add_entry.get() not in list(
                computers_data.values()) and len(self.add_entry.get()) > 8 and self.add_entry.get()[0:8] == "Computer":
            selected = self.tree.selection()[0]  # save selected data to (selected) variable
            # save new data into our tree
            focused = self.tree.focus()
            self.tree.item(focused, values=(
                selected,  # insert id
                self.add_entry.get(),  # insert updated computer name
            ), )
            # saves the list to our database (to be saved even after pausing the program
            js.update_computers_data_base(selected, self.add_entry.get())
            self.reset_entries()  # reset entries
        elif self.add_entry.get() == '':  # if no entered computer name
            mess_label = ttk.Label(self.edit_computers_frame, text="Computer Name can not be empty", foreground='red')
            mess_label.pack(pady=5)
            mess_label.after(3000, mess_label.destroy)

        elif len(self.add_entry.get()) <= 8:  # if computer name is less or greater than 8 charcaters
            mess_label3 = ttk.Label(self.edit_computers_frame, text="Computer Name must be at least 9 characters !!",
                                    foreground='red')
            mess_label3.pack(pady=5)
            mess_label3.after(3000, mess_label3.destroy)

        elif self.add_entry.get() in list(computers_data.values()):  # if computer name is already in the list
            mess_label2 = ttk.Label(self.edit_computers_frame, text="You did not change the name", foreground='red')
            mess_label2.pack(pady=5)
            mess_label2.after(3000, mess_label2.destroy)

        elif self.add_entry.get()[0:8] != "Computer":
            mess_label2 = ttk.Label(self.edit_computers_frame, text='Name not starting with "Computer"', foreground='red')
            mess_label2.pack(pady=5)
            mess_label2.after(3000, mess_label2.destroy)

        self.add_entry.delete(0, END)  # delete add entry


    def on_closing(self):
        """
        This function redefines protocol of button upon closing
        """
        EditComputers._instance = False
        self.page.destroy()