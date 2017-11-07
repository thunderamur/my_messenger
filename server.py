import time
import sys
from socket import socket, AF_INET, SOCK_STREAM

from jim.config import *
from jim.utils import dict_to_bytes, bytes_to_dict, get_message, send_message
from jim.messages import *


class MessengerServer(object):
    def __init__(self, host, port, max_connections = 5):
        self.clients = {}

        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(max_connections)

    def run(self):
        while True:
            client, addr = self.socket.accept()
            self.clients.update({addr: client})
            print('Connection from: {}'.format(str(addr)))
            self.send(addr, jim_response(200))
            self.send(addr, jim_probe())
            while True:
                if self.parse(addr) == 'quit':
                    break
            client.close()
            break  # Temporary
        self.close()

    def close(self):
        self.socket.close()

    def send(self, addr, msg):
        send_message(self.clients[addr], msg)

    def receive(self, addr):
        return get_message(self.clients[addr])

    def parse(self, addr):
        msg = self.receive(addr)
        print(msg)
        self.send(addr, jim_response(202))
        if 'action' in msg:
            return msg['action']
        return False


def main():
    if '-a' in sys.argv:
        host = sys.argv[sys.argv.index('-a') + 1]
    else:
        host = '0.0.0.0'
    if '-p' in sys.argv:
        port = int(sys.argv[sys.argv.index('-p') + 1])
    else:
        port = 7777

    srv = MessengerServer(host, port)
    srv.run()


if __name__ == '__main__':
    main()