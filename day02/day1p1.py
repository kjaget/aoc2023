#!/usr/bin/env python3

from dataclasses import dataclass
import fileinput
import re

@dataclass
class RGB:
    R:int = 0
    G:int = 0
    B:int = 0

def parse_hand_string(hand_string: str, max_rgb: RGB) -> RGB:
    cube_strings = hand_string.split(',')
    for cube_string in cube_strings:
        m = re.compile('\s+(\d+)\s+(blue|red|green)').match(cube_string)
        if m:
            if m.group(2) == 'red':
                max_rgb.R = max(max_rgb.R, int(m.group(1)))
            elif m.group(2) == 'green':
                max_rgb.G = max(max_rgb.G, int(m.group(1)))
            elif m.group(2) == 'blue':
                max_rgb.B = max(max_rgb.B, int(m.group(1)))

    return max_rgb

def parse_game_string(game_string: str):
    game_number_string, hands_string = game_string.split(':', 1)
    m = re.compile('Game\s+(\d+)').match(game_number_string)
    if m:
        game_number = int(m.group(1))
    else:
        print(f"Error : no game number string found in {game_string}")
        return None, None

    hands = hands_string.split(';')
    max_rgb = RGB(0, 0, 0)

    for hand in hands:
        max_rgb = parse_hand_string(hand, max_rgb)

    return game_number, max_rgb


sum = 0
power = 0
max_rgb = RGB(12, 13, 14)
for line in fileinput.input():
    game_number, game_rgb = parse_game_string(line)
    power += game_rgb.R * game_rgb.G * game_rgb.B
    if game_rgb.R > max_rgb.R:
        continue
    if game_rgb.G > max_rgb.G:
        continue
    if game_rgb.B > max_rgb.B:
        continue
    sum += game_number

print(f'Sum = {sum}')
print(f'Power = {power}')