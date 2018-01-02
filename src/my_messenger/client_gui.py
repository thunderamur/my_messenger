import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QThread, pyqtSlot
from queue import Queue
import time

from client_core import MyMessengerClient
import gui.MyMessengerUI
from jim.core import *
from handlers import GuiReceiver
from utils import start_thread, app_start


class MessengerClientGUI(MyMessengerClient):
    """Графический клиент."""

    def start_listener(self):
        """Перегрузка метода родителя. Получатель сообщений."""
        return None

    def sender(self):
        """Перегрузка метода родителя. Отправитель сообщений."""
        self.join_room('default_room')
        time.sleep(0.2)
        self.contact_list_request()

    def run(self, host, port):
        """Расширение метода родителя. Запуск клиента."""
        start_thread(super().run, 'ClientThread', host, port)

    def stop(self):
        """Перегрузка метода родителя. Останов клиента."""
        self.is_alive = False


@pyqtSlot(str)
def update_chat(msg):
    """Обновление чата."""
    update_widget(ui.listWidgetMessages, msg)


@pyqtSlot(str)
def update_contact_list(msg):
    """Обновление списка контактов."""
    update_widget(ui.listWidgetContactList, msg)


def update_widget(listWidget, msg):
    """Обновление содержимого listWidget"""
    try:
        print(msg)
        listWidget.addItem(msg)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    client = app_start(MessengerClientGUI)

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
