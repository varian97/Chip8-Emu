import pygame

class Keyboard:
    def __init__(self):
        self.KEYMAP = {
            pygame.K_1: 1,
            pygame.K_2: 2,
            pygame.K_3: 3,
            pygame.K_4: 0xc,

            pygame.K_q: 4,
            pygame.K_w: 5,
            pygame.K_e: 6,
            pygame.K_r: 0xd,

            pygame.K_a: 7,
            pygame.K_s: 8,
            pygame.K_d: 9,
            pygame.K_f: 0xe,

            pygame.K_z: 0xa,
            pygame.K_x: 0,
            pygame.K_c: 0xb,
            pygame.K_v: 0xf,
        }

        self.pressed_key = set()

    def is_key_pressed(self, chip8_key: int) -> bool:
        return chip8_key in self.pressed_key

    def on_key_pressed(self, pygame_key: int) -> None:
        if pygame_key in self.KEYMAP:
            self.pressed_key.add(self.KEYMAP[pygame_key])

    def on_key_released(self, pygame_key: int) -> None:
        if pygame_key in self.KEYMAP:
            self.pressed_key.remove(self.KEYMAP[pygame_key])
