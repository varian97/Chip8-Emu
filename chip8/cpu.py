class CPU:
    def __init__(self, keyboard, sound, display) -> None:
        self.keyboard = keyboard
        self.sound = sound
        self.display = display

        self.func_pointer = [
            self.__handle_0,
            self.__handle_1,
            self.__handle_2,
            self.__handle_3,
            self.__handle_4,
            self.__handle_5,
            self.__handle_6,
            self.__handle_7,
            self.__handle_8,
            self.__handle_9,
            self.__handle_A,
            self.__handle_B,
            self.__handle_C,
            self.__handle_D,
            self.__handle_E,
            self.__handle_F,
        ]

        # 4096 bytes ram
        # 0x00 - 0x1ff are where the original interpreter located and should not be used
        # program starts at 0x200
        self.memory = [0] * 4096

        # 8-bit general purpose registers called Vx where x is from 0 to f
        self.v = [0] * 16

        # special 16-bit register for holding memory addresses, only the first 12 bit used (because our ram is only 4 kb, 0x00 - 0xfff)
        self.i = 0

        # delay and sound, each 8 bit, when they are non zero -> decrement at a rate of 60Hz
        self.delay_timer = 0
        self.sound_timer = 0

        # 16-bit program counter (eip)
        self.pc = 0x200

        # 16 16-bit values
        self.stack = []

        # 8 bit stack pointer
        self.stack_pointer = 0

        self.paused = False

    def load_rom_into_memory(self, fileName):
        with open(fileName, 'rb') as infile:
            counter = 0
            while byte := infile.read(1):
                self.memory[counter + 0x200] = int.from_bytes(byte, 'big')
                counter += 1

    def cycle(self):
        if not self.paused:
            opcode = self.fetch_instruction()
            self.run_instruction(opcode)

    def fetch_instruction(self):
        first_nibble = self.memory[self.pc]
        second_nibble = self.memory[self.pc + 1]
        opcode = (first_nibble << 8) | second_nibble

        return opcode

    def run_instruction(self, opcode):
        prefix = opcode & 0x1000
        self.func_pointer[prefix]

    def __handle_0(self, opcode):
        pass

    def __handle_1(self, opcode):
        pass

    def __handle_2(self, opcode):
        pass

    def __handle_3(self, opcode):
        pass

    def __handle_4(self, opcode):
        pass

    def __handle_5(self, opcode):
        pass

    def __handle_6(self, opcode):
        pass

    def __handle_7(self, opcode):
        pass

    def __handle_8(self, opcode):
        pass

    def __handle_9(self, opcode):
        pass

    def __handle_A(self, opcode):
        pass

    def __handle_B(self, opcode):
        pass

    def __handle_C(self, opcode):
        pass

    def __handle_D(self, opcode):
        pass

    def __handle_E(self, opcode):
        pass

    def __handle_F(self, opcode):
        pass
