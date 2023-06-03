from tkinter import *
from src.entities.Server import Server
from src.entities.Client import Client
import threading

class Gui(Frame):

    logFrame = None
    portInput = None

    def __init__(self, parent=None):
        Frame.__init__(self,parent)
        self.parent = parent
        self.pack()
        self.make_widgets()

    def make_widgets(self):
        self.winfo_toplevel().title("p2p Music")

        mainFrame = Frame(self, padx=50, pady=50)
        connectFrame = Frame(mainFrame)
        self.logFrame = LabelFrame(mainFrame, text="Log", padx=5, pady=5)

        self.portInput = Entry(connectFrame, width=20)
        self.portInput.insert(0, "PORT")

        serverButton = Button(mainFrame, text="Run Server", width=20, command=self.runServer)
        registerButton = Button(mainFrame, text="Register", width=20, command=self.register)
        loginButton = Button(connectFrame, text="Connect", width=20, command=self.connect)
        
        orLabel = Label(mainFrame, text="or")

        mainFrame.pack()

        connectFrame.pack()
        self.portInput.grid(row=1, column=1)
        loginButton.grid(row=1, column=2)
        orLabel.pack()
        serverButton.pack()
        registerButton.pack()
        self.logFrame.pack()

    def log(self, text):
        logEntry = Label(self.logFrame, text="> " + text)
        logEntry.pack()

    def runServer(self):
        server = Server()
        thread = threading.Thread(target=server.start)
        thread.start()

    def register(self):
        client = Client(connection_port=None)

    def connect(self):
        client = Client(connection_port=self.portInput.get())

# root = Tk()
# abc = Gui(root)
# root.mainloop()