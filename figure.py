from random import randrange
import pygame
from copy import deepcopy


class Figure:
    def __init__(self, width, height, color, size, chosen_points, board, screen):
        self.left = randrange(0, board.width - 1 - width)  # Левая позиция клетки относительно поля board
        self.top = -height  # Верхняя позиция клетки относительно поля board
        self.width = width  # Ширина фигуры
        self.height = height  # Высота фигуры
        self.board = board  # Поле, на котором будут рисоваться фигуры
        self.screen = screen  # Холст, на котором будут рисоваться фигуры

        # Схема прямоугольника фигуры с закрашенными клетками
        self.field = [[0 for _ in range(self.width)] for _ in range(self.height)]

        self.color = color  # Цвет фигуры
        self.size = size  # Размер клетки
        self.chosen_points = chosen_points  # Выбранные точки внутри прямоугольника
        self.can_move = True  # Состояние, когда фигуру можно двигать

        for point in self.chosen_points:  # Закрашиваем выбранные клетки на поле
            self.field[point[1]][point[0]] = 1

    def copy(self):
        """Копирует себя, но с верхним углом в позиции -2 (для постепенного вывода фигуры на экран)"""
        return Figure(self.width, self.height, self.color, self.size, self.chosen_points, self.board,
                      self.screen)

    def rotate_to_left(self):
        """Поворачивает фигуру на 90 градусов против часовой стрелки"""

        # Если мы не можем двигаться, то ничего не происходит
        if not self.can_move or self.top < 0:
            return

        # Результаты переворота
        field, chosen_points = self.rotate_matrix_to_left(self.width, self.height, self.field)

        for x, y in chosen_points:  # Проверка на возможность поворота
            if y + self.top >= self.board.height or \
                    x + self.left >= self.board.width or \
                    self.board.field[y + self.top][x + self.left]:
                return False

        self.field, self.chosen_points = field, chosen_points  # Обновляем собственные переменные

        # Поле перевернули, то есть ширина и высота должны поменяться местами
        self.width, self.height = self.height, self.width

    def rotate_to_right(self):
        """Поворачивает фигуру на 90 градусов по часовой стрелке.
        Работа функции аналогична работе функции rotate_to_left"""

        if not self.can_move or self.top < 0:
            return False

        # Результаты переворота
        field, chosen_points = self.rotate_matrix_to_right(self.width, self.height, self.field)

        for x, y in chosen_points:  # Проверка на возможность поворота
            if y + self.top >= self.board.height or \
                    x + self.left >= self.board.width or \
                    self.board.field[y + self.top][x + self.left]:
                return False

        self.field, self.chosen_points = field, chosen_points

        self.width, self.height = self.height, self.width

    def move(self):
        """На каждом ходу двигаемся вниз"""
        if self.collide():  # Если мы сталкиваемся с чем-то, то мы не можем двигаться
            return False

        self.top += 1
        return True

    def move_right(self):
        """Двигаем фигуру на одну клетку вправо"""

        # Мы не должны выходить за пределы поля
        if self.top >= 0 and self.can_move and self.left + self.width < self.board.width and not self.collide_from_right():
            self.left += 1

    def move_left(self):
        """Двигаем фигуру на одну клетку влево"""

        if self.top >= 0 and self.can_move and self.left > 0 and not self.collide_from_left():
            self.left -= 1

    def move_down(self):
        """Двигаем фигуру максимально вниз"""

        while not self.collide():  # Пока не происходит столкновения можно двигать фигуру вниз
            self.top += 1

    def draw(self):
        """Вывод фигуры на экран"""

        for coord in self.chosen_points:
            if coord[1] + self.top >= 0:  # Мы не выводим части фигуры, которые расположены вне игрового поля
                x1 = (self.left + coord[0] + self.board.left_space) * self.size
                y1 = (self.top + coord[1] + self.board.top_space) * self.size
                pygame.draw.rect(self.screen, self.color, [x1, y1, self.size, self.size])

    def collide(self):
        if self.top + self.height >= self.board.height:  # Если фигура достигла дна поля

            for x, y in self.chosen_points:  # Заполняем игровое поле
                self.board.field[self.top + y][self.left + x] = 1

            self.can_move = False
            return True

        for x, y in self.chosen_points:
            if self.top + y < 0:  # Если часть фигуры находится за пределом экрана, то она не может ни с чем столкнуться
                continue

            # Если что-то есть под фигурой, то она останавливается
            if self.board.field[self.top + y + 1][self.left + x] == 1:

                # Заполнение поля board
                for x1, y1 in self.chosen_points:
                    self.board.field[self.top + y1][self.left + x1] = 1

                self.can_move = False
                return True

        return False

    def rotate_matrix_to_left(self, width_figure, height_figure, field):
        """Переворачиваем заданную матрицу против часовой стрелки"""
        res = []
        chosen_points = []

        # Создание уже перевернутой матрицы поля
        for col in range(width_figure - 1, -1, -1):
            r = []
            for row in field:
                r.append(row[col])
            res.append(r[:])

        # Заполнения массива с выбранными точками уже новыми координатами
        for x in range(height_figure):
            for y in range(width_figure):
                if res[y][x] == 1:
                    chosen_points.append((x, y))

        return deepcopy(res), deepcopy(chosen_points)

    def rotate_matrix_to_right(self, width_figure, height_figure, field):
        """Поворачивает фигуру на 90 градусов по часовой стрелке.
            Работа функции аналогична работе функции rotate_to_left"""

        res = []
        chosen_points = []

        for col in range(width_figure):
            r = []
            for row in field:
                r.append(row[col])
            res.append(r[::-1])

        for x in range(height_figure):
            for y in range(width_figure):
                if res[y][x] == 1:
                    chosen_points.append((x, y))

        return deepcopy(res), deepcopy(chosen_points)

    def collide_from_right(self):  # Проверка на наличие фигуры справа от заданной
        for x, y in self.chosen_points:
            if self.left + x + 1 < self.board.width and self.board.field[self.top + y][self.left + x + 1] == 1:
                return True

        return False

    def collide_from_left(self):  # Проверка на наличие фигуры слева от заданной
        for x, y in self.chosen_points:
            if self.left + x - 1 >= 0 and self.board.field[self.top + y][self.left + x - 1] == 1:
                return True

        return False