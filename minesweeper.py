import pygame

# import pygame.locals
from pygame.locals import (
    MOUSEBUTTONDOWN,
    QUIT
)

pygame.init()

# set up the display
# screen = pygame.display.set_mode([1000, 700])

# control variable for game loop
running = True
# vars for mouse click
LEFT = 1
RIGHT = 3

# to swap between light green and dark green
# to keep track of tile coordinates


# creating the enemy class inheriting from Sprites
class Tile(pygame.sprite.Sprite):
    def __init__(self, side_length, bomb=False):
        super().__init__()
        # create the sprite of the tile
        self.s = s
        self.bomb = bomb
        self.tile = pygame.Surface([side_length, side_length])

    def color_tile(self, color):
        self.tile.fill(color)

    def place_tile(self, x, y):
        screen.blit(self.tile, [x, y])


def set_up_tiles():
    tiles = []
    if mode == 'easy':
        # all the instances of Tile are in the list tiles
        for num in range(1, 81):
            object = Tile(50)
            tiles.append(object)
        # figure out the coordinates
        x_cors = [i * 50 for i in range(10)]
        y_cors = [i * 50 + 75 for i in range(8)]
        # call tiles and place them
        for y in range(8):
            for x in range(10):
                tile = tiles[y * 10 + x]
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
    if mode == 'easy':
        square_length = 50
        # 10 by 8 squares: each square is 75 x 75
        length = square_length * 10
        width = square_length * 8
        adjust_display(length, width)
    elif mode == 'normal':
        square_length = 40
        # 18 x 14
        length = square_length * 18
        width = square_length * 14
        adjust_display(length, width)
    else:
        # 24 x 20
        square_length = 35
        length = square_length * 24
        width = square_length * 20
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


def main_loop():
    global running
    # game loop
    # default easy mode, but changes if the mode is switched
    get_mode()
    window_generator()
    set_up_tiles()
    while running:
        events = pygame.event.get()
        for event in events:
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN and event.button == LEFT:
                pygame.draw.circle(screen, [0, 0, 255], pos, 3)
            elif event.type == MOUSEBUTTONDOWN and event.button == RIGHT:
                pygame.draw.circle(screen, [255, 255, 255], pos, 3)
        pygame.display.flip()


main_loop()
pygame.quit()
