from bytecore.replay_register import ReplayRegister
from bytecore.register import Register
from bytecore.byte import Byte


class ProxyRegister:
    def __init__(self, replay_register: ReplayRegister, subject: Register) -> None:
        self._replay_register = replay_register
        self._subject = subject

    def write_high(self) -> None:
        self._replay_register.set_subject(self._subject).write_high()

    def write_low(self) -> None:
        self._replay_register.set_subject(self._subject).write_low()

    def read_high(self) -> None:
        self._replay_register.set_subject(self._subject).read_high()

    def read_low(self) -> None:
        self._replay_register.set_subject(self._subject).read_low()

    def get_bus(self) -> Byte:
        return self._replay_register.set_subject(self._subject).get_bus()

    def set_bus(self, value: Byte) -> None:
        self._replay_register.set_subject(self._subject).set_bus(value)

    def dump(self) -> Byte:
        return self._subject.dump()
