import sys
from PyQt6.QtWidgets import *
from overlay_animations import testAnimation
import mainWindow


app = QApplication(sys.argv)

window = mainWindow.MainWindow()
window.showFullScreen()


# Run the application
sys.exit(app.exec())
