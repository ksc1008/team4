import sys

from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import *
from overlay_animations import testAnimation
import mainWindow


app = QApplication(sys.argv)
window = mainWindow.MainWindow(app)
window.showFullScreen()

try:
    sys.exit(app.exec())
except SystemExit:
    window.animator.stop()
    window.close()


print('window closed')