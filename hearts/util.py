# -*- coding: utf-8 -*-

from card import CLUB


'''
    Provide a list of cards and get the number of points they are worth
'''
def points(cards):
    return sum(card.points for card in cards) 

'''
    Filter everything not of the selected colour
'''
def filter_colour(cards, colour):
    correct_colour_cards = []
    for card in cards:
        if card.colour == colour:
            correct_colour_cards.append(card)
    return correct_colour_cards

'''
    returns cards sorted by value
'''
def sort_by_value(cards, reverse = False):
    return sorted(cards, key = lambda card: card.value, reverse = reverse)

'''
    Check if a card can legally be played for a given state
'''
def legal_moves(state, hand):
    if state.rounds_completed() == 0:
        if state.is_round_opening():
            ''' Starting player; only clubs 2 allowed '''
            for card in hand:
                if card.is_club_2:
                    return [card]
            raise Exception('starting player does not have clubs 2')
        clubs = filter_colour(hand, CLUB)
        if clubs:
            ''' We have clubs and didn't start '''
            return clubs
        else:
            no_points = [card for card in hand if not card.points]
            if no_points:
                ''' No clubs, so anything except points '''
                return no_points
            else:
                ''' Only points (this is really rare, but possible) '''
                return hand
    else:
        if state.is_round_opening():
            if state.hearts_played():
                ''' Hearts have been played, okay to open with '''
                return hand
            else:
                non_hearts = [card for card in hand if not card.is_hearts]
                if len(non_hearts):
                    ''' Open with anything except hearts '''
                    return non_hearts
                else:
                    ''' There are no hearts yet, but it's all we've got '''
                    return hand
        else:
            opening_colour = state.opening_colour(state._round)
            opening_colour_cards = filter_colour(hand, opening_colour)
            if opening_colour_cards:
                ''' We can recognize the opening color '''
                return opening_colour_cards
            else:
                ''' We can't recognize, play whatever we want '''
                return hand
            ''' or cooler: return opening_colour_cards or hand '''
    raise Exception('unknown game state')
    


