import time
import sys
from socket import socket, AF_INET, SOCK_STREAM
from queue import Queue

from jim.utils import send_message, get_message
from jim.core import *

from handlers import ConsoleReceiver
from utils import start_thread, get_hash, app_start
from client_errors import PresenceFail, AuthenticateFail
from client_core import MyMessengerClient


class MyMessengerClientConsole(MyMessengerClient):
    """Клиент my_messenger."""
    def __init__(self, account_name, password):
        super().__init__(account_name, password)
        self.listener = None
        self.listener_thread = None
        self.sender_thread = None

    def stop(self):
        """Расширение метода родителя. Останов клиента."""
        super().stop()
        self.listener.stop()

    def run(self, host, port):
        """Расширение метода родителя. Запуск клиента."""
        # Запускается поток listener_parser
        super().run(host, port)
        # Запускаем прием сообщений
        self.listener = ConsoleReceiver(self.socket, self.request_queue)
        self.listener_thread = start_thread(self.listener.poll, 'Listener')
        # Запускаем отправку сообщений
        self.sender_thread = start_thread(self.sender, 'Sender')

        self.listener_parser_thread.join()
        self.listener_thread.join()
        self.sender_thread.join()

    def sender(self):
        """Метод, запускаемый в отдельном потоке для отправки сообщений серверу."""
        self.join_room('default_room')
        while self.is_alive:
            command = input()
            self.sender_parser(command)


if __name__ == '__main__':
    app_start(MyMessengerClientConsole)