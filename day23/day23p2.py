#!/usr/bin/env python3
import fileinput
from typing import Optional 
from copy import deepcopy

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
    direction: Coord
    def __init__(self, coord: Coord, direction: Coord):
        self.coord = coord
        self.direction = direction
    
    def __hash__(self):
        return hash(self.coord) + hash(self.direction) * 31

    def __eq__(self, other) -> bool:
        return (self.coord == other.coord) and (self.direction == other.direction)
    
    def __str__(self):
        return f'({self.coord}, {self.direction})'

    def __lt__(self, other) -> bool:
        if (self.coord == other.coord):
            return self.direction < other.direction
        return self.coord < other.coord

    __repr__ = __str__

# left, right, forward, used to index into direction_left, right, up, down
N = Coord(0, -1)
S = Coord(0, 1)
E = Coord(1, 0) 
W = Coord(-1, 0)

opposite_directions = {W: E, E: W, N: S, S: N}

slides = {'v': S, '^': N, '<': W, '>': E}

# Get list of valid moves from current state
def neighbors(tiles: list, state: State, p1: bool) -> list[State]:
    ret = []
    if p1 and (tiles[state.coord.y][state.coord.x] in slides.keys()):
        new_direction = slides[tiles[state.coord.y][state.coord.x]]
        return [State(state.coord + new_direction, new_direction)]

    for new_direction in [N, S, E, W]:
        if new_direction == opposite_directions[state.direction]:
            continue

        new_coord = state.coord + new_direction
        if tiles[new_coord.y][new_coord.x] =='#':
            continue

        if (new_coord.x < 0) or (new_coord.x >= len(tiles[0])) or (new_coord.y < 0) or (new_coord.y >= len(tiles)):
            continue

        if p1 and (tiles[new_coord.y][new_coord.x] in slides.keys()):
           slide_dir = slides[tiles[new_coord.y][new_coord.x]] 
           if slide_dir == opposite_directions[new_direction]:
               continue

        ret.append(State(new_coord, new_direction))
    
    return ret

def add_state(start_coord, end_coord, path_len, edges, p1):
    if (end_coord in edges) and (start_coord in edges[end_coord]):
        print(f'\tdiscarding')
        return edges

    if start_coord not in edges:
        edges[start_coord] = {}
    if end_coord not in edges:
        edges[end_coord] = {}
    if end_coord in edges[start_coord]:
        edges[start_coord][end_coord] = max(edges[start_coord][end_coord], path_len)
    else:
        edges[start_coord][end_coord] = path_len
    if not p1:
        if start_coord in edges[end_coord]:
            edges[end_coord][start_coord] = max(edges[end_coord][start_coord], path_len)
        else:
            edges[end_coord][start_coord] = path_len
    return edges

def gen_graph(tiles: list, start: State, goal: Coord, p1: bool) -> (int, dict[State, Optional[State]]):
    states_to_check = []
    states_to_check.append((start, 1))

    edges = {}
    states_seen = set()
    while len(states_to_check) > 0:
        start_state, path_len = states_to_check.pop(0)
        path_len = 1
        if start_state.coord == goal:
            # print(f'Found goal {state}')
            continue

        n = neighbors(tiles, State(start_state.coord + start_state.direction, start_state.direction), p1)
        print(f'start_state: {start_state}, n: {n}')
    
        while len(n) == 1:
            end_state = n[0]
            path_len += 1
            if end_state.coord == goal:
                n = []
                edges = add_state(start_state.coord, end_state.coord, path_len, edges, p1)
                print(f'goal : start_state: {start_state}, end_state: {end_state}, len: {path_len}, n: {n}')
                print(edges)
            else:
                n = neighbors(tiles, end_state, p1)

        # print (f'  Visiting {state} : cost = {cost}')
        for new_state in n:
            esd = end_state.direction
            end_state = State(end_state.coord, new_state.direction)
            print(f'start_state: {start_state}, end_state: {end_state}, d: {esd}, len: {path_len}, n: {n}')
            edges = add_state(start_state.coord, end_state.coord, path_len, edges, p1)
            print(edges)
            if (start_state, end_state) not in states_seen:
                states_to_check.append((end_state, path_len + 1))
                states_seen.add((start_state, end_state))

    return edges


def toposort(coord: Coord, edges: dict, stack: list, visited: dict) -> (list, list):
    if visited[coord]:
        return stack, visited

    visited[coord] = True
    print(f'Visiting {coord}')
    for e in edges[coord]:
        print(f'\tchecking {e}')
        if not visited[e]:
            stack, visited = toposort(e, edges, stack, visited)

    stack.append(coord)

    return stack, visited


def longest_path(start_state: State, edges: dict) -> dict[int]:
    NINF:int = -10**9
    dist = {k: NINF for k in edges.keys()}
    visited = {k: False for k in edges.keys()}
    
    stack = []
    stack, visited = toposort(start_state, edges, stack, visited)
    print(f'stack: {stack}\nvisited: {visited}')

    dist[start_state] = 0
    visited = {k: False for k in edges.keys()}

    while len(stack) > 0:
        state = stack.pop(-1)
        print(f'checking coord {state}, visited = {visited[state]}')

        if dist[state] != NINF:
            visited[state] = True
            for k, v in edges[state].items():
                if dist[k] < dist[state] + v:
                    if not visited[k]:
                        print(f'\tupdating {k} to {dist[state] + v}')
                        dist[k] = dist[state] + v

    for k, v in dist.items():
        print(f'k: {k}, v: {v}')

    return dist

def exhaustive_search(start_coord: Coord, goal_coord: Coord, edges: dict, p1: bool) -> (int, set):
    coords_to_check = [(start_coord, 0, set())]
    longest_path = 0
    longest_path_edges = set()
    end_coords = set([goal_coord])
    if not p1:
        end_coords = end_coords.union({c for c in edges[goal_coord]})

    count: int = 0
    print(f'end_adjacent: {end_coords}')
    while len(coords_to_check) > 0:
        coord_to_check, path_len, coords_visited = coords_to_check.pop(-1)
        coords_visited.add(coord_to_check)
        count += 1
        if count == 100000:
            print(f'coords_to_check length = {len(coords_to_check)}')
            count = 0

        for next_coord in edges[coord_to_check]:
            if next_coord not in coords_visited:
                new_path_len = path_len + edges[coord_to_check][next_coord]
                if next_coord in end_coords:
                    if next_coord != goal_coord:
                        new_path_len += edges[next_coord][goal_coord]
                    if new_path_len > longest_path:
                        longest_path = new_path_len
                        longest_path_edges = coords_visited
                        longest_path_edges.union(end_coords)
                        print(f'New longest path is {longest_path}')
                    continue
                # print(f'Adding {next_coord}, {new_path_len}, {coords_visited}')
                coords_to_check.append((next_coord, new_path_len, deepcopy(coords_visited)))

    return longest_path, longest_path_edges


def print_path(tiles: list, coords_seen:set):
    for y in range(len(tiles)):
        for x in range(len(tiles[0])):
            if Coord(x, y) in coords_seen:
                print('O', end='')
            else:
                print(tiles[y][x], end='')
        print()


def write_dot(output_filename: str, graph_name: str, edges: dict):
    with open(output_filename, 'w') as f:
        f.write(f'digraph {graph_name} {{\n')
        for e in edges:
            for e2 in edges[e]:
                f.write(f'\t"{e.x}x{e.y}" -> "{e2.x}x{e2.y}" [label={edges[e][e2]}]\n')
        f.write('}')
            
def main():
    tiles = []
    for line in fileinput.input():
        tiles.append([c for c in line.strip()])

    start_state = State(Coord(1, 0), S)
    end_coord = Coord(len(tiles[0]) - 2, len(tiles) - 1) 
    p1_edges = gen_graph(tiles, start_state, end_coord, True)   
    write_dot("p1.dot", "p1", p1_edges)
    p1 = longest_path(start_state.coord, p1_edges)
    print(f'p1 = {p1[end_coord]}')
    # print_path(tiles, coords_seen)

    p1_length, p1_path = exhaustive_search(start_state.coord, end_coord, p1_edges, True)
    print(f'p1_length: {p1_length}')

    p2_edges = gen_graph(tiles, start_state, end_coord, False)   
    write_dot("p2.dot", "p2", p2_edges)
    p2 = longest_path(start_state.coord, p2_edges)
    print(f'p2 = {p2[end_coord]}')
    # print_path(tiles, coords_seen)
    p2_length, p2_path = exhaustive_search(start_state.coord, end_coord, p2_edges, False)
    print(f'p2_length: {p2_length}')


if __name__ == '__main__':
    main()