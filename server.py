import time
import sys
from socket import socket, AF_INET, SOCK_STREAM

from jim import bytes2msg, msg2bytes


responses = {
    200: 'ok',
    202: 'accepted'
}


def gen_response(code):
    response = {
        'response': code,
        'time': time.time()
    }
    if code < 299:
        response.update({'alert': responses[code]})

    return response


class MessengerServer(object):
    def __init__(self, host, port, max_connections = 5, buffer_size = 1024):
        self.buffer_size = buffer_size
        self.clients = {}

        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.bind((host, port))
        self.s.listen(max_connections)

    def run(self):
        while True:
            client, addr = self.s.accept()
            self.clients.update({addr: client})
            print('Connection from: {}'.format(str(addr)))
            self.send(addr, gen_response(200))
            self.send(addr, self.jim_probe())
            while True:
                if self.parse(addr) == 'quit':
                    break
            client.close()
            break  # Temporary
        self.close()

    def close(self):
        self.s.close()

    def send(self, addr, msg):
        self.clients[addr].send(msg2bytes(msg))

    def receive(self, addr):
        return bytes2msg(self.clients[addr].recv(self.buffer_size))

    def parse(self, addr):
        msg = self.receive(addr)
        print(msg)
        self.send(addr, gen_response(202))
        if 'action' in msg:
            return msg['action']
        return False

    def jim_probe(self):
        return {
            'action': 'probe',
            'time': time.time()
        }


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