from bytecore.memory import Memory
from bytecore.state import State
from bytecore.byte import Byte
from bytecore.opcode import Opcode
from bytecore.emulator import ByteCore
from bytecore.memory_bytes_builder import MemoryBytesBuilder


class TestEmulator:
    def test_dummy_test(self) -> None:
        # Arrange, act and assert
        assert 0 == 0

    def test__dump__after_init__returns_default_values(self) -> None:
        # Arrange
        byte_core = ByteCore(Memory.get_default_memory_bytes())

        # Act
        state: State = byte_core.dump()

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
        byte_core = ByteCore(Memory.get_default_memory_bytes())

        # Act and assert
        assert byte_core.dump().cycle_step == Byte(0)
        byte_core.step()
        assert byte_core.dump().cycle_step == Byte(1)
        byte_core.step()
        assert byte_core.dump().cycle_step == Byte(2)
        byte_core.step()
        assert byte_core.dump().cycle_step == Byte(3)
        byte_core.step()
        assert byte_core.dump().cycle_step == Byte(4)
        byte_core.step()
        assert byte_core.dump().cycle_step == Byte(5)
        byte_core.step()
        assert byte_core.dump().cycle_step == Byte(6)
        byte_core.step()
        assert byte_core.dump().cycle_step == Byte(7)
        byte_core.step()
        assert byte_core.dump().cycle_step == Byte(8)
        byte_core.step()

        state = byte_core.dump()
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

        byte_core = ByteCore(memory_bytes)

        # Act
        byte_core.cycle()
        dump = byte_core.dump()

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

        byte_core = ByteCore(memory_bytes)

        # Act
        byte_core.cycle()
        dump = byte_core.dump()

        # Assert
        assert dump.pc_msb_register == pc_msb_expected
        assert dump.pc_lsb_register == pc_lsb_expected

    def test__cycle_until_halt__simple_example_program__halts_and_last_memory_location_contains_expected_value(self) -> None:
        # Arrange
        expected = Byte(50)
        memory_bytes = Memory.get_default_memory_bytes()

        memory_bytes[0] = Opcode.LOAD
        # 00 00 LOAD
        memory_bytes[1] = Byte(0)
        # 00 01 00
        memory_bytes[2] = Byte(10)
        # 00 02 0A
        memory_bytes[3] = Opcode.ADD
        # 00 03 ADD
        memory_bytes[4] = Byte(0)
        # 00 04 00
        memory_bytes[5] = Byte(11)
        # 00 05 0B
        memory_bytes[6] = Opcode.STORE
        # 00 06 STORE
        memory_bytes[7] = Byte(255)
        # 00 07 FF
        memory_bytes[8] = Byte(255)
        # 00 08 FF
        memory_bytes[9] = Opcode.HALT
        # 00 09 HALT
        memory_bytes[10] = Byte(20)
        # 00 0A 14; 20
        memory_bytes[11] = Byte(30)
        # 00 0B 1E; 30

        byte_core = ByteCore(memory_bytes)

        # Act
        byte_core.cycle_until_halt()
        dump = byte_core.dump()

        # Assert
        assert dump.memory[-1] == expected
        assert dump.is_halt == Byte(1)

    def test__ported_to_python__simple_example_program__output_contains_expected_value(self) -> None:
        # Arrange
        expected = 50
        output = 0

        # Act
        a = 20
        b = 30
        accumulator = a       # LOAD
        accumulator += b      # ADD
        output = accumulator  # STORE
        #                     # HALT

        # Assert
        assert output == expected

    def test__cycle_until_halt__advanced_example_program_that_tests_all_opcodes__halts_and_last_memory_location_contains_expected_value(self) -> None:
        # Arrange
        expected = Byte(95)
        memory_bytes = MemoryBytesBuilder()\
            .msb('00').lsb('00').jmp()\
            .msb('00').lsb('01').data('FE')\
            .msb('00').lsb('02').data('00')\
            \
            .msb('01').lsb('00').data('37').comment('55')\
            .msb('01').lsb('01').data('14').comment('20')\
            .msb('01').lsb('02').data('02').comment(' 2')\
            .msb('01').lsb('03').data('01').comment(' 1')\
            \
            .msb('FE').lsb('00').load()\
            .msb('FE').lsb('01').data('01')\
            .msb('FE').lsb('02').data('00')\
            .msb('FE').lsb('03').add()\
            .msb('FE').lsb('04').data('01')\
            .msb('FE').lsb('05').data('02')\
            .msb('FE').lsb('06').store()\
            .msb('FE').lsb('07').data('01')\
            .msb('FE').lsb('08').data('00')\
            .msb('FE').lsb('09').load()\
            .msb('FE').lsb('0A').data('01')\
            .msb('FE').lsb('0B').data('01')\
            .msb('FE').lsb('0C').sub()\
            .msb('FE').lsb('0D').data('01')\
            .msb('FE').lsb('0E').data('03')\
            .msb('FE').lsb('0F').store()\
            .msb('FE').lsb('10').data('01')\
            .msb('FE').lsb('11').data('01')\
            .msb('FE').lsb('12').load()\
            .msb('FE').lsb('13').data('01')\
            .msb('FE').lsb('14').data('01')\
            .msb('FE').lsb('15').jz()\
            .msb('FE').lsb('16').data('FF')\
            .msb('FE').lsb('17').data('00')\
            .msb('FE').lsb('18').jmp()\
            .msb('FE').lsb('19').data('FE')\
            .msb('FE').lsb('1A').data('00')\
            \
            .msb('FF').lsb('00').load()\
            .msb('FF').lsb('01').data('01')\
            .msb('FF').lsb('02').data('00')\
            .msb('FF').lsb('03').store()\
            .msb('FF').lsb('04').data('FF')\
            .msb('FF').lsb('05').data('FF')\
            .msb('FF').lsb('06').halt()\
            .build()

        byte_core = ByteCore(memory_bytes)

        # Act
        byte_core.cycle_until_halt()
        dump = byte_core.dump()

        # Assert
        assert dump.memory[-1] == expected
        assert dump.is_halt == Byte(1)

    def test__ported_to_python__advanced_example_program_that_tests_all_opcodes__output_contains_expected_value(self) -> None:
        # Arrange
        expected = 95
        output = 0

        # Act
        #                         # JMP to 1
        a = 55
        b = 20
        c = 2
        d = 1
        while True:
            #                     # 1
            accumulator = a       # LOAD
            accumulator += c      # ADD
            a = accumulator       # STORE
            accumulator = b       # LOAD
            accumulator -= d      # SUB
            b = accumulator       # STORE
            accumulator = b       # LOAD
            if accumulator == 0:  # JZ to 2
                break
            #                     # JMP to 1

        #                         # 2
        accumulator = a           # LOAD
        output = accumulator      # STORE
        #                         # HALT

        # Assert
        assert output == expected

    def test__cycle__jz_works_as_expected_after_add__accumulator_and_pc_contains_expected_values(self) -> None:
        # Arrange
        expected_accumulator = Byte(1)
        expected_msb_register = Byte(0)
        expected_lsb_register = Byte(9)
        memory_bytes = MemoryBytesBuilder()\
            .msb('00').lsb('00').load()\
            .msb('00').lsb('01').data('01')\
            .msb('00').lsb('02').data('00')\
            .msb('00').lsb('03').add()\
            .msb('00').lsb('04').data('01')\
            .msb('00').lsb('05').data('01')\
            .msb('00').lsb('06').jz()\
            .msb('00').lsb('07').data('FF')\
            .msb('00').lsb('08').data('FF')\
            \
            .msb('01').lsb('00').data('00').comment(' 0')\
            .msb('01').lsb('01').data('01').comment(' 1')\
            .build()

        byte_core = ByteCore(memory_bytes)

        # Act
        byte_core.cycle()
        byte_core.cycle()
        byte_core.cycle()
        dump = byte_core.dump()

        # Assert
        assert dump.accumulator == expected_accumulator
        assert dump.pc_msb_register == expected_msb_register
        assert dump.pc_lsb_register == expected_lsb_register

    def test__cycle__jz_works_as_expected_after_sub__accumulator_and_pc_contains_expected_values(self) -> None:
        # Arrange
        expected_accumulator = Byte(255)
        expected_msb_register = Byte(0)
        expected_lsb_register = Byte(9)
        memory_bytes = MemoryBytesBuilder()\
            .msb('00').lsb('00').load()\
            .msb('00').lsb('01').data('01')\
            .msb('00').lsb('02').data('00')\
            .msb('00').lsb('03').sub()\
            .msb('00').lsb('04').data('01')\
            .msb('00').lsb('05').data('01')\
            .msb('00').lsb('06').jz()\
            .msb('00').lsb('07').data('FF')\
            .msb('00').lsb('08').data('FF')\
            \
            .msb('01').lsb('00').data('00').comment(' 0')\
            .msb('01').lsb('01').data('01').comment(' 1')\
            .build()

        byte_core = ByteCore(memory_bytes)

        # Act
        byte_core.cycle()
        byte_core.cycle()
        byte_core.cycle()
        dump = byte_core.dump()

        # Assert
        assert dump.accumulator == expected_accumulator
        assert dump.pc_msb_register == expected_msb_register
        assert dump.pc_lsb_register == expected_lsb_register

    def test__cycle__chaining_load_add_store_sub_jz__accumulator_and_pc_and_stored_value_contains_expected_values(self) -> None:
        # Arrange
        expected_accumulator = Byte(0)
        expected_msb_register = Byte(255)
        expected_lsb_register = Byte(255)
        expected_stored_value = Byte(1)
        memory_bytes = MemoryBytesBuilder()\
            .msb('00').lsb('00').load()\
            .msb('00').lsb('01').data('01')\
            .msb('00').lsb('02').data('00')\
            .msb('00').lsb('03').add()\
            .msb('00').lsb('04').data('01')\
            .msb('00').lsb('05').data('01')\
            .msb('00').lsb('06').store()\
            .msb('00').lsb('07').data('FF')\
            .msb('00').lsb('08').data('00')\
            .msb('00').lsb('09').sub()\
            .msb('00').lsb('0A').data('01')\
            .msb('00').lsb('0B').data('01')\
            .msb('00').lsb('0C').jz()\
            .msb('00').lsb('0D').data('FF')\
            .msb('00').lsb('0E').data('FF')\
            \
            .msb('01').lsb('00').data('00').comment(' 0')\
            .msb('01').lsb('01').data('01').comment(' 1')\
            .build()

        byte_core = ByteCore(memory_bytes)

        # Act
        for _ in range(5):
            byte_core.cycle()
        dump = byte_core.dump()

        # Assert
        assert dump.accumulator == expected_accumulator
        assert dump.pc_msb_register == expected_msb_register
        assert dump.pc_lsb_register == expected_lsb_register
        assert dump.memory[int('FF_00', 16)] == expected_stored_value

    def test__cycle__chaining_load_add_store_sub_sub_jz__accumulator_and_pc_and_stored_value_contains_expected_values(self) -> None:
        # Arrange
        expected_accumulator = Byte(255)
        expected_msb_register = Byte(0)
        expected_lsb_register = Byte(18)
        expected_stored_value = Byte(1)
        memory_bytes = MemoryBytesBuilder()\
            .msb('00').lsb('00').load()\
            .msb('00').lsb('01').data('01')\
            .msb('00').lsb('02').data('00')\
            .msb('00').lsb('03').add()\
            .msb('00').lsb('04').data('01')\
            .msb('00').lsb('05').data('01')\
            .msb('00').lsb('06').store()\
            .msb('00').lsb('07').data('FF')\
            .msb('00').lsb('08').data('00')\
            .msb('00').lsb('09').sub()\
            .msb('00').lsb('0A').data('01')\
            .msb('00').lsb('0B').data('01')\
            .msb('00').lsb('0C').sub()\
            .msb('00').lsb('0D').data('01')\
            .msb('00').lsb('0E').data('01')\
            .msb('00').lsb('0F').jz()\
            .msb('00').lsb('10').data('FF')\
            .msb('00').lsb('11').data('FF')\
            \
            .msb('01').lsb('00').data('00').comment(' 0')\
            .msb('01').lsb('01').data('01').comment(' 1')\
            .build()

        byte_core = ByteCore(memory_bytes)

        # Act
        for _ in range(6):
            byte_core.cycle()
        dump = byte_core.dump()

        # Assert
        assert dump.accumulator == expected_accumulator
        assert dump.pc_msb_register == expected_msb_register
        assert dump.pc_lsb_register == expected_lsb_register
        assert dump.memory[int('FF_00', 16)] == expected_stored_value

    def test__cycle__chaining_load_add_store_jz__accumulator_and_pc_and_stored_value_contains_expected_values(self) -> None:
        # Arrange
        expected_accumulator = Byte(2)
        expected_msb_register = Byte(0)
        expected_lsb_register = Byte(12)
        expected_stored_value = Byte(2)
        memory_bytes = MemoryBytesBuilder()\
            .msb('00').lsb('00').load()\
            .msb('00').lsb('01').data('01')\
            .msb('00').lsb('02').data('00')\
            .msb('00').lsb('03').add()\
            .msb('00').lsb('04').data('01')\
            .msb('00').lsb('05').data('00')\
            .msb('00').lsb('06').store()\
            .msb('00').lsb('07').data('FF')\
            .msb('00').lsb('08').data('00')\
            .msb('00').lsb('09').jz()\
            .msb('00').lsb('0A').data('FF')\
            .msb('00').lsb('0B').data('FF')\
            \
            .msb('01').lsb('00').data('01').comment(' 1')\
            .build()

        byte_core = ByteCore(memory_bytes)

        # Act
        byte_core.cycle()
        byte_core.cycle()
        byte_core.cycle()
        byte_core.cycle()
        dump = byte_core.dump()

        # Assert
        assert dump.accumulator == expected_accumulator
        assert dump.pc_msb_register == expected_msb_register
        assert dump.pc_lsb_register == expected_lsb_register
        assert dump.memory[int('FF_00', 16)] == expected_stored_value

    def test__cycle__chaining_load_sub_store_jz__accumulator_and_pc_and_stored_value_contains_expected_values(self) -> None:
        # Arrange
        expected_accumulator = Byte(0)
        expected_msb_register = Byte(255)
        expected_lsb_register = Byte(255)
        expected_stored_value = Byte(0)
        memory_bytes = MemoryBytesBuilder()\
            .msb('00').lsb('00').load()\
            .msb('00').lsb('01').data('01')\
            .msb('00').lsb('02').data('00')\
            .msb('00').lsb('03').sub()\
            .msb('00').lsb('04').data('01')\
            .msb('00').lsb('05').data('00')\
            .msb('00').lsb('06').store()\
            .msb('00').lsb('07').data('FF')\
            .msb('00').lsb('08').data('00')\
            .msb('00').lsb('09').jz()\
            .msb('00').lsb('0A').data('FF')\
            .msb('00').lsb('0B').data('FF')\
            \
            .msb('01').lsb('00').data('01').comment(' 1')\
            .build()

        byte_core = ByteCore(memory_bytes)

        # Act
        byte_core.cycle()
        byte_core.cycle()
        byte_core.cycle()
        byte_core.cycle()
        dump = byte_core.dump()

        # Assert
        assert dump.accumulator == expected_accumulator
        assert dump.pc_msb_register == expected_msb_register
        assert dump.pc_lsb_register == expected_lsb_register
        assert dump.memory[int('FF_00', 16)] == expected_stored_value

    def test__cycle__chaining_load_jmp_add_store_jz__accumulator_and_pc_and_stored_value_contains_expected_values(self) -> None:
        # Arrange
        expected_accumulator = Byte(2)
        expected_msb_register = Byte(0)
        expected_lsb_register = Byte(15)
        expected_stored_value = Byte(2)
        memory_bytes = MemoryBytesBuilder()\
            .msb('00').lsb('00').load()\
            .msb('00').lsb('01').data('01')\
            .msb('00').lsb('02').data('00')\
            .msb('00').lsb('03').jmp()\
            .msb('00').lsb('04').data('00')\
            .msb('00').lsb('05').data('06')\
            .msb('00').lsb('06').add()\
            .msb('00').lsb('07').data('01')\
            .msb('00').lsb('08').data('00')\
            .msb('00').lsb('09').store()\
            .msb('00').lsb('0A').data('FF')\
            .msb('00').lsb('0B').data('00')\
            .msb('00').lsb('0C').jz()\
            .msb('00').lsb('0D').data('FF')\
            .msb('00').lsb('0E').data('FF')\
            \
            .msb('01').lsb('00').data('01').comment(' 1')\
            .build()

        byte_core = ByteCore(memory_bytes)

        # Act
        for _ in range(5):
            byte_core.cycle()
        dump = byte_core.dump()

        # Assert
        assert dump.accumulator == expected_accumulator
        assert dump.pc_msb_register == expected_msb_register
        assert dump.pc_lsb_register == expected_lsb_register
        assert dump.memory[int('FF_00', 16)] == expected_stored_value

    def test__cycle__chaining_load_jmp_sub_store_jz__accumulator_and_pc_and_stored_value_contains_expected_values(self) -> None:
        # Arrange
        expected_accumulator = Byte(0)
        expected_msb_register = Byte(255)
        expected_lsb_register = Byte(255)
        expected_stored_value = Byte(0)
        memory_bytes = MemoryBytesBuilder()\
            .msb('00').lsb('00').load()\
            .msb('00').lsb('01').data('01')\
            .msb('00').lsb('02').data('00')\
            .msb('00').lsb('03').jmp()\
            .msb('00').lsb('04').data('00')\
            .msb('00').lsb('05').data('06')\
            .msb('00').lsb('06').sub()\
            .msb('00').lsb('07').data('01')\
            .msb('00').lsb('08').data('00')\
            .msb('00').lsb('09').store()\
            .msb('00').lsb('0A').data('FF')\
            .msb('00').lsb('0B').data('00')\
            .msb('00').lsb('0C').jz()\
            .msb('00').lsb('0D').data('FF')\
            .msb('00').lsb('0E').data('FF')\
            \
            .msb('01').lsb('00').data('01').comment(' 1')\
            .build()

        byte_core = ByteCore(memory_bytes)

        # Act
        for _ in range(5):
            byte_core.cycle()
        dump = byte_core.dump()

        # Assert
        assert dump.accumulator == expected_accumulator
        assert dump.pc_msb_register == expected_msb_register
        assert dump.pc_lsb_register == expected_lsb_register
        assert dump.memory[int('FF_00', 16)] == expected_stored_value

    def test__cycle__chaining_load_add_jmp_store_jz__accumulator_and_pc_and_stored_value_contains_expected_values(self) -> None:
        # Arrange
        expected_accumulator = Byte(2)
        expected_msb_register = Byte(0)
        expected_lsb_register = Byte(15)
        expected_stored_value = Byte(2)
        memory_bytes = MemoryBytesBuilder()\
            .msb('00').lsb('00').load()\
            .msb('00').lsb('01').data('01')\
            .msb('00').lsb('02').data('00')\
            .msb('00').lsb('03').add()\
            .msb('00').lsb('04').data('01')\
            .msb('00').lsb('05').data('00')\
            .msb('00').lsb('06').jmp()\
            .msb('00').lsb('07').data('00')\
            .msb('00').lsb('08').data('09')\
            .msb('00').lsb('09').store()\
            .msb('00').lsb('0A').data('FF')\
            .msb('00').lsb('0B').data('00')\
            .msb('00').lsb('0C').jz()\
            .msb('00').lsb('0D').data('FF')\
            .msb('00').lsb('0E').data('FF')\
            \
            .msb('01').lsb('00').data('01').comment(' 1')\
            .build()

        byte_core = ByteCore(memory_bytes)

        # Act
        for _ in range(5):
            byte_core.cycle()
        dump = byte_core.dump()

        # Assert
        assert dump.accumulator == expected_accumulator
        assert dump.pc_msb_register == expected_msb_register
        assert dump.pc_lsb_register == expected_lsb_register
        assert dump.memory[int('FF_00', 16)] == expected_stored_value

    def test__cycle__chaining_load_sub_jmp_store_jz__accumulator_and_pc_and_stored_value_contains_expected_values(self) -> None:
        # Arrange
        expected_accumulator = Byte(0)
        expected_msb_register = Byte(255)
        expected_lsb_register = Byte(255)
        expected_stored_value = Byte(0)
        memory_bytes = MemoryBytesBuilder()\
            .msb('00').lsb('00').load()\
            .msb('00').lsb('01').data('01')\
            .msb('00').lsb('02').data('00')\
            .msb('00').lsb('03').sub()\
            .msb('00').lsb('04').data('01')\
            .msb('00').lsb('05').data('00')\
            .msb('00').lsb('06').jmp()\
            .msb('00').lsb('07').data('00')\
            .msb('00').lsb('08').data('09')\
            .msb('00').lsb('09').store()\
            .msb('00').lsb('0A').data('FF')\
            .msb('00').lsb('0B').data('00')\
            .msb('00').lsb('0C').jz()\
            .msb('00').lsb('0D').data('FF')\
            .msb('00').lsb('0E').data('FF')\
            \
            .msb('01').lsb('00').data('01').comment(' 1')\
            .build()

        byte_core = ByteCore(memory_bytes)

        # Act
        for _ in range(5):
            byte_core.cycle()
        dump = byte_core.dump()

        # Assert
        assert dump.accumulator == expected_accumulator
        assert dump.pc_msb_register == expected_msb_register
        assert dump.pc_lsb_register == expected_lsb_register
        assert dump.memory[int('FF_00', 16)] == expected_stored_value

    def test__cycle__chaining_load_add_store_jmp_jz__accumulator_and_pc_and_stored_value_contains_expected_values(self) -> None:
        # Arrange
        expected_accumulator = Byte(2)
        expected_msb_register = Byte(0)
        expected_lsb_register = Byte(15)
        expected_stored_value = Byte(2)
        memory_bytes = MemoryBytesBuilder()\
            .msb('00').lsb('00').load()\
            .msb('00').lsb('01').data('01')\
            .msb('00').lsb('02').data('00')\
            .msb('00').lsb('03').add()\
            .msb('00').lsb('04').data('01')\
            .msb('00').lsb('05').data('00')\
            .msb('00').lsb('06').store()\
            .msb('00').lsb('07').data('FF')\
            .msb('00').lsb('08').data('00')\
            .msb('00').lsb('09').jmp()\
            .msb('00').lsb('0A').data('00')\
            .msb('00').lsb('0B').data('0C')\
            .msb('00').lsb('0C').jz()\
            .msb('00').lsb('0D').data('FF')\
            .msb('00').lsb('0E').data('FF')\
            \
            .msb('01').lsb('00').data('01').comment(' 1')\
            .build()

        byte_core = ByteCore(memory_bytes)

        # Act
        for _ in range(5):
            byte_core.cycle()
        dump = byte_core.dump()

        # Assert
        assert dump.accumulator == expected_accumulator
        assert dump.pc_msb_register == expected_msb_register
        assert dump.pc_lsb_register == expected_lsb_register
        assert dump.memory[int('FF_00', 16)] == expected_stored_value

    def test__cycle__chaining_load_sub_store_jmp_jz__accumulator_and_pc_and_stored_value_contains_expected_values(self) -> None:
        # Arrange
        expected_accumulator = Byte(0)
        expected_msb_register = Byte(255)
        expected_lsb_register = Byte(255)
        expected_stored_value = Byte(0)
        memory_bytes = MemoryBytesBuilder()\
            .msb('00').lsb('00').load()\
            .msb('00').lsb('01').data('01')\
            .msb('00').lsb('02').data('00')\
            .msb('00').lsb('03').sub()\
            .msb('00').lsb('04').data('01')\
            .msb('00').lsb('05').data('00')\
            .msb('00').lsb('06').store()\
            .msb('00').lsb('07').data('FF')\
            .msb('00').lsb('08').data('00')\
            .msb('00').lsb('09').jmp()\
            .msb('00').lsb('0A').data('00')\
            .msb('00').lsb('0B').data('0C')\
            .msb('00').lsb('0C').jz()\
            .msb('00').lsb('0D').data('FF')\
            .msb('00').lsb('0E').data('FF')\
            \
            .msb('01').lsb('00').data('01').comment(' 1')\
            .build()

        byte_core = ByteCore(memory_bytes)

        # Act
        for _ in range(5):
            byte_core.cycle()
        dump = byte_core.dump()

        # Assert
        assert dump.accumulator == expected_accumulator
        assert dump.pc_msb_register == expected_msb_register
        assert dump.pc_lsb_register == expected_lsb_register
        assert dump.memory[int('FF_00', 16)] == expected_stored_value
