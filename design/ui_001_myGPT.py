# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '001_myGPTtRKBbf.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLCDNumber, QLabel, QMainWindow, QMenuBar,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(920, 820)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(900, 750))
        self.frame.setStyleSheet(u"background-color: rgb(255, 255, 255)")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(200, 720))
        self.frame_2.setMaximumSize(QSize(200, 16777215))
        self.frame_2.setAutoFillBackground(False)
        self.frame_2.setStyleSheet(u"background-color: rgb(0,0,0)")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(180, 100))
        self.frame_5.setStyleSheet(u"background-color: rgb(0, 0, 0)")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.btn_submit = QPushButton(self.frame_5)
        self.btn_submit.setObjectName(u"btn_submit")
        self.btn_submit.setMinimumSize(QSize(170, 34))
        self.btn_submit.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(14)
        self.btn_submit.setFont(font)
        self.btn_submit.setFocusPolicy(Qt.StrongFocus)
        self.btn_submit.setStyleSheet(u"QPushButton {\n"
"color: rgb(255, 255, 255);\n"
"border-style: outset;\n"
"border-color: rgb(0, 0, 0);\n"
"border-width: 2px;\n"
"border-radius:5px;\n"
"padding: 1px;\n"
"background-color: rgb(0, 0, 0);\n"
"}\n"
"QPushButton:hover {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(50, 50, 50);\n"
"}")

        self.verticalLayout_2.addWidget(self.btn_submit)

        self.btn_clear = QPushButton(self.frame_5)
        self.btn_clear.setObjectName(u"btn_clear")
        self.btn_clear.setMinimumSize(QSize(170, 34))
        self.btn_clear.setFont(font)
        self.btn_clear.setFocusPolicy(Qt.StrongFocus)
        self.btn_clear.setStyleSheet(u"QPushButton {\n"
"color: rgb(255, 255, 255);\n"
"border-style: outset;\n"
"border-color: rgb(0, 0, 0);\n"
"border-width: 2px;\n"
"border-radius:5px;\n"
"padding: 1px;\n"
"background-color: rgb(0, 0, 0);\n"
"}\n"
"QPushButton:hover {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(50, 50, 50);\n"
"}")

        self.verticalLayout_2.addWidget(self.btn_clear)

        self.btn_exit = QPushButton(self.frame_5)
        self.btn_exit.setObjectName(u"btn_exit")
        self.btn_exit.setMinimumSize(QSize(170, 34))
        self.btn_exit.setFont(font)
        self.btn_exit.setFocusPolicy(Qt.StrongFocus)
        self.btn_exit.setStyleSheet(u"QPushButton {\n"
"color: rgb(255, 255, 255);\n"
"border-style: outset;\n"
"border-color: rgb(0, 0, 0);\n"
"border-width: 2px;\n"
"border-radius:5px;\n"
"padding: 1px;\n"
"background-color: rgb(0, 0, 0);\n"
"}\n"
"QPushButton:hover {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(50, 50, 50);\n"
"}")

        self.verticalLayout_2.addWidget(self.btn_exit)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.verticalLayout.addWidget(self.frame_5)

        self.line = QFrame(self.frame_2)
        self.line.setObjectName(u"line")
        self.line.setMinimumSize(QSize(170, 0))
        self.line.setStyleSheet(u"background-color: rgb(50, 50, 50)")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(180, 80))
        self.frame_4.setMaximumSize(QSize(180, 80))
        self.frame_4.setStyleSheet(u"background-color: rgb(0,0,0)")
        self.frame_4.setFrameShape(QFrame.WinPanel)
        self.frame_4.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setSpacing(1)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(5, 5, 4, 4)
        self.lcd_clock = QLCDNumber(self.frame_4)
        self.lcd_clock.setObjectName(u"lcd_clock")
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.lcd_clock.setFont(font1)
        self.lcd_clock.setStyleSheet(u"QLCDNumber {\n"
"color: rgb(255, 255, 255);\n"
"background-image: linear-gradient(180deg, #FFE32C 96%, #52ACFF 97%, #ffffff 99%, #ffffff 100%);\n"
"\n"
"}\n"
"QLCDNumber:hover {\n"
"color: rgb(255, 255, 0);\n"
"font: 700 13pt \"\ub9d1\uc740 \uace0\ub515\";\n"
"background-color:rgb(50, 50, 50)\n"
"}")
        self.lcd_clock.setDigitCount(8)
        self.lcd_clock.setProperty("value", 123456.000000000000000)

        self.horizontalLayout_3.addWidget(self.lcd_clock)


        self.verticalLayout.addWidget(self.frame_4)


        self.horizontalLayout.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 650))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_status = QLabel(self.frame_3)
        self.label_status.setObjectName(u"label_status")
        self.label_status.setMinimumSize(QSize(0, 30))
        self.label_status.setFont(font)
        self.label_status.setMouseTracking(True)
        self.label_status.setStyleSheet(u"border-style: outset;\n"
"border-color: rgb(0,0,0);\n"
"border-width: 2px;\n"
"border-radius: 5px;")
        self.label_status.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_status)

        self.text_answer = QTextEdit(self.frame_3)
        self.text_answer.setObjectName(u"text_answer")
        self.text_answer.setMinimumSize(QSize(0, 280))
        font2 = QFont()
        font2.setPointSize(12)
        self.text_answer.setFont(font2)

        self.verticalLayout_3.addWidget(self.text_answer)

        self.text_prompt = QPlainTextEdit(self.frame_3)
        self.text_prompt.setObjectName(u"text_prompt")
        self.text_prompt.setMaximumSize(QSize(16777215, 90))
        self.text_prompt.setFont(font2)

        self.verticalLayout_3.addWidget(self.text_prompt)


        self.horizontalLayout.addWidget(self.frame_3)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 920, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_submit.setText(QCoreApplication.translate("MainWindow", u"Submit Question", None))
        self.btn_clear.setText(QCoreApplication.translate("MainWindow", u"Clear Question", None))
        self.btn_exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.label_status.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">status</span></p></body></html>", None))
        self.text_answer.setMarkdown("")
        self.text_answer.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.text_answer.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Here is Answer  ", None))
        self.text_prompt.setPlainText("")
        self.text_prompt.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Question here", None))
    # retranslateUi

