from bytecore.register import Register
from bytecore.constant_register import ConstantRegister
from bytecore.memory import Memory
from bytecore.byte import Byte
from bytecore.bit import Bit


class Accumulator:
    def __init__(self,
                 accumulator: Register,
                 temp_register: Register,
                 memory: Memory,
                 pc_msb_register: Register,
                 pc_lsb_register: Register,
                 increment_register: ConstantRegister) -> None:
        self._accumulator = accumulator
        self._temp_register = temp_register
        self._memory = memory
        self._pc_msb_register = pc_msb_register
        self._pc_lsb_register = pc_lsb_register
        self._increment_register = increment_register

        self._overflow_flag = Bit.LOW
        self._zero_flag = Bit.LOW

        self._check_if_accumulator_is_zero()

    def increment_pc_msb_register(self) -> None:
        self._pc_msb_register.read_high()
        msb_byte = self._pc_msb_register.get_bus()
        self._pc_msb_register.read_low()

        self._increment_register.read_high()
        increment_byte = self._increment_register.get_bus()
        self._increment_register.read_low()

        self._pc_msb_register.write_high()
        self._pc_msb_register.set_bus(
            self._byte_adder_helper(increment_byte, msb_byte))
        self._pc_msb_register.write_low()

    def increment_pc_lsb_register(self) -> None:
        self._pc_lsb_register.read_high()
        lsb_byte = self._pc_lsb_register.get_bus()
        self._pc_lsb_register.read_low()

        self._increment_register.read_high()
        increment_byte = self._increment_register.get_bus()
        self._increment_register.read_low()

        self._pc_lsb_register.write_high()
        self._pc_lsb_register.set_bus(
            self._byte_adder_helper(increment_byte, lsb_byte))
        self._pc_lsb_register.write_low()

    def add_memory_to_accumulator(self) -> None:
        self._temp_register.read_high()
        temp = self._temp_register.get_bus()
        self._temp_register.read_low()

        self._memory.read_high()
        memory = self._memory.get_bus()
        self._memory.read_low()

        result = self._byte_adder_helper(temp, memory)

        self.write_high()
        self.set_bus(result)
        self.write_low()

    def sub_memory_from_accumulator(self) -> None:
        self._temp_register.read_high()
        temp = self._temp_register.get_bus()
        self._temp_register.read_low()

        self._memory.read_high()
        memory = self._memory.get_bus()
        self._memory.read_low()

        result = self._byte_subtractor_helper(temp, memory)

        self.write_high()
        self.set_bus(result)
        self.write_low()

    def write_high(self) -> None:
        self._accumulator.write_high()

    def write_low(self) -> None:
        self._accumulator.write_low()

    def read_high(self) -> None:
        self._accumulator.read_high()

    def read_low(self) -> None:
        self._accumulator.read_low()

    def get_bus(self) -> Byte:
        return self._accumulator.get_bus()

    def set_bus(self, value: Byte) -> None:
        self._accumulator.set_bus(value)
        self._check_if_accumulator_is_zero()

    def get_overflow_flag(self) -> Bit:
        return self._overflow_flag

    def _set_overflow_flag(self) -> None:
        self._overflow_flag = Bit.HIGH

    def _reset_overflow_flag(self) -> None:
        self._overflow_flag = Bit.LOW

    def get_zero_flag(self) -> Bit:
        return self._zero_flag

    def _set_zero_flag(self) -> None:
        self._zero_flag = Bit.HIGH

    def _reset_zero_flag(self) -> None:
        self._zero_flag = Bit.LOW

    def dump(self) -> Byte:
        return self._accumulator.dump()

    def _byte_adder_helper(self, left: Byte, right: Byte) -> Byte:
        value = left.value + right.value
        if value > Byte.MAX_VALUE:
            self._set_overflow_flag()
            return Byte(value - Byte.COUNT_VALUES)
        self._reset_overflow_flag()
        return Byte(value)

    def _byte_subtractor_helper(self, left: Byte, right: Byte) -> Byte:
        value = left.value - right.value
        if value < Byte.MIN_VALUE:
            self._set_overflow_flag()
            return Byte(value + Byte.COUNT_VALUES)
        self._reset_overflow_flag()
        return Byte(value)

    def _check_if_accumulator_is_zero(self) -> None:
        if self._accumulator.dump() == Byte.DEFAULT_BYTE:
            self._set_zero_flag()
            return
        self._reset_zero_flag()
