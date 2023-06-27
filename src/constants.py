import socket
import pyaudio

class Constants:
    localhost_ip = host = socket.gethostbyname(socket.gethostname())
    server_port = 8080
    request_port_msg = "REQUEST_NEW_PORT"
    MUSIC_EXCHANGE_PORT = 9000
    msg_max_size = 2048 # bytes
    MUSIC_CHUNK_SIZE = 1024
    UDP_BUFFER_SIZE = 65536
    MUSIC_BUFFER_SIZE = 5
    MUSIC_CHANNELS = 2
    MUSIC_FRAME_RATE = 44100