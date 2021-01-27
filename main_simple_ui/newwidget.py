import sys
import time
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QPushButton


class Add(QPushButton):
    def __init__(self, text="Add A Widget", icon="icons/plus.png", text_color='#0f4d14', color='#ced9cf'):
        super().__init__()
        self.text_color = QtGui.QColor(text_color)
        self.text = text
        self.color = QtGui.QColor(color)
        self.icon = QPixmap(icon)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )

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

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(self.color))
        brush.setStyle(Qt.SolidPattern)

        # QPainterPath to draw rectangle oth round shape
        path = QtGui.QPainterPath()
        path.addRoundedRect(rect, 5, 5)
        painter.fillPath(path, brush)

        # icon window
        painter.drawPixmap(QtCore.QRect(width * 0.8, height * 0.7, height * 0.2, height * 0.2), self.icon)

        # setting the text attributes through Qpen
        pen = painter.pen()
        pen.setColor(self.text_color)
        pen.setWidthF(1)
        painter.setPen(pen)
        font = painter.font()
        font.setFamily("Serif")
        font.setBold(True)
        # text relative size to the window
        font.setPointSize((width + height) / 20)
        painter.setFont(font)
        painter.drawText(QtCore.QRect(width * 0.05, height * 0.7, width, height), "{}".format(self.text))
        painter.end()


class BubbleWidget(QtWidgets.QWidget):
    def __init__(self, x=25,text_unit="Add unit", color_text="white" , text='new text', icon=None, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.x = x
        self.color_text = QtGui.QColor(color_text)
        self.text = text
        self.text_unit = text_unit
        self.colors = [
            "#4281f5",
            "#42b6f5",
            "#42f5a7",
            "#5df542",
            "#f2f542",
            "#f5ce42",
            "#f59342",
            "#f54242",
            "#f46d43",
            "#d53e4f",
            "#ad0000",
        ]
        self.icon = icon
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed,
        )

        self.value = 0
        self.color_value = 0
    def sizeHint(self):
        return QtCore.QSize(220, 70)


    def paintEvent(self, e):
        # Get current state.

        painter = QtGui.QPainter(self)
        width, height = painter.device().width(), painter.device().height()
        rect = QtCore.QRect(0, 0, width, height)

        # QBrush to fill color
        brush = QtGui.QBrush()
        brush.setColor(self.colors[self.color_value])
        brush.setStyle(Qt.SolidPattern)

        # QPainterPath to draw rectangle oth round shape
        path = QtGui.QPainterPath()
        path.addRoundedRect(rect, 5, 5)
        painter.fillPath(path, brush)

        # icon window
        painter.drawPixmap(QtCore.QRect(width * 0.7, height / 4, width * 0.21, height * 0.64), QPixmap(self.icon))

        # setting the text attributes though Qpen
        pen = painter.pen()
        pen.setColor(self.color_text)
        pen.setWidthF(3)
        painter.setPen(pen)
        font = painter.font()
        font.setFamily("Serif")
        # text relative size to the window
        font.setPointSize((width + height) / 20)
        painter.setFont(font)

        painter.drawText(QtCore.QRect(10, 10, width, height), "{},\n{}  {}".format(self.text, self.value,self.text_unit))
        painter.end()


    def _trigger_refresh(self):
        self.update()


class NotificationWidget(QtWidgets.QWidget):
    def __init__(self, color="#f54242", color_text='blue', text='new text', size_text=1, icon=None, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.size_text = size_text
        self.color_text = color_text
        self.text = text
        self.color = color
        self.icon = icon
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed,
        )

    def sizeHint(self):
        return QtCore.QSize(220, 350)

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        width, height = painter.device().width(), painter.device().height()
        rect = QtCore.QRect(0, 0, width, height)

        # QBrush to fill color
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(self.color))
        brush.setStyle(Qt.SolidPattern)

        # QPainterPath to draw rectangle oth round shape
        path = QtGui.QPainterPath()
        path.addRoundedRect(rect, 5, 5)
        painter.fillPath(path, brush)

        # icon window
        # painter.drawPixmap(QtCore.QRect(width * 0.7, height / 4, width * 0.21, height * 0.64), QPixmap(self.icon))

        # setting the text attributes though Qpen
        pen = painter.pen()
        pen.setColor(QtGui.QColor(self.color_text))
        pen.setWidthF(3)
        painter.setPen(pen)
        font = painter.font()
        font.setFamily("Serif")
        # text relative size to the window
        font.setPointSize((width + height) * self.size_text / 20)
        painter.setFont(font)

        painter.drawText(QtCore.QRect(10, 10, width, height), "{}".format(self.text))
        painter.end()

    def _trigger_refresh(self):
        self.update()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = Add()

    win.show()
    app.exec_()
