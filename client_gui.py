import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QThread, pyqtSlot
from queue import Queue
import time

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
        return None

    def run(self, host, port):
        start_thread(super().run, 'ClientThread', host, port)
        # **************
        # Переделать!!!
        time.sleep(1)
        self.contact_list_request()
        # **************


@pyqtSlot(str)
def update_chat(msg):
    update_item(ui.listWidgetMessages, msg)


@pyqtSlot(str)
def update_contact_list(msg):
    update_item(ui.listWidgetContactList, msg)


def update_item(item, msg):
    try:
        print(msg)
        item.addItem(msg)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    client = app_start(MessengerClientGUI)

    while not client.socket:
        pass

    listener = GuiReceiver(client.socket, client.request_queue)
    listener.gotMessage.connect(update_chat)
    listener.gotContactList.connect(update_contact_list)
    thread = QThread()
    listener.moveToThread(thread)
    thread.started.connect(listener.poll)
    thread.start()

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = gui.MyMessengerUI.Ui_MainWindow()
    ui.setupUi(window)

    window.show()
    sys.exit(app.exec_())