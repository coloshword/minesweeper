def set_up_tiles():
    tiles = []
    if mode == 'easy':
        # x_cors = []
        # x = 0
        # for i i
        x_cor = 0
        y_cor = 1
        y_base = 75
        # square length = 50
        # 10 by 8
        for num in range(1, 81):
            object = Tile(50)
            tiles.append(object)
        for index in range(0, 80):
            y = y_cor * y_base
            tiles[index].color_tile()
            tiles[index].place_tile(x_cor, y)
            y_cor += 1
            x_cor += 50
    pygame.display.flip()


def set_up_tiles():
    tiles = []
    if mode == 'easy':
        x_cors = []
        y_cors = []
        x = 0
        y = 75
        for