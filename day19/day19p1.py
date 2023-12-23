#!/usr/bin/env python3

import fileinput
import re
from dataclasses import dataclass
from typing import Optional
from copy import deepcopy

@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def get(self, register: str) -> int:
        if register == 'x':
            return self.x
        elif register == 'm':
            return self.m
        elif register == 'a':
            return self.a
        elif register == 's':
            return self.s
        else:
            raise ValueError(f"Invalid register: {register}")

    def set(self, register: str, value: int):
        if register == 'x':
            self.x = value
        elif register == 'm':
            self.m = value
        elif register == 'a':
            self.a = value
        elif register == 's':
            self.s = value
        else:
            raise ValueError(f"Invalid register: {register}")

    def value(self) -> int:
        return self.x + self.m + self.a + self.s

@dataclass
class Range:
    upper: Part = Part(4000, 4000, 4000, 4000)
    lower: Part = Part(1, 1, 1, 1)

    def valid(self):
        return self.upper.x > self.lower.x and self.upper.m > self.lower.m and self.upper.a > self.lower.a and self.upper.s > self.lower.s

    def value(self):
        return (self.upper.x - self.lower.x + 1) * (self.upper.m - self.lower.m + 1) * (self.upper.a - self.lower.a + 1) * (self.upper.s - self.lower.s + 1)


class Operation:
    def __init__(self, destination: str):
        self.destination = destination

    def __call__(self, part: Part) -> str:
        return self.destination

    def update_range(self, r: Range) -> Range:
        return r, None

    def __str__(self):
        return f'Operation : {self.destination}'
    __repr__ = __str__


class LessThanOperation(Operation):
    def __init__(self, destination: str, register: str, value: int):
        super().__init__(destination)
        self.register = register[0]
        self.value = value

    def __call__(self, part: Part) -> Optional[str]:
        # print(f'\t\tLessThanOperation.__call__({part}), {self.register}, {self.value}, {part.get(self.register)}')
        if part.get(self.register) < self.value:
            # print(f'\t\t\treturning {self.destination}')
            return self.destination
        return None

    def update_range(self, r: Range) -> (Range, Range):
        this_r = deepcopy(r)
        value = this_r.upper.get(self.register)
        if (value > self.value):
            this_r.upper.set(self.register, self.value - 1)

        next_r = deepcopy(r)
        value = next_r.lower.get(self.register)
        if (value < self.value):
            next_r.lower.set(self.register, self.value)

        # print(f'less than : self.value: {self.value}, self.register: {self.register}, r: {r}, \n\tthis_r: {this_r}, \n\tnext_r: {next_r}')

        return this_r, next_r


    def __str__(self):
        return f'LessThanOperation : {self.destination}, {self.register}, {self.value}'
    __repr__ = __str__


class GreaterThanOperation(Operation):
    def __init__(self, destination: str, register: str, value: int):
        super().__init__(destination)
        self.register = register[0]
        self.value = value

    def __call__(self, part: Part) -> Optional[str]:
        # print(f'GreaterThanOperation.__call__({part}), {self.register}, {self.value}, {part.get(self.register)}')
        if part.get(self.register) > self.value:
            return self.destination
        return None

    def __str__(self):
        return f'GreaterThanOperation : {self.destination}, {self.register}, {self.value}'
    __repr__ = __str__

    def update_range(self, r: Range) -> (Range, Range):

        this_r = deepcopy(r)
        value = this_r.lower.get(self.register)
        if (value < self.value):
            this_r.lower.set(self.register, self.value + 1)

        next_r = deepcopy(r)
        value = next_r.upper.get(self.register)
        if (value > self.value):
            next_r.upper.set(self.register, self.value)

        # print(f'greater than : self.value: {self.value}, self.register: {self.register}, r: {r}, \n\tthis_r: {this_r}, \n\tnext_r: {next_r}')

        return this_r, next_r



def parse_operation(line: str, operations: dict) -> dict:

    # print(f'parse_operation({line}, {operations})')
    # print(f'line.split(): {line.split("{")}')
    label, opcodes = line.split('{')
    # print(f'label: {label}')
    operations[label] = []

    # print(f'opcodes: {opcodes}')
    opcodes = opcodes.split('}')[0]
    # print(f'opcodes: {opcodes}')
    for opcode in opcodes.split(','):
        m = re.match('(\w+)<(\d+):(\w+)', opcode)
        if m:
            # print(m)
            operations[label].append(LessThanOperation(m[3], m[1], int(m[2])))
        else:
            m = re.match('(\w+)>(\d+):(\w+)', opcode)
            if m:
                operations[label].append(GreaterThanOperation(m[3], m[1], int(m[2])))
            else:
                operations[label].append(Operation(opcode))
    return operations


def parse_part(line: str, parts: list) -> list:
    print(f'parse_part({line}, {parts})')
    m = re.findall('{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}', line)
    print(m[0])
    parts.append(Part(int(m[0][0]), int(m[0][1]), int(m[0][2]), int(m[0][3])))
    return parts


def parse_line(line, operations, parts) -> (dict, list):
    if len(line) == 0:
        return operations, parts

    if line[0] == '{':
        return operations, parse_part(line, parts)
    return parse_operation(line, operations), parts

def run_part(part: Part, operations: dict) -> bool:
    opcode = 'in'
    # print(f'run_part({part}')
    while True:
        for operation in operations[opcode]:
            # print(f'\t{operation}')
            r = operation(part)
            if r == None:
                continue
            if r == 'A':
                return True
            if r == 'R':
                return False
            opcode = r
            break

def optimize_ar(operations: dict, ar: str) -> (bool, dict):
    for key, operation in operations.items():
        # print(f'optimize_ar({key}, {operation}, {ar})')
        if all([o.destination == ar for o in operation]):
            # print(f'All operations for {key} are {ar}')
            for op in operations.values():
                for o in op:
                    if o.destination == key:
                        o.destination = ar
            del operations[key]
            return True, operations
    return False, operations

def check_reachable(operations: dict, start: str) -> dict:
    reachable = set(['R', 'A'])
    to_check = [start]

    while len(to_check) > 0:
        opcode = to_check.pop(-1)
        reachable.add(opcode)
        for operation in operations[opcode]:
            if operation.destination not in reachable:
                to_check.append(operation.destination)
    
    for opcode in operations.keys():
        if opcode not in reachable:
            print(f'Unreachable opcode: {opcode}')
            del operations[opcode]

    return operations

def get_leaf_nodes(operations: dict) -> set:
    leaf_nodes = set()
    for key, operation in operations.items():
        if all([((o.destination == 'A') or (o.destination == 'R')) for o in operation]):
            print(f'Leaf node: {key}')
            leaf_nodes.add(key)
    return leaf_nodes

def prop_range(operations: dict, start: str) -> Range:
    val_range = Range()
    to_check = [(start, val_range)]
    accepted_ranges = []
    rejected_ranges = []

    while len(to_check) > 0:
        op, r = to_check.pop(-1)
        # print(f'op: {op}, r: {r}')
        for operation in operations[op]:
            r, next_r = operation.update_range(r)
            if not r.valid():
                print(f'Invalid range: {r}')
            elif operation.destination == 'A':
                accepted_ranges.append(deepcopy(r))
            elif operation.destination == 'R': 
                rejected_ranges.append(deepcopy(r))
            else:
                to_check.append((operation.destination, deepcopy(r)))
            r = next_r
            

        # print(f'accepted_ranges: {accepted_ranges}')
        # print(f'rejected_ranges: {rejected_ranges}')
        # print(f'to_check: {to_check}')

    for a in accepted_ranges:
        print(f'a.value(): {a.value()} : {a}')

    for r in rejected_ranges:
        print(f'r.value(): {r.value()} : {r}')

    print(sum([a.value() for a in accepted_ranges]))
    print(sum([r.value() for r in rejected_ranges]))

    return val_range

def main():
    operations = {}
    parts = []
    for line in fileinput.input():
        operations, parts = parse_line(line.strip(), operations, parts)
    print(operations)
    print(parts)
    p1_sum = 0
    for p in parts:
        if run_part(p, operations):
            p1_sum += p.value()
    print(p1_sum)

    changed: bool = True
    while changed:
        changed, operations = optimize_ar(operations, 'A')
        if not changed:
            changed, operations = optimize_ar(operations, 'R')


    p1_sum = 0
    for p in parts:
        if run_part(p, operations):
            p1_sum += p.value()
    print(p1_sum)

    #operations = check_reachable(operations, 'in')
    leaf_nodes = get_leaf_nodes(operations)

    prop_range(operations, 'in')


if __name__ == '__main__':
    main()