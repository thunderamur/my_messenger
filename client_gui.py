import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QThread, pyqtSlot
from queue import Queue

from client import MessengerClient
import gui.MyMessengerUI
from jim.core import *
from handlers import GuiReceiver


class MessengerGUI(MessengerClient):
    def get_listener(self):
        return GuiReceiver(self.socket, self.request_queue)


@pyqtSlot(str)
def update_chat(data):
    try:
        msg = data
        window.listWidgetMessages.addItem(msg)
    except Exception as e:
        print(e)


def run_gui():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = gui.MyMessengerUI.Ui_MainWindow()
    ui.setupUi(window)

    window.show()
    sys.exit(app.exec_())


def run_client():
    if len(sys.argv) < 2:
        print('Usage: client.py <addr> [<port>]')
        return -1
    host = sys.argv[1]

    port = 7777
    if len(sys.argv) == 3:
        if not sys.argv[2].startswith('-'):
            port = int(sys.argv[2])

    client = MessengerGUI('Vasya')
    client.run(host, port)


def main():
    c = Thread(target=run_client)
    c.name = 'client'
    c.daemon = True
    c.start()

    # g = Thread(target=run_gui)
    # g.name = 'gui'
    # g.daemon = True
    # g.start()
    # g.join()

    run_gui()
    c.join()


if __name__ == '__main__':
    main()