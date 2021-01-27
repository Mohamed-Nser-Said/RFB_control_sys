import sys
from PySide2.QtWidgets import QApplication
from dashboard import MainWindow
from pumpgui import PumpMainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    # window = MainWindow()

    window = PumpMainWindow() # to launch the pump widget only
    window.show()
    app.exec_()

