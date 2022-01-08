from tkinter import *
from tkinter import ttk
from tkinter.constants import N, S, E, W, VERTICAL, END

from json_funcs import A2_comp_data_func as js


class ShowComputers:
    """
    This class creates the show computers screen
    """
    # Class variable: keeps track of how many instances of this class have been called. 
    # 0 -> False, 1 -> True
    _instance = False

    def __init__(self):
        # Executes constructor only if no other instances have been called
        if ShowComputers._instance == False:
            # Builds new window
            page = Tk()
            page.title("Search Computer Page")
            page.minsize(500, 450)
            page.maxsize(550, 500)

            self.page = page

            # Defines style of new window
            style = ttk.Style(self.page)
            style.theme_use("clam")

            # Changes value of instance to one, which means an instance has been executed
            ShowComputers._instance = True
            # Calls function on_closing when window is closed
            self.page.protocol("WM_DELETE_WINDOW", self.on_closing)

            # Builds frame of widgets on page
            self.search_computers_frame = ttk.Frame(self.page)
            self.search_computers_frame.pack(fill="both", expand=True)

            # Builds all widgets
            self.build_tree()
            self.build_search_widgets()

            page.mainloop()

    def build_tree(self):
        """
        This function builds the treeview and its scrollbar
        """
        # Treeview frame
        tree_frame = ttk.Frame(self.search_computers_frame)

        # Column configuration
        self.search_computers_frame.columnconfigure(0, weight=10)
        self.search_computers_frame.columnconfigure(1, weight=1)

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
            # self.reset_entries()

        # Creates instance of scrollbar object
        s = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree['yscrollcommand'] = s.set

        # Grids the tree and scrollbar
        self.tree.grid(row=0, column=0)
        s.grid(row=0, column=1, sticky=(N, S, E, W))

        # Packs the frame
        tree_frame.pack(pady=20)


    def build_search_widgets(self):
        """
        Builds buttons in a frame and initializes their status to disabled.
        """
        # Creates a frame for the buttons
        search_frame = ttk.Frame(self.search_computers_frame)

        search_label = ttk.Label(search_frame, text='Search Computer Name')
        search_label.grid(row=0, column=0, padx=5)

        # Create entry boxes
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.grid(row=0, column=1, padx=5)

        # Seach Button
        search_computer = ttk.Button(search_frame, text='Search', width=15, command=self.search_by_computer_name)
        search_computer.grid(row=0, column=2, padx=5)

        # Build Report Frame
        self.search_widget_frame = ttk.Frame(self.search_computers_frame)

        # Packs the frame
        search_frame.pack(pady=20)


    def search_by_computer_name(self):
        """
        This function searches for a username in the database
        """
        # Flag turns True if username is found
        flag = False

        # Gets computers data dictionary
        computers_data = js.get_computers_data()  # gets member data dictionary
        # Gets computer name which is to be searched for
        com_name = self.search_entry.get()  # gets username which is wanted to be searched for
        for key in list(computers_data.keys()):
            if com_name == computers_data[key]:  # checks if username is correct(flag is true and break)
                # Checks if username is correct (flag is true and break)
                self.search_entry.delete(0, END)
                self.search_widget(com_name, key
                                   )
                flag = True
                break
            elif com_name != computers_data[key]:
                flag = False
        if not flag:  # checks if username is not in usernames(if flag is false)
            error_msg = ttk.Label(self.search_computers_frame, text="Computer Name is not correct or empty",
                                  foreground='red')  # show error message
            error_msg.pack()
            error_msg.after(3000, error_msg.destroy)


    def search_widget(self, computer_name, id):
        """
        Displays member report upon search
        """
        self.search_widget_frame.destroy()
        self.search_widget_frame = ttk.Frame(self.search_computers_frame)

        ttk.Label(self.search_widget_frame, text='Computer Name : ' + computer_name).grid(row=0, sticky=W)
        ttk.Label(self.search_widget_frame, text='ID : ' + str(id)).grid(row=1, sticky=W)
        self.tree.selection_set(id)  # a function in tree manages you to focus on searched item (by id(key=iid))

        self.search_widget_frame.pack(pady=10)


    def reset_entries(self):
        """
        Resets the content of entry
        """
        self.search_entry.delete(0, END)  # delete search entry

    def on_closing(self):
        """
        Called upon closing of the window
        """
        ShowComputers._instance = False
        self.page.destroy()