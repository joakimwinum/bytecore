from bytecore.bit import Bit


class Byte:
    MIN_VALUE: int = 0
    MAX_VALUE: int = 255
    COUNT_VALUES: int = 256
    DEFAULT_BYTE: 'Byte'

    _hex_characters = {'0', '1', '2', '3', '4', '5',
                       '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'}

    _bytes: dict[int, 'Byte'] = {}

    def __new__(cls, value: int) -> 'Byte':
        if not cls.MIN_VALUE <= value <= cls.MAX_VALUE:
            raise ValueError
        if value not in cls._bytes:
            cls._bytes[value] = super().__new__(cls)
        return cls._bytes[value]

    def __init__(self, value: int):
        self._value = value

    @staticmethod
    def from_bit(bit: Bit) -> 'Byte':
        return Byte(bit.value)

    @staticmethod
    def from_hex(hex_value: str) -> 'Byte':
        if len(hex_value) != 2:
            raise ValueError
        for hex_character in hex_value:
            if hex_character.upper() not in Byte._hex_characters:
                raise ValueError
        return Byte(int(hex_value, 16))

    @property
    def value(self) -> int:
        return self._value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Byte):
            return NotImplemented
        return self.value == other.value

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Byte):
            return NotImplemented
        return self.value != other.value

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Byte):
            return NotImplemented
        return self.value < other.value

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Byte):
            return NotImplemented
        return self.value <= other.value

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Byte):
            return NotImplemented
        return self.value > other.value

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Byte):
            return NotImplemented
        return self.value >= other.value

    def __repr__(self) -> str:
        return 'B' + str(self._value)


Byte.DEFAULT_BYTE = Byte(Byte.MIN_VALUE)
