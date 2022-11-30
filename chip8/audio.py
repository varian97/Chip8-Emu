import pygame
import numpy as np

pygame.mixer.init(size=32)

class Audio:

    def __init__(self) -> None:
        buffer = np.sin(2 * np.pi * np.arange(44100) * 440 / 44100).astype(np.float32)
        self.sound = pygame.mixer.Sound(buffer)

    def play(self) -> None:
        self.sound.play(0)

    def stop(self):
        self.sound.stop()
