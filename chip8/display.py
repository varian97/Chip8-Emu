import pygame

class Display:

    def __init__(self, height: int, width: int, scale: int) -> None:
        self.height = height * scale
        self.width = width * scale
        self.scale = scale

    def start(self):
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.surface.fill((255, 255, 255))

    def clear_display(self):
        self.surface.fill((255, 255, 255))
        pygame.display.update()

    def set_pixel(self, color, x: int, y: int) -> None:
        rect = pygame.Rect(x, y, self.scale, self.scale)
        self.surface.fill(color, rect)
        pygame.display.update()
