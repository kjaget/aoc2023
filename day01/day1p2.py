#!/usr/bin/env python3

import fileinput
from sys import maxsize

def find_in_line(line : str, strings : list, best_position: int, best_value: int, forward: bool):
    # Get both the index and the string for the list we're checking
    for index, string in enumerate(strings):
        # Use find / r[everse]find to get the first / last occurance of the
        # string being searched for
        # This returns in the index where the number string is found in line,
        # or -1 if it isn't found anywere
        position = line.find(string) if forward else line.rfind(string)
        if (position != -1): # If the string is found
            # And if the index is "better" than the previous best, meaning it is lower
            # if we're searching forwards or higher if we're searching in reverse,
            # update this instance as the best position and value
            if (forward and (position < best_position)) or (not forward and (position > best_position)):
                best_position = position
                best_value = index + 1 # strings to search for start with the value 1/one at index 0, so add 1 to find the int value
        #print(f'{forward}, {index}, {string} in {line.strip()} at pos {position} : best = {best_position}, {best_value}')

    return best_position, best_value


def read_digit_p2(line: str, forward: bool):
    numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    # Set position to be invalid, so that anything found at any position
    # is thought to be before this value and used as the initial best
    # result.
    position = maxsize if forward else -1
    position, value = find_in_line(line, numbers, position, None, forward)
    position, value = find_in_line(line, digits, position, value, forward)

    return value


sum = 0
for line in fileinput.input():
    sum += read_digit_p2(line, True) * 10
    sum += read_digit_p2(line, False)


print(f"Part 2: {sum}")