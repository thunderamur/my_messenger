import sys
import hmac
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
