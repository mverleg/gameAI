# -*- coding: utf-8 -*-

'''
    Asks for console input (so not really an AI)
'''

from base_ai import BaseAI
from util import legal_moves
from card import Card


class Human(BaseAI):
    
    def pass_cards(self, hand, direction = 2, all_is_win = False):
        print 'Please select three cards to pass to the the player %d places left of you' % direction
        pass_cards = []
        for k in range(3):
            card = self.input_choose_card(hand, 'hand')
            pass_cards.append(card)
            hand.remove(card)
        print 'you are passing %s' % ' '.join(str(card) for card in pass_cards)
        return pass_cards
    
    def play_turn(self, state, hand, all_is_win = False):
        legal = legal_moves(state, hand)
        print 'it is your turn to play a card'
        self.show_cards(state.table_cards(), 'table')
        self.show_short(hand, 'hand')
        if len(legal) > 1:
            card = self.input_choose_card(legal, 'possible')
        else:
            card = legal[0]
            print 'your only possible move %s was selected automatically' % card
        print 'you are playing %s' % card
        return card
    
    def input_choose_card(self, cards, label = ''):
        txt = label + ': ' if label else ''
        cards = Card.sort(cards)
        for k, card in enumerate(cards):
            txt += u'%d:%s ' % (k + 1, unicode(card))
        choice = -1
        while choice < 1 or choice > len(cards):
            try:
                print txt
                choice = int(raw_input('[enter the number to choose] '))
                if choice < 1:
                    print 'lowest possibility is 1'
                if choice > len(cards):
                    print 'highest possibility is %d' % len(cards)
            except ValueError:
                print 'this is not a number'
                choice = -1
        return cards[choice - 1]


