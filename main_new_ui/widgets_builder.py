import sys
import qtmodern.styles
import qtmodern.windows
from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QComboBox, QLabel, QGridLayout, QWidget, QDoubleSpinBox, QPushButton, QHBoxLayout, \
    QDialog, QLineEdit
from PySide2.QtWidgets import QMainWindow, QSpinBox, QGroupBox, QApplication
from RedoxFlowProject.main_new_ui.api import PortManger


class PumpAbstract(QWidget):
    def __init__(self, name):
        super().__init__()
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Maximum,
            QtWidgets.QSizePolicy.Maximum)

        layout = QGridLayout()

        self.pump_port_selection_QComboBox = QComboBox()
        self.pump_port_selection_QComboBox.setMaximumSize(80, 70)
        self.pump_port_selection_QComboBox.addItems(PortManger().get_ports_list)
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
        self.start_stop_QPushButton.setCheckable(True)
        layout.addWidget(self.start_stop_QPushButton, 3, 1)

        group_box_pump = QGroupBox(name)
        group_box_pump.setLayout(layout)

        v = QHBoxLayout()
        v.addWidget(group_box_pump)
        self.setLayout(v)

    def sizeHint(self):
        return QtCore.QSize(100, 70)


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


class NewProjectSetNameDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("new project")
        self.file_name_QLabel = QLabel("project Name")
        self.warning_QLabel = QLabel("project Name must be one word or multiple\nwords connected with '_'")
        self.save_QPushButton = QPushButton("save")
        self.cancel_QPushButton = QPushButton("cancel")
        self.layout = QGridLayout()
        self.file_name_QLineEdit = QLineEdit()
        self.layout.addWidget(self.file_name_QLabel, 2, 0)
        self.layout.addWidget(self.file_name_QLineEdit, 2, 1, 1, 2)
        self.layout.setVerticalSpacing(30)
        self.layout.addWidget(self.save_QPushButton, 3, 1)
        self.layout.addWidget(self.cancel_QPushButton, 3, 2)
        self.layout.addWidget(self.warning_QLabel, 0, 0, 1, 3)
        self.setLayout(self.layout)


class SetNewTableDialog(NewProjectSetNameDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("new Table")
        self.file_name_QLabel.setText("Table Name")
        self.warning_QLabel.setText(";) You Have to choose where you want to save this table\nand the table Name"
                                    " must be one word or multiple\nwords connected with '_'")

        self.table_QComboBox = QComboBox()
        self.table_QLabel = QLabel("Project Name")
        self.layout.addWidget(self.table_QLabel, 1, 0)
        self.layout.addWidget(self.table_QComboBox, 1, 1, 1, 2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    win = StepIncreaseWindow()

    qtmodern.styles.dark(app)
    # mw = qtmodern.windows.ModernWindow(win)
    win.show()

    app.exec_()
