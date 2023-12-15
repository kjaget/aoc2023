#!/usr/bin/env python3
import fileinput
from dataclasses import dataclass

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

    def get_rock_value(self) -> int:
        ret = 0
        for i in range(self.num_rocks):
            ret += self.y - (i + 1)
        return ret
    
    def get_rock_coords(self) -> list:
        return [Coord(self.x, self.y - (i + 1)) for i in range(self.num_rocks)]
    
    def __str__(self):
        return f'CoordNS({self.x}, {self.y}): {self.num_rocks}'

class CoordEW(Coord):
    num_rocks: int = 0

    def reset(self):
        self.num_rocks = 0

    # def get_rock_value(self) -> int:
    #     ret = 0
    #     for i in range(self.num_rocks):
    #         ret += self.y - (i + 1)
    #     return ret
    
    def get_rock_coords(self) -> list:
        return [Coord(self.x - (i + 1), self.y) for i in range(self.num_rocks)]

    def __str__(self):
        return f'CoordEW({self.x}, {self.y}): {self.num_rocks}'

def round_rocks_from_cube_rocks(cube_rocks: list) -> list:
    output_round_rocks = [set()] * len(cube_rocks)
    for cr in cube_rocks:
        for c in cr:
            for r in c.get_rock_coords():
                output_round_rocks[r.x - 1].add(r.y)
    return output_round_rocks

def tilt_ns(north: bool, num_rows: int, cube_rocks_ns: list, round_rocks: set) -> (list, set):
    for cr in cube_rocks_ns:
        for c in cr:
            c.reset()

    # Constuct a list of sets of round rocks for each column
    round_rocks_set = [set() for _ in range(len(cube_rocks_ns))]
    for r in round_rocks:
        round_rocks_set[r.x - 1].add(r.y)

    print(f'round_rocks = {round_rocks}')
    # For each column, iterate through the rows in the direction of tilt
    # If there are no other cube rocks in the way, add this round rock to the cube rock counter
    for col in range(len(cube_rocks_ns)):
        for c in cube_rocks_ns[col]:
            c.reset()
        cube_idx = 0
        print(f'cube_rocks[{col}] = {cube_rocks_ns[col]}')
        print(f'round_rocks_set[{col}] = {round_rocks_set[col]}')
        for row in reversed(range(1, num_rows+1)) if north else range(1, num_rows+1):
            print(f'col = {col}, row = {row}, cube_idx = {cube_idx}, cube_rocks[{col}][{cube_idx}] = {cube_rocks_ns[col][cube_idx]}')
            if row in round_rocks_set[col]:
                cube_rocks_ns[col][cube_idx].num_rocks += 1
            elif ((cube_idx + 1) < len(cube_rocks_ns[col])) and (cube_rocks_ns[col][cube_idx + 1].y == row):
                cube_idx += 1
        print(f'col = {col}, row = {row}, cube_idx = {cube_idx}, cube_rocks[{col}][{cube_idx}] = {cube_rocks_ns[col][cube_idx]}')

    return cube_rocks_ns, {r for cr in cube_rocks_ns for c in cr for r in c.get_rock_coords()}

def tilt_ew(east: bool, num_cols: int, cube_rocks_ew: list, round_rocks: set) -> (list, set):

    # Constuct a list of sets of round rocks for each row
    round_rocks_set = [set() for _ in range(len(cube_rocks_ew))]
    for r in round_rocks:
        round_rocks_set[r.y - 1].add(r.x)

    print(f'round_rocks = {sorted(round_rocks)}')
    # For row, iterate through the rows in the direction of tilt
    # If there are no other cube rocks in the way, add this round rock to the cube rock counter
    for row in range(len(cube_rocks_ew)):
        for c in cube_rocks_ew[row]:
            c.reset()
        cube_idx = 0
        print(f'cube_rocks[{row}] = {cube_rocks_ew[row]}')
        print(f'round_rocks_set[{row}] = {round_rocks_set[row]}')
        for col in reversed(range(1, num_cols+1)) if east else range(1, num_cols+1):
            print(f'row = {row}, col = {col}, cube_idx = {cube_idx}, cube_rocks[{row}][{cube_idx}] = {cube_rocks_ew[row][cube_idx]}')
            if col in round_rocks_set[row]:
                cube_rocks_ew[row][cube_idx].num_rocks += 1
            elif ((cube_idx + 1) < len(cube_rocks_ew[row])) and (cube_rocks_ew[row][cube_idx + 1].y == col):
                cube_idx += 1
        print(f'row = {row}, col = {col}, cube_idx = {cube_idx}, cube_rocks[{row}][{cube_idx}] = {cube_rocks_ew[row][cube_idx]}')

    return cube_rocks_ew, {r for cr in cube_rocks_ew for c in cr for r in c.get_rock_coords()}

def print_map(map: list, round_rocks: set, cols: int, rows: int) -> None:
    for r in reversed(range(1,len(map) + 1)):
        for c in range(1,len(map[r- 1]) + 1):
            if Coord(c, r) in round_rocks:
                print('O', end='')
            else:
                print(f'{map[len(map) + 1 - (r+1)][c-1]}', end='')
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
    cube_rocks_ew = [[CoordEW(x + 1, len(dish_map) - y) for x in range(len(dish_map[0])) if dish_map[y][x] == '#'] for y in range(len(dish_map))]
    print(f'cube_rocks_ew = {cube_rocks_ew}')
    for i in range(len(cube_rocks_ew)):
        cube_rocks_ew[i].insert(0, CoordEW(len(dish_map[0]) + 1, len(dish_map) - i))
        cube_rocks_ew[i].append(CoordEW(0, len(dish_map) - i))

    print(f'round_rocks = {round_rocks}')
    print(f'cube_rocks_ns = {cube_rocks_ns}')
    print(f'cube_rocks_ew = {cube_rocks_ew}')

    cube_rocks_ns, round_rocks = tilt_ns(True, len(dish_map), cube_rocks_ns, round_rocks)
    print_map(dish_map, round_rocks, len(dish_map[0]), len(dish_map))    

    p1_sum = 0
    for r in range(len(cube_rocks_ns)):
        print(f'cube_rocks_ns[{r}] = ')
        for c in range(len(cube_rocks_ns[r])):
            rock_val = cube_rocks_ns[r][c].get_rock_value()
            print(f'    {cube_rocks_ns[r][c]} = {rock_val}')
            p1_sum += rock_val

    print(f'p1_sum = {p1_sum}')

    cube_rocks_ew, round_rocks = tilt_ew(True, len(dish_map), cube_rocks_ew, round_rocks) 
    print_map(dish_map, round_rocks, len(dish_map[0]), len(dish_map))    
if __name__ == '__main__':
    main()