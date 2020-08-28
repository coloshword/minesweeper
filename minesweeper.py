from random import sample, randint
import pygame
import time
import sys
import pygame.gfxdraw

pygame.font.get_fonts

from pygame.locals import (
    Rect,
    MOUSEBUTTONUP,
    MOUSEBUTTONDOWN,
    QUIT
)

pygame.init()
pygame.font.init()
# pygame.font.SysFont(font, size)
font = pygame.font.SysFont('Roboto', 35)
win_font = pygame.font.SysFont('Times New Roman', 100)
font2 = pygame.font.SysFont('Calibri', 40)
# control variable for game loop
running = True
current_tile = None
# vars for mouse click
LEFT = 1
RIGHT = 3
# vars for number of horizontal and vertical tiles
grid = None
tiles_per_row = None
rows_per_grid = None
# number to color list
colors = [
    (86, 139, 192),
    (92, 152, 82),
    (211, 47, 47),
    (123, 30, 162),
    (252, 155, 9),
    (203, 69, 204),
    (246, 206, 232),
    (254, 255, 213),
    (254, 255, 213)
]

bombt_rgbs = [
    (255, 204, 255),
    (204, 229, 255),
    (255, 255, 204),
    (204, 255, 255),
    (204, 255, 204),
    (255, 204, 204)

]

bomb_colors = [
    (127, 0, 255),
    (0, 0, 255),
    (255, 0, 0),
    (102, 0, 204),
    (204, 0, 102),
    (255, 255, 0)
]
# win or lose variables
flags = None
tiles_left = None
# win message time
win_display_time = None


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, side_length, color, loc, bomb=False, pressed=False, number=0, flagged=False):
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
        self.flagged = flagged
        self.flag_color = [242, 53, 8]

    def color_tile(self):
        self.tile.fill(self.color)

    def place_tile(self, x, y):
        screen.blit(self.tile, [x, y])

    def get_pressed(self, x, y):
        global tiles_left
        if self.color == (169, 215, 79):
            new_color = (215, 185, 153)
        else:
            new_color = (229, 194, 159)
        self.tile.fill(new_color)
        screen.blit(self.tile, [x, y])
        if not (self.pressed):
            self.pressed = True
            tiles_left -= 1
        self.display_numb()

    def get_unpressed(self):
        global tiles_left
        self.pressed = False
        tiles_left += 1

    def numb_color(self):
        return colors[self.number]

    def display_numb(self):
        if self.number > 0 and not (self.bomb):
            display_numb = font.render(str(self.number), False, self.numb_color())
            screen.blit(display_numb, (int(self.x + square_length / 3), int(self.y + square_length / 5)))
            pygame.display.flip()

    def become_bomb(self):
        self.bomb = True

    def show_flag(self):
        if self.pressed:
            return
        elif self.flagged:
            self.flagged = False
            self.color_tile()
            self.place_tile(self.x, self.y)
        else:
            # draw the flag
            pygame.draw.polygon(screen, self.flag_color, ((self.x + square_length // 2, self.y + square_length // 6),
                                                          (self.x + square_length // 7, self.y + square_length // 3),
                                                          (self.x + square_length // 2, self.y + square_length // 2)))
            pygame.draw.rect(screen, self.flag_color, (self.x + square_length // 2, self.y + square_length // 6, 3, 25),
                             0)
            self.flagged = True
        pygame.display.flip()

    def show_bomb_tile(self):
        tile_color = bombt_rgbs[randint(0, 5)]
        bomb_color = bomb_colors[randint(0, 5)]
        self.tile.fill(tile_color)
        screen.blit(self.tile, (self.x, self.y))
        pygame.draw.circle(screen, bomb_color, (self.x + square_length // 2, self.y + square_length // 2), 7)
        pygame.display.flip()

    def double_pressed(self):
        if self.color == (169, 215, 79) and not (self.pressed):
            new_color = (191, 226, 125)
        elif not (self.pressed):
            new_color = (186, 221, 119)
        self.tile.fill(new_color)
        screen.blit(self.tile, (self.x, self.y))

    def revert(self):
        self.tile.fill(self.color)
        screen.blit(self.tile, (self.x, self.y))


def draw_rounded_rect(surface, rect, color, corner_radius):
    if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
        raise ValueError(f"Both height (rect.height) and width (rect.width) must be > 2 * corner radius ({corner_radius})")

    # need to use anti aliasing circle drawing routines to smooth the corners
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

    pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

    rect_tmp = pygame.Rect(rect)

    rect_tmp.width -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)

    rect_tmp.width = rect.width
    rect_tmp.height -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)


def draw_bordered_rounded_rect(text, text_color, loc, surface, rect, color, border_color, corner_radius, border_thickness):
    if corner_radius < 0:
        raise ValueError(f"border radius ({corner_radius}) must be >= 0")

    rect_tmp = pygame.Rect(rect)
    center = rect_tmp.center

    if border_thickness:
        if corner_radius <= 0:
            pygame.draw.rect(surface, border_color, rect_tmp)
        else:
            draw_rounded_rect(surface, rect_tmp, border_color, corner_radius)

        rect_tmp.inflate_ip(-2*border_thickness, -2*border_thickness)
        inner_radius = corner_radius - border_thickness + 1
    else:
        inner_radius = corner_radius

    if inner_radius <= 0:
        pygame.draw.rect(surface, color, rect_tmp)
    else:
        draw_rounded_rect(surface, rect_tmp, color, inner_radius)
    #draw text
    font = pygame.font.SysFont("Calibri", 30)
    text = font.render(text, True, text_color)
    surface.blit(text, loc)
    return Rect(rect)


def draw_text(text, style, text_color, background_color, loc):
    #(text, font)
    font = pygame.font.SysFont(style, 50)
    text = font.render(text, True, text_color, background_color)
    textRect = text.get_rect()
    textRect.topleft = loc
    screen.blit(text, textRect)
    return textRect


def mode_menu():
    global menu
    """A button that will lead to an options menu"""
    menu = draw_bordered_rounded_rect("Menu", (255, 255, 255), (35, 25), screen, (15, 15, 100, 40), (177, 156, 217), (0, 0 , 0), 3, 0)
    pygame.display.flip()


def check_menu(mouse):
    for event in events:
        if menu.collidepoint(mouse) and event.type == MOUSEBUTTONDOWN:
            options()
    pygame.display.flip()


def options():
    global running
    global master_run
    master_run = False
    options_surface = pygame.display.set_mode((500, 500))
    options_surface.fill((138, 43, 226))
    font = pygame.font.SysFont('Calibri', 60)
    text = font.render("GAME MODE", True, [255, 255, 255])
    screen.blit(text, (120, 30))
    pygame.draw.rect(screen, (160, 215, 79), (0, 75, 500, 425))
    # Game buttons
    easy = draw_bordered_rounded_rect("Easy", (255, 255, 255), (230, 128), screen, (180, 120, 150, 35), (0, 123, 255), (0, 0, 0), 3, 0)
    normal = draw_bordered_rounded_rect("Normal", (255, 255, 255), (220, 228), screen, (180, 220, 150, 35), (0, 123, 255), (0, 0, 0), 3, 0)
    hard = draw_bordered_rounded_rect("Hard", (255, 255, 255), (230, 328), screen, (180, 320, 150, 35), (0, 123, 255), (0, 0, 0), 3, 0)
    run_option = True
    while run_option:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif easy.collidepoint(pos) and event.type == MOUSEBUTTONDOWN:
                main_loop('easy')
                run_option = False
            elif normal.collidepoint(pos) and event.type == MOUSEBUTTONDOWN:
                main_loop()
                run_option = False
            elif hard.collidepoint(pos) and event.type == MOUSEBUTTONDOWN:
                main_loop('hard')
                run_option = False
        pygame.display.flip()
    pygame.display.flip()


def set_up_tiles(l, w, s_l):
    global grid
    global tiles_per_row
    global rows_per_grid
    grid = []
    tiles_per_row = l // s_l
    rows_per_grid = (w - 75) // s_l
    x_cors = [i * s_l for i in range(tiles_per_row)]
    y_cors = [i * s_l + 75 for i in range(rows_per_grid)]
    row_numb = 0
    for y in range(rows_per_grid):
        row = []
        tile_index = 0
        for x in range(tiles_per_row):
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


def window_generator():
    global length
    global width
    global square_length
    global bombs_spawned
    global flags
    global tiles_left
    global win_display_time
    if mode == 'easy':
        bombs_spawned = 10
        square_length = 50
        tiles_left = (10 * 8) - bombs_spawned
        length = square_length * 10
        width = square_length * 8 + 75
        win_display_time = 0.1
        adjust_display(length, width)
    elif mode == 'normal':
        bombs_spawned = 40
        square_length = 40
        tiles_left = (18 * 14) - bombs_spawned
        # 18 x 14
        length = square_length * 18
        width = square_length * 14 + 75
        adjust_display(length, width)
        win_display_time = 0.05
    else:
        bombs_spawned = 99
        # 24 x 20
        tiles_left = (24 * 20) - bombs_spawned
        square_length = 35
        length = square_length * 24
        width = square_length * 20 + 75
        adjust_display(length, width)
        win_display_time = 0.03
    flags = bombs_spawned
    pygame.display.flip()


def set_up_tool_bar(l_e):
    global tool_bar
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
    # index starts at 0, each row has 1
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
        if tile_pressed.bomb and not (tile_pressed.flagged):
            running = False
            get_fukt(tile_pressed)
        elif tile_pressed.flagged:
            return
        else:
            tile_pressed.get_pressed(tile_pressed.x, tile_pressed.y)
            current_tile = tile_pressed
        pygame.display.flip()


def place_flag(mouse_position):
    global current_tile
    if mouse_position[1] > 75:
        loc_pressed = index_tile_press(mouse_position[0], mouse_position[1], square_length)
        current_tile = grid[loc_pressed[0]][loc_pressed[1]]
        current_tile.show_flag()


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
        tile.get_unpressed()


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
            if (0 <= (row_pressed + row) <= (rows_per_grid - 1)) and (
                    0 <= (tile_pressed + tile) <= (tiles_per_row - 1)):
                if grid[row_pressed + row][tile_pressed + tile].bomb:
                    bombs_near += 1
    return bombs_near


def get_numbs():
    """Gives all tiles their numbers"""
    for row in grid:
        for tile in row:
            tile.number = adjacent_bombs((index_tile_press(tile.x, tile.y, square_length)))


def open_map(tile):
    if tile.flagged:
        return
    elif tile.number > 0:
        tile.get_pressed(tile.x, tile.y)
    else:
        # call all eight adjacent tiles, if they are not pressed, and if tile.number == 0
        tile.get_pressed(tile.x, tile.y)
        loc = tile.loc
        row = loc[0]
        tile = loc[1]
        loc_modifier = range(-1, 2)
        neighbors = [(row + r, tile + t) for r in loc_modifier for t in loc_modifier if
                     0 <= (row + r) <= (rows_per_grid - 1) and 0 <= (tile + t) <= (tiles_per_row - 1)]
        for neighbor in neighbors:
            cur_tile = grid[neighbor[0]][neighbor[1]]
            if not (cur_tile.pressed) and not (cur_tile.flagged):
                cur_tile.get_pressed(cur_tile.x, cur_tile.y)
                open_map(cur_tile)
        pygame.display.flip()


def win():
    global running
    # if all the tiles left are bombs
    if tiles_left == 0:
        win_message()
        running = False


def win_message():
    for i in (range(rows_per_grid)[::-1]):
        pygame.draw.rect(screen, [255, 255, 255], (0, square_length * i + 75, length, square_length), 0)
        time.sleep(win_display_time)
        pygame.display.flip()
    pygame.draw.rect(screen, [0, 0, 0], (0, 0, length, 75), 0)
    pygame.display.flip()
    display = win_font.render('YOU WIN', False, [173, 216, 230])
    screen.blit(display, (length / 3.5, (width + 75) // 3))
    pygame.display.flip()


def get_fukt(first_tile_pressed):
    """Displays a you lose"""
    first_tile_pressed.show_bomb_tile()
    time.sleep(1)
    for row in grid:
        for tile in row:
            if tile.bomb and tile != first_tile_pressed:
                tile.show_bomb_tile()
                time.sleep(0.1)
    time.sleep(2)
    pygame.draw.rect(screen, (255, 255, 255), (0, width // 5, length, width - 200), 0)
    display = win_font.render('Get fukt', False, [173, 216, 230])
    screen.blit(display, (length / 3.5, (width + 75) // 3))
    pygame.display.flip()


def double_pressed(mouse_pos):
    global adjacent_tiles
    global adjacent_not_flagged
    global numb
    global number_flagged
    x = mouse_pos[0]
    y = mouse_pos[1]
    loc = index_tile_press(x, y, square_length)
    tile_pressed = grid[loc[0]][loc[1]]
    row = loc[0]
    tile = loc[1]
    numb = tile_pressed.number
    adjacent_tiles_loc = [(row + x, tile + y) for x in range(-1, 2) for y in range(-1, 2) if
                          0 <= (row + x) <= rows_per_grid and 0 <= (tile + y) <= tiles_per_row]
    adjacent_tiles_loc.remove(loc)
    adjacent_tiles = [grid[loc[0]][loc[1]] for loc in adjacent_tiles_loc if not (grid[loc[0]][loc[1]].pressed)]
    adjacent_not_flagged = [tile for tile in adjacent_tiles if not (tile.flagged)]
    number_flagged = len(adjacent_tiles) - len(adjacent_not_flagged)
    if 1 <= numb and number_flagged < numb:
        for tile in adjacent_not_flagged:
            tile.double_pressed()
        pygame.display.flip()
    elif 1 <= numb == number_flagged:
        not_bombs = [tile for tile in adjacent_not_flagged if not (tile.bomb)]
        for tile in not_bombs:
            change_tile_color((tile.x, tile.y), square_length)
        pygame.display.flip()
        for tile in adjacent_not_flagged:
            change_tile_color((tile.x, tile.y), square_length)
        pygame.display.flip()


def main_loop(game_mode='normal'):
    global running
    global events
    global mouse
    global mode
    global master_run
    running = True
    master_run = True
    mode = game_mode
    window_generator()
    mode_menu()
    set_up_tiles(length, width, square_length)
    while running and master_run:
        events = pygame.event.get()
        for event in events:
            pos = pygame.mouse.get_pos()
            check_menu(pos)
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN and event.button == LEFT:
                create_safe_spots(pos)
                spawn_bombs(grid, bombs_spawned)
                get_numbs()
                open_map(current_tile)
                running = False
            pygame.display.flip()
    running = True
    while running and master_run:
        events = pygame.event.get()
        for event in events:
            pos = pygame.mouse.get_pos()
            check_menu(pos)
            mouse = pygame.mouse.get_pressed()
            win()
            if event.type == QUIT:
                running = False
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == RIGHT:
                place_flag(pos)
            elif event.type == MOUSEBUTTONDOWN and event.button == LEFT:
                change_tile_color(pos, square_length)
                open_map(current_tile)
            elif (mouse[0] and mouse[2]):
                double_pressed(pos)
                loop = True
                while loop:
                    events2 = pygame.event.get()
                    mouse2 = pygame.mouse.get_pressed()
                    for event in events2:
                        if event.type == QUIT:
                            running = False
                    if mouse2[2] and mouse2[0]:
                        continue
                    else:
                        loop = False
                if numb != number_flagged:
                    for tile in adjacent_not_flagged:
                        tile.revert()
                    pygame.display.flip()
    running = True
    while running and master_run:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                running = False
                sys.exit()


main_loop()
pygame.quit()