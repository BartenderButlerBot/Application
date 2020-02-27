# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stackedFinalSetup.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

import sys
import paho.mqtt.client as mqtt
import sqlite3
from sqlite3 import Error
from PyQt5 import QtCore, QtGui, QtWidgets

client = None 
MQTT_SERVER = "192.168.1.75"
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
    client.connect(MQTT_SERVER, MQTT_PORT)
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

class Ui_B3GUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("B3 GUI")
        self.setGeometry(0, 0, 1024, 600)
        #self.setWindowIcon(QtGui.Icon('B3symbol.png'))
        _translate = QtCore.QCoreApplication.translate
        self.exit = QtWidgets.QDialog()

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
        
        self.stackedWidget = QtWidgets.QStackedWidget(self)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 1024, 600))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 87, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 87, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 87, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 87, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.stackedWidget.setPalette(palette)
        self.stackedWidget.setObjectName("stackedWidget")

        self.setupPrimary()
        self.show()
    
    def setupPrimary(self):

        _translate = QtCore.QCoreApplication.translate
        
        ##################### Page 1 #####################
        
        self.page = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page.sizePolicy().hasHeightForWidth())
        self.page.setSizePolicy(sizePolicy)
        self.page.setObjectName("page")
        self.pushButton_config = QtWidgets.QPushButton(self.page)
        self.pushButton_config.setGeometry(QtCore.QRect(820, 30, 161, 61))
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
        self.pushButton_config.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MathJax_Main")
        self.pushButton_config.setFont(font)
        self.pushButton_config.setObjectName("pushButton_config")
        self.pushButton_toMenu = QtWidgets.QPushButton(self.page)
        self.pushButton_toMenu.setGeometry(QtCore.QRect(40, 40, 621, 201))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.pushButton_toMenu.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        font.setPointSize(60)
        self.pushButton_toMenu.setFont(font)
        self.pushButton_toMenu.setObjectName("pushButton_toMenu")

        self.pushButton_toMenu.clicked.connect(self.toMenu)
        
        self.progressBar_config_dynamicLater2 = QtWidgets.QProgressBar(self.page)
        self.progressBar_config_dynamicLater2.setGeometry(QtCore.QRect(890, 220, 118, 31))
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
        self.progressBar_config_dynamicLater2.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Piboto Thin")
        self.progressBar_config_dynamicLater2.setFont(font)
        self.progressBar_config_dynamicLater2.setProperty("value", 100)
        self.progressBar_config_dynamicLater2.setObjectName("progressBar_config_dynamicLater2")
        self.progressBar_config_dynamicLater4 = QtWidgets.QProgressBar(self.page)
        self.progressBar_config_dynamicLater4.setGeometry(QtCore.QRect(890, 300, 118, 31))
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
        self.progressBar_config_dynamicLater4.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Piboto Thin")
        self.progressBar_config_dynamicLater4.setFont(font)
        self.progressBar_config_dynamicLater4.setProperty("value", 100)
        self.progressBar_config_dynamicLater4.setObjectName("progressBar_config_dynamicLater4")
        self.label_config_dynamicLater3 = QtWidgets.QLabel(self.page)
        self.label_config_dynamicLater3.setGeometry(QtCore.QRect(780, 260, 90, 28))
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.label_config_dynamicLater3.setFont(font)
        self.label_config_dynamicLater3.setObjectName("label_config_dynamicLater3")
        self.progressBar_config_dynamicLater1 = QtWidgets.QProgressBar(self.page)
        self.progressBar_config_dynamicLater1.setGeometry(QtCore.QRect(890, 180, 118, 31))
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
        self.progressBar_config_dynamicLater1.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Piboto Thin")
        self.progressBar_config_dynamicLater1.setFont(font)
        self.progressBar_config_dynamicLater1.setProperty("value", 94)
        self.progressBar_config_dynamicLater1.setObjectName("progressBar_config_dynamicLater1")
        self.label_imageB3 = QtWidgets.QLabel(self.page)
        self.label_imageB3.setGeometry(QtCore.QRect(920, 540, 90, 28))
        self.label_imageB3.setText("")
        self.label_imageB3.setObjectName("label_imageB3")
        self.line = QtWidgets.QFrame(self.page)
        self.line.setGeometry(QtCore.QRect(380, 370, 271, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_curOrder_DynamicLaterName = QtWidgets.QLabel(self.page)
        self.label_curOrder_DynamicLaterName.setGeometry(QtCore.QRect(380, 420, 121, 28))
        self.label_curOrder_DynamicLaterName.setObjectName("label_curOrder_DynamicLaterName")
        self.label_config_dynamicLater1 = QtWidgets.QLabel(self.page)
        self.label_config_dynamicLater1.setGeometry(QtCore.QRect(780, 180, 90, 28))
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.label_config_dynamicLater1.setFont(font)
        self.label_config_dynamicLater1.setObjectName("label_config_dynamicLater1")
        self.widget_rightInfo = QtWidgets.QListWidget(self.page)
        self.widget_rightInfo.setGeometry(QtCore.QRect(770, 0, 254, 600))
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
        self.widget_rightInfo.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.widget_rightInfo.setFont(font)
        self.widget_rightInfo.setObjectName("widget_rightInfo")
        self.widget_curOrder = QtWidgets.QListWidget(self.page)
        self.widget_curOrder.setGeometry(QtCore.QRect(370, 290, 291, 251))
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
        self.widget_curOrder.setPalette(palette)
        self.widget_curOrder.setObjectName("widget_curOrder")
        self.label_config_dynamicLater4 = QtWidgets.QLabel(self.page)
        self.label_config_dynamicLater4.setGeometry(QtCore.QRect(780, 300, 90, 28))
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.label_config_dynamicLater4.setFont(font)
        self.label_config_dynamicLater4.setObjectName("label_config_dynamicLater4")
        self.label_curOrder_IngAmount = QtWidgets.QLabel(self.page)
        self.label_curOrder_IngAmount.setGeometry(QtCore.QRect(560, 390, 90, 28))
        self.label_curOrder_IngAmount.setObjectName("label_curOrder_IngAmount")
        self.pushButton_curOrder = QtWidgets.QPushButton(self.page)
        self.pushButton_curOrder.setGeometry(QtCore.QRect(40, 290, 291, 111))
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
        self.pushButton_curOrder.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        font.setPointSize(26)
        self.pushButton_curOrder.setFont(font)
        self.pushButton_curOrder.setObjectName("pushButton_curOrder")
        self.pushButton_quit = QtWidgets.QPushButton(self.page)
        self.pushButton_quit.setGeometry(QtCore.QRect(240, 450, 90, 90))
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
        self.pushButton_quit.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MathJax_Main")
        self.pushButton_quit.setFont(font)
        self.pushButton_quit.setObjectName("pushButton_quit")

        self.pushButton_quit.clicked.connect(self.exitPopup)
        
        self.label_config = QtWidgets.QLabel(self.page)
        self.label_config.setGeometry(QtCore.QRect(780, 140, 90, 28))
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.label_config.setFont(font)
        self.label_config.setObjectName("label_config")
        self.label_curOrder = QtWidgets.QLabel(self.page)
        self.label_curOrder.setGeometry(QtCore.QRect(380, 310, 151, 28))
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.label_curOrder.setFont(font)
        self.label_curOrder.setObjectName("label_curOrder")
        self.pushButton_dock = QtWidgets.QPushButton(self.page)
        self.pushButton_dock.setGeometry(QtCore.QRect(140, 450, 90, 90))
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
        self.pushButton_dock.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MathJax_Main")
        self.pushButton_dock.setFont(font)
        self.pushButton_dock.setObjectName("pushButton_dock")
        self.progressBar_batteryCharge = QtWidgets.QProgressBar(self.page)
        self.progressBar_batteryCharge.setGeometry(QtCore.QRect(800, 540, 101, 31))
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
        self.progressBar_batteryCharge.setPalette(palette)
        self.progressBar_batteryCharge.setProperty("value", 100)
        self.progressBar_batteryCharge.setObjectName("progressBar_batteryCharge")
        self.progressBar_config_dynamicLater3 = QtWidgets.QProgressBar(self.page)
        self.progressBar_config_dynamicLater3.setGeometry(QtCore.QRect(890, 260, 118, 31))
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
        self.progressBar_config_dynamicLater3.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Piboto Thin")
        self.progressBar_config_dynamicLater3.setFont(font)
        self.progressBar_config_dynamicLater3.setProperty("value", 100)
        self.progressBar_config_dynamicLater3.setObjectName("progressBar_config_dynamicLater3")
        self.label_curOrder_Name = QtWidgets.QLabel(self.page)
        self.label_curOrder_Name.setGeometry(QtCore.QRect(380, 340, 141, 28))
        font = QtGui.QFont()
        font.setFamily("MathJax_Main")
        self.label_curOrder_Name.setFont(font)
        self.label_curOrder_Name.setObjectName("label_curOrder_Name")
        self.progressBar_config = QtWidgets.QProgressBar(self.page)
        self.progressBar_config.setGeometry(QtCore.QRect(890, 140, 118, 31))
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
        self.progressBar_config.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Piboto Thin")
        self.progressBar_config.setFont(font)
        self.progressBar_config.setProperty("value", 80)
        self.progressBar_config.setObjectName("progressBar_config")
        self.label_curOrder_DynamicLaterAmt = QtWidgets.QLabel(self.page)
        self.label_curOrder_DynamicLaterAmt.setGeometry(QtCore.QRect(560, 420, 90, 28))
        self.label_curOrder_DynamicLaterAmt.setObjectName("label_curOrder_DynamicLaterAmt")
        self.label_curOrder_IngName = QtWidgets.QLabel(self.page)
        self.label_curOrder_IngName.setGeometry(QtCore.QRect(380, 390, 121, 28))
        self.label_curOrder_IngName.setObjectName("label_curOrder_IngName")
        self.label_config_dynamicLater2 = QtWidgets.QLabel(self.page)
        self.label_config_dynamicLater2.setGeometry(QtCore.QRect(780, 220, 90, 28))
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.label_config_dynamicLater2.setFont(font)
        self.label_config_dynamicLater2.setObjectName("label_config_dynamicLater2")
        self.pushButton_advTools = QtWidgets.QPushButton(self.page)
        self.pushButton_advTools.setGeometry(QtCore.QRect(40, 450, 90, 90))
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
        self.pushButton_advTools.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MathJax_Main")
        self.pushButton_advTools.setFont(font)
        self.pushButton_advTools.setObjectName("pushButton_advTools")
        self.label_batteryCharge = QtWidgets.QLabel(self.page)
        self.label_batteryCharge.setGeometry(QtCore.QRect(780, 510, 141, 28))
        font = QtGui.QFont()
        font.setFamily("MathJax_Main")
        self.label_batteryCharge.setFont(font)
        self.label_batteryCharge.setObjectName("label_batteryCharge")
        self.pushButton_toMenu.raise_()
        self.widget_rightInfo.raise_()
        self.widget_curOrder.raise_()
        self.label_curOrder_IngAmount.raise_()
        self.pushButton_curOrder.raise_()
        self.pushButton_quit.raise_()
        self.label_config.raise_()
        self.label_curOrder.raise_()
        self.pushButton_dock.raise_()
        self.progressBar_batteryCharge.raise_()
        self.progressBar_config_dynamicLater3.raise_()
        self.label_curOrder_Name.raise_()
        self.label_curOrder_DynamicLaterAmt.raise_()
        self.label_curOrder_IngName.raise_()
        self.label_config_dynamicLater2.raise_()
        self.pushButton_advTools.raise_()
        self.label_batteryCharge.raise_()
        self.line.raise_()
        self.label_imageB3.raise_()
        self.label_config_dynamicLater1.raise_()
        self.label_config_dynamicLater3.raise_()
        self.label_config_dynamicLater4.raise_()
        self.progressBar_config.raise_()
        self.progressBar_config_dynamicLater1.raise_()
        self.progressBar_config_dynamicLater2.raise_()
        self.progressBar_config_dynamicLater4.raise_()
        self.label_curOrder_DynamicLaterName.raise_()
        self.pushButton_config.raise_()
        
        self.stackedWidget.addWidget(self.page)

        ##################### Page 2 #####################
        
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.pushButton_pageToPrimary = QtWidgets.QPushButton(self.page_2)
        self.pushButton_pageToPrimary.setGeometry(QtCore.QRect(11, 441, 131, 111))
        self.pushButton_pageToPrimary.setObjectName("pushButton_pageToPrimary")
        self.pushButton_pageToPrimary.setText(_translate("B3GUI", "Main Window"))

        self.pushButton_pageToPrimary.clicked.connect(self.toPrimary)

        self.pushButton_pageToCustom = QtWidgets.QPushButton(self.page_2)
        self.pushButton_pageToCustom.setGeometry(QtCore.QRect(11, 311, 131, 111))
        self.pushButton_pageToCustom.setObjectName("pushButton_pageToCustom")
        self.pushButton_pageToCustom.setText(_translate("B3GUI", "Custom Order"))

        self.pushButton_pageToCustom.clicked.connect(self.toCustom)

        self.scrollArea_menu = QtWidgets.QScrollArea(self.page_2)
        self.scrollArea_menu.setGeometry(QtCore.QRect(150, 20, 721, 561))
        self.scrollArea_menu.setWidgetResizable(True)
        self.scrollArea_menu.setObjectName("scrollArea_menu")
        self.scrollArea_menuContents = QtWidgets.QWidget()
        self.scrollArea_menuContents.setGeometry(QtCore.QRect(0, 0, 719, 559))
        self.scrollArea_menuContents.setObjectName("scrollArea_menuContents")
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.scrollArea_menuContents)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(10, 10, 701, 541))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_menu = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_menu.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_menu.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_menu.setObjectName("gridLayout_menu")

        numRecipe = 5

        for i in range(numRecipe):
            verticalLayout_menuRecipe = QtWidgets.QVBoxLayout()
            verticalLayout_menuRecipe.setObjectName("verticalLayout_menuRecipe")
                                             
            label_recipeName = QtWidgets.QLabel(self.gridLayoutWidget_4)                            
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(label_recipeName.sizePolicy().hasHeightForWidth())
            label_recipeName.setSizePolicy(sizePolicy)
            label_recipeName.setMinimumSize(QtCore.QSize(0, 199))
            label_recipeName.setObjectName("label_recipeName")
            label_recipeName.setText(_translate("B3GUI", "NameofDrink"))
            verticalLayout_menuRecipe.addWidget(label_recipeName)
                                             
            line_menuRecipe = QtWidgets.QFrame(self.gridLayoutWidget_4)
            line_menuRecipe.setFrameShape(QtWidgets.QFrame.HLine)
            line_menuRecipe.setFrameShadow(QtWidgets.QFrame.Sunken)
            line_menuRecipe.setObjectName("line_menuRecipe")
            verticalLayout_menuRecipe.addWidget(line_menuRecipe)

            
            if (i%2 == 1):
                spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.gridLayout_menu.addItem(spacerItem, (int((i-1)/2)), 1, 1, 1)

            numIng = 3

            for j in range(numIng):
                label_recipeIng = QtWidgets.QLabel(self.gridLayoutWidget_4)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(label_recipeIng.sizePolicy().hasHeightForWidth())
                label_recipeIng.setSizePolicy(sizePolicy)
                label_recipeIng.setMinimumSize(QtCore.QSize(0, 13))
                label_recipeIng.setObjectName("label_recipeIng" + str(j + 1))
                verticalLayout_menuRecipe.addWidget(label_recipeIng)
                label_recipeIng.setText(_translate("B3GUI", "Ingredient " + str(j + 1)))
          
            self.gridLayout_menu.addLayout(verticalLayout_menuRecipe, int(i/2), int(2*(i%2)), 1, 1)

            if (numRecipe == 1):
                verticalLayout_menuRecipe = QtWidgets.QVBoxLayout()
                verticalLayout_menuRecipe.setObjectName("verticalLayout_menuRecipe")
                                                 
                label_recipeName = QtWidgets.QLabel(self.gridLayoutWidget_4)                            
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(label_recipeName.sizePolicy().hasHeightForWidth())
                label_recipeName.setSizePolicy(sizePolicy)
                label_recipeName.setMinimumSize(QtCore.QSize(0, 199))
                label_recipeName.setObjectName("label_recipeName")
                label_recipeName.setText(_translate("B3GUI", " "))
                verticalLayout_menuRecipe.addWidget(label_recipeName)

                numIng = 3

                for j in range(numIng):
                    label_recipeIng = QtWidgets.QLabel(self.gridLayoutWidget_4)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(label_recipeIng.sizePolicy().hasHeightForWidth())
                    label_recipeIng.setSizePolicy(sizePolicy)
                    label_recipeIng.setMinimumSize(QtCore.QSize(0, 13))
                    label_recipeIng.setObjectName("label_recipeIng" + str(j + 1))
                    verticalLayout_menuRecipe.addWidget(label_recipeIng)
                    label_recipeIng.setText(_translate("B3GUI", " "))
          
            self.gridLayout_menu.addLayout(verticalLayout_menuRecipe, 0, 2, 1, 1)
        
        self.scrollArea_menu.setWidget(self.scrollArea_menuContents)
        
        self.stackedWidget.addWidget(self.page_2)

        ##################### Page 3 #####################

        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.widget_3 = QtWidgets.QWidget(self.page_3)
        self.widget_3.setGeometry(QtCore.QRect(150, 20, 721, 561))
        self.widget_3.setAutoFillBackground(False)
        self.widget_3.setObjectName("widget_3")
        self.scrollArea_custom = QtWidgets.QScrollArea(self.widget_3)
        self.scrollArea_custom.setGeometry(QtCore.QRect(0, 0, 721, 561))
        self.scrollArea_custom.setWidgetResizable(True)
        self.scrollArea_custom.setObjectName("scrollArea_custom")
        self.scrollArea_cudtomContents = QtWidgets.QWidget()
        self.scrollArea_cudtomContents.setGeometry(QtCore.QRect(0, 0, 719, 559))
        self.scrollArea_cudtomContents.setObjectName("scrollArea_cudtomContents")
        self.gridLayoutWidget_6 = QtWidgets.QWidget(self.scrollArea_cudtomContents)
        self.gridLayoutWidget_6.setGeometry(QtCore.QRect(10, 10, 671, 471))
        self.gridLayoutWidget_6.setObjectName("gridLayoutWidget_6")
        self.gridLayout_custom = QtWidgets.QGridLayout(self.gridLayoutWidget_6)
        self.gridLayout_custom.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_custom.setObjectName("gridLayout_custom")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_custom.addItem(spacerItem1, 0, 1, 1, 1)
        self.gridLayout_customRecipe = QtWidgets.QGridLayout()
        self.gridLayout_customRecipe.setObjectName("gridLayout_customRecipe")
        self.label_51 = QtWidgets.QLabel(self.gridLayoutWidget_6)
        self.label_51.setObjectName("label_51")
        self.gridLayout_customRecipe.addWidget(self.label_51, 3, 0, 1, 1)
        self.label_52 = QtWidgets.QLabel(self.gridLayoutWidget_6)
        self.label_52.setObjectName("label_52")
        self.gridLayout_customRecipe.addWidget(self.label_52, 2, 0, 1, 1)
        self.label_53 = QtWidgets.QLabel(self.gridLayoutWidget_6)
        self.label_53.setObjectName("label_53")
        self.gridLayout_customRecipe.addWidget(self.label_53, 4, 0, 1, 1)
        self.line_9 = QtWidgets.QFrame(self.gridLayoutWidget_6)
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.gridLayout_customRecipe.addWidget(self.line_9, 1, 0, 1, 1)
        self.label_54 = QtWidgets.QLabel(self.gridLayoutWidget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_54.sizePolicy().hasHeightForWidth())
        self.label_54.setSizePolicy(sizePolicy)
        self.label_54.setMinimumSize(QtCore.QSize(0, 50))
        self.label_54.setObjectName("label_54")
        self.gridLayout_customRecipe.addWidget(self.label_54, 0, 0, 1, 1)
        self.gridLayout_custom.addLayout(self.gridLayout_customRecipe, 0, 0, 1, 1)
        self.gridLayout_12 = QtWidgets.QGridLayout()
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.label_55 = QtWidgets.QLabel(self.gridLayoutWidget_6)
        self.label_55.setObjectName("label_55")
        self.gridLayout_12.addWidget(self.label_55, 3, 0, 1, 1)
        self.label_56 = QtWidgets.QLabel(self.gridLayoutWidget_6)
        self.label_56.setObjectName("label_56")
        self.gridLayout_12.addWidget(self.label_56, 2, 0, 1, 1)
        self.label_57 = QtWidgets.QLabel(self.gridLayoutWidget_6)
        self.label_57.setObjectName("label_57")
        self.gridLayout_12.addWidget(self.label_57, 4, 0, 1, 1)
        self.line_10 = QtWidgets.QFrame(self.gridLayoutWidget_6)
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.gridLayout_12.addWidget(self.line_10, 1, 0, 1, 1)
        self.label_58 = QtWidgets.QLabel(self.gridLayoutWidget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_58.sizePolicy().hasHeightForWidth())
        self.label_58.setSizePolicy(sizePolicy)
        self.label_58.setMinimumSize(QtCore.QSize(0, 50))
        self.label_58.setObjectName("label_58")
        self.gridLayout_12.addWidget(self.label_58, 0, 0, 1, 1)
        self.gridLayout_custom.addLayout(self.gridLayout_12, 0, 2, 1, 1)
        self.scrollArea_custom.setWidget(self.scrollArea_cudtomContents)
        self.pushButton_pageToMenu2 = QtWidgets.QPushButton(self.page_3)
        self.pushButton_pageToMenu2.setGeometry(QtCore.QRect(11, 311, 131, 111))
        self.pushButton_pageToMenu2.setObjectName("pushButton_pageToMenu2")
        
        self.pushButton_pageToMenu2.clicked.connect(self.toMenu)

        self.pushButton_pageToPrimary2 = QtWidgets.QPushButton(self.page_3)
        self.pushButton_pageToPrimary2.setGeometry(QtCore.QRect(11, 441, 131, 111))
        self.pushButton_pageToPrimary2.setObjectName("pushButton_pageToPrimary2")

        self.pushButton_pageToPrimary2.clicked.connect(self.toPrimary)

        self.stackedWidget.addWidget(self.page_3)

        self.retranslateUi()
        self.stackedWidget.setCurrentIndex(0)
        #QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("B3GUI", "B3GUI"))
        self.pushButton_config.setText(_translate("B3GUI", "Drink\n"
"Configuration"))
        self.pushButton_toMenu.setText(_translate("B3GUI", "Menu"))
        self.label_config_dynamicLater3.setText(_translate("B3GUI", "Ing. D"))
        self.label_curOrder_DynamicLaterName.setText(_translate("B3GUI", "Ingredient B"))
        self.label_config_dynamicLater1.setText(_translate("B3GUI", "Ing. B"))
        self.label_config_dynamicLater4.setText(_translate("B3GUI", "Ing. E"))
        self.label_curOrder_IngAmount.setText(_translate("B3GUI", "300 mL"))
        self.pushButton_curOrder.setText(_translate("B3GUI", "Quick Order"))
        self.pushButton_quit.setText(_translate("B3GUI", "Quit"))
        self.label_config.setText(_translate("B3GUI", "Ing. A"))
        self.label_curOrder.setText(_translate("B3GUI", "Current Order:"))
        self.pushButton_dock.setText(_translate("B3GUI", "Dock"))
        self.label_curOrder_Name.setText(_translate("B3GUI", "Test Order 1"))
        self.label_curOrder_DynamicLaterAmt.setText(_translate("B3GUI", "45 mL"))
        self.label_curOrder_IngName.setText(_translate("B3GUI", "Ingredient A"))
        self.label_config_dynamicLater2.setText(_translate("B3GUI", "Ing. C"))
        self.pushButton_advTools.setText(_translate("B3GUI", "Adv. \n"
"Tools"))
        self.label_batteryCharge.setText(_translate("B3GUI", "Battery Charge"))


        '''
        self.pushButton_pageToPrimary.setText(_translate("B3GUI", "Main Window"))
        self.pushButton_pageToCustom.setText(_translate("B3GUI", "Custom Order"))
        self.label_recipeName.setText(_translate("B3GUI", "NameofDrink"))
        self.label_recipeIng1.setText(_translate("B3GUI", "Ingredient 1"))
        self.label_recipeIngDynamicLater.setText(_translate("B3GUI", "Ingredient 2"))
        self.label_recipeIngDynamicLater2.setText(_translate("B3GUI", "Ingredient 3"))
        self.label_recipeName_2.setText(_translate("B3GUI", "NameofDrink"))
        self.label_recipeIng1_2.setText(_translate("B3GUI", "Ingredient 1"))
        self.label_recipeIngDynamicLater_2.setText(_translate("B3GUI", "Ingredient 2"))
        self.label_recipeIngDynamicLater2_2.setText(_translate("B3GUI", "Ingredient 3"))
        self.label_recipeName_3.setText(_translate("B3GUI", "NameofDrink"))
        self.label_recipeIng1_3.setText(_translate("B3GUI", "Ingredient 1"))
        self.label_recipeIngDynamicLater_3.setText(_translate("B3GUI", "Ingredient 2"))
        self.label_recipeIngDynamicLater2_3.setText(_translate("B3GUI", "Ingredient 3"))
        self.label_recipeName_4.setText(_translate("B3GUI", "NameofDrink"))
        self.label_recipeIng1_4.setText(_translate("B3GUI", "Ingredient 1"))
        self.label_recipeIngDynamicLater_4.setText(_translate("B3GUI", "Ingredient 2"))
        self.label_recipeIngDynamicLater2_4.setText(_translate("B3GUI", "Ingredient 3"))
'''

        
        self.label_51.setText(_translate("B3GUI", "Ingredient 2"))
        self.label_52.setText(_translate("B3GUI", "Ingredient 1"))
        self.label_53.setText(_translate("B3GUI", "Ingredient 3"))
        self.label_54.setText(_translate("B3GUI", "Temp Curstom Drank Layout"))
        self.label_55.setText(_translate("B3GUI", "Ingredient 2"))
        self.label_56.setText(_translate("B3GUI", "Ingredient 1"))
        self.label_57.setText(_translate("B3GUI", "Ingredient 3"))
        self.label_58.setText(_translate("B3GUI", "This is not currently finalized"))
        self.pushButton_pageToMenu2.setText(_translate("B3GUI", "Menu"))
        self.pushButton_pageToPrimary2.setText(_translate("B3GUI", "Main Window"))

    def toMenu(self):
        self.stackedWidget.setCurrentIndex(1)

    def toCustom(self):
        self.stackedWidget.setCurrentIndex(2)

    def toPrimary(self):
        self.stackedWidget.setCurrentIndex(0)


    def exitPopup(self):
        self.exit.setObjectName("ExitWindow")
        self.exit.setGeometry(332, 350, 360, 150)
        self.exitLayout = QtWidgets.QGridLayout()

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
        self.exit.setPalette(palette)
        
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

        self.exit.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        
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
    window = Ui_B3GUI()

    client.loop_start()

    sys.exit(application.exec_())

if __name__ == '__main__':
    #try:
    main()
