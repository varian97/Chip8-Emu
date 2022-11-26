import pygame

class Display:

    def __init__(self, height: int, width: int, scale: int) -> None:
        self.height = height * scale
        self.width = width * scale
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
        pygame.display.update()

    def set_pixel(self, x: int, y: int, val:int) -> None:
        erased = False
        _x = x * self.scale
        _y = y * self.scale

        if _x > self.width - 1:
            _x -= self.width
        elif x < 0:
            _x += self.width

        if _y > self.height - 1:
            _y -= self.height
        elif y < 0:
            _y += self.height

        rect = pygame.Rect(_x, _y, self.scale, self.scale)

        if self.logic_surface[_y][_x] == 1 and val == 1:
            self.logic_surface[_y][_x] = 0
            self.surface.fill((0, 0, 0), rect)
            erased = True
        if self.logic_surface[_y][_x] == 0 and val == 1:
            self.logic_surface[_y][_x] = 1
            self.surface.fill((255, 255, 255), rect)

        pygame.display.update()
        return erased
