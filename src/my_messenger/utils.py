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


def app_start(client_class):
    """Старт приложения."""
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
            elif key == '-user':
                name = val
            elif key == '-pass':
                password = val

    if host and port and name and password:
        client = client_class(name, password)
        client.run(host, port)
        # Ждем создания сокета.
        while not client.socket:
            pass
        return client
    else:
        print('Usage: client.py <addr> [-port=<port>] -user=<user> -pass=<password>')
        return -1