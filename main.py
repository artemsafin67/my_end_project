import pygame
import sys
from copy import deepcopy
from random import choice, randrange

pygame.init()
pygame.mouse.set_visible(False)


class Board:
    def __init__(self, width, height, size, left_space, top_space):
        self.width = width  # Ширина поля
        self.height = height  # Высота поля
        self.field = [[0] * self.width for i in range(self.height)]  # Создание матрицы, описывающей состояние поля
        self.size = size  # Размер клетки
        self.left_space = left_space
        self.top_space = top_space

    def draw(self):
        """Чертит поле"""

        for x in range(self.width + 1):
            start = ((x + self.left_space) * self.size, self.top_space * self.size)
            end = ((x + self.left_space) * self.size, (self.height + self.top_space) * self.size)
            pygame.draw.line(screen, pygame.Color('#423189'), start, end, 3)

        for y in range(self.height + 1):
            start = (self.left_space * self.size, (y + self.top_space) * self.size)
            end = ((self.width + self.left_space) * self.size, (y + self.top_space) * self.size)
            pygame.draw.line(screen, pygame.Color('#423189'), start, end, 3)


class Figure:
    def __init__(self, width, height, color, size, *chosen_points, top=0):
        self.left = randrange(0, board.width - 1 - width)  # Левая позиция клетки относительно поля board
        self.top = top  # Верхняя позиция клетки относительно поля board
        self.width = width  # Ширина фигуры
        self.height = height  # Высота фигуры

        # Схема прямоугольника фигуры с закрашенными клетками
        self.field = [[0 for _ in range(self.width)] for _ in range(self.height)]

        self.color = color  # Цвет фигуры
        self.size = size  # Размер клетки
        self.chosen_points = chosen_points  # Выбранные точки внутри прямоугольника
        self.can_move = True  # Состояние, когда фигуру можно двигать

        for point in self.chosen_points:  # Закрашиваем выбранные клетки на поле
            self.field[point[1]][point[0]] = 1

    def copy(self):
        """Копирует себя, но с верзним углом в позиции -2 (для постепенного вывода фигуры на экран)"""
        return Figure(self.width, self.height, self.color, self.size, *self.chosen_points, top=-2)

    def rotate_to_left(self):
        """Поворачивает фигуру на 90 градусов против часовой стрелки"""

        # Если мы не можем двигаться, то ничего не происходит
        if not self.can_move or self.top < 0:
            return

        # Результаты переворота
        field, chosen_points = rotate_to_left(self.width, self.height, self.field)

        for x, y in chosen_points:  # Проверка на возможность поворота
            if y + self.top >= board.height or \
                    x + self.left >= board.width or \
                    board.field[y + self.top][x + self.left]:
                return False

        self.field, self.chosen_points = field, chosen_points

        # Поле перевернули, то есть ширина и высота должны поменяться местами
        self.width, self.height = self.height, self.width

    def rotate_to_right(self):
        """Поворачивает фигуру на 90 градусов по часовой стрелке.
        Работа функции аналогична работе функции rotate_to_left"""

        if not self.can_move or self.top < 0:
            return False

        # Результаты переворота
        field, chosen_points = rotate_to_right(self.width, self.height, self.field)

        for x, y in chosen_points:  # Проверка на возможность поворота
            if y + self.top >= board.height or \
                    x + self.left >= board.width or \
                    board.field[y + self.top][x + self.left]:
                return False

        self.field, self.chosen_points = field, chosen_points

        self.width, self.height = self.height, self.width

    def move(self):
        if collide(self):
            return False

        self.top += 1
        return True

    def move_right(self):
        """Двигаем фигуру на одну клетку вправо"""

        if self.top >= 0 and self.can_move and self.left + self.width < board.width and not collide_from_right(self):  # Мы не должны выходить за пределы поля
            self.left += 1

    def move_left(self):
        """Двигаем фигуру на одну клетку влево"""

        if self.top >= 0 and self.can_move and self.left > 0 and not collide_from_left(self):
            self.left -= 1

    def move_down(self):
        """Двигаем фигуру максимально вниз"""

        while not collide(self):  # Пока не происходит столкновения можно двигать фигуру вниз
            self.top += 1

    def draw(self):
        """Вывод фигуры на экран"""

        for coord in self.chosen_points:
            if coord[1] + self.top >= 0:  # Мы не выводим части фигуры, которые расположены вне игрового поля
                x1 = (self.left + coord[0] + board.left_space) * self.size
                y1 = (self.top + coord[1] + board.top_space) * self.size
                pygame.draw.rect(screen, self.color, [x1, y1, self.size, self.size])


def terminate():
    """Выход из программы"""

    if int(record) < int(current_score):
        record_file.close()
        new = open('record.txt', 'w')
        new.write(current_score)
        new.close()

    pygame.quit()
    sys.exit()


def update_display():
    """Обновление игрового поля"""

    global current_level_label, current_score_label  # Переменные - информаторы

    screen.fill(pygame.Color('white'))

    # Обновляем текущие результаты
    current_score_label = font.render('Счёт: ' + current_score, 1, pygame.Color('#42aaff'))
    current_level_label = font.render('Уровень: ' + current_level, 1, pygame.Color('green'))

    # Рисуем текущие результаты
    screen.blit(record_label, (1000, 100))
    screen.blit(current_score_label, (1000, 300))
    screen.blit(current_level_label, (1000, 500))

    # Рисуем использованные фигуры
    for figure in used_figures:
        figure.draw()

    # Рисуем текущую фигуру
    current_figure.draw()

    # Рисуем поле
    board.draw()

    pygame.display.update()


def rotate_to_left(width_figure, height_figure, field):
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


def rotate_to_right(width_figure, height_figure, field):
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


def collide(figure):
    if figure.top + figure.height >= board.height:  # Если фигура достигла дна поля

        for x, y in figure.chosen_points:  # Заполняем игровое поле
            board.field[figure.top + y][figure.left + x] = 1

        figure.can_move = False
        return True

    for x, y in figure.chosen_points:
        if figure.top + y < 0:  # Если часть фигуры находится за пределом экрана, то она не может ни с чем столкнуться
            continue

        # Если что-то есть под фигурой, то она останавливается
        if board.field[figure.top + y + 1][figure.left + x] == 1:

            # Заполнение поля board
            for x1, y1 in figure.chosen_points:
                board.field[figure.top + y1][figure.left + x1] = 1

            figure.can_move = False
            return True

    return False


def collide_from_right(figure):  # Проверка на наличие фигуры справа от заданной
    for x, y in figure.chosen_points:
        if figure.left + x + 1 < board.width and board.field[figure.top + y][figure.left + x + 1] == 1:
            return True

    return False


def collide_from_left(figure):  # Проверка на наличие фигуры слева от заданной
    for x, y in figure.chosen_points:
        if figure.left + x - 1 >= 0 and board.field[figure.top + y][figure.left + x - 1] == 1:
            return True

    return False


def check_field():
    """Проверка на заполнение полной линии фигурами"""

    global current_score  # Переменная для изменения текущего результата

    to_del = []  # В этом списке хранятся номера строк для удаления

    for row in range(board.height):
        if 0 not in board.field[row]:  # Если все элементы заполнены
            to_del.append(row)

            for figure in used_figures:
                # В фигуре остаются только квадратики, не принадлежащие удаленной линии
                figure.chosen_points = list(filter(lambda point: point[1] + figure.top != row, figure.chosen_points))

                # Если вершина фигуры находится выше удаленной линии, то надо сдвинуть её на ряд вниз
                if figure.top < row:
                    for ind in range(len(figure.chosen_points)):
                        x, y = figure.chosen_points[ind]
                        if y + figure.top > row:  # Если часть фигуры находится ниже удаленной линии
                            figure.chosen_points[ind] = [x, y - 1]  # Она поднимается вверх, т.е. приближается к верху
                    figure.top += 1  # Опускаем низ на один элемент

    current_score = str(int(current_score) + len(to_del) ** 2 * 10)

    # Проигрываем мелолию
    if to_del:
        ended_string_sound.play()

    for el in to_del:  # Удаляем заполненные строки и добавляем пустые сверху
        del board.field[el]
        board.field.insert(0, [0] * board.width)


def check_to_lose():
    """Проверка на проигрыш"""

    if 1 in board.field[0]:  # Если часть фигуры содержится на верхней линии
        # Проигрываем мелодии
        lose_sound.play()
        pygame.mixer.music.stop()

        lose_font = pygame.font.Font(None, 150)
        lose_label = lose_font.render('You lost!', 1, pygame.Color('pink'))

        screen.blit(lose_label, (750, 400))
        pygame.display.update()

        if int(record) < int(current_score):
            record_file.close()
            new = open('record.txt', 'w')
            new.write(current_score)
            new.close()

        pygame.time.delay(6000)
        terminate()


size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Тетрис')

clock = pygame.time.Clock()
fps = 200
frames_done = 0

current_level = '1'
figure_added = 0

board = Board(10, 20, 40, 10, 1)

# Загружаем мелодии
lose_sound = pygame.mixer.Sound('sounds/lose.wav')
figure_down_sound = pygame.mixer.Sound('sounds/figure_down.wav')
ended_string_sound = pygame.mixer.Sound('sounds/ended_string.wav')
pygame.mixer.music.load('sounds/background_music.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.25)



# Создаём образцы фигур
square = Figure(2, 2, pygame.Color('yellow'), board.size, (0, 0), (1, 0), (0, 1), (1, 1))
stick = Figure(1, 4, pygame.Color('#42aaff'), board.size, (0, 0), (0, 1), (0, 2), (0, 3))
something_left = Figure(3, 2, pygame.Color('red'), board.size, (0, 1), (1, 1), (1, 0), (2, 0))
something_right = Figure(3, 2, pygame.Color('green'), board.size, (0, 0), (1, 0), (1, 1), (2, 1))
t_letter = Figure(3, 2, pygame.Color('purple'), board.size, (0, 0), (1, 0), (2, 0), (1, 1))
l_letter_left = Figure(2, 3, pygame.Color('pink'), board.size, (0, 0), (0, 1), (0, 2), (1, 2))
l_letter_right = Figure(2, 3, pygame.Color('orange'), board.size, (1, 0), (1, 1), (1, 2), (0, 2))

# Из этого списка будут выбираться фигуры для вывода на экран
possible_figures = [square, stick, something_left, something_right, t_letter, l_letter_left,
                    l_letter_right]

font = pygame.font.Font(None, 50)

# Загружаем данные прошлых игр
record_file = open('record.txt')
record = record_file.read()
current_score = '0'

# Создаём окна для вывода информации
record_label = font.render('Рекорд: ' + record, 1, pygame.Color('red'))
current_score_label = font.render('Счёт: ' + current_score, 1, pygame.Color('#42aaff'))
current_level_label = font.render('Уровень: ' + current_level, 1, pygame.Color('green'))

used_figures = []  # Хранит использованные фигуры

let_next_figure = False  # Флаг, обозначающий возможность запустить новую фигуру

current_figure = choice(possible_figures).copy()  # Выбираем текущую фигуру
current_figure.top = -current_figure.height
update_display()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # Двигаем фигуру влево
                current_figure.move_left()
                update_display()

            if event.key == pygame.K_RIGHT:  # Двигаем фигуру вправо
                current_figure.move_right()
                update_display()

            if event.key == pygame.K_DOWN:  # Двигаем фигуру вниз
                current_figure.move_down()
                update_display()

            if event.key == pygame.K_a:  # Поворачиваем фигуру на 90 градусов против часовой
                current_figure.rotate_to_left()
                update_display()

            if event.key == pygame.K_s:   # Поворачиваем фигуру на 90 градусов по часовой
                current_figure.rotate_to_right()
                update_display()

    if frames_done >= 200:  # Каждые 200 итераций обновляем картинку
        if not current_figure.move():  # Если мы не можем никуда пойти, то появляется новая фигура
            used_figures.append(current_figure)
            let_next_figure = True
            figure_down_sound.play()  # Проигрываем звук

            figure_added += 1
            if figure_added % int(current_level) ** 2 == 0:  # Увеличиваем уровень
                current_level = str(int(current_level) + 1)
                figure_added = 0

        check_field()
        update_display()
        check_to_lose()
        frames_done = 0

    if let_next_figure:
        current_figure = choice(possible_figures).copy()
        current_figure.top = -current_figure.height
        let_next_figure = False
        update_display()

    clock.tick(fps)
    frames_done += int(current_level)