# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'finalGui.ui'
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
MQTT_SERVER = "192.168.1.77"
MQTT_SERVERP = "192.168.1.68"
MQTT_SERVERC = "172.16.105.218"
MQTT_SERVERC2 = "Core"
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
orderName = "Test Order 1"
batteryCharge = "Battery Charge"
configIng1Name = "Ing. A"
configIng3Name = "Ing. C"
configIng5Name = "Ing. E"
configIng4Name = "Ing. D"
configIng2Name = "Ing. B"
currentOrderIng1Name = "Ingredient A"
currentOrderIng2Name = "Ingredient B"
currentOrderIng1Amount =  "300 mL"
currentOrderIng2Amount = "45 mL"

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
    client.connect(MQTT_SERVERC, MQTT_PORT)
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
        
class Ui_Primary_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("B3 GUI")
        self.setGeometry(0, 0, 1024, 600)
        #self.setWindowIcon(QtGui.Icon('B3symbol.png'))
        self.exit = QtWidgets.QDialog()

        self.setupPrimary()
        self.show()
    
    def setupPrimary(self):
        
        #lastOrderTuple = ('recipe Name', 'ing. type', 'ing. name', 'ing. amount')        
        palette = QtGui.QPalette()
        
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(85, 87, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        
        self.setPalette(palette)

        
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(40, 40, 621, 201))
        
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        
        self.pushButton.setPalette(palette)
        
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        font.setPointSize(60)
        
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 290, 291, 111))
        
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(85, 87, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        
        self.pushButton_2.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        font.setPointSize(26)
        
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 450, 90, 90))
        
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(85, 87, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        
        self.pushButton_3.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MathJax_Main")
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self)
        self.pushButton_4.setGeometry(QtCore.QRect(140, 450, 90, 90))
        
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(85, 87, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        
        self.pushButton_4.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MathJax_Main")
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self)
        self.pushButton_5.setGeometry(QtCore.QRect(240, 450, 90, 90))
        
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(85, 87, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        
        self.pushButton_5.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MathJax_Main")
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self)
        self.pushButton_6.setGeometry(QtCore.QRect(820, 30, 161, 61))
        
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(186, 189, 182))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(186, 189, 182))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(186, 189, 182))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        
        self.pushButton_6.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MathJax_Main")
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")
        self.BatteryCharge = QtWidgets.QProgressBar(self)
        self.BatteryCharge.setGeometry(QtCore.QRect(800, 540, 101, 31))
        
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(115, 210, 22))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(115, 210, 22))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(145, 145, 145))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        
        self.BatteryCharge.setPalette(palette)
        self.BatteryCharge.setProperty("value", 100)
        self.BatteryCharge.setObjectName("BatteryCharge")
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setGeometry(QtCore.QRect(770, 0, 254, 600))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 87, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(85, 87, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)

        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(85, 87, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(85, 87, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        
        self.listWidget.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.listWidget.setFont(font)
        self.listWidget.setObjectName("listWidget")
        self.listWidget_2 = QtWidgets.QListWidget(self)
        self.listWidget_2.setGeometry(QtCore.QRect(370, 290, 291, 251))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 87, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 87, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 87, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 87, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.listWidget_2.setPalette(palette)
        self.listWidget_2.setObjectName("listWidget_2")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(380, 310, 151, 28))
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(380, 340, 141, 28))
        font = QtGui.QFont()
        font.setFamily("MathJax_Main")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(780, 510, 141, 28))
        font = QtGui.QFont()
        font.setFamily("MathJax_Main")
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(890, 140, 118, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(252, 233, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(252, 233, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(145, 145, 145))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, brush)
        self.progressBar.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Piboto Thin")
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 80)
        self.progressBar.setObjectName("progressBar")
        self.progressBar_2 = QtWidgets.QProgressBar(self)
        self.progressBar_2.setGeometry(QtCore.QRect(890, 180, 118, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(252, 233, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(252, 233, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(145, 145, 145))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, brush)
        self.progressBar_2.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Piboto Thin")
        self.progressBar_2.setFont(font)
        self.progressBar_2.setProperty("value", 94)
        self.progressBar_2.setObjectName("progressBar_2")
        self.progressBar_3 = QtWidgets.QProgressBar(self)
        self.progressBar_3.setGeometry(QtCore.QRect(890, 220, 118, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(252, 233, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(252, 233, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(145, 145, 145))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, brush)
        self.progressBar_3.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Piboto Thin")
        
        self.progressBar_3.setFont(font)
        self.progressBar_3.setProperty("value", 100)
        self.progressBar_3.setObjectName("progressBar_3")
        self.progressBar_4 = QtWidgets.QProgressBar(self)
        self.progressBar_4.setGeometry(QtCore.QRect(890, 300, 118, 31))
        
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(252, 233, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(252, 233, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(145, 145, 145))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, brush)
        self.progressBar_4.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Piboto Thin")
        self.progressBar_4.setFont(font)
        self.progressBar_4.setProperty("value", 100)
        self.progressBar_4.setObjectName("progressBar_4")
        self.progressBar_5 = QtWidgets.QProgressBar(self)
        self.progressBar_5.setGeometry(QtCore.QRect(890, 260, 118, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(252, 233, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(252, 233, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(145, 145, 145))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, brush)
        self.progressBar_5.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Piboto Thin")
        self.progressBar_5.setFont(font)
        self.progressBar_5.setProperty("value", 100)
        self.progressBar_5.setObjectName("progressBar_5")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(780, 140, 90, 28))
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(780, 220, 90, 28))
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setGeometry(QtCore.QRect(780, 300, 90, 28))
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self)
        self.label_7.setGeometry(QtCore.QRect(780, 260, 90, 28))
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self)
        self.label_8.setGeometry(QtCore.QRect(780, 180, 90, 28))
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self)
        self.label_9.setGeometry(QtCore.QRect(920, 540, 90, 28))
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(380, 370, 271, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_10 = QtWidgets.QLabel(self)
        self.label_10.setGeometry(QtCore.QRect(380, 390, 121, 28))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self)
        self.label_11.setGeometry(QtCore.QRect(380, 420, 121, 28))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self)
        self.label_12.setGeometry(QtCore.QRect(560, 390, 90, 28))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self)
        self.label_13.setGeometry(QtCore.QRect(560, 420, 90, 28))
        self.label_13.setObjectName("label_13")
        
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        self.pushButton_4.raise_()
        self.pushButton_5.raise_()
        self.listWidget.raise_()
        self.BatteryCharge.raise_()
        self.pushButton_6.raise_()
        self.listWidget_2.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.progressBar.raise_()
        self.progressBar_2.raise_()
        self.progressBar_3.raise_()
        self.progressBar_4.raise_()
        self.progressBar_5.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.label_9.raise_()
        self.line.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.label_12.raise_()
        self.label_13.raise_()

        self.retranslateUi(self)
        self.pushButton.clicked.connect(self.openMenuShell)
        self.pushButton_5.clicked.connect(self.exitPopup)
        #QtCore.QMetaObject.connectSlotsByName(Form)
        
        self.qTimer = QtCore.QTimer()
        self.qTimer.setInterval(777)
        self.qTimer.timeout.connect(self.refreshUi)
        self.qTimer.start()
        
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "B3 GUI"))
        self.pushButton.setText(_translate("Form", "Menu"))
        self.pushButton_2.setText(_translate("Form", "Quick Order"))
        self.pushButton_3.setText(_translate("Form", "Adv. \n"
"Tools"))
        self.pushButton_4.setText(_translate("Form", "Dock"))
        self.pushButton_5.setText(_translate("Form", "Quit"))
        self.pushButton_6.setText(_translate("Form", "Drink\n"
"Configuration"))
        self.label.setText(_translate("Form", "Current Order:"))
        self.label_2.setText(_translate("Form", "Test Order 1"))
        self.label_3.setText(_translate("Form", "Battery Charge"))
        self.label_4.setText(_translate("Form", "Ing. A"))
        self.label_5.setText(_translate("Form", "Ing. C"))
        self.label_6.setText(_translate("Form", "Ing. E"))
        self.label_7.setText(_translate("Form", "Ing. D"))
        self.label_8.setText(_translate("Form", "Ing. B"))
        self.label_10.setText(_translate("Form", "Ingredient A"))
        self.label_11.setText(_translate("Form", "Ingredient B"))
        self.label_12.setText(_translate("Form", "300 mL"))
        self.label_13.setText(_translate("Form", "45 mL"))

    def refreshUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_2.setText(_translate("Form", orderName))
        self.label_3.setText(_translate("Form", batteryCharge))
        self.label_4.setText(_translate("Form", configIng1Name))
        self.label_5.setText(_translate("Form", configIng3Name))
        self.label_6.setText(_translate("Form", configIng5Name))
        self.label_7.setText(_translate("Form", configIng4Name))
        self.label_8.setText(_translate("Form", configIng2Name))
        self.label_10.setText(_translate("Form", currentOrderIng1Name))
        self.label_11.setText(_translate("Form", currentOrderIng2Name))
        self.label_12.setText(_translate("Form", currentOrderIng1Amount))
        self.label_13.setText(_translate("Form", currentOrderIng2Amount))

    def openMenuShell(self):
        self.window = QtWidgets
        
    def exitPopup(self):
        self.exit.setObjectName("ExitWindow")
        self.exit.setGeometry(332, 350, 360, 150)
        self.exitLayout = QtWidgets.QGridLayout()

        
        self.exitDialog = QtWidgets.QDialogButtonBox(self.exit)
        self.exitDialog.setGeometry(QtCore.QRect(90, 110, 180, 32))
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exitDialog.sizePolicy().hasHeightForWidth())
        
        self.exitDialog.setSizePolicy(sizePolicy)
        self.exitDialog.setOrientation(QtCore.Qt.Horizontal)
        self.exitDialog.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.exitDialog.setCenterButtons(True)
        self.exitDialog.setObjectName("buttonBox")
        self.exitLabel = QtWidgets.QLabel(self.exit)
        self.exitLabel.setGeometry(QtCore.QRect(105, 30, 161, 71))
        self.exitLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.exitLabel.setWordWrap(True)
        self.exitLabel.setObjectName("label")

        self.retranslateExit()
        self.exitDialog.accepted.connect(self.killUi)
        self.exitDialog.rejected.connect(self.exit.destroy)

        self.exitLayout.addWidget(self.exitLabel, 0, 0)
        self.exitLayout.addWidget(self.exitDialog, 1, 0)
        self.exit.setLayout(self.exitLayout)
        
        self.exit.show()

    def killUi(self):
        #self.exit.getdfsdfogjh()
        self.exit.destroy()
        closeSQL(sqlConnect)
        QtCore.QCoreApplication.instance().quit
        sys.exit()

    def retranslateExit(self):
        _translate = QtCore.QCoreApplication.translate
        self.exit.setWindowTitle(_translate("ExitWindow", "Dialog"))
        self.exitLabel.setText(_translate("ExitWindow", "Are you sure you want to quit?"))


def main():
    initMQTT(client)
    initSQL(sqlConnect)

    application = QtWidgets.QApplication(sys.argv)
    application.setStyle('Fusion')   
    window = Ui_Primary_Window()

    client.loop_start()
    
    sys.exit(application.exec_())


if __name__ == '__main__':
    #try:
    main()

    #except Exception as e:
        #sys.stderr.write("Error: {0}".format(e))
