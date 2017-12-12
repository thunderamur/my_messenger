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
    def __init__(self, account_name):
        super().__init__(account_name)
        self.window = None
        self.app = None
        
    def start_listener(self):
        self.listener = GuiReceiver(self.socket, self.request_queue)
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

        self.listener.gotData.connect(self.update_chat)
    
        self.window.show()
        sys.exit(self.app.exec_())


def main():
    if len(sys.argv) < 2:
        print('Usage: client.py <addr> [-port=<port>] -name=<name>')
        return -1
    host = sys.argv[1]
    port = 7777

    for option in sys.argv[2:]:
        key, val = option.split('=')
        if key == '-port':
            port = val
        elif key == '-name':
            name = val

    client = MessengerGUI(name)
    client.run(host, port)


if __name__ == '__main__':
    main()