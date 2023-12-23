#!/usr/bin/env python3

from asyncio.format_helpers import _format_callback_source
import fileinput
from dataclasses import dataclass

class Box:
    def __init__(self) -> None:
        self.labels = []
        self.focal_lengths = []

    def add(self, label:str, focal_length:int) -> None:
        if label in self.labels:
            self.focal_lengths[self.labels.index(label)] = focal_length
        else:
            self.labels.append(label)
            self.focal_lengths.append(focal_length)

    def remove(self, label:str) -> None:
        if label in self.labels:
            idx = self.labels.index(label)
            self.labels.pop(idx)
            self.focal_lengths.pop(idx)

    def power(self) -> int:
        return sum([self.focal_lengths[i] * (i + 1) for i in range(len(self.focal_lengths))])


def hash(code: str) -> int:
    current_value = 0
    for c in code:
        current_value = ((current_value + ord(c)) * 17) % 256
    return current_value

def main():
    codes = [line.strip().split(',') for line in fileinput.input()][0]
    # print(codes)
    print(f'p1_sum = {sum([hash(code) for code in codes])}')

    # p2
    boxes = [Box() for _ in range(256)]
    for code in codes:
        if '=' in code:
            label, focal_length = code.split('=')
            boxes[hash(label)].add(label, int(focal_length))
        else:
            s = code[:-1]
            boxes[hash(s)].remove(s)

        """
        print(f'code = {code}')
        for i in range(len(boxes)):
            if len(boxes[i].labels) > 0:
                print(f'{i}: {boxes[i].labels} {boxes[i].focal_lengths}')
        """

    p2_sum = sum([boxes[i].power() * (i + 1) for i in range(len(boxes))])
    print(f'p2_sum = {p2_sum}')



if __name__ == '__main__':
    main()