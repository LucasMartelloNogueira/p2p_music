from tkinter import *
from src.entities.Server import Server
from src.entities.Client import Client
import threading

class Gui(Frame):

    def __init__(self, parent=None):
        Frame.__init__(self,parent)
        self.parent = parent
        self.pack()
        self.logArray: list[Label] = []
        self.make_widgets()

    def make_widgets(self):
        self.winfo_toplevel().title("p2p Music")

        self.mainFrame = Frame(self, padx=50, pady=50)
        self.commandFrame = Frame(self.mainFrame)
        self.connectFrame = Frame(self.commandFrame)
        self.logFrame = LabelFrame(self.mainFrame, text="Log", padx=5, pady=5)
        self.clientFrame = Frame(self.mainFrame)
        self.registerSongFrame = Frame(self.clientFrame)
        self.requestSongFrame = Frame(self.clientFrame)

        self.portInput = Entry(self.connectFrame, width=20)
        self.portInput.insert(0, "SERVER CONNECTION PORT")
        self.tcpInput = Entry(self.connectFrame, width=20)
        self.tcpInput.insert(0, "TCP PORT")
        self.udpInput = Entry(self.connectFrame, width=20)
        self.udpInput.insert(0, "UDP PORT")
        self.songInput = Entry(self.registerSongFrame, width=30)
        self.songInput.insert(0, "Song Name")
        self.songRequestInput = Entry(self.requestSongFrame, width=30)
        self.songRequestInput.insert(0, "Song Name")
        self.songRequestIpInput = Entry(self.requestSongFrame, width=30)
        self.songRequestIpInput.insert(0, "Client IP")
        self.songRequestPortInput = Entry(self.requestSongFrame, width=30)
        self.songRequestPortInput.insert(0, "Client Port")

        self.serverButton = Button(self.commandFrame, text="Run Server", width=20, command=self.runServer)
        self.registerButton = Button(self.commandFrame, text="Register", width=20, command=self.register)
        self.loginButton = Button(self.connectFrame, text="Connect", width=20, command=self.connect)
        self.registerSongButton = Button(self.registerSongFrame, text="Register Song",  width=20, command=self.registerSong)
        self.viewServerRegistersButton = Button(self.clientFrame, text="Available Songs",  width=20, command=self.viewServerRegisters)
        self.requestSongButton = Button(self.requestSongFrame, text="Request Song",  width=20, command=self.requestSong)
        self.endConnectionButton = Button(self.clientFrame, text="End Connection",  width=20, command=self.endConnection)
        self.listSongsButton = Button(self.mainFrame, text="List AVailable Songs",  width=20, command=self.listSongs)

        self.orLabel = Label(self.commandFrame, text="or")

        self.mainFrame.pack()
        self.commandFrame.pack()
        self.connectFrame.pack()
        self.portInput.grid(row=1, column=1)
        self.tcpInput.grid(row=1, column=2)
        self.udpInput.grid(row=1, column=3)
        self.loginButton.grid(row=1, column=4)
        self.orLabel.pack()
        self.serverButton.pack()
        self.registerButton.pack()
        self.logFrame.pack()

    def log(self, text):
        logEntry = Label(self.logFrame, text="> " + text, justify="left", anchor="w", font=('Courier', 11))
        self.logArray.append(logEntry)
        logEntry.pack()

    def runServer(self):
        self.server = Server()
        self.serverThread = threading.Thread(target=self.server.start_v2)
        self.serverThread.start()
        self.commandFrame.pack_forget()
        self.listSongsButton.pack()
        self.logFrame.pack()
        self.log("Escutando por clientes na porta: " + str(self.server.entry_port))

    def register(self):
        self.client = Client(connection_port=None)
        self.log(f"Registro criado com sucesso na porta {self.client.server_conn_port}")
        # self.commandFrame.pack_forget()
        # self.clientFrame.pack()
        # self.registerSongFrame.pack()
        # self.songInput.grid(row=1, column=1)
        # self.registerSongButton.grid(row=1, column=2)
        # self.viewServerRegistersButton.pack()
        # self.endConnectionButton.pack()
        # self.logFrame.pack()

    def connect(self):
        self.client = Client(self, "fulano", self.portInput.get(), self.tcpInput.get(), self.udpInput.get())
        self.client.start_v2()
        self.commandFrame.pack_forget()
        self.logFrame.pack_forget()
        self.clientFrame.pack()
        self.registerSongFrame.pack()
        self.requestSongFrame.pack()
        self.songInput.grid(row=1, column=1)
        self.registerSongButton.grid(row=1, column=2)
        self.songRequestInput.grid(row=1, column=1)
        self.songRequestIpInput.grid(row=1, column=2)
        self.songRequestPortInput.grid(row=1, column=3)
        self.requestSongButton.grid(row=1, column=4)
        self.viewServerRegistersButton.pack()
        self.endConnectionButton.pack()
        self.logFrame.pack()

    def endConnection(self):
        if self.client != None:
            self.client.end_connection()
            self.clientFrame.pack_forget()
            self.clearLog()
            self.logFrame.pack_forget()
            self.commandFrame.pack()
            self.logFrame.pack()
    
    def registerSong(self):
        if self.client != None:
            if self.songInput.get():
                msg = self.client.register_song(self.songInput.get())
                self.log(msg)

    def viewServerRegisters(self):
        if self.client != None:
            msg = self.client.view_server_registers()
            self.log(msg)

    def clearLog(self):
        for entry in self.logArray:
            entry.destroy()
        self.logArray = []

    def listSongs(self):
        self.log("\n" + str(self.server.list_songs()))

    def requestSong(self):
        if self.client != None:
            if self.songRequestInput.get() and self.songRequestIpInput.get():
                self.client.request_music(self.songRequestInput.get(), self.songRequestIpInput.get(), self.songRequestPortInput.get())