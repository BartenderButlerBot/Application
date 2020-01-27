#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 18:06:39 2020

@author: pi
"""

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QMainWindow, QAction

class MyPopup(QWidget):
    def __init__(self):
        QWidget.__init__(self)

    '''def paintEvent(self, e):
        dc = QPainter(self)
        dc.drawLine(0, 0, 100, 100)
        dc.drawLine(100, 0, 0, 100)'''

class MainWindow(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        self.cw = QWidget(self)
        self.setCentralWidget(self.cw)
        self.btn1 = QtWidgets.QPushButton("Click me", self.cw)
        self.btn1.setGeometry(QtCore.QRect(0, 0, 100, 30))
        self.btn1.clicked.connect(self.doit)
        self.w = None

    def doit(self):
        print ("Opening a new popup window...")
        '''self.w = MyPopup()
        self.w.setGeometry(QtCore.QRect(100, 100, 400, 200))
        self.w.show()'''

class App(QApplication):
    def __init__(self, *args):
        QApplication.__init__(self, *args)
        self.main = MainWindow()
        #self.connect(self, QtCore.SIGNAL("lastWindowClosed()"), self.byebye )
        self.main.show()

    '''def byebye( self ): 
        self.exit(0)'''

def main(args):
    global app
    app = App(args)
    app.exec_()

if __name__ == "__main__":
    main(sys.argv)