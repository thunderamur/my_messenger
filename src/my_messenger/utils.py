import sys
import hmac
import time
import select
from threading import Thread

from jim.config import ENCODING

HASH_SALT = b'MPwWyL4K7Av5q98f'


def start_thread(target, name, *args):
    """Запуск потока."""
    t = Thread(target=target, args=args)
    t.name = name
    t.daemon = True
    t.start()
    return t


def get_hash(text):
    """Получить хэш."""
    hashed = hmac.new(HASH_SALT, text.encode(ENCODING))
    return hashed.hexdigest()


# def wait(condition):
#     while not condition:
#
#         time.sleep(0.1)


# def is_socket_ready(socket, mode):
#     wait = 0
#     r = []
#     w = []
#     try:
#         r, w, e = select.select([socket], [socket], [], wait)
#     except:
#         pass  # Socket disconnected
#     if mode == 'r':
#         return r != []
#     elif mode == 'w':
#         return w != []
#     else:
#         raise Exception('is_socket_ready() mode must be "r" or "w"')
