import time
import sys
import logging
from socket import socket, AF_INET, SOCK_STREAM
from queue import Queue

from jim.utils import send_message, get_message
from jim.core import *

from handlers import ConsoleReceiver
from utils import start_thread, get_hash, app_start
from client_errors import PresenceFail, AuthenticateFail
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
            send_message(self.client_core.socket, JimQuit().to_dict())
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
            send_message(self.client_core.socket, JimMessage(self.client_core.room, self.client_core.user.account_name, command).to_dict())

    def sender(self):
        self.client_core.join_room('default_room')
        while self.client_core.is_alive:
            command = input()
            self.sender_parser(command)
        self.stop()


if __name__ == '__main__':
    app_start(MyMessengerClientConsole)