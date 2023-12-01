#!/usr/bin/env python3

import fileinput

# Given an input line, find the first
# digit on that line. Return the int
# value of the digit found
def read_first_digit(line : str):
    for c in line:
        if c.isnumeric():
            return int(c)

    return None

sum = 0
for line in fileinput.input():
    # The first digit found in the line is the 10s
    # place for the number created from that line
    sum += read_first_digit(line) * 10

    # Finding the first digit of the reversed input line
    # will get the last digit on the line. That
    # goes into the 1s place for the number created
    # from this input line
    sum += read_first_digit(reversed(line))

print(f"Part 1: {sum}")