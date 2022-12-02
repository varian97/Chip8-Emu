import pygame

from chip8.emulator import Emulator

pygame.init()
pygame.display.set_caption('Chip8 Emulator')
clock = pygame.time.Clock()

if __name__ == '__main__':
    emulator = Emulator()
    emulator.start()
    emulator.loop()
