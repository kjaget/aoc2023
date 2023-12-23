#!/usr/bin/env python3

import fileinput
import numpy as np
import cv2

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

direction_map = {'U': U, 'D': D, 'R': R, 'L': L}

def add_to_perimiter(perimiter: list, direction_char: str, distance: int) -> list:
    direction = direction_map[direction_char[0]]

    for _ in range(distance):
        perimiter.append(perimiter[-1] + direction)

    return perimiter

def add_to_perimiter2(perimiter: list, direction_char: str, distance: int) -> list:
    direction = direction_map[direction_char[0]]

    perimiter.append(perimiter[-1] + direction * distance)

    return perimiter

def add_to_perimiter3(perimiter: list, color_str:str) -> (list[Coord], int):
    direction_char = int(color_str[-2])
    directions = [R, D, L, U]
    distance = int(color_str[2:-2], 16)

    perimiter.append(perimiter[-1] + directions[direction_char] * distance)

    return perimiter, distance

def shoelace_area(perimiter: list[Coord]) -> int:
    sum1 = 0
    sum2 = 0

    perimiter_len = len(perimiter)
    for i in range(perimiter_len - 1):
        sum1 += perimiter[i].x * perimiter[i + 1].y
        sum2 += perimiter[i].y * perimiter[i + 1].x


    sum1 += perimiter[perimiter_len - 1].x * perimiter[0].y
    sum2 += perimiter[0].x * perimiter[perimiter_len - 1].y

    return abs(sum1 - sum2) // 2

def main():
    perimiter2 = [Coord(0,0)]
    perimiter3 = [Coord(0,0)]
    p2 = 1
    p3 = 1
    for line in fileinput.input():
        #print(line.strip().split(' '))
        direction, distance, color = line.strip().split(' ')
        perimiter2 = add_to_perimiter2(perimiter2, direction, int(distance))
        p2 += int(distance)
        perimiter3, distance = add_to_perimiter3(perimiter3, color)
        p3 += distance

    # Shoelace area + pick's theorem
    print(f'shoelace area p1: {shoelace_area(perimiter2) + (p2 + 1)// 2 }')
    print(f'shoelace area p2: {shoelace_area(perimiter3) + (p3 + 1)// 2 }')

if __name__ == '__main__':
    main()