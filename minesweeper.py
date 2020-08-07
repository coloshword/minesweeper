from math import floor
from random import randint
import pygame

# import pygame.locals
from pygame.locals import (
    MOUSEBUTTONDOWN,
    QUIT
)

pygame.init()
pygame.font.init()
# pygame.font.SysFont(font, size)
font = pygame.font.SysFont('Comic Sans MS', 30)

# control variable for game loop
running = True
# vars for mouse click
LEFT = 1
RIGHT = 3


# to swap between light green and dark green
# to keep track of tile coordinates


# creating the enemy class inheriting from Sprites
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, side_length, color, bomb=False, pressed=False, number=0):
        super().__init__()
        # create the sprite of the tile
        self.x = x
        self.y = y
        self.s = side_length
        self.bomb = bomb
        self.pressed = pressed
        self.tile = pygame.Surface([side_length, side_length])
        self.color = color
        self.number = number

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
    global grid
    grid = []
    num_hsquares = l // s_l
    num_vsquares = w // s_l
    x_cors = [i * s_l for i in range(num_hsquares)]
    y_cors = [i * s_l + 75 for i in range(num_vsquares)]
    for y in range(num_vsquares):
        row = []
        for x in range(num_hsquares):
            if (x+y) % 2 == 0:
                color = (169, 215, 79)
            else:
                color = (163, 209, 72)
            obj = Tile(x_cors[x], y_cors[y], s_l, color)
            row.append(obj)
        grid.append(row)
    for row in grid:
        for tile in row:
            tile.color_tile()
            tile.place_tile(tile.x, tile.y)
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


def index_tile_press(x, y, s_l):
    """Gets the tile that was pressed given the x and y cors of the mouse click"""
    # if mode is easy, 10 x 8: length is 500, width is 400 + 75
    # index starts at 0, each row has 10
    y -= 75
    row = (y // s_l)
    index = x // s_l
    return(int(row), int(index))


def change_tile_color(list_tiles, mouse_position, s_l):
    global running
    if mouse_position[1] > 75:
        loc_tile_pressed = index_tile_press(mouse_position[0], mouse_position[1], s_l)
        tile_pressed = list_tiles[loc_tile_pressed[0]][loc_tile_pressed[1]]
        if tile_pressed.bomb:
            running = False
        else:
            if tile_pressed.color == (169, 215, 79):
                new_color = (215, 185, 153)
            else:
                new_color = (229, 194, 159)
            tile_pressed.get_pressed(new_color, tile_pressed.x, tile_pressed.y)
            pygame.display.flip()
            return loc_tile_pressed

#
# def create_safe_spots(list_tiles, mouse_position, s_l):
#     # run this instead of change_tile_color the first time
#     global safe_tiles
#     safe_tiles = [change_tile_color(list_tiles, mouse_position, s_l)]
#     row_safe = safe_tiles[0][0]
#     index_safe = safe_tiles[0][1]
#     for row in range(-1, 2):
#         safe_in_row = []
#         for index in range(-1, 2):
#             safe_index = index_safe + index
#
#     # for tile in safe_tiles:
#     #     if tile.color == (169, 215, 79):
#     #         new_color = (215, 185, 153)
#     #     else:
#     #         new_color = (229, 194, 159)
#     #     tile.get_pressed(new_color, tile.x, tile.y)
#     # pygame.display.flip()


def create_safe_spots(list_tiles, mouse_position, s_l):
    # run this instead of change_tile_color for the first tile
    global safe_tile_locations
    # in the list is the tuple of (row, list)
    safe_tile_locations = [change_tile_color(list_tiles, mouse_position, s_l)]
    row_safe = safe_tile_locations[0][0]
    index_safe = safe_tile_locations[0][1]
    for row in range(-1, 2):
        for index in range(-1, 2):
            if row_safe + row > 0 and index_safe + index > 0:
                safe_tile_locations.append((row_safe + row, index_safe + index))
    for location in safe_tile_locations:
        tile = list_tiles[location[0]][location[1]]
        if tile.color == (169, 215, 79):
            new_color = (215, 185, 153)
        else:
            new_color = (229, 194, 159)
        tile.get_pressed(new_color, tile.x, tile.y)


def spawn_bombs(list_of_tiles, game_mode):
    can_be_bomb = list_of_tiles.copy()
    for tile in can_be_bomb:
        if tile.pressed:
            can_be_bomb.remove(tile)
    if game_mode == 'easy':
        # 10 bombs
        for bomb in range(10):
            # bomb is the index of a randomly generated bomb
            bomb = randint(0, len(can_be_bomb))
            can_be_bomb[bomb].become_bomb()
    if game_mode == 'normal':
        for bomb in range(40):
            bomb = randint(0, len(can_be_bomb))
            can_be_bomb[bomb].become_bomb()
    if game_mode == 'hard':
        for bomb in range(99):
            bomb = randint(0, len(can_be_bomb))
            can_be_bomb[bomb].become_bomb()


def get_indices_of_adjacent_tiles(index_of_tile, num_hsquares):
    adjacent_indices = []
    for y in range(-1, 2):
        for x in range(-1, 2):
            index_adjacent = index_of_tile + (y * num_hsquares) + x
            if index_adjacent != index_of_tile and index_adjacent >= 0:
                adjacent_indices.append(index_adjacent)
    return adjacent_indices


def get_numbers(list_of_tiles):
    """Gets the number displayed on each tile"""
    new_list = list_of_tiles.copy()
    current_tile = 0
    for tile in new_list:
        if not(tile.bomb):
            adjacent_bombs = 0
            for tile_index in get_indices_of_adjacent_tiles(current_tile, length // square_length):
                if new_list[tile_index].bomb:
                    adjacent_bombs += 1
            tile.number = adjacent_bombs
        current_tile += 1


def display_them_numbers(list_of_tiles):
    for tile in list_of_tiles:
        if tile.pressed and tile.number > 0:
            displayed_number = font.render(str(tile.number), False, (255, 255, 255))
            screen.blit(displayed_number, (tile.x, tile.y))


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
                create_safe_spots(grid, pos, square_length)
            pygame.display.flip()
    #             create_safe_spots(grid, pos, length, square_length)
    #             spawn_bombs(grid, mode)
    #             get_numbers(grid)
    #             display_them_numbers(grid)
    #             running = False
    # # game loop after bombs are placed
    # running = True
    # while running:
    #     events = pygame.event.get()
    #     for event in events:
    #         pos = pygame.mouse.get_pos()
    #         if event.type == QUIT:
    #             running = False
    #         elif event.type == MOUSEBUTTONDOWN and event.button == LEFT:
    #             change_tile_color(grid, pos, length, square_length)
    #             display_them_numbers(grid)
    #     pygame.display.flip()


main_loop()
pygame.quit()
