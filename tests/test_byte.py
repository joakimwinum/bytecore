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
