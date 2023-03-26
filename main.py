import sys

from PyQt6.QtWidgets import QApplication

from loading_circle import Loading_Circle

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loading_circle = Loading_Circle()
    loading_circle.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        loading_circle.shortcut.stop()
        loading_circle.shortcut.terminate()
        loading_circle.close()
