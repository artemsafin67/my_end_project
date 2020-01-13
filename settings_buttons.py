from button import Button


class SettingsButton(Button):
    def __init__(self, func, x, y, width, height, text, var, options, size, color,
                 screen, *args, bg_color=None, border_color=None):

        super().__init__(func, x, y, width, height, text + ': ' + var, size, color,
                         screen, *args, bg_color=bg_color, border_color=border_color)

        self.options = options  # Массив с опциями
        self.setting = text  # Настройка конкретной опции
        self.current_option = self.options.index(var)  # Индекс опции

    def change_text(self, text):
        # Меняем текст кнопки по заданному значению параметра
        self.text = self.setting + ': ' + text
        self.label = self.font.render(self.text, 1, self.color, self.bg_color)

    def select_option(self, is_down):
        """Изменяем текущую опцию по нажатию клавиш UP и DOWN"""

        if is_down:
            self.current_option = (self.current_option + 1) % len(self.options)
        else:
            self.current_option = (self.current_option - 1) % len(self.options)

        self.change_text(self.options[self.current_option])


