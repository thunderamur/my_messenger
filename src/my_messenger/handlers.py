import time
from PyQt5.QtCore import QObject, pyqtSignal

from .jim.utils import get_message
from .jim.core import *
from .client_config import DEBUG


class Receiver:
    """Получатель сообщений. Базовый класс."""
    def __init__(self, sock, request_queue):
        self.request_queue = request_queue
        self.sock = sock
        self.is_alive = False

    def show_message(self, jm):
        """Показать сообщение."""
        pass

    def poll(self):
        """Слушать сообщения от сервера."""
        self.is_alive = True
        while self.is_alive:
            msg = get_message(self.sock)
            jm = Jim.from_dict(msg)
            if DEBUG:
                print('RESPONSE: ', jm.__dict__)
            if isinstance(jm, JimMessage):
                self.show_message(jm)
            else:
                self.request_queue.put(jm)

    def stop(self):
        """Останов получателя сообщений."""
        self.is_alive = False


class ConsoleReceiver(Receiver):
    """Консольный получатель сообщений."""

    def show_message(self, jm):
        """Показать сообщение."""
        print("{} ({}): {}".format(jm.from_, time.strftime('%H:%M:%S'), jm.message))


class GuiReceiver(Receiver, QObject):
    """Графический получатель сообщений."""
    # Получено сообщение.
    gotMessage = pyqtSignal(str)
    # Останов получателя.
    finished = pyqtSignal(int)

    def __init__(self, sock, request_queue):
        Receiver.__init__(self, sock, request_queue)
        QObject.__init__(self)

    def show_message(self, jm):
        """Показать сообщение в GUI."""
        text = '{} ({}):\n{}'.format(jm.from_, time.strftime('%H:%M:%S'), jm.message)
        self.gotMessage.emit(text)

    def poll(self):
        """Слушать сообщения от сервера. При выходе сообщить GUI."""
        super().poll()
        self.finished.emit(0)