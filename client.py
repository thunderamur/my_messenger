# import time
import sys
import dis
from socket import socket, AF_INET, SOCK_STREAM

# from jim.config import *
from jim.utils import send_jim, get_jim
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



# class MessengerClient(metaclass=ClientVerifier):
class MessengerClient():
    """
    Класс Клиент - класс, реализующий клиентскую часть системы.
    """
    def __init__(self):
        self.user = {}

    def close(self):
        self.socket.close()

    def set_user(self, account_name, status):
        self.user = {
            'account_name': account_name,
            'status': status
        }

    def parse(self, msg):
        print(msg.__dict__)
        # if 'action' in msg:
        #     if msg['action'] == 'msg':
        #         print(msg['message'])
        #     else:
        #         print(msg)

    def write(self, txt):
        if txt == '<quit>':
            return False
        else:
            return JimMessage('#room_name', self.user['account_name'], txt)

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
                        send_jim(self.socket, msg)
                    else:
                        break
                else:
                    msg = get_jim(self.socket)
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
