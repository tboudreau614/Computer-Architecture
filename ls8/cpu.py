"""CPU functionality."""

import sys
# print(sys.argv)

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        # address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        try:
            address = 0
            file_name = sys.argv[1]

            with open(file_name) as fn:
                address = 0
                file_name=sys.argv[1]
                for line in fn:

                    split_hash = line.split('#')

                    string_int = split_hash[0].strip()

                    if string_int == "":
                        continue
                    bin_int = int(string_int, 2)

                    self.ram[address] = bin_int
                    address += 1
        
        except:
            print("No file found")
            print(sys.argv[1])
            print(sys.argv[0])

    # ram_read() should accept the address to read and return the value stored there.
    def ram_read(self, MAR):
        return self.ram[MAR]

    # ram_write() should accept a value to write, and the address to write it to.
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            inst = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            #  Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b.
            if inst == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            # Print value of register when the instruction is PRN
            elif inst == PRN:
                reg = self.ram[self.pc+1]
                print(self.reg[reg])
                self.pc += 2

            # Find value of MUL operation
            elif inst == MUL:
                self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
                # print(self.reg[operand_a]) this makes it print twice
                self.pc += 3

            # Stop what the program is doing and quit if the instruction is HLT
            elif inst == HLT:
                running = False
                self.pc += 1