from RedoxFlowProject.QtController.helper import ErrorMassage, PortManger,\
 ModbusBuilder, Pump
import serial
import time
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QSize, Qt, QRunnable, Slot



class PumpConnectionManger:
    """
    this class manage the connection of the Pumps though the usb Ports, send the message
    with update connection method
    """
    # def __init__(self):
    #     self.update_connection()

    def send_pump(self, data, send_to):
        if self.update_connection() != False:
                
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
        self.serial.write(data)
        time.sleep(0.012)
        self.serial.close()


    def update_connection(self):
        self.maste_pump_port = None
        self.second_pump_port = None
        if PortManger().get_number_of_pump_connected == 2:
            self.maste_pump_port = PortManger().get_master_pump_port
            self.second_pump_port = PortManger().get_second_pump_port
        elif PortManger().get_number_of_pump_connected == 1:
            self.maste_pump_port = PortManger().get_master_pump_port

        else :
            ErrorMassage("Error", "No pump was found, please check you connections")
            return False


def find_my_pump(send_to):
    m = ModbusBuilder()
    p = PumpConnectionManger()
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
        p = PumpConnectionManger()
        start_ = m.build_start().get_modbus
        stop_ = m.build_stop().get_modbus
        stop_ = m.build_stop().get_modbus
        p.send_pump(data=start_, send_to=send_to)
        speed_ = m.build_change_speed(start).get_modbus
        time.sleep(0.012)
        if abs(steps) != steps or abs(stop) != stop \
                or abs(start) != start or abs(duration) != duration :
            steps = abs(steps)
            stop = abs(stop)
            start = abs(start)
            duration = abs(duration)

        if  start > stop:
            stop = stop-1
            steps = - steps
        elif start < stop:
            stop = stop+1
        for i in range(start, stop, steps):
            speed_ = m.build_change_speed(i).get_modbus
            p.send_pump(data=speed_, send_to=send_to)
            time.sleep(duration)



if __name__ == "__main__":
    m = ModbusBuilder()
    p = PumpConnectionManger()
    start_ = m.build_start().get_modbus
    stop_ = m.build_stop().get_modbus
    speed_ = m.build_change_speed(10).get_modbus
    p.send_pump(data=speed_, send_to=Pump.MASTER)
    time.sleep(0.2)
    # p.send_pump(data=start_,send_to=Pump.MASTER)
    # time.sleep(0.2)
    # p.send_pump(data=stop_, send_to=Pump.MASTER)
    # step_increase(5, 24, 5, 1, Pump.BOTH)


