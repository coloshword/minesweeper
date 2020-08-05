def index_tile_press(x, y, l_e, s_l):
    """Gets the tile that was pressed given the x and y cors of the mouse click"""
    # if mode is easy, 10 x 8: length is 500, width is 400 + 75
    # index starts at 0, each row has 10
    y -= 75
    row = (y // s_l) * (l_e / s_l)
    index = x // s_l
    return(int(row), int(index))

print(set_up_tiles(500, 400, 50)[0][0])
