#!/usr/bin/env python3

import numpy as np
from sys import argv
from math import floor, ceil


with open(argv[1], 'r') as f:
    lines = f.read().splitlines()
times = lines[0].split(':')[1].split()
distances = lines[1].split(':')[1].split()

margin = 1
for t, d in zip(times, distances):
    #print(t, d)
    bottom, top = sorted(np.roots([-1, float(t), -float(d)-.001]))
    margin *= floor(top) - ceil(bottom) + 1
    print(ceil(bottom), floor(top), floor(top) - ceil(bottom) + 1)
print(margin)

p2_time =''.join(times) 
p2_distance = ''.join(distances)
bottom, top = sorted(np.roots([-1, float(p2_time), -float(p2_distance)-.001]))
print(floor(top) - ceil(bottom) + 1)

