import sys
import select
import logging
from socket import socket, AF_INET, SOCK_STREAM

from jim.utils import send_message, get_message
from jim.core import *

from chat.chat import Chat

from repo.server_models import session
from repo.server_repo import Repo
from repo.server_errors import ContactDoesNotExist, WrongLoginOrPassword

from log.logger_config import logger_config
from log.decorators import Log


logger_config('server', logging.DEBUG)
logger = logging.getLogger('server')
log = Log(logger)


class MyMessengerServer(object):
    """Сервер my_messenger"""

    def __init__(self):
        self.is_alive = False
        self.clients = []
        # {'room_name': Chat()}
        self.rooms = {}
        self.repo = Repo(session)
        self.repo.show_all_clients()

    @log
    def close(self):
        """Закрыть соединение."""
        self.socket.close()

    @log
    def presence_response(self, presence):
        """
        Формирование ответа клиенту
        :param presence_message: Словарь presence запроса
        :return: Словарь ответа
        """
        # Делаем проверки
        try:
            username = presence.user.account_name
            status = presence.user.status
            #
            # Добавить ведение статуса пользователя
            #
        except Exception as e:
            # Шлем код ошибки
            response = JimResponse(WRONG_REQUEST, error=str(e))
            return response.to_dict()
        else:
            # Если всё хорошо шлем ОК
            response = JimResponse(OK)
            return response.to_dict()

    @log
    def authenticate_response(self, authenticate):
        """
        Формирование ответа клиенту
        :param presence_message: Словарь presence запроса
        :return: Словарь ответа
        """
        # Делаем проверки
        try:
            username = authenticate.user.account_name
            password = authenticate.user.password
            # сохраняем пользователя в базу если его там еще нет
            if not self.repo.client_exists(username):
                self.repo.add_client(username, password)
            client = self.repo.get_client_by_username(username)
            if client.Password != password:
                raise WrongLoginOrPassword
        except WrongLoginOrPassword as e:
            response = JimResponse(WRONG_LOGIN_OR_PASSWORD, error=str(e))
            return response.to_dict()
        except Exception as e:
            # Шлем код ошибки
            response = JimResponse(WRONG_REQUEST, error=str(e))
            return response.to_dict()
        else:
            # Если всё хорошо шлем ОК
            response = JimResponse(OK)
            return response.to_dict()

    def parse(self, requests):
        """Парсер сообщений."""
        results = {}

        for sock in requests:
            action = Jim.from_dict(requests[sock])
            print(action.__dict__)

            if hasattr(action, ACTION):

                if action.action == GET_CONTACTS:
                    # Добавить обработку пустого списка контактов
                    contacts = self.repo.get_contacts(action.account_name)
                    if action.quantity == 0:
                        index = 0
                    else:
                        index = len(contacts) - action.quantity
                    quantity = len(contacts) - index - 1
                    if len(contacts) > 0:
                        name = contacts[index].Name
                    else:
                        name = ''
                    message = JimContactList(name, quantity)
                    print(message.to_dict())
                    send_message(sock, message.to_dict())

                elif action.action == ADD_CONTACT:
                    user_id = action.user_id
                    username = action.account_name
                    try:
                        self.repo.add_contact(username, user_id)
                        # шлем удачный ответ
                        response = JimResponse(ACCEPTED)
                        # Отправляем
                        send_message(sock, response.to_dict())
                    except ContactDoesNotExist as e:
                        # формируем ошибку, такого контакта нет
                        response = JimResponse(WRONG_REQUEST, error='Такого контакта нет')
                        # Отправляем
                        send_message(sock, response.to_dict())

                elif action.action == DEL_CONTACT:
                    user_id = action.user_id
                    username = action.account_name
                    try:
                        self.repo.del_contact(username, user_id)
                        # шлем удачный ответ
                        response = JimResponse(ACCEPTED)
                        # Отправляем
                        send_message(sock, response.to_dict())
                    except ContactDoesNotExist as e:
                        # формируем ошибку, такого контакта нет
                        response = JimResponse(WRONG_REQUEST, error='Такого контакта нет')
                        # Отправляем
                        send_message(sock, response.to_dict())

                elif action.action == PRESENCE:
                    send_message(sock, self.presence_response(action))

                elif action.action == AUTHENTICATE:
                    print(AUTHENTICATE)
                    send_message(sock, self.authenticate_response(action))

                elif action.action == MSG:
                    self.rooms[action.to].put(sock, action)
                    send_message(sock, JimResponse(OK).to_dict())

                elif action.action == JOIN:
                    if action.room not in self.rooms:
                        self.rooms.update({action.room: Chat()})
                    self.rooms[action.room].join(sock)
                    send_message(sock, JimResponse(ACCEPTED).to_dict())

                elif action.action == LEAVE:
                    if action.room in self.rooms:
                        self.rooms[action.room].leave(sock)
                        send_message(sock, JimResponse(GONE).to_dict())
                    else:
                        send_message(sock, JimResponse(NOT_FOUND).to_dict())

                elif action.action == QUIT:
                    #
                    # !!!! дописать удаление клиента из комнат
                    #
                    print('Client {} {} quit'.format(sock.fileno(), sock.getpeername()))
                    send_message(sock, JimResponse(OK).to_dict())
                    self.clients.remove(sock)

            else:
                print('!!!!!!!!!!!!! NO ACTION !!!!!!!!!!!!!!!!')
                print(action.__dict__)

        for sock in self.clients:
            for room in self.rooms:
                if self.rooms[room].is_member(sock):
                    if not self.rooms[room].is_empty(sock):
                        results[sock] = self.rooms[room].get(sock)

        return results

    def client_disconnected(self, sock):
        """Клиент отключился."""
        msg = 'Client {} {} disconnected'.format(sock.fileno(), sock.getpeername())
        logger.info(msg)
        print(msg)

    def read_requests(self, r_clients):
        """Читаем запросы от клиентов."""
        responses = {}  # Словарь ответов сервера вида {сокет: запрос}
        for sock in r_clients:
            try:
                data = get_message(sock)
                responses[sock] = data
            except:
                self.client_disconnected(sock)
                self.clients.remove(sock)
        return responses

    def write_responses(self, responses, w_clients):
        """Отправляем сообщения клиентам."""
        for sock in w_clients:
            if sock in responses:
                try:
                    message = responses[sock]
                    send_message(sock, message.to_dict())
                except:  # Сокет недоступен, клиент отключился
                    self.client_disconnected(sock)
                    sock.close()
                    self.clients.remove(sock)

    @log
    def run(self, host, port, max_connections=5):
        """Запуск сервера."""
        with socket(AF_INET, SOCK_STREAM) as sock:
            self.socket = sock
            self.socket.bind((host, port))
            self.socket.listen(max_connections)
            self.socket.settimeout(0.2)
            self.is_alive = True

            while self.is_alive:
                try:
                    sock, addr = self.socket.accept()
                except OSError as e:
                    pass  # timeout вышел
                except KeyboardInterrupt:
                    print('\nEXIT')
                    self.is_alive = False
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


@log
def main():
    if '-a' in sys.argv:
        host = sys.argv[sys.argv.index('-a') + 1]
    else:
        host = '0.0.0.0'
    if '-p' in sys.argv:
        port = int(sys.argv[sys.argv.index('-p') + 1])
    else:
        port = 7777

    srv = MyMessengerServer()
    srv.run(host, port)


if __name__ == '__main__':
    main()