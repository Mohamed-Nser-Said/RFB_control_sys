def xor(a, b):  # this function replicate the XOR operation
    if a != b:
        return "1"
    else:
        return "0"


class DataConverting:  # this class for converting from/to hex, binary, decimal

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


def ieee754_converter(float_num):  # this function converts form float to Single-precision floating-point format
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
    def change_format(x):  # the purpose to change the message to a format acceptable by pump (MODBUS) **not finished**
        # print(x)
        # value = [x[i:i + 2] for i in range(0, len(x), 2)]
        # return [f"0x{i}" for i in value]
        # # ---------------------------

        decimal = [int(DataConverting(x[i:i + 2]).hex_to_dec()) for i in range(0, len(x), 2)]
        t = bytearray(decimal)
        return t
        # ----------------------------

    def __str__(self):
        return f"message = {self.message}\nCRC code = {self.crc}\nfull code = {self.full_code}"

