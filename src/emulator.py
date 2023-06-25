from src.memory import Memory
from src.byte_register import ByteRegister
from src.byte import Byte
from src.state import State
from src.cpu import Cpu


class ByteCore:
    def __init__(self, memory_bytes: list[Byte]) -> None:
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
        self._cpu = cpu

    def step(self) -> None:
        self._cpu.step()

    def cycle(self) -> None:
        self._cpu.cycle()

    def cycle_until_halt(self) -> None:
        self._cpu.cycle_until_halt()

    def dump(self) -> State:
        return self._cpu.dump()
