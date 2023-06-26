from bytecore.memory import Memory
from bytecore.state import State
from bytecore.byte import Byte
from bytecore.opcode import Opcode
from bytecore.emulator import ByteCore


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
        memory_bytes = Memory.get_default_memory_bytes()

        memory_bytes[0] = Opcode.JMP
        # 00 00 JMP
        memory_bytes[1] = Byte(254)
        # 00 01 FE
        memory_bytes[2] = Byte(0)
        # 00 02 00

        memory_bytes[256] = Byte(55)
        # 01 00 37; 55
        memory_bytes[257] = Byte(20)
        # 01 01 14; 20
        memory_bytes[258] = Byte(2)
        # 01 02 02;  2
        memory_bytes[259] = Byte(1)
        # 01 03 01;  1

        memory_bytes[65024] = Opcode.LOAD
        # FE 00 LOAD
        memory_bytes[65025] = Byte(1)
        # FE 01 01
        memory_bytes[65026] = Byte(0)
        # FE 02 00
        memory_bytes[65027] = Opcode.ADD
        # FE 03 ADD
        memory_bytes[65028] = Byte(1)
        # FE 04 01
        memory_bytes[65029] = Byte(2)
        # FE 05 02
        memory_bytes[65030] = Opcode.STORE
        # FE 06 STORE
        memory_bytes[65031] = Byte(1)
        # FE 07 01
        memory_bytes[65032] = Byte(0)
        # FE 08 00
        memory_bytes[65033] = Opcode.LOAD
        # FE 09 LOAD
        memory_bytes[65034] = Byte(1)
        # FE 0A 01
        memory_bytes[65035] = Byte(1)
        # FE 0B 01
        memory_bytes[65036] = Opcode.SUB
        # FE 0C SUB
        memory_bytes[65037] = Byte(1)
        # FE 0D 01
        memory_bytes[65038] = Byte(3)
        # FE 0E 03
        memory_bytes[65039] = Opcode.STORE
        # FE 0F STORE
        memory_bytes[65040] = Byte(1)
        # FE 10 01
        memory_bytes[65041] = Byte(1)
        # FE 11 01
        memory_bytes[65042] = Opcode.LOAD
        # FE 0F LOAD
        memory_bytes[65043] = Byte(1)
        # FE 11 01
        memory_bytes[65044] = Byte(1)
        # FE 12 01
        memory_bytes[65045] = Opcode.JZ
        # FE 13 JZ
        memory_bytes[65046] = Byte(255)
        # FE 14 FF
        memory_bytes[65047] = Byte(0)
        # FE 15 00
        memory_bytes[65048] = Opcode.JMP
        # FE 16 JMP
        memory_bytes[65049] = Byte(254)
        # FE 17 FE
        memory_bytes[65050] = Byte(0)
        # FE 18 00

        memory_bytes[65280] = Opcode.LOAD
        # FF 00 LOAD
        memory_bytes[65281] = Byte(1)
        # FF 01 01
        memory_bytes[65282] = Byte(0)
        # FF 02 00
        memory_bytes[65283] = Opcode.STORE
        # FF 03 STORE
        memory_bytes[65284] = Byte(255)
        # FF 04 FF
        memory_bytes[65285] = Byte(255)
        # FF 05 FF
        memory_bytes[65286] = Opcode.HALT
        # FF 06 HALT

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
