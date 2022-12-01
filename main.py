import pygame

from chip8.cpu import CPU
from chip8.audio import Audio
from chip8.display import Display
from chip8.keyboard import Keyboard

pygame.init()
pygame.display.set_caption('Chip8 Emulator')
clock = pygame.time.Clock()

if __name__ == '__main__':
    running = True

    display = Display(scale=10)
    keyboard = Keyboard()
    audio = Audio()
    cpu = CPU(audio=audio, keyboard=keyboard, display=display)

    cpu.load_rom_into_memory('./roms/SpaceInvaders.ch8')
    display.start()

    while running:
        cpu.cycle()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                keyboard.on_key_pressed(event.key)
                if cpu.paused:
                    cpu.handle_keyboard_press_callback(event.key)
            if event.type == pygame.KEYUP:
                keyboard.on_key_released(event.key)

        clock.tick(60)
