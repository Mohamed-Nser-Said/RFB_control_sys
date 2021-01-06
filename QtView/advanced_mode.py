import sys
import pandas as pd
import qtmodern.styles
import qtmodern.windows
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QIcon, QKeySequence, QColor, QPalette
from PySide2.QtWidgets import (QAction, QApplication, QCheckBox, QLabel,
                               QMainWindow, QStatusBar, QToolBar, QStyle, QFileDialog)
from PySide2.QtWidgets import QDoubleSpinBox, QGridLayout, \
    QWidget, QPushButton, QComboBox, QDockWidget
from RedoxFlowProject.QtView.AdvancedModeWidgets import PumpQWidget, SettingWindow, StepIncreaseWindow, TableModel


class DataBase:
    pass


class HelpAction(QAction):
    def __init__(self):
        super().__init__()
        self.setText("Help")
        self.setStatusTip("Need Help")
        self.triggered.connect(self.clicked)
        self.setShortcut(QKeySequence("Ctrl+h"))

    def clicked(self):
        print("help ist da")


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
        self.setIcon(QIcon("bug.png"))
        self.setStatusTip("Exit from the App")
        self.triggered.connect(self.clicked)
        self.setShortcut(QKeySequence("Ctrl+e"))

    def clicked(self):
        quit()


class NewProjectAction(QAction):
    def __init__(self):
        super().__init__()
        self.setText("New Project")
        self.setIcon(QIcon("../QtIcons/new_project.png"))
        self.setStatusTip("start a new project")
        self.triggered.connect(self.clicked)
        self.setShortcut(QKeySequence("Ctrl+n"))

    def clicked(self):
        print("starting a new project")


class OpenAction(QAction):
    def __init__(self):
        super().__init__()
        self.setText("Open")
        self.setIcon(QIcon("../QtIcons/open.png"))
        self.setStatusTip("open old project")
        self.triggered.connect(self.clicked)

    def clicked(self):
        self.file = QFileDialog.getOpenFileName(self.parent(), "Open Project", "C:/Users/abuaisha93/Desktop/")
        if isinstance(self.file[0], str) and len(self.file[0]) > 0:
            f = open(self.file[0], "r")
            print(f.read())


class SaveAction(QAction):
    def __init__(self):
        super().__init__()
        self.setText("Save Project")
        self.setIcon(QIcon("../QtIcons/save.png"))
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
        self.setIcon(QIcon(r"../QtIcons/setting.png"))
        self.setStatusTip("setting")
        self.triggered.connect(self.clicked)
        self.setShortcut(QKeySequence("Ctrl+Alt+s"))
        self.w = SettingWindow()
    def clicked(self):
        self.w.show()


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
        self.triggered.connect(self.clicked)
        self.setIcon(QIcon(r"../QtIcons/dark_mode.png"))
        self.setCheckable(True)

    @staticmethod
    def clicked(s):
        if s:
            qtmodern.styles.dark(app)
        else:
            qtmodern.styles.light(app)


class StartRecordAction(QAction):
    def __init__(self):
        super().__init__()
        self.setText("Start Record")
        self.triggered.connect(self.clicked)
        self.setStatusTip("Recording data")
        self.setIcon(QIcon(r"../QtIcons/play.png"))
        self.setCheckable(True)

    def clicked(self, s):
        if s:
            self.setText("Start Record")
            self.setIcon(QIcon(r"../QtIcons/pause_.png"))
        elif not s:
            self.setText("Stop Record")
            self.setIcon(QIcon(r"../QtIcons/play.png"))


class NewRecordAction(QAction):
    def __init__(self):
        super().__init__()
        self.setText("Start Record")
        self.triggered.connect(self.clicked)
        self.setStatusTip("New Table")
        self.setIcon(QIcon(r"../QtIcons/add.png"))

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Preferred)

        self.setWindowTitle("RedoX App Gen 2.0")
        self.setWindowIcon(QIcon(r"../QtIcons/app.png"))
        self.setCentralWidget(Tables())

        # QDocks
        self.addDockWidget(Qt.BottomDockWidgetArea, PumpQDock())
        self.addDockWidget(Qt.BottomDockWidgetArea, StepIncreaseQDock())
        # self.addDockWidget(Qt.LeftDockWidgetArea, Tables())

        # all actions
        self.open_action = OpenAction()
        self.save_action = SaveAction()
        self.start_stop_record = StartRecordAction()
        self.add_new_measurement = NewRecordAction()
        self.exit_action = ExitAction()
        self.new_project = NewProjectAction()
        self.monitor = MonitorAction()
        self.analyse = AnalyseAction()
        self.get_pdf_report = GetPDFReportAction()
        self.setting = SettingAction()

        self.menu = self.menuBar()
        self.file = self.menu.addMenu("File")

        self.file.addAction(self.new_project)
        self.file.addAction(self.open_action)
        self.file.addAction(self.save_action)

        self.file.addSeparator()
        self.file.addAction(self.get_pdf_report)
        self.file.addSeparator()
        self.file.addAction(self.setting)
        self.file.addSeparator()
        self.file.addAction(self.exit_action)

        self.tools = self.menu.addMenu("Tools")

        self.tools.addAction(self.monitor)
        self.tools.addSeparator()
        self.tools.addAction(self.analyse)

        self.view = self.menu.addMenu("View")

        self.appearance = self.view.addMenu("Appearance")
        self.dark_mode_action = DarkModeAction()
        self.appearance.addAction(self.dark_mode_action)

        self.browse = self.menu.addMenu("Browse")

        self.remote = self.menu.addMenu("Remote")

        self.help = self.menu.addMenu("Help")
        self.help_action = HelpAction()
        self.about_action = AboutAction()
        self.help.addAction(self.help_action)
        self.help.addAction(self.about_action)

        # self.add_menu("Analysis", ["All Reading", "Voltage", "Current"])
        # self.add_menu("View", ["Pump Widget", "Keithley", "Monitor"])

        toolbar = QToolBar("Record")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        toolbar.addAction(self.new_project)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.save_action)

        toolbar.addSeparator()
        toolbar.addAction(self.dark_mode_action)
        toolbar.addSeparator()

        toolbar.addAction(self.add_new_measurement)
        toolbar.addAction(self.start_stop_record)

        self.setStatusBar(QStatusBar(self))

    def sizeHint(self):
        return QtCore.QSize(1080, 650)


class PumpQDock(QDockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flow Control")
        self.setWidget(PumpQWidget())
        # self.setAllowedAreas(Qt.RightDockWidgetArea)
        self.setFloating(True)


class StepIncreaseQDock(QDockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Step Increase Tool")
        self.setWidget(StepIncreaseWindow())
        self.setFloating(False)


class Tables(QDockWidget):
    def __init__(self):
        super().__init__()

        self.table = QtWidgets.QTableView()

        data = pd.DataFrame(
            [[1, 9, 2, 3, 5], [1, 0, -1, 3, 5], [3, 5, 2, 3, 5], [3, 3, 2, 3, 5], [5, 8, 9, 3, 5]],
            columns=["Time [s]", "Pump 1 Speed [rpm]", "Pump 2 Speed [rpm]", "Voltage [V]", "Current [A]"],
            index=["1", "2", "3", "4", "5"],
        )

        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.setWidget(self.table)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    # pal = QPalette()
    # pal.setColor(QPalette.Background, '#545454')
    # PumpMainWindow.setAutoFillBackground(True)
    # PumpMainWindow.setPalette(pal)
    #
    # qtmodern.styles.dark(app)
    # mw = qtmodern.windows.ModernWindow(window)
    # mw.show()

    app.exec_()
