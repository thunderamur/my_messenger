import time
import sys
from socket import socket, AF_INET, SOCK_STREAM

from jim.config import *
from jim.utils import dict_to_bytes, bytes_to_dict, get_message, send_message
from jim.messages import *


class MessengerClient(object):

    def __init__(self):
        self.user = {}
        self.action = JIMAction()
        self.response = JIMResponse()

    def close(self):
        self.socket.close()

    def set_user(self, account_name, status):
        self.user = {
            'account_name': account_name,
            'status': status
        }

    def parse(self, msg):
        if 'action' in msg:
            if msg['action'] == 'msg':
                print(msg['message'])
            else:
                print(msg)

    def write(self, txt):
        if txt == '<quit>':
            return False
        else:
            return self.action.msg('#room_name', self.user['account_name'], txt)

    def run(self, host, port, mode = 'r'):
        with socket(AF_INET, SOCK_STREAM) as self.socket:
            self.set_user('user-name', 'user-status')

            try:
                self.socket.connect((host, port))
            except ConnectionRefusedError:
                print('Connection Refused Error!')
                print('Check IP and port parameters.')
                return False

            while True:
                if mode == 'w':
                    txt = input('>>')
                    msg = self.write(txt)
                    if msg:
                        send_message(self.socket, msg)
                    else:
                        break
                else:
                    msg = get_message(self.socket)
                    self.parse(msg)


def main():
    if len(sys.argv) < 2:
        print('Usage: client.py <addr> [<port>] [-r, -w]')
        return -1
    host = sys.argv[1]

    port = 7777
    if len(sys.argv) == 3:
        if not sys.argv[2].startswith('-'):
            port = int(sys.argv[2])

    mode = 'r'
    if '-w' in sys.argv:
        mode = 'w'

    client = MessengerClient()
    client.run(host, port, mode)


if __name__ == '__main__':
    main()
    input()
