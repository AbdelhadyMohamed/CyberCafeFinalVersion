from tkinter import *
from tkinter import ttk, messagebox

from _0_welcome import WelcomePage


class Source:
    """
    This class acts as the root/door to the program. 
    The user instantiates this class to start the app
    """

    def __init__(self):

        # Creates instance of the whole app
        self.window = Tk()
        self.window.title("Cyber Cafe System")

        # Displays the app window at a custom position
        self.window.geometry("+550+250")

        # Defines style of program
        style = ttk.Style(self.window)
        style.theme_use("clam")

        # Instantiates Welcome Page
        WelcomePage(self.window)

        # Redefines protocol upon window closing
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Displays window
        self.window.mainloop()                  # Executes the instance of  the app (root)


    def on_closing(self):
        """
        Defines behavior of program when clicking on X button
        """
        if messagebox.askokcancel("Close the program", "Do you want to quit?"):
            self.window.destroy()

Source()