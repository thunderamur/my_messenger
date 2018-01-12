import sys
import select
import logging
from socket import socket, AF_INET, SOCK_STREAM

from ..jim.utils import send_message, get_message
from ..jim.core import *
from ..logger.config import logger_config
from ..logger.decorators import Log
from .chat.chat import Chat
from .repo.models import session
from .repo.repo import Repo
from .repo.errors import ContactDoesNotExist, WrongLoginOrPassword


logger_config('server', logging.DEBUG)
logger = logging.getLogger('server')
log = Log(logger)


class MyMessengerServer(object):
    """MyMessenger server"""

    def __init__(self):
        self.is_alive = False
        self.clients = []
        self.rooms = {}
        self.repo = Repo(session)
        self.repo.show_all_clients()

    @log
    def close(self):
        """Close connection."""
        self.socket.close()

    @log
    def presence_response(self, presence):
        """
        Prepare response to client on presence request
        :param presence_message: Dict of presense request
        :return: Dict of response
        """
        try:
            username = presence.user.account_name
            status = presence.user.status
        except Exception as e:
            response = JimResponse(WRONG_REQUEST, error=str(e))
            return response.to_dict()
        else:
            response = JimResponse(OK)
            return response.to_dict()

    @log
    def authenticate_response(self, authenticate):
        """
        Prepare response to client on authenticate request
        :param presence_message: Dict of authenticate request
        :return: Dict of response
        """
        try:
            username = authenticate.user.account_name
            password = authenticate.user.password
            # If user is not in DB save it
            if not self.repo.client_exists(username):
                self.repo.add_client(username, password)
            client = self.repo.get_client_by_username(username)
            if client.Password != password:
                raise WrongLoginOrPassword
        except WrongLoginOrPassword as e:
            response = JimResponse(WRONG_LOGIN_OR_PASSWORD, error=str(e))
            return response.to_dict()
        except Exception as e:
            response = JimResponse(WRONG_REQUEST, error=str(e))
            return response.to_dict()
        else:
            response = JimResponse(OK)
            return response.to_dict()

    def parse(self, requests):
        """Parser of JIM messages"""
        results = {}

        for sock in requests:
            action = Jim.from_dict(requests[sock])
            print(action.__dict__)
            if hasattr(action, ACTION):

                if action.action == GET_CONTACTS:
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
                        response = JimResponse(ACCEPTED)
                        send_message(sock, response.to_dict())
                    except ContactDoesNotExist as e:
                        response = JimResponse(WRONG_REQUEST, error='User not found')
                        send_message(sock, response.to_dict())

                elif action.action == DEL_CONTACT:
                    user_id = action.user_id
                    username = action.account_name
                    try:
                        self.repo.del_contact(username, user_id)
                        response = JimResponse(ACCEPTED)
                        send_message(sock, response.to_dict())
                    except ContactDoesNotExist as e:
                        response = JimResponse(WRONG_REQUEST, error='User not found')
                        send_message(sock, response.to_dict())

                elif action.action == PRESENCE:
                    send_message(sock, self.presence_response(action))

                elif action.action == AUTHENTICATE:
                    print(AUTHENTICATE)
                    send_message(sock, self.authenticate_response(action))

                elif action.action == MSG:
                    try:
                        self.rooms[action.to].put(sock, action)
                        send_message(sock, JimResponse(OK).to_dict())
                    except KeyError:
                        send_message(sock, JimResponse(NOT_FOUND).to_dict())

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
                    # TODO: Remove client from rooms.
                    print('Client {} {} quit'.format(sock.fileno(), sock.getpeername()))
                    send_message(sock, JimResponse(OK).to_dict())
                    self.clients.remove(sock)

            else:
                msg = 'No action in JIM message.\n' + action.__dict__
                print(msg)
                logger.warning(msg)

        for sock in self.clients:
            for room in self.rooms:
                if self.rooms[room].is_member(sock):
                    if not self.rooms[room].is_empty(sock):
                        results[sock] = self.rooms[room].get(sock)

        return results

    def client_disconnected(self, sock):
        """Output message about client disconnected event."""
        msg = 'Client {} {} disconnected'.format(sock.fileno(), sock.getpeername())
        logger.info(msg)
        print(msg)

    def read_requests(self, r_clients):
        """Read requests from clients."""
        responses = {}  # Dict of server's responses like {socket: response}
        for sock in r_clients:
            try:
                data = get_message(sock)
                responses[sock] = data
            except:
                self.client_disconnected(sock)
                self.clients.remove(sock)
        return responses

    def write_responses(self, responses, w_clients):
        """Send messages to clients."""
        for sock in w_clients:
            if sock in responses:
                try:
                    message = responses[sock]
                    send_message(sock, message.to_dict())
                except:  # Socket closed, client disconnected
                    self.client_disconnected(sock)
                    sock.close()
                    self.clients.remove(sock)

    @log
    def run(self, host, port, max_connections=5):
        """Server start."""
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
                    pass
                except KeyboardInterrupt:
                    print('\nServer stopped')
                    self.is_alive = False
                else:
                    print('Connection from: {}'.format(str(addr)))
                    self.clients.append(sock)
                finally:
                    # Check IO events.
                    wait = 0
                    r = []
                    w = []
                    try:
                        r, w, e = select.select(self.clients, self.clients, [], wait)
                    except:
                        pass  # Client disconnected

                    requests = self.read_requests(r)
                    responses = self.parse(requests)
                    self.write_responses(responses, w)


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