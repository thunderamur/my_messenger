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
        self.window = None
        self.app = None
        
    def start_listener(self):
        self.listener = GuiReceiver(self.socket, self.request_queue)
        self.listener.gotData.connect(self.update_chat)
        th = QThread()
        self.listener.moveToThread(th)
        th.started.connect(self.listener.poll)
        th.start()

    @pyqtSlot(str)
    def update_chat(self, data):
        try:
            msg = data
            self.window.listWidgetMessages.addItem(msg)
        except Exception as e:
            print(e)

    def run(self, host, port):
        start_thread(super().run, 'ClientThread', host, port)

        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QMainWindow()
        ui = gui.MyMessengerUI.Ui_MainWindow()
        ui.setupUi(self.window)

        self.window.show()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    app_start(MessengerClientGUI)