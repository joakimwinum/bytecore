import pytest
from bytecore.memory import Memory
from bytecore.byte import Byte
from bytecore.opcode import Opcode
from bytecore.memory_bytes_builder import MemoryBytesBuilder


class TestMemoryBytesBuilder:
    def test_dummy_test(self) -> None:
        # Arrange, act and assert
        assert 0 == 0

    def test__build__simple_example_program__build_is_the_same(self) -> None:
        # Arrange
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

        expected = memory_bytes

        # Act
        actual = MemoryBytesBuilder()\
            .msb('00').lsb('00').load()\
            .msb('00').lsb('01').data('00')\
            .msb('00').lsb('02').data('0A')\
            .msb('00').lsb('03').add()\
            .msb('00').lsb('04').data('00')\
            .msb('00').lsb('05').data('0B')\
            .msb('00').lsb('06').store()\
            .msb('00').lsb('07').data('FF')\
            .msb('00').lsb('08').data('FF')\
            .msb('00').lsb('09').halt()\
            .msb('00').lsb('0A').data('14').comment('20')\
            .msb('00').lsb('0B').data('1E').comment('30')\
            .build()

        # Assert
        assert actual == expected

    def test__build__advanced_example_program_that_tests_all_opcodes__build_is_the_same(self) -> None:
        # Arrange
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
        # FE 12 LOAD
        memory_bytes[65043] = Byte(1)
        # FE 13 01
        memory_bytes[65044] = Byte(1)
        # FE 14 01
        memory_bytes[65045] = Opcode.JZ
        # FE 15 JZ
        memory_bytes[65046] = Byte(255)
        # FE 16 FF
        memory_bytes[65047] = Byte(0)
        # FE 17 00
        memory_bytes[65048] = Opcode.JMP
        # FE 18 JMP
        memory_bytes[65049] = Byte(254)
        # FE 19 FE
        memory_bytes[65050] = Byte(0)
        # FE 1A 00

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

        expected = memory_bytes

        # Act
        actual = MemoryBytesBuilder()\
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

        # Assert
        assert actual == expected

    def test__msb__invalid_hex_value_0__raises_ValueError(self) -> None:
        # Arrange, act and assert
        with pytest.raises(ValueError):
            MemoryBytesBuilder().msb('0')

    def test__lsb__invalid_hex_value_0__raises_ValueError(self) -> None:
        # Arrange, act and assert
        with pytest.raises(ValueError):
            MemoryBytesBuilder().lsb('0')

    def test__data__invalid_hex_value_0__raises_ValueError(self) -> None:
        # Arrange, act and assert
        with pytest.raises(ValueError):
            MemoryBytesBuilder().data('0')

    def test__comment__input_comment__has_no_effect(self) -> None:
        # Arrange
        expected = MemoryBytesBuilder().load().build()

        # Act
        actual = MemoryBytesBuilder().comment('foobar').load().build()

        # Assert
        assert actual == expected

    def test__build__setting_msb_once__has_same_affect_at_setting_it_twice(self) -> None:
        # Arrange
        expected = MemoryBytesBuilder()\
            .msb('FF').lsb('00').load()\
            .msb('FF').lsb('01').load()\
            .build()

        # Act
        actual = MemoryBytesBuilder()\
            .msb('FF').lsb('00').load()\
            .lsb('01').load()\
            .build()

        # Assert
        assert actual == expected

    def test__build__setting_lsb_once__has_same_affect_at_setting_it_twice(self) -> None:
        # Arrange
        expected = MemoryBytesBuilder()\
            .msb('00').lsb('FF').load()\
            .msb('01').lsb('FF').load()\
            .build()

        # Act
        actual = MemoryBytesBuilder()\
            .msb('00').lsb('FF').load()\
            .msb('01').load()\
            .build()

        # Assert
        assert actual == expected

    def test__build__all_opcodes__build_is_the_same(self) -> None:
        # Arrange
        memory_bytes = Memory.get_default_memory_bytes()

        memory_bytes[0] = Opcode.HALT
        # 00 00 HALT
        memory_bytes[1] = Opcode.LOAD
        # 00 01 LOAD
        memory_bytes[2] = Byte(255)
        # 00 02 FF
        memory_bytes[3] = Byte(255)
        # 00 03 FF
        memory_bytes[4] = Opcode.STORE
        # 00 04 STORE
        memory_bytes[5] = Byte(255)
        # 00 05 FF
        memory_bytes[6] = Byte(255)
        # 00 06 FF
        memory_bytes[7] = Opcode.ADD
        # 00 07 ADD
        memory_bytes[8] = Byte(255)
        # 00 08 FF
        memory_bytes[9] = Byte(255)
        # 00 09 FF
        memory_bytes[10] = Opcode.SUB
        # 00 0A SUB
        memory_bytes[11] = Byte(255)
        # 00 0B FF
        memory_bytes[12] = Byte(255)
        # 00 0C FF
        memory_bytes[13] = Opcode.JMP
        # 00 0D JMP
        memory_bytes[14] = Byte(255)
        # 00 0E FF
        memory_bytes[15] = Byte(255)
        # 00 0F FF
        memory_bytes[16] = Opcode.JZ
        # 00 10 JZ
        memory_bytes[17] = Byte(255)
        # 00 11 FF
        memory_bytes[18] = Byte(255)
        # 00 12 FF

        expected = memory_bytes

        # Act
        actual = MemoryBytesBuilder()\
            .msb('00').lsb('00').halt()\
            .msb('00').lsb('01').load()\
            .msb('00').lsb('02').data('FF')\
            .msb('00').lsb('03').data('FF')\
            .msb('00').lsb('04').store()\
            .msb('00').lsb('05').data('FF')\
            .msb('00').lsb('06').data('FF')\
            .msb('00').lsb('07').add()\
            .msb('00').lsb('08').data('FF')\
            .msb('00').lsb('09').data('FF')\
            .msb('00').lsb('0A').sub()\
            .msb('00').lsb('0B').data('FF')\
            .msb('00').lsb('0C').data('FF')\
            .msb('00').lsb('0D').jmp()\
            .msb('00').lsb('0E').data('FF')\
            .msb('00').lsb('0F').data('FF')\
            .msb('00').lsb('10').jz()\
            .msb('00').lsb('11').data('FF')\
            .msb('00').lsb('12').data('FF')\
            .build()

        # Assert
        assert actual == expected
