
'''
    Pass cards with high numbers, open with low cards, react with high if no points yet
'''

from util import legal_moves
from AIs.nonwin1st_ai import NonWinFirst


class NoPointsHigh(NonWinFirst):
    
    def play_turn(self, state, hand, all_is_win = False):
        legal = self.sort_by_value(legal_moves(state, hand))
        if state.is_round_opening():
            ''' opening player; play lowest '''
            return legal[0]
        if state.round_points():
            ''' there are points; dodge '''
            non_win = self.non_win_cards(state, legal)
            if len(non_win):
                ''' react with the highest card that can't win '''
                return non_win[-1]
        ''' no points or can't dodge '''
        return legal[-1]


