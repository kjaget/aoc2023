#!/usr/bin/env python3
import fileinput
from queue import PriorityQueue
from typing import Optional 


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

class State():
    coord: Coord
    heading: Coord
    forward_count: int
    def __init__(self, coord: Coord, direction: Coord, forward_count: int = 0):
        self.coord = coord
        self.heading = direction
        self.forward_count = forward_count
    
    def __hash__(self):
        return hash(self.coord) + hash(self.heading) * 31 + self.forward_count * (31 * 31 - 1)

    def __eq__(self, other) -> bool:
        return (self.coord == other.coord) and (self.heading == other.heading) and (self.forward_count == other.forward_count)
    
    def __str__(self):
        return f'({self.coord}, {self.heading}, {self.forward_count})'

    def __lt__(self, other) -> bool:
        if (self.coord == other.coord):
            if (self.heading == other.heading):
                return self.forward_count < other.forward_count
            return self.heading < other.heading
        return self.coord < other.coord

    __repr__ = __str__

# left, right, forward, used to index into direction_left, right, up, down
L = 0
R = 1
F = 2 

N = Coord(0, -1)
S = Coord(0, 1)
E = Coord(1, 0) 
W = Coord(-1, 0)

direction_west  = [S, N, W]
direction_east  = [N, S, E]
direction_north = [W, E, N]
direction_south = [E, W, S]

directions = {W: direction_west, E: direction_east, N: direction_north, S: direction_south}

def calc_cost(tiles: list, dest_coord: Coord) -> int:
    return tiles[dest_coord.y][dest_coord.x]


# Get list of valid moves from current state
def neighbors(tiles: list, state: State, p1: bool) -> list[list[State]]:
    ret = []
    if p1 and (state.forward_count >= 3):
        return ret
    if (not p1) and (state.forward_count >= 10):
        return ret
    for d in [L, R, F]:
        new_direction = directions[state.heading][d]
        new_coord = state.coord + new_direction

        if (new_coord.x < 0) or (new_coord.x >= len(tiles[0])) or (new_coord.y < 0) or (new_coord.y >= len(tiles)):
            continue

        forward_count = state.forward_count + 1 if d == F else 0
        if p1 and (forward_count >= 3):
            continue

        new_states = [State(new_coord, new_direction, forward_count)]
        if not p1:
            inside_map = True
            while inside_map and (forward_count < 3):
                new_coord = new_coord + new_direction
                if (new_coord.x < 0) or (new_coord.x >= len(tiles[0])) or (new_coord.y < 0) or (new_coord.y >= len(tiles)):
                    # print(f'        Out of bounds {new_coord}')
                    inside_map = False
                    continue
                forward_count += 1
                new_states.append(State(new_coord, new_direction, forward_count))
            if not inside_map:
                continue
            if forward_count >= 10:
                continue 

        ret.append(new_states)
    
    return ret

def bfs(tiles: list, starts: list[State], costs: list[int], goal: Coord, p1: bool) -> (int, dict[State, Optional[State]]):
    states_to_check = PriorityQueue()
    reached: dict[State, int] = {}
    came_from: dict[State] = {}
    for start, cost in zip(starts, costs):
        states_to_check.put((cost, start))
        reached[start] = cost
        came_from[start] = None

    while not states_to_check.empty():
        state: State = states_to_check.get()[1]
        if state.coord == goal:
            print(f'Found goal {state}')
            cost = reached[state]
            break

        cost = reached[state]
        # print (f'  Visiting {state} : cost = {cost}')
        for new_states in neighbors(tiles, state, p1):
            # print(f'        new_state {new_states}')
            new_cost = cost
            for new_state in new_states:
                new_cost = new_cost + calc_cost(tiles, new_state.coord)
                # print(f'            new_state {new_state} : new_cost = {new_cost}')
            if (new_state not in reached) or (new_cost < reached[new_state]):
                # print(f'        new_state {new_state} : new_cost = {new_cost} : adding to queue')
                reached[new_state] = new_cost
                states_to_check.put((new_cost, new_state))
                came_from[new_state] = state

    return cost, came_from

def get_goal_state(came_from: dict[State, Optional[State]], goal: Coord) -> Optional[State]:
    for d in [N, S, E, W]:
        for s in range(11):
            if State(goal, d, s) in came_from:
                return State(goal, d, s)

    return None

def reconstruct_path(came_from: dict[State, Optional[State]], start: Coord, goal: Coord) -> list[Coord]:
    current: State = get_goal_state(came_from, goal)
    ret:list[Coord] = []
    if (current not in came_from):
        return ret
    while current.coord != start:
        ret.append(current.coord)
        current = came_from[current]
    ret.append(start)
    ret.reverse()
    return ret

def print_path(tiles: list, path: list[Coord]):
    for y in range(len(tiles)):
        for x in range(len(tiles[0])):
            if Coord(x, y) in path:
                print('#', end='')
            else:
                print('.', end='')
        print()
            
def main():
    tiles = []
    for line in fileinput.input():
        tiles.append([int(c) for c in line.strip()])

    cost, came_from = bfs(tiles, [State(Coord(0, 0), E, 1), State(Coord(0,0), S, 1)], [0, 0], Coord(len(tiles[0]) - 1, len(tiles) - 1), True)   
    path = reconstruct_path(came_from, Coord(0, 0), Coord(len(tiles[0]) - 1, len(tiles) - 1))

    print_path(tiles, path)

    print(f'p1 = {cost}')

    e_start = neighbors(tiles, State(Coord(-1, 0), E, -1), False)[0]
    e_start_cost = sum([tiles[c.coord.y][c.coord.x] for c in e_start[1:]])
    s_start = neighbors(tiles, State(Coord(0, -1), S, -1), False)[0]
    s_start_cost = sum([tiles[c.coord.y][c.coord.x] for c in s_start[1:]])
    cost, came_from = bfs(tiles, [e_start[-1], s_start[-1]], [e_start_cost, s_start_cost], Coord(len(tiles[0]) - 1, len(tiles) - 1), False)   
    #path = reconstruct_path(came_from, Coord(0, 0), Coord(len(tiles[0]) - 1, len(tiles) - 1))

    #print_path(tiles, path)

    print(f'p2 = {cost}')

if __name__ == '__main__':
    main()