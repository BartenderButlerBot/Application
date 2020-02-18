# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menuShell.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_menuShell(object):
    def setupUi(self, menuShell):
        menuShell.setObjectName("menuShell")
        menuShell.resize(1024, 600)
        self.backToMain = QtWidgets.QPushButton(menuShell)
        self.backToMain.setGeometry(QtCore.QRect(20, 440, 181, 111))
        self.backToMain.setObjectName("backToMain")
        self.backToMain_2 = QtWidgets.QPushButton(menuShell)
        self.backToMain_2.setGeometry(QtCore.QRect(20, 310, 181, 111))
        self.backToMain_2.setObjectName("backToMain_2")
        self.widget = QtWidgets.QWidget(menuShell)
        self.widget.setGeometry(QtCore.QRect(229, 19, 521, 561))
        self.widget.setAutoFillBackground(False)
        self.widget.setObjectName("widget")

        self.retranslateUi(menuShell)
        QtCore.QMetaObject.connectSlotsByName(menuShell)

    def retranslateUi(self, menuShell):
        _translate = QtCore.QCoreApplication.translate
        menuShell.setWindowTitle(_translate("menuShell", "Form"))
        self.backToMain.setText(_translate("menuShell", "Main Window"))
        self.backToMain_2.setText(_translate("menuShell", "Custom Order"))

