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
MQTT_SERVERY = "172.16.210.200"
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
STARTSIGNAL = "app/start"

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
        #print("order topic test")
        
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
    
    ip = MQTT_SERVER
    print("~~MQTT~~ Attempting broker connection:  ", ip)
    client.connect(ip, MQTT_PORT)
    
    while not client.connected_flag: #wait in loop
        time.sleep(1)
        if client.connected_flag != True:
            print("~~MQTT~~ Connecting...")

    print("~~MQTT~~ Initialized.")
    client.subscribe([(SENSORLOAD, 1), (BARTSTATUS, 2), (STARTSIGNAL, 2)])

########################## SQLite3 SETUP ##########################

def initSQL(self):
    global sqlConnect
    global cursor
    sqlConnect = sqlite3.connect('B3_blackbook_v1.db')
    cursor = sqlConnect.cursor()
    print("~~SQL~~ Initialized.")

def insertSQL(self, tableName, columnNames, values):
    try:
        cursor.execute("INSERT INTO " + str(tableName) + "(" + 
                       str(columnNames) + ") values(" + str(values) + ")")
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
        self.setGeometry(0, 0, 640, 480)
        #self.setWindowIcon(QtGui.Icon('B3symbol.png'))
        _translate = QtCore.QCoreApplication.translate
        self.exit = QtWidgets.QDialog()
        self.configAddConfirm = QtWidgets.QDialog()
        #self.customAddConfirm = QtWidgets.QDialog()
        
        self.paletteButton = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 136, 136))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.paletteButton.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 136, 136))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.paletteButton.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 136, 136))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.paletteButton.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)


        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.setPalette(palette)
        
        self.stackedWidget = QtWidgets.QStackedWidget(self)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 640, 480))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.stackedWidget.setPalette(palette)
        self.stackedWidget.setObjectName("stackedWidget")

        self.setupPrimary()
        #self.showFullScreen()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
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
        self.pushButton_config.setGeometry(QtCore.QRect(513, 24, 101, 49))
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
        self.pushButton_toMenu.setGeometry(QtCore.QRect(25, 25, 429, 161))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 136, 136))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 136, 136))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 136, 136))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.pushButton_toMenu.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        font.setPointSize(60)
        self.pushButton_toMenu.setFont(font)
        self.pushButton_toMenu.setObjectName("pushButton_toMenu")
        self.progressBar_config_dynamicLater2 = QtWidgets.QProgressBar(self.page)
        self.progressBar_config_dynamicLater2.setGeometry(QtCore.QRect(556, 176, 74, 25))
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
        self.progressBar_config_dynamicLater4.setGeometry(QtCore.QRect(556, 240, 74, 25))
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
        self.label_config_dynamicLater3.setGeometry(QtCore.QRect(488, 208, 56, 25))
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.label_config_dynamicLater3.setFont(font)
        self.label_config_dynamicLater3.setObjectName("label_config_dynamicLater3")
        self.progressBar_config_dynamicLater1 = QtWidgets.QProgressBar(self.page)
        self.progressBar_config_dynamicLater1.setGeometry(QtCore.QRect(556, 144, 74, 25))
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
        self.label_imageB3.setGeometry(QtCore.QRect(575, 432, 56, 22))
        self.label_imageB3.setText("")
        self.label_imageB3.setObjectName("label_imageB3")
        self.line = QtWidgets.QFrame(self.page)
        self.line.setGeometry(QtCore.QRect(259, 275, 189, 13))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_config_dynamicLater1 = QtWidgets.QLabel(self.page)
        self.label_config_dynamicLater1.setGeometry(QtCore.QRect(488, 144, 56, 25))
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.label_config_dynamicLater1.setFont(font)
        self.label_config_dynamicLater1.setObjectName("label_config_dynamicLater1")
        self.widget_rightInfo = QtWidgets.QListWidget(self.page)
        self.widget_rightInfo.setGeometry(QtCore.QRect(480, -1, 161, 482))
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
        self.widget_curOrder.setGeometry(QtCore.QRect(252, 211, 202, 201))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 87, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.widget_curOrder.setPalette(palette)
        self.widget_curOrder.setObjectName("widget_curOrder")
        self.label_config_dynamicLater4 = QtWidgets.QLabel(self.page)
        self.label_config_dynamicLater4.setGeometry(QtCore.QRect(488, 240, 56, 25))
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.label_config_dynamicLater4.setFont(font)
        self.label_config_dynamicLater4.setObjectName("label_config_dynamicLater4")
        self.label_curOrder_IngAmount = QtWidgets.QLabel(self.page)
        self.label_curOrder_IngAmount.setGeometry(QtCore.QRect(371, 291, 76, 72))
        self.label_curOrder_IngAmount.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_curOrder_IngAmount.setObjectName("label_curOrder_IngAmount")
        self.pushButton_curOrder = QtWidgets.QPushButton(self.page)
        self.pushButton_curOrder.setGeometry(QtCore.QRect(25, 211, 202, 96))
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
        self.pushButton_quit.setGeometry(QtCore.QRect(167, 332, 60, 80))
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
        self.label_config = QtWidgets.QLabel(self.page)
        self.label_config.setGeometry(QtCore.QRect(488, 112, 56, 25))
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.label_config.setFont(font)
        self.label_config.setObjectName("label_config")
        self.label_curOrder = QtWidgets.QLabel(self.page)
        self.label_curOrder.setGeometry(QtCore.QRect(259, 227, 170, 22))
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.label_curOrder.setFont(font)
        self.label_curOrder.setObjectName("label_curOrder")
        self.pushButton_dock = QtWidgets.QPushButton(self.page)
        self.pushButton_dock.setGeometry(QtCore.QRect(96, 332, 60, 80))
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
        self.progressBar_batteryCharge.setGeometry(QtCore.QRect(500, 432, 63, 25))
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
        self.progressBar_config_dynamicLater3.setGeometry(QtCore.QRect(556, 208, 74, 25))
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
        self.label_curOrder_Name.setGeometry(QtCore.QRect(261, 250, 170, 28))
        font = QtGui.QFont()
        font.setFamily("MathJax_Main")
        self.label_curOrder_Name.setFont(font)
        self.label_curOrder_Name.setObjectName("label_curOrder_Name")
        self.progressBar_config = QtWidgets.QProgressBar(self.page)
        self.progressBar_config.setGeometry(QtCore.QRect(556, 112, 74, 25))
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
        self.label_curOrder_IngName.setGeometry(QtCore.QRect(261, 291, 96, 120))
        self.label_curOrder_IngName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_curOrder_IngName.setObjectName("label_curOrder_IngName")
        self.label_config_dynamicLater2 = QtWidgets.QLabel(self.page)
        self.label_config_dynamicLater2.setGeometry(QtCore.QRect(488, 176, 56, 25))
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.label_config_dynamicLater2.setFont(font)
        self.label_config_dynamicLater2.setObjectName("label_config_dynamicLater2")
        self.pushButton_advTools = QtWidgets.QPushButton(self.page)
        self.pushButton_advTools.setGeometry(QtCore.QRect(25, 332, 60, 80))
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
        self.label_batteryCharge.setGeometry(QtCore.QRect(488, 408, 88, 22))
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

        self.pushButton_dock.clicked.connect(self.dock)
        self.pushButton_advTools.clicked.connect(self.cupGift)
        self.pushButton_quit.clicked.connect(self.exitPopup)
        self.pushButton_curOrder.clicked.connect(self.quickOrder)
        
        self.pushButton_config.clicked.connect(self.toConfig)
        self.pushButton_toMenu.clicked.connect(self.toMenu)
        
        self.stackedWidget.addWidget(self.page)

        ##################### Menu Page #####################
        
        self.page_menuWindow = QtWidgets.QWidget()   
        self.page_menuWindow.setObjectName("page_menuWindow")

        self.stackedMenuWidget = self.generateMenu()
        self.stackedMenuWidget.setGeometry(QtCore.QRect(94, 16, 451, 417))
        self.stackedMenuWidget.setObjectName("stackedMenuWidget")
        self.stackedMenuWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)

        if self.stackedMenuWidget.count() != 1:
            self.pushButton_menuRight = QtWidgets.QPushButton(self.page_menuWindow)
            self.pushButton_menuRight.setGeometry(QtCore.QRect(375, 440, 76, 33))
            self.pushButton_menuRight.setPalette(self.paletteButton)
            self.pushButton_menuRight.setObjectName("pushButton_menuRight")
            self.pushButton_menuRight.setText("------->")
            self.pushButton_menuRight.clicked.connect(self.menuRight)
            

        self.widget_menu_rightInfo = QtWidgets.QListWidget(self.page_menuWindow)
        self.widget_menu_rightInfo.setGeometry(QtCore.QRect(560, -1, 81, 482))
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
        self.widget_menu_rightInfo.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.widget_menu_rightInfo.setFont(font)
        self.widget_menu_rightInfo.setObjectName("widget_menu_rightInfo")
        self.widget_menu_leftInfo = QtWidgets.QListWidget(self.page_menuWindow)
        self.widget_menu_leftInfo.setGeometry(QtCore.QRect(-1, -1, 81, 482))
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
        self.widget_menu_leftInfo.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.widget_menu_leftInfo.setFont(font)
        self.widget_menu_leftInfo.setObjectName("widget_menu_leftInfo")

        pushButton_pageToPrimary = QtWidgets.QPushButton(self.page_menuWindow)
        pushButton_pageToPrimary.setGeometry(QtCore.QRect(8, 350, 64, 61))
        pushButton_pageToPrimary.setPalette(self.paletteButton)
        pushButton_pageToPrimary.setObjectName("pushButton_pageToPrimary")
        pushButton_pageToPrimary.setText(_translate("B3GUI", "Main\nWindow"))
        
        pushButton_pageToCustom = QtWidgets.QPushButton(self.page_menuWindow)
        pushButton_pageToCustom.setGeometry(QtCore.QRect(8, 275, 64, 61))
        pushButton_pageToCustom.setPalette(self.paletteButton)
        pushButton_pageToCustom.setObjectName("pushButton_pageToCustom")
        pushButton_pageToCustom.setText(_translate("B3GUI", "Custom\nOrder"))
        
        pushButton_pageToCustom.clicked.connect(self.toCustom)
        pushButton_pageToPrimary.clicked.connect(self.toPrimary)
        
        self.stackedWidget.addWidget(self.page_menuWindow)

        ##################### Custom page #####################

        self.page_custom = QtWidgets.QWidget()
        self.page_custom.setObjectName("page_custom")

        self.frame_2 = QtWidgets.QFrame(self.page_custom)
        self.frame_2.setGeometry(QtCore.QRect(95, 15, 451, 455))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.gridLayoutWidget = QtWidgets.QWidget(self.frame_2)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(2, 2, 446, 449))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_custom = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_custom.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_custom.setObjectName("gridLayout_custom")

        self.label_custom_ingNameHead = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_custom_ingNameHead.sizePolicy().hasHeightForWidth())
        self.label_custom_ingNameHead.setSizePolicy(sizePolicy)
        self.label_custom_ingNameHead.setMinimumSize(QtCore.QSize(0, 70))
        self.label_custom_ingNameHead.setAlignment(QtCore.Qt.AlignCenter)
        self.label_custom_ingNameHead.setObjectName("label_custom_ingNameHead")
        self.gridLayout_custom.addWidget(self.label_custom_ingNameHead, 0, 0, 1, 1)
        self.label_custom_ingAmountHead = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_custom_ingAmountHead.sizePolicy().hasHeightForWidth())
        self.label_custom_ingAmountHead.setSizePolicy(sizePolicy)
        self.label_custom_ingAmountHead.setMinimumSize(QtCore.QSize(0, 70))
        self.label_custom_ingAmountHead.setAlignment(QtCore.Qt.AlignCenter)
        self.label_custom_ingAmountHead.setObjectName("label_custom_ingAmountHead")
        self.gridLayout_custom.addWidget(self.label_custom_ingAmountHead, 0, 2, 1, 1)
        self.label_custom_ingUnitHead = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_custom_ingUnitHead.sizePolicy().hasHeightForWidth())
        self.label_custom_ingUnitHead.setSizePolicy(sizePolicy)
        self.label_custom_ingUnitHead.setMinimumSize(QtCore.QSize(25, 70))
        self.label_custom_ingUnitHead.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_custom_ingUnitHead.setObjectName("label_custom_ingUnitHead")
        self.gridLayout_custom.addWidget(self.label_custom_ingUnitHead, 0, 3, 1, 1)
        self.label_custom_ingNameHead.setText(_translate("B3GUI", "Ingredient"))
        self.label_custom_ingAmountHead.setText(_translate("B3GUI", "Amount"))
        self.label_custom_ingUnitHead.setText(_translate("B3GUI", "Unit"))


        self.lineEdit_custom_ingName = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_custom_ingName.setAutoFillBackground(False)
        self.lineEdit_custom_ingName.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:0, stop:0 rgba(136, 138, 133, 255), stop:1 rgba(255, 255, 255, 255));")
        self.lineEdit_custom_ingName.setObjectName("lineEdit_custom_ingName")
        self.gridLayout_custom.addWidget(self.lineEdit_custom_ingName, 1, 0, 1, 1)
        
        self.line_customing = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line_customing.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_customing.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_customing.setObjectName("line_customing")
        self.gridLayout_custom.addWidget(self.line_customing, 1, 1, 1, 1)

        self.lineEdit_custom_ingAmount = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_custom_ingAmount.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lineEdit_custom_ingAmount.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:0, stop:0 rgba(136, 138, 133, 255), stop:1 rgba(255, 255, 255, 255));")
        self.lineEdit_custom_ingAmount.setObjectName("lineEdit_custom_ingAmount")
        self.gridLayout_custom.addWidget(self.lineEdit_custom_ingAmount, 1, 2, 1, 1)
        
        self.lineEdit_custom_ingName_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_custom_ingName_2.setAutoFillBackground(False)
        self.lineEdit_custom_ingName_2.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:0, stop:0 rgba(136, 138, 133, 255), stop:1 rgba(255, 255, 255, 255));")
        self.lineEdit_custom_ingName_2.setObjectName("lineEdit_custom_ingName_2")
        self.gridLayout_custom.addWidget(self.lineEdit_custom_ingName_2, 2, 0, 1, 1)

        self.line_customing_2 = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line_customing_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_customing_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_customing_2.setObjectName("line_customing_2")
        self.gridLayout_custom.addWidget(self.line_customing_2, 2, 1, 1, 1)

        self.lineEdit_custom_ingAmount_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_custom_ingAmount_2.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lineEdit_custom_ingAmount_2.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:0, stop:0 rgba(136, 138, 133, 255), stop:1 rgba(255, 255, 255, 255));")
        self.lineEdit_custom_ingAmount_2.setObjectName("lineEdit_custom_ingAmount_2")
        self.gridLayout_custom.addWidget(self.lineEdit_custom_ingAmount_2, 2, 2, 1, 1)

        self.lineEdit_custom_ingName_3 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_custom_ingName_3.setAutoFillBackground(False)
        self.lineEdit_custom_ingName_3.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:0, stop:0 rgba(136, 138, 133, 255), stop:1 rgba(255, 255, 255, 255));")
        self.lineEdit_custom_ingName_3.setObjectName("lineEdit_custom_ingName_3")
        self.gridLayout_custom.addWidget(self.lineEdit_custom_ingName_3, 3, 0, 1, 1)
        
        self.line_customing_3 = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line_customing_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_customing_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_customing_3.setObjectName("line_customing_3")
        self.gridLayout_custom.addWidget(self.line_customing_3, 3, 1, 1, 1)

        self.lineEdit_custom_ingAmount_3 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_custom_ingAmount_3.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lineEdit_custom_ingAmount_3.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:0, stop:0 rgba(136, 138, 133, 255), stop:1 rgba(255, 255, 255, 255));")
        self.lineEdit_custom_ingAmount_3.setObjectName("lineEdit_custom_ingAmount_3")
        self.gridLayout_custom.addWidget(self.lineEdit_custom_ingAmount_3, 3, 2, 1, 1)

        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_custom.addItem(spacerItem5, 4, 0, 1, 1)
        self.label_custom_unit = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_custom_unit.setObjectName("label_custom_unit")
        self.gridLayout_custom.addWidget(self.label_custom_unit, 1, 3, 1, 1)
        self.label_custom_unit_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_custom_unit_2.setObjectName("label_custom_unit_2")
        self.gridLayout_custom.addWidget(self.label_custom_unit_2, 2, 3, 1, 1)
        self.label_custom_unit_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_custom_unit_3.setObjectName("label_custom_unit_3")
        self.gridLayout_custom.addWidget(self.label_custom_unit_3, 3, 3, 1, 1)
        self.label_custom_unit.setText(_translate("B3GUI", "mL"))
        self.label_custom_unit_2.setText(_translate("B3GUI", "mL"))
        self.label_custom_unit_3.setText(_translate("B3GUI", "mL"))

        self.buttonBox_custom = QtWidgets.QDialogButtonBox(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox_custom.sizePolicy().hasHeightForWidth())
        self.buttonBox_custom.setSizePolicy(sizePolicy)
        self.buttonBox_custom.setPalette(self.paletteButton)
        self.buttonBox_custom.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.buttonBox_custom.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox_custom.setStandardButtons(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Reset)
        self.buttonBox_custom.setCenterButtons(False)
        self.buttonBox_custom.setObjectName("buttonBox_custom")

        self.buttonBox_custom.accepted.connect(self.customAdd)
        self.buttonBox_custom.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self.customReset)
        self.gridLayout_custom.addWidget(self.buttonBox_custom, 5, 2, 1, 1)


        
        self.widget_custom_rightInfo = QtWidgets.QListWidget(self.page_custom)
        self.widget_custom_rightInfo.setGeometry(QtCore.QRect(560, -1, 81, 482))
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
        self.widget_custom_rightInfo.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.widget_custom_rightInfo.setFont(font)
        self.widget_custom_rightInfo.setObjectName("widget_custom_rightInfo")
        self.widget_custom_leftInfo = QtWidgets.QListWidget(self.page_custom)
        self.widget_custom_leftInfo.setGeometry(QtCore.QRect(-1, -1, 81, 482))
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
        self.widget_custom_leftInfo.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.widget_custom_leftInfo.setFont(font)
        self.widget_custom_leftInfo.setObjectName("widget_custom_leftInfo")

        self.pushButton_custom_pageToMenu = QtWidgets.QPushButton(self.page_custom)
        self.pushButton_custom_pageToMenu.setGeometry(QtCore.QRect(8, 275, 64, 61))
        self.pushButton_custom_pageToMenu.setPalette(self.paletteButton)
        self.pushButton_custom_pageToMenu.setObjectName("pushButton_custom_pageToMenu")
        self.pushButton_custom_pageToMenu.setText(_translate("B3GUI", "Menu"))
        self.pushButton_custom_pageToPrimary = QtWidgets.QPushButton(self.page_custom)
        self.pushButton_custom_pageToPrimary.setGeometry(QtCore.QRect(8, 350, 64, 61))
        self.pushButton_custom_pageToPrimary.setPalette(self.paletteButton)
        self.pushButton_custom_pageToPrimary.setObjectName("pushButton_custom_pageToPrimary")
        self.pushButton_custom_pageToPrimary.setText(_translate("B3GUI", "Main\nWindow"))
        
        self.widget_custom_leftInfo.raise_()
        self.frame_2.raise_()
        self.pushButton_custom_pageToMenu.raise_()
        self.pushButton_custom_pageToPrimary.raise_()
        self.widget_custom_rightInfo.raise_()

        self.pushButton_custom_pageToMenu.clicked.connect(self.toMenu)
        self.pushButton_custom_pageToPrimary.clicked.connect(self.toPrimary)

        self.stackedWidget.addWidget(self.page_custom)

        ##################### Config page #####################
        
        self.page_config = QtWidgets.QWidget()
        self.page_config.setObjectName("page_config")
        self.pushButton_config_toMain = QtWidgets.QPushButton(self.page_config)
        self.pushButton_config_toMain.setGeometry(QtCore.QRect(576, 24, 50, 55))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 136, 136))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 136, 136))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 136, 136))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.pushButton_config_toMain.setPalette(palette)
        self.pushButton_config_toMain.setObjectName("pushButton_config_toMain")
        self.frame_config = QtWidgets.QFrame(self.page_config)
        self.frame_config.setGeometry(QtCore.QRect(40, 15, 506, 453))
        self.frame_config.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_config.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_config.setObjectName("frame_config")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.frame_config)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(2, 2, 501, 449))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_config = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_config.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_config.setObjectName("gridLayout_config")
        self.lineEdit_config_pumpid = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_config_pumpid.setMaximumSize(QtCore.QSize(35, 16777215))
        self.lineEdit_config_pumpid.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:0, stop:0 rgba(136, 138, 133, 255), stop:1 rgba(255, 255, 255, 255));")
        self.lineEdit_config_pumpid.setObjectName("lineEdit_config_pumpid")
        self.lineEdit_config_pumpid.setText(_translate("B3GUI", "1"))
        self.lineEdit_config_pumpid.setReadOnly(True)
        self.gridLayout_config.addWidget(self.lineEdit_config_pumpid, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.lineEdit_config_ingName = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_config_ingName.setAutoFillBackground(False)
        self.lineEdit_config_ingName.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:0, stop:0 rgba(136, 138, 133, 255), stop:1 rgba(255, 255, 255, 255));")
        self.lineEdit_config_ingName.setObjectName("lineEdit_config_ingName")
        self.lineEdit_config_ingName.setText(_translate("B3GUI", "Test Liquor A"))
        self.lineEdit_config_ingName.setReadOnly(True)
        self.gridLayout_config.addWidget(self.lineEdit_config_ingName, 1, 2, 1, 1)
        self.lineEdit_config_pumpid_3 = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_config_pumpid_3.setMaximumSize(QtCore.QSize(35, 16777215))
        self.lineEdit_config_pumpid_3.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:0, stop:0 rgba(136, 138, 133, 255), stop:1 rgba(255, 255, 255, 255));")
        self.lineEdit_config_pumpid_3.setObjectName("lineEdit_config_pumpid_3")
        self.lineEdit_config_pumpid_3.setText(_translate("B3GUI", "3"))
        self.lineEdit_config_pumpid_3.setReadOnly(True)
        self.gridLayout_config.addWidget(self.lineEdit_config_pumpid_3, 3, 0, 1, 1, QtCore.Qt.AlignRight)
        self.label_config_ingNameHead = QtWidgets.QLabel(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_config_ingNameHead.sizePolicy().hasHeightForWidth())
        self.label_config_ingNameHead.setSizePolicy(sizePolicy)
        self.label_config_ingNameHead.setMinimumSize(QtCore.QSize(0, 70))
        self.label_config_ingNameHead.setAlignment(QtCore.Qt.AlignCenter)
        self.label_config_ingNameHead.setObjectName("label_config_ingNameHead")
        self.label_config_ingNameHead.setText(_translate("B3GUI", "Ingredient"))
        self.gridLayout_config.addWidget(self.label_config_ingNameHead, 0, 2, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_config.addItem(spacerItem6, 4, 2, 1, 1)
        self.label_config_ingAmountHead = QtWidgets.QLabel(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_config_ingAmountHead.sizePolicy().hasHeightForWidth())
        self.label_config_ingAmountHead.setSizePolicy(sizePolicy)
        self.label_config_ingAmountHead.setMinimumSize(QtCore.QSize(0, 70))
        self.label_config_ingAmountHead.setAlignment(QtCore.Qt.AlignCenter)
        self.label_config_ingAmountHead.setObjectName("label_config_ingAmountHead")
        self.label_config_ingAmountHead.setText(_translate("B3GUI", "Amount\nRemaining"))
        self.gridLayout_config.addWidget(self.label_config_ingAmountHead, 0, 4, 1, 1)
        self.label_config_ingUnitHead = QtWidgets.QLabel(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_config_ingUnitHead.sizePolicy().hasHeightForWidth())
        self.label_config_ingUnitHead.setSizePolicy(sizePolicy)
        self.label_config_ingUnitHead.setMinimumSize(QtCore.QSize(25, 70))
        self.label_config_ingUnitHead.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_config_ingUnitHead.setObjectName("label_config_ingUnitHead")
        self.label_config_ingUnitHead.setText(_translate("B3GUI", "Unit"))
        self.gridLayout_config.addWidget(self.label_config_ingUnitHead, 0, 5, 1, 1)
        self.label_config_unit = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_config_unit.setObjectName("label_config_unit")
        self.label_config_unit.setText(_translate("B3GUI", "mL"))
        self.gridLayout_config.addWidget(self.label_config_unit, 1, 5, 1, 1)    
        self.buttonBox_config = QtWidgets.QDialogButtonBox(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox_config.sizePolicy().hasHeightForWidth())
        self.buttonBox_config.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 136, 136))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 136, 136))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 136, 136))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.buttonBox_config.setPalette(palette)
        self.buttonBox_config.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.buttonBox_config.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox_config.setStandardButtons(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Reset)
        self.buttonBox_config.setCenterButtons(False)
        self.buttonBox_config.setObjectName("buttonBox_config")

        self.buttonBox_config.accepted.connect(self.configAdd)
        self.buttonBox_config.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self.configReset)

        self.gridLayout_config.addWidget(self.buttonBox_config, 5, 4, 1, 1)
        self.label_config_unit_2 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_config_unit_2.setObjectName("label_config_unit_2")
        self.label_config_unit_2.setText(_translate("B3GUI", "mL"))
        self.gridLayout_config.addWidget(self.label_config_unit_2, 2, 5, 1, 1)
        self.lineEdit_config_pumpid_2 = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_config_pumpid_2.setMaximumSize(QtCore.QSize(35, 16777215))
        self.lineEdit_config_pumpid_2.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:0, stop:0 rgba(136, 138, 133, 255), stop:1 rgba(255, 255, 255, 255));")
        self.lineEdit_config_pumpid_2.setObjectName("lineEdit_config_pumpid_2")
        self.lineEdit_config_pumpid_2.setText(_translate("B3GUI", "2"))
        self.lineEdit_config_pumpid_2.setReadOnly(True)
        self.gridLayout_config.addWidget(self.lineEdit_config_pumpid_2, 2, 0, 1, 1, QtCore.Qt.AlignRight)
        self.label_config_unit_3 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_config_unit_3.setObjectName("label_config_unit_3")
        self.label_config_unit_3.setText(_translate("B3GUI", "mL"))
        self.gridLayout_config.addWidget(self.label_config_unit_3, 3, 5, 1, 1)
        self.lineEdit_config_ingName_3 = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_config_ingName_3.setAutoFillBackground(False)
        self.lineEdit_config_ingName_3.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:0, stop:0 rgba(136, 138, 133, 255), stop:1 rgba(255, 255, 255, 255));")
        self.lineEdit_config_ingName_3.setText("Test Ingredient A")
        self.lineEdit_config_ingName_3.setObjectName("lineEdit_config_ingName_3")
        self.lineEdit_config_ingName_3.setReadOnly(True)
        self.gridLayout_config.addWidget(self.lineEdit_config_ingName_3, 3, 2, 1, 1)
        self.lineEdit_config_ingName_2 = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_config_ingName_2.setAutoFillBackground(False)
        self.lineEdit_config_ingName_2.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:0, stop:0 rgba(136, 138, 133, 255), stop:1 rgba(255, 255, 255, 255));")
        self.lineEdit_config_ingName_2.setText("Test Liquor B")
        self.lineEdit_config_ingName_2.setObjectName("lineEdit_config_ingName_2")
        self.lineEdit_config_ingName_2.setReadOnly(True)
        self.gridLayout_config.addWidget(self.lineEdit_config_ingName_2, 2, 2, 1, 1)
        self.label_config_pumpHead = QtWidgets.QLabel(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_config_pumpHead.sizePolicy().hasHeightForWidth())
        self.label_config_pumpHead.setSizePolicy(sizePolicy)
        self.label_config_pumpHead.setMinimumSize(QtCore.QSize(40, 0))
        self.label_config_pumpHead.setAlignment(QtCore.Qt.AlignCenter)
        self.label_config_pumpHead.setObjectName("label_config_pumpHead")
        self.gridLayout_config.addWidget(self.label_config_pumpHead, 0, 0, 1, 1, QtCore.Qt.AlignRight)
        self.line_configing = QtWidgets.QFrame(self.gridLayoutWidget_2)
        self.line_configing.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_configing.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_configing.setObjectName("line_configing")
        self.gridLayout_config.addWidget(self.line_configing, 1, 3, 1, 1, QtCore.Qt.AlignHCenter)
        self.line_configpump = QtWidgets.QFrame(self.gridLayoutWidget_2)
        self.line_configpump.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_configpump.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_configpump.setObjectName("line_configpump")
        self.gridLayout_config.addWidget(self.line_configpump, 1, 1, 1, 1)
        self.lineEdit_config_ingAmount = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_config_ingAmount.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lineEdit_config_ingAmount.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:0, stop:0 rgba(136, 138, 133, 255), stop:1 rgba(255, 255, 255, 255));")
        self.lineEdit_config_ingAmount.setObjectName("lineEdit_config_ingAmount")
        self.lineEdit_config_ingAmount.setText(_translate("B3GUI", "300"))
        self.lineEdit_config_ingAmount.setReadOnly(True)
        self.gridLayout_config.addWidget(self.lineEdit_config_ingAmount, 1, 4, 1, 1)
        self.lineEdit_config_ingAmount_2 = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_config_ingAmount_2.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lineEdit_config_ingAmount_2.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:0, stop:0 rgba(136, 138, 133, 255), stop:1 rgba(255, 255, 255, 255));")
        self.lineEdit_config_ingAmount_2.setObjectName("lineEdit_config_ingAmount_2")
        self.lineEdit_config_ingAmount_2.setText(_translate("B3GUI", "300"))
        self.lineEdit_config_ingAmount_2.setReadOnly(True)
        self.gridLayout_config.addWidget(self.lineEdit_config_ingAmount_2, 2, 4, 1, 1)
        self.lineEdit_config_ingAmount_3 = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_config_ingAmount_3.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lineEdit_config_ingAmount_3.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:0, stop:0 rgba(136, 138, 133, 255), stop:1 rgba(255, 255, 255, 255));")
        self.lineEdit_config_ingAmount_3.setObjectName("lineEdit_config_ingAmount_3")
        self.lineEdit_config_ingAmount_3.setText(_translate("B3GUI", "300"))
        self.lineEdit_config_ingAmount_3.setReadOnly(True)
        self.gridLayout_config.addWidget(self.lineEdit_config_ingAmount_3, 3, 4, 1, 1)
        self.line_configpump_3 = QtWidgets.QFrame(self.gridLayoutWidget_2)
        self.line_configpump_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_configpump_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_configpump_3.setObjectName("line_configpump_3")
        self.gridLayout_config.addWidget(self.line_configpump_3, 3, 1, 1, 1)
        self.line_configpump_2 = QtWidgets.QFrame(self.gridLayoutWidget_2)
        self.line_configpump_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_configpump_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_configpump_2.setObjectName("line_configpump_2")
        self.gridLayout_config.addWidget(self.line_configpump_2, 2, 1, 1, 1)
        self.line_configing_2 = QtWidgets.QFrame(self.gridLayoutWidget_2)
        self.line_configing_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_configing_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_configing_2.setObjectName("line_configing_2")
        self.gridLayout_config.addWidget(self.line_configing_2, 2, 3, 1, 1)
        self.line_configing_3 = QtWidgets.QFrame(self.gridLayoutWidget_2)
        self.line_configing_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_configing_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_configing_3.setObjectName("line_configing_3")
        self.gridLayout_config.addWidget(self.line_configing_3, 3, 3, 1, 1)
        self.widget_config_rightInfo = QtWidgets.QListWidget(self.page_config)
        self.widget_config_rightInfo.setGeometry(QtCore.QRect(560, 0, 81, 482))
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
        self.widget_config_rightInfo.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.widget_config_rightInfo.setFont(font)
        self.widget_config_rightInfo.setObjectName("widget_config_rightInfo")
        self.widget_config_rightInfo.raise_()
        self.frame_config.raise_()
        self.pushButton_config_toMain.raise_()
        
        self.pushButton_config_toMain.clicked.connect(self.toPrimary)
        
        self.stackedWidget.addWidget(self.page_config)

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
                    gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 451, 415))
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
                pushButton.setMinimumSize(QtCore.QSize(0, 120))
                #pushButton.setFlat(True)
                pushButton.setPalette(self.paletteButton)
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
                label_recipeIng.setMinimumSize(QtCore.QSize(0, 56))
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
                    spacerItem = QtWidgets.QSpacerItem(13, 32, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                    gridLayout_menu.addItem(spacerItem, (int(((menuCount%4)-1)/2)), 1, 1, 1)

                if (menuCount%4 == 3):
                    gridLayout_menu.itemAtPosition(0, 0).invalidate()
    
                menuCount += 1
        if (menuCount%4 == 1 or menuCount%4 == 2):
            spacerItem = QtWidgets.QSpacerItem(13, 32, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            gridLayout_menu.addItem(spacerItem, 1, 1, 1, 1)
        if (menuCount%4 == 1):
            spacerItem = QtWidgets.QSpacerItem(25, 16, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
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
            self.pushButton_menuLeft.setGeometry(QtCore.QRect(188, 440, 76, 33))
            self.pushButton_menuLeft.setPalette(self.paletteButton)
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
            self.pushButton_menuRight.setGeometry(QtCore.QRect(375, 440, 76, 33))
            self.pushButton_menuRight.setPalette(self.paletteButton)
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
            #print(orderRaw)
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
            #print(order)
            pubMQTT(client, ORDER, order)
            self.toPrimary()
        else:
            print("Please place a cup in Alfred the Butler's tray.")

    def quickOrder(self):
        if bartOrder != "":
            pubMQTT(client, ORDER, bartOrder)
            self.toPrimary()

    def customReset(self):
        for i in range(1, self.gridLayout_custom.rowCount() - 2):
            self.gridLayout_custom.itemAtPosition(i, 0).widget().clear()
            self.gridLayout_custom.itemAtPosition(i, 2).widget().clear()
            
    def customAdd(self):
        self.recipeName = None
        self.customAddConfirm = QtWidgets.QDialog()
        self.customAddConfirm.setObjectName("CustomAddConfirmWindow")
        self.customAddConfirm.setGeometry(160, 240, 320, 160)
        self.layout_customAddConfirm = QtWidgets.QVBoxLayout(self.customAddConfirm)
        self.layout_customAddConfirm.setObjectName("CustomverticalLayout")

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.customAddConfirm.setPalette(palette)

        label_customAddConfirm = QtWidgets.QLabel()
        label_customAddConfirm.setAlignment(QtCore.Qt.AlignCenter)
        label_customAddConfirm.setWordWrap(True)
        label_customAddConfirm.setObjectName("label_customAddConfirm")
        self.layout_customAddConfirm.addWidget(label_customAddConfirm)

        lineEdit_custom_recipeName = QtWidgets.QLineEdit()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(lineEdit_custom_recipeName.sizePolicy().hasHeightForWidth())
        lineEdit_custom_recipeName.setSizePolicy(sizePolicy)
        lineEdit_custom_recipeName.setMinimumSize(QtCore.QSize(220, 0))
        lineEdit_custom_recipeName.setObjectName("lineEdit_custom_recipeName")
        self.layout_customAddConfirm.addWidget(lineEdit_custom_recipeName, 0, QtCore.Qt.AlignHCenter)

        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.layout_customAddConfirm.addItem(spacerItem)
       
        dialog_customAddConfirm = QtWidgets.QDialogButtonBox()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialog_customAddConfirm.sizePolicy().hasHeightForWidth())
        dialog_customAddConfirm.setSizePolicy(sizePolicy)
        dialog_customAddConfirm.setOrientation(QtCore.Qt.Horizontal)
        dialog_customAddConfirm.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        dialog_customAddConfirm.setCenterButtons(True)
        dialog_customAddConfirm.setObjectName("buttonBox_customAddConfirm")
        self.layout_customAddConfirm.addWidget(dialog_customAddConfirm)

        _translate = QtCore.QCoreApplication.translate
        self.customAddConfirm.setWindowTitle(_translate("CustomAddConfirmWindow", "CustomDialog"))
        label_customAddConfirm.setText(_translate("CustomAddConfirmWindow", "Choose a name for you custom recipe."))
        dialog_customAddConfirm.accepted.connect(self.customConfirm)
        dialog_customAddConfirm.rejected.connect(self.customAddConfirm.destroy)
        self.layout_customAddConfirm.addWidget(dialog_customAddConfirm)
        
        self.customAddConfirm.setLayout(self.layout_customAddConfirm)

        self.customAddConfirm.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #self.customAddConfirm.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.customAddConfirm.show()

    def customConfirm(self):
        self.recipeName = self.layout_customAddConfirm.itemAt(1).widget().text()
        for i in range(1, self.gridLayout_custom.rowCount() - 2):
            ingName = str(self.gridLayout_custom.itemAtPosition(i, 0).widget().text())
            ingAmnt = str(self.gridLayout_custom.itemAtPosition(i, 2).widget().text())
            values = None
            values = "\'" + self.recipeName + "\', \'" + ingName + "\', \'" + ingAmnt + "\'"
            if ingName != "" and ingAmnt != "" and self.recipeName != "":
                insertSQL(cursor, "recipes", "recipe_name, ingredient_name, ingredient_amount_", values)
        self.customAddConfirm.destroy

    def configInit(self):
        

        return layout

    def configReset(self):
        for i in range(1, self.gridLayout_config.rowCount() - 2):
            self.gridLayout_config.itemAtPosition(i, 0).widget().clear()
            self.gridLayout_config.itemAtPosition(i, 1).widget().clear()
            self.gridLayout_config.itemAtPosition(i, 3).widget().clear()
        '''for i in range(1, self.gridLayout_config.rowCount() - 2):
            pumpid = str(self.gridLayout_config.itemAtPosition(i, 0).widget().text())
            ingName = str(self.gridLayout_config.itemAtPosition(i, 1).widget().text())
            ingAmnt = str(self.gridLayout_config.itemAtPosition(i, 3).widget().text())
            print(ingName)
            print(ingAmnt)
            if i == 3:
            self.gridLayout_config.itemAtPosition(i, 1).widget().clear()
            self.gridLayout_config.itemAtPosition(i, 3).widget().clear()'''
            
    def configAdd(self):
        self.configAddConfirm.setObjectName("ConfigWindow")
        self.configAddConfirm.setGeometry(160, 240, 320, 160)
        self.layout_configAddConfirm = QtWidgets.QVBoxLayout(self.configAddConfirm)
        self.layout_configAddConfirm.setObjectName("verticalLayout")

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.configAddConfirm.setPalette(palette)

        label_configAddConfirm = QtWidgets.QLabel()
        label_configAddConfirm.setAlignment(QtCore.Qt.AlignCenter)
        label_configAddConfirm.setWordWrap(True)
        label_configAddConfirm.setObjectName("label_configAddConfirm")
        self.layout_configAddConfirm.addWidget(label_configAddConfirm)

        lineEdit_config_recipeName = QtWidgets.QLineEdit()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(lineEdit_config_recipeName.sizePolicy().hasHeightForWidth())
        lineEdit_config_recipeName.setSizePolicy(sizePolicy)
        lineEdit_config_recipeName.setMinimumSize(QtCore.QSize(220, 0))
        lineEdit_config_recipeName.setObjectName("lineEdit_config_recipeName")
        self.layout_configAddConfirm.addWidget(lineEdit_config_recipeName, 0, QtCore.Qt.AlignHCenter)

        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.layout_configAddConfirm.addItem(spacerItem)

       
        dialog_configAddConfirm = QtWidgets.QDialogButtonBox()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialog_configAddConfirm.sizePolicy().hasHeightForWidth())
        dialog_configAddConfirm.setSizePolicy(sizePolicy)
        dialog_configAddConfirm.setOrientation(QtCore.Qt.Horizontal)
        dialog_configAddConfirm.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        dialog_configAddConfirm.setCenterButtons(True)
        dialog_configAddConfirm.setObjectName("buttonBox_configAddConfirm")
        self.layout_configAddConfirm.addWidget(dialog_configAddConfirm)

        _translate = QtCore.QCoreApplication.translate
        self.configAddConfirm.setWindowTitle(_translate("ConfigAddConfirmWindow", "ConfigDialog"))
        label_configAddConfirm.setText(_translate("ConfigAddConfirmWindow", "Are you sure you want to make these changes?"))
        dialog_configAddConfirm.accepted.connect(self.configConfirm)
        dialog_configAddConfirm.rejected.connect(self.configAddConfirm.destroy)
        self.layout_configAddConfirm.addWidget(dialog_configAddConfirm)
        
        self.configAddConfirm.setLayout(self.layout_configAddConfirm)

        self.configAddConfirm.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #self.configAddConfirm.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.configAddConfirm.show()        

    def configConfirm(self):
        for i in range(1, self.gridLayout_config.rowCount() - 2):
            pumpid = str(self.gridLayout_config.itemAtPosition(i, 0).widget().text())
            ingName = str(self.gridLayout_config.itemAtPosition(i, 1).widget().text())
            ingAmnt = str(self.gridLayout_config.itemAtPosition(i, 3).widget().text())
            values = None
            values = "\'" + pumpid + "\', \'" + ingName + "\', \'" + ingAmnt + "\'"
            if ingName != "" and ingAmnt != "" and pump_id != "":
                insertSQL(cursor, "config", "pump_id, ingredient_name, inventory", values)
    
        self.configAddConfirm.destroy
        
    def test(self):
        pubMQTT(client, STARTSIGNAL, "hi yianni")

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
        self.pushButton_menuRight.setText(_translate("B3GUI", "------->"))
        self.label_51.setText(_translate("B3GUI", "Ingredient 2"))
        self.label_52.setText(_translate("B3GUI", "Ingredient 1"))
        self.label_53.setText(_translate("B3GUI", "Ingredient 3"))
        self.label_54.setText(_translate("B3GUI", "Temp Custom Drank Layout"))
        self.label_55.setText(_translate("B3GUI", "Ingredient 2"))
        self.label_56.setText(_translate("B3GUI", "Ingredient 1"))
        self.label_57.setText(_translate("B3GUI", "Ingredient 3"))
        self.label_58.setText(_translate("B3GUI", "This is not currently finalized"))'''
        self.pushButton_config_toMain.setText(_translate("B3GUI", "Return"))
        '''self.label_config_ingNameHead.setText(_translate("B3GUI", "Ingredient Name"))
        self.label_config_ingAmountHead.setText(_translate("B3GUI", "Amount"))
        self.label_config_ingUnitHead.setText(_translate("B3GUI", "Unit"))
        self.label_config_unit.setText(_translate("B3GUI", "mL"))
        self.label_config_unit_2.setText(_translate("B3GUI", "mL"))
        self.label_config_unit_3.setText(_translate("B3GUI", "mL"))'''
        self.label_config_pumpHead.setText(_translate("B3GUI", "Pump ID"))

    def toMenu(self):
        self.stackedWidget.setCurrentIndex(1)

    def toConfig(self):
        self.stackedWidget.setCurrentIndex(3)

    def toCustom(self):
        self.stackedWidget.setCurrentIndex(2)

    def toPrimary(self):
        self.retranslateUi()
        self.stackedWidget.setCurrentIndex(0)

        
    def cupGift(self): ##purely for test purposes in toggling cup present flag
        global cupPresent
        temp = not cupPresent
        print("~~MQTT~~ Received message \"" + "1" + "\" from topic \"" + "alfred/cupStatus" + "\".")
        cupPresent = temp

    def dock(self):
        pubMQTT(client, DOCK, "hey this is the emergency dock signal")
        
    def exitPopup(self):
        self.exit.setObjectName("ExitWindow")
        self.exit.setGeometry(208, 280, 225, 120)
        self.exitLayout = QtWidgets.QGridLayout()

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.exit.setPalette(palette)
        
        self.exitDialog = QtWidgets.QDialogButtonBox(self.exit)
        self.exitDialog.setGeometry(QtCore.QRect(56, 88, 50, 26))
        
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
        self.exitLabel.setGeometry(QtCore.QRect(66, 24, 101, 57))
        self.exitLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.exitLabel.setWordWrap(True)
        self.exitLabel.setObjectName("label")

        _translate = QtCore.QCoreApplication.translate
        self.exit.setWindowTitle(_translate("ExitWindow", "Dialog"))
        self.exitLabel.setText(_translate("ExitWindow", "Are you sure you want to quit?"))
        self.exitDialog.accepted.connect(self.killUi)
        self.exitDialog.rejected.connect(self.exit.destroy)

        self.exitLayout.addWidget(self.exitLabel, 0, 0)
        self.exitLayout.addWidget(self.exitDialog, 1, 0)
        self.exit.setLayout(self.exitLayout)

        self.exit.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.exit.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.exit.show()

    def killUi(self):
        print("")
        self.exit.destroy()
        closeSQL(sqlConnect)
        client.disconnect()
        QtCore.QCoreApplication.instance().quit
        sys.exit()


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
