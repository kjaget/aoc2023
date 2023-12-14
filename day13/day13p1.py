#!/usr/bin/env python3

import fileinput

DEBUG=0

def check_row(map: list, check_index: int) -> bool:
    for offset in range(len(map) - 1):
        i1 = check_index + offset + 1
        i2 = check_index - offset
        # print(f'Checking row {check_index} offset {offset} : i1 = {i1} and i2 = {i2}')
        # Walking off the map in either direction without a miscompare
        # means the check index is a mirror axis
        if (i1 >= len(map)) or (i2 < 0):
            return True
        # print(f'\tmap[{i1}] = {map[i1]}\n\tmap[{i2}] = {map[i2]}')
        # Bail out on first miscompare
        if map[i1] != map[i2]:
            return False
    return True

# Check all the rows in the map for a mirror axis
# Return a list of the indices of the mirror axes
# For part 1, this should only ever be 0 or 1
# For part 2, this could be 0, 1, or 2, since adding a
# smudge could create a second mirror axis while leaving 
# the first one intact
def check_map(map:list) -> list:
    results = []
    for index in range(len(map) - 1):
        if check_row(map, index):
            if DEBUG:
                print(f"Found mirror at index: {index + 1}")
            results.append(index + 1)
    return results

# Call check_map twice, once for the rows and once for the columns
# Return the axis not id'd by ignore
def mirror(map: list, ignore:int=-1) -> int:
    if DEBUG:
        for l in map:
            print(l)
        print(f'Checking map, ignore = {ignore}')
    # Get the list of valid reflections for the rows. The score is 
    # multipled by 100 for each.  Keep any (hopefully only 0 or 1)
    # that aren't in the list of scores to ignore. This ignore value
    # is used by part 2 to ignore the unsmudged map reflections
    result = [c * 100 for c in check_map(map) if (c * 100) != ignore]
    if len(result) == 0:
        if DEBUG:
            print('Checking map transpose')
        # Same for here, but transpose the map first to check the columns
        # Since cols count for 1 point, the 100x multiplier is not needed
        result = [c for c in check_map([[x[k] for x in map] for k in range(len(map[0]))]) if c != ignore]

    if len(result) == 0:
        return 0
    if len(result) > 1: # This Will Never Happen(tm)
        print(f'Error: Multiple mirrors found: {result}')
        return -1
    return result[0]

# Iteratively smudge (flip . -> # and vice versa) a givem map
# until a result other than the unsmuged reflection axis is found
def smudge_map(map: list) -> int:
    unsmudged_result = mirror(map)
    for y in range(len(map)):
        for x in range(len(map[y])):
            if DEBUG:
                print(f'Checking {x}, {y}')
            map[y][x] = '.' if map[y][x] == '#' else '#'
            result = mirror(map, unsmudged_result)
            if result != 0:
                return result
            map[y][x] = '.' if map[y][x] == '#' else '#'
    return 0

# Smudge a map in both directions (rows and columns)
# until a result other than the unsmuged reflection axis is found
def smudge(map: list) -> int:
    if DEBUG:
        for l in map:
            print(l)
    result = smudge_map(map)
    if result == 0:
        result = smudge_map([[x[k] for x in map] for k in range(len(map[0]))])
    return result

def main():
    maps = [[]]
    for line in fileinput.input():
        if line.strip() == '':
            maps.append([])
        else:
            maps[-1].append([c for c in line.strip()])

    if len(maps[-1]) == 0:
        maps.pop(-1)

    print(sum([mirror(m) for m in maps]))
    print(sum([smudge(m) for m in maps]))

if __name__ == '__main__':
    main()