# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MyMessenger.ui'
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
        self.pushButtonAddContact.setGeometry(QtCore.QRect(10, 40, 90, 27))
        self.pushButtonAddContact.setObjectName("pushButtonAddContact")
        self.pushButtonContactList = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonContactList.setGeometry(QtCore.QRect(110, 40, 90, 27))
        self.pushButtonContactList.setObjectName("pushButtonContactList")
        self.lineEditAddContact = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditAddContact.setGeometry(QtCore.QRect(10, 10, 191, 27))
        self.lineEditAddContact.setObjectName("lineEditAddContact")
        self.textEditChatInput = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditChatInput.setGeometry(QtCore.QRect(220, 300, 271, 41))
        self.textEditChatInput.setObjectName("textEditChatInput")
        self.pushButtonChatSend = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonChatSend.setGeometry(QtCore.QRect(500, 300, 81, 41))
        self.pushButtonChatSend.setObjectName("pushButtonChatSend")
        self.listWidgetMessages = QtWidgets.QListWidget(self.centralwidget)
        self.listWidgetMessages.setGeometry(QtCore.QRect(220, 40, 361, 251))
        self.listWidgetMessages.setObjectName("listWidgetMessages")
        self.groupBoxChatName = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxChatName.setGeometry(QtCore.QRect(210, 10, 381, 341))
        self.groupBoxChatName.setObjectName("groupBoxChatName")
        self.listWidgetContactList = QtWidgets.QListWidget(self.centralwidget)
        self.listWidgetContactList.setGeometry(QtCore.QRect(10, 80, 191, 271))
        self.listWidgetContactList.setObjectName("listWidgetContactList")
        self.pushButtonAddContact.raise_()
        self.pushButtonContactList.raise_()
        self.lineEditAddContact.raise_()
        self.groupBoxChatName.raise_()
        self.listWidgetMessages.raise_()
        self.pushButtonChatSend.raise_()
        self.textEditChatInput.raise_()
        self.listWidgetContactList.raise_()
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
        self.pushButtonChatSend.setText(_translate("MainWindow", "Отправить"))
        self.groupBoxChatName.setTitle(_translate("MainWindow", "Чат не выбран"))

