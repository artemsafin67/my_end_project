from game import game
from button import Button
from net_game import net_game
import settings
import pygame
import sys
import solver

# Настройка экрана
size = width, height = 1200, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Тетрис')

# Загрузка изображения - фона
background_image = pygame.image.load('background.jpg')
background_image = pygame.transform.scale(background_image, size)

# Читаем настройки
settings_config = settings.read_settings()

# Создание кнопок
start_game = Button(game, 450, 100, 300, 60, 'Новая игра', 78,
                    pygame.Color('pink'), screen, *(screen, settings_config),
                    border_color=pygame.Color('white'))

net_game = Button(net_game, 450, 250, 300, 60, 'Игра по сети', 70,
                  pygame.Color('pink'), screen, *(screen, settings_config),
                  border_color=pygame.Color('white'))

settings_label = Button(settings.settings, 450, 400, 300, 60, 'Настройки', 82,
                        pygame.Color('pink'), screen, screen, background_image,
                        border_color=pygame.Color('white'))

buttons = [start_game, net_game, settings_label]  # Список кнопок

# Отрисовываем меню
screen.blit(background_image, (0, 0))
for b in buttons:
    b.draw_button()
pygame.display.update()

running = True
while running:
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:

                if button.check(*event.pos):  # Если мы нажали на какую-то кнопку, то отрисовываем все заново

                    # Читаем правила, если изменяли настройки
                    if button.text == 'Настройки':
                        settings_config.clear()
                        for opt, key in settings.read_settings().items():
                            settings_config[opt] = key

                    # Отрисовываем экран
                    screen.blit(background_image, (0, 0))
                    for b in buttons:
                        b.draw_button()
                    pygame.display.update()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
