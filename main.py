import sys, os
import asyncio
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calorie Counter")
        self.setGeometry(100, 100, 980, 720)
        self.createUserUI()
        self.show()
	
    def createUserUI(self):
    	button = QPushButton("Name", self)
    	button.clicked.connect(self.action)

    def action(self):
    	print('bota loh')

app = QApplication(sys.argv)

if __name__ == "__main__":
	window = MainWindow()
	window.show()
	app.exec()

