#!/usr/bin/env python3

from dataclasses import dataclass
from copy import deepcopy
import fileinput
import re

DEBUG = 0
class State:
    def __init__(self, arrangement: str):
        self.arrangement = deepcopy(arrangement)
        self.arrangement_idx = 0
        self.counts_idx = 0
        self.this_counts = []
        self.in_pound = False

    def __str__(self):
        s = f'{self.arrangement[:self.arrangement_idx]}[{self.arrangement[self.arrangement_idx]}]{self.arrangement[self.arrangement_idx+1:]}' if self.arrangement_idx < len(self.arrangement) else self.arrangement
        return f'arrangement: {s}, this_counts: {self.this_counts}, counts_idx: {self.counts_idx}, arrangement_idx: {self.arrangement_idx}, in_pound: {self.in_pound}'

    def key(self):
        return (self.arrangement[self.arrangement_idx-1:], tuple(self.this_counts))


# This could probably be optimized by not having to do a deepcopy of the state
def check_arrangement(state: State, counts: list, saved_matches: dict = {}) -> (int, State, dict):
    if DEBUG:
        print(f'checking {state}')

    # Make sure there enough remaining characters to satisfy the remaining counts
    # This is conservative, might be able to make it better?
    num_non_dot = sum([1 for c in state.arrangement if c != '.']) 
    non_dots_needed = sum(counts)
    if DEBUG:
        print(f'num_non_dot: {num_non_dot}, non_dots_needed: {non_dots_needed}') 
    if num_non_dot < non_dots_needed:
        if DEBUG:
            print(f'failed due to not enough chars') 
        saved_matches[state.key()] = 0
        return 0, state, saved_matches

    while (state.arrangement_idx < len(state.arrangement)) and (state.arrangement[state.arrangement_idx] != '?'):
        c = state.arrangement[state.arrangement_idx]
        if DEBUG:
            print(f'checking {c} from state: {state}')
        # Transitioning from non-# to #, start a new this_count entry
        # to count the number of #s in this current group
        if (not state.in_pound) and (c == '#'):
            # Can't have more # groups than the list of counts for them
            if len(state.this_counts) == len(counts):
                if DEBUG:
                    print(f'failed at {c}, too many # groups')
                saved_matches[state.key()] = 0
                return 0, state, saved_matches

            # Otherwise, add a new group to the count
            state.in_pound = True
            state.this_counts.append(1)
        elif (state.in_pound) and (c == '#'):
            # Still in the same # group as before, increment the count
            state.this_counts[-1] += 1
            # Make sure the current group doesn't exceed the requested count
            if state.this_counts[-1] > counts[state.counts_idx]:
                if DEBUG:
                    print(f'failed at {c}, {state.this_counts[-1]} > {counts[state.counts_idx]} : counts: {counts}, state.this_counts: {state.this_counts}')
                saved_matches[state.key()] = 0
                return 0, state, saved_matches
        elif (state.in_pound) and (c != '#'):
            # Leaving a # group
            # Make sure there are the correct number of #s in the group
            if state.this_counts[-1] != counts[state.counts_idx]:
                if DEBUG:
                    print(f'failed at {c}, {state.this_counts[-1]} != {counts[state.counts_idx]} : counts: {counts}, state.this_counts: {state.this_counts}')
                saved_matches[state.key()] = 0
                return 0, state, saved_matches
            state.in_pound = False
            state.counts_idx += 1
        
        state.arrangement_idx += 1
        # If we've hit this state before, we can just return the saved value
        if DEBUG:
            print(f'after {c}, key: {state.key()}, state: {state}')
        if state.key() in saved_matches:
            if DEBUG:
                print(f'Hit saved match: {state.key()}, {saved_matches[state.key()]}')
            return saved_matches[state.key()], state, saved_matches

    # If we've reached the end of the arrangement, make sure we've also reached the end of the counts
    if state.arrangement_idx == len(state.arrangement):
        if counts[-1] == state.this_counts[-1]:
            if DEBUG:
                print(f'found a match: {state.arrangement}, counts: {counts}, state.this_counts: {state.this_counts}')
            return 1, state, saved_matches
        if DEBUG:
            print(f'failed at end, {state.this_counts[-1]} != {counts[state.counts_idx]} : counts: {counts}, state.this_counts: {state.this_counts}')
        return 0, state, saved_matches

    # Should be sitting on a ? character.  Replace it with a . and a # and recurse
    s = state.arrangement
    state.arrangement = s[:state.arrangement_idx] + '.' + s[state.arrangement_idx+1:]
    c1, new_state1, saved_matches = check_arrangement(deepcopy(state), counts, saved_matches=saved_matches)
    # state.arrangement = s[:state.arrangement_idx] + '?' + s[state.arrangement_idx+1:]
    if DEBUG:
        print(f'c1: {c1}, state: {state}, new_state1: {new_state1}')
    if (state.arrangement_idx < len(state.arrangement)) and (new_state1.key() not in saved_matches):
        if DEBUG:
            print(f'Saving c1: {c1}, {new_state1.key()}\n\tstate: {state}\n\tnew_state1: {new_state1}')
        saved_matches[new_state1.key()] = c1

    state.arrangement = s[:state.arrangement_idx] + '#' + s[state.arrangement_idx+1:]
    c2, new_state2, saved_matches = check_arrangement(deepcopy(state), counts, saved_matches=saved_matches)
    state.arrangement = s[:state.arrangement_idx] + '?' + s[state.arrangement_idx+1:]

    if DEBUG:
        print(f'c2: {c2}, state: {state}, new_state: {new_state2}, key: {state.key()}')
    if state.arrangement_idx < (len(state.arrangement)):
        if state.key() not in saved_matches:
            if DEBUG:
                print(f'Saving c2: {c2}, {state.key()}\n\tstate: {state}\n\tnew_state: {new_state2}')
            saved_matches[state.key()] = c1 + c2
    if DEBUG:
        print(f'returning, c1:{c1}, c2:{c2}, state: {state}')
    return c1 + c2, state, saved_matches

def calc_possible_arrangements(line: str, dupes: int) -> int:

    m = re.match('([\?\.#]+)\s+([\d,]+)', line)
    if m:
        condition = m.group(1) 
        if dupes > 1:
            condition += ('?'+condition) * (dupes - 1)
        counts = [int(d) for d in m.group(2).split(',')] * dupes

        #print(condition, counts)

        arrangements, _, _ = check_arrangement(State(condition), counts, {})
        #print(f'Total for {condition} {counts} is {arrangements[0]}')
        return arrangements
    return -1


p1_sum = 0
p2_sum = 0
for line in fileinput.input():
    p1_sum += calc_possible_arrangements(line.strip(), 1)
    p2_sum += calc_possible_arrangements(line.strip(), 5)
print(f'Part 1: {p1_sum}')
print(f'Part 2: {p2_sum}')

