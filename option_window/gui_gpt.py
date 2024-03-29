# Form implementation generated from reading ui file 'gui_gpt.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from option_window.gui_gpt_api import Api_MainWindow
from option_window.gui_gpt_model import Model_Dialog
from option_window.gui_gpt_keyboard import Keyboard_MainWindow
from option_window.gui_gpt_hyperparameter import Parameter_MainWindow

import sys


class Option_MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.initiateSignals()
        self.show()

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(480, 527)
        self.setMinimumSize(QtCore.QSize(480, 527))
        self.setMaximumSize(QtCore.QSize(480, 527))
        self.button1 = QtWidgets.QPushButton(self)
        self.button1.setGeometry(QtCore.QRect(120, 50, 260, 80))
        self.button1.setObjectName("button1")
        self.button2 = QtWidgets.QPushButton(self)
        self.button2.setGeometry(QtCore.QRect(120, 160, 260, 80))
        self.button2.setObjectName("button2")
        self.button3 = QtWidgets.QPushButton(self)
        self.button3.setGeometry(QtCore.QRect(120, 280, 260, 80))
        self.button3.setObjectName("button3")
        self.button4 = QtWidgets.QPushButton(self)
        self.button4.setGeometry(QtCore.QRect(120, 400, 260, 80))
        self.button4.setObjectName("button4")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "옵션"))
        self.button1.setText(_translate("Form", "모델 설정"))
        self.button2.setText(_translate("Form", "API 입력 및 파일 경로 설정"))
        self.button3.setText(_translate("Form", "단축키 설정"))
        self.button4.setText(_translate("Form", "ChatGPT 변수 설정"))

    def initiateSignals(self):
        self.button1.clicked.connect(self.model_clicked)
        self.button2.clicked.connect(self.api_clicked)
        self.button3.clicked.connect(self.keyboard_clicked)
        self.button4.clicked.connect(self.parameter_clicked)

    def model_clicked(self):
        self.model = Model_Dialog()
        self.show()

    def api_clicked(self):
        self.api = Api_MainWindow()
        self.show()

    def keyboard_clicked(self):
        self.key = Keyboard_MainWindow()
        self.show()

    def parameter_clicked(self):
        self.para = Parameter_MainWindow()
        self.show()


