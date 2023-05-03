import socket
import pandas as pd
import json
import os

class Server:

    def __init__(self, port=8080, filepath="assets\csv_files\clients.csv") -> None:
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.connection = None
        self.filepath = filepath


    def connect_to_client(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.bind((self.host, self.port))
        self.connection.listen()

        client_connection, client_info = self.connection.accept()

        with client_connection as conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(data.decode("utf-8"))
                conn.send(data)

        self.connection.close()
        client_connection.close()

    
    def end_connection(self):
        self.connection.close()
        self.connection = None


    def create_register(self):

        client_conn, client_info = self.connection.accept()
        data = client_conn.recv(2048)
        data =  json.loads(data.decode("utf-8"))

        if (os.path.exists(self.filepath)) is True:
            clients = pd.read(self.filepath)
        else:
            clients = pd.DataFrame(self.filepath, columns=["name", "ip", "port"])

        clients._append(data)
        clients.to_csv(self.filepath, index=False)