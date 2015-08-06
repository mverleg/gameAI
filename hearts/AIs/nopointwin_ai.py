
'''
    Pass cards with high numbers, play cards with lowest non-winning numbers first,
    but highest if you can't get points (opening round; last player in round)
'''

from util import legal_moves
from AIs.nonwin1st_ai import NonWinFirst


class NoPointWin(NonWinFirst):
    
    def play_turn(self, state, hand, all_is_win = False):
        legal = self.sort_by_value(legal_moves(state, hand))
        if state.is_round_opening():
            ''' opening player; play lowest '''
            return legal[0]
        elif state.turn_nr() == 3:
            if state.round_points() == 0:
                ''' last player and no points; dump high cards '''
                return legal[-1]
        elif state.rounds_completed() == 0:
            ''' first round; no points allowed; dump highest '''
            return legal[-1]
        ''' there are or could be points '''
        non_win = self.non_win_cards(state, legal)
        if len(non_win):
            ''' react with the highest card that can't win '''
            return non_win[-1]
        else:
            ''' we can't dodge; might as well dump high card '''
            return legal[-1]


