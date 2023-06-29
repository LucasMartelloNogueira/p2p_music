class Connection:
    def __init__(self, server_ip, server_port, client_ip, client_port, client_tcp_port) -> None:
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_ip = client_ip
        self.client_port = client_port
        self.client_tcp_port = client_tcp_port
