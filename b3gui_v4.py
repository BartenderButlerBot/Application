# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'B3GUI-v3.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import sys
import paho.mqtt.client as mqtt
from PyQt5 import QtCore, QtGui, QtWidgets

MQTT_SERVER = "192.168.1.78"
MQTT_SERVERP = "192.168.1.68"
MQTT_SERVERC = "172.16.105.250"
MQTT_PORT = 1883
MQTT_USERNAME = ""
MQTT_PASSWORD = ""
MQTT_ID = "application"
BARORDER = "barOrder"
BARINVA = "barInvA"
BARINVB = "barInvB"
SENSECONNACK = "senseConnack"
SENSEDATA = "senseData"


bartenderACK = "bartenderACK"
bartenderOrder = "bartenderOrder"
butlerStatus = "butlerStatus"
bartenderInventoryA = "bartenderInventoryA"
bartenderInventoryB = "bartenderInventoryB"

########################## MQTT SETUP ##########################

def on_message(client, userdata, message):
    print(message.topic+" "+str(message.payload))
    msg = str(message.payload.decode("utf-8"))
    print("message received: " , msg)
    
    if BARORDER in message.topic:
        global bartenderOrder
        bartenderOrder = msg
    if message.topic == BARINVA:
        global bartenderInventoryA
        bartenderInventoryA = msg
    if message.topic == BARINVB:
        global bartenderInventoryB
        bartenderInventoryB = msg

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
def placeOrder(self):
    dummyOrder = "gimme something else"
    client.publish("B3Order", dummyOrder, qos = 0, retain = False)

client = mqtt.Client()
    
client.on_message = on_message
client.on_connect = on_connect
client.connect(MQTT_SERVERP, MQTT_PORT)
client.subscribe([(BARORDER, 1),(BARINVA, 1),(BARINVB, 1)])
client.publish("testTopic2", "application can publish", qos = 0, retain = False)

### exit ###

class Ui_ExitWindow(object):
    def setupUi(self, ExitWindow):
        self.mainFrame = ExitWindow
        
        ExitWindow.setObjectName("ExitWindow")
        ExitWindow.resize(360, 150)
        
        self.terminateFlag = False
        
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
        self.buttonBox.accepted.connect(self.killUi)
        self.buttonBox.rejected.connect(ExitWindow.close)
        QtCore.QMetaObject.connectSlotsByName(ExitWindow)

    def retranslateUi(self, ExitWindow):
        _translate = QtCore.QCoreApplication.translate
        ExitWindow.setWindowTitle(_translate("ExitWindow", "Dialog"))
        self.label.setText(_translate("ExitWindow", "Are you sure you want to quit?"))
        
    def killUi(self):
        self.terminateFlag = True
        self.mainFrame.close

########################## MAIN UI ##########################

class Ui_Form(object):
    def setupUi(self, Form):
        self.mainFrame = Form
        
        Form.setObjectName("Form")
        Form.resize(802, 542)
        self.exitFrame = None
        self.exitWindow = None
        
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
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

        ### BUTTON ACTION LINK ###

        self.retranslateUi(Form)
        self.pushButton_4.clicked.connect(self.exitPopup)
        ### test close remove later ###
        self.pushButton_3.clicked.connect(Form.close)
        ### test close remove later ###
        self.pushButton.clicked.connect(placeOrder)
        QtCore.QMetaObject.connectSlotsByName(Form)

        ### REFRESH TIMER ###
        
        self.qTimer = QtCore.QTimer()
        self.qTimer.setInterval(777)
        self.qTimer.timeout.connect(self.refreshUi)
        self.qTimer.start()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_2.setText(_translate("Form", "Change Order"))
        self.label_2.setText(_translate("Form", "butlerACK"))
        self.pushButton.setText(_translate("Form", "Order Drink"))
        self.pushButton_3.setText(_translate("Form", "Dock Butler"))
        self.label.setText(_translate("Form", bartenderACK))
        self.label_3.setText(_translate("Form", bartenderOrder))
        self.label_4.setText(_translate("Form", butlerStatus))
        self.label_5.setText(_translate("Form", bartenderInventoryA))
        self.label_6.setText(_translate("Form", bartenderInventoryB))
        self.pushButton_4.setText(_translate("Form", "Quit"))
        
    def refreshUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Form", bartenderACK))
        self.label_3.setText(_translate("Form", bartenderOrder))
        self.label_4.setText(_translate("Form", butlerStatus))
        self.label_5.setText(_translate("Form", bartenderInventoryA))
        self.label_6.setText(_translate("Form", bartenderInventoryB))

            
        
    def setBAck(ack):
        global bartenderACK
        bartenderACK= ack

    def setBOrder(order):
        global bartenderOrder 
        bartenderOrder= order

    def setBStatus(status):
        global butlerStatus
        butlerStatus = status

    def setBInvA(invA):
        global bartenderInventoryA
        bartenderInventoryA = invA

    def setBInvB(invB):
        global bartenderInventoryB
        bartenderInventoryB = invB

    def exitPopup(self):
        '''self.exitFrame = QtWidgets.QWidget()
        self.exitWindow = Ui_ExitWindow()
        self.exitWindow.setupUi(self.exitFrame)
        self.exitFrame.show()
        if self.exitWindow.terminateFlag == True:'''
        
        self.mainFrame.close
        
    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QtGui.QMessageBox.question(self, 'Message', 
                         quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
########################## Primary Code ##########################
    
def main():
    application = QtWidgets.QApplication(sys.argv)
    application.setStyle('Fusion')
    
    main = QtWidgets.QWidget()
    window = Ui_Form()
    window.setupUi(main)
    main.show()

    client.loop_start()
    
    sys.exit(application.exec_())

'''
try:
    client = mqtt.Client()
    client.connect(MQTT_SERVERC, MQTT_PORT)
    client.subscribe(SUB_TOPIC, qos = 1)
    client.loop_start()

    application = QtWidgets.QApplication(sys.argv)
    application.setStyle('Fusion')
    
    main = QtWidgets.QWidget()
    window = Ui_Form()
    window.setupUi(main)

    main.show()
    client.on_message = on_message()
    
    sys.exit(application.exec_())
    
except Exception as e:
    sys.stderr.write("Error: {0}".format(e))
'''

if __name__ == '__main__':
    #try:
    main()
        
    #except Exception as e:
     #   sys.stderr.write("Error: {0}".format(e))
