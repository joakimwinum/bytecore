from src.byte import Byte
from src.bit import Bit


class ControlUnitState:
    def __init__(self) -> None:
        # These are internal circuit state, and not registers.
        self.opcode = Byte(0)
        self.cycle_step = Byte(0)
        self.is_halt = Bit.LOW
