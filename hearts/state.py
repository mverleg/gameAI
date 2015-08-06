
'''
    Current state of the game.
    You may only use the methods, not access the properties directly.
'''

from card import HEART, Card
from util import filter_colour


class State():
    
    def __init__(self):
        self._round = 0
        self._current_player = None
        self._cards_played = [4 * [None] for li in range(13)]
        self._opening_player = [None for li in range(13)]
    #todo: test
    #def turn_cards(self):
    #    return [self._cards_played[(player + self._opening_player[self._round]) % 4] for player in range(4) if self._cards_played[(player + self._opening_player[self._round]) % 4]]
    
    ''' Cards on the table this round '''
    def table_cards(self):
        return self.round_cards(self.round)
    
    ''' Player that opened this round '''
    def table_opening_player(self):
        return self.round_opening_player(self.round)
    
    ''' Players that still have to play '''
    def pending_players(self):
        return [(self.table_opening_player() + k) % 4 for k in range(4) if self._cards_played[self.round][(self.table_opening_player() + k) % 4] is None]
    
    ''' Cards played this round (in the order they were played '''
    def round_cards(self, round):  # @ReservedAssignment
        offset = self.table_opening_player()
        cards = []
        for k in range(4):
            card = self._cards_played[round][(offset + k) % 4]
            if not card:
                break
            cards.append(card)
        return cards
    
    #test
    ''' How many-th player currently? '''
    def turn_nr(self):
        return len(self.table_cards())
    
    #test
    ''' How many points in a round (so far)? '''
    def round_points(self, round = None):
        round = round if round is not None else self.round
        return sum(card.points for card in self.round_cards(round))
    
    #test
    ''' highest played value that is of the correct color '''
    def highest_colour_value(self, round = None):
        round = round if round is not None else self.round
        opening_colour_cards = self.opening_colour_cards(round)
        return max(opening_colour_cards) if len(opening_colour_cards) else None
    
    #test
    ''' return all cards in a round that are of the correct colour '''
    def opening_colour_cards(self, round = None):
        round = round if round is not None else self.round
        return filter_colour(self.round_cards(round), self.opening_colour(round))
    
    ''' Player that plays/ed first this round '''
    def round_opening_player(self, round):
        return self.get_cards_player()[round]
    
    #todo: test
    def current_colour(self):
        if self.is_round_opening():
            return None
        return self._cards_played[self._opening_player[self._round]]
    
    #todo: test
    def is_round_opening(self):
        return not any(self._cards_played[self._round])
    
    def rounds_started(self):
        return self.round + 1
    
    ''' (This is the current round, zero-indexed) '''
    def rounds_completed(self):
        return self.round
    
    @property
    def round(self):
        return self._round
    
    #todo: test
    ''' have hearts been played? '''
    def hearts_played(self):
        return self.cards_played_colour(HEART)
    #todo: test
    ''' get_cards_played is a list with an entry for each turn
        each such entry contains, in the order of players, the cards played '''
    def get_cards_played(self):
        return self._cards_played
    #todo: test
    ''' which player played first during each turn 
        for the first card, use get_cards_played()[get_cards_player()] '''
    def get_cards_player(self):
        return self._opening_player
    
    def cards_played_all(self):
        return [card for card in sum(self._cards_played, []) if card]
    
    def cards_played_by(self, player_number):
        return [cards[player_number] for cards in self._cards_played if cards[player_number] is not None]
    
    #todo: test
    def cards_played_colour(self, colour):
        return filter_colour(self.cards_played_all(), colour)
    
    def colours_not_recognized_by(self, player_number):
        cards = self.cards_played_by(player_number)
        not_recognized = []
        for round, card in enumerate(cards):
            round_colour = self.opening_colour(round = round)
            if round_colour != card.colour:
                not_recognized.append(round_colour)
        return not_recognized
    
    #todo: test
    def cards_won_by(self, player_number):
        cards = []
        for round_nr in range(len(self._cards_played)):
            if self.round_winner(round_nr) == player_number:
                cards.extend(self._cards_played[round_nr])
        return cards
    
    #test
    def opening_card(self, round = None):
        round = round if round is not None else self.round
        return self._cards_played[round][self._opening_player[round]]
    
    def opening_colour(self, round = None):  # @ReservedAssignment
        round = round if round is not None else self.round
        card = self.opening_card(round = round)
        return card.colour if card else None
    
    ''' Provide the number of rounds completed (which is the index of the 
        current round, which starts at 0) '''
    def round_winner(self, round):  # @ReservedAssignment
        ''' Consider only opening-colour cards '''
        opening_colour = self.opening_colour(round)
        cards = filter_colour(self._cards_played[round], opening_colour)
        ''' Pick the highest one '''
        highest_val = 0
        for k, card in enumerate(cards):
            if card.value > highest_val:
                highest_val = card.value
                highest_player = k
        return highest_player
    
    ''' total number of cards played '''
    def count_cards_played(self):
        return len(self.cards_played_all())
        #return sum(len(self.round_cards(round)) for round in range(13))
    
    #test
    '''  check consistency (no duplicates) at end of game '''
    def check_consistency(self):
        table = {sym: {name: 0 for name in Card.names.keys()} for sym in Card.symbols.keys()}
        for round in range(13):
            for card in self.round_cards(round):
                if card is None:
                    raise Exception('consistency can only be checked for complete games')
                table[card.colour][card.value] += 1
        if not all(all(cell == 1 for cell in row.values()) for row in table.values()):
            raise Exception('inconsistent game state! not exactly one occurence of every card!')


