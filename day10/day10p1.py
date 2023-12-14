#!/usr/bin/env python3

import fileinput
from dataclasses import dataclass
from matplotlib.path import Path
import numpy as np
import cv2

@dataclass
class Coord():
    x: int
    y: int

    # write a function to generate a perfect hash from two integers less than 200
    def __hash__(self):
        return self.x * 31 + self.y

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

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

map = []
s_coord = None
for line in fileinput.input():
    line = line.strip()
    if len(map) == 0:
        map.append(['.'] * (len(line) + 2))
    
    map.append(['.'] + [c for c in line] + ['.'])

    if 'S' in line:
        s_coord = Coord(map[-1].index('S'), len(map) - 1)

map.append(['.'] * len(map[0]))

#print(map)

N = Coord(0, -1)
S = Coord(0, 1)
E = Coord(1, 0) 
W = Coord(-1, 0)
# Maps to find next direction from prev direction
direction_map_n = {'|': N, 'F': E, '7': W}
direction_map_s = {'|': S, 'L': E, 'J': W}
direction_map_e = {'-': E, 'J': N, '7': S}
direction_map_w = {'-': W, 'L': N, 'F': S}
direction_map = {N: direction_map_n, S: direction_map_s, E: direction_map_e, W: direction_map_w}

# Find a start coord next to an S char which could legally return
# to that char. Return the coord and the direction moved to get to that char
# as the starting point of building the pipe
def get_start_coord_direction(coord: Coord, map: list, direction_map: dict) -> (Coord, Coord):
    for d in [N, S, E, W]:
        potential_start_coord = coord + d
        potential_start_char = map[potential_start_coord.y][potential_start_coord.x]
        for return_direction in [N, S, E, W]:
            if potential_start_char in direction_map[return_direction]:
                if (potential_start_coord + direction_map[return_direction][potential_start_char]) == coord:
                    return potential_start_coord, d

    return None, None

# Iteratively build the pipe.  The start coord is 1 step from the start
# char, and direction is the direction moved from the start char to that
# starting coord. Use the direction maps to continue building the pipe
# until the start char is seen.
def build_pipe(coord: Coord, direction: Coord, map: list, direction_map: list) -> list:
    print(f'coord = {coord}, direction = {direction}')
    pipe = [coord]
    while map[pipe[-1].y][pipe[-1].x] != 'S':
        # The new direction is based on the current direction and the map char
        # This new direction lets us get the next coord in the pipe
        # and is also carried over as the input direction to that
        # next coord's calculation
        direction = direction_map[direction][map[pipe[-1].y][pipe[-1].x]]
        pipe.append(pipe[-1] + direction)
    return pipe

start_coord, start_direction = get_start_coord_direction(s_coord, map, direction_map)
print(f'start_coord = {start_coord}, start_direction = {start_direction}')

pipe = build_pipe(start_coord, start_direction, map, direction_map)
pipe_map = set()
for p in pipe:
    pipe_map.add(p)
#print(pipe)
print(len(pipe) // 2)

poly = Path([(p.x, p.y) for p in pipe])
sum = 0
for y in range(len(map)):
    for x in range(len(map[0])):
        if (Coord(x, y) not in pipe_map) and poly.contains_point((x, y)):
            #print(f'contains {x}, {y}')
            sum += 1    
print(sum)

nd = np.array([[[c.x, c.y]] for c in pipe], dtype=np.int32)

sum2 = 0
for x in range(len(map[0])):
    for y in range(len(map)):
        if (Coord(x, y) not in pipe_map) and (cv2.pointPolygonTest(nd, (x,y), False) == 1):
            #print(f'contains {x}, {y}')
            sum2 += 1
print(sum2)
