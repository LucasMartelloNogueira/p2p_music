from src.entities.Server import Server
from src.entities.Client import Client

import sys

args_dict = dict()

for arg in sys.argv[1:]:
    key, value = arg.split("=")
    args_dict[key] = value

if __name__ == "__main__":
    if args_dict["type"] == "server":
        server = Server()

    if args_dict["type"] == "client":
        port = args_dict.get("port", None)
        client = Client(connection_port=port)