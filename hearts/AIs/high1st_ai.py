
'''
    Pass cards with high numbers but also play high first (so as not to have them at the end)
'''

from base_ai import BaseAI
from random import choice
from util import legal_moves
from card import Card
from AIs.low1st_ai import LowFirst


class HighFirst(LowFirst):
    
    def play_turn(self, state, hand, all_is_win = False):
        legal = self.sort_by_value(legal_moves(state, hand))
        return legal[-1]


