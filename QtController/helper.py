from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow, QMessageBox
from serial.tools import list_ports as ports
from enum import Enum


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


class IS(Enum):
    UNI = 1
    DUAL_CLONE = 2
    DUAL_CUSTOM = 3


class Pump(Enum):
    MASTER = 1
    SECOND = 2
    BOTH = 0


class MasterSend:
    def __init__(self):
        self.start_stop = Pump.MASTER
        self.direction = Pump.MASTER
        self.speed = Pump.MASTER


class Type:
    def __init__(self):
        self.start_stop = IS.UNI
        self.direction = IS.UNI
        self.speed = IS.UNI


class MasterValues:
    def __init__(self):
        self.start_stop = None
        self.direction = "cw"
        self.speed = 0
        self.speed_list = [0]


class SecondValues:
    def __init__(self):
        self.start_stop = None
        self.direction = "cw"
        self.speed = 0
        self.speed_list = [0]


def xor(a, b):
    """
    this function replicate the XOR operation
    """
    if a != b:
        return "1"
    else:
        return "0"


class DataConverting:
    """
    this class for converting from/to hex, binary, decimal
    """
    def __init__(self, number=None):
        self.number = number

    def bin_to_hex(self):
        return hex(int(self.number, 2))[2:]

    def hex_to_bin(self, n_bits=8):
        return bin(int(self.number, 16))[2:].zfill(n_bits)

    def dec_to_hex(self):
        return hex(int(self.number, 10))[2:]

    def hex_to_dec(self):
        return int(self.number, 16)

    def bin_to_dec(self):
        return int(self.number, 2)

    def dec_to_bin(self, n_bits=8):
        return bin(int(self.number, 10))[2:].zfill(n_bits)


def ieee754_converter(float_num):
    """
    this function converts form float to Single-precision floating-point format
    """
    sign = "0"
    if abs(float_num) != float_num:  # check the sign
        sign = "1"
        float_num = abs(float_num)

    integer = str(int(float_num))
    fraction = float_num - int(integer)
    mantissa = DataConverting(integer).dec_to_bin(n_bits=0)
    exponent = DataConverting(number=str(127 + len(mantissa[1:]))).dec_to_bin(n_bits=8)

    for i in range(23 - len(mantissa[1:])):  # converting the decimal part to a binary
        fraction *= 2
        if int(fraction) == 0:
            mantissa += "0"
        elif int(fraction) > 0:
            mantissa += "1"
            fraction -= int(fraction)

    iee_code = DataConverting(sign + exponent + mantissa[1:]).bin_to_hex()

    return iee_code.upper()


class CRCGenerator:
    """
        def generate(self):  # this function generates a crc code for a given message
        crc = list("1" * 16)  # 16 bits register into hexadecimal FFFF
        polynomial = "1010000000000001"   Polynomial: G(X)=X16+X15+X2+1
    """
    def __init__(self, message=None):
        self.crc = None
        self.message = message
        self.full_code = None

    @property
    def generate(self):  # this function generates a crc code for a given message
        crc = list("1" * 16)  # 16 bits register into hexadecimal FFFF
        polynomial = "1010000000000001"  # Polynomial: G(X)=X16+X15+X2+1

        # converting each two bit in the message from hex to binary
        message_hex_2bit = [DataConverting(self.message[i:i + 2]).hex_to_bin(8) for i in range(0, len(self.message), 2)]

        # the outer loop to iterate each 8 bit in the message
        for i in message_hex_2bit:

            # the first inner iteration for XOR crc initial value and the fist 8 bits of the message
            for index, bit in enumerate(i):
                crc[index + 8] = xor(bit, crc[index + 8])

            # the second inner iteration for 8 shifts
            for _ in range(8):
                if crc[-1] == "1":
                    crc = ["0"] + crc[:15]
                    for index, bit in enumerate(polynomial):
                        crc[index] = xor(bit, crc[index])
                else:
                    crc = ["0"] + crc[:15]

        crc = list(DataConverting("".join(crc)).bin_to_hex())
        self.crc = "".join(crc[2:] + crc[:2]).upper()
        self.full_code = self.message + self.crc
        return self

    def get_crc_code(self):
        return self.change_format(self.crc)

    def get_full_code(self):
        return self.change_format(self.full_code)

    @staticmethod
    def change_format(x):
        """
        the purpose of this static method is to change the message to a Hexadecimal bytearray format acceptable
         by pyserial and python (MODBUS)
         """

        decimal = [int(DataConverting(x[i:i + 2]).hex_to_dec()) for i in range(0, len(x), 2)]
        return bytearray(decimal)
        # ----------------------------

    def __str__(self):
        return f"message = {self.message}\nCRC code = {self.crc}\nfull code = {self.full_code}"


class ModbusBuilder:
    """
    this class responsible of constructing the message for Pump lab s1 with crc code and prepare it to be send
    """
    def __init__(self):
        self.__slave_address = "01"
        self._function_code_int = "06"
        self._function_code_float = "10"
        self._register_address = {"start_stop": "03E8", "Running_direction": "03E9", "speed": "03EA"}
        self._The_number_of_register = "0002"  # float only
        self.data = {"start": "0001", "stop": "0000", "cw": "0001", "ccw": "0000"}
        self._the_number_of_bit = "04"
        self.modbus = None

    def build_start(self):
        message = f"{self.__slave_address}{self._function_code_int}" \
                  f"{self._register_address['start_stop']}{self.data['start']}"
        self.modbus = CRCGenerator(message).generate.get_full_code()  # generating the crc code
        return self

    def build_stop(self):
        message = f"{self.__slave_address}{self._function_code_int}" \
                  f"{self._register_address['start_stop']}{self.data['stop']}"
        self.modbus = CRCGenerator(message).generate.get_full_code()  # generating the crc code
        return self

    def build_flow_direction(self, direction: object = "cc") -> object:
        message = f"{self.__slave_address}{self._function_code_int}" \
                  f"{self._register_address['Running_direction']}{self.data[direction]}"
        self.modbus = CRCGenerator(message).generate.get_full_code()  # generating the crc code
        return self

    def build_change_speed(self, new_speed=0):
        data = ieee754_converter(new_speed)  # converting to IEEE754
        message = f"{self.__slave_address}{self._function_code_float}" \
                  f"{self._register_address['speed']}{self._The_number_of_register}" \
                  f"{self._the_number_of_bit}{data}"
        self.modbus = CRCGenerator(message).generate.get_full_code()  # generating the crc code
        return self

    @property
    def get_modbus(self):
        return self.modbus

    def __str__(self):
        return f" current message {str(self.modbus)}"


if __name__ == "__main__":

    my_port = PortManger()
    print(my_port.get_master_pump_port)

    p = ModbusBuilder()
    print(p.build_start())
