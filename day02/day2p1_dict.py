#!/usr/bin/env python3

import fileinput
from math import prod
import re

def parse_hand_string(hand_string: str, max_rgb: dict) -> dict:
    for cube_string in hand_string.split(','):
        m = re.compile('\s+(\d+)\s+(blue|red|green)').match(cube_string)
        if m:
            max_rgb[m.group(2)] = max(max_rgb[m.group(2)], int(m.group(1)))

    return max_rgb

def parse_game_string(game_string: str):
    game_number_string, hands_string = game_string.split(':', 1)
    m = re.compile('Game\s+(\d+)').match(game_number_string)
    if m:
        game_number = int(m.group(1))
    else:
        raise Exception(f"Error : no game number string found in {game_string}")

    max_rgb = {'red': 0, 'green': 0, 'blue': 0}
    for hand in hands_string.split(';'):
        max_rgb = parse_hand_string(hand, max_rgb)

    return game_number, max_rgb

sum = 0
power = 0
max_rgb = {'red': 12, 'green': 13, 'blue': 14}
for line in fileinput.input():
    game_number, game_rgb = parse_game_string(line)
    power += prod(game_rgb.values())
    if all([value <= max_rgb[color] for color, value in game_rgb.items()]):
        sum += game_number

print(f'Sum = {sum}')
print(f'Power = {power}')