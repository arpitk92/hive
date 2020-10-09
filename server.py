import select
import socket
import sys

from utils import JSON


class Server:

    def __init__(self):
        self.json = JSON()
        self.HeaderLength = self.json.header_length
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.json.server_host, self.json.server_port))
        self.server_socket.listen()
        self.sockets_list = [self.server_socket]

    def receive_incoming_transmission(self, client_socket):
        try:
            header = client_socket.recv(self.HeaderLength)
            if not len(header):
                return False
            msg_len = int(header.decode("utf-8").strip())
            return {"header": header, "data": client_socket.recv(msg_len)}
        except:
            return False


def run():
    clients = {}
    print(f"Starting Mainframe")
    server = Server()
    while True:
        read_sockets, _, excep_sockets = select.select(server.sockets_list, [], server.sockets_list)

        for used_socket in read_sockets:
            if used_socket == server.server_socket:
                client_socket, client_addr = server.server_socket.accept()
                receiver = server.receive_incoming_transmission(client_socket)

                if not receiver:
                    continue
                server.sockets_list.append(client_socket)
                clients[client_socket] = receiver
                print(
                    f"Link connected from {client_addr[0]}:{client_addr[1]} | username:{receiver['data'].decode('utf-8')}")

            else:
                msg = server.receive_incoming_transmission(used_socket)
                if not msg:
                    print(f"Link closed from {clients[used_socket]['data'].decode('utf-8')}")
                    server.sockets_list.remove(used_socket)
                    del clients[used_socket]
                    continue
                user = clients[used_socket]
                print(f"Receving transmission from {user['data'].decode('utf-8')}: {msg['data'].decode('utf-8')}")

                for csc in clients:
                    if csc != used_socket:
                        csc.send(user['header'] + user['data'] + msg['header'] + msg['data'])
        for notified_socket in excep_sockets:
            server.sockets_list.remove(notified_socket)
            del clients[notified_socket]


if __name__ == '__main__':
    globals()[sys.argv[1]]()
