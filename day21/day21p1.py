#!/usr/bin/env python3
import fileinput


class Coord():
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    # write a function to generate a perfect hash from two integers less than 200
    def __hash__(self):
        return self.x * 255 + self.y

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Coord(self.x * other, self.y * other)

    def __eq__(self, other: object) -> bool:
        return (self.x == other.x) and (self.y == other.y)

    def __lt__(self, other: object) -> bool:
        return ((self.y == other.y) and (self.x < other.x)) or (self.y < other.y)


    def __str__(self):
        if (self.x == 0) and (self.y == -1):
            return 'N'
        if (self.x == 0) and (self.y == 1):
            return 'S'
        if (self.x == -1) and (self.y == 0):
            return 'W'
        if (self.x == 1) and (self.y == 0):
            return 'E'
        return f'({self.x}, {self.y})'
    __repr__ = __str__


U = Coord(0, -1)
D = Coord(0, 1)
R = Coord(1, 0) 
L = Coord(-1, 0)

def do_move(prev_locations: set, rock_coords: set, map_width: int, map_height: int) -> set:
    new_locations = set()
    for pl in prev_locations:
        for move in [U, D, L, R]:
            new_loc = pl + move
            if (new_loc.x < 0) or (new_loc.x >= map_width) or (new_loc.y < 0) or (new_loc.y >= map_height):
                continue
            if new_loc in rock_coords:
                continue
            new_locations.add(new_loc)

    return new_locations

def main():
    rock_coords = set()
    move_coords = set()

    for y, line in enumerate(fileinput.input()):
        for x, c in enumerate(line.strip()):
            if c == '#':
                rock_coords.add(Coord(x, y))
            elif c == 'S':
                move_coords.add(Coord(x, y))

    map_width = x
    map_height = y

    for _ in range(64):
        move_coords = do_move(move_coords, rock_coords, map_width, map_height)

    print(len(move_coords))


if __name__ == '__main__':
    main()