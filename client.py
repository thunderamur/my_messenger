# import time
import sys
import dis
from socket import socket, AF_INET, SOCK_STREAM

# from jim.config import *
from jim.utils import send_message, get_message
from jim.core import *


# class ClientVerifier(type):
#     """
#     4. *Реализовать метакласс ClientVerifier, выполняющий базовую проверку класса Клиент
#         (для некоторых проверок уместно использовать модуль dis):
#
#         отсутствие вызовов accept и listen для сокетов
#         использование сокетов для работы по TCP
#         отсутствие создания сокетов на уровне классов, т.е. отсутствие конструкций вида:
#
#     class Client:
#         s = socket()
#         ...
#     """
#     def __init__(self, clsname, bases, clsdict):
#         for key, value in clsdict.items():
#             # Пропустить специальные и частные методы
#             if key.startswith('__'): continue
#
#             # Пропустить любые невызываемые объекты
#             if not hasattr(value, '__call__'): continue
#
#             # Проверить наличие строки документирования
#             # if not getattr(value, '__doc__'):
#             #     raise TypeError('Метод {} должен иметь строку документации'.format(key))
#
#             print(key, dis.code_info(value), end='\n\n\n\n\n')
#
#         type.__init__(self, clsname, bases, clsdict)


class User:
    def __init__(self, account_name, status=''):
        self.account_name = account_name
        self.status = status

# class MessengerClient(metaclass=ClientVerifier):
class MessengerClient:
    """
    Класс Клиент - класс, реализующий клиентскую часть системы.
    """
    def __init__(self, account_name):
        self.user = User(account_name)
        self.socket = None
        self.room = None

    def presence(self):
        presence = JimPresence(self.user.account_name)
        send_message(self.socket, presence.to_dict())
        response = get_message(self.socket)
        response = Jim.from_dict(response).to_dict()
        if response['response'] == OK:
            return True

    def join_room(self, room):
        self.room = room
        message = JimJoin(self.room)
        self.command(message)

    def leave_room(self):
        message = JimLeave(self.room)
        self.command(message)

    def add_contact(self, param):
        message = JimAddContact(self.user.account_name, param)
        self.command(message)

    def del_contact(self, param):
        message = JimDelContact(self.user.account_name, param)
        self.command(message)

    def command(self, message):
        send_message(self.socket, message.to_dict())
        response = get_message(self.socket)
        response = Jim.from_dict(response)
        if response.response == ACCEPTED:
            print('Успешно')
        else:
            print(response.error)

    def show_list(self):
        # запрос на список контактов
        jimmessage = JimGetContacts(self.user.account_name)
        # отправляем
        send_message(self.socket, jimmessage.to_dict())
        # получаем ответ
        response = get_message(self.socket)

        # приводим ответ к ответу сервера
        response = Jim.from_dict(response)
        # там лежит количество контактов
        quantity = response.quantity
        # делаем цикл и получаем каждый контакт по отдельности
        print('У вас ', quantity, 'друзей')
        print('Вот они:')
        for i in range(quantity):
            message = get_message(self.socket)
            message = Jim.from_dict(message)
            print(message.user_id)

    def parse(self, msg):
        print(msg)
        # if 'action' in msg:
        #     if msg['action'] == 'msg':
        #         print(msg['message'])
        #     else:
        #         print(msg)

    def run(self, host, port, mode = 'r'):
        with socket(AF_INET, SOCK_STREAM) as sock:
            self.socket = sock

            try:
                self.socket.connect((host, port))
            except ConnectionRefusedError:
                print('Connection Refused Error!')
                print('Check IP and port parameters.')
                return False

            if not self.presence():
                sys.exit()

            self.join_room('#room_name')

            if mode == 'w':
                while True:
                    text = input('>> ')
                    if text == '<quit>':
                        send_message(self.socket, JimQuit().to_dict())
                        break
                    elif text == '<leave>':
                        self.leave_room()
                    elif text.startswith('<list>'):
                        self.show_list()
                    elif text.startswith('<'):
                        command, param = text.split()
                        if command == '<add>':
                            self.add_contact(param)
                        elif command == '<del>':
                            self.del_contact(param)
                        elif command == '<join>':
                            self.join_room(param)
                    else:
                        send_message(self.socket, JimMessage(self.room, self.user.account_name, text).to_dict())

            else:
                while True:
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

    if mode == 'w':
        client = MessengerClient('Vasya')
    else:
        client = MessengerClient('Petya')
    client.run(host, port, mode)


if __name__ == '__main__':
    main()
    input()
