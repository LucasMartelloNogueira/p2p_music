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
        print("************************************")
        print("REGISTRO CRIADO COM SUCESSO")
        print("************************************\n")

    
    def connect_to_server(self, server_ip=Constants.localhost_ip):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((server_ip, Constants.server_port))

        conn_msg = f"OP/CONNECT/{self.connection_port}"
        connection.send(bytes(conn_msg, "utf-8"))

        server_response = connection.recv(Constants.msg_max_size).decode("utf-8")
        if server_response.split("/")[1] == "ACCEPT_CONNECTION":
            print("************************************")
            print("CONEXAO ACEITA COM SUCESSO")
            print("************************************\n")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((server_ip, int(self.connection_port)))
        else:
            print(f"não foi possivel conectar ao servidor = {server_response}")
            

    def start(self):
        # primeira conexao
        # recebendo do servidor a porta que sera usada para conexao de fato
        if self.connection_port is None:
            self.first_connection()
        
        self.connect_to_server()

        if self.socket is not None:
            with self.socket as sc:
                while True:
                    print("************************************")
                    print("SELECIONE UMA OPÇÃO")
                    print("1 - encerrar conexao")
                    print("2 - registrar musica")
                    print("************************************")

                    options = {1: self.end_connection, 2: self.register_song}
                    opt = int(input("digite a opção escolhida: "))

                    if opt in options:
                        options[opt]()
                        if opt == 1:
                            break

            #     while True:
            #         msg = input("digite a sua msg: ")
            #         if len(msg) == 0:
            #             break
            #         sc.send(bytes(msg, "utf-8"))
            #         server_msg = sc.recv(1024).decode("utf-8")
            #         print(f"msg do server: {server_msg}")

            # self.socket.close()
        

    def view_server_registers(self):
        # TODO: implement this
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


    def register_song(self):
        # TODO: implement this
        print("************************************")
        song_name = input("digite o nome da musica que deseja registrar: ")
        print("************************************\n")
        msg = f"OP/REGISTER_SONG/{song_name}"

        self.socket.send(bytes(msg, "utf-8"))
        response = self.socket.recv(Constants.msg_max_size).decode("utf-8")
        data = response.split("/")

        if data[0] == "ERROR":
            if data[1] == "SONG_ALREADY_REGISTRED":
                print("************************************")
                print("ERRO: MUSICA JÁ CADASTRADA")
                print("************************************\n")
            
            if data[1] == "UNEXPECTED_ERROR":
                print("************************************")
                print("ERRO: NÃO FOI POSSIVEL REGISTAR MUSICA / ERRO INESPERADO")
                print("************************************\n")
        
        elif data[1] == "MUSIC_REGISTRED":
            print("************************************")
            print("SUCESSO: MUSICA CADASTRADA COM SUCESSO")
            print("************************************\n")

        else:
            print("************************************")
            print("WARNING: RESPOSTA NÃO ESPERADA PELO SERVIDOR")
            print("************************************\n")


    def end_connection(self):
        # TODO: implement this
        # has to send msg to server informing that will disconnect

        msg = "OP/END_CONNECTION"
        self.socket.send(bytes(msg, "utf-8"))
        print("************************************")
        print("ENCERRANDO A CONEXÃO")
        print("************************************")
        self.socket.close()
