# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stackedFinalSetup.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

import sys, time
import paho.mqtt.client as mqtt
import sqlite3
from sqlite3 import Error
from PyQt5 import QtCore, QtGui, QtWidgets

client = None 
MQTT_SERVER = "192.168.1.78"
MQTT_SERVERC = "Core"
MQTT_PORT = 1883
MQTT_USERNAME = ""
MQTT_PASSWORD = ""
MQTT_ID = "application"

sqlConnect = None
cursor = None

#### TOPICS ####
ORDER = "app/order"
DOCK = "app/emergencyDock"
BARTSTATUS = "bart/status"
SENSORLOAD = "alfred/sensorLoad"

#### FLAGS  ####
cupPresent = False
bartConnected = "disconnected"
bartOrder = ""

butlerStatus = "butlerStatus"
batteryCharge = 100
bartAligned = None



########################## MQTT SETUP ##########################
    
def on_message(client, userdata, message):
    #print(message.topic+" "+str(message.payload))
    msg = str(message.payload.decode("utf-8"))
    print("~~MQTT~~ Received message \"" + msg + "\" from topic \"" + message.topic + "\".")

    if message.topic == ORDER:
        global bartenderOrder
        bartenderOrder = msg
        print("order topic test")
        
    if message.topic == SENSORLOAD:
        global cupPresent
        if float(msg) > 1:
            cupPresent = True
        #will need to reformat based off output from Alfred
            
    if message.topic == BARTSTATUS:
        print(msg)
        global bartConnected
        bartConnected = msg
        
        
    
def on_connect(client, userdata, flags, rc): #do this when connecting to mqtt broker
    print("~~MQTT~~ Connected with result code "+ str(rc) + ".")
    client.connected_flag = True

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("~~MQTT~~ Unexpected broker disconnection.")
    else:
        print("~~MQTT~~ Successfully disconnected.")
    
def subMQTT(self, subTopic):
    global client
    client.subscribe(subTopic, qos = 2)

def pubMQTT(self, subTopic, message):
    global client
    client.publish(subTopic, str(message), qos = 2)
    print("~~MQTT~~ Sent message \"" + str(message) + "\" to topic \"" + subTopic + "\".")

def initMQTT(self):
    global client
    mqtt.Client.connected_flag=False
    client = mqtt.Client()
    
        
    client.on_message = on_message #connect custom on message function to on message event
    client.on_connect = on_connect #connect custom on connect function to on connect event
    client.on_disconnect = on_disconnect #connect custom on disconnect function to on connect event

    client.loop_start()
    print("~~MQTT~~ Attempting broker connection:  ", MQTT_SERVER)
    
    client.connect("192.168.1.78")
    
    while not client.connected_flag: #wait in loop
        time.sleep(1)
        if client.connected_flag != True:
            print("~~MQTT~~ Connecting...")

    print("~~MQTT~~ Initialized.")
    client.subscribe([(ORDER, 2),(SENSORLOAD, 1), (BARTSTATUS, 2)])

########################## SQLite3 SETUP ##########################

def initSQL(self):
    global sqlConnect
    global cursor
    sqlConnect = sqlite3.connect('B3_blackbook_v1.db')
    cursor = sqlConnect.cursor()
    print("~~SQL~~ Initialized.")

def insertSQL(self, tableName, columnName, values):
    try:
        cursor.execute("INSERT INTO " + str(tableName) + "(" + 
                       str(columnName) + ") values(" + str(values) + ")")
        print("Successfully inserted " + str(values) + 
              " into table " + str(tableName))
        sqlConnect.commit()
    except Error as e:
        print(e)

def fetchSQL(self, table, column, condtional, condition):
    try:
        cursor.execute('SELECT * FROM ' + str(table) + ' WHERE ' + 
                       str(column) + str(condtional) +
                       '\'' + str(condition) + '\'')
        value = cursor.fetchall()
        return value
    except Error as e:
        print(e)
    
def closeSQL(connect):
    try: 
        print("~~SQL~~ Closed successfully.")
        connect.close()
    except Error as e:
        print(e)

########################## MAIN UI ##########################

class Ui_B3GUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.randomCounter = 0
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
        self.label_curOrder_IngAmount.setGeometry(QtCore.QRect(560, 390, 90, 90))
        self.label_curOrder_IngAmount.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
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
        self.label_curOrder.setGeometry(QtCore.QRect(380, 310, 191, 28))
        font = QtGui.QFont()
        font.setPointSize(18)
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
        self.label_curOrder_IngName = QtWidgets.QLabel(self.page)
        self.label_curOrder_IngName.setGeometry(QtCore.QRect(380, 390, 121, 150))
        self.label_curOrder_IngName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
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
        self.pushButton_config.raise_()
        
        self.stackedWidget.addWidget(self.page)

        ##################### Menu Page #####################
        
        self.page_menuWindow = QtWidgets.QWidget()
        self.page_menuWindow.setObjectName("page_menuWindow")
        
        self.pushButton_pageToPrimary = QtWidgets.QPushButton(self.page_menuWindow)
        self.pushButton_pageToPrimary.setGeometry(QtCore.QRect(11, 441, 131, 111))
        self.pushButton_pageToPrimary.setObjectName("pushButton_pageToPrimary")
        self.pushButton_pageToCustom = QtWidgets.QPushButton(self.page_menuWindow)
        self.pushButton_pageToCustom.setGeometry(QtCore.QRect(11, 311, 131, 111))
        self.pushButton_pageToCustom.setObjectName("pushButton_pageToCustom")

        self.stackedMenuWidget = self.generateMenu()
        self.stackedMenuWidget.setGeometry(QtCore.QRect(150, 20, 721, 521))
        self.stackedMenuWidget.setObjectName("stackedMenuWidget")
        self.stackedMenuWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)

        #print(str(self.stackedMenuWidget.count()))

        if self.stackedMenuWidget.count() != 1:
            self.pushButton_menuRight = QtWidgets.QPushButton(self.page_menuWindow)
            self.pushButton_menuRight.setGeometry(QtCore.QRect(600, 550, 121, 41))
            self.pushButton_menuRight.setObjectName("pushButton_menuRight")
            self.pushButton_menuRight.setText("------->")
            self.pushButton_menuRight.clicked.connect(self.menuRight)
        
        '''
        self.stackedWidget_2 = QtWidgets.QStackedWidget(self.page_menuWindow)
        self.stackedWidget_2.setGeometry(QtCore.QRect(150, 20, 721, 521))
        self.stackedWidget_2.setObjectName("stackedWidget_2")
        self.stackedWidget_2.setFrameShape(QtWidgets.QFrame.StyledPanel)

        
        self.page_menu1 = QtWidgets.QWidget()
        self.page_menu1.setObjectName("page_menu1")
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.page_menu1)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(0, 0, 721, 521))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_menu = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_menu.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_menu.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_menu.setObjectName("gridLayout_menu")

        
        self.verticalLayout_menuRecipe_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_menuRecipe_11.setObjectName("verticalLayout_menuRecipe_11")
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_menuRecipe_11.addWidget(self.pushButton_2)
        self.line_menuRecipe_11 = QtWidgets.QFrame(self.gridLayoutWidget_4)
        self.line_menuRecipe_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_menuRecipe_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_menuRecipe_11.setObjectName("line_menuRecipe_11")
        self.verticalLayout_menuRecipe_11.addWidget(self.line_menuRecipe_11)
        self.label_recipeIng1_11 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIng1_11.sizePolicy().hasHeightForWidth())
        self.label_recipeIng1_11.setSizePolicy(sizePolicy)
        self.label_recipeIng1_11.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIng1_11.setObjectName("label_recipeIng1_11")
        self.verticalLayout_menuRecipe_11.addWidget(self.label_recipeIng1_11)
        self.label_recipeIngDynamicLater_11 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIngDynamicLater_11.sizePolicy().hasHeightForWidth())
        self.label_recipeIngDynamicLater_11.setSizePolicy(sizePolicy)
        self.label_recipeIngDynamicLater_11.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIngDynamicLater_11.setObjectName("label_recipeIngDynamicLater_11")
        self.verticalLayout_menuRecipe_11.addWidget(self.label_recipeIngDynamicLater_11)
        self.label_recipeIngDynamicLater2_11 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIngDynamicLater2_11.sizePolicy().hasHeightForWidth())
        self.label_recipeIngDynamicLater2_11.setSizePolicy(sizePolicy)
        self.label_recipeIngDynamicLater2_11.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIngDynamicLater2_11.setObjectName("label_recipeIngDynamicLater2_11")
        self.verticalLayout_menuRecipe_11.addWidget(self.label_recipeIngDynamicLater2_11)
        self.gridLayout_menu.addLayout(self.verticalLayout_menuRecipe_11, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_menu.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_menu.addItem(spacerItem1, 1, 1, 1, 1)
        self.verticalLayout_menuRecipe_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_menuRecipe_10.setObjectName("verticalLayout_menuRecipe_10")
        self.pushButton_4 = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setFlat(True)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_menuRecipe_10.addWidget(self.pushButton_4)
        self.line_menuRecipe_10 = QtWidgets.QFrame(self.gridLayoutWidget_4)
        self.line_menuRecipe_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_menuRecipe_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_menuRecipe_10.setObjectName("line_menuRecipe_10")
        self.verticalLayout_menuRecipe_10.addWidget(self.line_menuRecipe_10)
        self.label_recipeIng1_10 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIng1_10.sizePolicy().hasHeightForWidth())
        self.label_recipeIng1_10.setSizePolicy(sizePolicy)
        self.label_recipeIng1_10.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIng1_10.setObjectName("label_recipeIng1_10")
        self.verticalLayout_menuRecipe_10.addWidget(self.label_recipeIng1_10)
        self.label_recipeIngDynamicLater_10 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIngDynamicLater_10.sizePolicy().hasHeightForWidth())
        self.label_recipeIngDynamicLater_10.setSizePolicy(sizePolicy)
        self.label_recipeIngDynamicLater_10.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIngDynamicLater_10.setObjectName("label_recipeIngDynamicLater_10")
        self.verticalLayout_menuRecipe_10.addWidget(self.label_recipeIngDynamicLater_10)
        self.label_recipeIngDynamicLater2_10 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIngDynamicLater2_10.sizePolicy().hasHeightForWidth())
        self.label_recipeIngDynamicLater2_10.setSizePolicy(sizePolicy)
        self.label_recipeIngDynamicLater2_10.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIngDynamicLater2_10.setObjectName("label_recipeIngDynamicLater2_10")
        self.verticalLayout_menuRecipe_10.addWidget(self.label_recipeIngDynamicLater2_10)
        self.gridLayout_menu.addLayout(self.verticalLayout_menuRecipe_10, 0, 2, 1, 1)
        self.verticalLayout_menuRecipe_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_menuRecipe_12.setObjectName("verticalLayout_menuRecipe_12")
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_menuRecipe_12.addWidget(self.pushButton)
        self.line_menuRecipe_12 = QtWidgets.QFrame(self.gridLayoutWidget_4)
        self.line_menuRecipe_12.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_menuRecipe_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_menuRecipe_12.setObjectName("line_menuRecipe_12")
        self.verticalLayout_menuRecipe_12.addWidget(self.line_menuRecipe_12)
        self.label_recipeIng1_12 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIng1_12.sizePolicy().hasHeightForWidth())
        self.label_recipeIng1_12.setSizePolicy(sizePolicy)
        self.label_recipeIng1_12.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIng1_12.setObjectName("label_recipeIng1_12")
        self.verticalLayout_menuRecipe_12.addWidget(self.label_recipeIng1_12)
        self.label_recipeIngDynamicLater_12 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIngDynamicLater_12.sizePolicy().hasHeightForWidth())
        self.label_recipeIngDynamicLater_12.setSizePolicy(sizePolicy)
        self.label_recipeIngDynamicLater_12.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIngDynamicLater_12.setObjectName("label_recipeIngDynamicLater_12")
        self.verticalLayout_menuRecipe_12.addWidget(self.label_recipeIngDynamicLater_12)
        self.label_recipeIngDynamicLater2_12 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIngDynamicLater2_12.sizePolicy().hasHeightForWidth())
        self.label_recipeIngDynamicLater2_12.setSizePolicy(sizePolicy)
        self.label_recipeIngDynamicLater2_12.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIngDynamicLater2_12.setObjectName("label_recipeIngDynamicLater2_12")
        self.verticalLayout_menuRecipe_12.addWidget(self.label_recipeIngDynamicLater2_12)
        self.gridLayout_menu.addLayout(self.verticalLayout_menuRecipe_12, 1, 2, 1, 1)
        self.verticalLayout_menuRecipe = QtWidgets.QVBoxLayout()
        self.verticalLayout_menuRecipe.setObjectName("verticalLayout_menuRecipe")
        self.pushButton_3 = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setFlat(True)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_menuRecipe.addWidget(self.pushButton_3)
        self.line_menuRecipe = QtWidgets.QFrame(self.gridLayoutWidget_4)
        self.line_menuRecipe.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_menuRecipe.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_menuRecipe.setObjectName("line_menuRecipe")
        self.verticalLayout_menuRecipe.addWidget(self.line_menuRecipe)
        self.label_recipeIng1 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIng1.sizePolicy().hasHeightForWidth())
        self.label_recipeIng1.setSizePolicy(sizePolicy)
        self.label_recipeIng1.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIng1.setObjectName("label_recipeIng1")
        self.verticalLayout_menuRecipe.addWidget(self.label_recipeIng1)
        self.label_recipeIngDynamicLater = QtWidgets.QLabel(self.gridLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIngDynamicLater.sizePolicy().hasHeightForWidth())
        self.label_recipeIngDynamicLater.setSizePolicy(sizePolicy)
        self.label_recipeIngDynamicLater.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIngDynamicLater.setObjectName("label_recipeIngDynamicLater")
        self.verticalLayout_menuRecipe.addWidget(self.label_recipeIngDynamicLater)
        self.label_recipeIngDynamicLater2 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIngDynamicLater2.sizePolicy().hasHeightForWidth())
        self.label_recipeIngDynamicLater2.setSizePolicy(sizePolicy)
        self.label_recipeIngDynamicLater2.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIngDynamicLater2.setObjectName("label_recipeIngDynamicLater2")
        self.verticalLayout_menuRecipe.addWidget(self.label_recipeIngDynamicLater2)
        self.gridLayout_menu.addLayout(self.verticalLayout_menuRecipe, 0, 0, 1, 1)

        self.pushButton.clicked.connect(self.generateMenu)
        self.pushButton_2.clicked.connect(self.sendOrder)
        self.pushButton_3.clicked.connect(self.sendOrder)
        self.pushButton_4.clicked.connect(self.sendOrder)
        
        self.stackedWidget_2.addWidget(self.page_menu1)

        ##### temp page 2 #####
        self.page_menu2 = QtWidgets.QWidget()
        self.page_menu2.setObjectName("page_menu2")
        self.gridLayoutWidget_5 = QtWidgets.QWidget(self.page_menu2)
        self.gridLayoutWidget_5.setGeometry(QtCore.QRect(0, 0, 721, 542))
        self.gridLayoutWidget_5.setObjectName("gridLayoutWidget_5")
        self.gridLayout_menu_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_5)
        self.gridLayout_menu_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_menu_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_menu_2.setObjectName("gridLayout_menu_2")
        self.verticalLayout_menuRecipe_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_menuRecipe_13.setObjectName("verticalLayout_menuRecipe_13")
        self.label_recipeIngName_13 = QtWidgets.QLabel(self.gridLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIngName_13.sizePolicy().hasHeightForWidth())
        self.label_recipeIngName_13.setSizePolicy(sizePolicy)
        self.label_recipeIngName_13.setMinimumSize(QtCore.QSize(0, 199))
        self.label_recipeIngName_13.setObjectName("label_recipeIngName_13")
        self.verticalLayout_menuRecipe_13.addWidget(self.label_recipeIngName_13)
        self.line_menuRecipe_13 = QtWidgets.QFrame(self.gridLayoutWidget_5)
        self.line_menuRecipe_13.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_menuRecipe_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_menuRecipe_13.setObjectName("line_menuRecipe_13")
        self.verticalLayout_menuRecipe_13.addWidget(self.line_menuRecipe_13)
        self.label_recipeIng1_13 = QtWidgets.QLabel(self.gridLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIng1_13.sizePolicy().hasHeightForWidth())
        self.label_recipeIng1_13.setSizePolicy(sizePolicy)
        self.label_recipeIng1_13.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIng1_13.setObjectName("label_recipeIng1_13")
        self.verticalLayout_menuRecipe_13.addWidget(self.label_recipeIng1_13)
        self.label_recipeIngDynamicLater_13 = QtWidgets.QLabel(self.gridLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIngDynamicLater_13.sizePolicy().hasHeightForWidth())
        self.label_recipeIngDynamicLater_13.setSizePolicy(sizePolicy)
        self.label_recipeIngDynamicLater_13.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIngDynamicLater_13.setObjectName("label_recipeIngDynamicLater_13")
        self.verticalLayout_menuRecipe_13.addWidget(self.label_recipeIngDynamicLater_13)
        self.label_recipeIngDynamicLater2_13 = QtWidgets.QLabel(self.gridLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIngDynamicLater2_13.sizePolicy().hasHeightForWidth())
        self.label_recipeIngDynamicLater2_13.setSizePolicy(sizePolicy)
        self.label_recipeIngDynamicLater2_13.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIngDynamicLater2_13.setObjectName("label_recipeIngDynamicLater2_13")
        self.verticalLayout_menuRecipe_13.addWidget(self.label_recipeIngDynamicLater2_13)
        self.gridLayout_menu_2.addLayout(self.verticalLayout_menuRecipe_13, 1, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_menu_2.addItem(spacerItem2, 0, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_menu_2.addItem(spacerItem3, 1, 1, 1, 1)
        self.verticalLayout_menuRecipe_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_menuRecipe_14.setObjectName("verticalLayout_menuRecipe_14")
        self.label_recipeIngName_14 = QtWidgets.QLabel(self.gridLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIngName_14.sizePolicy().hasHeightForWidth())
        self.label_recipeIngName_14.setSizePolicy(sizePolicy)
        self.label_recipeIngName_14.setMinimumSize(QtCore.QSize(0, 199))
        self.label_recipeIngName_14.setObjectName("label_recipeIngName_14")
        self.verticalLayout_menuRecipe_14.addWidget(self.label_recipeIngName_14)
        self.line_menuRecipe_14 = QtWidgets.QFrame(self.gridLayoutWidget_5)
        self.line_menuRecipe_14.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_menuRecipe_14.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_menuRecipe_14.setObjectName("line_menuRecipe_14")
        self.verticalLayout_menuRecipe_14.addWidget(self.line_menuRecipe_14)
        self.label_recipeIng1_14 = QtWidgets.QLabel(self.gridLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIng1_14.sizePolicy().hasHeightForWidth())
        self.label_recipeIng1_14.setSizePolicy(sizePolicy)
        self.label_recipeIng1_14.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIng1_14.setObjectName("label_recipeIng1_14")
        self.verticalLayout_menuRecipe_14.addWidget(self.label_recipeIng1_14)
        self.label_recipeIngDynamicLater_14 = QtWidgets.QLabel(self.gridLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIngDynamicLater_14.sizePolicy().hasHeightForWidth())
        self.label_recipeIngDynamicLater_14.setSizePolicy(sizePolicy)
        self.label_recipeIngDynamicLater_14.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIngDynamicLater_14.setObjectName("label_recipeIngDynamicLater_14")
        self.verticalLayout_menuRecipe_14.addWidget(self.label_recipeIngDynamicLater_14)
        self.label_recipeIngDynamicLater2_14 = QtWidgets.QLabel(self.gridLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIngDynamicLater2_14.sizePolicy().hasHeightForWidth())
        self.label_recipeIngDynamicLater2_14.setSizePolicy(sizePolicy)
        self.label_recipeIngDynamicLater2_14.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIngDynamicLater2_14.setObjectName("label_recipeIngDynamicLater2_14")
        self.verticalLayout_menuRecipe_14.addWidget(self.label_recipeIngDynamicLater2_14)
        self.gridLayout_menu_2.addLayout(self.verticalLayout_menuRecipe_14, 0, 2, 1, 1)
        self.verticalLayout_menuRecipe_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_menuRecipe_15.setObjectName("verticalLayout_menuRecipe_15")
        self.label_recipeIngName_15 = QtWidgets.QLabel(self.gridLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIngName_15.sizePolicy().hasHeightForWidth())
        self.label_recipeIngName_15.setSizePolicy(sizePolicy)
        self.label_recipeIngName_15.setMinimumSize(QtCore.QSize(0, 199))
        self.label_recipeIngName_15.setObjectName("label_recipeIngName_15")
        self.verticalLayout_menuRecipe_15.addWidget(self.label_recipeIngName_15)
        self.line_menuRecipe_15 = QtWidgets.QFrame(self.gridLayoutWidget_5)
        self.line_menuRecipe_15.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_menuRecipe_15.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_menuRecipe_15.setObjectName("line_menuRecipe_15")
        self.verticalLayout_menuRecipe_15.addWidget(self.line_menuRecipe_15)
        self.label_recipeIng1_15 = QtWidgets.QLabel(self.gridLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIng1_15.sizePolicy().hasHeightForWidth())
        self.label_recipeIng1_15.setSizePolicy(sizePolicy)
        self.label_recipeIng1_15.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIng1_15.setObjectName("label_recipeIng1_15")
        self.verticalLayout_menuRecipe_15.addWidget(self.label_recipeIng1_15)
        self.label_recipeIngDynamicLater_15 = QtWidgets.QLabel(self.gridLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIngDynamicLater_15.sizePolicy().hasHeightForWidth())
        self.label_recipeIngDynamicLater_15.setSizePolicy(sizePolicy)
        self.label_recipeIngDynamicLater_15.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIngDynamicLater_15.setObjectName("label_recipeIngDynamicLater_15")
        self.verticalLayout_menuRecipe_15.addWidget(self.label_recipeIngDynamicLater_15)
        self.label_recipeIngDynamicLater2_15 = QtWidgets.QLabel(self.gridLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIngDynamicLater2_15.sizePolicy().hasHeightForWidth())
        self.label_recipeIngDynamicLater2_15.setSizePolicy(sizePolicy)
        self.label_recipeIngDynamicLater2_15.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIngDynamicLater2_15.setObjectName("label_recipeIngDynamicLater2_15")
        self.verticalLayout_menuRecipe_15.addWidget(self.label_recipeIngDynamicLater2_15)
        self.gridLayout_menu_2.addLayout(self.verticalLayout_menuRecipe_15, 1, 2, 1, 1)
        self.verticalLayout_menuRecipe_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_menuRecipe_2.setObjectName("verticalLayout_menuRecipe_2")
        self.label_recipeIngName_2 = QtWidgets.QLabel(self.gridLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIngName_2.sizePolicy().hasHeightForWidth())
        self.label_recipeIngName_2.setSizePolicy(sizePolicy)
        self.label_recipeIngName_2.setMinimumSize(QtCore.QSize(0, 199))
        self.label_recipeIngName_2.setObjectName("label_recipeIngName_2")
        self.verticalLayout_menuRecipe_2.addWidget(self.label_recipeIngName_2)
        self.line_menuRecipe_2 = QtWidgets.QFrame(self.gridLayoutWidget_5)
        self.line_menuRecipe_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_menuRecipe_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_menuRecipe_2.setObjectName("line_menuRecipe_2")
        self.verticalLayout_menuRecipe_2.addWidget(self.line_menuRecipe_2)
        self.label_recipeIng1_2 = QtWidgets.QLabel(self.gridLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIng1_2.sizePolicy().hasHeightForWidth())
        self.label_recipeIng1_2.setSizePolicy(sizePolicy)
        self.label_recipeIng1_2.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIng1_2.setObjectName("label_recipeIng1_2")
        self.verticalLayout_menuRecipe_2.addWidget(self.label_recipeIng1_2)
        self.label_recipeIngDynamicLater_2 = QtWidgets.QLabel(self.gridLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIngDynamicLater_2.sizePolicy().hasHeightForWidth())
        self.label_recipeIngDynamicLater_2.setSizePolicy(sizePolicy)
        self.label_recipeIngDynamicLater_2.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIngDynamicLater_2.setObjectName("label_recipeIngDynamicLater_2")
        self.verticalLayout_menuRecipe_2.addWidget(self.label_recipeIngDynamicLater_2)
        self.label_recipeIngDynamicLater2_2 = QtWidgets.QLabel(self.gridLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recipeIngDynamicLater2_2.sizePolicy().hasHeightForWidth())
        self.label_recipeIngDynamicLater2_2.setSizePolicy(sizePolicy)
        self.label_recipeIngDynamicLater2_2.setMinimumSize(QtCore.QSize(0, 13))
        self.label_recipeIngDynamicLater2_2.setObjectName("label_recipeIngDynamicLater2_2")
        self.verticalLayout_menuRecipe_2.addWidget(self.label_recipeIngDynamicLater2_2)
        self.gridLayout_menu_2.addLayout(self.verticalLayout_menuRecipe_2, 0, 0, 1, 1)
        self.stackedWidget_2.addWidget(self.page_menu2)
        

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

        '''
        self.pushButton_pageToCustom.clicked.connect(self.toCustom)
        self.pushButton_pageToPrimary.clicked.connect(self.toPrimary)

        
        self.stackedWidget.addWidget(self.page_menuWindow)

        ##################### Custom page #####################

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
        self.pushButton_dock.clicked.connect(self.dock)
        self.pushButton_advTools.clicked.connect(self.cupGift)
        self.pushButton_curOrder.clicked.connect(self.quickOrder)

        self.pushButton_pageToPrimary2 = QtWidgets.QPushButton(self.page_3)
        self.pushButton_pageToPrimary2.setGeometry(QtCore.QRect(11, 441, 131, 111))
        self.pushButton_pageToPrimary2.setObjectName("pushButton_pageToPrimary2")

        self.pushButton_pageToPrimary2.clicked.connect(self.toPrimary)

        self.stackedWidget.addWidget(self.page_3)

        self.retranslateUi()
        self.stackedWidget.setCurrentIndex(0)
        #QtCore.QMetaObject.connectSlotsByName(self)

    def generateMenu(self):
        menuRaw = fetchSQL(cursor, 'menu', 'id_start', '>', 0)
        #print(menuRaw)
        _translate = QtCore.QCoreApplication.translate

        stackedWidget = QtWidgets.QStackedWidget(self.page_menuWindow)

        menuPage = None
        menuCount = 0
        for i in menuRaw:
            menuName = str(i[0])
            availableFlag = 1
            for j in range(0,i[2]):
                ing = fetchSQL(cursor, 'recipes', 'id', '=', (int(i[1]) + j))
                test = fetchSQL(cursor, 'config', 'ingredient_name', '=', ing[0][3])
                if test == []:
                    availableFlag = 0
                    #print('   ERROR: Recipe \'' + menuName + '\' has none of Ingredient \'' + str(ing[0][3]) + '\' in configuration.')
                    break
                if test[0][3] < ing[0][4]:
                    availableFlag = 0
                    print('   ERROR: There is an insuffecient amount of Ingredient \'' + str(ing[0][3]) + '\' configured.')
                    break
                    
            if availableFlag == 1:
                if menuCount%4 == 0:
                    if menuPage!= None:
                        stackedWidget.addWidget(menuPage)
                    menuPage = None
                    menuPage = QtWidgets.QWidget()
                    menuPage.setObjectName("menuPage " + str(int(menuCount/4) + 1))
                    #print('created menu page ' + str(int(menuCount/4) + 1))
                    gridLayoutWidget = None
                    gridLayoutWidget = QtWidgets.QWidget(menuPage)
                    gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 721, 521))
                    gridLayoutWidget.setObjectName("gridLayoutWidget " + str(int(menuCount/4) + 1))
                    gridLayout_menu = None
                    gridLayout_menu = QtWidgets.QGridLayout(gridLayoutWidget)
                    gridLayout_menu.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
                    gridLayout_menu.setContentsMargins(0, 0, 0, 0)
                    gridLayout_menu.setObjectName("gridLayout_menu " + str(int(menuCount/4) + 1))
                    #spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
                    #gridLayout_menu.addItem(spacerItem, 2, 1, 1, 1)

                menuItem = None
                menuItem = QtWidgets.QVBoxLayout()
                menuItem.setObjectName(menuName + " Item")
                pushButton= QtWidgets.QPushButton()
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(pushButton.sizePolicy().hasHeightForWidth())
                pushButton.setSizePolicy(sizePolicy)
                pushButton.setMinimumSize(QtCore.QSize(0, 150))
                pushButton.setFlat(True)
                pushButton.setObjectName(menuName + " pushButton")
                #print(menuName)
                pushButton.setText(_translate("B3GUI", menuName))
                pushButton.clicked.connect(self.sendOrder)
                menuItem.addWidget(pushButton)              
                line_menuRecipe = QtWidgets.QFrame()
                line_menuRecipe.setFrameShape(QtWidgets.QFrame.HLine)
                line_menuRecipe.setFrameShadow(QtWidgets.QFrame.Sunken)
                line_menuRecipe.setObjectName(menuName + " line_menuRecipe")
                menuItem.addWidget(line_menuRecipe)

                '''
                ingItemWidget = QtWidgets.QWidget()
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(ingItemWidget.sizePolicy().hasHeightForWidth())
                ingItemWidget.setSizePolicy(sizePolicy)
                ingItemWidget.setMinimumSize(QtCore.QSize(0, 70))
                ingItemWidget.setObjectName(menuName + " Ingredient List Widget")
                
                ingItem = QtWidgets.QVBoxLayout(ingItemWidget)
                ingItem.setObjectName(menuName + " Ingredient List")

                for j in range(0,i[2]):
                    ing = fetchSQL(cursor, 'recipes', 'id', '=', (int(i[1]) + j))
                    ingName = str(ing[0][3])
                    
                    label_recipeIng = QtWidgets.QLabel()
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(label_recipeIng.sizePolicy().hasHeightForWidth())
                    label_recipeIng.setSizePolicy(sizePolicy)
                    label_recipeIng.setMinimumSize(QtCore.QSize(0, 13))
                    label_recipeIng.setObjectName("label_recipeIng" + str(int(j) + 1))
                    label_recipeIng.setText(_translate("B3GUI", ingName))
                    ingItem.addWidget(label_recipeIng)

                #ingItemWidget.addLayout(ingItem)
                menuItem.addWidget(ingItemWidget)'''

                label_recipeIng = QtWidgets.QLabel()
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(label_recipeIng.sizePolicy().hasHeightForWidth())
                label_recipeIng.setSizePolicy(sizePolicy)
                label_recipeIng.setMinimumSize(QtCore.QSize(0, 70))
                label_recipeIng.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
                label_recipeIng.setObjectName(menuName + "label_recipeIng")
                label_recipeIng.setIndent(2)

                ingString = ""
                
                for j in range(0,i[2]):
                    ing = fetchSQL(cursor, 'recipes', 'id', '=', (int(i[1]) + j))
                    ingName = str(ing[0][3])

                    temp = (ingString + "<p>" + ingName + "</p>")
                    ingString = temp

                temp = ("<html><head/><body>" + ingString + "</body></html>")
                label_recipeIng.setText(_translate("B3GUI", ingString))
                
                menuItem.addWidget(label_recipeIng)
                gridLayout_menu.addLayout(menuItem, int((menuCount%4)/2), int(2*((menuCount%4)%2)), 1, 1)
                
                if (menuCount%2 == 1):
                    spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                    gridLayout_menu.addItem(spacerItem, (int(((menuCount%4)-1)/2)), 1, 1, 1)
    
                menuCount += 1
        if (menuCount%4 == 1 or menuCount%4 == 2):
            spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            gridLayout_menu.addItem(spacerItem, 1, 1, 1, 1)
        if (menuCount%4 == 1):
            spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            gridLayout_menu.addItem(spacerItem, 0, 2, 1, 1)
        if menuPage != None:
            stackedWidget.addWidget(menuPage)
        else:
            print("   ERROR: you idiot you have nothing configured")
        stackedWidget.setCurrentIndex(0)
        stackedWidget.menuCount = menuCount
        return stackedWidget
    ##stackedWidget.count() returns for loop viable thing for making dynamic menu page change buttons
    

    def menuRight(self):
        if(self.stackedMenuWidget.currentIndex() == 0):
            self.pushButton_menuLeft = QtWidgets.QPushButton(self.page_menuWindow)
            self.pushButton_menuLeft.setGeometry(QtCore.QRect(300, 550, 121, 41))
            self.pushButton_menuLeft.setObjectName("pushButton_menuLeft")
            self.pushButton_menuLeft.setText("<-------")
            self.pushButton_menuLeft.clicked.connect(self.menuLeft)
            self.pushButton_menuLeft.show()
        self.stackedMenuWidget.setCurrentIndex((self.stackedMenuWidget.currentIndex() + 1))
        if((self.stackedMenuWidget.currentIndex() + 1) == self.stackedMenuWidget.count()):
            self.pushButton_menuRight.close()


    def menuLeft(self):
        if((self.stackedMenuWidget.currentIndex() + 1) == self.stackedMenuWidget.count()):
            self.pushButton_menuRight = QtWidgets.QPushButton(self.page_menuWindow)
            self.pushButton_menuRight.setGeometry(QtCore.QRect(600, 550, 121, 41))
            self.pushButton_menuRight.setObjectName("pushButton_menuRight")
            self.pushButton_menuRight.setText("------->")
            self.pushButton_menuRight.clicked.connect(self.menuRight)
            self.pushButton_menuRight.show()
        self.stackedMenuWidget.setCurrentIndex((self.stackedMenuWidget.currentIndex() - 1))

        if(self.stackedMenuWidget.currentIndex() == 0):
            self.pushButton_menuLeft.close()
            
    def sendOrder(self):
        if cupPresent:
            _translate = QtCore.QCoreApplication.translate
            sender = self.sender()
            orderName = sender.text()
            self.label_curOrder_Name.setText(_translate("B3GUI", str(orderName)))
            #print(orderName)
            orderRaw = fetchSQL(cursor, 'recipes', 'recipe_name', '=', str(orderName))
            print(orderRaw)
            order = None
            ingName = ""
            ingAmt = ""
                    
            '''for j in range(0,i[2]):
                        ing = fetchSQL(cursor, 'recipes', 'id', '=', (int(i[1]) + j))
                        ingName = str(ing[0][3])

                        temp = (ingString + "<p>" + ingName + "</p>")
                        ingString = temp'''

                    
            for i in orderRaw:
                temp = (ingName + "<p>" + str(i[3]) + "</p>")
                ingName = temp
                temp = (ingAmt + "<p>" + str(i[4]) + " mL" + "</p>")
                ingAmt = temp

                pumpConfig = fetchSQL(cursor, 'config', 'ingredient_name', '=', str(i[3]))
                if order == None:
                    temp = (pumpConfig[0][0], i[4])
                    order = temp
                else:
                    temp = order, (pumpConfig[0][0], i[4])
                    order = temp
            self.label_curOrder_IngName.setText(_translate("B3GUI", ingName))
            self.label_curOrder_IngAmount.setText(_translate("B3GUI", ingAmt))
            global bartOrder
            bartOrder = order
            print(order)
            pubMQTT(client, ORDER, order)
            self.toPrimary()
        else:
            print("Please place cup in thingy.")

    def quickOrder(self):
        if bartOrder != "":
            pubMQTT(client, ORDER, bartOrder)
            self.toPrimary()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("B3GUI", "Form"))
        self.pushButton_config.setText(_translate("B3GUI", "Drink\n"
"Configuration"))
        self.pushButton_toMenu.setText(_translate("B3GUI", "Menu"))
        self.label_config_dynamicLater3.setText(_translate("B3GUI", "Ing. D"))
        self.label_config_dynamicLater1.setText(_translate("B3GUI", "Ing. B"))
        self.label_config_dynamicLater4.setText(_translate("B3GUI", "Bartender is \n" + bartConnected))
        self.label_curOrder_IngAmount.setText(_translate("B3GUI", " "))
        self.pushButton_curOrder.setText(_translate("B3GUI", "Quick Order"))
        self.pushButton_quit.setText(_translate("B3GUI", "Quit"))
        self.label_config.setText(_translate("B3GUI", "Ing. A"))
        self.label_curOrder.setText(_translate("B3GUI", "Current Order: "))
        self.pushButton_dock.setText(_translate("B3GUI", "Dock"))
        self.label_config_dynamicLater2.setText(_translate("B3GUI", "Ing. C"))
        self.pushButton_advTools.setText(_translate("B3GUI", "Adv. \n"
"Tools"))
        self.label_batteryCharge.setText(_translate("B3GUI", "Battery Charge"))
        self.pushButton_pageToPrimary.setText(_translate("B3GUI", "Main Window"))
        self.pushButton_pageToCustom.setText(_translate("B3GUI", "Custom Order"))

        
        '''self.pushButton_2.setText(_translate("B3GUI", "Test Drink B"))
        self.label_recipeIng1_11.setText(_translate("B3GUI", "Test Liquor A"))
        self.label_recipeIngDynamicLater_11.setText(_translate("B3GUI", "Test Liquor B"))
        #self.label_recipeIngDynamicLater2_11.setText(_translate("B3GUI", "Ingredient 3"))
        self.pushButton_4.setText(_translate("B3GUI", "Test Drink C"))
        self.label_recipeIng1_10.setText(_translate("B3GUI", "Test Liquor A"))
        self.label_recipeIngDynamicLater_10.setText(_translate("B3GUI", "Test Ingredient A"))
        #self.label_recipeIngDynamicLater2_10.setText(_translate("B3GUI", "Ingredient 3"))
        self.pushButton.setText(_translate("B3GUI", "Test Drink D"))
        self.label_recipeIng1_12.setText(_translate("B3GUI", "Test Liquor B"))
        self.label_recipeIngDynamicLater_12.setText(_translate("B3GUI", "Ingredient B"))
        #self.label_recipeIngDynamicLater2_12.setText(_translate("B3GUI", "Ingredient 3"))
        self.pushButton_3.setText(_translate("B3GUI", "Test Drink A"))
        self.label_recipeIng1.setText(_translate("B3GUI", "Test Liquor A"))
        #self.label_recipeIngDynamicLater.setText(_translate("B3GUI", "Ingredient 2"))
        #self.label_recipeIngDynamicLater2.setText(_translate("B3GUI", "Ingredient 3"))'''
        '''
        self.label_recipeIngName_13.setText(_translate("B3GUI", "NameofDrink"))
        self.label_recipeIng1_13.setText(_translate("B3GUI", "Ingredient 1"))
        self.label_recipeIngDynamicLater_13.setText(_translate("B3GUI", "Ingredient 2"))
        self.label_recipeIngDynamicLater2_13.setText(_translate("B3GUI", "Ingredient 3"))
        self.label_recipeIngName_14.setText(_translate("B3GUI", "NameofDrink"))
        self.label_recipeIng1_14.setText(_translate("B3GUI", "Ingredient 1"))
        self.label_recipeIngDynamicLater_14.setText(_translate("B3GUI", "Ingredient 2"))
        self.label_recipeIngDynamicLater2_14.setText(_translate("B3GUI", "Ingredient 3"))
        self.label_recipeIngName_15.setText(_translate("B3GUI", "NameofDrink"))
        self.label_recipeIng1_15.setText(_translate("B3GUI", "Ingredient 1"))
        self.label_recipeIngDynamicLater_15.setText(_translate("B3GUI", "Ingredient 2"))
        self.label_recipeIngDynamicLater2_15.setText(_translate("B3GUI", "Ingredient 3"))
        self.label_recipeIngName_2.setText(_translate("B3GUI", "NameofDrink"))
        self.label_recipeIng1_2.setText(_translate("B3GUI", "Ingredient 1"))
        self.label_recipeIngDynamicLater_2.setText(_translate("B3GUI", "Ingredient 2"))
        self.label_recipeIngDynamicLater2_2.setText(_translate("B3GUI", "Ingredient 3"))
        
        self.pushButton_menuLeft.setText(_translate("B3GUI", "<-------"))
        self.pushButton_menuRight.setText(_translate("B3GUI", "------->"))'''
        self.label_51.setText(_translate("B3GUI", "Ingredient 2"))
        self.label_52.setText(_translate("B3GUI", "Ingredient 1"))
        self.label_53.setText(_translate("B3GUI", "Ingredient 3"))
        self.label_54.setText(_translate("B3GUI", "Temp Custom Drank Layout"))
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
        self.retranslateUi()
        self.stackedWidget.setCurrentIndex(0)

        
    def cupGift(self): ##purely for test purposes in toggling cup present flag
        global cupPresent
        temp = not cupPresent
        cupPresent = temp

    def dock(self):
        pubMQTT(client, DOCK, "hey this is the emergency dock signal")
        
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
        print("")
        self.exit.destroy()
        closeSQL(sqlConnect)
        client.disconnect()
        QtCore.QCoreApplication.instance().quit
        sys.exit()

    def retranslateExit(self):
        _translate = QtCore.QCoreApplication.translate
        self.exit.setWindowTitle(_translate("ExitWindow", "Dialog"))
        self.exitLabel.setText(_translate("ExitWindow", "Are you sure you want to quit?"))

def main():
    initMQTT(client)
    initSQL(sqlConnect)
    print("")
    
    application = QtWidgets.QApplication(sys.argv)
    application.setStyle('Fusion')
    window = Ui_B3GUI()
    
    sys.exit(application.exec_())
    
    

if __name__ == '__main__':
    #try:
    main()
