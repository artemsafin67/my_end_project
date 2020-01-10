from game import game
from button import Button
import pygame
import sys

# Настройка экрана
size = width, height = 1200, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Тетрис')

# Загрузка изображения - фона
background_image = pygame.image.load('background.jpg')
background_image = pygame.transform.scale(background_image, size)

# Создание кнопок
start_game = Button(game, 450, 100, 300, 60, 'Новая игра', 78,
                    pygame.Color('pink'), screen, *(screen, width, height),
                    border_color=pygame.Color('white'))

net_game = Button(lambda x: None, 450, 250, 300, 60, 'Игра по сети', 70,
                  pygame.Color('pink'), screen, screen, width, height,
                  border_color=pygame.Color('white'))

settings = Button(game, 450, 400, 300, 60, 'Настройки', 82,
                  pygame.Color('pink'), screen, screen, width, height,
                  border_color=pygame.Color('white'))

buttons = [start_game, net_game, settings]

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
                    screen.blit(background_image, (0, 0))

                    for b in buttons:
                        b.draw_button()

                    pygame.display.update()
                    continue

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
