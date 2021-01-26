
import qtmodern.styles
import qtmodern.windows
from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import QAction, QApplication, QMainWindow, QStatusBar, QToolBar, QFileDialog, QTabWidget, \
    QMessageBox, QDialog
from PySide2.QtWidgets import QLabel, QLineEdit, QGridLayout, QTextEdit, QHBoxLayout, QGroupBox, QComboBox, QWidget
from PySide2.QtWidgets import QDoubleSpinBox, QPushButton
from PySide2.QtWidgets import QDockWidget

from RedoxFlowProject.main_new_ui.widgets_builder import PumpAbstract
from RedoxFlowProject.main_new_ui.api import PumpMode, Pump, PumpModbusCommandSender, PortManger
import os
import shutil
import sys


class NewProjectDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("new project")
        self.file_name_QLabel = QLabel("project Name")
        self.warning_QLabel = QLabel("project Name must be one word or multiple\nwords connected with '_'")
        self.save_QPushButton = QPushButton("save")
        self.cancel_QPushButton = QPushButton("cancel")
        self.layout = QGridLayout()
        self.file_name_QLineEdit = QLineEdit()
        self.layout.addWidget(self.file_name_QLabel, 1, 0)
        self.layout.addWidget(self.file_name_QLineEdit, 1, 1, 1, 2)
        self.layout.setVerticalSpacing(30)
        self.layout.addWidget(self.save_QPushButton, 2, 1)
        self.layout.addWidget(self.cancel_QPushButton, 2, 2)
        self.layout.addWidget(self.warning_QLabel, 0, 0, 1, 3)
        self.setLayout(self.layout)


#
#
#
#
# class MainWindow(QMainWindow):
#     # end::MainWindow[]
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("My App")
#
#         button = QPushButton("Press me for a dialog!")
#         button.clicked.connect(self.button_clicked)
#         self.setCentralWidget(button)
#
#     # tag::button_clicked[]
#
#     # __init__ skipped for clarity
#     def button_clicked(self, s):
#         dlg = QMessageBox(self)
#         dlg.setWindowTitle("I have a question!")
#         dlg.setText("This is a question dialog")
#         dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
#         dlg.setIcon(QMessageBox.Question)
#         button = dlg.exec_()
#
#         if button == QMessageBox.Yes:
#             print("Yes!")
#         else:
#             print("No!")

    # end::button_clicked[]


app = QApplication([])

window = NewProjectDialog()
window.show()

app.exec_()
