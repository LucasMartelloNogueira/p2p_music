import socket
from constants import Constants

host = socket.gethostbyname(socket.gethostname())
port = Constants.server_port
nova_porta = None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
nova_porta = int(s.recv(1024).decode("utf-8"))
print(f"porta escolhida = {nova_porta}")

conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_socket.connect((host, nova_porta))

with conn_socket as cs:
    while True:
        msg = input("digite a sua msg: ")
        if len(msg) == 0:
            break
        cs.send(bytes(msg, "utf-8"))
        server_msg = cs.recv(1024).decode("utf-8")
        print(f"msg do server: {server_msg}")

s.close()