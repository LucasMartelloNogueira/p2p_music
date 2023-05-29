import socket
from abc import ABC, abstractmethod
from constants import Constants
import threading

class IConnector(ABC):

    @abstractmethod
    def start(self):
        pass
    

class Connector(IConnector):

    def __init__(self, ip=Constants.localhost_ip) -> None:
        super().__init__()
        self.entry_port = Constants.server_port
        self.current_port = Constants.server_port + 1
        self.ip = ip
        self.entry_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.start()

    def client_connection(self, ip, port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.bind((ip, port))
        client_socket.listen()
        connection, addr = client_socket.accept()
        print(f"connectou com o cliente - ip:{addr} / porta: {port}")
        
        with connection as conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(data.decode("utf-8"))
                conn.send(data)

        connection.close()
        self.current_port - 1

    def start(self):
        print(f"comecando o server na porta: {self.entry_port}")
        self.entry_socket.bind((self.ip, self.entry_port))
        self.entry_socket.listen()

        while True:
            connection, address = self.entry_socket.accept()
            client

            # mandar a porta que sera usada na nova conexao
            connection.send(bytes(str(self.current_port), "utf-8"))
            print(f"escolhendo a porta {self.current_port} / para a cliente: {address[0]}")
            connection.close()

            # iniciar a thread
            chosen_port = self.current_port
            thread = threading.Thread(target=self.client_connection, args=(address[0], chosen_port))
            thread.start()
            print(f"criando a thread para a porta {self.current_port}")
            print(f"quantidade de threads activas: {threading.active_count()}")
            self.current_port += 1


server = Connector()