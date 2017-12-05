import sys
from PyQt5 import QtWidgets
from threading import Thread
from queue import Queue

from client import MessengerClient
import gui.MyMessengerUI

from jim.core import *

buffer = Queue()


class MessengerGUI(MessengerClient):
    def parse(self, msg):
        super().parse(msg)
        action = Jim.from_dict(msg)
        buffer.put(action)


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