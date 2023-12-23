#!/usr/bin/env python3
import fileinput
from dataclasses import dataclass

from sympy import cycle_length

@dataclass
class Coord():
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __lt__(self, other):
        return ((self.y == other.y) and (self.x < other.x)) or (self.y > other.y)

@dataclass
class CoordNS(Coord):
    num_rocks: int = 0

    def reset(self):
        self.num_rocks = 0

    def get_rock_coords(self, north: bool) -> list:
        return [Coord(self.x, self.y - (i + 1) if north else self.y + i + 1) for i in range(self.num_rocks)]
    
    def __str__(self):
        return f'CoordNS({self.x}, {self.y}): {self.num_rocks}'

class CoordEW(Coord):
    num_rocks: int = 0

    def reset(self):
        self.num_rocks = 0

    def get_rock_coords(self, east) -> list:
        return [Coord(self.x - (i + 1) if east else self.x + i + 1, self.y) for i in range(self.num_rocks)]

    def __str__(self):
        return f'CoordEW({self.x}, {self.y}): {self.num_rocks}'

def tilt_ns(north: bool, cube_rocks_ns: list, round_rocks: set) -> set:

    # Constuct a list of sets of round rocks for each column
    round_rocks_set = [set() for _ in range(len(cube_rocks_ns))]
    for r in round_rocks:
        round_rocks_set[r.x - 1].add(r.y)

    # print(f'round_rocks = {round_rocks}')
    # For each column, iterate through the rows in the direction of tilt
    # If there are no other cube rocks in the way, add this round rock to the cube rock counter
    for col in range(len(cube_rocks_ns)):
        for c in cube_rocks_ns[col]:
            c.reset()
        # print(f'round_rocks_set[{col}] = {round_rocks_set[col]}')
        if len(round_rocks_set[col]) == 0:
            continue
        cube_idx = 0 if north else len(cube_rocks_ns[col]) - 1
        cube_idx_add = 1 if north else -1
        # print(f'cube_rocks[{col}] = {cube_rocks_ns[col]}')
        rows_to_test = {r for r in round_rocks_set[col]}.union(c.y for c in cube_rocks_ns[col])
        for row in reversed(sorted(rows_to_test)) if north else sorted(rows_to_test):
            # print(f'col = {col}, row = {row}, cube_idx = {cube_idx}, cube_rocks[{col}][{cube_idx}] = {cube_rocks_ns[col][cube_idx]}')
            if row in round_rocks_set[col]:
                cube_rocks_ns[col][cube_idx].num_rocks += 1
            elif ((cube_idx + cube_idx_add) < len(cube_rocks_ns[col])) and ((cube_idx + cube_idx_add) >= 0) and (cube_rocks_ns[col][cube_idx + cube_idx_add].y == row):
                cube_idx += cube_idx_add
        # print(f'col = {col}, row = {row}, cube_idx = {cube_idx}, cube_rocks[{col}][{cube_idx}] = {cube_rocks_ns[col][cube_idx]}')

    return {r for cr in cube_rocks_ns for c in cr for r in c.get_rock_coords(north)}

def tilt_ew(east: bool, cube_rocks_ew: list, round_rocks: set) -> set:

    # Constuct a list of sets of round rocks for each row
    round_rocks_set = [set() for _ in range(len(cube_rocks_ew))]
    for r in round_rocks:
        round_rocks_set[len(cube_rocks_ew) - r.y].add(r.x)

    # print(f'round_rocks = {sorted(round_rocks)}')
    # For row, iterate through the rows in the direction of tilt
    # If there are no other cube rocks in the way, add this round rock to the cube rock counter
    for row in range(len(cube_rocks_ew)):
        for c in cube_rocks_ew[row]:
            c.reset()
        # print(f'round_rocks_set[{row}] = {round_rocks_set[row]}')
        if len(round_rocks_set[row]) == 0:
            continue
        cube_idx = 0 if east else len(cube_rocks_ew[row]) - 1
        cube_idx_add = 1 if east else -1
        # print(f'cube_rocks[{row}] = {cube_rocks_ew[row]}')
        cols_to_test = {r for r in round_rocks_set[row]}.union(c.x for c in cube_rocks_ew[row])
        for col in reversed(sorted(cols_to_test)) if east else sorted(cols_to_test):
            # print(f'row = {row}, col = {col}, cube_idx = {cube_idx}, cube_rocks[{row}][{cube_idx}] = {cube_rocks_ew[row][cube_idx]}')
            if col in round_rocks_set[row]:
                cube_rocks_ew[row][cube_idx].num_rocks += 1
            elif ((cube_idx + cube_idx_add) < len(cube_rocks_ew[row])) and ((cube_idx + cube_idx_add) >= 0) and (cube_rocks_ew[row][cube_idx + cube_idx_add].x == col):
                cube_idx += cube_idx_add
        # print(f'row = {row}, col = {col}, cube_idx = {cube_idx}, cube_rocks[{row}][{cube_idx}] = {cube_rocks_ew[row][cube_idx]}')

    return {r for cr in cube_rocks_ew for c in cr for r in c.get_rock_coords(east)}

def print_map(map: list, round_rocks: set) -> None:
    for r in reversed(range(1,len(map) + 1)):
        for c in range(1,len(map[r- 1]) + 1):
            if Coord(c, r) in round_rocks:
                print('O', end='')
            else:
                m = map[len(map) + 1 - (r + 1)][c-1]
                if m == 'O':
                    print('.', end='')
                else:
                    print (m, end='')
        print()
    print()

def main():
    dish_map = [l.strip() for l in fileinput.input()]
    print(dish_map)

    # Set of all coords for round rocks
    round_rocks = {Coord(x + 1, len(dish_map) - y) for y in range(len(dish_map)) for x in range(len(dish_map[0])) if dish_map[y][x] == 'O'}
    
    # List of coords of cube rocks for each column of the map
    cube_rocks_ns = [[CoordNS(x + 1, len(dish_map) - y) for y in range(len(dish_map)) if dish_map[y][x] == '#'] for x in range(len(dish_map[0]))]
    for i in range(len(cube_rocks_ns)):
        cube_rocks_ns[i].insert(0, CoordNS(i + 1, len(dish_map)+1))
        cube_rocks_ns[i].append(CoordNS(i + 1, 0))

    # List of coords of cube rocks for each row of the map
    cube_rocks_ew = [[CoordEW(x + 1, len(dish_map) - y) for x in reversed(range(len(dish_map[0]))) if dish_map[y][x] == '#'] for y in range(len(dish_map))]
    print(f'cube_rocks_ew = {cube_rocks_ew}')
    for i in range(len(cube_rocks_ew)):
        cube_rocks_ew[i].insert(0, CoordEW(len(dish_map[0]) + 1, len(dish_map) - i))
        cube_rocks_ew[i].append(CoordEW(0, len(dish_map) - i))

    print(f'round_rocks = {round_rocks}')
    print(f'cube_rocks_ns = {cube_rocks_ns}')
    print(f'cube_rocks_ew = {cube_rocks_ew}')

    round_rocks = tilt_ns(True, cube_rocks_ns, round_rocks)
    print_map(dish_map, round_rocks)    

    print(f'p1_sum = {sum([c.y for c in round_rocks])}')

    # Start of p2
    # Re-init starting round rock starting positions from map
    round_rocks = {Coord(x + 1, len(dish_map) - y) for y in range(len(dish_map)) for x in range(len(dish_map[0])) if dish_map[y][x] == 'O'}

    saved_round_rocks = {}
    saved_weights = []
    cycle_length = 0
    cycle_offset = 0
    for i in range(1000000000):
        round_rocks = tilt_ns(True, cube_rocks_ns, round_rocks)
        round_rocks = tilt_ew(False, cube_rocks_ew, round_rocks) 
        round_rocks = tilt_ns(False, cube_rocks_ns, round_rocks)
        round_rocks = tilt_ew(True, cube_rocks_ew, round_rocks) 
        #print(f'i = {i}, p2_sum = {sum([c.y for c in round_rocks])}')
        key = tuple(round_rocks)
        if key in saved_round_rocks:
            index = saved_round_rocks[key]
            if cycle_length == 0:
                cycle_length = i - index
                cycle_offset = index
                print(f'cycle_length = {cycle_length}, cycle_offset = {cycle_offset}')
            break
        saved_round_rocks[tuple(round_rocks)] = i
        saved_weights.append(sum([c.y for c in round_rocks]))

    # for i in range(2, 30):
    #     print(f'i = {i}, p2_sum = {saved_weights[i]}, p2_sum from cycle = {saved_weights[(i - cycle_offset) % cycle_length + cycle_offset]}')
    print(f'p2_sum from cycle = {saved_weights[(1000000000 - 1 - cycle_offset) % cycle_length + cycle_offset]}')

if __name__ == '__main__':
    main()