import pygame
import time

from chip8.cpu import CPU
from chip8.display import Display
from chip8.keyboard import Keyboard

pygame.init()
pygame.display.set_caption('Chip8 Emulator')

if __name__ == '__main__':
    running = True

    cycle_clock = 1 / 60
    previous = None

    display = Display(32, 64, 10)
    keyboard = Keyboard()
    cpu = CPU(sound=None, keyboard=keyboard, display=display)

    cpu.load_rom_into_memory('./roms/Blitz.ch8')
    display.start()

    while running:
        now = time.time()
        if previous is not None and now - previous > cycle_clock:
            cpu.cycle()
            previous = now
        elif previous is None:
            cpu.cycle()
            previous = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                keyboard.on_key_pressed(event.key)
                if cpu.paused:
                    cpu.handle_keyboard_press_callback(event.key)
            if event.type == pygame.KEYUP:
                keyboard.on_key_released(event.key)
