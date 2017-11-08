import time

from .config import *


def jim_presence(account_name, status):
    return {
        'action': 'presence',
        'time': time.time(),
        'type': 'status',
        'user': {
            'account_name': account_name,
            'status': status
        }
    }


def jim_quit():
    return {
        'action': 'quit'
    }


def jim_probe():
    return {
        'action': 'probe',
        'time': time.time()
    }


def jim_response(code):
    response = {
        'response': code,
        'time': time.time()
    }
    if code < 299:
        response.update({'alert': RESPONSE_CODES[code]})
    return response


def jim_msg(dest, src, message):
    return {
        'action': 'msg',
        'time': time.time(),
        'to': dest,
        'from': src,
        'message': message
    }
