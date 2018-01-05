import sys
import time
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QThread, pyqtSlot
from queue import Queue

from client_core import MyMessengerClient
from gui.MyMessengerUI import Ui_MainWindow
from gui.ConnectDialogUI import Ui_ConnectDialog
from jim.core import *
from handlers import GuiReceiver
from utils import start_thread


class ConnectUI(QtWidgets.QDialog):
    """Modal window to set connection params."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ConnectDialog()
        self.ui.setupUi(self)
        self.ui.pushButtonConnect.clicked.connect(self.connect)

    def connect(self):
        """Get params and transfer to parent"""
        ip, port = self.ui.lineEditIP.text().split(':')
        self.parent().ip = ip
        self.parent().port = int(port)
        self.parent().login = self.ui.lineEditLogin.text()
        self.parent().password = self.ui.lineEditPassword.text()
        self.close()


class ClientGUI(QtWidgets.QMainWindow):
    """GUI for MyMessenger"""
    def __init__(self, parent=None):
        super().__init__()

        # Client
        self.ip = None
        self.port = None
        self.login = None
        self.password = None
        self.client = None
        self.listener = None
        self.listener_thread = None

        # UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButtonChatSend.clicked.connect(self.chat_send)

    def run(self):
        """Start client."""
        self.connect()
        self.client = MyMessengerClient(self.login, self.password)
        client_thread = start_thread(self.client.run, 'Client', self.ip, self.port)
        while not self.client.is_alive:
            if not client_thread.is_alive():
                return False
        self.listener, self.listener_thread = self.start_listener()
        self.client.contact_list_request()
        # TODO: FIX this stupid hack!
        time.sleep(0.5)
        self.client.join_room('default_room')
        return True

    def connect(self):
        """Open connect dialog modal window"""
        cui = ConnectUI(parent=self)
        cui.exec()

    def start_listener(self):
        """Start GuiReceiver"""
        listener = GuiReceiver(self.client.socket, self.client.request_queue)
        listener.gotMessage.connect(self.update_chat)
        thread = QThread()
        listener.moveToThread(thread)
        thread.started.connect(listener.poll)
        thread.start()
        return listener, thread

    def update_chat(self, msg):
        """Chat update."""
        try:
            print(msg)
            self.ui.listWidgetMessages.addItem(msg)
        except Exception as e:
            print(e)

    def chat_send(self):
        """Send message."""
        msg_txt = self.ui.textEditChatInput.toPlainText()
        jm = JimMessage(self.client.room, self.client.user.account_name, msg_txt)
        self.client.request(jm)
        self.ui.textEditChatInput.clear()
        text = '{} ({}):\n{}'.format(jm.from_, time.strftime('%H:%M:%S'), jm.message)
        self.ui.listWidgetMessages.addItem(text)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    client_gui = ClientGUI()
    client_gui.show()
    while not client_gui.run():
        print('Run FAILED. Trying again...')

    sys.exit(app.exec_())
