
'''
    Pass cards with high numbers, play cards with highest non-winning numbers first
'''

from util import legal_moves
from AIs.low1st_ai import LowFirst


class NonWinFirst(LowFirst):
    
    ''' return only cards that can't win the round (preserves order) '''
    def non_win_cards(self, state, cards):
        ''' (either all or none of the play cards recognize colour) '''
        if state.current_colour() == cards[0].colour:
            ''' recognizing colour; filter high ones '''
            highest = state.highest_colour_value()
            return [card for card in cards if card.value < highest]
        ''' not recognizing colour; nothing can win '''
        return cards
    
    def play_turn(self, state, hand, all_is_win = False):
        legal = self.sort_by_value(legal_moves(state, hand))
        if state.is_round_opening():
            ''' opening player; play lowest '''
            return legal[0]
        else:
            non_win = self.non_win_cards(state, legal)
            if len(non_win):
                ''' react with the highest card that can't win '''
                return non_win[-1]
            else:
                ''' have no cards to dodge '''
                return legal[0]


