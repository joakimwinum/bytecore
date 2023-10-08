# ByteCore Emulator

ByteCore is a simple 8-bit CPU design following Von Neumann architecture (The design where both instructions and data share the same memory address space) capable of addressing 65536 (64KB) bytes of memory.

ByteCore Emulator is the Python implementation of the ByteCore CPU to test out the instruction set.

## Registers

- **Accumulator (A)**: An 8-bit register where arithmetic and logic operations are carried out.
- **Program Counter (PC)**: A 16-bit register which keeps track of the address of the current instruction being executed and points to the next instruction to be executed.

## Internal Registers

In addition to the Accumulator and Program Counter registers, the ByteCore CPU uses a few internal registers to manage its operations:

- **Temp Register (T)**: An 8-bit register used by the CPU to temporarily store data during arithmetic and logic operations.
- **Memory Address Register (MAR)**: A 16-bit register used by the CPU to hold the address to be accessed during memory operations.
- **Increment Register (IR)**: A constant register, permanently set to 1, used by the CPU specifically to increment the Program Counter.

These registers are used internally by the CPU and are not directly accessible to user programs. They are essential to the operation of the CPU and understanding their role can help users better understand the internal workings of the ByteCore CPU.

## Addressing Modes

The ByteCore CPU uses a big-endian memory architecture. In this design, the most significant byte (MSB) of a multi-byte value is stored at the smallest memory address.

- **Extended Mode**: Each instruction is directly followed in memory by a 16-bit address. This address is stored across two consecutive memory locations, with the most significant byte in the first location.

*Note: All uninitialized memory defaults to 0x0.*

## Word Size

In the context of the ByteCore CPU architecture, a "word" is defined as an 8-bit unit of data, consistent with its 8-bit design. This is the primary unit of data that can be manipulated with arithmetic and logic instructions.

A "double word" is a 16-bit unit of data, or two consecutive 8-bit words. This is primarily used in memory addressing, allowing the ByteCore CPU to access 65536 ($2^{16}$) individual memory locations.

## Instructions

Each instruction is represented by a unique 8-bit operation code, commonly abbreviated as "opcode". The instructions supported by the ByteCore CPU are as follows:

| Opcode (Binary) | Opcode (Hexadecimal) | Opcode (Decimal) | Instruction | Description |
| --- | --- | --- | --- | --- |
| `00000000` | `0x0` | `0` | `HALT` | Stop execution. |
| `00000001` | `0x1` | `1` | `LOAD` | Load the value from an extended memory address into the accumulator. |
| `00000010` | `0x2` | `2` | `STORE` | Store the value in the accumulator into an extended memory address. |
| `00000100` | `0x4` | `4` | `ADD` | Add the value from an extended memory address to the value in the accumulator. |
| `00001000` | `0x8` | `8` | `SUB` | Subtract the value from an extended memory address from the value in the accumulator. |
| `00010000` | `0x10` | `16` | `JMP` | Unconditional jump to an extended memory address. |
| `00100000` | `0x20` | `32` | `JZ` | Conditional jump to an extended memory address if the accumulator is zero. |

*Note: The opcode for HALT being 0x0 means that any uninitialized memory (which defaults to 0x0) will also halt the CPU, providing a fail-safe for programs that exceed their intended bounds.*

*Note: The opcode assignments are set up so that each opcode has exactly one bit set to 1. This is chosen to simplify hardware implementation where it will be possible to use a bit-selection logic to decode the opcodes.*

### HALT Instruction

The HALT instruction (opcode 0x0) stops the CPU from processing further instructions. When a HALT instruction is encountered, the CPU will enter a loop where it continually fetches and decodes the HALT instruction without incrementing the Program Counter (PC). This effectively suspends the CPU's operation until an external event occurs or the emulation is manually stopped. This behavior can be particularly useful for handling error situations or stopping the CPU after a program has finished execution.

### Unrecognized Opcodes

In the ByteCore CPU, any opcode that does not correspond to a defined instruction is treated as an invalid opcode. To ensure the stability and predictability of the system, the CPU defaults to executing the HALT operation when it encounters an invalid opcode.

This fail-safe mechanism prevents the execution of unintended or unknown instructions, aiding in error detection and debugging. It's important to note that when the CPU halts unexpectedly, it may be due to an unrecognized opcode in the instruction set.

## Instruction Cycle

This is a description of the instruction cycle, also known as the fetch-decode-execute cycle. The steps look like this:

1. **Fetch**: The CPU fetches the instruction from memory. This is the location pointed to by the program counter (PC).
2. **Decode**: The CPU decodes the instruction to determine what operation to perform.
3. **Evaluate Address MSB**: If the instruction involves data from memory, the CPU calculates the address of the most significant byte (MSB) of the data.
4. **Fetch Operand MSB**: If the instruction involves data from memory, the CPU fetches the most significant byte (MSB) of the data.
5. **Evaluate Address LSB**: The CPU calculates the address of the least significant byte (LSB) of the data.
6. **Fetch Operand LSB**: The CPU fetches the least significant byte (LSB) of the data.
7. **Execute**: The CPU performs the operation.
8. **Store Result**: If the operation produces a result, the CPU stores it in the appropriate place (either a register or a memory location).
9. **Increment PC**: The CPU increments the program counter to point to the next instruction.

These nine steps form one complete instruction cycle. The speed at which the CPU can complete these steps is determined by its clock speed. Each tick of the clock allows the CPU to move one step forward in the cycle.

## Boundary Conditions

The ByteCore CPU handles certain edge cases as follows:

- **Accumulator Overflow and Underflow**: The accumulator (A register) is an 8-bit register. If the result of an operation would be greater than 0xFF or less than 0x00, the value wraps around to fit within 8 bits. For example, if the accumulator holds the value 0xFF and an ADD instruction adds 1 to it, the result will be 0x00 (overflow). Similarly, if the accumulator holds the value 0x00 and a SUB instruction subtracts 1 from it, the result will be 0xFF (underflow).
- **Memory Address Overflow**: If an instruction attempts to read or write to an address that's outside the valid memory range (greater than 0xFFFF), the address wraps around to start from 0 again. For example, if a LOAD or STORE instruction tries to access the address 0x10000, it will instead access address 0x0000.

## Running the Emulator

Follow these steps to run the emulator.

### Manual Setup

Ensure that you have Python 3.11 or newer installed on your system.

Clone the repository and navigate into the root directory. You may want to create a Python virtual environment to isolate the project's dependencies.

To install the necessary dependencies, run:

```bash
pip3 install -r requirements.txt
```

### Gitpod Setup

You can also use Gitpod to run the emulator by clicking [here](https://gitpod.io/#https://github.com/joakimwinum/bytecore).

### Running the Emulator

Create a new Python file (e.g., `example.py`) in the src directory and add the following import statements:

```python
from bytecore.memory import Memory
from bytecore.byte import Byte
from bytecore.opcode import Opcode
from bytecore.emulator import ByteCore
```

Next, initialize a 64KB array of bytes as the memory:

```python
memory_bytes = Memory.get_default_memory_bytes()
```

You can then load your program into memory. Here is a simple example which loads the `HALT` instruction:

```python
memory_bytes[0] = Opcode.HALT
```

Instantiate the emulator with the provided memory:

```python
byte_core = ByteCore(memory_bytes)
```

You now have three options for running the emulator:

1. Execute a single step of the current instruction cycle:

    ```python
    byte_core.step()
    ```

2. Complete the current instruction cycle:

    ```python
    byte_core.cycle()
    ```

3. Execute instructions until the `HALT` state is reached:

    ```python
    byte_core.cycle_until_halt()
    ```

To inspect the state of memory at any point, use:

```python
dump = byte_core.dump()
memory_dump = dump.memory
```

You can print the entire memory dump, though please note that this will print 64KB of data to your screen:

```python
print(memory_dump)
```

For a more manageable output, consider printing a slice of the memory:

```python
print(memory_dump[0:20])
```

Finally, to run your `example.py` file, use:

```bash
python src/example.py
```

## Example Programs

Below, you'll find two example programs demonstrating how to utilize the ByteCore emulator. The first is a basic introduction, while the second one engages all the opcodes.

### Example 1: Simple Program

This program begins with a simple syntax using hexadecimal numbers for ease of drafting. It's then converted into a format the emulator understands, which uses decimal numbers (0 to 255) encapsulated in a Byte class.

```python
# Initial draft in hexadecimal:
# 00 00 LOAD
# 00 01 00
# 00 02 0A
# 00 03 ADD
# 00 04 00
# 00 05 0B
# 00 06 STORE
# 00 07 FF
# 00 08 FF
# 00 09 HALT
# 00 0A 14; 20
# 00 0B 1E; 30
```

Conversion to a format that the emulator understands:

```python
from bytecore.memory import Memory
from bytecore.byte import Byte
from bytecore.opcode import Opcode
from bytecore.emulator import ByteCore

memory_bytes = Memory.get_default_memory_bytes()

memory_bytes[0] = Opcode.LOAD
memory_bytes[1] = Byte(0)
memory_bytes[2] = Byte(10)
memory_bytes[3] = Opcode.ADD
memory_bytes[4] = Byte(0)
memory_bytes[5] = Byte(11)
memory_bytes[6] = Opcode.STORE
memory_bytes[7] = Byte(255)
memory_bytes[8] = Byte(255)
memory_bytes[9] = Opcode.HALT
memory_bytes[10] = Byte(20)
memory_bytes[11] = Byte(30)

byte_core = ByteCore(memory_bytes)
byte_core.cycle_until_halt()
dump = byte_core.dump()

dump.memory[-1]  # equals 50
```

To aid understanding, here is a Python equivalent of the ByteCore program:

```python
output = 0

a = 20
b = 30
accumulator = a       # LOAD
accumulator += b      # ADD
output = accumulator  # STORE
#                     # HALT

print(output)  # prints 50
```

### Example 2: Advanced Program

This advanced example begins similarly, drafting in hexadecimal. The transition to the emulator's format benefits from a custom builder class, streamlining the assembly of Byte instances.

```python
# Initial draft in hexadecimal:
# 00 00 JMP
# 00 01 FE
# 00 02 00

# 01 00 37; 55
# 01 01 14; 20
# 01 02 02;  2
# 01 03 01;  1

# FE 00 LOAD
# FE 01 01
# FE 02 00
# FE 03 ADD
# FE 04 01
# FE 05 02
# FE 06 STORE
# FE 07 01
# FE 08 00
# FE 09 LOAD
# FE 0A 01
# FE 0B 01
# FE 0C SUB
# FE 0D 01
# FE 0E 03
# FE 0F STORE
# FE 10 01
# FE 11 01
# FE 12 LOAD
# FE 13 01
# FE 14 01
# FE 15 JZ
# FE 16 FF
# FE 17 00
# FE 18 JMP
# FE 19 FE
# FE 1A 00

# FF 00 LOAD
# FF 01 01
# FF 02 00
# FF 03 STORE
# FF 04 FF
# FF 05 FF
# FF 06 HALT
```

Translation to the emulator-friendly format:

```python
from bytecore.memory_bytes_builder import MemoryBytesBuilder
from bytecore.emulator import ByteCore

memory_bytes = MemoryBytesBuilder()\
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

byte_core = ByteCore(memory_bytes)
byte_core.cycle_until_halt()
dump = byte_core.dump()

dump.memory[-1]  # equals 95
```

For further clarity, here's the Python equivalent of the ByteCore advanced program:

```python
output = 0

#                         # JMP to 1
a = 55
b = 20
c = 2
d = 1
while True:
    #                     # 1
    accumulator = a       # LOAD
    accumulator += c      # ADD
    a = accumulator       # STORE
    accumulator = b       # LOAD
    accumulator -= d      # SUB
    b = accumulator       # STORE
    accumulator = b       # LOAD
    if accumulator == 0:  # JZ to 2
        break
    #                     # JMP to 1

#                         # 2
accumulator = a           # LOAD
output = accumulator      # STORE
#                         # HALT

print(output)  # prints 95
```

## License

This project is licensed under the terms of the MIT License. See the [LICENSE](https://github.com/joakimwinum/bytecore/blob/main/LICENSE) file for the full text.
