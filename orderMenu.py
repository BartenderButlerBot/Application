# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'orderMenu.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_orderMenu(object):
    def setupUi(self, orderMenu):
        orderMenu.setObjectName("orderMenu")
        orderMenu.resize(403, 300)
        self.verticalLayoutWidget = QtWidgets.QWidget(orderMenu)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 381, 271))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)

        self.retranslateUi(orderMenu)
        QtCore.QMetaObject.connectSlotsByName(orderMenu)

    def retranslateUi(self, orderMenu):
        _translate = QtCore.QCoreApplication.translate
        orderMenu.setWindowTitle(_translate("orderMenu", "Order Menu"))
        self.pushButton.setText(_translate("orderMenu", "Drink #1"))
        self.pushButton_2.setText(_translate("orderMenu", "Drink #2"))
        self.pushButton_3.setText(_translate("orderMenu", "Drink #3"))

