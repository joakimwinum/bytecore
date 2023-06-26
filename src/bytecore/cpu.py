from bytecore.memory import Memory
from bytecore.register import Register
from bytecore.accumulator import Accumulator
from bytecore.byte_register import ByteRegister
from bytecore.byte import Byte
from bytecore.state import State
from bytecore.control_unit import ControlUnit
from bytecore.control_unit_state import ControlUnitState


class Cpu:
    def __init__(self,
                 memory: Memory,
                 accumulator: Register,
                 pc_msb_register: Register,
                 pc_lsb_register: Register,
                 temp_register: Register,
                 mar_msb_register: Register,
                 mar_lsb_register: Register) -> None:
        self._memory = memory
        self._increment_register = ByteRegister.init_constant_register_with_byte(
            Byte(1))

        self._accumulator = Accumulator(accumulator,
                                        temp_register,
                                        memory,
                                        pc_msb_register,
                                        pc_lsb_register,
                                        self._increment_register)

        self._pc_msb_register = pc_msb_register
        self._pc_lsb_register = pc_lsb_register
        self._temp_register = temp_register
        self._mar_msb_register = mar_msb_register
        self._mar_lsb_register = mar_lsb_register

        self._control_unit_state = ControlUnitState()

        self._control_unit = ControlUnit(memory,
                                         self._accumulator,
                                         pc_msb_register,
                                         pc_lsb_register,
                                         temp_register,
                                         mar_msb_register,
                                         mar_lsb_register,
                                         self._increment_register,
                                         self._control_unit_state)

    def step(self) -> None:
        self._control_unit.step_instruction_cycle()

    def cycle(self) -> None:
        self._control_unit.complete_instruction_cycle()

    def cycle_until_halt(self) -> None:
        self._control_unit.complete_instruction_cycles_until_halt()

    def dump(self) -> State:
        return State(self._memory,
                     self._accumulator,
                     self._pc_msb_register,
                     self._pc_lsb_register,
                     self._temp_register,
                     self._mar_msb_register,
                     self._mar_lsb_register,
                     self._control_unit_state)
