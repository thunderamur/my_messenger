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
        self.client = MyMessengerClient(account_name, password)
        self.client_thread = None
        self.listener = None
        self.listener_thread = None

    def stop(self):
        self.listener.stop()

    def run(self, host, port):
        self.client_thread = start_thread(self.client.run, 'Client', host, port)
        while not self.client.is_alive:
            pass
        self.listener = ConsoleReceiver(self.client.socket, self.client.request_queue)
        self.listener_thread = start_thread(self.listener.poll, 'Listener')
        self.sender()
        self.client_thread.join()
        self.listener_thread.join()

    def sender(self):
        self.client.join_room('default_room')
        while self.client.is_alive:
            command = input()
            self.client.sender_parser(command)
        self.stop()


if __name__ == '__main__':
    app_start(MyMessengerClientConsole)