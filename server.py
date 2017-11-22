#import time
import sys
import select
from socket import socket, AF_INET, SOCK_STREAM

# from jim.config import *
from jim.utils import send_jim, get_jim
from jim.core import *

from chat.chat import Chat

# import logging
from log.server_log_config import server_logger
from log.decorators import Log

log = Log(server_logger)


class MessengerServer(object):

    def __init__(self):
        self.clients = []

        # {'room_name': Chat()}
        self.rooms = {}

    def close(self):
        self.socket.close()

    @log
    def parse(self, requests):
        results = {}
        message = False

        for sock in requests:
            data = requests[sock]
            print(data.__dict__)

            if hasattr(data, ACTION):

                if data.action == PRESENCE:
                    send_jim(sock, JimResponse(OK))

                elif data.action == MSG:
                    self.rooms[data.to].put(sock, data)
                    send_jim(sock, JimResponse(OK))

                elif data.action == JOIN:
                    if data.room not in self.rooms:
                        self.rooms.update({data.room: Chat()})
                    self.rooms[data.room].join(sock)
                    send_jim(sock, JimResponse(ACCEPTED))

                elif data.action == LEAVE:
                    if data.room in self.rooms:
                        self.rooms[data.room].leave(sock)
                        send_jim(sock, JimResponse(GONE))
                    else:
                        send_jim(sock, JimResponse(NOT_FOUND))

                elif data.action == QUIT:
                    #
                    # !!!! дописать удаление клиента из комнат
                    #
                    print('Client {} {} quit'.format(sock.fileno(), sock.getpeername()))
                    self.clients.remove(sock)
            else:
                print('!!!!!!!!!!!!! NO ACTION !!!!!!!!!!!!!!!!')
                print(data.__dict__)

        for sock in self.clients:
            if sock not in results:
                for room in self.rooms:
                    if self.rooms[room].is_member(sock):
                        if not self.rooms[room].is_empty(sock):
                            results[sock] = self.rooms[room].get(sock)

        return results

    def read_requests(self, r_clients):
        responses = {}  # Словарь ответов сервера вида {сокет: запрос}
        for sock in r_clients:
            try:
                data = get_jim(sock)
                responses[sock] = data
            except:
                print('Client {} {} disconnected'.format(sock.fileno(), sock.getpeername()))
                self.clients.remove(sock)
        return responses

    def write_responses(self, requests, w_clients):
        for sock in w_clients:
            if sock in requests:
                try:
                    data = requests[sock]
                    send_jim(sock, data)
                except:  # Сокет недоступен, клиент отключился
                    print('Client {} {} disconnected'.format(sock.fileno(), sock.getpeername()))
                    sock.close()
                    self.clients.remove(sock)

    def run(self, host, port, max_connections = 5):
        with socket(AF_INET, SOCK_STREAM) as self.socket:
            self.socket.bind((host, port))
            self.socket.listen(max_connections)
            self.socket.settimeout(0.2)

            while True:
                try:
                    sock, addr = self.socket.accept()
                except OSError as e:
                    pass  # timeout вышел
                else:
                    print('Connection from: {}'.format(str(addr)))
                    self.clients.append(sock)
                finally:
                    # Проверить наличие событий ввода-вывода
                    wait = 0
                    r = []
                    w = []
                    try:
                        r, w, e = select.select(self.clients, self.clients, [], wait)
                    except:
                        pass  # Ничего не делать, если какой-то клиент отключился

                    requests = self.read_requests(r)  # Сохраним запросы клиентов
                    responses = self.parse(requests)
                    self.write_responses(responses, w)  # Выполним отправку ответов клиентам


def main():
    if '-a' in sys.argv:
        host = sys.argv[sys.argv.index('-a') + 1]
    else:
        host = '0.0.0.0'
    if '-p' in sys.argv:
        port = int(sys.argv[sys.argv.index('-p') + 1])
    else:
        port = 7777

    srv = MessengerServer()
    srv.run(host, port)


if __name__ == '__main__':
    main()