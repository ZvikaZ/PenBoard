def paint(board, pressure, x, y, prev_point):
    width = 6 * (pressure / 2 + 0.5)
    board.add((x, y), prev_point, width)


def erase(board, pressure, x, y):
    width = pressure * 30
    board.remove(x, y, width)
    return width
