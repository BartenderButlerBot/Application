# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testHideWidget.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import sys, time
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(802, 542)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(0, 0, 801, 541))
        self.widget.setObjectName("widget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.widget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 10, 791, 521))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 2, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 3, 0, 1, 3)

        self.retranslateUi(Form)
        self.pushButton_4.clicked.connect(Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.pushButton.clicked.connect(self.hideWidget)
  
    def hideWidget(self):
        print('made it to hideWidget')
        self.gridLayoutWidget.hide()
        print('should be hiding')
        print('starting sleep')
        time.sleep(2)
        print('ending sleep')
        self.gridLayoutWidget.show()
        print('Should be showing')

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_2.setText(_translate("Form", "Change Order"))
        self.label_2.setText(_translate("Form", "butlerACK"))
        self.pushButton.setText(_translate("Form", "Order Drink"))
        self.pushButton_3.setText(_translate("Form", "Dock Butler"))
        self.label.setText(_translate("Form", "bartenderACK"))
        self.label_3.setText(_translate("Form", "bartenderOrder"))
        self.label_4.setText(_translate("Form", "butlerStatus"))
        self.label_5.setText(_translate("Form", "bartenderInventoryA"))
        self.label_6.setText(_translate("Form", "bartenderInventoryB"))
        self.pushButton_4.setText(_translate("Form", "Quit"))


try:
    application = QtWidgets.QApplication(sys.argv)
    application.setStyle('Fusion')
    
    main = QtWidgets.QWidget()
    window = Ui_Form()
    window.setupUi(main)
    main.show()
    
    sys.exit(application.exec_())
    
except Exception as e:
    sys.stderr.write("Error: {0}".format(e))
