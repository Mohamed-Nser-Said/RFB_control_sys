from PySide2.QtCore import QSize, Qt, QThreadPool, QRunnable, Slot, QRect, QTimer
from PySide2.QtGui import QIcon, QKeySequence, QColor, QPainter, QBrush, QPainterPath
from PySide2.QtWidgets import QApplication, QDoubleSpinBox, QGridLayout, QSizePolicy
from PySide2.QtWidgets import QMainWindow, QWidget, QPushButton, QHBoxLayout, QSlider, QLabel, QVBoxLayout
from PySide2.QtWidgets import QTabWidget, QComboBox, QLineEdit, QSpinBox, QMenu, QAction

from pumpAPI import PumpConnectionManger, find_my_pump, step_increase
from helper import ErrorMassage, PortManger, ModbusBuilder, CRCGenerator, Pump, IS
from helper import MasterSend, Type, MasterValues, SecondValues, icon
from newwidget import BubbleWidget
import pyqtgraph as pg
import sys
import time
import serial


class AbstractQPushButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setIconSize(QSize(self.size() / 12))
        self.clicked.connect(self.button_clicked)

    def sizeHint(self):
        return QSize(70, 70)

    def button_clicked(self):
        pass


class AbstractBackGround(QWidget):
    def __init__(self, color='#ced9cf'):
        super().__init__()
        self.color = QColor(color)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def sizeHint(self):
        return QSize(400, 250)

    def paintEvent(self, e):
        painter = QPainter(self)
        width, height = painter.device().width(), painter.device().height()
        rect = QRect(0, 0, width, height)

        # QBrush to fill color
        brush = QBrush()
        brush.setColor(self.color)
        brush.setStyle(Qt.SolidPattern)

        # QPainterPath to draw rectangle oth round shape
        path = QPainterPath()
        path.addRoundedRect(rect, 5, 5)
        painter.fillPath(path, brush)

        painter.end()


master_send = MasterSend()
typ = Type()
master_state = MasterValues()
second_state = SecondValues()


class SpeedMonitor(AbstractBackGround):
    def __init__(self, color='#000000'):
        super().__init__()
        self.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding)
        self.color = QColor(color)
        self.close = CloseQPushButton()
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground("000000")
        self.graphWidget.showGrid(x=True, y=True)
        pen1 = pg.mkPen(color="#ff0000", width=3)
        pen2 = pg.mkPen(color="#307cff", width=3)

        self.time = [0, 0]
        self.speed_master = [0, 0]
        self.speed_second = [0, 0]

        self.data_line1 = self.graphWidget.plot(self.time, self.speed_master, pen=pen2)

        self.timer = QTimer()
        self.timer = QTimer()
        self.timer.setInterval(60)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        if PortManger().get_number_of_pump_connected > 1:
            self.data_line = self.graphWidget.plot(self.time, self.speed_second, pen=pen1)
        self.timer2 = QTimer()
        self.timer2 = QTimer()
        self.timer2.setInterval(65)
        self.timer2.timeout.connect(self.update_plot_data2)
        self.timer2.start()
        layout = QGridLayout()
        layout.addWidget(self.close, 0, 2)
        layout.addWidget(self.graphWidget, 0, 0, 2, 2)
        self.setLayout(layout)

    def update_plot_data(self):
        if PortManger().get_number_of_pump_connected > 0:
            self.time.append(self.time[-1] + 1)
            self.speed_master.append(master_state.speed_list[-1])
            self.speed_second.append(second_state.speed_list[-1])

            self.data_line.setData(self.time, self.speed_master)
            self.data_line1.setData(self.time, self.speed_second)

    def update_plot_data2(self):
        if PortManger().get_number_of_pump_connected > 0:
            self.time = self.time[1:]
            self.speed_master = self.speed_master[1:]
            self.speed_second = self.speed_second[1:]

            self.data_line.setData(self.time, self.speed_master)
            self.data_line1.setData(self.time, self.speed_second)

    def sizeHint(self):
        return QSize(500, 300)


class MasterPumpTab(QTabWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.port_QLabel = QLabel('Port Auto Detection')
        self.port_QComboBox = QComboBox()
        self.port_QComboBox.addItems(["Enabled", "Disabled"])
        self.port_QComboBox.setDisabled(True)
        layout.addWidget(self.port_QLabel, 0, 0)
        layout.addWidget(self.port_QComboBox, 0, 1)

        self.select_port_QLabel = QLabel('Select Port')
        self.select_port_QComboBox = QComboBox()
        self.select_port_QComboBox.addItems(PortManger().get_ports_list)
        self.select_port_QComboBox.setDisabled(True)
        layout.addWidget(self.select_port_QLabel, 1, 0)
        layout.addWidget(self.select_port_QComboBox, 1, 1)

        if PortManger().get_master_pump_port is not None:
            self.select_port_QComboBox.setCurrentText(PortManger().get_master_pump_port_name_raw)

        self.test_btn = QPushButton("Find me !!")
        self.test_btn.clicked.connect(self.find_me)
        layout.addWidget(self.test_btn, 2, 1)
        layout.setContentsMargins(20, 0, 20, 300)

        self.setLayout(layout)

    @staticmethod
    def find_me():
        if PortManger().get_master_pump_port is not None:
            find_my_pump(Pump.MASTER)


class SecondPumpTab(QTabWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.second_pump_QLabel = QLabel('Second Pump')
        self.second_pump_QComboBox = QComboBox()
        self.second_pump_QComboBox.addItems(["Disabled", "Enabled"])
        self.second_pump_QComboBox.currentTextChanged.connect(self.set_disabled_)
        layout.addWidget(self.second_pump_QLabel, 0, 0)
        layout.addWidget(self.second_pump_QComboBox, 0, 1)

        self.speed_QLabel = QLabel('Speed')
        self.speed_QComboBox = QComboBox()
        self.speed_QComboBox.addItems(["Follow Master Pump", "Custom"])
        self.speed_QComboBox.setDisabled(True)
        layout.addWidget(self.speed_QLabel, 1, 0)
        layout.addWidget(self.speed_QComboBox, 1, 1)

        self.start_stop_QLabel = QLabel('Start/ Stop')
        self.start_stop_QComboBox = QComboBox()
        self.start_stop_QComboBox.addItems(["Follow Master Pump", "Custom"])
        self.start_stop_QComboBox.setDisabled(True)
        layout.addWidget(self.start_stop_QLabel, 2, 0)
        layout.addWidget(self.start_stop_QComboBox, 2, 1)

        self.direction_QLabel = QLabel('Direction')
        self.direction_QComboBox = QComboBox()
        self.direction_QComboBox.addItems(["Follow Master Pump", "Custom"])
        self.direction_QComboBox.setDisabled(True)
        layout.addWidget(self.direction_QLabel, 3, 0)
        layout.addWidget(self.direction_QComboBox, 3, 1)

        self.apply = QPushButton("Apply")
        self.apply.setDisabled(True)
        self.apply.clicked.connect(self.apply_setting)
        layout.addWidget(self.apply, 4, 1)

        self.test_btn = QPushButton("Find me !!")
        self.test_btn.clicked.connect(self.find_me)
        layout.addWidget(self.test_btn, 5, 1)

        layout.setContentsMargins(20, 0, 20, 150)
        self.setLayout(layout)

    @staticmethod
    def find_me():
        if PortManger().get_second_pump_port is not None:
            find_my_pump(Pump.SECOND)

    def set_disabled_(self):
        n = PortManger().get_number_of_pump_connected
        s = self.second_pump_QComboBox.currentText()
        if s == "Enabled" and n == 1:
            ErrorMassage("Error", f"Only {n} Pump is connected, please check the connection of the "
                                  "other pump")
            self.second_pump_QComboBox.setCurrentText("Disabled")
        elif s == "Enabled" and n == 2:
            self.apply.setDisabled(False)
            self.speed_QComboBox.setDisabled(False)
            self.direction_QComboBox.setDisabled(False)
            self.start_stop_QComboBox.setDisabled(False)

        elif s == "Disabled":
            self.apply.setDisabled(True)
            self.speed_QComboBox.setDisabled(True)
            self.direction_QComboBox.setDisabled(True)
            self.start_stop_QComboBox.setDisabled(True)
            self.apply_setting()

    def apply_setting(self):

        s = self.second_pump_QComboBox.currentText()
        sp = self.speed_QComboBox.currentText()
        st = self.start_stop_QComboBox.currentText()
        d = self.direction_QComboBox.currentText()

        if s == "Enabled":
            if sp == "Follow Master Pump":
                master_send.speed = Pump.BOTH
                typ.speed = IS.DUAL_CLONE
            elif sp == "Custom":
                master_send.speed = Pump.MASTER
                typ.speed = IS.DUAL_CUSTOM

            if d == "Follow Master Pump":
                master_send.direction = Pump.BOTH
                typ.direction = IS.DUAL_CLONE
            elif d == "Custom":
                master_send.direction = Pump.MASTER
                typ.direction = IS.DUAL_CUSTOM
            if st == "Follow Master Pump":
                master_send.start_stop = Pump.BOTH
                typ.start_stop = IS.DUAL_CLONE
            elif st == "Custom":
                master_send.start_stop = Pump.MASTER
                typ.start_stop = IS.DUAL_CUSTOM

        elif s == "Disabled":
            master_send.speed = Pump.MASTER
            master_send.direction = Pump.MASTER
            master_send.start_stop = Pump.MASTER
            typ.speed = IS.UNI
            typ.start_stop = IS.UNI
            typ.direction = IS.UNI

        window.update_my_window()


class ModbusSenderTab(QTabWidget):
    def __init__(self):
        super().__init__()
        self.modbus = serial.Serial()
        layout = QGridLayout()
        self.Select_Port_QLabel = QLabel('Select Port')
        self.Select_Port_QComboBox = QComboBox()
        self.Select_Port_QComboBox.activated.connect(self.update_port_selection)
        self.Select_Port_QComboBox.addItems(PortManger().get_ports_list)
        self.update_port_selection()
        if PortManger().get_master_pump_port is not None:
            self.Select_Port_QComboBox.setCurrentText(PortManger().get_master_pump_port_name_raw)

        layout.addWidget(self.Select_Port_QLabel, 0, 0)
        layout.addWidget(self.Select_Port_QComboBox, 0, 1)

        self.baud_rate_QLabel = QLabel('Baudrate')
        self.baud_rate_QComboBox = QComboBox()
        self.baud_rate_QComboBox.addItems(['1800', '2400', '4800', '9600', '19200'])
        self.baud_rate_QComboBox.setCurrentText('9600')
        layout.addWidget(self.baud_rate_QLabel, 1, 0)
        layout.addWidget(self.baud_rate_QComboBox, 1, 1)

        self.timeout_QLabel = QLabel('Timeout')
        self.timeout_QSpinBox = QDoubleSpinBox()
        self.timeout_QSpinBox.setSingleStep(0.1)
        self.timeout_QSpinBox.setValue(1.0)
        layout.addWidget(self.timeout_QLabel, 2, 0)
        layout.addWidget(self.timeout_QSpinBox, 2, 1)

        self.byte_size_QLabel = QLabel('Byte Size')
        self.byte_size_QComboBox = QComboBox()
        self.byte_size_QComboBox.addItems(['5', '6', '7', '8'])
        self.byte_size_QComboBox.setCurrentText('8')
        layout.addWidget(self.byte_size_QLabel, 3, 0)
        layout.addWidget(self.byte_size_QComboBox, 3, 1)

        self.stop_bits_QLabel = QLabel('Stop Bits')
        self.stop_bits_QComboBox = QComboBox()
        self.stop_bits_QComboBox.addItems(['1', '2'])
        self.stop_bits_QComboBox.setCurrentText('2')
        layout.addWidget(self.stop_bits_QLabel, 4, 0)
        layout.addWidget(self.stop_bits_QComboBox, 4, 1)

        self.parity_QLabel = QLabel('Parity')
        self.parity_QComboBox = QComboBox()
        self.parity_QComboBox.addItems(["Odd", "Even", "None"])
        self.parity_QComboBox.setCurrentText('None')
        layout.addWidget(self.parity_QLabel, 5, 0)
        layout.addWidget(self.parity_QComboBox, 5, 1)

        self.text_QLineEdit = QLineEdit('011003EA000204426B33335829')
        self.send_QPushButton = QPushButton("Send")
        self.send_QPushButton.clicked.connect(self.button_clicked)
        layout.addWidget(self.text_QLineEdit, 6, 1)
        layout.addWidget(self.send_QPushButton, 6, 0)

        layout.setContentsMargins(20, 0, 20, 150)

        self.setLayout(layout)

    def update_port_selection(self):
        select = self.Select_Port_QComboBox.currentText()
        master = PortManger().get_master_pump_port_name_raw
        second = PortManger().get_second_pump_port_name_raw

        if select or master or second not in PortManger().get_ports_list:
            self.Select_Port_QComboBox.clear()
            self.Select_Port_QComboBox.addItems(PortManger().get_ports_list)
            self.Select_Port_QComboBox.setCurrentText(select)

    def update_fields(self):

        self.update_port_selection()
        self.modbus.port = PortManger(s=self.Select_Port_QComboBox.currentText()).get_master_pump_port
        self.modbus.baudrate = int(self.baud_rate_QComboBox.currentText())
        self.modbus.timeout = float(self.timeout_QSpinBox.value())
        self.modbus.bytesize = int(self.byte_size_QComboBox.currentText())
        self.modbus.stopbits = int(self.stop_bits_QComboBox.currentText())

        if self.parity_QComboBox.currentText() == "Odd":
            self.modbus.parity = serial.PARITY_ODD
        elif self.parity_QComboBox.currentText() == "Even":
            self.modbus.parity = serial.PARITY_EVEN
        elif self.parity_QComboBox.currentText() == "None":
            self.modbus.parity = serial.PARITY_NONE

    def button_clicked(self):
        self.update_fields()
        modbus = CRCGenerator.change_format(self.space_cleaner(self.text_QLineEdit.text()))
        try:
            self.modbus.open()
            self.modbus.write(modbus)
            time.sleep(0.1)
            self.modbus.close()
        except:
            ErrorMassage("Error", "Something went wrong, please check your connections and ports")

    @staticmethod
    def space_cleaner(s):
        if " " in s:
            s = s.replace(" ", "")
        return s


class SettingWindow(QMainWindow):
    """
    Setting window GUI
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advance Setting")
        self.setWindowIcon(icon("settings.png"))
        self.setFixedSize(380, 500)
        self.SecondPumpTab = SecondPumpTab()

        # Ok button Setting
        self.ok_btn = QPushButton("OK")
        self.ok_btn.setFixedSize(80, 30)
        self.ok_btn.clicked.connect(self.ok_btn_clicked)

        # Tab setting
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        tabs.setMinimumSize(340, 450)
        tabs.setMovable(True)
        v_layout = QVBoxLayout()

        tabs.addTab(self.SecondPumpTab, "Second Pump")
        tabs.addTab(MasterPumpTab(), "Master Pump")
        tabs.addTab(ModbusSenderTab(), "Modbus Sender")

        # layout setting
        v_layout.addWidget(tabs)
        v_layout.addWidget(tabs)

        h_layout = QHBoxLayout()

        h_layout.addWidget(self.ok_btn)
        v_layout.addLayout(h_layout)
        self.setLayout(v_layout)
        widget = QWidget()
        widget.setLayout(v_layout)

        self.setCentralWidget(widget)

    def ok_btn_clicked(self):
        self.close()


class StepIncreaseWindow(QMainWindow):
    """
    Steps increase window GUI
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("speed adjusting")
        self.setWindowIcon(icon("settings.png"))
        self.setFixedSize(300, 300)

        layout = QGridLayout()
        self.Select_pump = QLabel('Select Pump')
        self.Select_pump_QComboBox = QComboBox()
        self.Select_pump_QComboBox.addItems(["Master", "Second", "Both"])
        layout.addWidget(self.Select_pump, 0, 0)
        layout.addWidget(self.Select_pump_QComboBox, 0, 1)

        self.start_QLabel = QLabel('Start Speed (rpm)')
        self.start_QSpinBox = QSpinBox()
        self.start_QSpinBox.setMaximum(300)
        self.start_QSpinBox.setMinimum(0)
        layout.addWidget(self.start_QLabel, 1, 0)
        layout.addWidget(self.start_QSpinBox, 1, 1)
        self.start_QSpinBox.setValue(2)

        self.stop_QLabel = QLabel('Stop Speed (rpm)')
        self.stop_QSpinBox = QSpinBox()
        layout.addWidget(self.stop_QLabel, 2, 0)
        layout.addWidget(self.stop_QSpinBox, 2, 1)
        self.stop_QSpinBox.setMaximum(300)
        self.stop_QSpinBox.setMinimum(0)
        self.stop_QSpinBox.setValue(10)

        self.step_QLabel = QLabel('Increasing Steps (rpm)')
        self.step_QSpinBox = QSpinBox()
        layout.addWidget(self.step_QLabel, 3, 0)
        layout.addWidget(self.step_QSpinBox, 3, 1)
        self.step_QSpinBox.setMaximum(300)
        self.step_QSpinBox.setMinimum(1)
        self.step_QSpinBox.setValue(1)

        self.duration_QLabel = QLabel('Duration (S)')
        self.duration_QSpinBox = QSpinBox()
        layout.addWidget(self.duration_QLabel, 4, 0)
        layout.addWidget(self.duration_QSpinBox, 4, 1)
        self.duration_QSpinBox.setValue(1)

        # Ok button Setting
        self.start_ = QPushButton("Start")
        self.start_.setFixedSize(80, 30)
        self.start_.clicked.connect(self.start_it)
        layout.addWidget(self.start_, 5, 0)

        # Ok button Setting
        self.ok_btn = QPushButton("OK")
        self.ok_btn.setFixedSize(80, 30)
        self.ok_btn.clicked.connect(self.ok_btn_clicked)
        layout.addWidget(self.ok_btn, 6, 0)

        layout.setContentsMargins(20, 0, 20, 50)

        self.setLayout(layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.threadpool = QThreadPool()

    def ok_btn_clicked(self):
        self.close()

    def start_it(self):
        if PortManger().get_number_of_pump_connected > 1:
            send_to = self.Select_pump_QComboBox.currentText()
            if send_to == "Master":
                send_to = Pump.MASTER
            elif send_to == "Second":
                send_to = Pump.SECOND
            elif send_to == "Both":
                send_to = Pump.BOTH

        elif PortManger().get_number_of_pump_connected == 1:
            send_to = Pump.MASTER
        elif PortManger().get_number_of_pump_connected == 0:
            ErrorMassage("Error", "No pump is Connected, please check your connection and try again ")
        duration = int(self.duration_QSpinBox.value())
        steps = int(self.step_QSpinBox.value())
        stop = int(self.stop_QSpinBox.text())
        start = int(self.start_QSpinBox.text())

        class StepsIncrease(QRunnable):
            @Slot()
            def run(self):
                if PortManger().get_number_of_pump_connected > 0:
                    step_increase(start, stop, steps, duration, send_to)

        self.threadpool.start((StepsIncrease()))


class SettingsQPushButton(AbstractQPushButton):
    def __init__(self):
        super().__init__()
        self.setIcon(icon("settings.png"))
        self.setShortcut(QKeySequence("Ctrl+s"))

    def button_clicked(self):
        self.parent().SettingWindow.show()


class PowerQPushButton(AbstractQPushButton):
    def __init__(self, send_to):
        super().__init__()
        self.power_button_state = False
        self.setIcon(icon("on.png"))
        self.setCheckable(True)
        self.setChecked(self.power_button_state)
        self.setShortcut(QKeySequence("Space"))
        self.send_to = send_to
        self.pumpConnectionManger = PumpConnectionManger()
        self.modbusBuilder = ModbusBuilder()

    def button_clicked(self, checked):
        if checked:
            self.setIcon(icon("off.png"))
            self.pumpConnectionManger.send_pump(data=self.modbusBuilder.build_start().get_modbus, send_to=self.send_to)
            if isinstance(self.parent(), PumpMasterWidget):
                master_state.speed_list.append(self.parent().SpeedQDoubleSpinBox.value())
                master_state.start_stop = True
                if typ.start_stop == IS.DUAL_CLONE:
                    second_state.speed_list.append(self.parent().SpeedQDoubleSpinBox.value())
                    second_state.start_stop = True

            elif isinstance(self.parent(), PumpSecondWidget) or typ.start_stop == IS.DUAL_CLONE:
                second_state.speed_list.append(self.parent().SpeedQDoubleSpinBox.value())
                second_state.start_stop = True
        if not checked:
            self.setIcon(icon("on.png"))
            self.pumpConnectionManger.send_pump(data=self.modbusBuilder.build_stop().get_modbus, send_to=self.send_to)
            if isinstance(self.parent(), PumpMasterWidget):
                master_state.speed_list.append(0)
                master_state.start_stop = False
                if typ.start_stop == IS.DUAL_CLONE:
                    second_state.speed_list.append(0)
                    second_state.start_stop = False

            elif isinstance(self.parent(), PumpSecondWidget):
                second_state.speed_list.append(0)
                second_state.start_stop = False


class DirectionQPushButton(AbstractQPushButton):
    def __init__(self, send_to):
        super().__init__()
        self.direction_button_state = False
        self.setIcon(icon("forward.png"))
        self.setCheckable(True)
        self.setShortcut(QKeySequence("Ctrl+d"))
        self.setChecked(self.direction_button_state)

        self.pumpConnectionManger = PumpConnectionManger()
        self.modbusBuilder = ModbusBuilder()
        self.send_to = send_to

    def button_clicked(self, checked):
        if checked:
            self.setIcon(icon("backward.png"))
            self.pumpConnectionManger.send_pump(
                data=self.modbusBuilder.build_flow_direction("ccw").get_modbus, send_to=self.send_to)
            master_state.direction = "ccw"

        if not checked:
            self.setIcon(icon("forward.png"))
            self.pumpConnectionManger.send_pump(
                data=self.modbusBuilder.build_flow_direction("cw").get_modbus, send_to=self.send_to)
            master_state.direction = "cw"


class AddSecondPumpQPushButton(AbstractQPushButton):
    def __init__(self):
        super().__init__()
        self.setIcon(icon("two.png"))
        self.setShortcut(QKeySequence("Ctrl+2"))

    def button_clicked(self):
        self.parent().SettingWindow.SecondPumpTab.second_pump_QComboBox.setCurrentText("Enabled")
        self.parent().SettingWindow.SecondPumpTab.apply_setting()


class AddMasterPumpQPushButton(AbstractQPushButton):
    def __init__(self):
        super().__init__()
        self.setIcon(icon("one.png"))
        self.setShortcut(QKeySequence("Ctrl+1"))

    def button_clicked(self):
        self.parent().show_master_pump()


class AddMonitorQPushButton(AbstractQPushButton):
    def __init__(self):
        super().__init__()
        self.setIcon(icon("line-graph.png"))
        self.setShortcut(QKeySequence("Ctrl+m"))

    def button_clicked(self):
        self.parent().show_monitor()


class MergeQPushButton(AbstractQPushButton):
    def __init__(self):
        super().__init__()
        self.setIcon(icon("merging.png"))

    def button_clicked(self):
        self.parent().SpeedQDoubleSpinBox.setValue(master_state.speed)


class StepIncreaseQPushButton(AbstractQPushButton):
    def __init__(self):
        super().__init__()
        self.setIcon(icon("stepincrease.png"))
        self.StepIncreaseWindow = StepIncreaseWindow()
        self.setShortcut(QKeySequence("Ctrl+t"))

    def button_clicked(self):
        self.StepIncreaseWindow.show()


class CloseQPushButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.clicked.connect(self.mini_button_clicked)
        self.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Fixed,
        )
        self.setIcon(icon("close.png"))

    def sizeHint(self):
        return QSize(25, 25)

    def mini_button_clicked(self):
        if self.parent().isVisible():
            self.parent().hide()


class InfoQPushButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.clicked.connect(self.button_clicked)
        self.setIcon(icon("help.png"))
        self.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Fixed,
        )
        # self.setIconSize(QSize(self.size() / 8))

    def sizeHint(self):
        return QSize(25, 25)

    @staticmethod
    def button_clicked():
        print("clicked")


class ExternalQPushButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.clicked.connect(self.button_clicked)
        self.setIcon(icon("external.png"))
        self.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Fixed,
        )
        # self.setIconSize(QSize(self.size() / 8))

    def sizeHint(self):
        return QSize(25, 25)

    def button_clicked(self):
        if self.parent().isVisible():
            self.parent().close()
            self.wi = PumpWidget()
            self.wi.show()


class SpeedQSlider(QSlider):
    def __init__(self):
        # super().__init__()
        super().__init__(Qt.Horizontal)
        self.setMaximum(300)
        self.setMinimum(0)
        self.setSingleStep(10)
        self.valueChanged.connect(self.value_changed)

        self.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding,
        )

    def sizeHint(self):
        return QSize(100, 50)

    def value_changed(self, i):
        self.parent().SpeedQDoubleSpinBox.setValue(i)


class SpeedQDoubleSpinBox(QDoubleSpinBox):
    def __init__(self, send_to):
        super().__init__()
        self.setMinimum(0)
        self.setMaximum(300)
        self.setPrefix("speed in rpm : ")
        self.setSingleStep(1)
        self.valueChanged.connect(self.value_changed)

        self.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Fixed)

        # define which pump to send to and the ModBus builder
        self.send_to = send_to
        self.modbusBuilder = ModbusBuilder()
        self.pumpConnectionManger = PumpConnectionManger()

    def sizeHint(self):
        return QSize(100, 30)

    def value_changed(self, i):
        self.pumpConnectionManger.send_pump(data=self.modbusBuilder.build_change_speed(i).get_modbus,
                                            send_to=self.send_to)

        self.parent().SpeedQSlider.setValue(i)
        self.parent().PumpBubbleWidget.value = i
        self.parent().PumpBubbleWidget.color_value = int(i * 10 // 300)
        master_state.speed = i
        if isinstance(self.parent(), PumpMasterWidget) and master_state.start_stop is True:
            master_state.speed_list.append(i)
            if typ.speed == IS.DUAL_CLONE:
                second_state.speed_list.append(i)

        elif isinstance(self.parent(), PumpSecondWidget) and second_state.start_stop is True:
            second_state.speed_list.append(i)


class AbstractPumpWidget(AbstractBackGround):
    def __init__(self, color='#ced9cf'):
        super().__init__()
        self.PumpBubbleWidget = BubbleWidget(text='Pump Speed', text_unit="rpm")
        self.color = QColor(color)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def sizeHint(self):
        return QSize(400, 250)


class PumpWidget(AbstractPumpWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.pump_master_widget = PumpMasterWidget()
        self.pump_second_widget = PumpSecondWidget()
        self.SpeedMonitor = SpeedMonitor()

        self.SettingWindow = SettingWindow()

        self.AddMasterPumpQPushButton = AddMasterPumpQPushButton()
        self.AddMonitorQPushButton = AddMonitorQPushButton()
        self.AddPumpQPushButton = AddSecondPumpQPushButton()
        self.MiniQPushButton = CloseQPushButton()
        self.ExternalQPushButton = ExternalQPushButton()
        self.InfoQPushButton = InfoQPushButton()

        self.g_layout = QGridLayout()
        self.h_layout = QHBoxLayout()
        self.v_layout1 = QHBoxLayout()

        self.settingsQPushButton = SettingsQPushButton()

        self.h_layout.addWidget(self.MiniQPushButton)
        self.h_layout.addWidget(self.ExternalQPushButton)
        self.h_layout.addWidget(self.InfoQPushButton)

        self.v_layout1.addWidget(self.settingsQPushButton)
        self.v_layout1.addWidget(self.AddMasterPumpQPushButton)
        self.v_layout1.addWidget(self.AddPumpQPushButton)
        self.v_layout1.addWidget(self.AddMonitorQPushButton)

        self.g_layout.addLayout(self.v_layout1, 0, 0, 1, 2)
        self.g_layout.addWidget(self.pump_master_widget, 1, 0)

        self.g_layout.addLayout(self.h_layout, 4, 2)

        self.setLayout(self.g_layout)

    def update_my_window(self):
        self.pump_master_widget.power_button.send_to = master_send.start_stop
        self.pump_master_widget.direction_button.send_to = master_send.direction
        self.pump_master_widget.SpeedQDoubleSpinBox.send_to = master_send.speed
        self.g_layout.addWidget(self.pump_second_widget, 1, 1)
        self.pump_second_widget.update_my_window()
        if typ.speed != IS.UNI:
            self.pump_second_widget.show()

    def show_monitor(self):
        self.g_layout.addWidget(self.SpeedMonitor, 2, 0, 2, 2)
        self.SpeedMonitor.show()

    def show_master_pump(self):
        self.pump_master_widget.show()

    def sizeHint(self):
        return QSize(400, 400)

    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.exec_(e.globalPos())


class PumpMasterWidget(AbstractPumpWidget):

    def __init__(self, color='#6d18db'):
        super().__init__()
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.color = QColor(color)

        self.close = CloseQPushButton()
        self.power_button = PowerQPushButton(send_to=master_send.start_stop)
        self.direction_button = DirectionQPushButton(send_to=master_send.direction)
        self.StepIncreaseQPushButton = StepIncreaseQPushButton()
        self.SpeedQDoubleSpinBox = SpeedQDoubleSpinBox(send_to=master_send.speed)
        self.SpeedQSlider = SpeedQSlider()

        self.h_layout = QHBoxLayout()
        self.grid = QGridLayout()

        self.grid.addWidget(self.SpeedQSlider, 0, 0)
        self.grid.addWidget(self.close, 0, 1)
        self.h_layout.addWidget(self.power_button)
        self.h_layout.addWidget(self.direction_button)
        self.h_layout.addWidget(self.StepIncreaseQPushButton)
        self.grid.addLayout(self.h_layout, 1, 0)
        self.grid.addWidget(self.SpeedQDoubleSpinBox, 2, 0)
        self.setLayout(self.grid)
        self.update_my_window()

    def update_my_window(self):
        self.power_button.send_to = master_send.start_stop
        self.direction_button.send_to = master_send.direction
        self.SpeedQDoubleSpinBox.send_to = master_send.speed

    def sizeHint(self):
        return QSize(100, 80)


class PumpSecondWidget(AbstractPumpWidget):

    def __init__(self, color='#600075'):
        super().__init__()
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.color = QColor(color)

        self.close = CloseQPushButton()
        self.power_button_second = PowerQPushButton(send_to=Pump.SECOND)
        self.direction_button_second = DirectionQPushButton(send_to=Pump.SECOND)
        self.MergeQPushButton = MergeQPushButton()
        self.SpeedQSlider = SpeedQSlider()
        self.SpeedQDoubleSpinBox = SpeedQDoubleSpinBox(send_to=Pump.SECOND)

        self.h_layout = QHBoxLayout()
        self.grid = QGridLayout()

        self.grid.addWidget(self.SpeedQSlider, 0, 0)
        self.grid.addWidget(self.close, 0, 1)
        self.h_layout.addWidget(self.power_button_second)
        self.h_layout.addWidget(self.direction_button_second)
        self.h_layout.addWidget(self.MergeQPushButton)
        self.grid.addLayout(self.h_layout, 1, 0)
        self.grid.addWidget(self.SpeedQDoubleSpinBox, 2, 0)
        self.setLayout(self.grid)
        self.update_my_window()

    def update_my_window(self):

        if typ.speed == IS.DUAL_CUSTOM:
            self.SpeedQSlider.setDisabled(False)
            self.SpeedQDoubleSpinBox.setDisabled(False)
        elif typ.speed == IS.DUAL_CLONE or typ.speed == IS.UNI:
            self.SpeedQSlider.setDisabled(True)
            self.SpeedQDoubleSpinBox.setDisabled(True)

        if typ.start_stop == IS.DUAL_CUSTOM:
            self.power_button_second.setDisabled(False)
        elif typ.start_stop == IS.DUAL_CLONE or typ.speed == IS.UNI:
            self.power_button_second.setDisabled(True)

        if typ.direction == IS.DUAL_CUSTOM:
            self.direction_button_second.setDisabled(False)
        elif typ.direction == IS.DUAL_CLONE or typ.speed == IS.UNI:
            self.direction_button_second.setDisabled(True)

    def sizeHint(self):
        return QSize(100, 80)


class PumpMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # setting the window title and dimensions
        self.setWindowTitle("Pump Control")
        self.setWindowIcon(QIcon(r""))
        self.setGeometry(200, 200, 400, 225)

        self.PumpWidget = PumpWidget()
        self.setCentralWidget(self.PumpWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = PumpWidget()

    # qtmodern.styles.dark(app)
    # mw = qtmodern.windows.ModernWindow(window)
    # mw.show()
    window.show()
    app.exec_()