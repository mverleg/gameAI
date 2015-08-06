# -*- coding: utf-8 -*-

'''
    Script for the Hearts AI competition
'''

from game import Game
from AIs.random_ai import Random
from AIs.human_ai import Human
from AIs.low1st_ai import LowFirst
from AIs.nonwin1st_ai import NonWinFirst
from AIs.nopointwin_ai import NoPointWin
from AIs.nopointhigh import NoPointsHigh
from AIs.high1st_ai import HighFirst
from AIs.isocolour_ai import IsolateColour
from AIs.henk_ai import Henk


def main():
    print 'Welcome to Hearts AI competition'
    
    #AIs = [Human, Random, Random, Random]
    #AIs = [LowFirst, NonWinFirst, NoPointWin, Random]
    AIs = [Random, Henk, Random, Random]
    
    ''' one game '''
    game = Game('game#1', AIs, text = True, all_is_win = False)
    game.play_random()
    
    ''' many games '''
    if False:
        total = [0, 0, 0, 0]
        for k in range(20):
            game = Game('game#1', AIs, text = False, all_is_win = True)
            score = game.play_permutations()
            print k+1, score
            for m in range(4):
                total[m] += score[m]
        mean = sum(total) / 4
        score_percent = [100 * (float(k) / mean - 1) for k in total]
        for k in range(4):
            print '%-16s %.2f' % (AIs[k].__name__, score_percent[k])
    
    print 'Terminating Hearts AI competition'
    

if __name__ == '__main__':
    main()
    

