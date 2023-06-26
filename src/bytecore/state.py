from bytecore.memory import Memory
from bytecore.register import Register
from bytecore.byte import Byte
from bytecore.control_unit_state import ControlUnitState


class State:
    def __init__(self,
                 memory: Memory,
                 accumulator: Register,
                 pc_msb_register: Register,
                 pc_lsb_register: Register,
                 temp_register: Register,
                 mar_msb_register: Register,
                 mar_lsb_register: Register,
                 control_unit_state: ControlUnitState) -> None:

        self.memory: list[Byte] = memory.dump()
        self.accumulator: Byte = accumulator.dump()
        self.pc_msb_register: Byte = pc_msb_register.dump()
        self.pc_lsb_register: Byte = pc_lsb_register.dump()
        self.temp_register: Byte = temp_register.dump()
        self.mar_msb_register: Byte = mar_msb_register.dump()
        self.mar_lsb_register: Byte = mar_lsb_register.dump()

        self.opcode: Byte = control_unit_state.opcode
        self.cycle_step: Byte = control_unit_state.cycle_step
        self.is_halt: Byte = Byte.from_bit(control_unit_state.is_halt)
