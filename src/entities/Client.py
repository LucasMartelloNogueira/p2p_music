from src.constants import Constants

import socket
import json
import colorama


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
        return("SUCCESS")

    
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
            return("SUCCESS")
        else:
            print(f"não foi possivel conectar ao servidor = {server_response}")
            return(f"Não foi possivel conectar ao servidor = {server_response}")
            

    def start(self):
        # primeira conexao
        # recebendo do servidor a porta que sera usada para conexao de fato
        if self.connection_port is None:
            return self.first_connection()
        
        return self.connect_to_server()

        # if self.socket is not None:
        #     with self.socket as sc:
        #         while True:
        #             print("************************************")
        #             print("SELECIONE UMA OPÇÃO")
        #             print("1 - encerrar conexao")
        #             print("2 - registrar musica")
        #             print("3 - ver musicas de pessoas online")
        #             print("************************************")

        #             options = {
        #                 1: self.end_connection, 
        #                 2: self.register_song,
        #                 3: self.view_server_registers
        #             }

        #             opt = int(input("digite a opção escolhida: "))

        #             if opt in options:
        #                 options[opt]()
        #                 if opt == 1:
        #                     break

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
        # print("oiiiiiiiiiii")
        msg = "OP/VIEW_REGISTERS"
        self.socket.send(bytes(msg, "utf-8"))
        response = self.socket.recv(Constants.msg_max_size).decode("utf-8")
        data = response.split("/")
        if data[0] == "OP" and data[1] == "NEXT_MSG_SIZE":
            self.socket.send(bytes("OP/ACK", "utf-8"))
            size = int(data[2])
            json_data = json.loads(self.socket.recv(size).decode("utf-8"))
            print(json.dumps(json_data, indent=4))
            return (json.dumps(json_data, indent=4))

        

    def register_song(self, songName):
        # print("************************************")
        # song_name = input("digite o nome da musica que deseja registrar: ")
        # print("************************************\n")
        msg = f"OP/REGISTER_SONG/{songName}"

        self.socket.send(bytes(msg, "utf-8"))
        response = self.socket.recv(Constants.msg_max_size).decode("utf-8")
        data = response.split("/")

        if data[0] == "ERROR":
            if data[1] == "SONG_ALREADY_REGISTRED":
                print("************************************")
                print("ERRO: MUSICA JÁ CADASTRADA")
                print("************************************\n")
                return("ERRO: MUSICA JÁ CADASTRADA")
            
            if data[1] == "UNEXPECTED_ERROR":
                print("************************************")
                print("ERRO: NÃO FOI POSSIVEL REGISTAR MUSICA / ERRO INESPERADO")
                print("************************************\n")
                return("ERRO: NÃO FOI POSSIVEL REGISTAR MUSICA / ERRO INESPERADO")
        
        elif data[1] == "MUSIC_REGISTRED":
            print("************************************")
            print("SUCESSO: MUSICA CADASTRADA COM SUCESSO")
            print("************************************\n")
            return("SUCCESS")

        else:
            print("************************************")
            print("WARNING: RESPOSTA NÃO ESPERADA PELO SERVIDOR")
            print("************************************\n")
            return("WARNING: RESPOSTA NÃO ESPERADA PELO SERVIDOR")


    def end_connection(self):
        # TODO: implement this
        # has to send msg to server informing that will disconnect

        msg = "OP/END_CONNECTION"
        self.socket.send(bytes(msg, "utf-8"))
        print("************************************")
        print("ENCERRANDO A CONEXÃO")
        print("************************************")
        self.socket.close()
