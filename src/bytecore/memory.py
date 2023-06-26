from bytecore.byte_register import ByteRegister
from bytecore.register import Register
from bytecore.proxy_register import ProxyRegister
from bytecore.replay_register import ReplayRegister
from bytecore.byte import Byte


class Memory:
    CAPACITY_IN_BYTES = Byte.COUNT_VALUES * Byte.COUNT_VALUES

    def __init__(self, memory_bytes: list[Byte]) -> None:
        if len(memory_bytes) != Memory.CAPACITY_IN_BYTES:
            raise ValueError('Not a valid number of memory bytes.')

        self._address_msb_register: Register = ByteRegister()
        self._address_msb_register.read_high()
        self._address_lsb_register: Register = ByteRegister()
        self._address_lsb_register.read_high()

        self._replay_register = ReplayRegister()

        memory: list[list[Register]] = []
        register_row: list[Register] = []
        for byte in memory_bytes:
            if len(register_row) == Byte.COUNT_VALUES:
                memory.append(register_row)
                register_row = []
            register_row.append(ProxyRegister(
                self._replay_register, ByteRegister.init_register_with_byte(byte)))
        memory.append(register_row)
        self._memory = memory

    @staticmethod
    def get_default_memory_bytes() -> list[Byte]:
        return [Byte(0) for _ in range(Memory.CAPACITY_IN_BYTES)]

    def address_msb_write_high(self) -> None:
        self._address_msb_register.write_high()

    def address_msb_write_low(self) -> None:
        self._address_msb_register.write_low()

    def address_lsb_write_high(self) -> None:
        self._address_lsb_register.write_high()

    def address_lsb_write_low(self) -> None:
        self._address_lsb_register.write_low()

    def set_address_msb_bus(self, value: Byte) -> None:
        self._address_msb_register.set_bus(value)

    def set_address_lsb_bus(self, value: Byte) -> None:
        self._address_lsb_register.set_bus(value)

    def _get_current_register(self) -> Register:
        return self._memory[self._address_msb_register.get_bus().value][self._address_lsb_register.get_bus().value]

    def write_high(self) -> None:
        self._get_current_register().write_high()

    def write_low(self) -> None:
        self._get_current_register().write_low()

    def read_high(self) -> None:
        self._get_current_register().read_high()

    def read_low(self) -> None:
        self._get_current_register().read_low()

    def get_bus(self) -> Byte:
        return self._get_current_register().get_bus()

    def set_bus(self, value: Byte) -> None:
        self._get_current_register().set_bus(value)

    def dump(self) -> list[Byte]:
        return [register.dump() for register_row in self._memory for register in register_row]
