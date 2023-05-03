import socket

class Client:
    def __init__(self, name="fulano") -> None:
        self.name = name
        self.ip = socket.gethostbyname(socket.gethostname())
        self.connection = None


    def connect_to_server(self, server_ip, server_port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((server_ip, server_port))

        # while True:
        #     msg = input("digite sua msg: ")
            
        #     if len(msg) == 0:
        #         break
            
        #     self.connection.send(bytes(msg, "utf-8"))
        #     print(self.connection.recv(1024).decode("utf-8"))

        # self.end_connection()



    def register(self):
        msg = "{'name': {}, 'ip': {}, 'port': {}}".format(self.name, self.ip, self.port)
        self.connection.send(bytes(msg, "utf-8"))

    
    def view_register():
        pass


    def end_connection(self):
        self.connection.close()

    

    
    def cli(self):
        while True:

            print("** select your comand **")
            print("1 - connect to server")
            print("2 - create register")
            print("3 - close connection")

            command = int(input("enter a command: "))

            # commands = {
            #     1: self.connect_to_server, 
            #     2: self.register,
            #     3: self.end_connection
            # }

            # if (command not in range(1, 4)):
            #     print("comando invalido")
            # else:
            #     if (command == 1):
            #         self.connect_to_server(self.ip, 8080)
                
            #     if (command == 2):
            #         self.register()
                
            #     if ()

            

