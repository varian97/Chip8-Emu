import pygame

K_WHITE = (255, 255, 255)
K_BLACK = (0, 0, 0)


class Display:

    def __init__(self, scale: int) -> None:
        self.rows = 32
        self.cols = 64

        self.height = self.rows * scale
        self.width = self.cols * scale
        self.scale = scale
        self.logic_surface = [[0] * self.width for _ in range(self.height)]

    def start(self) -> None:
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.surface.fill(K_BLACK)

    def draw_welcome_screen(self) -> None:
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Chip 8 Emulator', True, K_WHITE)

        font = pygame.font.Font('freesansbold.ttf', 14)
        text2 = font.render('by varian97', True, K_WHITE)

        font = pygame.font.Font('freesansbold.ttf', 20)
        text3 = font.render('Press Space to Load ROM', True, K_WHITE)

        text_rect = text.get_rect()
        text_rect2 = text2.get_rect()
        text_rect3 = text3.get_rect()

        text_rect.center = (self.width // 2, 70)
        text_rect2.center = (self.width // 2, 100)
        text_rect3.center = (self.width // 2, self.height // 2 + 50)

        self.surface.blit(text, text_rect)
        self.surface.blit(text2, text_rect2)
        self.surface.blit(text3, text_rect3)

    def clear_display(self) -> None:
        self.surface.fill(K_BLACK)
        for i in range(self.height):
            for j in range(self.width):
                self.logic_surface[i][j] = 0

    def set_pixel(self, x: int, y: int) -> None:
        _x = x * self.scale
        _y = y * self.scale

        rect = pygame.Rect(_x, _y, self.scale, self.scale)

        self.logic_surface[_y][_x] ^= 1
        if self.logic_surface[_y][_x] == 0:
            self.surface.fill(K_BLACK, rect)
        else:
            self.surface.fill(K_WHITE, rect)

        return self.logic_surface[_y][_x] == 0

    def update_display(self) -> None:
        pygame.display.update()
