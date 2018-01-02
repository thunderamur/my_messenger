import sys
import logging
from socket import socket, AF_INET, SOCK_STREAM
from queue import Queue

from jim.utils import send_message, get_message
from jim.core import *

from utils import start_thread, get_hash

from client_errors import PresenceFail, AuthenticateFail

from log.logger_config import logger_config
from log.decorators import Log


logger_config('client', logging.DEBUG)
logger = logging.getLogger('client')
log = Log(logger)


class MyMessengerClient:
    """Клиент my_messenger."""

    def __init__(self, account_name, password):
        """Передаем имя пользователя и пароль."""
        self.user = JimUser(account_name, get_hash(password))
        self.socket = None
        self.room = None
        self.is_alive = False
        self.request_queue = Queue()
        self.listener_parser_thread = None
        self.contact_list = []

    @log
    def presence(self):
        """Отправить приветствие серверу и обработать ответ."""
        print('Presence... ', end='')
        presence = JimPresence(self.user)
        send_message(self.socket, presence.to_dict())
        response = get_message(self.socket)
        response = Jim.from_dict(response).to_dict()
        if response['response'] == OK:
            print('OK')
            return True

    @log
    def authenticate(self):
        """Отправить запрос аутентификации и обработать ответ."""
        print('Authenticate... ', end='')
        authenticate = JimAuthenticate(self.user)
        send_message(self.socket, authenticate.to_dict())
        response = get_message(self.socket)
        response = Jim.from_dict(response).to_dict()
        if response['response'] == OK:
            print('OK')
        else:
            print('FAIL')
            logger.warning('Authenticate FAILED')
            raise AuthenticateFail(response)

    @log
    def join_room(self, room):
        """Подключиться к комнате/чату."""
        self.room = room
        message = JimJoin(self.room)
        self.request(message)

    @log
    def leave_room(self):
        """Покупнить комнату/чат."""
        message = JimLeave(self.room)
        self.request(message)

    @log
    def add_contact(self, param):
        """Добавить контакт в список контактов."""
        message = JimAddContact(self.user.account_name, param)
        self.request(message)

    @log
    def del_contact(self, param):
        """Удалить контакт из списка контактов."""
        message = JimDelContact(self.user.account_name, param)
        self.request(message)

    @log
    def request(self, message):
        """Отправить сообщение."""
        try:
            send_message(self.socket, message.to_dict())
        except:
            logger.exception('Request to server ERROR. {}'.format(message.to_dict()))

    @staticmethod
    def response(response):
        """Обработка ответа от сервера."""
        if response.response == ACCEPTED:
            pass
        elif response.error is not None:
            print(response.error)

    @log
    def contact_list_request(self, quantity=0):
        """Запросить список контактов."""
        if quantity == 0:
            self.contact_list = []
        message = JimGetContacts(self.user.account_name, quantity)
        self.request(message)

    @log
    def contact_list_result(self, contact_list):
        """Обработка сообщения о контакте от сервера."""
        self.contact_list.append(contact_list.user_id)
        if contact_list.quantity > 0:
            self.contact_list_request(contact_list.quantity)

    @log
    def listener_parser(self):
        """Обработка сообщений."""
        while self.is_alive:
            jm = self.request_queue.get()
            if isinstance(jm, JimResponse):
                self.response(jm)
            elif isinstance(jm, JimContactList):
                self.contact_list_result(jm)

    @log
    def sender_parser(self, command):
        """Обработка команд пользователя."""
        if command == '<quit>':
            send_message(self.socket, JimQuit().to_dict())
            self.stop()
        elif command == '<leave>':
            self.leave_room()
        elif command.startswith('<list>'):
            self.contact_list_request()
        elif command.startswith('<'):
            action, param = command.split()
            if action == '<add>':
                self.add_contact(param)
            elif action == '<del>':
                self.del_contact(param)
            elif action == '<join>':
                self.join_room(param)
        else:
            send_message(self.socket, JimMessage(self.room, self.user.account_name, command).to_dict())

    @log
    def stop(self):
        """Останов клиента."""
        self.is_alive = False

    @log
    def run(self, host, port):
        """Запуск клиента."""
        self.socket = socket(AF_INET, SOCK_STREAM)

        try:
            self.socket.connect((host, port))
        except ConnectionRefusedError:
            print('Connection Refused Error!')
            print('Check IP and port parameters.')
            return False

        try:
            self.authenticate()
        except AuthenticateFail as e:
            print(e)
            sys.exit()

        self.is_alive = True

        self.listener_parser_thread = start_thread(self.listener_parser, 'listener_parser')
