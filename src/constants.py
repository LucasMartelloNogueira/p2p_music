import socket

class Constants:
    localhost_ip = host = socket.gethostbyname(socket.gethostname())
    server_port = 8080
    request_port_msg = "REQUEST_NEW_PORT"
    msg_max_size = 2048 # bytes