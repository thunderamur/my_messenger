import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QThread, pyqtSlot
from queue import Queue
import time

from client_core import MyMessengerClient
from gui.MyMessengerUI import Ui_MainWindow
from jim.core import *
from handlers import GuiReceiver
from utils import start_thread, app_start


class ClientGUI(QtWidgets.QMainWindow):
    def __init__(self, client, parent=None):
        super().__init__()
        self.client = client
        self.client.client_core.contact_list_request()
        time.sleep(0.5)
        self.client.client_core.join_room('default_room')
        # UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButtonChatSend.clicked.connect(self.chat_send)

    def chat_send(self):
        msg_txt = self.ui.textEditChatInput.toPlainText()
        jm = JimMessage(self.client.client_core.room, self.client.client_core.user.account_name, msg_txt)
        self.client.client_core.request(jm)
        self.ui.textEditChatInput.clear()
        text = '{} ({}):\n{}'.format(jm.from_, time.strftime('%H:%M:%S'), jm.message)
        self.ui.listWidgetMessages.addItem(text)


class MyMessengerClientGUI:
    """Клиент my_messenger."""
    def __init__(self, account_name, password):
        self.client_core = MyMessengerClient(account_name, password)
        self.client_thread = None
        self.listener = None
        self.listener_thread = None

    def stop(self):
        self.listener.stop()

    def run(self, host, port):
        self.client_thread = start_thread(self.client_core.run, 'Client', host, port)
        while not self.client_core.is_alive:
            pass
        self.listener = GuiReceiver(self.client_core.socket, self.client_core.request_queue)
        self.listener_thread = start_thread(self.listener.poll, 'Listener')
        self.client_thread.join()
        self.listener_thread.join()


@pyqtSlot(str)
def update_chat(msg):
    """Обновление чата."""
    try:
        print(msg)
        client_gui.ui.listWidgetMessages.addItem(msg)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # ======================
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
            elif key == '-user':
                name = val
            elif key == '-pass':
                password = val

    if host and port and name and password:
        mmc = MyMessengerClientGUI(name, password)
        start_thread(mmc.run, 'Client', host, port)
    else:
        print('Usage: client.py <addr> [-port=<port>] -user=<user> -pass=<password>')
        sys.exit()
    # =============================

    app = QtWidgets.QApplication(sys.argv)
    while not mmc.client_core.is_alive:
        pass
    client_gui = ClientGUI(mmc)
    client_gui.show()

    listener = GuiReceiver(mmc.client_core.socket, mmc.client_core.request_queue)
    listener.gotMessage.connect(update_chat)
    thread = QThread()
    listener.moveToThread(thread)
    thread.started.connect(listener.poll)
    thread.start()

    sys.exit(app.exec_())
