import pygame
import tkinter
import tkinter.filedialog

from chip8.cpu import CPU
from chip8.audio import Audio
from chip8.display import Display
from chip8.keyboard import Keyboard

pygame.init()
pygame.display.set_caption('Chip8 Emulator')
clock = pygame.time.Clock()

def prompt_file():
    top = tkinter.Tk()
    top.withdraw()

    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()

    return file_name

if __name__ == '__main__':
    running = True
    rom_file = None

    display = Display(scale=10)
    keyboard = Keyboard()
    audio = Audio()
    cpu = CPU(audio=audio, keyboard=keyboard, display=display)

    display.start()
    display.draw_welcome_screen()

    while running:
        clock.tick(60)

        if cpu.is_rom_loaded():
            cpu.cycle()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    rom_file = prompt_file()
                    cpu.load_rom_into_memory(rom_file)
                    display.start()
                else:
                    keyboard.on_key_pressed(event.key)
                    if cpu.paused:
                        cpu.handle_keyboard_press_callback(event.key)
            if event.type == pygame.KEYUP:
                keyboard.on_key_released(event.key)

        display.update_display()
