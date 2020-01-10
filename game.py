def game(screen, width, height):
    import pygame
    from figure import Figure
    from board import Board
    from random import choice

    pygame.init()

    def terminate():
        """Выход из программы"""
        nonlocal running

        if int(record) < int(current_score):
            record_file.close()
            new = open('record.txt', 'w')
            new.write(current_score)
            new.close()

        running = False


    def update_display():
        """Обновление игрового поля"""

        nonlocal current_level_label, current_score_label  # Переменные - информаторы

        screen.fill(pygame.Color('white'))

        # Обновляем текущие результаты
        current_score_label = font.render('Счёт: ' + current_score, 1, pygame.Color('#42aaff'))
        current_level_label = font.render('Уровень: ' + current_level, 1, pygame.Color('green'))

        # Рисуем текущие результаты
        x_coord = (board.left_space + board.width) * board.size + 50
        screen.blit(record_label, (x_coord, 80))
        screen.blit(current_score_label, (x_coord, 270))
        screen.blit(current_level_label, (x_coord, 450))

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

            screen.blit(lose_label, (width // 2 - 200, height // 2 - 100))
            pygame.display.update()

            if int(record) < int(current_score):
                record_file.close()
                new = open('record.txt', 'w')
                new.write(current_score)
                new.close()

            pygame.time.delay(6000)
            terminate()

    def manage_with_event(event):
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
    pygame.mixer.music.load('sounds/background_music.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.25)

    # Создаём образцы фигур
    square = Figure(2, 2, pygame.Color('yellow'), board.size, [(0, 0), (1, 0), (0, 1), (1, 1)], board, screen)
    stick = Figure(1, 4, pygame.Color('#42aaff'), board.size, [(0, 0), (0, 1), (0, 2), (0, 3)], board, screen)
    something_left = Figure(3, 2, pygame.Color('red'), board.size, [(0, 1), (1, 1), (1, 0), (2, 0)], board, screen)
    something_right = Figure(3, 2, pygame.Color('green'), board.size, [(0, 0), (1, 0), (1, 1), (2, 1)], board, screen)
    t_letter = Figure(3, 2, pygame.Color('purple'), board.size, [(0, 0), (1, 0), (2, 0), (1, 1)], board, screen)
    l_letter_left = Figure(2, 3, pygame.Color('pink'), board.size, [(0, 0), (0, 1), (0, 2), (1, 2)], board, screen)
    l_letter_right = Figure(2, 3, pygame.Color('orange'), board.size, [(1, 0), (1, 1), (1, 2), (0, 2)], board, screen)

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
    update_display()

    running = True
    while running:  # Основной игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                manage_with_event(event)

        if frames_done >= 200:  # Каждые 200 итераций обновляем картинку

            if not current_figure.move():  # Если мы не можем никуда пойти, то появляется новая фигура
                used_figures.append(current_figure)
                let_next_figure = True
                figure_down_sound.play()  # Проигрываем звук

                figure_added += 1
                if figure_added % int(current_level) ** 2 == 0:  # Увеличиваем уровень
                    current_level = str(int(current_level) + 1)
                    figure_added = 0

            check_field()  # Проверка на заполнение линии фигурами
            update_display()  # Обновление экрана
            check_to_lose()  # Проверка на проигрыш
            frames_done = 0

        if let_next_figure:
            current_figure = choice(possible_figures).copy()
            let_next_figure = False
            update_display()

        clock.tick(fps)
        frames_done += int(current_level)
