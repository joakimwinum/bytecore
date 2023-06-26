import pytest
from bytecore.bit import Bit


class TestBit:
    def test_dummy_test(self) -> None:
        # Arrange, act and assert
        assert 0 == 0

    def test__value_init_0__returns_init_value(self) -> None:
        # Arrange
        value = 0

        # Act
        bit = Bit(value)

        # Assert
        assert bit.value == value

    def test__value_init_1__returns_init_value(self) -> None:
        # Arrange
        value = 1

        # Act
        bit = Bit(value)

        # Assert
        assert bit.value == value

    def test__init__set_2__raises_ValueError(self) -> None:
        # Arrange, act and assert
        with pytest.raises(ValueError):
            Bit(2)

    def test__init__set_minus_1__raises_ValueError(self) -> None:
        # Arrange, act and assert
        with pytest.raises(ValueError):
            Bit(-1)

    def test__init__two_objects_with_init_value_0__is_same_instance(self) -> None:
        # Arrange
        value = 0

        # Act
        bit1 = Bit(value)
        bit2 = Bit(value)

        # Assert
        assert bit1 is bit2
