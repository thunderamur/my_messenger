# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MyMessenger.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
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
        self.pushButtonAddContact.setGeometry(QtCore.QRect(10, 40, 90, 27))
        self.pushButtonAddContact.setObjectName("pushButtonAddContact")
        self.pushButtonContactList = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonContactList.setGeometry(QtCore.QRect(110, 40, 90, 27))
        self.pushButtonContactList.setObjectName("pushButtonContactList")
        self.lineEditAddContact = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditAddContact.setGeometry(QtCore.QRect(10, 10, 191, 27))
        self.lineEditAddContact.setObjectName("lineEditAddContact")
        self.listViewContactList = QtWidgets.QListView(self.centralwidget)
        self.listViewContactList.setGeometry(QtCore.QRect(10, 70, 191, 281))
        self.listViewContactList.setObjectName("listViewContactList")
        self.textEditChat = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditChat.setGeometry(QtCore.QRect(210, 40, 381, 251))
        self.textEditChat.setObjectName("textEditChat")
        self.labelChat = QtWidgets.QLabel(self.centralwidget)
        self.labelChat.setGeometry(QtCore.QRect(210, 10, 381, 17))
        self.labelChat.setObjectName("labelChat")
        self.textEditChatInput = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditChatInput.setGeometry(QtCore.QRect(210, 300, 291, 51))
        self.textEditChatInput.setObjectName("textEditChatInput")
        self.pushButtonChatSend = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonChatSend.setGeometry(QtCore.QRect(510, 300, 85, 51))
        self.pushButtonChatSend.setObjectName("pushButtonChatSend")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MyMessenger"))
        self.pushButtonAddContact.setText(_translate("MainWindow", "Добавить"))
        self.pushButtonContactList.setText(_translate("MainWindow", "Удалить"))
        self.labelChat.setText(_translate("MainWindow", "Чат не выбран"))
        self.pushButtonChatSend.setText(_translate("MainWindow", "Отправить"))

