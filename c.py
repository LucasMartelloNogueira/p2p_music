import socket
import sys
import os
import wave
import json
import pyaudio
import math
import threading

from src.constants import Constants


def send_music(music_filename, server_ip, server_port):
    music_file = open(music_filename, "rb")
    wf = wave.open(music_file, 'rb')

    meta_data = {
        "width": wf.getsampwidth(),
        "num_chanels": wf.getnchannels(),
        "frame_rate": wf.getframerate()
    }

    data = json.dumps(meta_data)

    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # tcp
    tcp_sock.connect((server_ip, server_port))
    tcp_sock.send(bytes(data, "utf-8"))
    tcp_sock.close()

    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    with music_file as f:
        while (b := f.read(Constants.MUSIC_CHUNK_SIZE)):
            # info = {
            #     "chunk": b,
            #     "size": len(b)
            # }
            # data = json.dumps(info)
            # udp_sock.sendto(bytes(data, "utf-8"), (server_ip, server_port))
            
            udp_sock.sendto(b, (server_ip, server_port))
    
    udp_sock.close()
        


class Client:
    def __init__(self, port) -> None:
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.socket = self.get_socket()
        self.frames = []
        self.counter = 0


    
    def get_socket(self):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        # _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
        _socket.bind((self.ip, int(self.port)))
        return _socket


    def get_music_frames(self, music_filename):
        with wave.open(music_filename, "rb") as wf:
            contador = 0
            while len(data := wf.readframes(Constants.MUSIC_CHUNK_SIZE)):
                self.socket.sendto(data, (server_ip, server_port))
                print(f"enviou frame {contador}")
                contador += 1
                # self.frames.append(data)
                # print(f"sizeof data {sys.getsizeof(data)}")
                # if self.frames != None:
                #     self.frames += data
                # else:
                #     self.frames = data
                
                # print(f"tamanho chunk = {sys.getsizeof(data)}")
                # print(f"tamanho atual frames = {sys.getsizeof(self.frames)}")
                # print("\n----------------\n")
                # self.counter += 1


    def send_music(self):
        server_port = 9000
        server_ip = self.ip

        while True:
            if (self.counter >= Constants.MUSIC_BUFFER_SIZE):
                for i in range(len(self.frames)):
                    self.socket.sendto(self.frames.pop(0), (server_ip, server_port))
                    print(f"enviou o frame = {i}")
                # print(sys.getsizeof(self.frames))
                # self.socket.sendto(self.frames, (server_ip, server_port))
                # self.frames = None
                # self.counter = 0
                # print(f"enviou frame {contador}")
                # contador += 1
                self.counter = 0

    
    def start(self, music_filename):
        wf = wave.open(music_filename, "rb")

        meta_data = {
            "width": wf.getsampwidth(),
            "num_chanels": wf.getnchannels(),
            "frame_rate": wf.getframerate(),
            "seconds": 2
        }

        data = json.dumps(meta_data)

        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # tcp
        tcp_sock.connect((server_ip, server_port))
        tcp_sock.send(bytes(data, "utf-8"))
        tcp_sock.close()

        # buffer_size = meta_data["frame_rate"] * meta_data["seconds"]
        # buffer_size = 10
        # chunk_size = meta_data["width"]
        # print(f"chunk size: {chunk_size}")

        # for i, fr in enumerate(frames):
        #     print(f"frame {i}: {fr}")
        # print(len(frames))
        # print(frames[1])
        # print(type(frames[0]))
        # print(bytes(frames[1]))
        # print(frames)

        threading.Thread(target=self.get_music_frames, args=(music_filename,)).start()
        # threading.Thread(target=self.send_music, args=()).start()


# link util: https://stackoverflow.com/questions/21164804/udp-sound-transfer-played-sound-have-big-noise

args = sys.argv
client_ip = socket.gethostbyname(socket.gethostname())
server_ip = client_ip
server_port = 9000
port = 9876

# _socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # udp
# _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # tcp
# _socket.bind((client_ip, int(port)))
# _socket.connect((server_ip, server_port))



musics = {
    0: "assets\\music\\wav_file_1mb.wav",
    1: "assets\\music\\Uplifting_Motivational_Pop_Anthem_Coldplay_-_DimmyPlus.mp3"
}


# send_music(musics[0], server_ip, server_port)

# stream = []

# with open(musics[0], "rb") as f:
    # ler os bytes do arquivo e enviar via socket
    # while (b := f.read(Constants.MUSIC_CHUNK_SIZE)):
        # _socket.sendto(b, (server_ip, server_port))
        # stream.append(b)

# teste com envio de musica
# with _socket as sc:
#     for chunck in stream:
#         sc.sendto(chunck, (server_ip, server_port))

    # end = f.read()
    # print(end)
    # end2 = f.read()
    # print(end)
    # print(f"final pos = {f.tell()}")
    # print(f"final pos2 = {f.tell()}")

# teste com varios clientes
# with _socket as sc:
#     while True:
#         msg = input("digite uma msg: ")
#         sc.send(bytes(msg, "utf"))
#         response = sc.recv(2048).decode("utf-8")
#         print(f"server respondeu: {response}")



def main():
    c = Client(port)
    c.start(musics[0])

    # send_music(musics[0], server_ip, server_port)


if __name__ == "__main__":
    main()