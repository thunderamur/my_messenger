from PyQt5 import QtWidgets

from .ConnectDialogUI import Ui_ConnectDialog
from .utils import center


class ConnectUI(QtWidgets.QDialog):
    """Modal window to set connection params."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent().is_started = False
        self.ui = Ui_ConnectDialog()
        self.ui.setupUi(self)
        self.ui.pushButtonConnect.clicked.connect(self.connect)
        center(self)

    def connect(self):
        """Get params and transfer to parent"""
        ip, port = self.ui.lineEditIP.text().split(':')
        port = int(port)
        login = self.ui.lineEditLogin.text()
        password = self.ui.lineEditPassword.text()
        self.parent().ip = ip
        self.parent().port = port
        self.parent().login = login
        self.parent().password = password
        self.parent().is_started = True
        self.accept()
