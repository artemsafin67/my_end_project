def game(screen, settings):
    """Функция, которая запускает игру"""
    import pygame
    from figure import Figure
    from board import Board
    from random import choice
    import sys

    pygame.init()

    width, height = 1200, 600

    # Читаем правила и определяем глобальные параметры
    for opt, key in settings.items():
        if opt == 'music':
            if key == 'Да':
                play_music = True
            else:
                play_music = False

        # Other options

    def terminate(kill=False):
        """Выход из программы"""
        nonlocal running

        if int(record) < int(current_score):
            record_file.close()
            new = open('record.txt', 'w')
            new.write(current_score)
            new.close()

        running = False
        if kill:
            pygame.quit()
            sys.exit()

    def update_display():
        """Обновление игрового поля"""

        nonlocal current_level_label, current_score_label  # Переменные - информаторы

        screen.fill(pygame.Color('white'))

        # Обновляем текущие результаты
        current_score_label = font.render('Счёт: ' + current_score, 1, pygame.Color('#42aaff'))
        current_level_label = font.render('Уровень: ' + current_level, 1, pygame.Color('green'))

        # Рисуем текущие результаты
        x_coord = (board.left_space + board.width) * board.size + 50

        screen.blit(record_label, (x_coord, 210))
        screen.blit(current_score_label, (x_coord, 330))
        screen.blit(current_level_label, (x_coord, 450))

        # Рисуем следующую фигуру
        figure_to_draw.draw_next_in_the_rect(x_coord + 75, board.size * 2)
        board_to_draw_figure_on = Board(figure_to_draw.width, figure_to_draw.height,
                                        figure_to_draw.size, x_coord + 75, board.size * 2, figure_to_draw.screen, True)
        board_to_draw_figure_on.draw()

        # Рисуем использованные фигуры
        for figure in used_figures:
            figure.draw()

        # Рисуем текущую фигуру
        current_figure.draw()

        # Рисуем поле
        board.draw()

        pygame.display.update()

    def check_field():
        """Проверка на заполнение полной линии фигурами"""

        nonlocal current_score  # Переменная для изменения текущего результата

        to_del = []  # В этом списке хранятся номера строк для удаления

        for row in range(board.height):
            if 0 not in board.field[row]:  # Если все элементы заполнены
                to_del.append(row)

                for figure in used_figures:
                    # В фигуре остаются только квадратики, не принадлежащие удаленной линии
                    figure.chosen_points = list(
                        filter(lambda point: point[1] + figure.top != row, figure.chosen_points))

                    # Если вершина фигуры находится выше удаленной линии, то надо сдвинуть её на ряд вниз
                    if figure.top < row:
                        for ind in range(len(figure.chosen_points)):
                            x, y = figure.chosen_points[ind]
                            if y + figure.top > row:  # Если часть фигуры находится ниже удаленной линии
                                figure.chosen_points[ind] = [x,
                                                             y - 1]  # Она поднимается вверх, т.е. приближается к верху
                        figure.top += 1  # Опускаем низ на один элемент

        # В зависимости от количества удаленных линий зачисляем пользователю очки
        if len(to_del) == 1:
            current_score = str(int(current_score) + 10)
        if len(to_del) == 2:
            current_score = str(int(current_score) + 30)
        if len(to_del) == 3:
            current_score = str(int(current_score) + 60)
        if len(to_del) == 4:
            current_score = str(int(current_score) + 100)

        # Проигрываем мелолию, если параметр play_music стоит в позиции True
        if to_del and play_music:
            ended_string_sound.play()

        for el in to_del:  # Удаляем заполненные строки и добавляем пустые сверху
            del board.field[el]
            board.field.insert(0, [0] * board.width)

    def check_to_lose():
        """Проверка на проигрыш"""

        if 1 in board.field[0]:  # Если часть фигуры содержится на верхней линии

            # Проигрываем мелодии
            if play_music:
                lose_sound.play()
                pygame.mixer.music.stop()

            # Выводим сообщение о проигрыше
            lose_font = pygame.font.Font(None, 150)
            lose_label = lose_font.render('You lost!', 1, pygame.Color('pink'))

            screen.blit(lose_label, (width // 2 - 200, height // 2 - 100))
            pygame.display.update()

            # Если мы побили рекорд, то обновляем его
            if int(record) < int(current_score):
                record_file.close()
                new_record_file = open('record.txt', 'w')
                new_record_file.write(current_score)
                new_record_file.close()

            # Ждём 6 секунд для проигрывания мелодии
            pygame.time.delay(6000)
            terminate()

    def manage_with_event(event):
        # В зависимости от типа события двигаем фигуру

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

        if event.key == pygame.K_s:  # Поворачиваем фигуру на 90 градусов по часовой
            current_figure.rotate_to_right()
            update_display()

    clock = pygame.time.Clock()
    fps = 200
    frames_done = 0

    current_level = '1'
    figure_added = 0

    board = Board(10, 20, 25, 3, 1, screen)

    # Загружаем мелодии
    lose_sound = pygame.mixer.Sound('sounds/lose.wav')
    figure_down_sound = pygame.mixer.Sound('sounds/figure_down.wav')
    ended_string_sound = pygame.mixer.Sound('sounds/ended_string.wav')
    pygame.mixer.music.load('sounds/background_music.wav')

    if play_music:
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.25)

    # Создаём образцы фигур
    square = Figure(2, 2, pygame.Color('yellow'), 'y', board.size, [(0, 0), (1, 0), (0, 1), (1, 1)], board, screen)
    stick = Figure(1, 4, pygame.Color('#42aaff'), 'b', board.size, [(0, 0), (0, 1), (0, 2), (0, 3)], board, screen)
    something_left = Figure(3, 2, pygame.Color('red'), 'r', board.size, [(0, 1), (1, 1), (1, 0), (2, 0)], board, screen)
    something_right = Figure(3, 2, pygame.Color('green'), 'g', board.size, [(0, 0), (1, 0), (1, 1), (2, 1)], board, screen)
    t_letter = Figure(3, 2, pygame.Color('purple'), 'p', board.size, [(0, 0), (1, 0), (2, 0), (1, 1)], board, screen)
    l_letter_left = Figure(2, 3, pygame.Color('pink'), 'pi', board.size, [(0, 0), (0, 1), (0, 2), (1, 2)], board, screen)
    l_letter_right = Figure(2, 3, pygame.Color('orange'), 'o', board.size, [(1, 0), (1, 1), (1, 2), (0, 2)], board, screen)

    # Из этого списка будут выбираться фигуры для вывода на экран
    possible_figures = [square, stick, something_left, something_right, t_letter, l_letter_left,
                        l_letter_right]

    # Загружаем данные прошлых игр
    record_file = open('record.txt')
    record = record_file.read()
    current_score = '0'

    # Создаём окна для вывода информации
    font = pygame.font.Font(None, 50)
    record_label = font.render('Рекорд: ' + record, 1, pygame.Color('red'))
    current_score_label = font.render('Счёт: ' + current_score, 1, pygame.Color('#42aaff'))
    current_level_label = font.render('Уровень: ' + current_level, 1, pygame.Color('green'))

    used_figures = []  # Хранит использованные фигуры

    let_next_figure = False  # Флаг, обозначающий возможность запустить новую фигуру

    current_figure = choice(possible_figures).copy()  # Выбираем текущую фигуру
    figure_to_draw = choice(possible_figures).copy()  # Выбираем фигуру для отрисовки в отдельной части экрана
    update_display()

    running = True
    while running:  # Основной игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate(True)

            if event.type == pygame.KEYDOWN:
                manage_with_event(event)

        if frames_done >= 200:  # Каждые 200 итераций обновляем картинку

            # Если мы не можем никуда пойти, то появляется новая фигура
            if not (current_figure.can_move and current_figure.move()):
                used_figures.append(current_figure)  # Добавляем фигуру в список для отрисовки
                let_next_figure = True  # Ждём новую фигуру

                # Проигрываем мелодию
                if play_music:
                    figure_down_sound.play()

                figure_added += 1  # Количество фигур увеличивается
                current_score = str(int(current_score) + 1)  # За каждую фигуру + одно очко

                if figure_added % int(current_level) ** 2 == 0:  # Увеличиваем уровень через определенное число фигур
                    current_level = str(int(current_level) + 1)
                    figure_added = 0

            check_field()  # Проверка на заполнение линии фигурами
            update_display()  # Обновление экрана
            check_to_lose()  # Проверка на проигрыш
            frames_done = 0  # Заново начинаем отсчёт кадров

        if let_next_figure:  # Добавляем новую фигуру
            current_figure = figure_to_draw  # Обновляем новую фигуру
            figure_to_draw = choice(possible_figures).copy()  # Выбираем фигуру для отрисовки
            let_next_figure = False  # Не ждём новую фигуру

        clock.tick(fps)  # Следим на контролем времени
        frames_done += int(current_level)  # С каждым уровнем число кадров увеличивается на большее число