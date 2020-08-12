from random import sample
import pygame
import sys

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
current_tile = None
# vars for mouse click
LEFT = 1
RIGHT = 3


# to swap between light green and dark green
# to keep track of tile coordinates


# creating the enemy class inheriting from Sprites
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, side_length, color, loc, bomb=False, pressed=False, number=0):
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
        self.loc = loc

    def color_tile(self):
        self.tile.fill(self.color)

    def place_tile(self, x, y):
        screen.blit(self.tile, [x, y])

    def get_pressed(self, x, y):
        if self.color == (169, 215, 79):
            new_color = (215, 185, 153)
        else:
            new_color = (229, 194, 159)
        self.tile.fill(new_color)
        screen.blit(self.tile, [x, y])
        self.pressed = True
        self.display_numb()

    def get_unpressed(self, x, y):
        if self.color == (215, 185, 153):
            new_color = (169, 215, 79)
        else:
            new_color = (163, 209, 72)
        self.pressed = False

    def display_numb(self):
        if self.number > 0:
            display_numb = font.render(str(self.number), False, [255, 255, 255])
            screen.blit(display_numb, (int(self.x + square_length / 2.5), int(self.y + square_length / 3)))
            pygame.display.flip()

    def become_bomb(self):
        self.bomb = True


def instances_needed(l, w):
    """Gets number of instances set_up_tiles needs to return"""
    return l * w


def set_up_tiles(l, w, s_l):
    global grid
    grid = []
    num_hsquares = l // s_l
    num_vsquares = (w - 75) // s_l
    x_cors = [i * s_l for i in range(num_hsquares)]
    y_cors = [i * s_l + 75 for i in range(num_vsquares)]
    row_numb = 0
    for y in range(num_vsquares):
        row = []
        tile_index = 0
        for x in range(num_hsquares):
            if (x + y) % 2 == 0:
                color = (169, 215, 79)
            else:
                color = (163, 209, 72)
            obj = Tile(x_cors[x], y_cors[y], s_l, color, (row_numb, tile_index))
            tile_index += 1
            row.append(obj)
        grid.append(row)
        row_numb += 1
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
    global bombs_spawned
    if mode == 'easy':
        bombs_spawned = 10
        square_length = 50
        # 10 by 8 squares: each square is 75 x 75
        length = square_length * 10
        width = square_length * 8 + 75
        adjust_display(length, width)
    elif mode == 'normal':
        bombs_spawned = 40
        square_length = 40
        # 18 x 14
        length = square_length * 18
        width = square_length * 14 + 75
        adjust_display(length, width)
    else:
        bombs_spawned = 99
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
    return (int(row), int(index))


def test_index(index):
    tile = grid[index[0]][index[1]]
    return tile.loc


def change_tile_color(mouse_position, s_l):
    global running
    global current_tile
    if mouse_position[1] > 75:
        loc_pressed = index_tile_press(mouse_position[0], mouse_position[1], s_l)
        tile_pressed = grid[loc_pressed[0]][loc_pressed[1]]
        current_tile = tile_pressed
        if tile_pressed.bomb:
            running = False
        else:
            tile_pressed.get_pressed(tile_pressed.x, tile_pressed.y)


def create_safe_spots(mouse_position):
    global current_tile
    global safe_tiles_loc
    if mouse_position[1] > 75:
        loc_pressed = index_tile_press(mouse_position[0], mouse_position[1], square_length)
        current_tile = grid[loc_pressed[0]][loc_pressed[1]]
    row_safe = loc_pressed[0]
    index_safe = loc_pressed[1]
    safe_tiles_loc = []
    for row in range(-1, 2):
        for index in range(-1, 2):
            if row_safe + row >= 0 and index_safe + index >= 0:
                safe_tiles_loc.append((row_safe + row, index_safe + index))
    for loc in safe_tiles_loc:
        tile = grid[loc[0]][loc[1]]
        tile.get_pressed(tile.x, tile.y)


def spawn_bombs(list_of_tiles, num_bombs):
    flatten_list = sum(list_of_tiles, [])
    flatten_list = [tile for tile in flatten_list if not tile.pressed]
    bombs = sample(flatten_list, num_bombs)
    for bomb in bombs:
        bomb.become_bomb()
    # unpress all the pressed tiles so open_map() works properly
    for loc in safe_tiles_loc:
        tile = grid[loc[0]][loc[1]]
        tile.get_unpressed(tile.x, tile.y)


def show_bombs():
    """A test function to see if the correct number of bombs spawn"""
    for row in grid:
        for tile in row:
            if tile.bomb:
                pygame.draw.circle(screen, [255, 255, 255], [tile.x + 25, tile.y + 25], 5)


def adjacent_bombs(tile_loc):
    row_pressed = tile_loc[0]  # 1
    tile_pressed = tile_loc[1]  # 0
    bombs_near = 0
    for row in range(-1, 2):
        for tile in range(-1, 2):
            if (0 <= (row_pressed + row) <= 7) and (0 <= (tile_pressed + tile) <= 9):
                if grid[row_pressed + row][tile_pressed + tile].bomb:
                    bombs_near += 1
    return bombs_near


def get_numbs():
    """Gives all tiles their numbers"""
    for row in grid:
        for tile in row:
            tile.number = adjacent_bombs((index_tile_press(tile.x, tile.y, square_length)))


def open_map(tile):
    if tile.number > 0:
        tile.get_pressed(tile.x, tile.y)
        pygame.display.flip()
    else:
        # call all eight adjacent tiles, if they are not pressed, and if tile.number == 0
        tile.get_pressed(tile.x, tile.y)
        loc = tile.loc
        row = loc[0]
        tile = loc[1]
        loc_modifier = range(-1, 2)
        neighbors = [(row + r, tile + t) for r in loc_modifier for t in loc_modifier if (row + r) >= 0 and (tile + t) >= 0]
        for neighbor in neighbors:
            print(neighbor)
            cur_tile = grid[neighbor[0]][neighbor[1]]
            if not(cur_tile.pressed):
                cur_tile.get_pressed(cur_tile.x, cur_tile.y)
                open_map(cur_tile)
                pygame.display.flip()


def main_loop():
    global running
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
                create_safe_spots(pos)
                spawn_bombs(grid, bombs_spawned)
                show_bombs()
                get_numbs()
                open_map(current_tile)
                running = False
            pygame.display.flip()
    #             get_numbers(grid)
    #             display_them_numbers(grid)
    #             running = False
    # game loop after bombs are placed
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN and event.button == LEFT:
                change_tile_color(pos, square_length)
        pygame.display.flip()


main_loop()
pygame.quit()
