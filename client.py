import time
import sys
#import dis
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from queue import Queue

from jim.utils import send_message, get_message
from jim.core import *

from handlers import ConsoleReceiver
from utils import start_thread, get_hash

from client_errors import PresenceFail, AuthenticateFail


class MessengerClient:
    def __init__(self, account_name, password):
        self.user = JimUser(account_name, get_hash(password))
        self.socket = None
        self.room = None
        self.is_alive = False
        self.request_queue = Queue()
        self.listener = None

    def presence(self):
        print('Presence... ', end='')
        presence = JimPresence(self.user)
        send_message(self.socket, presence.to_dict())
        response = get_message(self.socket)
        response = Jim.from_dict(response).to_dict()
        if response['response'] == OK:
            print('OK')
            return True

    def authenticate(self):
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
        self.room = room
        message = JimJoin(self.room)
        self.request(message)

    def leave_room(self):
        message = JimLeave(self.room)
        self.request(message)

    def add_contact(self, param):
        message = JimAddContact(self.user.account_name, param)
        self.request(message)

    def del_contact(self, param):
        message = JimDelContact(self.user.account_name, param)
        self.request(message)

    def request(self, message):
        send_message(self.socket, message.to_dict())

    @staticmethod
    def response(response):
        if response.response == ACCEPTED:
            pass
        elif response.error is not None:
            print(response.error)

    def contact_list_request(self, quantity=0):
        message = JimGetContacts(self.user.account_name, quantity)
        self.request(message)

    def contact_list_result(self, contact_list):
        if contact_list.quantity > 0:
            self.contact_list_request(contact_list.quantity)

    def parser(self):
        while self.is_alive:
            jm = self.request_queue.get()
            if isinstance(jm, JimResponse):
                self.response(jm)
            elif isinstance(jm, JimContactList):
                self.contact_list_result(jm)

    def sender(self):
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
        self.listener = ConsoleReceiver(self.socket, self.request_queue)
        return start_thread(self.listener.poll, 'Listener')

    def start_sender(self):
        return start_thread(self.sender, 'Sender')

    def start_parser(self):
        return start_thread(self.parser, 'Parser')

    def stop(self):
        self.is_alive = False
        self.listener.stop()

    def run(self, host, port):
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


def main():
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
            elif key == '-name':
                name = val
            elif key == '-password':
                password = val

    if host and port and name and password:
        client = MessengerClient(name, password)
        client.run(host, port)
    else:
        print('Usage: client.py <addr> [-port=<port>] -name=<name> -password=<password>')
        return -1


if __name__ == '__main__':
    main()