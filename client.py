import errno
import socket
import sys

from utils import JSON


class Client:
    def __init__(self):
        self.json = JSON()
        self.HeaderLength = self.json.header_length
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.client_socket.connect((self.json.server_host, self.json.server_port))
        self.client_socket.setblocking(False)

        self.my_username = self.new_user()

    def new_user(self):
        my_username = input("Enter Username: ")
        print(f"Welcome to the H.I.V.E, {my_username}")
        username = my_username.encode("utf-8")
        username_header = f"{len(username):<{self.HeaderLength}}".encode("utf-8")

        self.client_socket.send(username_header + username)

        return my_username


def run():
    client = Client()

    while True:
        message = input(f"{client.my_username} > ")
        if message:
            message = message.encode("utf-8")
            message_header = f"{len(message):<{client.HeaderLength}}".encode("utf-8")
            client.client_socket.send(message_header + message)

        try:
            while True:
                # receive transmissions
                username_header = client.client_socket.recv(client.HeaderLength)
                if not len(username_header):
                    print("Transmission lost")
                    sys.exit()
                username_length = int(username_header.decode("utf-8").strip())
                username = client.client_socket.recv(username_length).decode("utf-8")

                message_header = client.client_socket.recv(client.HeaderLength)
                message_length = int(message_header.decode("utf-8").strip())
                message = client.client_socket.recv(message_length).decode("utf-8")
                print(f"{username} > {message}")
        except IOError as e:
            if e.errno != errno.EAGAIN or e.errno != errno.EWOULDBLOCK:
                print("IO Error: ", str(e))
                sys.exit()
            continue
        except Exception as e:
            print("Error: ", str(e))
            sys.exit()


if __name__ == '__main__':
    globals()[sys.argv[1]]()
