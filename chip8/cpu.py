import random
from .display import Display
from .audio import Audio
from .keyboard import Keyboard

class CPU:
    def __init__(self, keyboard: Keyboard, audio: Audio, display: Display) -> None:
        self.instructions_per_cycle = 10
        self.rom_file = None

        self.keyboard = keyboard
        self.audio = audio
        self.display = display

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

        self.paused = False
        self.register_for_waiting_key = None

        self.sprites = [
            0xf0, 0x90, 0x90, 0x90, 0xf0,  # 0
            0x20, 0x60, 0x20, 0x20, 0x70,  # 1
            0xf0, 0x10, 0xf0, 0x80, 0xf0,  # 2
            0xf0, 0x10, 0xf0, 0x10, 0xf0,  # 3
            0x90, 0x90, 0xf0, 0x10, 0x10,  # 4
            0xf0, 0x80, 0xf0, 0x10, 0xf0,  # 5
            0xf0, 0x80, 0xf0, 0x90, 0xf0,  # 6
            0xf0, 0x10, 0x20, 0x40, 0x40,  # 7
            0xf0, 0x90, 0xf0, 0x90, 0xf0,  # 8
            0xf0, 0x90, 0xf0, 0x10, 0xf0,  # 9
            0xf0, 0x90, 0xf0, 0x90, 0x90,  # A
            0xe0, 0x90, 0xe0, 0x90, 0xe0,  # B
            0xf0, 0x80, 0x80, 0x80, 0xf0,  # C
            0xe0, 0x90, 0x90, 0x90, 0xe0,  # D
            0xf0, 0x80, 0xf0, 0x80, 0xf0,  # E
            0xf0, 0x80, 0xf0, 0x80, 0x80,  # F
        ]

        for i in range(len(self.sprites)):
            self.memory[i] = self.sprites[i]

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

    def is_rom_loaded(self) -> bool:
        return self.rom_file is not None

    def load_rom_into_memory(self, filepath):
        with open(filepath, 'rb') as infile:
            counter = 0
            while byte := infile.read(1):
                self.memory[counter + 0x200] = int.from_bytes(byte, 'big')
                counter += 1
        self.rom_file = filepath

    def cycle(self):
        for _ in range(self.instructions_per_cycle):
            if not self.paused:
                opcode = self.fetch_instruction()
                self.run_instruction(opcode)

        if not self.paused:
            self.update_timers()

        self.play_audio()

    def fetch_instruction(self):
        first_byte = self.memory[self.pc]
        second_byte = self.memory[self.pc + 1]
        opcode = (first_byte << 8) | second_byte

        return opcode

    def run_instruction(self, opcode):
        prefix = opcode >> 12
        func = self.func_pointer[prefix]
        if func:
            func(opcode=opcode)

    def update_timers(self):
        if self.sound_timer > 0:
            self.sound_timer -= 1
        if self.delay_timer > 0:
            self.delay_timer -= 1

    def play_audio(self):
        if self.sound_timer > 0:
            self.audio.play()
        else:
            self.audio.stop()

    def handle_keyboard_press_callback(self, key: int) -> None:
        self.v[self.register_for_waiting_key] = key
        self.register_for_waiting_key = None
        self.paused = False
        self.pc += 2

    def __handle_0(self, opcode):
        # 0x0nnn ignored for most modern interpreter
        if opcode == 0x00e0:
            self.display.clear_display()
            self.pc += 2
        elif opcode == 0x00ee:
            self.pc = self.stack.pop()
            pass

    def __handle_1(self, opcode):
        self.pc = (opcode & 0xfff)

    def __handle_2(self, opcode):
        self.stack.append(self.pc + 2)
        self.pc = (opcode & 0xfff)

    def __handle_3(self, opcode):
        x = (opcode >> 8) & 0xf
        kk = (opcode & 0xff)
        if self.v[x] == kk:
            self.pc += 2
        self.pc += 2

    def __handle_4(self, opcode):
        x = (opcode >> 8) & 0xf
        kk = (opcode & 0xff)
        if self.v[x] != kk:
            self.pc += 2
        self.pc += 2

    def __handle_5(self, opcode):
        x = (opcode >> 8) & 0xf
        y = (opcode >> 4) & 0xf
        if self.v[x] == self.v[y]:
            self.pc += 2
        self.pc += 2

    def __handle_6(self, opcode):
        x = (opcode >> 8) & 0xf
        kk = (opcode & 0xff)
        self.v[x] = kk
        self.pc += 2

    def __handle_7(self, opcode):
        x = (opcode >> 8) & 0xf
        kk = (opcode & 0xff)
        total = (self.v[x] + kk) & 0xff
        self.v[x] = total
        self.pc += 2

    def __handle_8(self, opcode):
        x = (opcode >> 8) & 0xf
        y = (opcode >> 4) & 0xf

        nibble = opcode & 0xf
        if nibble == 0:
            self.v[x] = self.v[y]
        elif nibble == 1:
            self.v[x] |= self.v[y]
        elif nibble == 2:
            self.v[x] &= self.v[y]
        elif nibble == 3:
            self.v[x] ^= self.v[y]
        elif nibble == 4:
            self.v[0xf] = 0
            total = self.v[x] + self.v[y]
            if total > 0xff:
                self.v[0xf] = 1
            self.v[x] = total & 0xff
        elif nibble == 5:
            self.v[0xf] = (self.v[x] > self.v[y])
            diff = self.v[x] - self.v[y]
            if diff < 0:
                diff += 256
            self.v[x] = diff
        elif nibble == 6:
            self.v[0xf] = (self.v[x] & 0x1)
            self.v[x] >>= 1
        elif nibble == 7:
            self.v[0xf] = (self.v[y] > self.v[x])
            diff = self.v[y] - self.v[x]
            if diff < 0:
                diff += 256
            self.v[x] = diff
        else:  # 8xyE
            self.v[0xf] = (self.v[x] & 0x80)
            self.v[x] <<= 1
            self.v[x] &= 0xff

        self.pc += 2

    def __handle_9(self, opcode):
        x = (opcode >> 8) & 0xf
        y = (opcode >> 4) & 0xf

        if self.v[x] != self.v[y]:
            self.pc += 2
        self.pc += 2

    def __handle_A(self, opcode):
        self.i = (opcode & 0xfff)
        self.pc += 2

    def __handle_B(self, opcode):
        self.pc = (opcode & 0xfff) + self.v[0]

    def __handle_C(self, opcode):
        x = (opcode >> 8) & 0xf
        kk = (opcode & 0xff)
        self.v[x] = kk & random.randint(0, 255)
        self.pc += 2

    def __handle_D(self, opcode):
        x = (opcode >> 8) & 0xf
        y = (opcode >> 4) & 0xf
        n = opcode & 0xf

        base_x = self.v[x] % self.display.cols
        base_y = self.v[y] % self.display.rows
        self.v[0xf] = 0

        for height in range(n):
            b = self.memory[self.i + height]

            for width in range(8):
                x_pos = base_x + width
                y_pos = base_y + height
                if ((0x80 & b) > 0) and x_pos < self.display.cols and y_pos < self.display.rows:
                    erased = self.display.set_pixel(x_pos, y_pos)
                    self.v[0xf] |= erased
                b <<= 1

        self.pc += 2

    def __handle_E(self, opcode):
        x = (opcode >> 8) & 0xf
        second_byte = opcode & 0xff
        if second_byte == 0x9e:
            if self.keyboard.is_key_pressed(self.v[x]):
                self.pc += 2
        else:  # ExA1
            if not self.keyboard.is_key_pressed(self.v[x]):
                self.pc += 2

        self.pc += 2

    def __handle_F(self, opcode):
        x = (opcode >> 8) & 0xf
        second_byte = opcode & 0xff

        if second_byte == 0x07:
            self.v[x] = self.delay_timer
            self.pc += 2
        elif second_byte == 0x0a:
            self.paused = True
            self.register_for_waiting_key = x
        elif second_byte == 0x15:
            self.delay_timer = self.v[x]
            self.pc += 2
        elif second_byte == 0x18:
            self.sound_timer = self.v[x]
            self.pc += 2
        elif second_byte == 0X1e:
            self.i += self.v[x]
            self.pc += 2
        elif second_byte == 0x29:
            self.i = self.v[x] * 5
            self.pc += 2
        elif second_byte == 0x33:
            self.memory[self.i] = self.v[x] / 100
            self.memory[self.i + 1] = (self.v[x] % 100) // 10
            self.memory[self.i + 2] = self.v[x] % 10
            self.pc += 2
        elif second_byte == 0x55:
            for i in range(x + 1):
                self.memory[self.i + i] = self.v[i]
            self.pc += 2
        else:  # Fx65
            for i in range(x + 1):
                self.v[i] = self.memory[self.i + i]
            self.pc += 2
