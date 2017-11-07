import time
import sys
from socket import socket, AF_INET, SOCK_STREAM

from jim.config import *
from jim.utils import dict_to_bytes, bytes_to_dict, get_message, send_message
from jim.messages import *


class MessengerClient(object):
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.user = {}

    def connect(self, host, port):
        try:
            self.socket.connect((host, port))
        except ConnectionRefusedError:
            print('Connection Refused Error!')
            print('Check IP and port parameters.')
            return False
        msg = self.receive()
        self.parse(msg)
        return True

    def close(self):
        self.socket.close()

    def set_user(self, account_name, status):
        self.user = {
            'account_name': account_name,
            'status': status
        }

    def send(self, msg):
        send_message(self.socket, msg)

    def receive(self):
        return get_message(self.socket)

    def parse(self, msg):
        print(msg)
        if 'action' in msg:
            return msg['action']
        return False

    def run(self, host, port):
        while True:
            self.set_user('user name', 'user status')
            if not self.connect(host, port):
                print('Method connect(host, port) returned error')
                return False
            while True:
                msg = self.receive()
                if self.parse(msg) == 'probe':
                    account_name = self.user['account_name']
                    status = self.user['status']
                    self.send(jim_presence(account_name, status))
                msg = self.receive()
                self.parse(msg)
                self.send(jim_quit())
                break  # Temporary
            self.close()
            break  # Temporary


def main():
    if len(sys.argv) < 2:
        print('Usage: client.py <addr> [<port>]')
        return -1
    host = sys.argv[1]
    if len(sys.argv) == 3:
        port = int(sys.argv[2])
    else:
        port = 7777

    client = MessengerClient()
    client.run(host, port)


if __name__ == '__main__':
    main()