
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow, QMessageBox
from serial.tools import list_ports as ports
from enum import Enum
from RedoxFlowProject.main_new_ui.modbus import ModbusBuilder
import serial
import time

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QSize, Qt, QRunnable, Slot

class PumpMode(Enum):
    COUPLED = 0
    DECOUPLED = 1


class Pump(Enum):
    MASTER = 1
    SECOND = 2
    BOTH = 0


class PortManger:
    """
    this is port manger to check how many pumps are connected and return the specific port for each pump
    """

    def __init__(self, s="USB-SERIAL CH340"):
        self.__port = [str(i) for i in ports.comports(include_links=False)]
        self.__s = s

    @property
    def get_ports_list(self):
        return self.__port

    @property
    def get_all_pump_ports_list(self):
        return [self.get_master_pump_port, self.get_second_pump_port]

    @property
    def get_master_pump_port(self):
        for _ in self.__port:
            if self.__s in _:
                return _[_.find("(") + 1:-1]
        return None

    @property
    def get_master_pump_port_name_raw(self):
        for _ in self.__port:
            if self.__s in _:
                return _
        return None

    def get_second_pump_port_name_raw(self):
        p = []
        for _ in self.__port:
            if self.__s in _:
                p.append(_)
            if len(p) > 1:
                return p[2]
        return None

    @property
    def get_number_of_pump_connected(self):
        num = []
        for _ in self.__port:
            if self.__s in _:
                num.append(_)
        return len(num)

    @property
    def get_second_pump_port(self):
        num = []
        for _ in self.__port:
            if self.__s in _:
                num.append(_)
        if len(num) > 1:
            return num[1][num[1].find("(") + 1:-1]
        return None


class ErrorMassage(QMainWindow):
    """error handler for general use """

    def __init__(self, title, message):
        super().__init__()
        self.setWindowIcon(QIcon(r"../QtIcons/warning.png"))
        self.title = title
        self.message = message
        QMessageBox.warning(self, self.title, self.message)


class PumpModbusCommandSender:
    """
    this class manage the connection of the Pumps though the usb Ports, send the message
    with update connection method
    """

    def __init__(self):
        self.ModbusBuilder = ModbusBuilder()
        self.start = self.ModbusBuilder.build_start()
        self.stop = self.ModbusBuilder.build_stop()
        self.speed = self.ModbusBuilder.build_change_speed(1)
        self.direction_cc = self.ModbusBuilder.build_flow_direction("cw")
        self.direction_ccw = self.ModbusBuilder.build_flow_direction("ccw")

    def send_pump(self, data, send_to):
        if self._update_connection():

            if send_to == Pump.MASTER:
                self._write_s(self.maste_pump_port, data)

            elif send_to == Pump.SECOND:
                self._write_s(self.second_pump_port, data)

            elif send_to == Pump.BOTH:
                self._write_s(self.maste_pump_port, data)
                self._write_s(self.second_pump_port, data)

    def _write_s(self, port, data):
        self.serial = serial.Serial(baudrate=9600, timeout=0.005, bytesize=8, stopbits=2,
                                    parity=serial.PARITY_NONE)

        self.serial.port = port
        self.serial.open()
        # with self.serial as s:
        #     s.write(data)
        self.serial.write(data)
        time.sleep(0.012)
        self.serial.close()

    def _update_connection(self):
        self.maste_pump_port = None
        self.second_pump_port = None
        if PortManger().get_number_of_pump_connected == 2:
            self.maste_pump_port = PortManger().get_master_pump_port
            self.second_pump_port = PortManger().get_second_pump_port
        elif PortManger().get_number_of_pump_connected == 1:
            self.maste_pump_port = PortManger().get_master_pump_port

        else:
            ErrorMassage("Error", "No pump was found, please check you connections")
            return False


def find_my_pump(send_to):
    m = ModbusBuilder()
    p = PumpModbusCommandSender()
    start_ = m.build_start().get_modbus
    stop_ = m.build_stop().get_modbus
    speed_ = m.build_change_speed(30).get_modbus
    p.send_pump(data=speed_, send_to=send_to)
    time.sleep(0.1)
    p.send_pump(data=start_, send_to=send_to)
    time.sleep(0.2)
    p.send_pump(data=stop_, send_to=send_to)
    time.sleep(0.1)
    p.send_pump(data=start_, send_to=send_to)
    time.sleep(0.2)
    p.send_pump(data=stop_, send_to=send_to)


def step_increase(start, stop, steps, duration, send_to):
    m = ModbusBuilder()
    p = PumpModbusCommandSender()
    start_ = m.build_start().get_modbus
    stop_ = m.build_stop().get_modbus
    stop_ = m.build_stop().get_modbus
    p.send_pump(data=start_, send_to=send_to)
    speed_ = m.build_change_speed(start).get_modbus
    time.sleep(0.012)
    if abs(steps) != steps or abs(stop) != stop \
            or abs(start) != start or abs(duration) != duration:
        steps = abs(steps)
        stop = abs(stop)
        start = abs(start)
        duration = abs(duration)

    if start > stop:
        stop = stop - 1
        steps = - steps
    elif start < stop:
        stop = stop + 1
    for i in range(start, stop, steps):
        speed_ = m.build_change_speed(i).get_modbus
        p.send_pump(data=speed_, send_to=send_to)
        time.sleep(duration)


if __name__ == "__main__":
    m = ModbusBuilder()
    p = PumpModbusCommandSender()
    start_ = m.build_start().get_modbus
    stop_ = m.build_stop().get_modbus
    speed_ = m.build_change_speed(30).get_modbus

    # time.sleep(0.2)

    p.send_pump(data=stop_, send_to=Pump.MASTER)

    # p.send_pump(data=s,send_to=Pump.MASTER)
    # time.sleep(0.2)
    # p.send_pump(data=stop_, send_to=Pump.MASTER)
    # step_increase(5, 24, 5, 1, Pump.BOTH)

