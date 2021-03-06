# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButtonAddContact = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonAddContact.setGeometry(QtCore.QRect(170, 10, 31, 27))
        self.pushButtonAddContact.setObjectName("pushButtonAddContact")
        self.lineEditAddContact = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditAddContact.setGeometry(QtCore.QRect(10, 10, 151, 27))
        self.lineEditAddContact.setObjectName("lineEditAddContact")
        self.pushButtonChatSend = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonChatSend.setGeometry(QtCore.QRect(500, 320, 81, 41))
        self.pushButtonChatSend.setObjectName("pushButtonChatSend")
        self.groupBoxChatName = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxChatName.setGeometry(QtCore.QRect(210, 10, 381, 361))
        self.groupBoxChatName.setObjectName("groupBoxChatName")
        self.pushButtonFormatB = QtWidgets.QPushButton(self.groupBoxChatName)
        self.pushButtonFormatB.setGeometry(QtCore.QRect(10, 280, 21, 21))
        self.pushButtonFormatB.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../img/icon/b.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonFormatB.setIcon(icon)
        self.pushButtonFormatB.setObjectName("pushButtonFormatB")
        self.pushButtonFormatI = QtWidgets.QPushButton(self.groupBoxChatName)
        self.pushButtonFormatI.setGeometry(QtCore.QRect(40, 280, 21, 21))
        self.pushButtonFormatI.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../img/icon/i.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonFormatI.setIcon(icon1)
        self.pushButtonFormatI.setObjectName("pushButtonFormatI")
        self.pushButtonFormatU = QtWidgets.QPushButton(self.groupBoxChatName)
        self.pushButtonFormatU.setGeometry(QtCore.QRect(70, 280, 21, 21))
        self.pushButtonFormatU.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../img/icon/u.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonFormatU.setIcon(icon2)
        self.pushButtonFormatU.setObjectName("pushButtonFormatU")
        self.textEditChatInput = QtWidgets.QTextEdit(self.groupBoxChatName)
        self.textEditChatInput.setGeometry(QtCore.QRect(10, 310, 271, 41))
        self.textEditChatInput.setObjectName("textEditChatInput")
        self.textEditChat = QtWidgets.QTextEdit(self.groupBoxChatName)
        self.textEditChat.setGeometry(QtCore.QRect(10, 30, 361, 241))
        self.textEditChat.setReadOnly(True)
        self.textEditChat.setObjectName("textEditChat")
        self.labelSmileBtn = QtWidgets.QLabel(self.groupBoxChatName)
        self.labelSmileBtn.setGeometry(QtCore.QRect(100, 280, 21, 21))
        self.labelSmileBtn.setText("")
        self.labelSmileBtn.setPixmap(QtGui.QPixmap("../img/smile/ab.gif"))
        self.labelSmileBtn.setObjectName("labelSmileBtn")
        self.listWidgetContactList = QtWidgets.QListWidget(self.centralwidget)
        self.listWidgetContactList.setGeometry(QtCore.QRect(10, 50, 191, 321))
        self.listWidgetContactList.setObjectName("listWidgetContactList")
        self.pushButtonAddContact.raise_()
        self.lineEditAddContact.raise_()
        self.groupBoxChatName.raise_()
        self.pushButtonChatSend.raise_()
        self.listWidgetContactList.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 27))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.help = QtWidgets.QMenu(self.menubar)
        self.help.setObjectName("help")
        self.settings = QtWidgets.QMenu(self.menubar)
        self.settings.setObjectName("settings")
        MainWindow.setMenuBar(self.menubar)
        self.quit = QtWidgets.QAction(MainWindow)
        self.quit.setObjectName("quit")
        self.profile = QtWidgets.QAction(MainWindow)
        self.profile.setObjectName("profile")
        self.about = QtWidgets.QAction(MainWindow)
        self.about.setObjectName("about")
        self.menu.addAction(self.quit)
        self.help.addAction(self.about)
        self.settings.addAction(self.profile)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.settings.menuAction())
        self.menubar.addAction(self.help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MyMessenger"))
        self.pushButtonAddContact.setText(_translate("MainWindow", "+"))
        self.pushButtonChatSend.setText(_translate("MainWindow", "Отправить"))
        self.groupBoxChatName.setTitle(_translate("MainWindow", "Чат не выбран"))
        self.menu.setTitle(_translate("MainWindow", "Меню"))
        self.help.setTitle(_translate("MainWindow", "Помощь"))
        self.settings.setTitle(_translate("MainWindow", "Настройки"))
        self.quit.setText(_translate("MainWindow", "Выход"))
        self.profile.setText(_translate("MainWindow", "Профиль"))
        self.about.setText(_translate("MainWindow", "Справка"))

