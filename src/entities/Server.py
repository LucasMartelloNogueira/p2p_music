#  builtin inports
import socket
import threading
import os
import sys


# Project imports
from abc import ABC, abstractmethod
from src.constants import Constants
from src.entities.Connection import Connection

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
        self.entry_port = Constants.server_port
        self.ip = ip
        self.entry_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.register_filename = register_filename
        self.dataframe = self.get_client_dataframe()
        self.current_free_port = self.get_current_free_port()
        self.active_connections = []

        # self.start()
 
    def get_current_free_port(self):
        return self.entry_port + self.dataframe.shape[0] + 1

    def get_client_dataframe(self):
        filepath = os.path.join(os.getcwd(), "assets", "csv_files", self.register_filename)
        if os.path.exists(filepath):
            return pd.read_csv("assets\\csv_files\\clients.csv")
        else:
            df = pd.DataFrame(columns=["ip", "port", "name"])
            df.to_csv(filepath, index=False)
            return df


    def register_client(self, ip, port, name):
        new_row = {"ip": ip, "port": int(port), "name": name}
        new_line_index = self.dataframe.shape[0]
        self.dataframe.loc[new_line_index, :] = new_row
        self.dataframe.to_csv("assets\\csv_files\\clients.csv", index=False)
        
        print("************************************")
        print("CLIENTE CADASTRADO COM SUCESSO")
        print("dados do cliente")
        print(f"nome: {name}")
        print(f"ip: {ip}")
        print(f"porta: {port}")
        print("************************************\n")


    def check_client_connection(self, ip, port):
        # ok: tem registro e n ta ativo
        # erro: n tem registro
        # erro: tem registro mas ta ativo
        filt = (self.dataframe["ip"] == ip) & (self.dataframe["port"] == int(port))
        df = self.dataframe.loc[filt]
        
        if df.shape[0] == 0:
            return "ERROR/CLIENT_NOT_REGISTRED"

        for conn in self.active_connections:
            if conn.client_ip == ip and conn.client_port == port:
                return "ERROR/CLIENT_ONLINE"
        
        return "OP/ACCEPT_CONNECTION"


    def client_connection(self, ip, port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.bind((ip, port))
        client_socket.listen()
        connection, addr = client_socket.accept()
        current_conection = Connection(ip, port, addr[0], addr[1])
        self.active_connections.append(current_conection)
        
        print("************************************")
        print(f"CONECTADO COM O CLIENTE")
        print("dados da conexão")
        print(f"Servidor: ip = {ip} / porta = {port}")
        print(f"cliente: ip = {addr[0]} / porta = {addr[1]}")
        print("************************************\n")
        
        with connection as conn:
            while True:
                try:
                    data = conn.recv(Constants.msg_max_size).decode("utf-8")
                    if data:
                        # print(f"DATA = {data}")
                        data_list = data.split("/")
                        if data_list[1] == "END_CONNECTION":
                            print("************************************")
                            print("ENCERRANDO CONEXÃO")
                            print("dados da conexão encerrada")
                            print(f"cliente: ip = {current_conection.client_ip} / porta = {current_conection.client_port}")
                            print("************************************\n")

                            # TODO: remover cliente do dataframe de clientes online
                            self.active_connections.remove(current_conection)
                            connection.close()
                            break

                except ConnectionResetError:
                    print("************************************")
                    print("CONEXAO PERDIDA")
                    print("dados do cliente")
                    print(f"cliente: ip = {current_conection.client_ip} / porta = {current_conection.client_port}")
                    print("************************************\n")
                    connection.close()
                    break

                except TypeError:
                    print("************************************")
                    print(f"nenhuma msg recebida de: {current_conection.client_ip} / porta = {current_conection.client_port}")
                    print("************************************\n")


    def start(self):
        self.entry_socket.bind((self.ip, self.entry_port))
        self.entry_socket.listen()

        while True:
            print(f"escutando por clientes na porta: {self.entry_port}")
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
                msg = self.check_client_connection(address[0], data[2])

                if msg == "OP/ACCEPT_CONNECTION":
                    client_port = int(data[2])
                    msg = f"{msg}/{client_port}"
                    thread = threading.Thread(target=self.client_connection, args=(address[0], client_port))
                    thread.start()
                
                connection.send(bytes(msg, "utf-8"))

            connection.close()
