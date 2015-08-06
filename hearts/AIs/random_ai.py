# -*- coding: utf-8 -*-

'''
    Picks one of the legal moves at random
'''

from base_ai import BaseAI
from random import choice, sample
from util import legal_moves
from card import Card


class Random(BaseAI):
    
    def pass_cards(self, hand, direction = 2, all_is_win = False):
        return sample(hand, 3)
    
    def play_turn(self, state, hand, all_is_win = False):
        legal = legal_moves(state, hand)
        if not len(legal):
            print 'hand: ', Card.show_summarized(hand)
            print 'table:', Card.show_summarized(state.table_cards())
            raise Exception('no legal cards to play; should not be possible!')
        return choice(legal)


