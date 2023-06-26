from typing import Protocol
from bytecore.byte import Byte


class ConstantRegister(Protocol):  # pragma: no cover
    def read_high(self) -> None:
        pass

    def read_low(self) -> None:
        pass

    def get_bus(self) -> Byte:
        pass

    def dump(self) -> Byte:
        pass
