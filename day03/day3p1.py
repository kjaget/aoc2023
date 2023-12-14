#!/usr/bin/env python3
import fileinput

from dataclasses import dataclass
from math import prod

@dataclass
class Coord():
    x: int
    y: int

    def is_adjacent(self, symbols: set):
        offsets = [-1, 0, 1]
        for xo in offsets:
            for yo in offsets:
                for s in symbols:
                    if ((self.x + xo) == s.x) and ((self.y + yo) == s.y):
                        print(f'{self} is adjacent to {s}')
                        return True

        return False

    # write a function to generate a perfect hash from two integers less than 200
    def __hash__(self):
        return self.x * 31 + self.y

symbols = set()
gears = set()
lines = []
y = 0
for line in fileinput.input():
    lines.append(line)
    for x, ch in enumerate(lines[-1]):
        if (not ch.isnumeric()) and (ch != '.') and (ch != '\n'):
            symbols.add(Coord(x, y))
            if ch == '*':
                gears.add(Coord(x,y))
    y += 1

print(f'symbols = {symbols}')
sum = 0
y = 0
for line in lines:
    current_val = 0
    keep_number = False
    for x, ch in enumerate(line):
        if ch.isnumeric():
            current_val = current_val * 10 + int(ch)
            #print(f'Testing {ch} at {x}, {y}')
            if (not keep_number) and Coord(x,y).is_adjacent(symbols):
                keep_number = True
        else:
            # on the first non-number seen after a value which was
            # adjacent to a symbol, update the running sum of such numbers
            if keep_number: 
                print(f'Keeping {current_val}')
                sum += current_val
                keep_number = False
            elif current_val != 0:
                print(f'Not keeping {current_val}')
            # Reset current value on non-number inputs
            current_val = 0

    y += 1


gear_ratio = 0
for g in gears:
    y = 0
    print(f'testing {g}')
    products = []
    for line in lines:
        current_val = 0
        keep_number = False
        for x, ch in enumerate(line):
            if ch.isnumeric():
                current_val = current_val * 10 + int(ch)
                #print(f'Testing {ch} at {x}, {y}')
                if (not keep_number) and Coord(x,y).is_adjacent([g]):
                    keep_number = True
            else:
                # on the first non-number seen after a value which was
                # adjacent to a symbol, update the running sum of such numbers
                if keep_number: 
                    print(f'Keeping {current_val}')
                    products.append(current_val)
                    keep_number = False
                elif current_val != 0:
                    print(f'Not keeping {current_val}')
                # Reset current value on non-number inputs
                current_val = 0

        y += 1

    if len(products) == 2:
        gear_ratio += prod(products)

print(f'Sum = {sum}')
print(f'Gear ratio = {gear_ratio}')
