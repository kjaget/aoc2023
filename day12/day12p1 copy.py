#!/usr/bin/env python3

from dataclasses import dataclass
from copy import deepcopy
import fileinput
import re

def get_question_mark_groups(arrangement: str) -> list:
    in_question_mark = False
    start_idx = -1
    ret = []
    for idx, c in enumerate(arrangement):
        if (not in_question_mark) and (c == '?'):
            start_idx = idx
            in_question_mark = True
        elif (c != '?') and in_question_mark:
            in_question_mark = False
            ret.append(range(start_idx, idx))

    return ret

def check_range(arrangement: str, r: range, counts: list, saved_matches: dict = {}) -> (int, dict):
    for idx in r:
        print(f'arrangement: {arrangement}, idx: {idx}, arrangement[idx]: {arrangement[idx]}')

    

DEBUG = 1
# Some check with remaining ?s and counts to bail early
def check_arrangement(arrangement: str, counts: list, saved_matches: dict = {}) -> (int, dict):
    this_counts = []
    counts_idx = 0
    in_pound = False
    question_mark_seen = False
    if DEBUG:
        print(f'checking {arrangement}, counts: {counts}')
    num_non_dot = sum([1 for c in arrangement if c != '.']) 
    non_dots_needed = sum(counts)
    if DEBUG:
        print(f'arrangement: {arrangement} at end, counts: {counts}, this_counts: {this_counts}, counts: {counts}, num_non_dot: {num_non_dot}, non_dots_needed: {non_dots_needed}') 
    if num_non_dot < non_dots_needed:
        if DEBUG:
            print(f'failed due to not enough chars : arrangement: {arrangement}, counts: {counts}, this_counts: {this_counts}, counts: {counts}, num_non_dot: {num_non_dot}, non_dots_needed: {non_dots_needed}') 
        return 0, saved_matches
    for c in arrangement:
        # Transitioning from non-# to #, start a new this_count entry
        # to count the number of #s in this current group
        if (not in_pound) and (c == '#'):
            in_pound = True
            this_counts.append(1)
            # Can't have more # groups than the list of counts for them
            if len(this_counts) > len(counts):
                if DEBUG:
                    print(f'failed at {c}, too many # groups')
                if not question_mark_seen:
                    return 0, saved_matches
                break
        elif (in_pound) and (c == '#'):
            # Still in the same # group as before, increment the count
            this_counts[-1] += 1
        elif (in_pound) and (c != '#'):
            # Leaving a # group
            if (c != '#'):
                in_pound = False
            if this_counts[-1] > counts[counts_idx]:
                if DEBUG:
                    print(f'failed at {c}, {this_counts[-1]} > {counts[counts_idx]} : counts: {counts}, this_counts: {this_counts}')
                if not question_mark_seen:
                    return 0, saved_matches
                break
            if (not question_mark_seen) and (c == '.') and (this_counts[-1] != counts[counts_idx]):
                if DEBUG:
                    print(f'failed at {c}, {this_counts[-1]} != {counts[counts_idx]} : counts: {counts}, this_counts: {this_counts}')
                return 0, saved_matches
            counts_idx += 1
        if c == '?':
            question_mark_seen = True

    '''
    if (len(this_counts) > 0) and (this_counts[-1] > counts[counts_idx]):
        print(f'failed at end, {this_counts[-1]} > {counts[counts_idx]} : counts: {counts}, this_counts: {this_counts}')
        return 0, saved_matches
    '''
    if '?' not in arrangement:
        if counts == this_counts:
            if DEBUG:
                print(f'found a match: {arrangement}, counts: {counts}, this_counts: {this_counts}')
            return 1, saved_matches
        if DEBUG:
            print(f'failed at end, {this_counts[-1]} != {counts[counts_idx]} : counts: {counts}, this_counts: {this_counts}')
        return 0, saved_matches

    if len(this_counts) > 0:
        if this_counts[-1] == 1:
            this_counts.pop(-1)
        else:
            this_counts[-1] -= 1
    for idx, c in enumerate(arrangement):
        if c != '?':
            if DEBUG:
                print(f'c != ?, arrangement: {arrangement}, idx: {idx}, a: {arrangement[idx+1:]}, this_counts: {this_counts}')
            if (arrangement[idx+1:], tuple(this_counts)) in saved_matches:
                if DEBUG:
                    print(f'Hit saved match: {arrangement[idx+1:]}, {this_counts}, {saved_matches[(arrangement[idx+1:], tuple(this_counts))]}')
                saved_matches[(arrangement[idx:], tuple(this_counts))] = saved_matches[(arrangement[idx+1:], tuple(this_counts))]
                #return saved_matches[(arrangement[idx+1:], tuple(this_counts))], saved_matches
        elif c == '?':
            if DEBUG:
                print(f'arrangement: {arrangement}, idx: {idx}, a: {arrangement[idx+1:]}, this_counts: {this_counts}')
            c1, saved_matches = check_arrangement(arrangement.replace('?', '.', 1), counts, saved_matches=saved_matches)

            if c1 > 0:
                if DEBUG:
                    print(f'Saving c1: {c1}, a: {arrangement.replace("?", ".", 1)[idx:]}, this_counts: {this_counts}')
                saved_matches[(arrangement.replace('?', '.', 1)[idx:], tuple(this_counts))] = c1
            c2, saved_matches = check_arrangement(arrangement.replace('?', '#', 1), counts, saved_matches=saved_matches)
            if  c2 > 0:
                if DEBUG:
                    print(f'Saving c2: {c2}, a: {arrangement.replace("?", "#", 1)[idx:]}, this_counts: {this_counts}')
                saved_matches[(arrangement.replace('?', '#', 1)[idx:], tuple(this_counts))] = c1
            return c1 + c2, saved_matches

class State:
    arrangement: str
    counts: list
    counts_idx: int = 0
    arrangement_idx: int = 0
    this_counts: list
    in_pound: bool = False

    def __init__(self, arrangement: str, counts: list):
        self.arrangement = deepcopy(arrangement)
        self.counts = counts
        self.this_counts = []

    def __str__(self):
        print(self.arrangement_idx)
        return f'arrangement: {self.arrangement[:self.arrangement_idx]}[{self.arrangement[self.arrangement_idx]}]{self.arrangement[self.arrangement_idx+1:]}, counts: {self.counts}, this_counts: {self.this_counts}, counts_idx: {self.counts_idx}, arrangement_idx: {self.arrangement_idx}, in_pound: {self.in_pound}'

    def key(self):
        return (self.arrangement[self.arrangement_idx+1:], tuple(self.this_counts))


def check_arrangement2(state: State, saved_matches: dict = {}) -> (int, State, dict):
    if DEBUG:
        print(f'checking {state}')
    num_non_dot = sum([1 for c in state.arrangement if c != '.']) 
    non_dots_needed = sum(state.counts)
    if DEBUG:
        print(f'num_non_dot: {num_non_dot}, non_dots_needed: {non_dots_needed}') 
    if num_non_dot < non_dots_needed:
        if DEBUG:
            print(f'failed due to not enough chars') 
        saved_matches[state.key()] = 0
        return 0, state, saved_matches
    while (state.arrangement_idx < len(state.arrangement)) and (state.arrangement[state.arrangement_idx] != '?'):
        c = state.arrangement[state.arrangement_idx]
        print(f'checking {c} from state: {state}')
        # Transitioning from non-# to #, start a new this_count entry
        # to count the number of #s in this current group
        if (not state.in_pound) and (c == '#'):
            state.in_pound = True
            # Can't have more # groups than the list of state.counts for them
            if len(state.this_counts) == len(state.counts):
                if DEBUG:
                    print(f'failed at {c}, too many # groups')
                saved_matches[state.key()] = 0
                return 0, state, saved_matches

            # Otherwise, add a new group to the count
            state.this_counts.append(1)
        elif (state.in_pound) and (c == '#'):
            # Still in the same # group as before, increment the count
            state.this_counts[-1] += 1
        elif (state.in_pound) and (c != '#'):
            # Leaving a # group
            if (c != '#'):
                state.in_pound = False
            if state.this_counts[-1] > state.counts[state.counts_idx]:
                if DEBUG:
                    print(f'failed at {c}, {state.this_counts[-1]} > {state.counts[state.counts_idx]} : state.counts: {state.counts}, state.this_counts: {state.this_counts}')
                saved_matches[state.key()] = 0
                return 0, state, saved_matches
            if (c == '.') and (state.this_counts[-1] != state.counts[state.counts_idx]):
                if DEBUG:
                    print(f'failed at {c}, {state.this_counts[-1]} != {state.counts[state.counts_idx]} : state.counts: {state.counts}, state.this_counts: {state.this_counts}')
                saved_matches[state.key()] = 0
                return 0, state, saved_matches
            state.counts_idx += 1

        state.arrangement_idx += 1

    # End of arragement, check if we have a match
    if state.arrangement_idx == len(state.arrangement):
        if state.counts == state.this_counts:
            if DEBUG:
                print(f'found a match: {state.arrangement}, state.counts: {state.counts}, state.this_counts: {state.this_counts}')
            return 1, state, saved_matches
        if DEBUG:
            print(f'failed at end, {state.this_counts[-1]} != {state.counts[state.counts_idx]} : state.counts: {state.counts}, state.this_counts: {state.this_counts}')
        return 0, state, saved_matches

    # Should be sitting on a ? character.  Replace it with a . and a # and recurse
    s = state.arrangement
    state.arrangement = s[:state.arrangement_idx] + '.' + s[state.arrangement_idx+1:]
    c1, new_state, saved_matches = check_arrangement2(deepcopy(state), saved_matches=saved_matches)
    if c1 > 0:
        if DEBUG:
            print(f'Saving c1: {c1}, {new_state.key()}\n\tstate: {state}\n\tnew_state: {new_state}')
        saved_matches[new_state.key()] = c1

    state.arrangement = s[:state.arrangement_idx] + '#' + s[state.arrangement_idx+1:]
    c2, new_state, saved_matches = check_arrangement2(deepcopy(state), saved_matches=saved_matches)
    if c2 > 0:
        if (len(state.this_counts) > 0) and state.in_pound:
            state.this_counts[-1] += 1
        else:
            state.this_counts.append(1)

        if DEBUG:
            print(f'Saving c2: {c2}, {state.key()}\n\tstate: {state}\n\tnew_state: {new_state}')
        saved_matches[state.key()] = c2
    return c1 + c2, state, saved_matches



def calc_possible_arrangements(line: str, dupes: int) -> int:

    m = re.match('([\?\.#]+)\s+([\d,]+)', line)
    if m:
        condition = m.group(1) 
        if dupes > 1:
            condition += '?'
            condition *= dupes
        counts = [int(d) for d in m.group(2).split(',')] * dupes

        print(condition, counts)

        '''
        ranges = get_question_mark_groups(line.strip())
        for r in ranges:
            check_range(line.strip(), r, counts)
        return 0, 0
        '''
        
        #arrangements = check_arrangement(condition, counts)
        arrangements = check_arrangement2(State(condition, counts))
        print(f'Total for {condition} is {arrangements[0]}')
        return arrangements
    return -1



p1_sum = 0
p2_sum = 0
for line in fileinput.input():
    
    p1_sum += calc_possible_arrangements(line.strip(), 1)[0]
    # p2_sum += calc_possible_arrangements(line.strip(), 5)[0]
print(f'Part 1: {p1_sum}')
print(f'Part 2: {p2_sum}')

