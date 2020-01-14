import pygame

pygame.init()


class Button:
    def __init__(self, func, x, y, width, height, text, size, color, screen, *args, bg_color=None, border_color=None):
        # Инициализируем координаты и размеры кнопки
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Инициализируем характеристики внешенего вида
        self.text = text
        self.size = size
        self.color = color
        self.bg_color = bg_color
        self.border_color = border_color

        # Функция для запуска по нажатию кнопки
        self.func = func
        self.args = args

        # Создание холстов для вывода на экран
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, self.size)
        self.label = self.font.render(self.text, 1, self.color, self.bg_color)

    def change_text(self, setting, meaning):
        # Меняем текст кнопки по заданному значению параметра
        self.text = setting + ': ' + meaning
        self.label = self.font.render(self.text, 1, self.color, self.bg_color)

    def check(self, x, y):
        """Проверка на нажатие кнопки"""
        if self.rect.collidepoint(x, y):
            if self.func:  # Если у кнопки есть функция
                self.func(*self.args)  # Запуск функции
            return True

    def draw_button(self):
        """Рисуем кнопку"""
        self.screen.blit(self.label, (self.x, self.y))

        if self.border_color:  # Если надо рисовать границу
            pygame.draw.lines(self.screen, self.border_color, True,
                              [(self.x, self.y), (self.x + self.width, self.y),
                               (self.x + self.width, self.y + self.height), (self.x, self.y + self.height)])
