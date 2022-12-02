import pygame
import tkinter
import tkinter.filedialog

from chip8.cpu import CPU
from chip8.audio import Audio
from chip8.display import Display
from chip8.keyboard import Keyboard

class Emulator:

    def __init__(self) -> None:
        self.running = False

        self.display = Display(scale=10)
        self.keyboard = Keyboard()
        self.audio = Audio()
        self.cpu = CPU(audio=self.audio, keyboard=self.keyboard, display=self.display)
        self.clock = None

    def prompt_file(self) -> None:
        top = tkinter.Tk()
        top.withdraw()

        file_name = tkinter.filedialog.askopenfilename(parent=top)
        top.destroy()

        return file_name

    def handle_event(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    rom_file = self.prompt_file()
                    if rom_file:
                        self.cpu.reset(rom_file)
                else:
                    self.keyboard.on_key_pressed(event.key)
                    if self.cpu.paused and event.key in self.keyboard.KEYMAP:
                        self.cpu.handle_keyboard_press_callback(event.key)
            if event.type == pygame.KEYUP:
                self.keyboard.on_key_released(event.key)

    def start(self) -> None:
        self.running = True
        self.display.start()
        self.display.draw_welcome_screen()
        self.clock = pygame.time.Clock()

    def loop(self) -> None:
        while self.running:
            self.clock.tick(60)

            if self.cpu.is_rom_loaded():
                self.cpu.cycle()

            self.handle_event()

            self.display.update_display()
