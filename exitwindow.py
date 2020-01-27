# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'exitwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ExitWindow(object):
    def setupUi(self, ExitWindow):
        ExitWindow.setObjectName("ExitWindow")
        ExitWindow.resize(360, 150)
        self.buttonBox = QtWidgets.QDialogButtonBox(ExitWindow)
        self.buttonBox.setGeometry(QtCore.QRect(90, 110, 180, 32))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(ExitWindow)
        self.label.setGeometry(QtCore.QRect(105, 30, 161, 71))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        self.retranslateUi(ExitWindow)
        self.buttonBox.accepted.connect(ExitWindow.accept)
        self.buttonBox.rejected.connect(ExitWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(ExitWindow)

    def retranslateUi(self, ExitWindow):
        _translate = QtCore.QCoreApplication.translate
        ExitWindow.setWindowTitle(_translate("ExitWindow", "Dialog"))
        self.label.setText(_translate("ExitWindow", "Are you sure you want to quit?"))

