from typing import Protocol
from bytecore.byte import Byte


class Register(Protocol):  # pragma: no cover
    def write_high(self) -> None:
        pass

    def write_low(self) -> None:
        pass

    def read_high(self) -> None:
        pass

    def read_low(self) -> None:
        pass

    def get_bus(self) -> Byte:
        pass

    def set_bus(self, value: Byte) -> None:
        pass

    def dump(self) -> Byte:
        pass
