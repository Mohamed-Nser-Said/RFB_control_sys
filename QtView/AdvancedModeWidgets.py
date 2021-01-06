from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import QThreadPool, Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QComboBox, QLabel, QGridLayout, QWidget, QDoubleSpinBox, QPushButton, QHBoxLayout, \
    QVBoxLayout, QTabWidget, QLineEdit, QMainWindow, QSpinBox, QGroupBox


class SettingWindow(QMainWindow):
    """
    Setting window GUI
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advance Setting")
        self.setWindowIcon(QIcon(r"../QtIcons/settings.png"))
        self.setFixedSize(300, 400)

        # Ok button Setting
        self.ok_btn = QPushButton("OK")
        self.ok_btn.setFixedSize(80, 30)
        self.ok_btn.clicked.connect(self.ok_btn_clicked)

        # Tab setting
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        # tabs.setMinimumSize(340, 450)
        tabs.setMovable(True)
        v_layout = QVBoxLayout()

        tabs.addTab(PumpTab(), "Pump Communication")

        # layout setting
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


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class PumpTab(QTabWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()

        self.baud_rate_QLabel = QLabel('Baudrate')
        self.baud_rate_QComboBox = QComboBox()
        self.baud_rate_QComboBox.addItems(['1800', '2400', '4800', '9600', '19200'])
        self.baud_rate_QComboBox.setCurrentText('9600')
        layout.addWidget(self.baud_rate_QLabel, 0, 0)
        layout.addWidget(self.baud_rate_QComboBox, 0, 1)

        self.timeout_QLabel = QLabel('Timeout')
        self.timeout_QSpinBox = QDoubleSpinBox()
        self.timeout_QSpinBox.setSingleStep(0.1)
        self.timeout_QSpinBox.setValue(1.0)
        layout.addWidget(self.timeout_QLabel, 1, 0)
        layout.addWidget(self.timeout_QSpinBox, 1, 1)

        self.byte_size_QLabel = QLabel('Byte Size')
        self.byte_size_QComboBox = QComboBox()
        self.byte_size_QComboBox.addItems(['5', '6', '7', '8'])
        self.byte_size_QComboBox.setCurrentText('8')
        layout.addWidget(self.byte_size_QLabel, 2, 0)
        layout.addWidget(self.byte_size_QComboBox, 2, 1)

        self.stop_bits_QLabel = QLabel('Stop Bits')
        self.stop_bits_QComboBox = QComboBox()
        self.stop_bits_QComboBox.addItems(['1', '2'])
        self.stop_bits_QComboBox.setCurrentText('2')
        layout.addWidget(self.stop_bits_QLabel, 3, 0)
        layout.addWidget(self.stop_bits_QComboBox, 3, 1)

        self.parity_QLabel = QLabel('Parity')
        self.parity_QComboBox = QComboBox()
        self.parity_QComboBox.addItems(["Odd", "Even", "None"])
        self.parity_QComboBox.setCurrentText('None')
        layout.addWidget(self.parity_QLabel, 4, 0)
        layout.addWidget(self.parity_QComboBox, 4, 1)

        self.apply_QPushButton = QPushButton("Apply")
        layout.addWidget(self.apply_QPushButton, 5, 0)

        layout.setContentsMargins(20, 0, 20, 70)

        self.setLayout(layout)


class Pump(QWidget):
    def __init__(self, name):
        super().__init__()
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Preferred)

        layout = QGridLayout()

        self.pump_port_selection_QComboBox = QComboBox()
        self.pump_port_selection_QComboBox.addItems(["COM1", "COM2"])
        self.pump_port_selection_QLabel = QLabel('Select port')

        layout.addWidget(self.pump_port_selection_QLabel, 0, 0)
        layout.addWidget(self.pump_port_selection_QComboBox, 0, 1)

        self.pump_speed_QLabel = QLabel('Speed')
        self.pump_speed_QDoubleSpinBox = QDoubleSpinBox()
        layout.addWidget(self.pump_speed_QLabel, 1, 0)
        layout.addWidget(self.pump_speed_QDoubleSpinBox, 1, 1)

        self.pump_direction_QLabel = QLabel('Direction')
        self.pump_direction_QComboBox = QComboBox()
        self.pump_direction_QComboBox.addItems(["CW", "CCW"])
        layout.addWidget(self.pump_direction_QLabel, 2, 0)
        layout.addWidget(self.pump_direction_QComboBox, 2, 1)

        self.start_stop_QPushButton = QPushButton("Start")
        self.start_stop_QPushButton.clicked.connect(self.start_stop_btn)
        layout.addWidget(self.start_stop_QPushButton, 3, 1)

        group_box_pump = QGroupBox(name)
        group_box_pump.setLayout(layout)

        v = QHBoxLayout()
        v.addWidget(group_box_pump)
        self.setLayout(v)

    def sizeHint(self):
        return QtCore.QSize(100, 70)

    def start_stop_btn(self):
        print("Apply")


class PumpQWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Preferred)

        group_box_pump_mode = QGroupBox("Mode")

        self.mode_QLabel = QLabel("Pump Mode")
        self.mode_QComboBox = QComboBox()
        self.mode_QComboBox.addItems(["coupled", "decoupled"])

        h_layout_pump_mode = QHBoxLayout()
        h_layout_pump_mode.addWidget(self.mode_QLabel)
        h_layout_pump_mode.addWidget(self.mode_QComboBox)
        group_box_pump_mode.setLayout(h_layout_pump_mode)

        self.pump1 = Pump("Pump 1")
        self.pump2 = Pump("Pump 2")

        g_layout = QGridLayout()
        g_layout.addWidget(group_box_pump_mode, 0, 0)
        g_layout.addWidget(self.pump1, 0, 1)
        g_layout.addWidget(self.pump2, 0, 2)
        self.setLayout(g_layout)

    def sizeHint(self):
        return QtCore.QSize(200, 70)


class StepIncreaseWindow(QMainWindow):
    """
    Steps increase window GUI
    """
    def __init__(self):
        super().__init__()
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Preferred)
        self.setWindowTitle("speed adjusting")
        self.setWindowIcon(QIcon(r"../QtIcons/settings.png"))

        layout = QGridLayout()
        self.Select_pump = QLabel('Select Pump')
        self.Select_pump_QComboBox = QComboBox()
        self.Select_pump_QComboBox.addItems(["pump 1", "Pump 2", "Both"])
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
        self.start_.clicked.connect(self.start_it)
        layout.addWidget(self.start_, 5, 0)
        gb = QGroupBox()
        gb.setLayout(layout)
        self.setCentralWidget(gb)

    def start_it(self):
        print("starting ...")

    def sizeHint(self):
        return QtCore.QSize(100, 70)


