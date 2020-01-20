def net_game(screen, settings):
    """Функция, которая запускает игру"""
    import pygame
    from figure import Figure
    from board import Board
    from random import choice
    from client import MessageSenderAndReceiver
    from settings_buttons import SettingsButtonWithTextEnter
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

        if opt == 'username':
            username = key

        # Other options

    def terminate(kill=False):
        """Выход из программы"""
        nonlocal running

        if int(record) < int(current_score):
            record_file.close()
            new = open('record.txt', 'w')
            new.write(current_score)
            new.close()

        message_sender_and_receiver.send_message('cancel_invitation')
        message_sender_and_receiver.close()

        running = False
        if kill:
            pygame.quit()
            sys.exit()

    def draw_all_for_enemy(enemy_board_data, enemy_score, enemy_level):
        x_space = enemy_board.left_space * enemy_board.size
        y_space = enemy_board.top_space * enemy_board.size
        pygame.draw.rect(screen, pygame.Color('white'), [x_space, y_space, enemy_board.width * enemy_board.size + 400,
                                                         enemy_board.height * enemy_board.size + 400])
        draw_enemy_board(enemy_board_data)

        enemy_name_label = font.render(enemy_name, 1, pygame.Color('red'))
        enemy_score_label = font.render('Счёт: ' + enemy_score, 1, pygame.Color('#42aaff'))
        enemy_level_label = font.render('Уровень: ' + enemy_level, 1, pygame.Color('green'))

        screen.blit(enemy_name_label, (980, 210))
        screen.blit(enemy_score_label, (980, 330))
        screen.blit(enemy_level_label, (980, 450))

    def update_display():
        """Обновление игрового поля"""

        nonlocal current_level_label, current_score_label  # Переменные - информаторы

        screen.fill(pygame.Color('white'))

        # Обновляем текущие результаты
        current_score_label = font.render('Счёт: ' + current_score, 1, pygame.Color('#42aaff'))
        current_level_label = font.render('Уровень: ' + current_level, 1, pygame.Color('green'))

        # Рисуем текущие результаты
        x_coord = (board.left_space + board.width) * board.size + 50

        figure_to_draw.draw_next_in_the_rect(x_coord + 75, board.size * 2)
        board_to_draw_figure_on = Board(figure_to_draw.width, figure_to_draw.height,
                                        figure_to_draw.size, x_coord + 75, board.size * 2, figure_to_draw.screen, True)
        board_to_draw_figure_on.draw()


        screen.blit(record_label, (x_coord, 210))
        screen.blit(current_score_label, (x_coord, 330))
        screen.blit(current_level_label, (x_coord, 450))

        # Рисуем использованные фигуры
        for figure in used_figures:
            figure.draw()

        draw_all_for_enemy(enemy_board_data, enemy_score, enemy_level)

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
            message_sender_and_receiver.send_message('message:' + make_board_matrix(used_figures,
                                                                                    current_figure, board.width,
                                                                                    board.height)
                                                     + '!!!' + current_score + '!!!' + current_level)

        if event.key == pygame.K_RIGHT:  # Двигаем фигуру вправо
            current_figure.move_right()
            update_display()
            message_sender_and_receiver.send_message('message:' + make_board_matrix(used_figures,
                                                                                    current_figure, board.width,
                                                                                    board.height)
                                                     + '!!!' + current_score + '!!!' + current_level)

        if event.key == pygame.K_DOWN:  # Двигаем фигуру вниз
            current_figure.move_down()
            update_display()
            message_sender_and_receiver.send_message('message:' + make_board_matrix(used_figures,
                                                                                    current_figure, board.width,
                                                                                    board.height)
                                                     + '!!!' + current_score + '!!!' + current_level)

        if event.key == pygame.K_a:  # Поворачиваем фигуру на 90 градусов против часовой
            current_figure.rotate_to_left()
            update_display()
            message_sender_and_receiver.send_message('message:' + make_board_matrix(used_figures,
                                                                                    current_figure, board.width,
                                                                                    board.height)
                                                     + '!!!' + current_score + '!!!' + current_level)

        if event.key == pygame.K_s:  # Поворачиваем фигуру на 90 градусов по часовой
            current_figure.rotate_to_right()
            update_display()
            message_sender_and_receiver.send_message('message:' + make_board_matrix(used_figures,
                                                                                    current_figure, board.width,
                                                                                    board.height)
                                                     + '!!!' + current_score + '!!!' + current_level)

    def make_board_matrix(list_of_figures, current_figure, width, height):
        """Составляет матрицу поля для отправки"""

        matrix = [['.'] * width for _ in range(height)]

        for figure in list_of_figures:
            for x, y in figure.chosen_points:
                if figure.top + y < 0:
                    continue
                matrix[figure.top + y][figure.left + x] = figure.text_color

        if current_figure:
            for x, y in current_figure.chosen_points:
                if current_figure.top + y < 0:
                    continue
                matrix[current_figure.top + y][current_figure.left + x] = current_figure.text_color

        for i in range(len(matrix)):
            matrix[i] = ''.join(matrix[i])

        return ';'.join(matrix)

    def draw_enemy_board(field):
        """Рисует поле соперника по заданной матрице"""

        # Задаём отступы
        x_space = enemy_board.left_space * enemy_board.size
        y_space = enemy_board.top_space * enemy_board.size

        for x in range(len(field[0])):
            for y in range(len(field)):
                if field[y][x] == '.':  # Если клетка свободна
                    continue
                else:
                    pygame.draw.rect(screen, letter_to_color[field[y][x]], [x_space + x * board.size,
                                                                            y_space + y * board.size, board.size,
                                                                            board.size])

        enemy_board.draw()

    def receive_messages(client):
        if client.received:  # Если есть непрочитанные сообщения
            field, score, level = client.received.split('!!!')  # Получение данных
            field = field.split(';')

            # Нет непрочитанных сообщений
            client.received = None

            return field, score, level

        return (False, False, False)

    def start_game():
        tick = pygame.image.load('tick.png')
        cross = pygame.image.load('cross.jpg')

        tick_rect = tick.get_rect()
        tick_rect.left = 250
        tick_rect.top = 250
        cross_rect = cross.get_rect()
        cross_rect.left = 900
        cross_rect.top = 250

        bg = pygame.image.load('background.jpg')
        bg = pygame.transform.scale(bg, (width, height))

        enemy_name_enter = SettingsButtonWithTextEnter(None, 250, 200, 700, 50, 'Имя соперника',
                                                       '', 70, pygame.Color('pink'), screen,
                                                       parameter_for_file='enemy',
                                                       border_color=pygame.Color('white'))

        screen.blit(bg, (0, 0))
        enemy_name_enter.draw_button()
        screen.blit(tick, (250, 250))
        screen.blit(cross, (900, 250))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    enemy_name_enter.manage_event(event)

                    screen.blit(bg, (0, 0))
                    enemy_name_enter.draw_button()
                    screen.blit(tick, (400, 350))
                    screen.blit(cross, (550, 350))

                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if tick_rect.collidepoint(event.pos):
                        return enemy_name_enter.current_var

                    if cross_rect.collidepoint(event.pos):
                        return False

    clock = pygame.time.Clock()
    fps = 200
    frames_done = 0

    current_level = '1'
    figure_added = 0

    board = Board(10, 20, 25, 3, 1, screen)

    # Создаём все необходимое для отрисовки поля соперника
    enemy_board = board.copy()
    enemy_board.left_space = 25
    enemy_board.top_space = 1

    enemy_board_data = make_board_matrix([], None, board.width, board.height).split(';')
    enemy_score = '0'
    enemy_level = '1'

    # Экземпляр класса для отправки сообщений
    message_sender_and_receiver = MessageSenderAndReceiver()

    enemy = start_game()
    if enemy:
        message_sender_and_receiver.send_message('registration:{}'.format(username))
        message_sender_and_receiver.send_message('start_game_with:{}'.format(enemy))
    else:
        message_sender_and_receiver.close()
        return

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
    something_right = Figure(3, 2, pygame.Color('green'), 'g', board.size, [(0, 0), (1, 0), (1, 1), (2, 1)], board,
                             screen)
    t_letter = Figure(3, 2, pygame.Color('purple'), 'p', board.size, [(0, 0), (1, 0), (2, 0), (1, 1)], board, screen)
    l_letter_left = Figure(2, 3, pygame.Color('pink'), 'i', board.size, [(0, 0), (0, 1), (0, 2), (1, 2)], board, screen)
    l_letter_right = Figure(2, 3, pygame.Color('orange'), 'o', board.size, [(1, 0), (1, 1), (1, 2), (0, 2)], board,
                            screen)

    # Словарь цветов для отрисовки поля врага
    letter_to_color = {'r': pygame.Color('red'), 'y': pygame.Color('yellow'), 'g': pygame.Color('green'),
                       'p': pygame.Color('purple'), 'i': pygame.Color('pink'),
                       'o': pygame.Color('orange'), 'b': pygame.Color('#42aaff')}

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

        field_to_draw, score, level = receive_messages(message_sender_and_receiver)

        if field_to_draw:
            enemy_board_data = field_to_draw
            enemy_level = level
            enemy_score = score

        draw_all_for_enemy(enemy_board_data, enemy_score, enemy_level)
        pygame.display.update()

        if frames_done >= 200:  # Каждые 200 итераций обновляем картинку
            # Отправляем данные противнику
            message_sender_and_receiver.send_message('message:' + make_board_matrix(used_figures,
                                                                                    current_figure, board.width,
                                                                                    board.height)
                                                     + '!!!' + current_score + '!!!' + current_level)

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