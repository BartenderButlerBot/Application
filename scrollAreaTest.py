
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QVBoxLayout, QGroupBox, QLabel, QPushButton, QFormLayout
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
        formLayout =QFormLayout()
        groupBox = QGroupBox("This Is Group Box")
        labelLis = []
        comboList = []
        for i in  range(val):
            labelLis.append(QLabel("Label " + str(i)))
            comboList.append(QPushButton("Click Me " + str(i)))
            formLayout.addRow(labelLis[i], comboList[i])

        formLayout.insertRow(0, QLabel("Label 01"), QPushButton("Click Me 01"))
        formLayout.itemAt(21).widget().deleteLater()
        
        #formLayout.addRow("test", fghj)

        
        groupBox.setLayout(formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(400)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        self.show()
App = QApplication(sys.argv)
window = Window(10)
sys.exit(App.exec())
