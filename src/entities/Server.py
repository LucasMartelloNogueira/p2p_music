#  builtin inports
import socket
import threading
import os
import sys


# Project imports
from abc import ABC, abstractmethod
from src.constants import Constants

# third party import
import pandas as pd


"""
posssiveis mensagens do servidor:

"OP/ACCEPT_CONNECTION"

"""



class IServer(ABC):

    @abstractmethod
    def start(self):
        pass
    

class Server(IServer):

    def __init__(self, ip=Constants.localhost_ip, current_free_port=Constants.server_port+1, register_filename="clients.csv") -> None:
        super().__init__()
        self.entry_port : int = Constants.server_port
        self.ip : str = ip
        self.current_free_port : int = current_free_port
        self.entry_socket : socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.register_filename = register_filename
        self.dataframe: pd.DataFrame = self.get_client_dataframe()

        self.start()

    
    def get_client_dataframe(self):
        if os.path.exists(os.path.join(os.getcwd(), f"/assets/csv_files/{self.register_filename}")):
            return pd.DataFrame(columns=["ip", "port", "name"])
        else:
            # TODO: criar funcao que cria arquivo no diretorio: <root>/assets/csv_files/<self.register_filename>
            pass


    def register_client(self, ip, port, name):
        new_row = {"ip": [ip], "port": [port], "name": [name]}
        self.dataframe = pd.concat([self.dataframe, pd.DataFrame(new_row)])
        self.dataframe.to_csv("clients.csv", index=False)


    def client_connection(self, ip, port):

        # TODO: falta consultar o dataframe para ver se o cliente esta registrado, se n estiver, enviar msg de erro "ERROR/NOT_REGISTERED"

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.bind((ip, port))
        client_socket.listen()
        connection, addr = client_socket.accept()
        print(f"connectou com o cliente - ip:{addr} / porta: {port}")
        
        with connection as conn:
            while True:
                data = conn.recv(Constants.msg_max_size)
                if not data:
                    break
                print(data.decode("utf-8"))
                conn.send(data)

        connection.close()


    def start(self):
        print(f"comecando o server na porta: {self.entry_port}")
        self.entry_socket.bind((self.ip, self.entry_port))
        self.entry_socket.listen()

        while True:
            connection, address = self.entry_socket.accept()
            data = connection.recv(Constants.msg_max_size).decode("utf-8").split("/")
            operation = data[1]

            if operation == "CREATE_REGISTER":
                self.register_client(data[2], self.current_free_port, data[3])
                connection.send(bytes(str(self.current_free_port), "utf-8"))
                print(f"escolhendo a porta {self.current_free_port} para o cliente {address}")
                self.current_free_port += 1
                print(f"proxima porta disponivel: {self.current_free_port}")
                connection.close()

            if operation == "CONNECT":
                client_port = int(data[2])
                thread = threading.Thread(target=self.client_connection, args=(address[0], client_port))
                connection.send(bytes("OP/ACCEPT_CONNECTION", "utf-8"))
                connection.close()
                thread.start()
