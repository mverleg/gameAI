# -*- coding: utf-8 -*-

from util import legal_moves, points
from random import shuffle, randint
from state import State
from itertools import permutations
from json import load, dumps
from card import CLUB, DIAMOND, HEART, SPADE, Card
from time import clock
from copy import copy


'''
    A four player game of Hearts
    Players play in the order they are provided
'''
class Game():
    
    text = True
    all_is_win = True
    name = '<noname>'
    player_cards = [[], [], [], []]
    player_AIs = []
    
    def __init__(self, name, AIs, text = True, all_is_win = True):
        self.name = name
        self.text = text
        self.all_is_win = all_is_win
        self.log('initializing game %s' % self.name)
        if not len(AIs) == 4:
            raise Exception('Not enough players')
        self.player_AIs = AIs
    
    def log(self, message):
        if self.text:
            print message
    
    def play_once(self, players, direction = 0):
        self.log('starting game %s' % self.name)
        time_limit = 5 * 13
        state = State()
        direction = direction % 4
        times = [0.0 for player in players]
        pass_cards = [[], [], [], []]
        if direction:
            for k, player in enumerate(players):
                ''' Select pass cards '''
                instant = clock()
                pass_cards[k] = player.pass_cards(copy(self.player_cards[k]), direction = direction, all_is_win = self.all_is_win)
                times[k] += clock() - instant
            for k in range(len(players)):
                ''' Now that everyone has selected, actually pass the cards '''
                self.pass_cards(pass_cards[k], k, (k + direction) % 4)
        for k in range(len(players)):
            ''' Find starting player '''
            for card in self.player_cards[k]:
                if card.is_club_2:
                    state._opening_player[0] = k
                    break
        self.log({ 0: 'no cards passing this game', 1: 'three cards passed left (playing direction)', 2: 'three cards passed opposite', 3: 'three cards passed right (counter to playing direction)', }[direction])
        for round in range(13):  # @ReservedAssignment
            ''' Rounds '''
            round_str = 'round %d:\t' % (round + 1)
            state._round = round
            if round:
                state._opening_player[round] = state.round_winner(round - 1)
            for k in range(4):
                ''' Players '''
                state._current_player = (state._opening_player[round] + k) % 4
                instant = clock()
                chosen_card = players[state._current_player].play_turn(state, copy(self.player_cards[state._current_player]), all_is_win = self.all_is_win)
                times[state._current_player] += clock() - instant
                self.play_card(state, state._current_player, chosen_card)
                round_str += 'p%d:%s\t' % (state._current_player + 1, chosen_card)
            self.log(round_str)
        ''' calculate the scores '''
        scores = [0, 0, 0, 0]
        for player_nr in range(len(players)):
            scores[player_nr] = points(state.cards_won_by(player_nr))
        if 26 in scores and self.all_is_win:
            self.log('ALL THE POINTS!!')
            scores = [0 if score else 26 for score in scores]
        if self.text:
            self.log('results    name              score   time')
            for k, player in enumerate(players):
                self.log('player %2d: %-20s %2d   %.2f' % (k + 1, player, scores[k], times[k]))
        if any(time > time_limit for time in times):
            scores = [0, 0, 0, 0]
            for k, time in enumerate(times):
                if time > time_limit:
                    print 'player #%d exceeded time limit' % k
                    scores[k] = 26
        state.check_consistency()
        if not sum(scores) in [26, 3*26]:
            raise Exception('Fraud (total score impossible)')
        self.log('ending game %s' % self.name)
        return scores
    
    ''' Player plays card '''
    def play_card(self, state, player_nr, card):
        ''' Check if no card played yet '''
        try:
            if state._cards_played[state._round][player_nr]:
                raise Exception('there is already a card for player %d in round %d' % (player_nr, state._round))
        except IndexError:
            ''' no card found (which is okay, though it should be None) '''
        ''' No need to check if it's player's turn, this function is only called if it is '''
        ''' Check if card in hand '''
        if card not in self.player_cards[player_nr]:
            raise Exception(u'tried to play %s, which is not in player #%s hand' % (unicode(card), player_nr))
        ''' Check if legal move '''
        if card not in legal_moves(state, self.player_cards[player_nr]):
            raise Exception(u'tried to play %s, which is not a legal move at this time for player #%s' % (unicode(card), player_nr))
        ''' If it's in hand, it can't secretly be a new instance '''
        ''' Remove from hand '''
        self.player_cards[player_nr].remove(card)
        ''' Put on stack '''
        state._cards_played[state._round][player_nr] = card
    
    ''' Player passes three cards '''
    def pass_cards(self, pass_cards, giving_nr, receiving_nr):
        for pass_card in pass_cards:
            ''' Check if in hand '''
            if not pass_card in self.player_cards[giving_nr]:
                print self.player_cards[giving_nr]
                raise Exception('Tried to pass a card %s that player doesn\'t have' % pass_card)
            ''' Pass the card along '''
            self.player_cards[giving_nr].remove(pass_card)
            self.player_cards[receiving_nr].append(pass_card)
    
    ''' Play with one random player order
        (actually it's just 1,2,3,4 but the cards are random '''
    def play_random(self):
        self.deal()
        players = [Player(player_nr = k) for k, Player in enumerate(self.player_AIs)]
        return self.play_once(players, direction = randint(0, 3))
    
    ''' Play all permutations of player order and passing direction for one deal '''
    def play_permutations(self):
        scores = [0 for k in range(4)]
        self.save_random(filename = 'permutation.json')
        for starting_order in permutations(range(4)):
            for passing_direction in [+1, -1, +2, 0]:
                players = [self.player_AIs[k](player_nr = k) for k in starting_order]
                self.deal(filename = 'permutation.json')
                game_scores = self.play_once(players, direction = passing_direction)
                for k in range(4):
                    scores[k] += game_scores[starting_order[k]]
        return scores
    
    ''' Deal cards and save them '''
    def save_random(self, filename):
        cards = Card.all()
        shuffle(cards)
        Card.json_save(cards, filename)
    
    ''' Play a non-random fixed deal (for consistent testing) '''
    def play_fixed(self, filename = 'fixed1.json'):
        self.deal(filename = filename)
        players = [Player() for Player in self.player_AIs]
        return self.play_once(players)
    
    def deal(self, filename = None):
        if filename:
            cards = Card.json_load(filename)
        else:
            cards = Card.all()
            shuffle(cards)
        for k in range(4):
            self.player_cards[k] = cards[k * 13:(k + 1) * 13]
    

