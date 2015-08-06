
'''
    Pass cards with high numbers, play cards with low numbers first unless 
    not recognizing color, play high if last player and no points
'''

from base_ai import BaseAI
from random import choice
from util import legal_moves, sort_by_value
from card import Card


class LowFirst(BaseAI):
    
    @classmethod
    def sort_by_value(cls, cards):
        return sort_by_value(cards)
    
    def pass_cards(self, hand, direction = 2, all_is_win = False):
        return self.sort_by_value(hand)[-3:]
    
    def play_turn(self, state, hand, all_is_win = False):
        legal = self.sort_by_value(legal_moves(state, hand))
        return legal[0]


