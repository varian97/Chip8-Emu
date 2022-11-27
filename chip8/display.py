import pygame

class Display:

    def __init__(self, scale: int) -> None:
        self.rows = 32
        self.cols = 64

        self.height = self.rows * scale
        self.width = self.cols * scale
        self.scale = scale
        self.logic_surface = [[0] * self.width for _ in range(self.height)]

    def start(self):
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.surface.fill((0, 0, 0))

    def clear_display(self):
        self.surface.fill((0, 0, 0))
        for i in range(self.height):
            for j in range(self.width):
                self.logic_surface[i][j] = 0

    def set_pixel(self, x: int, y: int) -> None:
        _x = x * self.scale
        _y = y * self.scale

        rect = pygame.Rect(_x, _y, self.scale, self.scale)

        self.logic_surface[_y][_x] ^= 1
        if self.logic_surface[_y][_x] == 0:
            self.surface.fill((0, 0, 0), rect)
        else:
            self.surface.fill((255, 255, 255), rect)

        return self.logic_surface[_y][_x] == 0

    def update_display(self):
        pygame.display.update()
