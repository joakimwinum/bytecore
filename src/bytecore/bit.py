class Bit:
    MIN_VALUE: int = 0
    MAX_VALUE: int = 1
    COUNT_VALUES: int = 2
    DEFAULT_BIT: 'Bit'
    LOW: 'Bit'
    HIGH: 'Bit'

    _bits: dict[int, 'Bit'] = {}

    def __new__(cls, value: int) -> 'Bit':
        if not cls.MIN_VALUE <= value <= cls.MAX_VALUE:
            raise ValueError
        if value not in cls._bits:
            cls._bits[value] = super().__new__(cls)
        return cls._bits[value]

    def __init__(self, value: int):
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bit):
            return self.value == other.value
        return False


Bit.DEFAULT_BIT = Bit(Bit.MIN_VALUE)
Bit.LOW = Bit(Bit.MIN_VALUE)
Bit.HIGH = Bit(Bit.MAX_VALUE)
