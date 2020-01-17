from button import Button
import pygame


class SettingsButtonWithOptions(Button):
    """Реализует класс кнопки с выбором опций"""

    def __init__(self, func, x, y, width, height, setting, current_var, options, size, color,
                 screen, *args, parameter_for_file, bg_color=None, border_color=None):

        super().__init__(func, x, y, width, height, setting + ': ' + current_var, size, color,
                         screen, *args, bg_color=bg_color, border_color=border_color)

        self.options = options  # Массив с опциями
        self.setting = setting  # Настройка конкретной опции
        self.current_option = self.options.index(current_var)  # Индекс опции

        self.parameter_for_file = parameter_for_file  # Параметр  задаваемого значения для записи в файл

    def select_option(self, is_down):
        """Изменяем текущую опцию по нажатию клавиш UP и DOWN"""

        if is_down:
            self.current_option = (self.current_option + 1) % len(self.options)
        else:
            self.current_option = (self.current_option - 1) % len(self.options)

        self.change_text(self.setting, self.options[self.current_option])

    def manage_event(self, event):
        # Разбираемся с типом событий

        if event.key == pygame.K_DOWN:
            self.select_option(True)
        if event.key == pygame.K_UP:
            self.select_option(False)


class SettingsButtonWithTextEnter(Button):
    """Реализует класс кнопки с вводом значения"""

    def __init__(self, func, x, y, width, height, setting, current_var, size, color,
                 screen, *args, parameter_for_file, bg_color=None, border_color=None):

        super().__init__(func, x, y, width, height, setting + ':' + current_var, size, color,
                         screen, *args, bg_color=bg_color, border_color=border_color)

        self.current_var = current_var  # Текущее введенное значение
        self.setting = setting  # Параметр по которому идет настройка

        self.parameter_for_file = parameter_for_file  # Параметр для записи в файл

    def change_option(self, symbol, need_to_add):
        # Изменяем текущее значение по нажатие клавиши

        if need_to_add:  # Если надо добавить символ
            self.current_var += symbol
            self.change_text(self.setting, self.current_var)

        else:  # Если надо убрать символ
            if self.current_var:
                self.current_var = self.current_var[:-1]
                self.change_text(self.setting, self.current_var)

    def manage_event(self, event):
        """В зависимости от события KEYDOWN добавляет или убирает буквы"""
        if event.key == pygame.K_BACKSPACE:
            self.change_option('', False)
        else:
            self.change_option(event.unicode, True)
