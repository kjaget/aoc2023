#!/usr/bin/env python3

import fileinput


card_values = {'A': 14, 'K': 13, 'Q': 12, 'T': 10, 'J': 1}
def get_card_value(card):
    if card in card_values:
        return card_values[card]
    else:
        return int(card)

class Hand:
    cards = []
    
    def __init__(self, line: str):
        hand, bid = line.split()
        self.bid = int(bid)
        self.cards = [c for c in hand]

    def gen_card_dict(self, cards: list) -> dict:
        card_dict = {}
        num_jokers = 0
        for c in cards:
            if c == 'J':
                num_jokers += 1
            elif c not in card_dict:
                card_dict[c] = 1
            else:
                card_dict[c] += 1
        for k in card_dict.keys():
            card_dict[k] += num_jokers
        if (len(card_dict) == 0):
            card_dict['J'] = num_jokers
        return card_dict

    def check_high_card(self, other_hand):
        print(f'check_high_card: {self.cards}, {other_hand.cards}')
        for s, o in zip(self.cards, other_hand.cards):
            if get_card_value(s) > get_card_value(o):
                return False
            elif get_card_value(s) < get_card_value(o):
                return True
        return None

    def check_n_of_a_kind(self, card_dict: dict, other_hand, other_card_dict: dict, n: int):
        print(f'check_n_of_a_kind: {card_dict}, {other_card_dict}, {n}')
        len_card_dict = max([v for v in card_dict.values()])
        len_other_card_dict = max([v for v in other_card_dict.values()])
        if (len_card_dict == n) and (len_other_card_dict == n):
            return self.check_high_card(other_hand)
        if (len_card_dict == n) and (len_other_card_dict != n):
            print(f'return False')
            return False
        if (len_card_dict != n) and (len_other_card_dict == n):
            print(f'return True')
            return True
        print('return None')
        return None

    def check_num_keys(self, card_dict: dict, other_hand, other_card_dict: dict, n: int):
        print(f'check_num_keys: {card_dict}, {other_card_dict}, {n}')
        card_dict_values = sorted([v for v in card_dict.values()])
        other_card_dict_values = sorted([v for v in other_card_dict.values()])

        if (len(card_dict_values) == n) and (len(other_card_dict_values) == n):
            return self.check_high_card(other_hand)
        if (len(card_dict_values) == n) and (len(other_card_dict_values) != n):
            print(f'return False')
            return False
        if (len(card_dict_values) != n) and (len(other_card_dict_values) == n):
            print(f'return True')
            return True
        print('return None')
        return None

    def __lt__(self, other_hand):
        card_dict = self.gen_card_dict(self.cards)
        other_card_dict = self.gen_card_dict(other_hand.cards)

        # Five of a kind   
        rc = self.check_n_of_a_kind(card_dict, other_hand, other_card_dict, 5)
        if rc is not None:
            return rc
        rc = self.check_n_of_a_kind(card_dict, other_hand, other_card_dict, 4)
        if rc is not None:
            return rc
        # Since 4 of a kind checks for 2 sets of card with 4, 1 members,
        # this will check the remaining 2 sets case which is full house
        rc = self.check_num_keys(card_dict, other_hand, other_card_dict, 2)
        if rc is not None:
            return rc
        rc = self.check_n_of_a_kind(card_dict, other_hand, other_card_dict, 3)
        if rc is not None:
            return rc
        # Two pairs plus a 3rd single card
        rc = self.check_num_keys(card_dict, other_hand, other_card_dict, 3)
        if rc is not None:
            return rc
        # One pair plus 3 single cards
        rc = self.check_num_keys(card_dict, other_hand, other_card_dict, 4)
        if rc is not None:
            return rc
        # No special case, check high card
        return self.check_high_card(other_hand)
    
hands = []
for line in fileinput.input():
    hands.append(Hand(line))

hands.sort()    

for ranking, hand in enumerate(hands):
    print(f'{ranking + 1} {hand.bid}')

print(f'{sum([(ranking + 1) * hand.bid for ranking, hand  in enumerate(hands)])}')