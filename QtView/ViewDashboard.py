import sys

from PySide2.QtGui import QIcon, QPalette, QPixmap
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QWidget, QGridLayout, QPushButton, QComboBox, \
    QVBoxLayout, QLCDNumber, QLabel, QDoubleSpinBox, QSlider
from RedoxFlowProject.QtView.NewWidget import BubbleWidget, Add, NotificationWidget

from RedoxFlowProject.QtView.PumpWidget import PumpWidget
from enum import Enum


class Notification(NotificationWidget):
    def __init__(self):
        super().__init__()
        self.size_text = 0.5
        self.color_text = "white"
        self.color = '#5ba1c2'
        self.text = "***Notifications***\n\n>Pump is ON\n>Pump is OFF\n>Speed Changed"


class AddWidget(Add):
    def __init__(self):
        super().__init__()

        self.clicked.connect(self.button_clicked)

    @staticmethod
    def button_clicked(s):
        print("Adding Widgets", s)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # setting the window title and dimensions
        self.setWindowTitle("Main Window")
        self.setGeometry(200, 200, 1000, 400)
        self.grid_layout = QGridLayout()

        v_layout = QtWidgets.QVBoxLayout()
        # self.pump_speed = BubbleWidget(text='Pump Speed')

        self.battery_level = BubbleWidget(text='Battery Level')
        self.temp = BubbleWidget(icon=r"../QtIcons/temperature.png", text='Temperature')
        self.liquid_level = BubbleWidget(text='Liquid Level')

        # v_layout.addWidget(self.pump_speed)
        v_layout.addWidget(self.battery_level)
        v_layout.addWidget(self.temp)
        v_layout.addWidget(self.liquid_level)

        # self.graphx1 = ToolBar()
        self.PumpWidget = PumpWidget()
        self.graphx3 = AddWidget()
        self.graphx4 = AddWidget()
        self.graphx5 = AddWidget()
        self.Notification = Notification()

        v_layout.addWidget(self.PumpWidget.PumpBubbleWidget)

        # print(self.StateWidget.pump_speed.value)

        print(self.grid_layout.horizontalSpacing())
        # self.grid_layout.setHorizontalSpacing(0)

        # self.grid_layout.addWidget(self.graphx1, 0, 0, 1, 4)

        self.grid_layout.addWidget(self.PumpWidget, 1, 0)
        self.grid_layout.addWidget(self.graphx3, 2, 0)
        self.grid_layout.addWidget(self.graphx4, 1, 1)
        self.grid_layout.addWidget(self.graphx5, 2, 1)

        self.grid_layout.addWidget(self.Notification, 2, 2)
        self.grid_layout.addLayout(v_layout, 1, 2)

        self.widget = QWidget()
        self.widget.setLayout(self.grid_layout)
        self.setCentralWidget(self.widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()

    # pal = QPalette()
    # pal.setColor(QPalette.Background, '#d1e3d3')
    # window.setAutoFillBackground(True)
    # window.setPalette(pal)
    window.show()
    app.exec_()
