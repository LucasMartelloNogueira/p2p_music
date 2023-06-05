#  builtin inports
import socket
import threading
import os
import sys
import json


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

    def __init__(self, ip=Constants.localhost_ip, register_filename="clients.csv", music_filename="music.csv"):
        super().__init__()
        self.entry_port = Constants.server_port
        self.ip = ip
        self.entry_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.register_filename = register_filename
        self.music_filename = music_filename
        self.clients_dataframe = self.get_client_dataframe()
        self.music_dataframe = self.get_music_dataframe()
        self.current_free_port = self.get_current_free_port()
        self.active_connections : list[Connection] = []

        # self.start()
 

    def get_current_free_port(self):
        return self.entry_port + self.clients_dataframe.shape[0] + 1


    def get_fullpath_music_filename(self):
        return os.path.join(os.getcwd(), "assets", "csv_files", self.music_filename)


    def get_music_dataframe(self):
        filepath = self.get_fullpath_music_filename()
        if os.path.exists(filepath):
            return pd.read_csv(f"assets\\csv_files\\{self.music_filename}")
        else:
            df = pd.DataFrame(columns=["ip", "port", "song_name"])
            df.to_csv(filepath, index=False)
            return df


    def get_client_dataframe(self):
        filepath = os.path.join(os.getcwd(), "assets", "csv_files", self.register_filename)
        if os.path.exists(filepath):
            return pd.read_csv(f"assets\\csv_files\\{self.register_filename}")
        else:
            df = pd.DataFrame(columns=["ip", "port", "name"])
            df.to_csv(filepath, index=False)
            return df


    def register_client(self, ip, port, name):
        new_row = {"ip": ip, "port": int(port), "name": name}
        new_line_index = self.clients_dataframe.shape[0]
        self.clients_dataframe.loc[new_line_index, :] = new_row
        self.clients_dataframe.to_csv("assets\\csv_files\\clients.csv", index=False)
        
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
        filt = (self.clients_dataframe["ip"] == ip) & (self.clients_dataframe["port"] == int(port))
        df = self.clients_dataframe.loc[filt]
        
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
        _socket, addr = client_socket.accept()
        current_conection = Connection(ip, port, addr[0], addr[1])
        self.active_connections.append(current_conection)
        
        print("************************************")
        print(f"CONECTADO COM O CLIENTE")
        print("dados da conexão")
        print(f"Servidor: ip = {ip} / porta = {port}")
        print(f"cliente: ip = {addr[0]} / porta = {addr[1]}")
        print("************************************\n")
        
        with _socket as sc:
            while True:
                try:
                    data = sc.recv(Constants.msg_max_size).decode("utf-8")
                    if data:
                        # print(f"DATA = {data}")
                        data_list = data.split("/")
                        if data_list[1] == "END_CONNECTION":
                            self.end_client_connection(current_conection, _socket)
                            _socket.close()
                            break
                        
                        if data_list[1] == "REGISTER_SONG":
                            print("quis registrar musica")
                            song_name = data_list[2]
                            self.register_song(current_conection, _socket, song_name)

                        if data_list[1] == "VIEW_REGISTERS":
                            print("************************************")
                            print(f"cliente {current_conection.client_ip} quis ver registros")
                            print("************************************\n")
                            self.get_connected_clients_musics(_socket)

                except ConnectionResetError:
                    print("************************************")
                    print("CONEXAO PERDIDA")
                    print("dados do cliente")
                    print(f"cliente: ip = {current_conection.client_ip} / porta = {current_conection.server_port}")
                    print("************************************\n")
                    self.active_connections.remove(current_conection)
                    _socket.close()
                    break

                except TypeError:
                    print("************************************")
                    print(f"nenhuma msg recebida de: {current_conection.client_ip} / porta = {current_conection.server_port}")
                    print("************************************\n")


    def end_client_connection(self, conection, socket: socket.socket):
        print("************************************")
        print("ENCERRANDO CONEXÃO")
        print("dados da conexão encerrada")
        print(f"cliente: ip = {conection.client_ip} / porta = {conection.client_port}")
        print("************************************\n")

        socket.send(bytes("DATA/ACK_END_CONNECTION", "utf-8"))
        self.active_connections.remove(conection)


    def register_song(self, connection: Connection, socket: socket.socket, song_name: str) -> None:

        msg = "ERROR/UNEXPECTED_ERROR"

        # confere se o cliente já tem a musica cadastrada
        filt = (self.music_dataframe["ip"] == connection.client_ip) & (self.music_dataframe["port"] == connection.server_port) & (self.music_dataframe["song_name"] == song_name)
        df = self.music_dataframe[filt]
        if df.shape[0] > 0:
            print("************************************")
            print("ERRO AO CADASTRAR MUSICA")
            print(f"cliente: {connection.client_ip} / {connection.server_port} ja tem a música {song_name} cadastrada")
            print("************************************\n")
            msg = "ERROR/SONG_ALREADY_REGISTRED"
        else:
            new_row = {"ip": connection.client_ip, "port": connection.server_port, "song_name": song_name}
            n = self.music_dataframe.shape[0]
            self.music_dataframe.loc[n, :] = new_row
            self.music_dataframe.to_csv(self.get_fullpath_music_filename(), index=False)
            print("************************************")
            print("MUSICA CADASTRADA COM SUCESSO")
            print(f"cliente: {connection.client_ip} / {connection.server_port} CADASTROU A MUSICA {song_name}")
            print("************************************\n")
            msg = "DATA/MUSIC_REGISTRED"
        
        socket.send(bytes(msg, "utf-8"))
        
        
    def get_connected_clients_musics(self, socket: socket.socket):

        data = {"users": []}

        for connection in self.active_connections:
            user = {"ip": connection.client_ip}
            filt = (self.music_dataframe["ip"] == connection.client_ip) & (self.music_dataframe["port"] == connection.server_port)
            musics = list(self.music_dataframe.loc[filt, "song_name"].values)
            if len(musics) > 0:
                user["musics"] = musics
                data["users"].append(user)

        data_str = json.dumps(data)
        size = sys.getsizeof(data_str)
        msg = f"OP/NEXT_MSG_SIZE/{size}"
        socket.send(bytes(msg, "utf-8"))
        response = socket.recv(Constants.msg_max_size).decode("utf-8")
        if response == "OP/ACK":
            socket.send(bytes(data_str, "utf-8"))
            

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
