from bytecore.byte_register import ByteRegister
from bytecore.byte import Byte


class TestByteRegister:
    def test_dummy_test(self) -> None:
        # Arrange, act and assert
        assert 0 == 0

    def test__decimal__init__returns_0(self) -> None:
        # Arrange
        expected = Byte(0)
        register = ByteRegister()

        # Act
        actual = register.get_bus()

        # Assert
        assert actual == expected

    def test__get_binary__returns_8bit_binary(self) -> None:
        # Arrange
        expected = '00000000'
        register = ByteRegister()

        # Act
        actual = register.get_binary()

        # Assert
        assert actual == expected

    def test__get_hex__returns_double_letter_hex_value(self) -> None:
        # Arrange
        expected = '00'
        register = ByteRegister()

        # Act
        actual = register.get_hex()

        # Assert
        assert actual == expected

    def test__decimal__set_255__returns_correct_decimal_binary_and_hex(self) -> None:
        # Arrange
        expected_bus = Byte(255)
        expected_decimal = expected_bus.value
        expected_binary = '11111111'
        expected_hex = 'FF'
        register = ByteRegister()
        register.write_high()
        register.set_bus(expected_bus)
        register.read_high()

        # Act
        actual_bus = register.get_bus()
        actual_decimal = register.get_decimal()
        actual_binary = register.get_binary()
        actual_hex = register.get_hex()

        # Assert
        assert actual_bus == expected_bus
        assert actual_decimal == expected_decimal
        assert actual_binary == expected_binary
        assert actual_hex == expected_hex
