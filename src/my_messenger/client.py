import sys
from socket import socket, AF_INET, SOCK_STREAM
from queue import Queue

from jim.utils import send_message, get_message
from jim.core import *

from handlers import ConsoleReceiver
from utils import start_thread, get_hash, app_start

from client_errors import PresenceFail, AuthenticateFail


class MessengerClient:
    """Клиент my_messenger."""

    def __init__(self, account_name, password):
        """Передаем имя пользователя и пароль."""
        self.user = JimUser(account_name, get_hash(password))
        self.socket = None
        self.room = None
        self.is_alive = False
        self.request_queue = Queue()
        self.listener = None

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
            raise AuthenticateFail(response)

    def join_room(self, room):
        """Подключиться к комнате/чату."""
        self.room = room
        message = JimJoin(self.room)
        self.request(message)

    def leave_room(self):
        """Покупнить комнату/чат."""
        message = JimLeave(self.room)
        self.request(message)

    def add_contact(self, param):
        """Добавить контакт в список контактов."""
        message = JimAddContact(self.user.account_name, param)
        self.request(message)

    def del_contact(self, param):
        """Удалить контакт из списка контактов."""
        message = JimDelContact(self.user.account_name, param)
        self.request(message)

    def request(self, message):
        """Отправить сообщение."""
        send_message(self.socket, message.to_dict())

    @staticmethod
    def response(response):
        """Обработка ответа от сервера."""
        if response.response == ACCEPTED:
            pass
        elif response.error is not None:
            print(response.error)

    def contact_list_request(self, quantity=0):
        """Запросить список контактов."""
        message = JimGetContacts(self.user.account_name, quantity)
        self.request(message)

    def contact_list_result(self, contact_list):
        """Обработка сообщения о контакте от сервера."""
        if contact_list.quantity > 0:
            self.contact_list_request(contact_list.quantity)

    def parser(self):
        """Обработка сообщений."""
        while self.is_alive:
            jm = self.request_queue.get()
            if isinstance(jm, JimResponse):
                self.response(jm)
            elif isinstance(jm, JimContactList):
                self.contact_list_result(jm)

    def sender(self):
        """Метод, запускаемый в отдельном потоке для отправки сообщений серверу."""
        self.join_room('default_room')
        while self.is_alive:
            text = input()
            if text == '<quit>':
                send_message(self.socket, JimQuit().to_dict())
                self.stop()

            elif text == '<leave>':
                self.leave_room()
            elif text.startswith('<list>'):
                self.contact_list_request()
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

    def start_listener(self):
        """Создание объекта ConsoleReceiver и запуск прослушки (poll()) в отдельном потоке."""
        self.listener = ConsoleReceiver(self.socket, self.request_queue)
        return start_thread(self.listener.poll, 'Listener')

    def start_sender(self):
        """Запуск sender() в отдельном потоке."""
        return start_thread(self.sender, 'Sender')

    def start_parser(self):
        """Запуск parser() в отдельном потоке."""
        return start_thread(self.parser, 'Parser')

    def stop(self):
        """Останов клиента."""
        self.is_alive = False
        self.listener.stop()

    def run(self, host, port):
        """Запуск клиента."""
        with socket(AF_INET, SOCK_STREAM) as sock:
            self.socket = sock

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

            lt = self.start_listener()
            st = self.start_sender()
            pt = self.start_parser()

            if lt:
                lt.join()
            st.join()
            pt.join()


if __name__ == '__main__':
    app_start(MessengerClient)