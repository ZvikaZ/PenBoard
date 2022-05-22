import math


class Board:
    def __init__(self):
        self.lines = []

    def add(self, line):
        self.lines.append(line)

    def remove(self, x, y, threshold):
        # this is O(n), can be easily changed to O(1)...
        for line in self.lines:
            if math.dist([x, y], [line.x, line.y]) < threshold or \
                    math.dist([x, y], [line.x2, line.y2]) < threshold:
                self.lines.remove(line)
