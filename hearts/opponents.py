
from card import Card


class Opponent(object):
    
    def __init__(self, player_nr, state, hand):
        self.last_update_round = 0
        self.number = player_nr
        self.state = state
        self.cards = {sym: {name: None for name in Card.names.keys()} for sym in Card.symbols.keys()}
        self.player_hand = hand
        self.opponents = None
        self.filter_state()
        self.filter_hand()
    
    def add_opponents(self, opponents):
        self.opponents = [opponent for opponent in opponents if not opponent.number == self.number]
    
    def hand_count(self):
        return 13 - len(self.state.cards_played_by(self.number))
    
    ''' cards of a colour that this player might have '''
    def could_play(self, colour):
        return [value for value, state in self.cards[colour].items() if not state == False]
    
    ''' maximum number of cards of this colour the player might have '''
    def could_play_count(self, colour):
        colour_states = [state for value, state in self.cards[colour].items()]
        return min(self.hand_count() - self.certain_card_count() + sum(int(state == True) for state in colour_states), len(self.could_play(colour)))
    
    ''' list of cards this player certainly has (often empty) '''
    def certain_card_count(self):
        return sum(sum(int(state == True) for value, state in row.items()) for sym, row in self.cards.items())
    
    def filter(self):
        self.filter_state()
        self.filter_other_opponents()
        self.filter_other()
    
    def filter_state(self):
        ''' remove cards already played '''
        for round in range(self.last_update_round, self.state.round + 1):
            for card in self.state.round_cards(round):
                self.cards[card.colour][card.value] = False
        ''' remove colours not recognized '''
        colours = self.state.colours_not_recognized_by(self.number)
        for colour in colours:
            self.cards[colour] = {name: False for name in Card.names.keys()}
        ''' keep track of what was updated '''
        self.last_update_round = self.state.round
    
    def filter_other_opponents(self):
        assert self.opponents is not None
        for sym in Card.symbols.keys():
            for name in Card.names.keys():
                if any(opponent.cards[sym][name] == True for opponent in self.opponents):
                    self.cards[sym][name] = False
                if self.cards[sym][name] == None:
                    if all(opponent.cards[sym][name] == False for opponent in self.opponents):
                        ''' this is the only player that could have this card '''
                        self.cards[sym][name] = True
    
    def possible_colour_cards(self, colour):
        return [value for value, state in self.cards[colour].items() if not state == False]
    
    def filter_hand(self):
        ''' remove cards that you have '''
        for card in self.player_hand:
            self.cards[card.colour][card.value] = False
    
    def filter_other(self):
        possible_count = sum(sum(int(not val == False) for val in row.values()) for row in self.cards.values())
        if possible_count == self.hand_count():
            ''' set every doubtful value to True '''
            for sym in Card.symbols.keys():
                for name in Card.names.keys():
                    if self.cards[sym][name] == None:
                        self.cards[sym][name] = True
        certain_count = sum(sum(int(val == True) for val in row.values()) for row in self.cards.values())
        if certain_count == self.hand_count():
            ''' set every doubtful value to False '''
            for sym in Card.symbols.keys():
                for name in Card.names.keys():
                    if self.cards[sym][name] == None:
                        self.cards[sym][name] = False
    
    def show_opponent_state(self):
        print 'opponent %d (%d cards)' % (self.number, self.hand_count())
        disp_conv = {False: '-', True: '+', None: ' '}
        print '   %s' % ' '.join(Card.abbrev.values())
        for sym, row in self.cards.items():
            print '%-2s %s  %2d' % (Card.symbols[sym], ' '.join(disp_conv[item] for item in row.values()), self.could_play_count(sym))


