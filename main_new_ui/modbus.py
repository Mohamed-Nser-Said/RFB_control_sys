

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

    def build_flow_direction(self, direction: object = "cw") -> object:
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

    # my_port = PortManger()
    # print(my_port.get_master_pump_port)

    p = ModbusBuilder()
    print(p.build_start())
