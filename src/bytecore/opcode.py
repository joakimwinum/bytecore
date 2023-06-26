from bytecore.byte import Byte


class Opcode:
    HALT = Byte(0)
    LOAD = Byte(1)
    STORE = Byte(2)
    ADD = Byte(4)
    SUB = Byte(8)
    JMP = Byte(16)
    JZ = Byte(32)
