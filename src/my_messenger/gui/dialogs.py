from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL.ImageQt import ImageQt

from .utils import center
from .ConnectDialogUI import Ui_ConnectDialog
from .AboutDialogUI import Ui_AboutDialog
from .ProfileDialogUI import Ui_ProfileDialog


class ConnectUI(QtWidgets.QDialog):
    """Start window to set connection params."""
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


class AboutUI(QtWidgets.QDialog):
    """Window to show about info."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)
        center(self)


class ProfileUI(QtWidgets.QDialog):
    """Window to change profile."""
    def __init__(self, parent=None):
        super().__init__(parent)
        center(self)
        self.ui = Ui_ProfileDialog()
        self.ui.setupUi(self)
        # self.ui.groupBox.widgetAvatar
        self.ui.pushButtonBrowse.clicked.connect(self.browseFile)

    def browseFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Выберите аватар', '/home')[0]
        image = Image.open(fname)
        width = self.ui.labelAvatarImage.width()
        height = self.ui.labelAvatarImage.height()
        image = image.resize((width, height), Image.ANTIALIAS)
        img_tmp = ImageQt(image.convert('RGBA'))
        pixmap = QPixmap.fromImage(img_tmp)
        self.ui.labelAvatarImage.setPixmap(pixmap)