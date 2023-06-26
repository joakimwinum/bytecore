from bytecore.memory import Memory
from bytecore.register import Register
from bytecore.constant_register import ConstantRegister
from bytecore.byte import Byte
from bytecore.opcode import Opcode
from bytecore.control_unit_state import ControlUnitState
from bytecore.bit import Bit
from bytecore.accumulator import Accumulator


class ControlUnit:
    STEP_FETCH = Byte(0)
    STEP_DECODE = Byte(1)
    STEP_EVALUATE_ADDRESS_MSB = Byte(2)
    STEP_FETCH_OPERAND_MSB = Byte(3)
    STEP_EVALUATE_ADDRESS_LSB = Byte(4)
    STEP_FETCH_OPERAND_LSB = Byte(5)
    STEP_EXECUTE = Byte(6)
    STEP_STORE_RESULT = Byte(7)
    STEP_INCREMENT_PC = Byte(8)

    def __init__(self,
                 memory: Memory,
                 accumulator: Accumulator,
                 pc_msb_register: Register,
                 pc_lsb_register: Register,
                 temp_register: Register,
                 mar_msb_register: Register,
                 mar_lsb_register: Register,
                 increment_register: ConstantRegister,
                 control_unit_state: ControlUnitState) -> None:
        self._memory = memory
        self._accumulator = accumulator
        self._pc_msb_register = pc_msb_register
        self._pc_lsb_register = pc_lsb_register
        self._temp_register = temp_register
        self._mar_msb_register = mar_msb_register
        self._mar_lsb_register = mar_lsb_register
        self._increment_register = increment_register
        self._control_unit_state = control_unit_state

    def step_instruction_cycle(self) -> None:
        self._execute_instruction_step()
        self._increment_instruction_counter()

    def _execute_instruction_step(self) -> None:
        if self._control_unit_state.cycle_step == ControlUnit.STEP_FETCH:
            self._fetch()
        elif self._control_unit_state.cycle_step == ControlUnit.STEP_DECODE:
            self._decode()
        elif self._control_unit_state.cycle_step == ControlUnit.STEP_EVALUATE_ADDRESS_MSB:
            self._evaluate_address_msb()
        elif self._control_unit_state.cycle_step == ControlUnit.STEP_FETCH_OPERAND_MSB:
            self._fetch_operand_msb()
        elif self._control_unit_state.cycle_step == ControlUnit.STEP_EVALUATE_ADDRESS_LSB:
            self._evaluate_address_lsb()
        elif self._control_unit_state.cycle_step == ControlUnit.STEP_FETCH_OPERAND_LSB:
            self._fetch_operand_lsb()
        elif self._control_unit_state.cycle_step == ControlUnit.STEP_EXECUTE:
            self._execute()
        elif self._control_unit_state.cycle_step == ControlUnit.STEP_STORE_RESULT:
            self._store_result()
        elif self._control_unit_state.cycle_step == ControlUnit.STEP_INCREMENT_PC:
            self._increment_pc()

    def _increment_instruction_counter(self) -> None:
        self._control_unit_state.cycle_step = self._increment_byte_helper(
            self._control_unit_state.cycle_step)
        if self._control_unit_state.cycle_step > Byte(8):
            self._control_unit_state.cycle_step = Byte(0)

    def _increment_byte_helper(self, byte: Byte) -> Byte:
        return Byte(byte.value + 1)

    def complete_instruction_cycle(self) -> None:
        while True:
            self.step_instruction_cycle()
            if self._control_unit_state.cycle_step == Byte(0):
                break

    def complete_instruction_cycles_until_halt(self) -> None:
        while True:
            self.complete_instruction_cycle()
            if self._control_unit_state.is_halt == Bit.HIGH:
                break

    def _fetch(self) -> None:
        self._move_pc_to_memory_address()
        self._fetch_opcode_from_memory()

    def _move_pc_to_memory_address(self) -> None:
        # PC MSB
        self._memory.address_msb_write_high()
        self._pc_msb_register.read_high()

        self._memory.set_address_msb_bus(self._pc_msb_register.get_bus())

        self._memory.address_msb_write_low()
        self._pc_msb_register.read_low()

        # PC LSB
        self._memory.address_lsb_write_high()
        self._pc_lsb_register.read_high()

        self._memory.set_address_lsb_bus(self._pc_lsb_register.get_bus())

        self._memory.address_lsb_write_low()
        self._pc_lsb_register.read_low()

    def _fetch_opcode_from_memory(self) -> None:
        self._memory.read_high()

        self._control_unit_state.opcode = self._memory.get_bus()

        self._memory.read_low()

    def _decode(self) -> None:
        if self._control_unit_state.opcode == Opcode.HALT:
            self._control_unit_state.opcode = Opcode.HALT
        elif self._control_unit_state.opcode == Opcode.LOAD:
            self._control_unit_state.opcode = Opcode.LOAD
        elif self._control_unit_state.opcode == Opcode.STORE:
            self._control_unit_state.opcode = Opcode.STORE
        elif self._control_unit_state.opcode == Opcode.ADD:
            self._control_unit_state.opcode = Opcode.ADD
        elif self._control_unit_state.opcode == Opcode.SUB:
            self._control_unit_state.opcode = Opcode.SUB
        elif self._control_unit_state.opcode == Opcode.JMP:
            self._control_unit_state.opcode = Opcode.JMP
        elif self._control_unit_state.opcode == Opcode.JZ:
            self._control_unit_state.opcode = Opcode.JZ
        else:
            # HALT is set if the opcode is not recognized.
            self._control_unit_state.opcode = Opcode.HALT

    def _evaluate_address_msb(self) -> None:
        if self._control_unit_state.opcode == Opcode.HALT:
            return
        self._increment_pc_registers()
        self._move_pc_to_memory_address()

    def _increment_pc_registers(self) -> None:
        self._accumulator.increment_pc_lsb_register()
        if self._accumulator.get_overflow_flag() == Bit.HIGH:
            self._accumulator.increment_pc_msb_register()

    def _fetch_operand_msb(self) -> None:
        self._fetch_mar_msb_from_memory()

    def _fetch_mar_msb_from_memory(self) -> None:
        self._memory.read_high()
        self._mar_msb_register.write_high()

        self._mar_msb_register.set_bus(self._memory.get_bus())

        self._mar_msb_register.write_low()
        self._memory.read_low()

    def _evaluate_address_lsb(self) -> None:
        if self._control_unit_state.opcode == Opcode.HALT:
            return
        self._increment_pc_registers()
        self._move_pc_to_memory_address()

    def _fetch_operand_lsb(self) -> None:
        self._fetch_mar_lsb_from_memory()

    def _fetch_mar_lsb_from_memory(self) -> None:
        self._memory.read_high()
        self._mar_lsb_register.write_high()

        self._mar_lsb_register.set_bus(self._memory.get_bus())

        self._mar_lsb_register.write_low()
        self._memory.read_low()

    def _execute(self) -> None:
        if self._control_unit_state.opcode == Opcode.HALT:
            self._control_unit_state.is_halt = Bit.HIGH
            return
        elif self._control_unit_state.opcode == Opcode.LOAD:
            self._move_mar_to_memory_address()
            return
        elif self._control_unit_state.opcode == Opcode.STORE:
            self._move_mar_to_memory_address()
            return
        elif self._control_unit_state.opcode == Opcode.ADD:
            self._move_mar_to_memory_address()
            self._move_accumulator_to_temp()
            self._accumulator.add_memory_to_accumulator()
            return
        elif self._control_unit_state.opcode == Opcode.SUB:
            self._move_mar_to_memory_address()
            self._move_accumulator_to_temp()
            self._accumulator.sub_memory_from_accumulator()
            return
        elif self._control_unit_state.opcode == Opcode.JMP:
            return
        elif self._control_unit_state.opcode == Opcode.JZ:
            return

    def _move_mar_to_memory_address(self) -> None:
        # MAR MSB
        self._mar_msb_register.read_high()
        self._memory.address_msb_write_high()

        self._memory.set_address_msb_bus(self._mar_msb_register.get_bus())

        self._memory.address_msb_write_low()
        self._mar_msb_register.read_low()

        # MAR LSB
        self._mar_lsb_register.read_high()
        self._memory.address_lsb_write_high()

        self._memory.set_address_lsb_bus(self._mar_lsb_register.get_bus())

        self._memory.address_lsb_write_low()
        self._mar_lsb_register.read_low()

    def _move_accumulator_to_temp(self) -> None:
        self._accumulator.read_high()
        self._temp_register.write_high()

        self._temp_register.set_bus(self._accumulator.get_bus())

        self._temp_register.write_low()
        self._accumulator.read_low()

    def _store_result(self) -> None:
        if self._control_unit_state.opcode == Opcode.HALT:
            return
        if self._control_unit_state.opcode == Opcode.LOAD:
            self._move_memory_to_accumulator()
            return
        if self._control_unit_state.opcode == Opcode.STORE:
            self._move_accumulator_to_memory()
            return
        if self._control_unit_state.opcode == Opcode.ADD:
            return
        if self._control_unit_state.opcode == Opcode.SUB:
            return
        if self._control_unit_state.opcode == Opcode.JMP:
            self._move_mar_to_pc()
            return
        if self._control_unit_state.opcode == Opcode.JZ:
            if self._is_accumulator_zero():
                self._move_mar_to_pc()
            return

    def _move_memory_to_accumulator(self) -> None:
        self._memory.read_high()
        self._accumulator.write_high()

        self._accumulator.set_bus(self._memory.get_bus())

        self._accumulator.write_low()
        self._memory.read_low()

    def _move_accumulator_to_memory(self) -> None:
        self._accumulator.read_high()
        self._memory.write_high()

        self._memory.set_bus(self._accumulator.get_bus())

        self._memory.write_low()
        self._accumulator.read_low()

    def _move_mar_to_pc(self) -> None:
        # MAR MSB
        self._mar_msb_register.read_high()
        self._pc_msb_register.write_high()

        self._pc_msb_register.set_bus(self._mar_msb_register.get_bus())

        self._pc_msb_register.write_low()
        self._mar_msb_register.read_low()

        # MAR LSB
        self._mar_lsb_register.read_high()
        self._pc_lsb_register.write_high()

        self._pc_lsb_register.set_bus(self._mar_lsb_register.get_bus())

        self._pc_lsb_register.write_low()
        self._mar_lsb_register.read_low()

    def _is_accumulator_zero(self) -> bool:
        return self._accumulator.get_zero_flag() == Bit.HIGH

    def _increment_pc(self) -> None:
        if self._control_unit_state.opcode == Opcode.HALT:
            return
        if self._control_unit_state.opcode == Opcode.LOAD:
            self._increment_pc_registers()
            return
        if self._control_unit_state.opcode == Opcode.STORE:
            self._increment_pc_registers()
            return
        if self._control_unit_state.opcode == Opcode.ADD:
            self._increment_pc_registers()
            return
        if self._control_unit_state.opcode == Opcode.SUB:
            self._increment_pc_registers()
            return
        if self._control_unit_state.opcode == Opcode.JMP:
            return
        if self._control_unit_state.opcode == Opcode.JZ:
            if not self._is_accumulator_zero():
                self._increment_pc_registers()
