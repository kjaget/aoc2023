#!/usr/bin/env python3
import fileinput
from dataclasses import dataclass
import re
from math import lcm

@dataclass
class Node:
    left: str
    right: str

def get_path_length(start_node:str, stage1: bool, path: str, nodes:dict):
    position = start_node
    index = 0
    while True:
        position = nodes[position].left if path[index % len(path)] == 'L' else nodes[position].right
        index += 1
        if stage1 and (position == 'ZZZ'):
            return index
        if (not stage1) and (position[-1] == 'Z'):
            return index

    # This will never happen (TM)
    return None

path = ""
nodes = {}
for line in fileinput.input():
    line = line.strip()
    if not line:
        continue
    if '=' not in line:
        path = line.strip()
    else:
        m = re.compile('(\w+) = \((\w+), (\w+)\)').match(line)
        if m:
            nodes[m.group(1)] = Node(m.group(2), m.group(3))
            print(m.group(1), m.group(2), m.group(3))

#print(get_path_length('AAA', True, path, nodes))

counts = [get_path_length(k, False, path, nodes) for k in nodes.keys() if k[-1] == 'A']

print(counts)
print(lcm(*counts))