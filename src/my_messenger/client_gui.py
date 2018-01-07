import sys
import time
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread

from client_core import MyMessengerClient
from gui.MyMessengerUI import Ui_MainWindow
from gui.ConnectDialogUI import Ui_ConnectDialog
from jim.core import *
from handlers import GuiReceiver
from utils import start_thread


def center(widget):
    screen = QtWidgets.QDesktopWidget().screenGeometry()
    size = widget.geometry()
    x = (screen.width() - size.width()) // 2
    y = (screen.height() - size.height()) // 2
    widget.move(x, y)


class ConnectUI(QtWidgets.QDialog):
    """Modal window to set connection params."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ConnectDialog()
        self.ui.setupUi(self)
        self.ui.pushButtonConnect.clicked.connect(self.connect)
        center(self)

    def connect(self):
        """Get params and transfer to parent"""
        ip, port = self.ui.lineEditIP.text().split(':')
        self.parent().ip = ip
        self.parent().port = int(port)
        self.parent().login = self.ui.lineEditLogin.text()
        self.parent().password = self.ui.lineEditPassword.text()
        self.parent().is_started = True
        self.close()


class MyMessengerClientGUI(QtWidgets.QMainWindow):
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
        self.client_thread = None
        self.listener_thread = None
        self.is_started = False

        # UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButtonChatSend.clicked.connect(self.chat_send)
        self.ui.pushButtonAddContact.clicked.connect(self.add_contact)
        self.ui.pushButtonDelContact.clicked.connect(self.del_contact)
        self.ui.listWidgetContactList.itemDoubleClicked.connect(self.choose_room)

        center(self)

    def closeEvent(self, QCloseEvent):
        """Extend of method. Activate stop methods of client and listener before close GUI."""
        if self.is_started:
            print('Waiting for threads finish... ', sep='')
            self.listener.stop()
            self.client.stop()
            self.client_thread.join()
            print('OK')
        else:
            print('Launch aborted')
        super().closeEvent(QCloseEvent)

    def run(self):
        """Start client."""
        self.connect()
        if not self.is_started:
            return True
        self.client = MyMessengerClient(self.login, self.password)
        self.client_thread = start_thread(self.client.run, 'Client', self.ip, self.port)
        while not self.client.is_alive:
            if not self.client_thread.is_alive():
                return False
        self.listener, self.listener_thread = self.start_listener()

        while not self.client.is_ready:
            time.sleep(0.1)
        self.client.contact_list_request()
        self.update_contact_list()
        self.choose_room()

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

    def update_contact_list(self):
        """ContactWidget update."""
        try:
            self.ui.listWidgetContactList.clear()
            self.ui.listWidgetContactList.addItem('@all')
            for contact in self.client.get_contact_list():
                self.ui.listWidgetContactList.addItem(contact)
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

    def add_contact(self):
        """Add contact to contact list."""
        contact = self.ui.lineEditAddContact.text()
        self.ui.lineEditAddContact.clear()
        self.client.add_contact(contact)
        self.client.contact_list.append(contact)
        self.ui.listWidgetContactList.addItem(contact)

    def del_contact(self):
        """Remove contact from contact list."""
        widget = self.ui.listWidgetContactList
        contact = widget.currentItem().text()
        self.client.del_contact(contact)
        self.client.contact_list.remove(contact)
        widget.takeItem(widget.currentRow())

    def choose_room(self):
        item = self.ui.listWidgetContactList.currentItem() or self.ui.listWidgetContactList.item(0)
        room = item.text()
        self.client.room = room
        self.ui.groupBoxChatName.setTitle('Выбран чат: {}'.format(room))
        print('Room changed on: {}'.format(room))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    client_gui = MyMessengerClientGUI()
    client_gui.show()
    while not client_gui.run():
        print('Run FAILED. Trying again...')

    sys.exit(app.exec_())
