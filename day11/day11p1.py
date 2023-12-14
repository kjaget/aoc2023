#!/usr/bin/env python3

import fileinput
from dataclasses import dataclass
from copy import deepcopy

@dataclass
class Coord():
    x: int
    y: int
    x_add: int = 0
    y_add: int = 0

    def manhattan_distance(self, other):
        return abs((self.x + self.x_add) - (other.x + other.x_add)) + abs((self.y + self.y_add) - (other.y + other.y_add))

    def expand_row(self, row, factor):
        if self.y > row:
            self.y_add += factor

    def expand_col(self, col, factor):
        if self.x > col:
            self.x_add += factor

def expand_universe(map, galaxies, factor):
    for row in range(len(map)):
        if all([c == '.' for c in map[row]]):
            for g in galaxies:
                g.expand_row(row, factor)

    for col in range(len(map[0])):
        if all([c[col] == '.' for c in map]):
            for g in galaxies:
                g.expand_col(col, factor)

    return galaxies

def calc_distance(galaxies):
    return sum([g1.manhattan_distance(galaxies[i2]) for i1, g1 in enumerate(galaxies) for i2 in range(i1 + 1, len(galaxies))])

map = [l.strip() for l in fileinput.input()]
print(map)

galaxies = [Coord(x,y) for y, m in enumerate(map) for x, c in enumerate(m) if c == '#']

p1_galaxies = expand_universe(map, deepcopy(galaxies), 1)
print(f'p1_galaxies = {p1_galaxies}')

print(f'p1 : calc_distance(p1_galaxies) = {calc_distance(p1_galaxies)}')


p2_galaxies = expand_universe(map, deepcopy(galaxies), 1000000 - 1)
print(f'p2_galaxies = {p2_galaxies}')

print(f'p2 : calc_distance(p2_galaxies) = {calc_distance(p2_galaxies)}')