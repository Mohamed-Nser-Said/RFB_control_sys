import qtmodern.styles
import qtmodern.windows
from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import QAction, QApplication, QMainWindow, QStatusBar, QToolBar, QFileDialog, QTabWidget, \
    QMessageBox
from PySide2.QtWidgets import QLabel, QLineEdit, QGridLayout, QTextEdit, QHBoxLayout, QGroupBox, QComboBox, QWidget
from PySide2.QtWidgets import QDoubleSpinBox, QPushButton
from PySide2.QtWidgets import QDockWidget

from RedoxFlowProject.main_new_ui.widgets_builder import PumpAbstract, NewProjectSetNameDialog, SetNewTableDialog
from RedoxFlowProject.main_new_ui.api import PumpMode, Pump, PumpModbusCommandSender, PortManger, ErrorMassage
import os
import shutil
import sys
import tables as tb


# class NewProjectDialog(QMessageBox):
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("new project")
#
#         button = QLineEdit()
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


class PumpQWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Maximum,
            QtWidgets.QSizePolicy.Preferred)
        self.PumpModbusCommandSender = PumpModbusCommandSender()
        self.pump_mode_state = PumpMode.COUPLED
        group_box_pump_mode = QGroupBox("Mode")
        group_box_pump_mode.setMaximumSize(150, 80)
        self.mode_QLabel = QLabel("Pump Mode")
        self.mode_QComboBox = QComboBox()
        self.mode_QComboBox.addItems(["coupled", "decoupled"])
        self.mode_QComboBox.currentTextChanged.connect(self.pump_mode_changed)
        h_layout_pump_mode = QHBoxLayout()
        h_layout_pump_mode.addWidget(self.mode_QLabel)
        h_layout_pump_mode.addWidget(self.mode_QComboBox)
        group_box_pump_mode.setLayout(h_layout_pump_mode)

        self.pump1 = PumpAbstract("Pump 1")
        self.pump1.start_stop_QPushButton.clicked.connect(lambda _: self.start_stop_pump(Pump.MASTER, _))
        self.pump2 = PumpAbstract("Pump 2")
        self.pump2.start_stop_QPushButton.clicked.connect(lambda _: self.start_stop_pump(Pump.SECOND, _))
        self.pump2.setDisabled(True)

        g_layout = QGridLayout()
        g_layout.addWidget(group_box_pump_mode, 0, 0)
        g_layout.addWidget(self.pump1, 1, 0)
        g_layout.addWidget(self.pump2, 2, 0)
        self.setLayout(g_layout)

    def sizeHint(self):
        return QtCore.QSize(100, 200)

    def pump_mode_changed(self):
        if self.mode_QComboBox.currentText() == "coupled":
            self.pump2.setDisabled(True)
            self.pump_mode_state = PumpMode.COUPLED
        else:
            self.pump2.setDisabled(False)
            self.pump_mode_state = PumpMode.DECOUPLED

    def start_stop_pump(self, pump, s):
        if self.pump_mode_state == PumpMode.COUPLED:
            pump = Pump.BOTH
        if s:
            self.PumpModbusCommandSender.send_pump(data=self.PumpModbusCommandSender.start, send_to=pump)
            if pump == Pump.MASTER:
                self.pump1.start_stop_QPushButton.setText("Stop")
            elif pump == Pump.SECOND:
                self.pump2.start_stop_QPushButton.setText("Stop")
        if not s:
            self.PumpModbusCommandSender.send_pump(data=self.PumpModbusCommandSender.stop, send_to=pump)
            if pump == Pump.MASTER:
                self.pump1.start_stop_QPushButton.setText("Start")
            elif pump == Pump.SECOND:
                self.pump2.start_stop_QPushButton.setText("Start")


class AddPumpQWidgetAction(QAction):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.setText("Pump Control")
        self.setStatusTip("Add Pump Control")
        self.triggered.connect(self.clicked)
        self.setCheckable(True)
        self.setChecked(True)

    def clicked(self, s):
        if s:
            self.parent().PumpQWidget.show()

        else:
            self.parent().PumpQWidget.hide()


def icon(icon_name, root="images"):
    return QIcon(os.path.join("..", root, icon_name))


class SCPICommandLine(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)

        f = self.font()
        f.setPointSize(14)
        f.setWeight(5)
        self.setFont(f)
        self.setText(">>  ")
        # self.setEnabled(False)
        # self.returnPressed.connect(self.pressed)

    def keyReleaseEvent(self, e):
        if e.key() == 16777220:
            self.pressed()

    def sizeHint(self):
        return QtCore.QSize(1080, 100)

    def pressed(self):
        self.setText(">>  ")
        # print("enter")


class SCPICommandLineAction(QAction):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.setText("SCPI Command Line")
        self.triggered.connect(self.clicked)
        self.setStatusTip("add SCPI Command Line")
        self.setCheckable(True)
        self.SCPICommandLine = SCPICommandLine()

    def clicked(self, s):
        self.parent().layout.addWidget(self.SCPICommandLine, 2, 0, 1, 3)
        if s:
            self.SCPICommandLine.show()

        elif not s:
            self.SCPICommandLine.hide()


class NewProjectTab(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setDocumentMode(True)
        self.setTabsClosable(True)


class NewProjectAction(QAction):
    def __init__(self, parent):
        super().__init__()
        self.NewProjectSetNameDialog = NewProjectSetNameDialog()
        self.triggered.connect(self.NewProjectSetNameDialog.show)
        self.NewProjectSetNameDialog.save_QPushButton.clicked.connect(self.save_project_name_dialog)
        self.NewProjectSetNameDialog.cancel_QPushButton.clicked.connect(self.NewProjectSetNameDialog.close)
        self.setText("New Project")
        self.setIcon(icon("new_project.png"))
        self.setStatusTip("start a new project")
        self.setParent(parent)
        self.setShortcut(QKeySequence("Ctrl+n"))

        self.all_project_list = DataBase().get_old_projects_name_list

        self.tabs = NewProjectTab()

        self.tabs.currentChanged.connect(self.current_tab_changed)

        self.tabs.tabCloseRequested.connect(self.close_tab)

    def save_project_name_dialog(self):
        self.project_name = self.NewProjectSetNameDialog.file_name_QLineEdit.text()
        if self.project_name in self.all_project_list:
            ErrorMassage("Name already exist", "this project name is already exist\nplease try different name")

        else:
            self.add_new_tab()
            self.NewProjectSetNameDialog.hide()
            DataBase().create_new_project(project_name=self.project_name)

    def close_tab(self, i):
        self.tabs.removeTab(i)

        if len(self.all_project_list) == 0 and self.parent().label.isHidden():
            self.parent().label.setVisible(True)
            self.tabs.hide()

    def add_new_tab(self):
        n = len(self.all_project_list)
        if self.parent().label.isVisible():
            self.parent().label.hide()
            self.tabs.show()

        self.parent().layout.addWidget(self.tabs, 0, 1, 2, 2)
        i = self.tabs.addTab(Label(text=f'Project {n}:: {self.project_name}'), f'Project {n}::{self.project_name}')
        self.all_project_list.append(self.project_name)

        self.tabs.setCurrentIndex(i)

    def current_tab_changed(self, i):
        pass

    def update_title(self):
        self.tabs.currentWidget().page().title()


class CreatNewTableAction(QAction):
    def __init__(self):
        super().__init__()
        self.setText("New Table")
        self.setStatusTip("Creat a New Table")
        self.SetNewTableDialog = SetNewTableDialog()
        self.SetNewTableDialog.cancel_QPushButton.clicked.connect(self.SetNewTableDialog.close)
        self.SetNewTableDialog.save_QPushButton.clicked.connect(self.create_new_table)
        self.triggered.connect(self.show_table_dialog)

    def create_new_table(self):
        self.tabel_name = self.SetNewTableDialog.file_name_QLineEdit.text()
        print(self.tabel_name)
        self.SetNewTableDialog.hide()

    def show_table_dialog(self):
        self.SetNewTableDialog.table_QComboBox.addItems(DataBase().get_old_projects_name_list)
        self.SetNewTableDialog.show()


class Label(QLabel):
    def __init__(self, font_size=36, weight=12, text="new label"):
        super().__init__()
        f = self.font()
        f.setPointSize(font_size)
        f.setWeight(weight)
        self.setFont(f)
        self.setText(text)
        self.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)


class DataBase:
    def __init__(self, ):
        self.data_dir = "hdf_data"
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)
        self.main_file = os.path.join(self.data_dir, "main_data_file.h5")

    def create_new_project(self, project_name):
        # creat a new HDF5 file group
        with tb.open_file(self.main_file, "a") as t:
            t.create_group(t.root, project_name)

    def create_new_table(self, project_name, table_name):
        with tb.open_file(self.main_file, "a") as t:
            t.create_table(project_name, table_name)

    @property
    def get_old_projects_name_list(self):
        with tb.open_file(self.main_file, "a")as t:
            _ = list(t.root.__members__)
        return _


class HelpAction(QAction):
    def __init__(self):
        super().__init__()
        self.setText("Help")
        self.setStatusTip("Need Help")
        self.triggered.connect(self.clicked)
        self.setShortcut(QKeySequence("Ctrl+h"))

    def clicked(self):
        pass


class NewTableAction(QAction):
    def __init__(self, parent):
        super().__init__()
        self.setText("New Table")
        self.triggered.connect(self.clicked)
        self.setParent(parent)

    def clicked(self):
        pass


class AboutAction(QAction):
    def __init__(self):
        super().__init__()
        self.setText("About")
        self.triggered.connect(self.clicked)

    def clicked(self):
        print("about")


class ExitAction(QAction):
    def __init__(self):
        super(ExitAction, self).__init__()
        self.setText("Exit")
        self.setStatusTip("Exit from the App")
        self.triggered.connect(self.clicked)
        self.setShortcut(QKeySequence("Ctrl+e"))

    def clicked(self):
        quit()


class OpenAction(QAction):
    def __init__(self):
        super().__init__()
        self.setText("Open")

        self.setIcon(icon("open.png"))
        self.setStatusTip("open old project")
        self.triggered.connect(self.clicked)

    def clicked(self):
        self.file = QFileDialog.getOpenFileName(self.parent(), "Open Project", os.path.join(os.getcwd(), "hdf_data"))
        with tb.open_file(self.file[0], "a") as t:
            print(list(t.root.__members__))


class SaveAction(QAction):
    def __init__(self):
        super().__init__()
        self.setText("Save Project")
        self.setIcon(icon("save.png"))
        self.setStatusTip("save a new project")
        self.triggered.connect(self.clicked)
        self.setShortcut(QKeySequence("Ctrl+s"))

    def clicked(self):
        self.file = QFileDialog.getSaveFileName(self.parent(), "Save Project", "C:/Users/abuaisha93/Desktop/")
        file = open(self.file[0], "w")
        file.close()


class SettingAction(QAction):
    def __init__(self):
        super().__init__()
        self.setText("Settings")
        self.setIcon(icon("setting.png"))
        self.setStatusTip("setting")
        self.triggered.connect(self.clicked)
        self.setShortcut(QKeySequence("Ctrl+Alt+s"))
        # self.w = SettingWindow()

    def clicked(self):
        # self.w.show()
        print("setting")


class AnalyseAction(QAction):
    def __init__(self):
        super().__init__()
        self.setText("Analyse")
        self.triggered.connect(self.clicked)

    def clicked(self):
        print("Analysing")


class MonitorAction(QAction):
    def __init__(self):
        super().__init__()
        self.setText("Monitor")
        self.triggered.connect(self.clicked)

    def clicked(self):
        print("Monitor ...")


class DarkModeAction(QAction):
    def __init__(self):
        super().__init__()
        self.setText("DarkMode")
        self.setIcon(icon("dark_mode.png"))
        self.triggered.connect(self.clicked)
        self.setCheckable(True)

    @staticmethod
    def clicked(s):
        if s:
            qtmodern.styles.dark(app)
        else:
            qtmodern.styles.light(app)


class NewRecordAction(QAction):
    def __init__(self):
        super().__init__()
        self.setText("Start Record")
        self.triggered.connect(self.clicked)
        self.setStatusTip("New Table")
        icon = QIcon(os.path.join("..", "images", "add.png"))
        self.setIcon(QIcon(icon))

    def clicked(self, s):
        print("add")


class GetPDFReportAction(QAction):
    def __init__(self):
        super().__init__()
        self.setText("Generate PDF Report")
        self.setStatusTip("Get PDF report summary")
        self.triggered.connect(self.clicked)

    def clicked(self):
        print("report is loading")


class LaunchViTables(QAction):
    def __init__(self):
        super().__init__()
        self.setText("launch ViTables")
        self.setIcon(icon("setting.png"))
        self.setStatusTip("launch ViTables")
        self.triggered.connect(self.clicked)
        self.setShortcut(QKeySequence("Ctrl+Shift+l"))

    @staticmethod
    def clicked():
        from vitables.start import gui
        gui()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Preferred)
        # self.setDocumentMode(True)
        self.setWindowTitle("RedoX App 2.1")
        self.setWindowIcon(QIcon(os.path.join("..", "images", "app.png")))
        # self.setCentralWidget(Label(text="Creat New Project Ctrl+N"))

        self.layout = QGridLayout()
        self.label = Label(text="Create New Project Ctrl+N")
        #########################################
        self.layout.addWidget(self.label, 0, 1, 2, 2)

        self.PumpQWidget = PumpQWidget()
        self.layout.addWidget(self.PumpQWidget, 0, 0, 2, 1)

        self.w = QtWidgets.QWidget()
        self.w.setLayout(self.layout)
        self.setCentralWidget(self.w)

        # QDocks
        # self.addDockWidget(Qt.BottomDockWidgetArea, PumpQDock())
        # self.addDockWidget(Qt.BottomDockWidgetArea, StepIncreaseQDock())
        # self.addDockWidget(Qt.LeftDockWidgetArea, Tables())

        # all actions
        self.open_action = OpenAction()
        self.save_action = SaveAction()
        self.SCPICommandLine = SCPICommandLineAction(self)
        self.add_new_measurement = NewRecordAction()
        self.exit_action = ExitAction()
        self.new_project = NewProjectAction(self)
        self.AddPumpQWidgetAction = AddPumpQWidgetAction(self)
        self.LaunchViTables = LaunchViTables()
        self.NewTableAction = NewTableAction(self)
        self.monitor = MonitorAction()
        self.analyse = AnalyseAction()
        self.get_pdf_report = GetPDFReportAction()
        self.setting = SettingAction()
        self.dark_mode_action = DarkModeAction()
        self.CreatNewTableAction = CreatNewTableAction()


        self.help_action = HelpAction()
        self.about_action = AboutAction()

        self.menu = self.menuBar()
        self.file = self.menu.addMenu("File")

        self.file.addAction(self.new_project)
        self.file.addAction(self.open_action)
        self.file.addAction(self.save_action)

        self.file.addSeparator()
        self.file.addAction(self.LaunchViTables)
        self.file.addSeparator()
        self.file.addAction(self.get_pdf_report)
        self.file.addSeparator()
        self.file.addAction(self.setting)
        self.file.addSeparator()
        self.file.addAction(self.exit_action)

        self.tools = self.menu.addMenu("Tools")
        self.tools.addAction(self.SCPICommandLine)
        self.tools.addAction(self.AddPumpQWidgetAction)
        self.tools.addAction(self.monitor)
        self.tools.addSeparator()
        self.tools.addAction(self.analyse)

        self.view = self.menu.addMenu("View")

        self.appearance = self.view.addMenu("Appearance")

        self.appearance.addAction(self.dark_mode_action)

        self.browse = self.menu.addMenu("Browse")

        self.remote = self.menu.addMenu("Remote")

        self.help = self.menu.addMenu("Help")

        self.help.addAction(self.help_action)
        self.help.addAction(self.about_action)

        self.toolbar = QToolBar("main toolbar")
        self.toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.new_project)
        self.toolbar.addAction(self.open_action)
        self.toolbar.addAction(self.save_action)

        self.toolbar.addSeparator()
        self.toolbar.addAction(self.dark_mode_action)
        self.toolbar.addSeparator()

        self.project_toolbar = QToolBar("project")
        self.addToolBar(Qt.RightToolBarArea, self.project_toolbar)
        self.project_toolbar.setIconSize(QSize(16, 16))
        self.project_toolbar.setMovable(False)

        self.project_toolbar.addAction(self.CreatNewTableAction)

        self.setStatusBar(QStatusBar(self))

    def sizeHint(self):
        return QtCore.QSize(1080, 650)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()

    # qtmodern.styles.dark(app)
    # mw = qtmodern.windows.ModernWindow(window)
    # mw.show()
    window.show()
    app.exec_()
