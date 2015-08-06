# -*- coding: utf-8 -*-

'''
    Extend this AI to create your own
'''
from card import HEART, SPADE, DIAMOND, CLUB, Card


class BaseAI(object):
    
    def __init__(self, player_nr, *args, **kwargs):
        self.number = player_nr
    
    '''
        Pass cards to the player that is 'direction' places to the left (that
        is, the direction of the player who plays after you do)
    '''
    def pass_cards(self, hand, direction = 2, all_is_win = False):
        raise NotImplementedError('overwrite this method in child class')
    
    '''
        This is called when it's your turn. It should return the card played
        The all_is_win argument indicates if getting every point is a good thing
    '''
    def play_turn(self, state, hand, all_is_win = True):
        raise NotImplementedError('overwrite this method in child class')
    
    def __repr__(self):
        return self.__class__.__name__
    
    def show_cards(self, cards, label = ''):
        print u'%s%s' % ((label + ': ' if label else ''), u' '.join(unicode(card) for card in Card.sort(cards)))
    
    def show_short(self, cards, label = ''):
        print (label + ': ' if label else '') + Card.show_summarized(cards)


    