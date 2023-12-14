#!/usr/bin/env python3
import fileinput
from itertools import pairwise

p1_total = 0
p2_total = 0
for line in fileinput.input():
    seq = [[int(d) for d in line.strip().split()]]
    while any([d != 0 for d in seq[-1]]):
        seq.append([y - x for x, y in pairwise(seq[-1])])
        #seq.append([seq[-1][i + 1] - seq[-1][i] for i in range(len(seq[-1]) - 1)])
    p1 = 0
    p2 = 0
    for i in reversed(range(len(seq) - 1)):
        p1 += seq[i][-1]
        p2 = seq[i][0] - p2
    p1_total += p1
    p2_total += p2
    
print(p1_total)
print(p2_total)