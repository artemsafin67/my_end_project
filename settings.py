from settings_buttons import SettingsButtonWithOptions, SettingsButtonWithTextEnter
from button import Button
from client import MessageSenderAndReceiver
import pygame
import sys


def settings(screen, background_image):
    global buttons, username

    settings_config = read_settings()  # Тут хранятся ранее сохраненные настройки

    # Создаём кнопки-настройщики
    music_is_on = SettingsButtonWithOptions(func=None, x=300, y=100, width=600, height=40,
                                            setting='Включить звуковые эффекты',
                                            current_var=settings_config['music'],
                                            options=['Да', 'Нет'], size=50,
                                            color=pygame.Color('pink'), screen=screen,
                                            parameter_for_file='music',
                                            border_color=pygame.Color('white'))

    username = SettingsButtonWithTextEnter(func=None, x=300, y=200, width=600, height=40,
                                           setting='Имя пользователя',
                                           current_var=settings_config['username'],
                                           size=50, color=pygame.Color('pink'),
                                           screen=screen, parameter_for_file='username',
                                           border_color=pygame.Color('white'))

    register = Button(func=register_username, x=300, y=300, width=600, height=40, text='Регистрация',
                      size=50, color=pygame.Color('pink'), screen=screen, border_color=pygame.Color('white'))

    buttons = [music_is_on, username, register]  # Список кнопок-настройщиков

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
                        break

                if not found:  # Если мы не выбрали кнопку, то завершаем цикл
                    save_changes()
                    running = False

            if event.type == pygame.KEYDOWN:
                chosen_button.manage_event(event)

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
        if isinstance(button, SettingsButtonWithOptions):
            settings_config[button.parameter_for_file] = \
                button.options[button.current_option]

        if isinstance(button, SettingsButtonWithTextEnter):
            settings_config[button.parameter_for_file] = button.current_var

    # Заполняем файл для записи настроек
    settings_config_file = open('settings_config.txt', mode='w', encoding='utf-8')

    for a, b in settings_config.items():
        settings_config_file.write('{}:{}\n'.format(a, b))

    settings_config_file.close()


def register_username():
    """Отправляем запрос на регистрацию"""

    message_sender_and_receiver = MessageSenderAndReceiver()
    message_sender_and_receiver.send_message('registration:{}'.format(username.current_var))
    message_sender_and_receiver.close()
