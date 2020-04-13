# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stackedFinalSetup.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

import textwrap
import sys, time
import paho.mqtt.client as mqtt
import sqlite3
from sqlite3 import Error
from PyQt5 import QtCore, QtGui, QtWidgets

client = None 
MQTT_SERVER = "localhost"
MQTT_SERVERP = "192.168.1.73"
MQTT_SERVERD = "192.168.1.78"
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
STARTSIGNAL = "app/start"
BARTSTATUS = "bart/status"
BARTSENSOR = "bart/sr/alignment"
BOTSTATUS = "bot/status"

#### FLAGS  ####
bartConnected = "disconnected"
bartOrder = ""
bartAligned = False
bartTemp = False

systemReady = True

alfredLocation = ""
botAtBar = False


########################## MQTT SETUP ##########################
    
def on_message(client, userdata, message):
    #print(message.topic+" "+str(message.payload))
    msg = str(message.payload.decode("utf-8"))
    print("~~MQTT~~ Received message \"" + msg + "\" from topic \"" + message.topic + "\".")

    global bartConnected
    global systemReady
    global bartAligned
    global botAtBar
    global alfredLocation
    
     
    if message.topic == BARTSTATUS:
        print("Bartender is " + msg)
        bartConnected = msg
        if msg == "intake":
            systemReady = False

    if message.topic == BARTSENSOR:
        if msg == "true":
            bartAligned = True
            if (bartAligned and botAtBar and systemReady):
                pubMQTT(client, ORDER, bartOrder)
        else:
            bartAligned = False
        
        
    if message.topic == BOTSTATUS:
        alfredLocation = msg
        if msg == "docked@bar":
            botAtBar = True
        elif msg == "docked@base":
            time.sleep(10)
            botAtBar = False
            systemReady = True
        else:
            botAtBar = False
        
    
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
    
    ip = MQTT_SERVERP
    print("~~MQTT~~ Attempting broker connection:  ", ip)
    client.connect(ip, MQTT_PORT)
    
    while not client.connected_flag: #wait in loop
        time.sleep(1)
        if client.connected_flag != True:
            print("~~MQTT~~ Connecting...")

    print("~~MQTT~~ Initialized.")
    client.subscribe([(BARTSENSOR, 1), (BARTSTATUS, 2), (BOTSTATUS, 2)])

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
        print("Successfully inserted \"" + str(values) + 
              "\" into table \"" + str(tableName) + "\"")
        sqlConnect.commit()
    except Error as e:
        print(e)

def fetchSQL(self, table, column, condtional, condition):
    try:
        if isinstance(condition, str):
            conditionCheck = '\'' + str(condition) + '\''
        else:
            conditionCheck = str(condition)
        cursor.execute('SELECT * FROM ' + str(table) + ' WHERE ' + 
                       str(column) + str(condtional) + conditionCheck)
        value = cursor.fetchall()
        return value
    except Error as e:
        print(e)

def updateSQL(self, table, updatedInfo, column, conditional, condition):
    try:
        if isinstance(condition, str):
            conditionCheck = '\'' + str(condition) + '\''
        else:
            conditionCheck = str(condition)
        print('UPDATE ' + str(table) + ' SET ' + updatedInfo + ' WHERE ' + 
                   str(column) + str(conditional) + conditionCheck)
        cursor.execute('UPDATE ' + str(table) + ' SET ' + updatedInfo + ' WHERE ' + 
                       str(column) + str(conditional) + conditionCheck)
        sqlConnect.commit()        
    except Error as e:
        print(e)
        
def deleteSQL(self, table, column, conditional, condition):
    try:
        if isinstance(condition, str):
            conditionCheck = '\'' + str(condition) + '\''
        else:
            conditionCheck = str(condition)
            print(('DELETE FROM ' + str(table) + ' WHERE ' + 
                       str(column) + str(condtional) + conditionCheck))
        cursor.execute('DELETE FROM ' + str(table) + ' WHERE ' + 
                       str(column) + str(condtional) + conditionCheck)
        sqlConnect.commit()
        print("Successfully deleted all values in table \"" + str(table) + "\"")
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

        self.paletteWButton = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(186, 189, 182))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.paletteWButton.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(186, 189, 182))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.paletteWButton.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(186, 189, 182))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.paletteWButton.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)

        self.paletteWidget = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.paletteWidget.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.paletteWidget.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.paletteWidget.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.paletteWidget.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.paletteWidget.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.paletteWidget.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)

        self.palettePBar = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(175, 50, 25))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.palettePBar.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(225, 225, 225))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.palettePBar.setBrush(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 50, 25))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.palettePBar.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(225, 225, 225))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.palettePBar.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(145, 145, 145))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.palettePBar.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(225, 225, 225))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.palettePBar.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(186, 189, 182))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.palettePBar.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)

        self.paletteLine = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(175, 50, 25))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.paletteLine.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 50, 25))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.paletteLine.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 50, 25))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.paletteLine.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        
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
        #self.configRefresh()
        timer_battery = QtCore.QTimer(self)
        timer_battery.setInterval(72000)
        timer_battery.start()
        timer_battery.timeout.connect(self.batteryDecay)
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
        
        self.pushButton_toMenu = QtWidgets.QPushButton(self.page)
        self.pushButton_toMenu.setGeometry(QtCore.QRect(25, 25, 429, 161))
        self.pushButton_toMenu.setPalette(self.paletteButton)
        font = QtGui.QFont()
        font.setFamily("STLiti")
        font.setPointSize(60)
        self.pushButton_toMenu.setFont(font)
        self.pushButton_toMenu.setObjectName("pushButton_toMenu")
        self.pushButton_curOrder = QtWidgets.QPushButton(self.page)
        self.pushButton_curOrder.setGeometry(QtCore.QRect(25, 211, 202, 100))
        self.pushButton_curOrder.setPalette(self.paletteButton)
        font = QtGui.QFont()
        font.setFamily("STLiti")
        font.setPointSize(26)
        self.pushButton_curOrder.setFont(font)
        self.pushButton_curOrder.setObjectName("pushButton_curOrder")
        self.widget_curOrder = QtWidgets.QListWidget(self.page)
        self.widget_curOrder.setGeometry(QtCore.QRect(252, 211, 202, 201))
        self.widget_curOrder.setPalette(self.paletteWidget)
        self.widget_curOrder.setObjectName("widget_curOrder")
        self.label_curOrder = QtWidgets.QLabel(self.page)
        self.label_curOrder.setGeometry(QtCore.QRect(259, 227, 170, 22))
        font = QtGui.QFont()
        font.setFamily("STLiti")
        font.setPointSize(16)
        self.label_curOrder.setFont(font)
        self.label_curOrder.setObjectName("label_curOrder")
        self.label_curOrder_Name = QtWidgets.QLabel(self.page)
        self.label_curOrder_Name.setGeometry(QtCore.QRect(261, 250, 170, 28))
        font = QtGui.QFont()
        font.setFamily("STLiti")
        font.setPointSize(14)
        self.label_curOrder_Name.setFont(font)
        self.label_curOrder_Name.setObjectName("label_curOrder_Name")
        self.line = QtWidgets.QFrame(self.page)
        self.line.setGeometry(QtCore.QRect(259, 275, 189, 13))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setPalette(self.paletteLine)
        self.line.setObjectName("line")
        self.label_curOrder_IngName = QtWidgets.QLabel(self.page)
        self.label_curOrder_IngName.setGeometry(QtCore.QRect(261, 291, 96, 120))
        self.label_curOrder_IngName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_curOrder_IngName.setObjectName("label_curOrder_IngName")
        self.label_curOrder_IngAmount = QtWidgets.QLabel(self.page)
        self.label_curOrder_IngAmount.setGeometry(QtCore.QRect(371, 291, 76, 72))
        self.label_curOrder_IngAmount.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_curOrder_IngAmount.setObjectName("label_curOrder_IngAmount")
        
        '''self.pushButton_advTools = QtWidgets.QPushButton(self.page)
        self.pushButton_advTools.setGeometry(QtCore.QRect(25, 332, 60, 80))
        self.pushButton_advTools.setPalette(self.paletteButton)
        font = QtGui.QFont()
        font.setFamily("STLiti")
        self.pushButton_advTools.setFont(font)
        self.pushButton_advTools.setObjectName("pushButton_advTools")'''
        self.pushButton_dock = QtWidgets.QPushButton(self.page)
        self.pushButton_dock.setGeometry(QtCore.QRect(25, 328, 95, 84))
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
        font.setFamily("STLiti")
        font.setPointSize(20)
        self.pushButton_dock.setFont(font)
        self.pushButton_dock.setObjectName("pushButton_dock")
        self.pushButton_quit = QtWidgets.QPushButton(self.page)
        self.pushButton_quit.setGeometry(QtCore.QRect(132, 328, 95, 84))
        self.pushButton_quit.setPalette(self.paletteButton)
        font = QtGui.QFont()
        font.setFamily("STLiti")
        font.setPointSize(20)
        self.pushButton_quit.setFont(font)
        self.pushButton_quit.setObjectName("pushButton_quit")
        
        
        
        
        
        self.widget_rightInfo = QtWidgets.QListWidget(self.page)
        self.widget_rightInfo.setGeometry(QtCore.QRect(480, -1, 161, 482))
        self.widget_rightInfo.setPalette(self.paletteWidget)
        font = QtGui.QFont()
        font.setFamily("STLiti")
        self.widget_rightInfo.setFont(font)
        self.widget_rightInfo.setObjectName("widget_rightInfo")

        self.pushButton_config = QtWidgets.QPushButton(self.page)
        self.pushButton_config.setGeometry(QtCore.QRect(513, 24, 101, 49))
        self.pushButton_config.setPalette(self.paletteWButton)
        font = QtGui.QFont()
        font.setFamily("STLiti")
        font.setPointSize(12)
        font.setWeight(QtGui.QFont.Medium)
        self.pushButton_config.setFont(font)
        self.pushButton_config.setObjectName("pushButton_config")

        self.formLayoutWidget_progress = QtWidgets.QWidget(self.page)
        self.formLayoutWidget_progress.setGeometry(QtCore.QRect(480, 83, 155, 180))
        self.formLayoutWidget_progress.setObjectName("self.formLayoutWidget_progress")
        formLayout_progress = QtWidgets.QFormLayout(self.formLayoutWidget_progress)
        formLayout_progress.setVerticalSpacing(20)
        formLayout_progress.setFormAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignCenter)
        formLayout_progress.setContentsMargins(0, 0, 0, 0)
        formLayout_progress.setObjectName("formLayout_progress")

        label_progress = QtWidgets.QLabel()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(label_progress.sizePolicy().hasHeightForWidth())
        label_progress.setSizePolicy(sizePolicy)
        label_progress.setWordWrap(True)
        label_progress.setMinimumSize(QtCore.QSize(75, 20))
        label_progress.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        label_progress.setFont(font)
        label_progress.setObjectName("label_progress")
        label_progress.setText(_translate("B3GUI", "Ing. A"))
        formLayout_progress.setWidget(0, QtWidgets.QFormLayout.LabelRole, label_progress)
        
        progressBar_progress = QtWidgets.QProgressBar()
        progressBar_progress.setMinimumSize(QtCore.QSize(0, 25))
        progressBar_progress.setMaximumSize(QtCore.QSize(69, 16777215))
        progressBar_progress.setPalette(self.palettePBar)
        font = QtGui.QFont()
        font.setFamily("Piboto Thin")
        progressBar_progress.setFont(font)
        progressBar_progress.setProperty("value", 100)
        progressBar_progress.setObjectName("progressBar_progress")
        formLayout_progress.setWidget(0, QtWidgets.QFormLayout.FieldRole, progressBar_progress)

        label_progress_1 = QtWidgets.QLabel()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(label_progress_1.sizePolicy().hasHeightForWidth())
        label_progress_1.setSizePolicy(sizePolicy)
        label_progress_1.setWordWrap(True)
        label_progress_1.setMinimumSize(QtCore.QSize(75, 20))
        label_progress_1.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        label_progress_1.setFont(font)
        label_progress_1.setObjectName("label_progress_1")
        label_progress_1.setText(_translate("B3GUI", "Ing. A"))
        formLayout_progress.setWidget(1, QtWidgets.QFormLayout.LabelRole, label_progress_1)
        
        progressBar_progress_1 = QtWidgets.QProgressBar()
        progressBar_progress_1.setMinimumSize(QtCore.QSize(0, 25))
        progressBar_progress_1.setMaximumSize(QtCore.QSize(69, 16777215))
        progressBar_progress_1.setPalette(self.palettePBar)
        font = QtGui.QFont()
        font.setFamily("Piboto Thin")
        progressBar_progress_1.setFont(font)
        progressBar_progress_1.setProperty("value", 100)
        progressBar_progress_1.setObjectName("progressBar_progress_1")
        formLayout_progress.setWidget(1, QtWidgets.QFormLayout.FieldRole, progressBar_progress_1)

        label_progress_2 = QtWidgets.QLabel()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(label_progress_2.sizePolicy().hasHeightForWidth())
        label_progress_2.setSizePolicy(sizePolicy)
        label_progress_2.setWordWrap(True)
        label_progress_2.setMinimumSize(QtCore.QSize(75, 20))
        label_progress_2.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        label_progress_2.setFont(font)
        label_progress_2.setObjectName("label_progress_2")
        label_progress_2.setText(_translate("B3GUI", "Ing. A"))
        formLayout_progress.setWidget(2, QtWidgets.QFormLayout.LabelRole, label_progress_2)
        
        progressBar_progress_2 = QtWidgets.QProgressBar()
        progressBar_progress_2.setMinimumSize(QtCore.QSize(0, 25))
        progressBar_progress_2.setMaximumSize(QtCore.QSize(69, 16777215))
        progressBar_progress_2.setPalette(self.palettePBar)
        font = QtGui.QFont()
        font.setFamily("Piboto Thin")
        progressBar_progress_2.setFont(font)
        progressBar_progress_2.setProperty("value", 100)
        progressBar_progress_2.setObjectName("progressBar_progress_2")
        formLayout_progress.setWidget(2, QtWidgets.QFormLayout.FieldRole, progressBar_progress_2)
        

        self.label_batteryCharge = QtWidgets.QLabel(self.page)
        self.label_batteryCharge.setGeometry(QtCore.QRect(488, 408, 88, 22))
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        self.label_batteryCharge.setFont(font)
        self.label_batteryCharge.setObjectName("label_batteryCharge")       
        self.progressBar_batteryCharge = QtWidgets.QProgressBar(self.page)
        self.progressBar_batteryCharge.setGeometry(QtCore.QRect(500, 432, 63, 25))
        self.progressBar_batteryCharge.setPalette(self.palettePBar)
        self.progressBar_batteryCharge.setValue(100)
        self.progressBar_batteryCharge.setMaximum(100)
        self.progressBar_batteryCharge.setObjectName("progressBar_batteryCharge")
        
        label_primary_imageB3 = QtWidgets.QLabel(self.page)
        image = QtGui.QPixmap('B3LogoResize.png')
        label_primary_imageB3.setGeometry(QtCore.QRect(567, 407, 66, 66))
        label_primary_imageB3.setPixmap(image)
        label_primary_imageB3.setObjectName("label_primary_imageB3")
        
        
        
        
        
        self.pushButton_toMenu.raise_()
        self.widget_curOrder.raise_()
        self.label_curOrder_IngAmount.raise_()
        self.pushButton_curOrder.raise_()
        self.pushButton_quit.raise_()
        #label_progress.raise_()
        self.label_curOrder.raise_()
        self.pushButton_dock.raise_()
        self.progressBar_batteryCharge.raise_()
        self.label_curOrder_Name.raise_()
        self.label_curOrder_IngName.raise_()
        #self.pushButton_advTools.raise_()
        self.label_batteryCharge.raise_()
        self.line.raise_()
        label_primary_imageB3.raise_()
        #progressBar_progress.raise_()
        self.pushButton_config.raise_()

        self.pushButton_dock.clicked.connect(self.dock)
        #self.pushButton_advTools.clicked.connect(self.cupGift)
        self.pushButton_quit.clicked.connect(self.exitPopup)
        self.pushButton_curOrder.clicked.connect(self.quickOrder)
        
        self.pushButton_config.clicked.connect(self.toConfig)
        self.pushButton_toMenu.clicked.connect(self.toMenu)
        
        self.stackedWidget.addWidget(self.page)

        ##################### Menu Page #####################
        
        self.page_menuWindow = QtWidgets.QWidget()   
        self.page_menuWindow.setObjectName("page_menuWindow")

        self.stackedMenuWidget = self.menuGenerate()
        self.stackedMenuWidget.setGeometry(QtCore.QRect(94, 16, 451, 417))
        self.stackedMenuWidget.setObjectName("stackedMenuWidget")
        self.stackedMenuWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)

        if self.stackedMenuWidget.count() > 1:
            self.pushButton_menuRight = QtWidgets.QPushButton(self.page_menuWindow)
            self.pushButton_menuRight.setGeometry(QtCore.QRect(375, 440, 76, 33))
            self.pushButton_menuRight.setPalette(self.paletteButton)
            self.pushButton_menuRight.setObjectName("pushButton_menuRight")
            self.pushButton_menuRight.setText("------->")
            self.pushButton_menuRight.clicked.connect(self.menuRight)
            

        self.widget_menu_rightInfo = QtWidgets.QListWidget(self.page_menuWindow)
        self.widget_menu_rightInfo.setGeometry(QtCore.QRect(560, -1, 81, 482))
        self.widget_menu_rightInfo.setPalette(self.paletteWidget)
        font = QtGui.QFont()
        font.setFamily("STLiti")
        self.widget_menu_rightInfo.setFont(font)
        self.widget_menu_rightInfo.setObjectName("widget_menu_rightInfo")
        self.widget_menu_leftInfo = QtWidgets.QListWidget(self.page_menuWindow)
        self.widget_menu_leftInfo.setGeometry(QtCore.QRect(-1, -1, 81, 482))
        self.widget_menu_leftInfo.setPalette(self.paletteWidget)
        font = QtGui.QFont()
        font.setFamily("STLiti")
        self.widget_menu_leftInfo.setFont(font)
        self.widget_menu_leftInfo.setObjectName("widget_menu_leftInfo")

        pushButton_pageToPrimary = QtWidgets.QPushButton(self.page_menuWindow)
        pushButton_pageToPrimary.setGeometry(QtCore.QRect(8, 350, 64, 61))
        pushButton_pageToPrimary.setPalette(self.paletteWButton)
        font = QtGui.QFont()
        font.setFamily("STLiti")
        font.setPointSize(12)
        font.setWeight(QtGui.QFont.Medium)
        pushButton_pageToPrimary.setFont(font)
        pushButton_pageToPrimary.setObjectName("pushButton_pageToPrimary")
        pushButton_pageToPrimary.setText(_translate("B3GUI", "Home"))
        
        pushButton_pageToCustom = QtWidgets.QPushButton(self.page_menuWindow)
        pushButton_pageToCustom.setGeometry(QtCore.QRect(8, 275, 64, 61))
        pushButton_pageToCustom.setPalette(self.paletteWButton)
        font = QtGui.QFont()
        font.setFamily("STLiti")
        font.setPointSize(12)
        font.setWeight(QtGui.QFont.Medium)
        pushButton_pageToCustom.setFont(font)
        pushButton_pageToCustom.setObjectName("pushButton_pageToCustom")
        pushButton_pageToCustom.setText(_translate("B3GUI", "Custom\nOrder"))
        
        label_menu_imageB3 = QtWidgets.QLabel(self.page_menuWindow)
        label_menu_imageB3.setGeometry(QtCore.QRect(567, 407, 66, 66))
        label_menu_imageB3.setPixmap(image)
        label_menu_imageB3.setObjectName("label_menu_imageB3")
        
        pushButton_pageToCustom.clicked.connect(self.toCustom)
        pushButton_pageToPrimary.clicked.connect(self.toPrimary)
        
        self.stackedWidget.addWidget(self.page_menuWindow)

        ##################### Custom page #####################

        self.page_custom = QtWidgets.QWidget()
        self.page_custom.setObjectName("page_custom")

        self.frame_2 = QtWidgets.QFrame(self.page_custom)
        self.frame_2.setGeometry(QtCore.QRect(94, 16, 451, 456))
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
        self.line_customing.setPalette(self.paletteLine)
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
        self.line_customing_2.setPalette(self.paletteLine)
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
        self.line_customing_3.setPalette(self.paletteLine)
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
        self.buttonBox_custom.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox_custom.setStandardButtons(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Reset)
        self.buttonBox_custom.setCenterButtons(False)
        self.buttonBox_custom.setObjectName("buttonBox_custom")

        self.buttonBox_custom.accepted.connect(self.customAdd)
        self.buttonBox_custom.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self.customReset)
        self.gridLayout_custom.addWidget(self.buttonBox_custom, 5, 2, 1, 1)


        
        self.widget_custom_rightInfo = QtWidgets.QListWidget(self.page_custom)
        self.widget_custom_rightInfo.setGeometry(QtCore.QRect(560, -1, 81, 482))
        self.widget_custom_rightInfo.setPalette(self.paletteWidget)
        font = QtGui.QFont()
        font.setFamily("STLiti")
        self.widget_custom_rightInfo.setFont(font)
        self.widget_custom_rightInfo.setObjectName("widget_custom_rightInfo")
        self.widget_custom_leftInfo = QtWidgets.QListWidget(self.page_custom)
        self.widget_custom_leftInfo.setGeometry(QtCore.QRect(-1, -1, 81, 482))
        self.widget_custom_leftInfo.setPalette(self.paletteWidget)
        font = QtGui.QFont()
        font.setFamily("STLiti")
        self.widget_custom_leftInfo.setFont(font)
        self.widget_custom_leftInfo.setObjectName("widget_custom_leftInfo")

        pushButton_custom_pageToMenu = QtWidgets.QPushButton(self.page_custom)
        pushButton_custom_pageToMenu.setGeometry(QtCore.QRect(8, 275, 64, 61))
        pushButton_custom_pageToMenu.setPalette(self.paletteWButton)
        font = QtGui.QFont()
        font.setFamily("STLiti")
        font.setPointSize(12)
        font.setWeight(QtGui.QFont.Medium)
        pushButton_custom_pageToMenu.setFont(font)
        pushButton_custom_pageToMenu.setObjectName("pushButton_custom_pageToMenu")
        pushButton_custom_pageToMenu.setText(_translate("B3GUI", "Menu"))
        pushButton_custom_pageToPrimary = QtWidgets.QPushButton(self.page_custom)
        pushButton_custom_pageToPrimary.setGeometry(QtCore.QRect(8, 350, 64, 61))
        pushButton_custom_pageToPrimary.setPalette(self.paletteWButton)
        font = QtGui.QFont()
        font.setFamily("STLiti")
        font.setPointSize(12)
        font.setWeight(QtGui.QFont.Medium)
        pushButton_custom_pageToPrimary.setFont(font)
        pushButton_custom_pageToPrimary.setObjectName("pushButton_custom_pageToPrimary")
        pushButton_custom_pageToPrimary.setText(_translate("B3GUI", "Home"))

        label_custom_imageB3 = QtWidgets.QLabel(self.page_custom)        
        label_custom_imageB3.setGeometry(QtCore.QRect(567, 407, 66, 66))
        label_custom_imageB3.setPixmap(image)
        label_custom_imageB3.setObjectName("label_custom_imageB3")
        
        self.widget_custom_leftInfo.raise_()
        self.frame_2.raise_()
        pushButton_custom_pageToMenu.raise_()
        pushButton_custom_pageToPrimary.raise_()
        self.widget_custom_rightInfo.raise_()
        label_custom_imageB3.raise_()

        pushButton_custom_pageToMenu.clicked.connect(self.toMenu)
        pushButton_custom_pageToPrimary.clicked.connect(self.toPrimary)

        self.stackedWidget.addWidget(self.page_custom)

        ##################### Config page #####################
        self.page_config = QtWidgets.QWidget()
        self.page_config.setObjectName("page_config")
        pushButton_config_toMain = QtWidgets.QPushButton(self.page_config)
        pushButton_config_toMain.setGeometry(QtCore.QRect(576, 24, 50, 55))
        pushButton_config_toMain.setPalette(self.paletteWButton)
        font = QtGui.QFont()
        font.setFamily("STLiti")
        font.setPointSize(12)
        font.setWeight(QtGui.QFont.Medium)
        pushButton_config_toMain.setFont(font)
        pushButton_config_toMain.setObjectName("pushButton_config_toMain")
        pushButton_config_toMain.setText(_translate("B3GUI", "Return"))


        frame_config = QtWidgets.QFrame(self.page_config)
        frame_config.setGeometry(QtCore.QRect(40, 15, 506, 453))
        frame_config.setStyleSheet("#MainFrame{border: 1px solid red;}")
        frame_config.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame_config.setFrameShadow(QtWidgets.QFrame.Plain)
        frame_config.setObjectName("frame_config")
        self.gridLayoutWidget_config = QtWidgets.QWidget(frame_config)
        self.gridLayoutWidget_config.setGeometry(QtCore.QRect(2, 2, 501, 449))
        self.gridLayoutWidget_config.setObjectName("gridLayoutWidget_config")

        self.configGenerate()
        
        #right panel
        self.widget_config_rightInfo = QtWidgets.QListWidget(self.page_config)
        self.widget_config_rightInfo.setGeometry(QtCore.QRect(560, -1, 81, 482))
        self.widget_config_rightInfo.setPalette(self.paletteWidget)
        font = QtGui.QFont()
        font.setFamily("STLiti")
        self.widget_config_rightInfo.setFont(font)
        self.widget_config_rightInfo.setObjectName("widget_config_rightInfo")

        label_config_imageB3 = QtWidgets.QLabel(self.page_config)        
        label_config_imageB3.setGeometry(QtCore.QRect(567, 407, 66, 66))
        label_config_imageB3.setPixmap(image)
        label_config_imageB3.setObjectName("label_config_imageB3")
        
        self.widget_config_rightInfo.raise_()
        label_config_imageB3.raise_()
        frame_config.raise_()
        pushButton_config_toMain.raise_()
        
        pushButton_config_toMain.clicked.connect(self.toPrimary)
        
        self.stackedWidget.addWidget(self.page_config)

        self.retranslateUi()
        self.stackedWidget.setCurrentIndex(0)
        #QtCore.QMetaObject.connectSlotsByName(self)

    def batteryDecay(self):
        self.progressBar_batteryCharge.setValue(self.progressBar_batteryCharge.value()-1)

    def menuGenerate(self):
        ###potential issues with memory due to most of these not being constructed with parents. unsure- large scale testing/research
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
                #print(ing)
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

                menuItem = None
                menuItem = QtWidgets.QVBoxLayout()
                menuItem.setObjectName(menuName + " Item")
                pushButton= QtWidgets.QPushButton()
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(pushButton.sizePolicy().hasHeightForWidth())
                pushButton.setSizePolicy(sizePolicy)
                pushButton.setMinimumSize(QtCore.QSize(213, 120))
                pushButton.setMaximumSize(QtCore.QSize(213, 120))
                pushButton.setPalette(self.paletteButton)
                pushButton.setObjectName(menuName + " pushButton")
                font = QtGui.QFont()
                font.setFamily("STLiti")
                font.setPointSize(15)
                pushButton.setFont(font)
                if len(menuName) > 14:
                    temp = menuName
                    menuName = textwrap.fill(temp, 14)
                pushButton.setText(_translate("B3GUI", menuName))
                pushButton.clicked.connect(self.sendOrder)
                menuItem.addWidget(pushButton)
                
                line_menuRecipe = QtWidgets.QFrame()
                line_menuRecipe.setFrameShape(QtWidgets.QFrame.HLine)
                line_menuRecipe.setFrameShadow(QtWidgets.QFrame.Sunken)
                line_menuRecipe.setPalette(self.paletteLine)
                line_menuRecipe.setObjectName(menuName + " line_menuRecipe")
                menuItem.addWidget(line_menuRecipe)

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
                    #tiny horizontal spacer for column seperation

                #if (menuCount%4 == 3):
                    #gridLayout_menu.itemAtPosition(0, 0).invalidate()
                    #i have no idea what this is??
    
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
            print("   ERROR: you have nothing configured")
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
            self.pushButton_menuRight.deleteLater()


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
            self.pushButton_menuLeft.deleteLater()
            
    def sendOrder(self):
        #if cupPresent:
        _translate = QtCore.QCoreApplication.translate
        sender = self.sender()
        orderName = sender.text()
        self.label_curOrder_Name.setText(_translate("B3GUI", ("  " + str(orderName))))
        #print(orderName)
        orderRaw = fetchSQL(cursor, 'recipes', 'recipe_name', '=', str(orderName))
        #print(orderRaw)
        order = None
        ingName = ""
        ingAmt = ""
                
        for i in orderRaw:
            pumpConfig = fetchSQL(cursor, 'config', 'ingredient_name', '=', str(i[3]))
            updateInfo = ("inventory = " + str(int(pumpConfig[0][3]) - int(i[4])))
            updateSQL(cursor, "config", updateInfo, "ingredient_name", "=", str(i[3]))
            
            temp = (ingName + "<p>" + str(i[3]) + "</p>")
            ingName = temp
            temp = (ingAmt + "<p>" + str(i[4]) + " mL" + "</p>")
            ingAmt = temp

            if order == None:
                temp = ("M" + str(pumpConfig[0][0]), i[4])
                order = temp
            else:
                temp = order, ("M" + str(pumpConfig[0][0]), i[4])
                order = temp
        if len(orderRaw) == 1:
            temp = order
            convOrder = (temp,)
            order = (str(convOrder).rstrip(",)") + "))")
            
        self.label_curOrder_IngName.setText(_translate("B3GUI", ingName))
        self.label_curOrder_IngAmount.setText(_translate("B3GUI", ingAmt))
        global bartOrder
        bartOrder = order
        print(order)
        print(bartOrder)
        self.startButler()
        self.configRefresh()
        print(self.page_menuWindow.isAncestorOf(self.stackedMenuWidget))
        
        self.toPrimary()
        #else:
            #print("Please place a cup in Alfred the Butler's tray.")

    def quickOrder(self):
        if bartOrder != "":
            self.startButler()
            pumpConfig = fetchSQL(cursor, 'config', 'ingredient_name', '=', str(i[3]))
            updateInfo = ("inventory = '" + str(int(pumpConfig[0][3]) - int(i[4])))
            updateSQL(cursor, "config", updateInfo, "ingredient_name", "=", str(i[3]))

            self.configRefresh()
            self.configAddConfirm.destroy()
            self.toPrimary()
        else:
            print("There has not been a previous order yet!")
    def customReset(self):
        for i in range(1, self.gridLayout_custom.rowCount() - 2):
            self.gridLayout_custom.itemAtPosition(i, 0).widget().clear()
            self.gridLayout_custom.itemAtPosition(i, 2).widget().clear()
            
    def customAdd(self):
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
        self.customAddConfirm.setWindowTitle(_translate("CustomAddConfirmWindow", "Looks delicious! Give it a name"))
        label_customAddConfirm.setText(_translate("CustomAddConfirmWindow", "Choose a name for you custom recipe."))
        dialog_customAddConfirm.accepted.connect(self.customConfirm)
        dialog_customAddConfirm.rejected.connect(self.customAddConfirm.destroy)
        self.layout_customAddConfirm.addWidget(dialog_customAddConfirm)
        
        self.customAddConfirm.setLayout(self.layout_customAddConfirm)

        self.customAddConfirm.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #self.customAddConfirm.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.customAddConfirm.show()

    def customConfirm(self):
        recipeName = self.layout_customAddConfirm.itemAt(1).widget().text()
        numIng = 0
        cursor.execute('SELECT id FROM ' + 'recipes' + ' ORDER BY ' +
                       'id' + ' DESC LIMIT 1')
        value = cursor.fetchall()
        for i in range(1, self.gridLayout_custom.rowCount() - 2):
            ingName = str(self.gridLayout_custom.itemAtPosition(i, 0).widget().text())
            ingAmnt = str(self.gridLayout_custom.itemAtPosition(i, 2).widget().text())
            values = None
            values = "\'" + recipeName + "\', \'" + ingName + "\', \'" + ingAmnt + "\'"
            if ingName != "" and ingAmnt != "" and recipeName != "":
                numIng += 1
                insertSQL(cursor, "recipes", "recipe_name, ingredient_name, ingredient_amount", values)
            ##currently works under the assumption there are no correct inputs. return to allow
            ##for user error if time permits
            '''else:
                print("ERROR: Recipe List Update: Invalid Entry.")'''

        if numIng != 0:
            values = None
            values = "\'" + recipeName + "\', " + str((value[0][0] + 1)) + ", " + str(numIng)
            insertSQL(cursor, "menu", "name, id_start, num_ingredient", values)
            self.menuRefresh()
        self.customReset()
        time.sleep(.8)
        self.toMenu()
        self.customAddConfirm.destroy()

    def configGenerate(self):
        _translate = QtCore.QCoreApplication.translate

        #def start
        gridLayout_defConfig = QtWidgets.QGridLayout()
        gridLayout_defConfig.setContentsMargins(0, 0, 0, 0)
        gridLayout_defConfig.setObjectName("gridLayout_defConfig")

        ##headers
        label_config_pumpHead = QtWidgets.QLabel()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(label_config_pumpHead.sizePolicy().hasHeightForWidth())
        label_config_pumpHead.setSizePolicy(sizePolicy)
        label_config_pumpHead.setMinimumSize(QtCore.QSize(40, 0))
        label_config_pumpHead.setAlignment(QtCore.Qt.AlignCenter)
        label_config_pumpHead.setObjectName("label_config_pumpHead")
        label_config_pumpHead.setText(_translate("B3GUI", "Pump ID"))
        gridLayout_defConfig.addWidget(label_config_pumpHead, 0, 0, 1, 1, QtCore.Qt.AlignRight)

        label_config_ingNameHead = QtWidgets.QLabel()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(label_config_ingNameHead.sizePolicy().hasHeightForWidth())
        label_config_ingNameHead.setSizePolicy(sizePolicy)
        label_config_ingNameHead.setMinimumSize(QtCore.QSize(0, 70))
        label_config_ingNameHead.setAlignment(QtCore.Qt.AlignCenter)
        label_config_ingNameHead.setObjectName("label_config_ingNameHead")
        label_config_ingNameHead.setText(_translate("B3GUI", "Ingredient"))
        gridLayout_defConfig.addWidget(label_config_ingNameHead, 0, 2, 1, 1)

        label_config_ingAmountHead = QtWidgets.QLabel()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(label_config_ingAmountHead.sizePolicy().hasHeightForWidth())
        label_config_ingAmountHead.setSizePolicy(sizePolicy)
        label_config_ingAmountHead.setMinimumSize(QtCore.QSize(0, 70))
        label_config_ingAmountHead.setAlignment(QtCore.Qt.AlignCenter)
        label_config_ingAmountHead.setObjectName("label_config_ingAmountHead")
        label_config_ingAmountHead.setText(_translate("B3GUI", "Amount\nRemaining"))
        gridLayout_defConfig.addWidget(label_config_ingAmountHead, 0, 4, 1, 1)
        
        label_config_ingUnitHead = QtWidgets.QLabel()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(label_config_ingUnitHead.sizePolicy().hasHeightForWidth())
        label_config_ingUnitHead.setSizePolicy(sizePolicy)
        label_config_ingUnitHead.setMinimumSize(QtCore.QSize(25, 70))
        label_config_ingUnitHead.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        label_config_ingUnitHead.setObjectName("label_config_ingUnitHead")
        label_config_ingUnitHead.setText(_translate("B3GUI", "Unit"))
        gridLayout_defConfig.addWidget(label_config_ingUnitHead, 0, 5, 1, 1)

        ##pumpid and line

        configRaw = fetchSQL(cursor, 'config', 'pump_id', '>', 0)

        for i in range(0, 3):
            
            lineEdit_config_pumpid = QtWidgets.QLineEdit()
            lineEdit_config_pumpid.setMaximumSize(QtCore.QSize(35, 16777215))
            lineEdit_config_pumpid.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:0, stop:0 rgba(136, 138, 133, 255), stop:1 rgba(255, 255, 255, 255));")
            lineEdit_config_pumpid.setObjectName("lineEdit_config_pumpid")
            
            line_configpump = QtWidgets.QFrame()
            line_configpump.setFrameShape(QtWidgets.QFrame.VLine)
            line_configpump.setFrameShadow(QtWidgets.QFrame.Sunken)
            line_configpump.setPalette(self.paletteLine)
            line_configpump.setObjectName("line_configpump") 
            
            lineEdit_config_ingName = QtWidgets.QLineEdit()
            lineEdit_config_ingName.setAutoFillBackground(False)
            lineEdit_config_ingName.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:0, stop:0 rgba(136, 138, 133, 255), stop:1 rgba(255, 255, 255, 255));")
            lineEdit_config_ingName.setObjectName("lineEdit_config_ingName")

            line_configing = QtWidgets.QFrame()
            line_configing.setFrameShape(QtWidgets.QFrame.VLine)
            line_configing.setFrameShadow(QtWidgets.QFrame.Sunken)
            line_configing.setPalette(self.paletteLine)
            line_configing.setObjectName("line_configing")
            
            lineEdit_config_ingAmount = QtWidgets.QLineEdit()
            lineEdit_config_ingAmount.setMaximumSize(QtCore.QSize(90, 16777215))
            lineEdit_config_ingAmount.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:0, stop:0 rgba(136, 138, 133, 255), stop:1 rgba(255, 255, 255, 255));")
            lineEdit_config_ingAmount.setObjectName("lineEdit_config_ingAmount")
            
            label_config_unit = QtWidgets.QLabel()
            label_config_unit.setObjectName("label_config_unit")
            label_config_unit.setText(_translate("B3GUI", "mL"))

            gridLayout_defConfig.addWidget(lineEdit_config_pumpid, (i+1), 0, 1, 1, QtCore.Qt.AlignRight)
            gridLayout_defConfig.addWidget(line_configpump, (i+1), 1, 1, 1)
            gridLayout_defConfig.addWidget(lineEdit_config_ingName, (i+1), 2, 1, 1)
            gridLayout_defConfig.addWidget(line_configing, (i+1), 3, 1, 1, QtCore.Qt.AlignHCenter)
            gridLayout_defConfig.addWidget(lineEdit_config_ingAmount, (i+1), 4, 1, 1)
            gridLayout_defConfig.addWidget(label_config_unit, (i+1), 5, 1, 1)

            lineEdit_config_pumpid.setText(_translate("B3GUI", str(configRaw[i][0])))
            lineEdit_config_pumpid.setReadOnly(True)
            
            if configRaw[i][2] != "" and configRaw[i][3] != "":
                lineEdit_config_ingName.setText(_translate("B3GUI", str(configRaw[i][2])))
                lineEdit_config_ingAmount.setText(_translate("B3GUI", str(configRaw[i][3])))
                
                lineEdit_config_ingName.setReadOnly(True)
                lineEdit_config_ingAmount.setReadOnly(True)
            if i == 2:
                spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                gridLayout_defConfig.addItem(spacerItem, i+2, 2, 1, 1)
                buttonBox_config = QtWidgets.QDialogButtonBox()
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(buttonBox_config.sizePolicy().hasHeightForWidth())
                buttonBox_config.setSizePolicy(sizePolicy)
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
                buttonBox_config.setPalette(palette)
                buttonBox_config.setLayoutDirection(QtCore.Qt.RightToLeft)
                buttonBox_config.setOrientation(QtCore.Qt.Vertical)
                buttonBox_config.setStandardButtons(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Reset)
                buttonBox_config.setCenterButtons(False)
                buttonBox_config.setObjectName("buttonBox_config")
                buttonBox_config.accepted.connect(self.configAdd)
                buttonBox_config.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self.configReset)
                gridLayout_defConfig.addWidget(buttonBox_config, i+3, 4, 1, 1)

        self.gridLayoutWidget_config.setLayout(gridLayout_defConfig)

    def configDeleteRow(self):
        #deletes designated row in config page
        #same as reset basically but for a specifc row
        #completely optional QoL task. ignore this if more pressing issues are at hand
        self.configRefresh()

    def configRefresh(self):
        _translate = QtCore.QCoreApplication.translate
        layout = self.gridLayoutWidget_config.layout()
        layout_progress = self.formLayoutWidget_progress.layout()
        configRaw = fetchSQL(cursor, 'config', 'pump_id', '>', 0)
        for i in range(0, 3):
            if configRaw[i][2] != "" and configRaw[i][3] != "":
                layout.itemAtPosition((i+1), 2).widget().setText(_translate("B3GUI", str(configRaw[i][2])))
                layout.itemAtPosition((i+1), 4).widget().setText(_translate("B3GUI", str(configRaw[i][3])))
                layout.itemAtPosition((i+1), 2).widget().setReadOnly(True)
                layout.itemAtPosition((i+1), 4).widget().setReadOnly(True)
                
                layout_progress.itemAt(2*i).widget().setText(_translate("B3GUI", str(configRaw[i][2])))
                layout_progress.itemAt((2*i) + 1).widget().setMaximum(configRaw[i][4])
                layout_progress.itemAt((2*i) + 1).widget().setValue(configRaw[i][3])
                layout_progress.itemAt((2*i) + 1).widget().show()
                
            else:
                layout.itemAtPosition((i+1), 2).widget().setText(_translate("B3GUI", ""))
                layout.itemAtPosition((i+1), 4).widget().setText(_translate("B3GUI", "")) 
                layout.itemAtPosition((i+1), 2).widget().setReadOnly(False)
                layout.itemAtPosition((i+1), 4).widget().setReadOnly(False)
                
                layout_progress.itemAt(2*i).widget().setText(_translate("B3GUI", ("Pump " + str(i+1))))
                layout_progress.itemAt((2*i) + 1).widget().setMaximum(100)
                layout_progress.itemAt((2*i) + 1).widget().setValue(0)
                layout_progress.itemAt((2*i) + 1).widget().hide()

        self.menuRefresh()
        
            
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
        self.configAddConfirm.setWindowTitle(_translate("ConfigAddConfirmWindow", " "))
        label_configAddConfirm.setText(_translate("ConfigAddConfirmWindow", "Are you sure you add this to the configuration?"))
        dialog_configAddConfirm.accepted.connect(self.configConfirm)
        dialog_configAddConfirm.rejected.connect(self.configAddConfirm.destroy)
        self.layout_configAddConfirm.addWidget(dialog_configAddConfirm)
        
        self.configAddConfirm.setLayout(self.layout_configAddConfirm)

        self.configAddConfirm.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #self.configAddConfirm.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.configAddConfirm.show()        

    def configConfirm(self):
        layout = self.gridLayoutWidget_config.layout()
        for i in range(1,4):
            ingName = str(layout.itemAtPosition(i, 2).widget().text())
            ingAmnt = str(layout.itemAtPosition(i, 4).widget().text())
            if (ingName != "" and ingAmnt != "" and (not(layout.itemAtPosition(i, 2).widget().isReadOnly()))):                
                updateInfo = ("ingredient_name = '" + ingName + "', inventory = "
                              + ingAmnt + ", start_inventory = " + ingAmnt)
                updateSQL(cursor, "config", updateInfo, "pump_id", "=", str(i))
        self.configRefresh()
        self.configAddConfirm.destroy()

        
    def configReset(self):
        for i in range(1,4):
            updateInfo = "ingredient_name = '', inventory = '', start_inventory = ''"
            updateSQL(cursor, "config", updateInfo, "pump_id", "=", str(i))
        self.configRefresh()
        
    def startButler(self):
        pubMQTT(client, STARTSIGNAL, "start")

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("B3GUI", "Form"))
        self.pushButton_config.setText(_translate("B3GUI", "Drink\n"
"Configuration"))
        self.pushButton_toMenu.setText(_translate("B3GUI", "Menu"))
        self.label_curOrder_IngAmount.setText(_translate("B3GUI", " "))
        self.pushButton_curOrder.setText(_translate("B3GUI", "Quick Order"))
        self.pushButton_quit.setText(_translate("B3GUI", "Quit"))
        self.label_curOrder.setText(_translate("B3GUI", "Current Order: "))
        self.pushButton_dock.setText(_translate("B3GUI", "Dock"))
        #self.pushButton_advTools.setText(_translate("B3GUI", "Adv. \n"
                                                    #"Tools"))
        self.label_batteryCharge.setText(_translate("B3GUI", "Battery Charge"))
        

    def menuRefresh(self):
        if (self.stackedMenuWidget.count() < 2):
            pass
        elif (self.stackedMenuWidget.currentIndex() == 0):
            self.pushButton_menuRight.deleteLater()
        elif((self.stackedMenuWidget.currentIndex() + 1) == self.stackedMenuWidget.count()):
            self.pushButton_menuLeft.deleteLater()
        else:
            self.pushButton_menuRight.deleteLater()
            self.pushButton_menuLeft.deleteLater()
        
        for i in range (0, self.stackedMenuWidget.count()):
            self.stackedMenuWidget.widget(i).deleteLater()

        self.stackedMenuWidget.deleteLater()

        self.stackedMenuWidget = self.menuGenerate()
        self.stackedMenuWidget.setGeometry(QtCore.QRect(94, 16, 451, 417))
        self.stackedMenuWidget.setObjectName("stackedMenuWidget")
        self.stackedMenuWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.stackedMenuWidget.show()

        if self.stackedMenuWidget.count() != 1:
            self.pushButton_menuRight = QtWidgets.QPushButton(self.page_menuWindow)
            self.pushButton_menuRight.setGeometry(QtCore.QRect(375, 440, 76, 33))
            self.pushButton_menuRight.setPalette(self.paletteButton)
            self.pushButton_menuRight.setObjectName("pushButton_menuRight")
            self.pushButton_menuRight.setText("------->")
            self.pushButton_menuRight.clicked.connect(self.menuRight)
            self.pushButton_menuRight.show()

    def toMenu(self):
        self.stackedWidget.setCurrentIndex(1)

    def toConfig(self):
        self.stackedWidget.setCurrentIndex(3)

    def toCustom(self):
        self.stackedWidget.setCurrentIndex(2)

    def toPrimary(self):
        self.retranslateUi()
        self.stackedWidget.setCurrentIndex(0)

    def dock(self):
        self.configRefresh()
        #self.startButler()
        pubMQTT(client, DOCK, "dock")
        
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
        self.exit.setWindowTitle(_translate("ExitWindow", "Quit?"))
        self.exitLabel.setText(_translate("ExitWindow", "Are you sure you want to quit?"))
        self.exitDialog.accepted.connect(self.killUi)
        self.exitDialog.rejected.connect(self.exit.destroy)

        self.exitLayout.addWidget(self.exitLabel, 0, 0)
        self.exitLayout.addWidget(self.exitDialog, 1, 0)
        self.exit.setLayout(self.exitLayout)

        self.exit.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #self.exit.setWindowFlags(QtCore.Qt.FramelessWindowHint)
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
    try:
        main()
    except Error as e:
        print(e)
