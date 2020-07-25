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


def mode_generator(mode):
    if mode == 'easy':
        square_length = 75
        # 10 by 8 squares: each square is 75 x 75
        length = square_length * 10
        width = square_length * 8
        adjust_display(length, width)
    if mode == 'normal':
        square_length = 50
        # 18 x 14
        length = square_length * 18
        width = square_length * 14
        adjust_display(length, width)
    if mode == 'hard':
        # 24 x 20
        square_length = 38
        length = square_length * 24
        width = square_length * 20
        adjust_display(length, width)
    pygame.display.flip()


def adjust_display(l, w):
    global screen
    screen = pygame.display.set_mode([l, w])
    screen.fill([34, 139, 34])
    screen.blit(set_up_tool_bar(l), [0, 0])


def set_up_tool_bar(length):
    # tool_bar is 75 in height
    tool_bar = pygame.Surface([length, 75])
    tool_bar.fill([0, 0, 0])
    return tool_bar


def main_loop():
    global running
    # game loop
    # default easy mode, but changes if the mode is switched
    mode_generator('hard')
    while running:
        ev = pygame.event.get()
        for event in ev:
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
