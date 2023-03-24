import sys
import PyQt6.QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import QtCore
from PyQt6 import QtGui

class CustomWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.mx = 400
        self.my = 400

    def paintEvent(self, event=None):
        painter = QPainter(self)
        self.mx = self.mx + 0.1

        painter.setOpacity(0.2)
        painter.setBrush(PyQt6.QtGui.QColorConstants.White)
        painter.setPen(QPen(PyQt6.QtGui.QColorConstants.White))
        painter.drawRect(self.rect())
        painter.setOpacity(0.8)
        painter.drawEllipse(self.mx,self.my,300,300)


app = QApplication(sys.argv)

# Create the main window
window = CustomWindow()

window.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput)
window.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground, True)
window.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

# Create the button
pushButton = QPushButton(window)
pushButton.setGeometry(QRect(240, 190, 90, 31))
pushButton.setText("Finished")

# Center the button
qr = pushButton.frameGeometry()
cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
qr.moveCenter(cp)
pushButton.move(qr.topLeft())

# Run the application
window.showFullScreen()
sys.exit(app.exec())
