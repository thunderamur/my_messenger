import time

from .config import *


class JIMAction(object):
    """
    Класс JIMСообщение - класс, реализующий сообщение (msg) по протоколу JIM.
    """
    def presence(self, account_name, status):
        return {
            'action': 'presence',
            'time': time.time(),
            'type': 'status',
            'user': {
                'account_name': account_name,
                'status': status
            }
        }

    def probe(self):
        return {
            'action': 'probe',
            'time': time.time()
        }

    def msg(self, dest, src, message):
        return {
            'action': 'msg',
            'time': time.time(),
            'to': dest,
            'from': src,
            'message': message
        }

    def quit(self):
        return {
            'action': 'quit',
            'time': time.time()
        }

    def authenticate(self, account_name, password):
        return {
            'action': 'authenticate',
            'time': time.time(),
            'user': {
                'account_name': account_name,
                'password': password
            }
        }

    def join(self, room):
        return {
            'action': 'join',
            'time': time.time(),
            'room': room
        }

    def leave(self, room):
        return {
            'action': 'leave',
            'time': time.time(),
            'room': room
        }


class JIMResponse(object):
    """
    Класс JIMОтвет - класс, реализующий ответ (response) по протоколу JIM.
    """
    def response(self, code, message=''):
        return {
            'response': code,
            'time': time.time(),
            'alert' if code < 299 else 'error': message
        }
