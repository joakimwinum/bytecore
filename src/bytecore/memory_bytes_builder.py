from bytecore.memory import Memory
from bytecore.byte import Byte
from bytecore.opcode import Opcode


class MemoryBytesBuilder:

    def __init__(self) -> None:
        self._memory_bytes = Memory.get_default_memory_bytes()
        self._msb = '00'
        self._lsb = '00'

    def msb(self, msb: str) -> 'MemoryBytesBuilder':
        Byte.from_hex(msb)
        self._msb = msb
        return self

    def lsb(self, lsb: str) -> 'MemoryBytesBuilder':
        Byte.from_hex(lsb)
        self._lsb = lsb
        return self

    def _store_byte(self, byte: Byte) -> 'MemoryBytesBuilder':
        self._memory_bytes[int(self._msb + self._lsb, 16)] = byte
        return self

    def data(self, data: str) -> 'MemoryBytesBuilder':
        return self._store_byte(Byte.from_hex(data))

    def halt(self) -> 'MemoryBytesBuilder':
        return self._store_byte(Opcode.HALT)

    def load(self) -> 'MemoryBytesBuilder':
        return self._store_byte(Opcode.LOAD)

    def store(self) -> 'MemoryBytesBuilder':
        return self._store_byte(Opcode.STORE)

    def add(self) -> 'MemoryBytesBuilder':
        return self._store_byte(Opcode.ADD)

    def sub(self) -> 'MemoryBytesBuilder':
        return self._store_byte(Opcode.SUB)

    def jmp(self) -> 'MemoryBytesBuilder':
        return self._store_byte(Opcode.JMP)

    def jz(self) -> 'MemoryBytesBuilder':
        return self._store_byte(Opcode.JZ)

    def comment(self, _: str) -> 'MemoryBytesBuilder':
        return self

    def build(self) -> list[Byte]:
        return self._memory_bytes
