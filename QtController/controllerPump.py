from RedoxFlowProject.QtController.helper import ieee754_converter, CRCGenerator
import serial
from serial.tools import list_ports as ports
from enum import Enum
from PySide2.QtWidgets import QMainWindow, QWidget, QPushButton, QDialog, QMessageBox
from PySide2.QtGui import QIcon

class ErrorMassage(QMainWindow):
    """error handlear """
    def __init__(self,title, message):
        super().__init__()
        self.setWindowIcon(QIcon(r"../QtIcons/warning.png"))
        self.title = title
        self.message = message
        QMessageBox.warning(self, self.title, self.message)


class Error(Enum):
    PORT_OPENED = 1
    NO_CONNECTION = 2
    LOST_CONNECTION = 3


# instance of the serial class where all the Pump setting is defined in the initiation of the class
class PumpCommunicationSetting:
    """
    this class deals with the esablishing the comunication between the pump and the computer
    atumatic detection of the port, dealing with errors
    """
    def __init__(self):
        self.port_name = ""
        self.error_type = []

        self.port = [str(i) for i in ports.comports(include_links=False)]
        for _ in self.port:
            if "USB-SERIAL CH340" in _:
                self.port_state = True
                # the communication settings specifically for the pump lab s1
                self.ser = serial.Serial(baudrate=9600, timeout=1, bytesize=8, stopbits=2,
                                         parity=serial.PARITY_NONE)
                self.port_name = _[_.find("(") + 1:-1]
                self.ser.port = self.port_name

                try:
                    self.ser.open()

                except:
                    self.error_type.append(Error.PORT_OPENED)
                    ErrorMassage(Error.PORT_OPENED.name, Error.PORT_OPENED.name)
                    quit()
            else:
                self.port_state = False

    def __str__(self):
        return f"port setting {str(self.ser)}\n" \
               f"error info {'/'.join(self.error_type)}"


class PumpControl:
    """
    modbus message constructure  with send_data method for sending the modbus meassage to the pump
    """
    def __init__(self):
        self.communication = PumpCommunicationSetting()
        self.port_state = self.communication.port_state
        self.action = []
        self.__slave_address = "01"
        self._function_code_int = "06"
        self._function_code_float = "10"
        self._register_address = {"start_stop": "03E8", "Running_direction": "03E9", "speed": "03EA"}
        self._The_number_of_register = "0002"  # float only
        self.data = {"start": "0001", "stop": "0000", "cw": "0001", "ccw": "0000"}
        self._the_number_of_bit = "04"
        self.modbus = None

    def start(self):
        message = f"{self.__slave_address}{self._function_code_int}" \
                  f"{self._register_address['start_stop']}{self.data['start']}"
        self.modbus = CRCGenerator(message).generate.get_full_code()  # generating the crc code
        self.action.append(self.modbus)
        self.send_data()
        return self

    def stop(self):
        message = f"{self.__slave_address}{self._function_code_int}" \
                  f"{self._register_address['start_stop']}{self.data['stop']}"
        self.modbus = CRCGenerator(message).generate.get_full_code()  # generating the crc code
        self.action.append(self.modbus)
        self.send_data()
        return self

    def flow_direction(self, direction="cc"):
        message = f"{self.__slave_address}{self._function_code_int}" \
                  f"{self._register_address['Running_direction']}{self.data[direction]}"
        self.modbus = CRCGenerator(message).generate.get_full_code()  # generating the crc code
        self.action.append(self.modbus)
        self.send_data()
        return self

    def change_speed(self, new_speed=0):
        data = ieee754_converter(new_speed)  # converting to IEEE754
        message = f"{self.__slave_address}{self._function_code_float}" \
                  f"{self._register_address['speed']}{self._The_number_of_register}" \
                  f"{self._the_number_of_bit}{data}"
        self.modbus = CRCGenerator(message).generate.get_full_code()  # generating the crc code
        self.action.append(self.modbus)
        self.send_data()
        return self

    def send_data(self):
        if self.port_state:
            try:
                self.communication.ser.write(self.modbus)
                # self.communication.ser.close()
            except:
                self.communication.error_type.append(Error.LOST_CONNECTION)
                ErrorMassage(Error.LOST_CONNECTION.name, Error.LOST_CONNECTION.name)
        else:
            self.communication.error_type.append(Error.NO_CONNECTION)
            ErrorMassage(Error.NO_CONNECTION.name,Error.NO_CONNECTION.name)



    def __str__(self):
        return f" current message {str(self.modbus)}\n" \
               f" list of actions {str(self.action)}"


if __name__ == "__main__":
    p = PumpControl()

    p.stop()
    # p = pump.start().change_speed(232).flow_direction("ccw").stop()
    # p = pump.start().change_speed(212.34).flow_direction("cw").stop()
    # print(p)

    # new_modbus =[]
    # start = ['01', '06', '03', 'E8', '00', '01', 'C8', '7A']
    # ccw = ['01', '06', '03', 'E9', '00', '00', '58', '7A']
    # for i in ccw:
    #     #new_modbus.append("0"+DataConverting(i).hex_to_bin()+"11")
    #     new_modbus.append("0" + DataConverting(i).hex_to_bin()[::-1] + "1")
    #     print(new_modbus)
    # new_modbus = "".join(new_modbus)
    # new_modbus = "1"*28 + new_modbus + "1"*28
    # print(new_modbus)
