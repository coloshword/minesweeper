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
            obj = x_cors[x], y_cors[y]
            row.append(obj)
        grid.append(row)



def create_safe_spots(list_tiles, mouse_position, s_l):
    # run this instead of change_tile_color for the first tile
    global safe_tile_locations
    # in the list is the tuple of (row, list)
    safe_tile_locations = [change_tile_color(list_tiles, mouse_position, s_l)]
    row_safe = safe_tile_locations[0][0]
    index_safe = safe_tile_locations[0][1]
    print(row_safe)
    print(index_safe)

set_up_tiles(500, 400, 50)
create_safe_spots(grid, )


print((grid[1][0])[0])