import socket
import json
import threading
import queue
import os
import sys
import time

from src.constants import Constants

import pyaudio
import wave

"""
possiveis msgs do client:

"OP/CREATE_REGISTER"
"OP/CONNECT"
"""

class Client:

    def __init__(self, name="fulano", server_conn_port=59123, music_tcp_port=20_000, music_udp_port=21_000):
        self.name = name
        self.ip = socket.gethostbyname(socket.gethostname())
        self.server_conn_port = int(server_conn_port)
        self.socket = None
        self.music_tcp_port = int(music_tcp_port)
        self.music_udp_port = int(music_udp_port)

        # self.start()


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
        self.server_conn_port = int(first_connection.recv(Constants.msg_max_size).decode("utf-8"))
        first_connection.close()
        print("************************************")
        print("REGISTRO CRIADO COM SUCESSO")
        print("************************************\n")
        return("SUCCESS")

    
    def connect_to_server(self, server_ip=Constants.localhost_ip):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((server_ip, Constants.server_port))

        conn_msg = f"OP/CONNECT/{self.server_conn_port}"
        connection.send(bytes(conn_msg, "utf-8"))

        server_response = connection.recv(Constants.msg_max_size).decode("utf-8")
        if server_response.split("/")[1] == "ACCEPT_CONNECTION":
            print("************************************")
            print("CONEXAO ACEITA COM SUCESSO")
            print("************************************\n")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((server_ip, int(self.server_conn_port)))
            return("SUCCESS")
        else:
            print(f"não foi possivel conectar ao servidor = {server_response}")
            return(f"Não foi possivel conectar ao servidor = {server_response}")


    def connect_to_server_v2(self):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.bind((self.ip, self.server_conn_port))
        connection.connect((Constants.localhost_ip, Constants.server_port))
        # print("vendo status da conexao...")
        response = json.loads(connection.recv(Constants.msg_max_size).decode("utf-8"))
        # print("obteve primeira response do server")

        if response["permission"] == False:
            if response["reason"] == "first connection - not registered":
                connection.close()
                new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_conn_port = response["new_port"]
                new_sock.connect((Constants.localhost_ip, self.server_conn_port))
                self.socket = new_sock
            else:
                print("não possivel conectar ao servidor")
                print(response)

        if response["permission"] == True:
            self.socket = connection


    def listen_to_clients(self):
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.bind((self.ip, self.music_tcp_port))
        tcp_sock.listen()

        while True:
            connection, _ = tcp_sock.accept()
            data1 = json.loads(connection.recv(Constants.msg_max_size).decode("utf-8"))
            music = os.path.join("assets\music", data1["music_name"])

            tcp_ack_msg = {}

            if os.path.exists(music):
                wf = wave.open(music, "rb")
                tcp_ack_msg["status"] = "OK"
                tcp_ack_msg["width"] = wf.getsampwidth()
                tcp_ack_msg["num_chanels"] = wf.getnchannels()
                tcp_ack_msg["frame_rate"] = wf.getframerate()
                
                connection.send(bytes(json.dumps(tcp_ack_msg), "utf-8"))

                data2 = json.loads(connection.recv(Constants.msg_max_size).decode("utf-8"))
                connection.close()

                # p = pyaudio.PyAudio()
                # stream = p.open(
                #         format=p.get_format_from_width(wf.getsampwidth()),
                #         channels=wf.getnchannels(),
                #         rate=wf.getframerate(),
                #         input=True,
                #         frames_per_buffer=Constants.MUSIC_CHUNK_SIZE,
                # )
                
                if data2["status"] == "READY":
                    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, Constants.UDP_BUFFER_SIZE)
                    other_client_addr = (self.ip, data1["udp_port"])
                    
                    while (frame := wf.readframes(Constants.MUSIC_CHUNK_SIZE)):
                        udp_sock.sendto(frame, other_client_addr)
                        time.sleep(0.8 * Constants.MUSIC_CHUNK_SIZE / tcp_ack_msg["frame_rate"])

                    udp_sock.close()
            else:
                tcp_ack_msg["status"] = "404"
                tcp_ack_msg["status_msg"] = "Music not found"
                connection.send(bytes(json.dumps(tcp_ack_msg), "utf-8"))
                connection.close()

                
    def server_interaction(self):
        if self.socket is not None:
            with self.socket as sc:
                while True:
                    print("************************************")
                    print("SELECIONE UMA OPÇÃO")
                    print("1 - encerrar conexao")
                    print("2 - registrar musica")
                    print("3 - ver musicas de pessoas online")
                    print("4 - pedir musica")
                    print("************************************")

                    opt = int(input("digite a opção escolhida: "))

                    match opt:
                        case 1:
                            self.end_connection()

                        case 2:
                            self.register_song()

                        case 3:
                            self.view_server_registers
                            
                        case 4:
                            music_name = input("digite o nome da musica que deseja: ")
                            ip_other_client = input("digite o ip do outro cliente: ")
                            self.request_music(music_name, ip_other_client)
                        
                        case other:
                            print("opção não existe!")

                    if opt == 1:
                        break
                  
                # while True:
                #     msg = input("digite a sua msg: ")
                #     if len(msg) == 0:
                #         break
                #     sc.send(bytes(msg, "utf-8"))
                #     server_msg = sc.recv(1024).decode("utf-8")
                #     print(f"msg do server: {server_msg}")


    def start_v2(self):

        self.connect_to_server_v2()

        print("definiu o socket")

        # TODO: criar func de reconectar com cliente novo

        if self.socket is None:
            print("Não tem socket com servidor, terminando programa")
            sys.exit(1)
        else:
            print("conectado com o servidor")

        threading.Thread(target=self.server_interaction, args=()).start()
        threading.Thread(target=self.listen_to_clients, args=()).start()


    def start(self):
        # primeira conexao
        # recebendo do servidor a porta que sera usada para conexao de fato
        if self.server_conn_port is None:
            self.first_connection()
        
        self.connect_to_server()

        if self.socket is None:
            print("Não tem socket com servidor, terminando programa")
            sys.exit(1)

        threading.Thread(target=self.server_interaction, args=()).start()
        threading.Thread(target=self.listen_to_clients, args=()).start()

        
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

        
    def register_song(self, song_name):
        # print("************************************")
        # song_name = input("digite o nome da musica que deseja registrar: ")
        # print("************************************\n")
        msg = f"OP/REGISTER_SONG/{song_name}"

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


    def receive_and_play_song(self, music_name, other_client_ip):
        """
        faz a requisição de uma determinada musica para outro cliente
        """
        other_client_address = (other_client_ip, self.music_tcp_port)
        q = queue.Queue(maxsize=100_000)
        
        msg = { 
            "music_name": music_name,
            "udp_port": self.music_udp_port
        }

        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.connect(other_client_address)
        tcp_sock.send(bytes(json.dumps(msg), "utf-8"))

        response = json.loads(tcp_sock.recv(Constants.msg_max_size).decode("utf-8"))
        stream = None

        if response["status"] == "OK":
            p = pyaudio.PyAudio()
            stream = p.open(
                format=p.get_format_from_width(response["width"]),
                channels=response["num_chanels"],
                rate=response["frame_rate"],
                output=True
            )
        
            udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, Constants.UDP_BUFFER_SIZE)
            udp_sock.bind((self.ip, self.music_udp_port))

            def get_audio_data():
                while True:
                    try:
                        frame, _ = udp_sock.recvfrom(Constants.UDP_BUFFER_SIZE)
                        q.put(frame)
                    except:
                        return

            t2 = threading.Thread(target=get_audio_data, args=())
            t2.start()


            # indicando que agr esta pronto para receber a musica
            msg2 = {
                "status": "READY"
            }

            tcp_sock.send(bytes(json.dumps(msg2), "utf-8"))
            tcp_sock.close()

            time.sleep(5)  # deixand bufferizar um pouco...

            while True:
                try:
                    frame = q.get(timeout=10)
                    stream.write(frame)
                except:
                    print("\n*********\n musica acabou \n*********\n")
                    break
            
            # vai fechar o socket e acabar com a thread
            # acaba com a Thread pq gera excecao na hora de receber do socket udp pq ele vai estar fechado
            udp_sock.close()
        else:
            print("nao foi possivel obter a musica desejada")
            tcp_sock.close()
            
        
    def request_music(self, music_name, other_client_ip):
        threading.Thread(target=self.receive_and_play_song, args=(music_name, other_client_ip)).start()


    def end_connection(self):
        msg = "OP/END_CONNECTION"
        self.socket.send(bytes(msg, "utf-8"))
        print("************************************")
        print("ENCERRANDO A CONEXÃO")
        print("************************************")
        response = self.socket.recv(Constants.msg_max_size).decode("utf-8")
        if response == "DATA/ACK_END_CONNECTION":
            print("servidor reconheceu fim de conexao")
        self.socket.close()
