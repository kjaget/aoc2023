#!/usr/bin/env python3

from dataclasses import dataclass
import fileinput
from typing import Optional

class Coord():
    x: int
    y: int
    Z: int

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __hash__(self):
        return self.x * 511 + self.y * 31 + self.z

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y, self.z + other.z)

    def __eq__(self, other: object) -> bool:
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def __lt__(self, other: object) -> bool:
        if (self.z == other.z) and (self.y == other.y):
            return self.x < other.x
        if (self.z == other.z):
            return self.y < other.y
        return self.z < other.z
            
    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'
    __repr__ = __str__

@dataclass
class PositionVelocity():
    position: Coord
    velocity: Coord
    
    def __str__(self):
        return f'({self.position} @ {self.velocity})'

    def m(self) -> float:
        return float(self.velocity.y) / float(self.velocity.x)

    def b(self) -> float:
        return self.position.y - self.m() * self.position.x
    __repr__ = __str__

    def intersection(self, other) -> Optional[Coord]:
        a = self.m()
        b = other.m()
        c = self.b()
        d = other.b()

        if a == b:
            if c == d:
                return Coord(0, 0, -1)
            else:
                return None

        x = (d - c) / (a - b)
        y = a * (d - c) / (a - b) + c

        return Coord(x, y, 0)

'''
y - py  = vy / vx (x - px)
y = m x - m px + py
y = m x + ( py - m px )

x = (py2 - m2 px2) - (py1 - m1 px1)
'''

def read_hailstones(line: str) -> PositionVelocity:

    position, velocity = line.split('@')
    p = position.split(',')
    v = velocity.split(',')

    return PositionVelocity(Coord(int(p[0]), int(p[1]), int(p[2])), Coord(int(v[0]), int(v[1]), int(v[2])))

def main():
    hailstones = []
    for line in fileinput.input():
        hailstones.append(read_hailstones(line.strip()))

    print(hailstones)

    for h in hailstones:
        print(f'{h}, m: {h.m()}, b: {h.b()}')

    min_int = 7
    max_int = 27
    for r in range(len(hailstones)):
        for r2 in range(r + 1, len(hailstones)):
            print(f'Hailstone A: {hailstones[r]}')
            print(f'Hailstone B: {hailstones[r2]}')
            i = hailstones[r].intersection(hailstones[r2])
            print(i)
                



if __name__ == '__main__':
    main()