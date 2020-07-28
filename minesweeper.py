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
    def __init__(self, side_length, bomb=False, pressed=False):
        super().__init__()
        # create the sprite of the tile
        self.s = side_length
        self.bomb = bomb
        self.pressed = pressed
        self.tile = pygame.Surface([side_length, side_length])

    def color_tile(self, color):
        self.tile.fill(color)

    def place_tile(self, x, y):
        screen.blit(self.tile, [x, y])

    def get_pressed(self, color):
        self.pressed = True
        self.tile.fill(color)

    def become_bomb(self):
        self.bomb = True


def instances_needed(length, width):
    """Gets number of instances set_up_tiles needs to return"""
    return length * width


def set_up_tiles(length, width, square_length):
    global tiles
    tiles = []
    num_hsquares = int(length / square_length)
    num_vsquares = int(width / square_length)
    for num in range(num_hsquares * num_vsquares):
        object = Tile(square_length)
        tiles.append(object)
    # create a set of x and y coordinates
    x_cors = [i * square_length for i in range(num_hsquares)]
    y_cors = [i * square_length + 75 for i in range(num_vsquares)]
    for y in range(num_vsquares):
        for x in range(num_hsquares):
            tile = tiles[y * num_hsquares + x]
            if (x + y) % 2 == 0:
                tile.color_tile((0, 255, 0))
            else:
                tile.color_tile((34, 139, 34))
            tile.place_tile(x_cors[x], y_cors[y])
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


def set_up_tool_bar(length):
    # tool_bar is 75 in height
    tool_bar = pygame.Surface([length, 75])
    tool_bar.fill([135, 206, 235])
    return tool_bar


def adjust_display(length, width):
    global screen
    screen = pygame.display.set_mode([length, width])
    screen.fill([0, 0, 0])
    screen.blit(set_up_tool_bar(length), [0, 0])


def which_tile_press(x, y, length, square_length):
    """Gets the tile that was pressed given the x and y cors of the mouse click"""
    # if mode is easy, 10 x 8: length is 500, width is 400 + 75
    # index starts at 0, each row has 10
    y -= 75
    index_tile = (y // square_length) * (length / square_length)
    index_tile += floor(x / square_length)
    return int(index_tile)


def place_bombs(list_tiles, mouse_position):
    if mouse_position[1] > 75:
        list_tiles[which_tile_press(mouse_position[0], mouse_position[1], length, square_length)].get_pressed(
            [218, 203, 193])
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
                place_bombs(tiles, pos)
            elif event.type == MOUSEBUTTONDOWN and event.button == RIGHT:
                pygame.draw.circle(screen, [255, 255, 255], pos, 3)
        pygame.display.flip()


main_loop()
pygame.quit()
