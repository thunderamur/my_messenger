import sys
import logging
from jim.core import *

from handlers import ConsoleReceiver
from utils import start_thread
from client_core import MyMessengerClient

from log.logger_config import logger_config
from log.decorators import Log


logger_config('client', logging.DEBUG)
logger = logging.getLogger('client')
log = Log(logger)


class MyMessengerClientConsole:
    """Клиент my_messenger."""
    def __init__(self, account_name, password):
        self.client_core = MyMessengerClient(account_name, password)
        self.client_thread = None
        self.listener = None
        self.listener_thread = None

    def stop(self):
        self.listener.stop()

    def run(self, host, port):
        self.client_thread = start_thread(self.client_core.run, 'Client', host, port)
        while not self.client_core.is_alive:
            pass
        self.listener = ConsoleReceiver(self.client_core.socket, self.client_core.request_queue)
        self.listener_thread = start_thread(self.listener.poll, 'Listener')
        self.sender()
        self.client_thread.join()
        self.listener_thread.join()

    def sender_parser(self, command):
        """Обработка команд пользователя."""
        if command == '<quit>':
            self.client_core.request(JimQuit())
            self.client_core.stop()
        elif command == '<leave>':
            self.client_core.leave_room()
        elif command.startswith('<list>'):
            self.client_core.contact_list_request()
        elif command.startswith('<'):
            action, param = command.split()
            if action == '<add>':
                self.client_core.add_contact(param)
            elif action == '<del>':
                self.client_core.del_contact(param)
            elif action == '<join>':
                self.client_core.join_room(param)
        else:
            jm = JimMessage(self.client_core.room, self.client_core.user.account_name, command)
            self.client_core.request(jm)

    def sender(self):
        self.client_core.join_room('default_room')
        while self.client_core.is_alive:
            command = input()
            self.sender_parser(command)
        self.stop()


if __name__ == '__main__':
    host = None
    port = None
    name = None
    password = None
    if len(sys.argv) >= 4:
        host = sys.argv[1]
        port = 7777

        for option in sys.argv[2:]:
            key, val = option.split('=')
            if key == '-port':
                port = val
            elif key == '-user':
                name = val
            elif key == '-pass':
                password = val

    if host and port and name and password:
        client = MyMessengerClientConsole(name, password)
        client.run(host, port)
    else:
        print('Usage: client.py <addr> [-port=<port>] -user=<user> -pass=<password>')
