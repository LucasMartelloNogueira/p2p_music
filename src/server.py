import socket


host = socket.gethostbyname(socket.gethostname())
port = 8080

# OBS: socket.socket parametros:
# 1) Address family: ex: socket.AF_INET = ipv4
# 2) connection type: ex: socket.SOCK_STREAM = tcp / socket.SOCK_DGRAM = udp
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((host, port))
print(f"socket -> host: {host} / port: {port}")
socket.listen()

client_connection, client_info = socket.accept()

with client_connection as conn:
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(data.decode("utf-8"))
        conn.send(data)

client_connection.close()
print("conexao finalizada")

