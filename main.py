import pygame

from chip8.cpu import CPU
from chip8.display import Display

pygame.init()
pygame.display.set_caption('Chip8 Emulator')

if __name__ == '__main__':
    running = True

    display = Display(32, 64, 10)
    display.start()

    cpu = CPU(None, None, display=display)
    cpu.load_rom_into_memory('./roms/Blitz.ch8')

    while running:
        cpu.cycle()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
