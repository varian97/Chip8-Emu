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
