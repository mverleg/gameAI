# -*- coding: utf-8 -*-

'''
    Card object
'''
from json import load, dumps

HEART = u'heart'
SPADE = u'spade'
DIAMOND = u'diamond'
CLUB = u'club'
colours = (HEART, SPADE, DIAMOND, CLUB)

class Card():
    
    _colour = None
    _value = None
    
    names = { 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '9', 9: '9', 10: '10', 11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace', }
    abbrev = { 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '9', 9: '9', 10: 'T', 11: 'J', 12: 'Q', 13: 'K', 14: 'A', }
    symbols = { HEART: u'♥', DIAMOND: u'♦', SPADE: u'♠', CLUB: u'♣', }
    symbols = { HEART: u'♥ ', DIAMOND: u'♦ ', SPADE: u'♠ ', CLUB: u'♣ ', }
    
    def __init__(self, colour, value):
        self._colour = colour
        self._value = value
    
    def dict(self):
        return { 
            'colour': self.colour, 
            'value': self.value,
        }
    
    @property
    def colour(self):
        return self._colour
    
    @property
    def value(self):
        return self._value
    
    @property
    def points(self):
        if self.is_hearts:
            return 1
        if self.is_spade_queen:
            return 13
        return 0
    
    @classmethod
    def all(cls):
        try:
            cls._all_cards
        except AttributeError:
            cls._all_cards = []
            for colour in (HEART, DIAMOND, SPADE, CLUB):
                for value in range(2, 15):
                    cls._all_cards.append(cls(colour = colour, value = value))
        return cls._all_cards
    
    @classmethod
    def display_name(cls, colour, value):
        return '%ss %s' % (colour.title(), cls.names[value])
    
    @classmethod
    def display_symbol(cls, colour, value): 
        return '%s%s' % (cls.symbols[colour], cls.abbrev[value])
    
    def __repr__(self):
        return self.__class__.display_symbol(self.colour, self.value)
    
    @property
    def is_club_2(self):
        return self.colour == CLUB and self.value == 2
    
    @property
    def is_spade_queen(self):
        return self.colour == SPADE and self.value == 12
    
    @property
    def is_hearts(self):
        return self.colour == HEART
    
    @classmethod
    def sort(self, cards):
        def sort_key(card):
            if card.colour == HEART:
                return card.value
            if card.colour == SPADE:
                return 15 + card.value
            if card.colour == DIAMOND:
                return 30 + card.value
            if card.colour == CLUB:
                return 45 + card.value
        return sorted(cards, key = sort_key)
    
    @classmethod
    def show_summarized(cls, cards):
        from util import filter_colour
        txt = ''
        for colour in colours:
            card_values = [card.value for card in filter_colour(cards, colour)]
            if len(card_values):
                txt += u'%s%s ' % (cls.symbols[colour], ''.join(cls.abbrev[val] for val in sorted(card_values)))
        return txt
    
    @classmethod
    def json_load(cls, filename):
        with open('deals/%s' % filename) as fh:
            cards_json = load(fh)
        return [Card(**card_json) for card_json in cards_json]
    
    @classmethod
    def json_save(cls, cards, filename):
        jso = dumps([card.dict() for card in cards])
        with open('deals/%s' % filename, 'w+') as fh:
            fh.write(jso)
    


