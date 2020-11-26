import sys

from PyQt5.QtCore import QSize
from PySide2.QtGui import QIcon, QPalette, QPixmap
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QWidget, QGridLayout, QPushButton, QComboBox, \
    QVBoxLayout, QLCDNumber, QLabel, QDoubleSpinBox, QSlider
from QtView.NewWidget import BubbleWidget, Add, NotificationWidget

from QtView.PumpWidget import PumpWidget
from enum import Enum


class Notification(NotificationWidget):
    def __init__(self):
        super().__init__()
        self.size_text = 0.5
        self.color_text = "white"
        self.color = '#5ba1c2'
        self.text = "***Notifications***\n\n>Pump is ON\n>Pump is OFF\n>Speed Changed"


'''class StateWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout()

        self.temp = BubbleWidget(icon=r"../QtIcons/temperature.png", text='Temperature')
        layout.addWidget(self.temp)

        self.liquid_level = BubbleWidget(text='Liquid Level')
        layout.addWidget(self.liquid_level)

        self.pump_speed = BubbleWidget(text='Pump Speed')
        layout.addWidget(self.pump_speed)

        self.battery_level = BubbleWidget(text='Battery Level')
        layout.addWidget(self.battery_level)

        # self._dial.valueChanged.connect(self.pump_speed._trigger_refresh)

        """self._dial.valueChanged.connect(self.temp._trigger_refresh)
        self._dial.valueChanged.connect(self.liquid_level._trigger_refresh)
        
        self._dial.valueChanged.connect(self.battery_level._trigger_refresh)
        layout.addWidget(self._dial)"""
        self.setLayout(layout)'''


class AddWidget(Add):
    def __init__(self):
        super().__init__()

        self.clicked.connect(self.button_clicked)

    def button_clicked(self, s):
        print("Adding Widgets", s)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # setting the window title and dimensions
        self.setWindowTitle("Main Window")
        self.setGeometry(200, 200, 1200, 550)
        self.grid_layout = QGridLayout()

        v_layout = QtWidgets.QVBoxLayout()
        #self.pump_speed = BubbleWidget(text='Pump Speed')

        self.battery_level = BubbleWidget(text='Battery Level')
        self.temp = BubbleWidget(icon=r"../QtIcons/temperature.png", text='Temperature')
        self.liquid_level = BubbleWidget(text='Liquid Level')


        #v_layout.addWidget(self.pump_speed)
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
