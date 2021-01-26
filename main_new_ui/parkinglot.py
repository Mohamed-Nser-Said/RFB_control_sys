

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