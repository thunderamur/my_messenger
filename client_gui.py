import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QThread, pyqtSlot
from queue import Queue

from client import MessengerClient
import gui.MyMessengerUI
from jim.core import *
from handlers import GuiReceiver
from utils import start_thread


class MessengerGUI(MessengerClient):
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


def main():
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
            elif key == '-name':
                name = val
            elif key == '-password':
                password = val

    if host and port and name and password:
        client = MessengerGUI(name, password)
        client.run(host, port)
    else:
        print('Usage: client.py <addr> [-port=<port>] -name=<name> -password=<password>')
        return -1


if __name__ == '__main__':
    main()