import time
from PyQt5.QtCore import QObject, pyqtSignal

from jim.utils import send_message, get_message
from jim.core import *


class Receiver:
    def __init__(self, sock, request_queue):
        self.request_queue = request_queue
        self.sock = sock
        self.is_alive = False

    def show_message(self, message):
        pass

    def poll(self):
        self.is_alive = True
        while self.is_alive:
            msg = get_message(self.sock)
            jm = Jim.from_dict(msg)
            print(jm.__dict__)
            if isinstance(jm, JimMessage):
                self.show_message(jm)
            else:
                self.request_queue.put(jm)

    def stop(self):
        self.is_alive = False


class ConsoleReceiver(Receiver):
    def show_message(self, message):
        print("{} ({}): {}".format(message.from_, time.strftime('%H:%M:%S'), message.message))


class GuiReceiver(Receiver, QObject):
    gotData = pyqtSignal(str)
    finished = pyqtSignal(int)

    def __init__(self, sock, request_queue):
        Receiver.__init__(self, sock, request_queue)
        QObject.__init__(self)

    def show_message(self, message):
        text = '{} ({}):\n {}'.format(message.from_, self.get_time(), message.message)
        self.gotData.emit(text)

    def poll(self):
        super().poll()
        self.finished.emit(0)