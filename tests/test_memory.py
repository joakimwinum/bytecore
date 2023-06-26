from bytecore.memory import Memory
from bytecore.byte import Byte


class TestMemory:
    def test_dummy_test(self) -> None:
        # Arrange, act and assert
        assert 0 == 0

    def test__get_bus__write_to_bus__returns_same_value(self) -> None:
        # Arrange
        expected = Byte(255)
        memory = Memory(Memory.get_default_memory_bytes())
        memory.write_high()
        memory.set_bus(expected)
        memory.read_high()

        # Act
        actual = memory.get_bus()

        # Assert
        assert actual == expected

    def test__get_bus__write_to_multiple_places_modifying_msb_address__returns_same_values(self) -> None:
        # Arrange
        expected = (Byte(1), Byte(2), Byte(3))
        memory = Memory(Memory.get_default_memory_bytes())
        memory.write_high()
        memory.read_high()
        memory.set_bus(expected[0])
        memory.address_msb_write_high()
        memory.set_address_msb_bus(Byte(1))
        memory.set_bus(expected[1])
        memory.set_address_msb_bus(Byte(2))
        memory.set_bus(expected[2])

        # Act
        actual: list[Byte] = []
        memory.set_address_msb_bus(Byte(0))
        actual.append(memory.get_bus())
        memory.set_address_msb_bus(Byte(1))
        actual.append(memory.get_bus())
        memory.set_address_msb_bus(Byte(2))
        actual.append(memory.get_bus())

        # Assert
        assert actual[0] == expected[0]
        assert actual[1] == expected[1]
        assert actual[2] == expected[2]

    def test__get_bus__write_to_multiple_places_modifying_lsb_address__returns_same_values(self) -> None:
        # Arrange
        expected = (Byte(1), Byte(2), Byte(3))
        memory = Memory(Memory.get_default_memory_bytes())
        memory.write_high()
        memory.read_high()
        memory.set_bus(expected[0])
        memory.address_lsb_write_high()
        memory.set_address_lsb_bus(Byte(1))
        memory.set_bus(expected[1])
        memory.set_address_lsb_bus(Byte(2))
        memory.set_bus(expected[2])

        # Act
        actual: list[Byte] = []
        memory.set_address_lsb_bus(Byte(0))
        actual.append(memory.get_bus())
        memory.set_address_lsb_bus(Byte(1))
        actual.append(memory.get_bus())
        memory.set_address_lsb_bus(Byte(2))
        actual.append(memory.get_bus())

        # Assert
        assert actual[0] == expected[0]
        assert actual[1] == expected[1]
        assert actual[2] == expected[2]

    def test__dump__default_memory_bytes__dump_contains_only_default_values(self) -> None:
        # Arrange
        expected: list[Byte] = [Byte(0) for _ in range(256 * 256)]
        memory = Memory(Memory.get_default_memory_bytes())

        # Act
        actual: list[Byte] = memory.dump()

        # Assert
        assert actual == expected

    def test__dump__one_byte_changed__dump_contains_changed_byte(self) -> None:
        # Arrange
        expected: list[Byte] = [Byte(0) for _ in range(256 * 256)]
        expected[0] = Byte(1)

        memory = Memory(Memory.get_default_memory_bytes())
        memory.write_high()
        memory.set_bus(Byte(1))

        # Act
        actual: list[Byte] = memory.dump()

        # Assert
        assert actual == expected
