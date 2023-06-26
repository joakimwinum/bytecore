from bytecore.byte import Byte
from bytecore.bit import Bit
from bytecore.register import Register
from bytecore.constant_register import ConstantRegister


class ByteRegister:
    def __init__(self) -> None:
        self._byte: Byte = Byte.DEFAULT_BYTE
        self._read: Bit = Bit.LOW
        self._write: Bit = Bit.LOW

    @staticmethod
    def init_register_with_byte(byte: Byte) -> Register:
        register = ByteRegister()
        register._byte = byte
        return register

    @staticmethod
    def init_constant_register_with_byte(byte: Byte) -> ConstantRegister:
        return ByteRegister.init_register_with_byte(byte)

    def write_high(self) -> None:
        self._write = Bit.HIGH

    def write_low(self) -> None:
        self._write = Bit.LOW

    def read_high(self) -> None:
        self._read = Bit.HIGH

    def read_low(self) -> None:
        self._read = Bit.LOW

    def _get_byte(self) -> Byte:
        if self._read is Bit.LOW:
            return Byte.DEFAULT_BYTE
        return self._byte

    def _set_byte(self, value: Byte) -> None:
        if self._write is Bit.LOW:
            return
        self._byte = value

    @property
    def _value(self) -> Byte:
        return self._get_byte()

    @_value.setter
    def _value(self, value: Byte) -> None:
        self._set_byte(value)

    def get_decimal(self) -> int:
        return self._value.value

    def get_binary(self) -> str:
        return ('00000000' + bin(self._value.value)[2:])[-8:]

    def get_hex(self) -> str:
        return ('00' + hex(self._value.value)[2:].upper())[-2:]

    def get_bus(self) -> Byte:
        return self._value

    def set_bus(self, value: Byte) -> None:
        self._value = value

    def dump(self) -> Byte:
        return self._byte
