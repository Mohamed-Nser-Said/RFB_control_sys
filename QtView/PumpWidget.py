import sys

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QApplication, QDoubleSpinBox, QGridLayout, \
    QMainWindow, QWidget, QPushButton, QHBoxLayout, QSlider, QLabel, QSizePolicy
from QtController.controllerPump import PumpControl
from QtView.NewWidget import BubbleWidget
import time


class SettingsQPushButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Preferred,
        )
        self.setIcon(QIcon(r"../QtIcons/settings.png"))
        self.setIconSize(QSize(self.size() / 10))

    def sizeHint(self):
        return QtCore.QSize(70, 70)


class PowerQPushButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Preferred,
        )
        self.setIconSize(QSize(self.size() / 10))
        self.power_button_state = False
        self.setIcon(QIcon(r"../QtIcons/on.png"))
        self.setCheckable(True)
        self.clicked.connect(self.power_button_clicked)
        self.setChecked(self.power_button_state)

    def sizeHint(self):
        return QtCore.QSize(70, 70)

    def power_button_clicked(self, checked):
        self.btn_state = checked
        if self.btn_state == True:
            self.setIcon(QIcon(r"../QtIcons/off.png"))
            self.parent().pump.start()
            self.parent().InformationQLabel.setText(str(self.parent().pump.modbus))

        if self.btn_state == False:
            self.setIcon(QIcon(r"../QtIcons/on.png"))
            self.parent().pump.stop()
            self.parent().InformationQLabel.setText(str(self.parent().pump.modbus))


class DirectionQPushButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Preferred,
        )
        self.setIconSize(QSize(self.size() / 12))
        self.direction_button_state = False
        self.setIcon(QIcon(r"../QtIcons/forward.png"))
        self.setCheckable(True)
        self.clicked.connect(self.direction_button_clicked)
        self.setChecked(self.direction_button_state)

    def sizeHint(self):
        return QtCore.QSize(70, 70)

    def direction_button_clicked(self, checked):
        self.btn_state = checked
        if self.btn_state:
            self.setIcon(QIcon(r"../QtIcons/backward.png"))
            self.parent().pump.flow_direction("ccw")
            self.parent().InformationQLabel.setText(str(self.parent().pump.modbus))

        if not self.btn_state:
            self.setIcon(QIcon(r"../QtIcons/forward.png"))
            self.parent().pump.flow_direction("cw")
            self.parent().InformationQLabel.setText(str(self.parent().pump.modbus))


class CloseQPushButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.clicked.connect(self.mini_button_clicked)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed,
        )
        #self.setIconSize(QSize(self.size() /22))
        self.setIcon(QIcon(r"../QtIcons/close.png"))

    def sizeHint(self):
        return QtCore.QSize(25, 25)

    def mini_button_clicked(self):
        if self.parent().isVisible():
            self.parent().pump.stop()
            self.parent().close()
            self.parent().PumpBubbleWidget.close()


class InfoQPushButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.clicked.connect(self.button_clicked)
        self.setIcon(QIcon(r"../QtIcons/help.png"))
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed,
        )
        # self.setIconSize(QSize(self.size() / 8))

    def sizeHint(self):
        return QtCore.QSize(25, 25)

    def button_clicked(self):
        print("clicked")


class ExternalQPushButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.clicked.connect(self.button_clicked)
        self.setIcon(QIcon(r"../QtIcons/external.png"))
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed,
        )
        # self.setIconSize(QSize(self.size() / 8))

    def sizeHint(self):
        return QtCore.QSize(25, 25)

    def button_clicked(self, checked):
        print("clicked")
        if PumpMainWindow.isVisible():
            PumpMainWindow.close()
            time.sleep(2)
            wi = PumpWidget()
            wi.show()

            print("the operation is done")


class SpeedQSlider(QSlider):
    def __init__(self):
        super().__init__(Qt.Horizontal)
        self.setMaximum(600)
        self.setMinimum(0)
        self.setSingleStep(2)
        self.valueChanged.connect(self.value_changed)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Preferred,
        )

    def sizeHint(self):
        return QtCore.QSize(250, 70)

    def value_changed(self, i):
        self.parent().SpeedQDoubleSpinBox.setValue(i)


class SpeedQDoubleSpinBox(QDoubleSpinBox):
    def __init__(self):
        super().__init__()
        self.setMinimum(0)
        self.setMaximum(600)
        self.setPrefix("speed in rpm : ")
        self.setSingleStep(0.5)  # Or e.g. 0.5 for QDoubleSpinBox
        self.valueChanged.connect(self.value_changed)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Fixed,
        )

    def sizeHint(self):
        return QtCore.QSize(100, 50)

    def value_changed(self, i):
        self.parent().pump.change_speed(new_speed=i)
        self.parent().InformationQLabel.setText(str(self.parent().pump.modbus))
        self.parent().SpeedQSlider.setValue(i)
        self.parent().PumpBubbleWidget.value = i
        self.parent().PumpBubbleWidget.color_value = int(i * 10 // 600)


class InformationQLabel(QLabel):

    def __init__(self):
        super().__init__()
        self.text = "no text"
        self.setText(self.text)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Preferred,
        )
    def sizeHint(self):
        return QtCore.QSize(400, 50)


class PumpWidget(QWidget):

    def __init__(self, color='#ced9cf'):
        super().__init__()
        self.color = QtGui.QColor(color)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )

        # making an instance of the pump control class and BubbleWidget
        self.pump = PumpControl()
        self.PumpBubbleWidget = BubbleWidget(text='Pump Speed', text_unit="rpm")

        # instance of te predefined buttons classes
        self.power_button = PowerQPushButton()
        self.direction_button = DirectionQPushButton()
        self.AutoQPushButton = SettingsQPushButton()

        self.MiniQPushButton = CloseQPushButton()
        self.ExternalQPushButton = ExternalQPushButton()
        self.InfoQPushButton = InfoQPushButton()

        self.SpeedQDoubleSpinBox = SpeedQDoubleSpinBox()
        self.SpeedQSlider = SpeedQSlider()

        self.InformationQLabel = InformationQLabel()

        # connecting the SpeedQDoubleSpinBox and SpeedQSlider to the PumpBubbleWidget
        self.SpeedQDoubleSpinBox.valueChanged.connect(self.PumpBubbleWidget._trigger_refresh)
        self.SpeedQSlider.valueChanged.connect(self.PumpBubbleWidget._trigger_refresh)

        # layout setting
        h_layout1 = QHBoxLayout()
        h_layout1.addWidget(self.power_button)
        h_layout1.addWidget(self.direction_button)
        h_layout1.addWidget(self.AutoQPushButton)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.MiniQPushButton)
        h_layout.addWidget(self.ExternalQPushButton)
        h_layout.addWidget(self.InfoQPushButton)

        g_layout = QGridLayout()
        g_layout.addLayout(h_layout1, 0, 0, 1, 2)
        g_layout.addWidget(self.SpeedQDoubleSpinBox, 2, 0)
        g_layout.addWidget(self.SpeedQSlider, 1, 0)
        g_layout.addWidget(self.InformationQLabel, 3, 0)
        g_layout.addLayout(h_layout, 4, 1)

        self.setLayout(g_layout)

    def sizeHint(self):
        return QtCore.QSize(400, 250)

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        width, height = painter.device().width(), painter.device().height()
        rect = QtCore.QRect(0, 0, width, height)

        # QBrush to fill color
        brush = QtGui.QBrush()
        brush.setColor(self.color)
        brush.setStyle(Qt.SolidPattern)

        # QPainterPath to draw rectangle oth round shape
        path = QtGui.QPainterPath()
        path.addRoundedRect(rect, 5, 5)
        painter.fillPath(path, brush)

        painter.end()


class PumpMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # setting the window title and dimensions
        self.setWindowTitle("Pump Control")
        self.setWindowIcon(QIcon(r""))
        self.setGeometry(200, 200, 450, 225)

        self.PumpWidget = PumpWidget()
        self.setCentralWidget(self.PumpWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    PumpMainWindow = PumpWidget()

    # pal = QPalette()
    # pal.setColor(QPalette.Background, '#d1e3d3')
    # window.setAutoFillBackground(True)
    # window.setPalette(pal)
    PumpMainWindow.show()
    app.exec_()
