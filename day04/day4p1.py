#!/usr/bin/env python3

import fileinput
import time
import re

def process_card(line: str) -> (int, int):
    m = re.match('Card\s+(\d+):([\d\s]+)\|([\d\s]+)', line)
    if not m:
        print(f'Invalid line: {line}')
        return

    winnings_numbers = [int(x) for x in m.group(2).split()]
    played_numbers = [int(x) for x in m.group(3).split()]

    count = 0
    for played_number in played_numbers:
        if played_number in winnings_numbers:
            count += 1

    return int(m.group(1)), count

# Part 1
total_points = 0
winnings_points = {} # game number -> points, used for looking up the points for a given game number in part 2
for line in fileinput.input():
    game_number, points = process_card(line.strip())
    winnings_points[game_number] = points
    if points > 0:
        total_points += 2**(points - 1)

print(f'total points: {total_points}')

# Part 2
p2_start = time.perf_counter()
card_count = 0

# Start with the initial list of card game numbers
cards = list(winnings_points.keys())

# For each card in the list, find the number of subsequent
# cards that are won by this card, and add them to the list
while len(cards) > 0:
    card = cards.pop(-1) # popping the last element is O(1), vs popping the first element which is O(n)
    card_count += 1
    cards += [x for x in range(card + 1, card + winnings_points[card] + 1)]

print(f'card count: {card_count}')
p2_end = time.perf_counter()
print(f'part 2 time: {p2_end - p2_start}')

def get_points_for_card(card: int, winnings_points: dict, winnings_points_per_card: list) -> int:
    cards = [x for x in range(card + 1, card + winnings_points[card] + 1)] 
    #print(f'cards for {card}: {cards}')
    #print(f'winnings points per card: {winnings_points_per_card}')
    points = sum([winnings_points_per_card[x] for x in cards]) + 1
    #print(f'points for {card}: {points}')
    return points

# Similar to part 2, but work in reverse order, and cache the points for each card
# Use those saved values rather than recalculating them each time a card is seen
p2a_start = time.perf_counter()
winnings_points_per_card = [0] * (len(winnings_points) + 1)
for card in reversed(list(winnings_points.keys())):
    winnings_points_per_card[card] = get_points_for_card(card, winnings_points, winnings_points_per_card)

print(f'winning points per card: {winnings_points_per_card}')
print(f'sum = {sum(winnings_points_per_card)}')
p2a_end = time.perf_counter()
print(f'part 2a time: {p2a_end - p2a_start}')