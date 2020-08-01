from math import floor

import pygame

# import pygame.locals
from pygame.locals import (
    MOUSEBUTTONDOWN,
    QUIT
)

pygame.init()

# control variable for game loop
running = True
# vars for mouse click
LEFT = 1
RIGHT = 3


# to swap between light green and dark green
# to keep track of tile coordinates


# creating the enemy class inheriting from Sprites
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, side_length, color, bomb=False, pressed=False):
        super().__init__()
        # create the sprite of the tile
        self.x = x
        self.y = y
        self.s = side_length
        self.bomb = bomb
        self.pressed = pressed
        self.tile = pygame.Surface([side_length, side_length])
        self.color = color

    def color_tile(self):
        self.tile.fill(self.color)

    def place_tile(self, x, y):
        screen.blit(self.tile, [x, y])

    def get_pressed(self, color, x, y):
        self.tile.fill(color)
        screen.blit(self.tile, [x, y])
        self.pressed = True

    def become_bomb(self):
        self.bomb = True


def instances_needed(l, w):
    """Gets number of instances set_up_tiles needs to return"""
    return l * w


def set_up_tiles(l, w, s_l):
    global tiles
    tiles = []
    num_hsquares = l // s_l
    num_vsquares = w // s_l
    x_cors = [i * s_l for i in range(num_hsquares)]
    y_cors = [i * s_l + 75 for i in range(num_vsquares)]
    for y in range(num_vsquares):
        for x in range(num_hsquares):
            if (x + y) % 2 == 0:
                color = (169, 215, 79)
            else:
                color = (163, 209, 72)
            obj = Tile(x_cors[x], y_cors[y], s_l, color)
            tiles.append(obj)
    for obj in tiles:
        obj.color_tile()
        obj.place_tile(obj.x, obj.y)
    pygame.display.flip()


def get_mode():
    global mode
    mode = 'easy'


def window_generator():
    global length
    global width
    global square_length
    if mode == 'easy':
        square_length = 50
        # 10 by 8 squares: each square is 75 x 75
        length = square_length * 10
        width = square_length * 8 + 75
        adjust_display(length, width)
    elif mode == 'normal':
        square_length = 40
        # 18 x 14
        length = square_length * 18
        width = square_length * 14 + 75
        adjust_display(length, width)
    else:
        # 24 x 20
        square_length = 35
        length = square_length * 24
        width = square_length * 20 + 75
        adjust_display(length, width)
    pygame.display.flip()


def set_up_tool_bar(l_e):
    # tool_bar is 75 in height
    tool_bar = pygame.Surface([l_e, 75])
    tool_bar.fill([135, 206, 235])
    return tool_bar


def adjust_display(l_e, w):
    global screen
    screen = pygame.display.set_mode([l_e, w])
    screen.fill([0, 0, 0])
    screen.blit(set_up_tool_bar(l_e), [0, 0])


def which_tile_press(x, y, l_e, s_l):
    """Gets the tile that was pressed given the x and y cors of the mouse click"""
    # if mode is easy, 10 x 8: length is 500, width is 400 + 75
    # index starts at 0, each row has 10
    y -= 75
    index_tile = (y // s_l) * (l_e / s_l)
    index_tile += floor(x / s_l)
    return int(index_tile)


def place_bombs(list_tiles, mouse_position, l_e, s_l):
    if mouse_position[1] > 75:
        tile_pressed = list_tiles[which_tile_press(mouse_position[0], mouse_position[1], l_e, s_l)]
        if tile_pressed.color == (169, 215, 79):
            new_color = (215, 185, 153)
        else:
            new_color = (229, 194, 159)
        tile_pressed.get_pressed(new_color, tile_pressed.x, tile_pressed.y)
        pygame.display.flip()


def main_loop():
    global running
    # game loop
    # default easy mode, but changes if the mode is switched
    get_mode()
    window_generator()
    set_up_tiles(length, width, square_length)
    while running:
        events = pygame.event.get()
        for event in events:
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN and event.button == LEFT:
                place_bombs(tiles, pos, length, square_length)
            elif event.type == MOUSEBUTTONDOWN and event.button == RIGHT:
                pygame.draw.circle(screen, [255, 255, 255], pos, 3)
        pygame.display.flip()


main_loop()
pygame.quit()
