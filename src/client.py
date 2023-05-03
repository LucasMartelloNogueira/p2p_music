import socket

host = socket.gethostbyname(socket.gethostname())
# print(host)
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

while True:
    msg = input("digite sua msg: ")
    
    if len(msg) == 0:
        break
    
    s.send(bytes(msg, "utf-8"))
    print(s.recv(1024).decode("utf-8"))

s.close()