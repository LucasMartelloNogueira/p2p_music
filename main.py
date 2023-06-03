from tkinter import *

from src.entities.Server import Server
from src.entities.Client import Client
from src.entities.gui import Gui

import sys

# args_dict = dict()

# for arg in sys.argv[1:]:
#     key, value = arg.split("=")
#     args_dict[key] = value

# if __name__ == "__main__":
#     if args_dict["type"] == "server":
#         server = Server()

#     if args_dict["type"] == "client":
#         port = args_dict.get("port", None)
#         client = Client(connection_port=port)

# class Gui(Frame):

#     logFrame = None

#     def __init__(self, parent=None):
#         Frame.__init__(self,parent)
#         self.parent = parent
#         self.pack()
#         self.make_widgets()

#     def make_widgets(self):
#         self.winfo_toplevel().title("p2p Music")

#         mainFrame = Frame(root, padx=50, pady=50)
#         connectFrame = Frame(mainFrame)
#         self.logFrame = LabelFrame(mainFrame, text="Log", padx=5, pady=5)

#         portInput = Entry(connectFrame, width=20)
#         portInput.insert(0, "PORT")

#         serverButton = Button(mainFrame, text="Run Server", width=20, command=self.runServer())
#         registerButton = Button(mainFrame, text="Register", width=20, command=self.register())
#         loginButton = Button(connectFrame, text="Connect", width=20, command=self.connect(portInput.get()))
        
#         orLabel = Label(mainFrame, text="or")

#         mainFrame.pack()

#         connectFrame.pack()
#         portInput.grid(row=1, column=1)
#         loginButton.grid(row=1, column=2)
#         orLabel.pack()
#         serverButton.pack()
#         registerButton.pack()
#         self.logFrame.pack()

#     def log(self, text):
#         logEntry = Label(self.logFrame, text="> " + text)
#         logEntry.pack()

#     def runServer(self):
#         server = Server()

#     def register(self):
#         client = Client(connection_port=None)

#     def connect(self, port):
#         client = Client(connection_port=port)

root = Tk()
abc = Gui(root)
root.mainloop()