from math import floor

import pygame
pygame.init()
LEFT = 1
RIGHT = 3
running = True

from pygame.locals import(
    MOUSEBUTTONDOWN,
    QUIT
)

screen = pygame.display.set_mode([100, 100])


class Tile(pygame.sprite.Sprite):
    def __init__(self, side_length, bomb=False, pressed=False):
        self.s = side_length
        self.bomb = bomb
        self.pressed = pressed
        self.tile = pygame.Surface([side_length, side_length])

    def color_tile(self, color):
        self.tile.fill(color)

    def place_tile(self, x, y):
        screen.blit(self.tile, [x, y])

    def get_pressed(self, color):
        self.tile.fill(color)
        screen.blit(self.tile, [0, 0])
        self.pressed = True


def get_mode():
    global mode
    mode = "easy"


def window_generator():
    global square_length
    global length
    global width
    if mode == 'easy':
        # 300, 100
        square_length = 100
        length = square_length * 3
        width = square_length * 1
        adjust_display(length, width)


def adjust_display(l_e, w):
    global screen
    screen = pygame.display.set_mode([l_e, w])
    screen.fill([255, 255, 255])


def set_up_tiles(l_e, sq_l):
    global tiles
    tiles = []
    num_squares = int(l_e / sq_l)
    for num in range(num_squares):
        obj = Tile(sq_l)
        tiles.append(obj)
    x_cors = [i * sq_l for i in range(num_squares)]
    y_cor = 0
    for x in range(num_squares):
        tile = tiles[x]
        tile.color_tile((0, 255, 0))
        tile.place_tile(x_cors[x], y_cor)


def get_clicked():
    tiles[0].get_pressed([255, 255, 255])


def main_loop():
    global running
    get_mode()
    window_generator()
    set_up_tiles(length, square_length)
    pygame.display.flip()
    while running:
        events = pygame.event.get()
        for event in events:
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN and event.button == LEFT:
                get_clicked()
            elif event.type == MOUSEBUTTONDOWN and event.button == RIGHT:
                pygame.draw.circle(screen, [255, 255, 255], pos, 3)
            pygame.display.flip()


main_loop()
pygame.quit()

