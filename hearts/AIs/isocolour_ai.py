
'''
    Try to lose all cards of some colour
'''

from card import Card
from util import filter_colour, sort_by_value, legal_moves
from AIs.nopointwin_ai import NoPointWin


class IsolateColour(NoPointWin):
    
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
    
    def play_turn(self, state, hand, all_is_win = False):
        legal = sort_by_value(legal_moves(state, hand))
        if not legal[0].colour == state.current_colour():
            ''' lose colour if good option (1-2 cards), else just play '''
            lose_colours = [pair[1] for pair in self.colour_lose_order(hand) if 1 <= pair[0] <= 2]
            play_cards = []
            for colour in lose_colours:
                play_cards += sort_by_value(filter_colour(legal, colour), reverse = True)
            if len(play_cards):
                return play_cards[-1]
        ''' if recognizing or nothing to get rid of, just play '''
        return super(IsolateColour, self).play_turn(state = state, hand = hand, all_is_win = all_is_win)


