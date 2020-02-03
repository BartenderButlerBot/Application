# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'B3GUI-v3.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import sys
import paho.mqtt.client as mqtt
import sqlite3
from sqlite3 import Error
from PyQt5 import QtCore, QtGui, QtWidgets

client = None 
MQTT_SERVER = "192.168.1.78"
MQTT_SERVERP = "192.168.1.68"
MQTT_SERVERC = "172.16.105.250"
MQTT_SERVERC2 = "172.16.105.23"
MQTT_PORT = 1883
MQTT_USERNAME = ""
MQTT_PASSWORD = ""
MQTT_ID = "application"
BARORDER = "barOrder"
BARINVA = "barInvA"
BARINVB = "barInvB"
SENSECONNACK = "senseConnack"
SENSEDATA = "senseData"

sqlConnect = None
cursor = None

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
    
def subMQTT(self, subTopic):
    global client
    client.subscribe(subTopic, qos = 1)

def initMQTT(self):
    global client
    client = mqtt.Client()
        
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(MQTT_SERVERP, MQTT_PORT)
    client.subscribe([(BARORDER, 1),(BARINVA, 1),(BARINVB, 1)])

########################## SQLite3 SETUP ##########################

def initSQL(self):
    global sqlConnect
    global cursor
    sqlConnect = sqlite3.connect('B3_blackbook_v1.db')
    cursor = sqlConnect.cursor()

def insertSQL(self, tableName, columnName, values):
    try:
        cursor.execute("INSERT INTO " + str(tableName) + "(" + 
                       str(columnName) + ") values(" + str(values) + ")")
        print("Successfully inserted " + str(values) + 
              " into table " + str(tableName))
        sqlConnect.commit()
    except Error as e:
        print(e)
    
def closeSQL(connect):
    try: 
        print("SQL closed successfully")
        connect.close()
    except Error as e:
        print(e)

########################## MAIN UI ##########################

class Ui_Form(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
    
    def setupUi(self):
        self.setGeometry(0, 150, 1024, 600)
        self.setWindowTitle("Form")
        self.exit = QtWidgets.QDialog()

        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 10, 1021, 551))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(5, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(5)
        self.gridLayout.setObjectName("gridLayout")

        ### UI Creation ###
        
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

        self.pushButton_5 = QtWidgets.QPushButton(self)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setGeometry(QtCore.QRect(5, 555, 91, 36))

        ### BUTTON ACTION LINK ###

        self.retranslateUi()
        self.pushButton_4.clicked.connect(self.exitPopup)
        self.pushButton_3.clicked.connect(self.newRecipe)
        self.pushButton.clicked.connect(placeOrder)

        ### REFRESH TIMER ###
        
        self.qTimer = QtCore.QTimer()
        self.qTimer.setInterval(777)
        self.qTimer.timeout.connect(self.refreshUi)
        self.qTimer.start()

    def newRecipe(self):
        drink_name = "\"test drink sdfsdfg\""
        liquor1_name = "\"liq 1\""
        liquor1_amount_ml = 35
        liquor2_name = "\"liq 2\""
        liquor2_amount_ml = 40
        ingredient1_name = "\"ing 1\""
        ingredient1_amount_ml = 300
        values = str(str(drink_name) + ", " + str(liquor1_name) + ", " + 
                     str(liquor1_amount_ml) + ", " + str(liquor2_name) + ", " + 
                     str(liquor2_amount_ml) + ", " + str(ingredient1_name) + ", " + 
                     str(ingredient1_amount_ml))
        insertSQL(cursor, "recipe", "drink_name, liquor1_name, " + 
                  "liquor1_amount_ml,liquor2_name, liquor2_amount_ml," + 
                  " ingredient1_name, ingredient1_amount_ml", values)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
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
        self.pushButton_5.setText(_translate("Form", "Settings"))
        
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
        self.exit.setWindowTitle("ExitWindow")
        self.exit.setGeometry(220, 310, 360, 150)
        self.exitLayout = QtWidgets.QGridLayout()

        ### UI Creation ###
        
        self.exitDialog = QtWidgets.QDialogButtonBox(self.exit)
        self.exitDialog.setGeometry(QtCore.QRect(90, 110, 180, 32))
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, \
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exitDialog.sizePolicy().\
                                     hasHeightForWidth())

        self.exitDialog.setSizePolicy(sizePolicy)
        self.exitDialog.setOrientation(QtCore.Qt.Horizontal)
        self.exitDialog.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel\
                                           |QtWidgets.QDialogButtonBox.Ok)
        self.exitDialog.setCenterButtons(True)
        self.exitDialog.setObjectName("buttonBox")
        
        self.exitLabel = QtWidgets.QLabel(self.exit)
        self.exitLabel.setGeometry(QtCore.QRect(105, 30, 161, 71))
        self.exitLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.exitLabel.setWordWrap(True)
        self.exitLabel.setObjectName("label")

        ### BUTTON ACTION LINK ## 

        self.retranslateExit()
        self.exitDialog.accepted.connect(self.killUi)
        self.exitDialog.rejected.connect(self.exit.destroy)

        ### UI FORMAT AND EXECUTION ###

        self.exitLayout.addWidget(self.exitLabel, 0, 0)
        self.exitLayout.addWidget(self.exitDialog, 1, 0)
        self.exit.setLayout(self.exitLayout)

        self.exit.show()

    def killUi(self):
        self.exit.destroy()
        closeSQL(sqlConnect)
        self.destroy()
        sys.exit()
        
    def retranslateExit(self):
        _translate = QtCore.QCoreApplication.translate
        self.exit.setWindowTitle(_translate("Exit Window", "Dialog"))
        self.exitLabel.setText(_translate("ExitWindow", "Are you sure you want to quit?"))
            
########################## Primary Code ##########################
def main():
    initMQTT(client)
    initSQL(sqlConnect)
    
    application = QtWidgets.QApplication(sys.argv)
    window = Ui_Form()
    window.setupUi()
    window.show()

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
