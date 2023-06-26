from bytecore.register import Register
from typing import Optional
from bytecore.byte import Byte
from bytecore.bit import Bit


class ReplayRegister:
    def __init__(self) -> None:
        self._subject: Optional[Register] = None
        self._read: Bit = Bit.LOW
        self._write: Bit = Bit.LOW

    def set_subject(self, subject: Register) -> 'ReplayRegister':
        self._subject = subject
        return self

    def _eject_subject(self) -> None:
        self._subject = None

    def _get_subject(self) -> Register:
        if self._subject is None:
            raise MissingSubject()
        return self._subject

    def write_high(self) -> None:
        self._write = Bit.HIGH
        self._eject_subject()

    def write_low(self) -> None:
        self._write = Bit.LOW
        self._eject_subject()

    def read_high(self) -> None:
        self._read = Bit.HIGH
        self._eject_subject()

    def read_low(self) -> None:
        self._read = Bit.LOW
        self._eject_subject()

    def _replay_read(self) -> None:
        if self._read is Bit.HIGH:
            self._get_subject().read_high()
        else:
            self._get_subject().read_low()

    def _replay_write(self) -> None:
        if self._write is Bit.HIGH:
            self._get_subject().write_high()
        else:
            self._get_subject().write_low()

    def _replay(self) -> None:
        self._replay_read()
        self._replay_write()

    def replay(self) -> None:
        self._replay()
        self._eject_subject()

    def get_bus(self) -> Byte:
        self._replay()
        bus_value = self._get_subject().get_bus()
        self._eject_subject()
        return bus_value

    def set_bus(self, value: Byte) -> None:
        self._replay()
        self._get_subject().set_bus(value)
        self._eject_subject()


class MissingSubject(Exception):
    def __init__(self) -> None:
        self.message = 'Missing Subject'
        super().__init__(self.message)
