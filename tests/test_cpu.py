from bytecore.memory import Memory
from bytecore.byte_register import ByteRegister
from bytecore.cpu import Cpu
from bytecore.state import State
from bytecore.byte import Byte
from bytecore.opcode import Opcode


class TestCpu:
    def test_dummy_test(self) -> None:
        # Arrange, act and assert
        assert 0 == 0

    def test__dump__after_init__returns_default_values(self) -> None:
        # Arrange
        memory = Memory(Memory.get_default_memory_bytes())
        accumulator = ByteRegister()
        pc_msb_register = ByteRegister()
        pc_lsb_register = ByteRegister()
        temp_register = ByteRegister()
        mar_msb_register = ByteRegister()
        mar_lsb_register = ByteRegister()
        cpu = Cpu(
            memory,
            accumulator,
            pc_msb_register,
            pc_lsb_register,
            temp_register,
            mar_msb_register,
            mar_lsb_register
        )

        # Act
        state: State = cpu.dump()

        # Assert
        assert state.memory == [Byte(0) for _ in range(256 * 256)]
        assert state.accumulator == Byte(0)
        assert state.pc_msb_register == Byte(0)
        assert state.pc_lsb_register == Byte(0)
        assert state.temp_register == Byte(0)
        assert state.mar_msb_register == Byte(0)
        assert state.mar_lsb_register == Byte(0)

        assert state.opcode == Byte(0)
        assert state.cycle_step == Byte(0)
        assert state.is_halt == Byte(0)

    def test__step__stepping_full_instruction_cycle__dump_validates_cycle_steps(self) -> None:
        # Arrange
        memory = Memory(Memory.get_default_memory_bytes())
        accumulator = ByteRegister()
        pc_msb_register = ByteRegister()
        pc_lsb_register = ByteRegister()
        temp_register = ByteRegister()
        mar_msb_register = ByteRegister()
        mar_lsb_register = ByteRegister()
        cpu = Cpu(
            memory,
            accumulator,
            pc_msb_register,
            pc_lsb_register,
            temp_register,
            mar_msb_register,
            mar_lsb_register
        )

        # Act and assert
        assert cpu.dump().cycle_step == Byte(0)
        cpu.step()
        assert cpu.dump().cycle_step == Byte(1)
        cpu.step()
        assert cpu.dump().cycle_step == Byte(2)
        cpu.step()
        assert cpu.dump().cycle_step == Byte(3)
        cpu.step()
        assert cpu.dump().cycle_step == Byte(4)
        cpu.step()
        assert cpu.dump().cycle_step == Byte(5)
        cpu.step()
        assert cpu.dump().cycle_step == Byte(6)
        cpu.step()
        assert cpu.dump().cycle_step == Byte(7)
        cpu.step()
        assert cpu.dump().cycle_step == Byte(8)
        cpu.step()

        state = cpu.dump()
        assert state.memory == [Byte(0) for _ in range(256 * 256)]
        assert state.accumulator == Byte(0)
        assert state.pc_msb_register == Byte(0)
        assert state.pc_lsb_register == Byte(0)
        assert state.temp_register == Byte(0)
        assert state.mar_msb_register == Byte(0)
        assert state.mar_lsb_register == Byte(0)

        assert state.opcode == Byte(0)
        assert state.cycle_step == Byte(0)
        assert state.is_halt == Byte(1)

    def test__cycle__cycle_load_instruction__accumulator_contains_expected_value(self) -> None:
        # Arrange
        expected = Byte(1)  # DATA

        memory_bytes = Memory.get_default_memory_bytes()
        memory_bytes[0] = Opcode.LOAD  # LOAD
        memory_bytes[1] = Byte(255)    # DATA
        memory_bytes[2] = Byte(255)    # DATA
        memory_bytes[-1] = expected    # DATA

        memory = Memory(memory_bytes)
        accumulator = ByteRegister()
        pc_msb_register = ByteRegister()
        pc_lsb_register = ByteRegister()
        temp_register = ByteRegister()
        mar_msb_register = ByteRegister()
        mar_lsb_register = ByteRegister()
        cpu = Cpu(
            memory,
            accumulator,
            pc_msb_register,
            pc_lsb_register,
            temp_register,
            mar_msb_register,
            mar_lsb_register
        )

        # Act
        cpu.cycle()
        dump = cpu.dump()

        # Assert
        assert dump.accumulator == expected

    def test__cycle__cycle_store_instruction__memory_contains_expected_value(self) -> None:
        # Arrange
        expected = Byte(1)  # DATA
        accumulator = ByteRegister.init_register_with_byte(expected)

        memory_bytes = Memory.get_default_memory_bytes()
        memory_bytes[0] = Opcode.STORE  # STORE
        memory_bytes[1] = Byte(255)     # DATA
        memory_bytes[2] = Byte(255)     # DATA

        memory = Memory(memory_bytes)
        pc_msb_register = ByteRegister()
        pc_lsb_register = ByteRegister()
        temp_register = ByteRegister()
        mar_msb_register = ByteRegister()
        mar_lsb_register = ByteRegister()
        cpu = Cpu(
            memory,
            accumulator,
            pc_msb_register,
            pc_lsb_register,
            temp_register,
            mar_msb_register,
            mar_lsb_register
        )

        # Act
        cpu.cycle()
        dump = cpu.dump()

        # Assert
        assert dump.memory[-1] == expected

    def test__cycle__cycle_add_instruction__accumulator_contains_expected_value(self) -> None:
        # Arrange
        expected = Byte(2)  # DATA
        accumulator = ByteRegister.init_register_with_byte(Byte(1))

        memory_bytes = Memory.get_default_memory_bytes()
        memory_bytes[0] = Opcode.ADD  # ADD
        memory_bytes[1] = Byte(255)   # DATA
        memory_bytes[2] = Byte(255)   # DATA
        memory_bytes[-1] = Byte(1)    # DATA

        memory = Memory(memory_bytes)
        pc_msb_register = ByteRegister()
        pc_lsb_register = ByteRegister()
        temp_register = ByteRegister()
        mar_msb_register = ByteRegister()
        mar_lsb_register = ByteRegister()
        cpu = Cpu(
            memory,
            accumulator,
            pc_msb_register,
            pc_lsb_register,
            temp_register,
            mar_msb_register,
            mar_lsb_register
        )

        # Act
        cpu.cycle()
        dump = cpu.dump()

        # Assert
        assert dump.accumulator == expected

    def test__cycle__cycle_add_instruction_with_overflow__accumulator_contains_expected_value(self) -> None:
        # Arrange
        expected = Byte(1)  # DATA
        accumulator = ByteRegister.init_register_with_byte(Byte(255))

        memory_bytes = Memory.get_default_memory_bytes()
        memory_bytes[0] = Opcode.ADD  # ADD
        memory_bytes[1] = Byte(255)   # DATA
        memory_bytes[2] = Byte(255)   # DATA
        memory_bytes[-1] = Byte(2)    # DATA

        memory = Memory(memory_bytes)
        pc_msb_register = ByteRegister()
        pc_lsb_register = ByteRegister()
        temp_register = ByteRegister()
        mar_msb_register = ByteRegister()
        mar_lsb_register = ByteRegister()
        cpu = Cpu(
            memory,
            accumulator,
            pc_msb_register,
            pc_lsb_register,
            temp_register,
            mar_msb_register,
            mar_lsb_register
        )

        # Act
        cpu.cycle()
        dump = cpu.dump()

        # Assert
        assert dump.accumulator == expected

    def test__cycle__cycle_sub_instruction__accumulator_contains_expected_value(self) -> None:
        # Arrange
        expected = Byte(1)  # DATA
        accumulator = ByteRegister.init_register_with_byte(Byte(2))

        memory_bytes = Memory.get_default_memory_bytes()
        memory_bytes[0] = Opcode.SUB  # SUB
        memory_bytes[1] = Byte(255)   # DATA
        memory_bytes[2] = Byte(255)   # DATA
        memory_bytes[-1] = Byte(1)    # DATA

        memory = Memory(memory_bytes)
        pc_msb_register = ByteRegister()
        pc_lsb_register = ByteRegister()
        temp_register = ByteRegister()
        mar_msb_register = ByteRegister()
        mar_lsb_register = ByteRegister()
        cpu = Cpu(
            memory,
            accumulator,
            pc_msb_register,
            pc_lsb_register,
            temp_register,
            mar_msb_register,
            mar_lsb_register
        )

        # Act
        cpu.cycle()
        dump = cpu.dump()

        # Assert
        assert dump.accumulator == expected

    def test__cycle__cycle_sub_instruction_with_underflow__accumulator_contains_expected_value(self) -> None:
        # Arrange
        expected = Byte(255)  # DATA
        accumulator = ByteRegister.init_register_with_byte(Byte(0))

        memory_bytes = Memory.get_default_memory_bytes()
        memory_bytes[0] = Opcode.SUB  # SUB
        memory_bytes[1] = Byte(255)   # DATA
        memory_bytes[2] = Byte(255)   # DATA
        memory_bytes[-1] = Byte(1)    # DATA

        memory = Memory(memory_bytes)
        pc_msb_register = ByteRegister()
        pc_lsb_register = ByteRegister()
        temp_register = ByteRegister()
        mar_msb_register = ByteRegister()
        mar_lsb_register = ByteRegister()
        cpu = Cpu(
            memory,
            accumulator,
            pc_msb_register,
            pc_lsb_register,
            temp_register,
            mar_msb_register,
            mar_lsb_register
        )

        # Act
        cpu.cycle()
        dump = cpu.dump()

        # Assert
        assert dump.accumulator == expected

    def test__cycle__cycle_jmp_instruction__pc_contains_expected_value(self) -> None:
        # Arrange
        pc_msb_expected = Byte(255)  # DATA
        pc_lsb_expected = Byte(255)  # DATA

        memory_bytes = Memory.get_default_memory_bytes()
        memory_bytes[0] = Opcode.JMP  # JMP
        memory_bytes[1] = Byte(255)   # DATA
        memory_bytes[2] = Byte(255)   # DATA

        memory = Memory(memory_bytes)
        accumulator = ByteRegister()
        pc_msb_register = ByteRegister()
        pc_lsb_register = ByteRegister()
        temp_register = ByteRegister()
        mar_msb_register = ByteRegister()
        mar_lsb_register = ByteRegister()
        cpu = Cpu(
            memory,
            accumulator,
            pc_msb_register,
            pc_lsb_register,
            temp_register,
            mar_msb_register,
            mar_lsb_register
        )

        # Act
        cpu.cycle()
        dump = cpu.dump()

        # Assert
        assert dump.pc_msb_register == pc_msb_expected
        assert dump.pc_lsb_register == pc_lsb_expected

    def test__cycle__cycle_jz_instruction_and_accumulator_is_zero__pc_contains_expected_value(self) -> None:
        # Arrange
        accumulator = ByteRegister.init_register_with_byte(Byte(0))
        pc_msb_expected = Byte(255)  # DATA
        pc_lsb_expected = Byte(255)  # DATA

        memory_bytes = Memory.get_default_memory_bytes()
        memory_bytes[0] = Opcode.JZ  # JZ
        memory_bytes[1] = Byte(255)  # DATA
        memory_bytes[2] = Byte(255)  # DATA

        memory = Memory(memory_bytes)
        pc_msb_register = ByteRegister()
        pc_lsb_register = ByteRegister()
        temp_register = ByteRegister()
        mar_msb_register = ByteRegister()
        mar_lsb_register = ByteRegister()
        cpu = Cpu(
            memory,
            accumulator,
            pc_msb_register,
            pc_lsb_register,
            temp_register,
            mar_msb_register,
            mar_lsb_register
        )

        # Act
        cpu.cycle()
        dump = cpu.dump()

        # Assert
        assert dump.pc_msb_register == pc_msb_expected
        assert dump.pc_lsb_register == pc_lsb_expected

    def test__cycle__cycle_jz_instruction_and_accumulator_is_not_zero__pc_contains_expected_value(self) -> None:
        # Arrange
        accumulator = ByteRegister.init_register_with_byte(Byte(1))
        pc_msb_expected = Byte(0)  # DATA
        pc_lsb_expected = Byte(3)  # DATA

        memory_bytes = Memory.get_default_memory_bytes()
        memory_bytes[0] = Opcode.JZ  # JZ
        memory_bytes[1] = Byte(255)  # DATA
        memory_bytes[2] = Byte(255)  # DATA

        memory = Memory(memory_bytes)
        pc_msb_register = ByteRegister()
        pc_lsb_register = ByteRegister()
        temp_register = ByteRegister()
        mar_msb_register = ByteRegister()
        mar_lsb_register = ByteRegister()
        cpu = Cpu(
            memory,
            accumulator,
            pc_msb_register,
            pc_lsb_register,
            temp_register,
            mar_msb_register,
            mar_lsb_register
        )

        # Act
        cpu.cycle()
        dump = cpu.dump()

        # Assert
        assert dump.pc_msb_register == pc_msb_expected
        assert dump.pc_lsb_register == pc_lsb_expected

    def test__cycle_until_halt__cycle_add_instruction__halts_and_pc_contains_expected_value(self) -> None:
        # Arrange
        accumulator = ByteRegister.init_register_with_byte(Byte(0))
        pc_msb_expected = Byte(0)  # DATA
        pc_lsb_expected = Byte(3)  # DATA

        memory_bytes = Memory.get_default_memory_bytes()
        memory_bytes[0] = Opcode.ADD  # ADD
        memory_bytes[1] = Byte(255)   # DATA
        memory_bytes[2] = Byte(255)   # DATA

        memory = Memory(memory_bytes)
        pc_msb_register = ByteRegister()
        pc_lsb_register = ByteRegister()
        temp_register = ByteRegister()
        mar_msb_register = ByteRegister()
        mar_lsb_register = ByteRegister()
        cpu = Cpu(
            memory,
            accumulator,
            pc_msb_register,
            pc_lsb_register,
            temp_register,
            mar_msb_register,
            mar_lsb_register
        )

        # Act
        cpu.cycle_until_halt()
        dump = cpu.dump()

        # Assert
        assert dump.pc_msb_register == pc_msb_expected
        assert dump.pc_lsb_register == pc_lsb_expected
        assert dump.is_halt == Byte(1)

    def test__cycle_until_halt__cycle_two_add_instructions__halts_and_pc_contains_expected_value(self) -> None:
        # Arrange
        accumulator = ByteRegister.init_register_with_byte(Byte(0))
        pc_msb_expected = Byte(0)  # DATA
        pc_lsb_expected = Byte(6)  # DATA

        memory_bytes = Memory.get_default_memory_bytes()
        memory_bytes[0] = Opcode.ADD  # ADD
        memory_bytes[1] = Byte(255)   # DATA
        memory_bytes[2] = Byte(254)   # DATA
        memory_bytes[3] = Opcode.ADD  # ADD
        memory_bytes[4] = Byte(255)   # DATA
        memory_bytes[5] = Byte(255)   # DATA

        memory = Memory(memory_bytes)
        pc_msb_register = ByteRegister()
        pc_lsb_register = ByteRegister()
        temp_register = ByteRegister()
        mar_msb_register = ByteRegister()
        mar_lsb_register = ByteRegister()
        cpu = Cpu(
            memory,
            accumulator,
            pc_msb_register,
            pc_lsb_register,
            temp_register,
            mar_msb_register,
            mar_lsb_register
        )

        # Act
        cpu.cycle_until_halt()
        dump = cpu.dump()

        # Assert
        assert dump.pc_msb_register == pc_msb_expected
        assert dump.pc_lsb_register == pc_lsb_expected
        assert dump.is_halt == Byte(1)
