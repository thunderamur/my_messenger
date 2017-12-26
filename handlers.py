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

    def show_contact_list(self, message):
        pass

    def poll(self):
        self.is_alive = True
        while self.is_alive:
            msg = get_message(self.sock)
            jm = Jim.from_dict(msg)
            print(jm.__dict__)
            if isinstance(jm, JimMessage):
                self.show_message(jm)
            elif isinstance(jm, JimContactList):
                self.show_contact_list(jm)
            else:
                self.request_queue.put(jm)

    def stop(self):
        self.is_alive = False


class ConsoleReceiver(Receiver):
    def show_message(self, message):
        print("{} ({}): {}".format(message.from_, time.strftime('%H:%M:%S'), message.message))

    def show_contact_list(self, message):
        print(message.user_id)


class GuiReceiver(Receiver, QObject):
    gotMessage = pyqtSignal(str)
    finished = pyqtSignal(int)
    gotContactList = pyqtSignal(str)

    def __init__(self, sock, request_queue):
        Receiver.__init__(self, sock, request_queue)
        QObject.__init__(self)

    def show_message(self, message):
        text = '{} ({}):\n{}'.format(message.from_, time.strftime('%H:%M:%S'), message.message)
        self.gotMessage.emit(text)

    def show_contact_list(self, message):
        self.gotContactList.emit(message.user_id)

    def poll(self):
        super().poll()
        self.finished.emit(0)