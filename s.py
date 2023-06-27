import socket
import threading
import json
import sys
import time

from src.constants import Constants

import pyaudio

# link util: https://stackoverflow.com/questions/21164804/udp-sound-transfer-played-sound-have-big-noise


class Server:

    def __init__(self) -> None:
        self.ip = socket.gethostbyname(socket.gethostname())
        self.server_port = 9000
        self.socket = self.get_socket()
        self.frames = []
        self.buffer_size = 0

        self.start()
        

    def get_socket(self):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        # _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
        _socket.bind((self.ip, self.server_port))
        return _socket

    # para msg de texto normal / testes
    # funciona com server com um mesmo ip/porta e atende varios clientes com ip/portas diferentes
    def client_conn(self, conection: socket.socket, address):
        with conection as conn:
            print(f"cliente conectado no endereco: {address}")
            while True:
                msg = conn.recv(2048).decode("utf-8")
                conn.send(bytes(msg, "utf-8"))


    def client_music_conn(self):
        # print("esperando por musica")
        i = 0
        while True:
            data, addr = self.socket.recvfrom(Constants.MUSIC_CHUNK_SIZE * 5)
            # print(f"tamanho data = {sys.getsizeof(data)}")
            self.frames.append(data)
            # self.buffer_size += 1
            print(f"recebeu frame = {i}")
            i += 1
            # for i in range(Constants.MUSIC_BUFFER_SIZE):
            #     self.frames.append(data[Constants.MUSIC_CHUNK_SIZE*i : Constants.MUSIC_CHUNK_SIZE*(i+1)])



    def play(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=Constants.PYAUDIO_FORMAT,
                        channels=Constants.MUSIC_CHANNELS,
                        rate=Constants.MUSIC_FRAME_RATE,
                        output=True,
                        frames_per_buffer=Constants.MUSIC_CHUNK_SIZE
                        )
        # print("esperando para tocar")
        while True:
            if len(self.frames) == Constants.MUSIC_BUFFER_SIZE:
                for _ in range(Constants.MUSIC_BUFFER_SIZE):
                    stream.write(self.frames.pop(0), Constants.MUSIC_CHUNK_SIZE)


    def playV2(self, stream):

        while True:
            print("preso aqui")
            if len(self.frames) >= Constants.MUSIC_BUFFER_SIZE:
                # while (len(self.frames) > 0):
                for _ in range(Constants.MUSIC_BUFFER_SIZE):
                    stream.write(self.frames.pop(0))



    


    def start(self):
        # self.socket.listen()
        print(f"esperando por dados na porta {self.server_port}")
        # while True:
            # conn, addr = self.socket.accept()
            
            # thread para msgs / teste para clients com ip/porta fixo e varios clientes
            # threading.Thread(target=self.client_conn, args=(conn, addr)).start()


        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.bind((self.ip, self.server_port))
        tcp_sock.listen()
        conn, adrr = tcp_sock.accept()
        data = conn.recv(Constants.msg_max_size).decode("utf-8")
        info = json.loads(data)
        print("recebeu meta dados!")
        print(info)
        tcp_sock.close()

        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(info["width"]),
            channels=info["num_chanels"],
            rate=info["frame_rate"],
            output=True
        )


        # threads para musica: uma para receber a musica e outra para tocar
        threading.Thread(target=self.client_music_conn, args=()).start()
        threading.Thread(target=self.playV2, args=[stream]).start()

Server()
