import time
import sys
from socket import socket, AF_INET, SOCK_STREAM

from jim import bytes2msg, msg2bytes


class MessengerClient(object):
    def __init__(self, buffer_size = 1024):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.buffer_size = buffer_size
        self.user = {}

    def connect(self, host, port):
        try:
            self.s.connect((host, port))
        except ConnectionRefusedError:
            print('Connection Refused Error!')
            print('Check IP and port parameters.')
            return False
        self.parse()
        return True

    def close(self):
        self.s.close()

    def set_user(self, account_name, status):
        self.user = {
            'account_name': account_name,
            'status': status
        }

    def send(self, msg):
        self.s.send(msg2bytes(msg))

    def receive(self):
        return bytes2msg(self.s.recv(self.buffer_size))

    def parse(self):
        msg = self.receive()
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
                if self.parse() == 'probe':
                    self.send(self.jim_presence())
                self.parse()
                self.send(self.jim_quit())
                break  # Temporary
            self.close()
            break  # Temporary

    # Не нравятся мне методы ниже, по идее их надо вынести в отдельный класс протокола.
    # Переделаю к следующему ДЗ, сейчас не успею уже. Вообще мысль верная?
    def jim_presence(self):
        return {
            'action': 'presence',
            'time': time.time(),
            'type': 'status',
            'user': {
                'account_name': self.user['account_name'],
                'status': self.user['status']
            }
        }

    def jim_quit(self):
        return {
            'action': 'quit'
        }


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