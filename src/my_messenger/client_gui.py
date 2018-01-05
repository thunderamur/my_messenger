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
    def __init__(self, parent=None):
        super().__init__()

        self.client = MyMessengerClient('user1', '123')
        start_thread(self.client.run, 'Client', '127.0.0.1', 7777)
        while not self.client.is_alive:
            pass
        self.listener, self.listener_thread = self.start_listener()
        self.client.contact_list_request()
        time.sleep(0.5)
        self.client.join_room('default_room')

        # UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButtonChatSend.clicked.connect(self.chat_send)

    def start_listener(self):
        listener = GuiReceiver(self.client.socket, self.client.request_queue)
        listener.gotMessage.connect(self.update_chat)
        thread = QThread()
        listener.moveToThread(thread)
        thread.started.connect(listener.poll)
        thread.start()
        return listener, thread

    def update_chat(self, msg):
        """Обновление чата."""
        try:
            print(msg)
            self.ui.listWidgetMessages.addItem(msg)
        except Exception as e:
            print(e)

    def chat_send(self):
        msg_txt = self.ui.textEditChatInput.toPlainText()
        jm = JimMessage(self.client.room, self.client.user.account_name, msg_txt)
        self.client.request(jm)
        self.ui.textEditChatInput.clear()
        text = '{} ({}):\n{}'.format(jm.from_, time.strftime('%H:%M:%S'), jm.message)
        self.ui.listWidgetMessages.addItem(text)


if __name__ == '__main__':
    # ======================
    # host = None
    # port = None
    # name = None
    # password = None
    # if len(sys.argv) >= 4:
    #     host = sys.argv[1]
    #     port = 7777
    #
    #     for option in sys.argv[2:]:
    #         key, val = option.split('=')
    #         if key == '-port':
    #             port = val
    #         elif key == '-user':
    #             name = val
    #         elif key == '-pass':
    #             password = val
    #
    # if host and port and name and password:
    #     mmc = MyMessengerClientGUI(name, password)
    #     start_thread(mmc.run, 'Client', host, port)
    # else:
    #     print('Usage: client.py <addr> [-port=<port>] -user=<user> -pass=<password>')
    #     sys.exit()
    # =============================

    app = QtWidgets.QApplication(sys.argv)
    client_gui = ClientGUI()
    client_gui.show()

    sys.exit(app.exec_())
