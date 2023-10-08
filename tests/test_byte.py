import pytest
from bytecore.byte import Byte


class TestByte:
    def test_dummy_test(self) -> None:
        # Arrange, act and assert
        assert 0 == 0

    def test__value_init_0__returns_init_value(self) -> None:
        # Arrange
        value = 0

        # Act
        byte = Byte(value)

        # Assert
        assert byte.value == value

    def test__value_init_1__returns_init_value(self) -> None:
        # Arrange
        value = 1

        # Act
        byte = Byte(value)

        # Assert
        assert byte.value == value

    def test__init__set_256__raises_ValueError(self) -> None:
        # Arrange, act and assert
        with pytest.raises(ValueError):
            Byte(256)

    def test__init__set_minus_1__raises_ValueError(self) -> None:
        # Arrange, act and assert
        with pytest.raises(ValueError):
            Byte(-1)

    def test__init__two_objects_with_init_value_0__is_same_instance(self) -> None:
        # Arrange
        value = 0

        # Act
        byte1 = Byte(value)
        byte2 = Byte(value)

        # Assert
        assert byte1 is byte2

    def test__from_hex__hex_value_00__returns_byte_with_expected_value(self) -> None:
        # Arrange
        decimal_value = 0
        expected = Byte(decimal_value)
        hex_value = '00'

        # Act
        actual = Byte.from_hex(hex_value)

        # Assert
        assert actual == expected

    def test__from_hex__hex_value_FF__returns_byte_with_expected_value(self) -> None:
        # Arrange
        decimal_value = 255
        expected = Byte(decimal_value)
        hex_value = 'FF'

        # Act
        actual = Byte.from_hex(hex_value)

        # Assert
        assert actual == expected

    def test__from_hex__invalid_hex_value_0__raises_ValueError(self) -> None:
        # Arrange
        hex_value = '0'

        # Act and assert
        with pytest.raises(ValueError):
            Byte.from_hex(hex_value)

    def test__from_hex__invalid_hex_value_000__raises_ValueError(self) -> None:
        # Arrange
        hex_value = '000'

        # Act and assert
        with pytest.raises(ValueError):
            Byte.from_hex(hex_value)

    def test__from_hex__invalid_hex_value_with_leading_space__raises_ValueError(self) -> None:
        # Arrange
        hex_value = ' 0'

        # Act and assert
        with pytest.raises(ValueError):
            Byte.from_hex(hex_value)

    def test__from_hex__invalid_hex_value_with_trailing_space__raises_ValueError(self) -> None:
        # Arrange
        hex_value = '0 '

        # Act and assert
        with pytest.raises(ValueError):
            Byte.from_hex(hex_value)

    def test__from_hex__hex_value_ff__returns_byte_with_expected_value(self) -> None:
        # Arrange
        decimal_value = 255
        expected = Byte(decimal_value)
        hex_value = 'ff'

        # Act
        actual = Byte.from_hex(hex_value)

        # Assert
        assert actual == expected
