import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QThread, pyqtSlot
from queue import Queue

from client import MessengerClient
import gui.MyMessengerUI
from jim.core import *
from handlers import GuiReceiver
from utils import start_thread, app_start


class MessengerClientGUI(MessengerClient):
    def __init__(self, account_name, password):
        super().__init__(account_name, password)
        self.thread = None

    def start_listener(self):
        self.listener = GuiReceiver(self.socket, self.request_queue)
        self.listener.gotData.connect(update_chat)
        self.thread = QThread()
        self.listener.moveToThread(self.thread)
        self.thread.started.connect(self.listener.poll)
        self.thread.start()

    def run(self, host, port):
        start_thread(super().run, 'ClientThread', host, port)


@pyqtSlot(str)
def update_chat(data):
    print('update_chat')
    try:
        msg = data
        print(msg)
        window.listWidgetMessages.addItem(msg)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    app_start(MessengerClientGUI)

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = gui.MyMessengerUI.Ui_MainWindow()
    ui.setupUi(window)

    window.show()
    sys.exit(app.exec_())