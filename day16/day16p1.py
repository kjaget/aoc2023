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

    def __eq__(self, other: object) -> bool:
        return (self.x == other.x) and (self.y == other.y)

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

class State():
    coord: Coord
    direction: Coord
    def __init__(self, coord: Coord, direction: Coord):
        self.coord = coord
        self.direction = direction
    
    def __hash__(self):
        return hash(self.coord) + hash(self.direction) * 31

    def __eq__(self, other: object) -> bool:
        return (self.coord == other.coord) and (self.direction == other.direction)
    
    def __str__(self):
        return f'({self.coord}, {self.direction})'

    __repr__ = __str__

N = Coord(0, -1)
S = Coord(0, 1)
E = Coord(1, 0) 
W = Coord(-1, 0)

# Maps to find next direction from prev direction
direction_map_n = {'.': [N], '/': [E], '\\': [W], '|': [N], '-': [W, E]}
direction_map_s = {'.': [S], '/': [W], '\\': [E], '|': [S], '-': [W, E]}
direction_map_e = {'.': [E], '/': [N], '\\': [S], '-': [E], '|': [N, S]}
direction_map_w = {'.': [W], '/': [S], '\\': [N], '-': [W], '|': [N, S]}

# Make this a list instead, and make N,S,E,w constants 0..3
# might be faster
# would have to make a similar list of directions to do the next_state = coord + direction[DIRECTION] math below
direction_map = {N: direction_map_n, S: direction_map_s, E: direction_map_e, W: direction_map_w}

# Changing this to recursion would let the code save the coords added
# as a result of each starting state and save them in a dict. The results
# could be reused the next time the state is hit. This would be a lot faster
# for part 2?
def calc_map(tiles: list, start: State) -> int:
    states_to_check = [start]
    states_checked = set()
    while len(states_to_check) > 0:
        state_to_check = states_to_check.pop(-1)
        if (state_to_check.coord.x < 0) or (state_to_check.coord.x >= len(tiles[0])) or (state_to_check.coord.y < 0) or (state_to_check.coord.y >= len(tiles)):
            # print(f'Out of bounds {state_to_check}')
            continue
        states_checked.add(state_to_check)
        next_directions = direction_map[state_to_check.direction][tiles[state_to_check.coord.y][state_to_check.coord.x]]
        # print(f'Checking {state_to_check} on tile {tiles[state_to_check.coord.y][state_to_check.coord.x]} with next direction {next_directions}')
        # print(f'\tstates_checked {states_checked}')
        for next_direction in next_directions:
            next_state = State(state_to_check.coord + next_direction, next_direction)
            if next_state not in states_checked:
                # print(f'Next state {next_state}')
                states_to_check.append(next_state)
            else:
                # print(f'Already checked {next_state} : states checked {states_checked}')
                pass
    

    energized_tiles = set()
    for s in states_checked:
        energized_tiles.add(s.coord)

    # for r in range(len(tiles)):
    #     for c in range(len(tiles[0])):
    #         if Coord(c, r) in energized_tiles:
    #             print('#', end='')
    #         else:
    #             print('.', end='')
    #     print()
    return len(energized_tiles)


def main():
    tiles = []
    for line in fileinput.input():
        tiles.append([c for c in line.strip()])
    print(f'p1 = {calc_map(tiles, State(Coord(0, 0), E))}')

    p2_max = 0
    for c in range(len(tiles[0])):
        p2_max = max(p2_max, calc_map(tiles, State(Coord(c, 0), S)))
        p2_max = max(p2_max, calc_map(tiles, State(Coord(c, len(tiles[0]) - 1), N)))
        print('.', end='')

    for r in range(len(tiles)):
        p2_max = max(p2_max, calc_map(tiles, State(Coord(0, r), E)))
        p2_max = max(p2_max, calc_map(tiles, State(Coord(len(tiles) - 1, r), W)))
        print('.', end='')

    print(f'p2_max = {p2_max}')

if __name__ == '__main__':
    main()