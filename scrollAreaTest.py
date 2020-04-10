
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QVBoxLayout, QGroupBox, QLabel, QPushButton, QGridLayout
import sys
class Window(QWidget):
    def __init__(self, val):
        super().__init__()
        self.title = "PyQt5 Scroll Bar"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.gridLayout =QGridLayout()
        groupBox = QGroupBox("This Is Group Box")
        labelLis = []
        comboList = []
        for i in  range(val):
            l = QLabel("Label " + str(i))
            p = QPushButton("Click Me " + str(i))
            if i == 12:
                p.clicked.connect(self.deleteLayout)
            self.gridLayout.addWidget(l, i, 0, 1, 1)
            self.gridLayout.addWidget(p, i, 1, 1, 1)
        #self.gridLayout.insertRow(0, QLabel("Label 00"), QPushButton("Click Me 00"))
        self.gridLayout.itemAtPosition(0,0).widget().deleteLater()
        self.gridLayout.itemAtPosition(0,1).widget().deleteLater()
        #self.gridLayout.insertRow(10, QLabel("Label in 10"), QPushButton("Click Me in 10"))

        
        
        #gridLayout.addRow("test", fghj)

        
        groupBox.setLayout(self.gridLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(400)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        self.show()

    def deleteLayout(self):
        while self.gridLayout.count !=0:
            return nothing
        self.gridLayout.destroy()
        
App = QApplication(sys.argv)
window = Window(15)
sys.exit(App.exec())
