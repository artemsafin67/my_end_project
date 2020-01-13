def settings(screen, background_image):
    from settings_buttons import SettingsButton
    import pygame
    import sys

    global buttons

    settings_config = read_settings()  # Тут хранятся настройки

    # Создаём кнопки-настройщики
    music_is_on = SettingsButton(None, 300, 100, 600, 40, 'Включить звуковые эффекты', settings_config['music'],
                                 ['Да', 'Нет'], 50, pygame.Color('pink'), screen, border_color=pygame.Color('white'))

    buttons = [music_is_on]  # Список кнопок-настройщиков

    # Выводим все кнопки на экран
    screen.blit(background_image, (0, 0))
    for button in buttons:
        button.draw_button()
    pygame.display.update()

    chosen_button = None  # Пока нет выбранных кнопок

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                found = False  # Проверка на нажатие на кнопку

                for button in buttons:
                    if button.check(*event.pos):  # Если мы нажали на какую-то кнопку
                        chosen_button = button
                        found = True
                        continue

                if not found:  # Если мы не выбрали кнопку, то завершаем цикл
                    save_changes()
                    running = False

            if event.type == pygame.KEYDOWN:
                # Нажатие влияет только если есть выбранная кнопка
                if event.key == pygame.K_DOWN and chosen_button:
                    chosen_button.select_option(True)
                if event.key == pygame.K_UP and chosen_button:
                    chosen_button.select_option(False)

                # Обновляем экран, так как настройки и текст изменились (возможно)
                screen.blit(background_image, (0, 0))
                for button in buttons:
                    button.draw_button()
                pygame.display.update()


def read_settings():
    """Читаем старые настройки"""

    # Открываем файл со старыми настройками
    settings_config_file = open('settings_config.txt', encoding='utf-8')
    settings_config = {}  # Тут хранятся настройки

    for i in settings_config_file:
        a, b = i.strip('\n').split(':')
        settings_config[a] = b

    settings_config_file.close()

    return settings_config


def save_changes():
    """Сохраняем новые настройки"""

    settings_config = {}  # Тут хранятся настройки

    # Заполняем настройки
    for button in buttons:
        if button.options[button.current_option] == 'Да':
            settings_config['music'] = 'Да'
        else:
            settings_config['music'] = 'Нет'

    # Заполняем файл для записи настроек
    settings_config_file = open('settings_config.txt', mode='w', encoding='utf-8')

    for a, b in settings_config.items():
        settings_config_file.write('{}:{}\n'.format(a, b))

    settings_config_file.close()


