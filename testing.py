from random import sample

#
# def set_up_tiles(l, w, s_l):
#     global grid
#     grid = []
#     num_hsquares = l // s_l
#     num_vsquares = w // s_l
#     x_cors = [i * s_l for i in range(num_hsquares)]
#     y_cors = [i * s_l + 75 for i in range(num_vsquares)]
#     for y in range(num_vsquares):
#         row = []
#         for x in range(num_hsquares):
#             if (x+y) % 2 == 0:
#                 color = (169, 215, 79)
#             else:
#                 color = (163, 209, 72)
#             obj = x_cors[x], y_cors[y]
#             row.append(obj)
#         grid.append(row)
#
#
# def choose_bomb():
#     bomb = randint(0, ((length // square_length) * (width // square_length) - 1))
#     row = bomb // (length // square_length)
#     index = bomb % (length // square_length)
#     return (row, index)
#
#
# length = 500
# width = 400
# square_length = 50
# set_up_tiles(length, width, square_length)
#
# bomb_loc = choose_bomb()
# print(bomb_loc)
# print(grid[bomb_loc[0]][bomb_loc[1]])


list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print(sample(list, 5))
