
'''
    Henk is just a name
    calculates a score for each card based on how desirable it is to have,
      e.g. many lower/higher cards are in your hand and in play
'''

from base_ai import BaseAI
from util import legal_moves, sort_by_value, filter_colour
from card import Card
from math import ceil
from opponents import Opponent

HAND, TABLE, HIDDEN = +1, 0, -1

class Henk(BaseAI):
    
    def __init__(self, *args, **kwargs):
        super(Henk, self).__init__(*args, **kwargs)
        self.opponents = None
    
    def colour_stats(self, cards):
        stats = {sym: {'low': 15, 'high': 0, 'sum': 0, 'count': 0} for sym in Card.symbols.keys()}
        for card in cards:
            stats[card.colour]['low']  = min(stats[card.colour]['low'], card.value)
            stats[card.colour]['high'] = max(stats[card.colour]['high'], card.value)
            stats[card.colour]['sum'] += card.value
            stats[card.colour]['count'] += 1
        for sym in Card.symbols.keys():
            stats[sym]['mean'] = float(stats[card.colour]['sum']) / stats[card.colour]['count']
        return stats
    
    def colour_lose_order(self, cards):
        return sorted([(stat['count'], col) for col, stat in self.colour_stats(cards).items()], key = lambda x: x[0])
    
    def pass_cards(self, hand, direction = 2, all_is_win = False):
        pass_cards = []
        for count, colour in self.colour_lose_order(hand):
            pass_cards += sort_by_value(filter_colour(hand, colour), reverse = True)
            if len(pass_cards) >= 3:
                break
        return pass_cards[-3:]
    
    @classmethod
    def game_state(cls, state, hand):
        table = {sym: {name: HIDDEN for name in Card.names.keys()} for sym in Card.symbols.keys()}
        for round in range(13):
            for card in state.round_cards(round):
                if card is not None:
                    table[card.colour][card.value] = TABLE
        for card in hand:
            table[card.colour][card.value] = HAND
        return table
    
    @classmethod
    def show_game_state(cls, state, hand):
        table = cls.game_state(state, hand)
        disp_conv = {HAND: 'X', TABLE: '.', HIDDEN: ' '}
        print '   %s' % ' '.join(Card.abbrev.values())
        for sym, row in table.items():
            print '%-2s %s' % (Card.symbols[sym], ' '.join(disp_conv[item] for item in row.values()))
    
    ''' pessimistic win chance (if your opponents want you to lose the round) '''
    def win_chance(self, card, state, hand):
        """ 'copy' sure win-lose stuff from lose_chance """
    
    ''' pessimistic lose chance (if your opponents want you to win the round) '''
    def lose_chance(self, card, state, hand):
        print 'lose chance with my card', unicode(card)
        if state.is_round_opening():
            colour = card.colour
        else:
            colour = state.current_colour()
            if card.colour != colour:
                ''' not recognizing; sure to lose '''
                return 1.
        ''' already a higher card; sure to lose '''
        if any(card.value < played.value for played in state.opening_colour_cards()):
            return 1.
        ''' which players still have to play? '''
        pending_players = state.pending_players()[1:]
        ''' which players can recognize the colour? '''
        recognizing_players = []
        for player in range(4):
            if colour not in state.colours_not_recognized_by(player):
                recognizing_players.append(player)
        ''' overlap: which next ones can recognize '''
        recognizing_pending = [player for player in pending_players if player in recognizing_players]
        ''' special case: no next players '''
        if not len(recognizing_pending):
            return 1.
        ''' which cards can be played? '''
        game_cards = self.game_state(state, hand)
        playable_cards = [cardk for cardk, location in game_cards[colour].items() if location == HIDDEN]
        ''' which of those cards can defeat me? '''
        lower_cards = [value for value in playable_cards if value < card.value]
        ''' special case: no lower cards '''
        if not len(lower_cards):
            return 1.
        ''' what are the chances a next player does not have dangerous cards? '''
        if len(recognizing_players) == len(recognizing_pending):
            ''' all the danger cards are with players after you '''
            return 0.
        
        """
            strategy: how many hand positions of recognizing players:
            - in total?
            - for players who have already played?
            calculate how many of the permutations put all the cards in the unplayable ones
        """
        
        """
        ''' hand positions before where the card could be '''
        slots_before = 
        
        if next_recog_count == 1:
            if 2 * cards_per_player < danger_card_count:
                return 0.
            ''' chance that danger cards distributed such that none at next player '''
            return reduce(lambda x, y: x * y, cards_per_player / (recog_count * cards_per_player - k) for k in range(danger_card_count), 1)
        elif next_recog_count == 2:
            if cards_per_player < danger_card_count:
                return 0.
            ''' chance that danger cards are all on the same person (the one before you) '''
            return 
            #return 1. - reduce(lambda x, y: x * y, cards_per_player / (recog_count * cards_per_player - k) for k in range(danger_card_count), 1)
        else:
            ''' there are higher cards and everyone plays after me '''
            return 0.
        print 'cards_per_player', cards_per_player
        #lose_chance = 
        
        #print pending_players, recognizing_players, recognizing_pending
        #recognizing_pending = pending_players + set(recognizing_players)
        #print pending_players, recognizing_players
        #if not len(recognizing_pending):
        #    return 1.
        
        #print 'my card', unicode(card)
        #print 'other player playable cards', [value for value, location in colour_cards[colour].items() if location == HIDDEN]
        """
    
    def play_turn(self, state, hand, all_is_win = False):
        ''' keep track of opponents if not already '''
        if self.opponents is None:
            self.opponents = []
            for opp_nr in range(4):
                if not opp_nr == self.number:
                    self.opponents.append(Opponent(opp_nr, state, hand))
            for opp in self.opponents:
                opp.add_opponents(self.opponents)
        for opp in self.opponents:
            opp.filter()
            opp.show_opponent_state() #tmp
        ''' get all legal moves '''
        legal = sort_by_value(legal_moves(state, hand))
        #self.show_game_state(state, hand)
        return legal[-1]
    
        for card in legal:
            self.lose_chance(card, state, hand)
        legal = sort_by_value(legal_moves(state, hand))
        return legal[-1]




