import pygame


class Board:
    def __init__(self, width, height, size, left_space, top_space, screen):
        self.width = width  # Ширина поля
        self.height = height  # Высота поля
        self.field = [[0] * self.width for i in range(self.height)]  # Создание матрицы, описывающей состояние поля
        self.size = size  # Размер клетки
        self.left_space = left_space
        self.top_space = top_space
        self.screen = screen  # Поле для черчения

    def draw(self):
        """Чертит поле"""

        for x in range(self.width + 1):
            start = ((x + self.left_space) * self.size, self.top_space * self.size)
            end = ((x + self.left_space) * self.size, (self.height + self.top_space) * self.size)
            pygame.draw.line(self.screen, pygame.Color('#423189'), start, end, 3)

        for y in range(self.height + 1):
            start = (self.left_space * self.size, (y + self.top_space) * self.size)
            end = ((self.width + self.left_space) * self.size, (y + self.top_space) * self.size)
            pygame.draw.line(self.screen, pygame.Color('#423189'), start, end, 3)
