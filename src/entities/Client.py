from src.constants import Constants

import socket
import sys


"""
possiveis msgs do client:

"OP/CREATE_REGISTER"
"OP/CONNECT"
"""

class Client:

    def __init__(self, name="fulano", connection_port=None) -> None:
        self.name = name
        self.ip = socket.gethostbyname(socket.gethostname())
        self.connection_port = connection_port
        self.socket = None

        self.start()


    def first_connection(self, server_ip=Constants.localhost_ip):
        """
        connect to the server for the first time

        automaticaly creates a register in the server and receives a port user for a socket connection

        :param server_ip: ip of the server
        """
        first_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        first_connection.connect((server_ip, Constants.server_port))

        first_conn_msg = f"OP/CREATE_REGISTER/{self.ip}/{self.name}"
        first_connection.send(bytes(first_conn_msg, "utf-8"))
        self.connection_port = int(first_connection.recv(Constants.msg_max_size).decode("utf-8"))
        first_connection.close()

    
    def connect_to_server(self, server_ip=Constants.localhost_ip):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((server_ip, Constants.server_port))

        conn_msg = f"OP/CONNECT/{self.connection_port}"
        connection.send(bytes(conn_msg, "utf-8"))

        server_response = connection.recv(Constants.msg_max_size).decode("utf-8")
        if server_response == "OP/ACCEPT_CONNECTION":
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((server_ip, self.connection_port))
            

    def start(self):
        # primeira conexao
        # recebendo do servidor a porta que sera usada para conexao de fato
        if self.connection_port is None:
            self.first_connection()
        
        self.connect_to_server()

        with self.socket as sc:
            while True:
                msg = input("digite a sua msg: ")
                if len(msg) == 0:
                    break
                sc.send(bytes(msg, "utf-8"))
                server_msg = sc.recv(1024).decode("utf-8")
                print(f"msg do server: {server_msg}")
        
    
    def view_server_registers(self):
        pass
        # msg = "DATA/VIEW_REGISTERS"
        # msg_size = sys.getsizeof(msg)
        # ctrl_msg = f"CTRL/{msg_size}"

        # self.socket.send(bytes(ctrl_msg, "utf-8"))
        # response = self.socket.recv(1024).decode("utf-8")

        # if response == f"ACK/{ctrl_msg}":
        #     self.socket.send(bytes(msg, "utf-8"))
        #     client_registers = self.socket.recv(1024).decode("utf-8")
        #     client_registers.split("/")


    def end_connection(self):
        self.connection.close()

    

client = Client()        

