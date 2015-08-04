
"""
	2D square has 8 symmetry operations:
	* rotation pi/2, pi, -pi/2 = pi: inversion, +-pi/2: hor * diagonal
	* mirror horizontal & vertical
	* mirror diagonal (x2) = below, 2nd one is 1st * inversion
		[0 1]   [ 0 -1]
		[1 0]   ]-1  0]
	* inversion = mirror hor+ver
	So we need only combinations of horizontal and vertical flips with the transpose.

	There are 20 options, that and more info here:
	https://datascience.stackexchange.com/questions/6591/train-a-classifier-for-a-game-with-feedback-on-chosen-move-instead-of-true-label
"""

from game import Game
from AI import NeighbourAI
from numpy import flipud, fliplr, tril, triu


def make_board():
	game = Game(seed = None, quiet = True)
	plyr = NeighbourAI(game)
	for k in range(150):
		if not plyr.play_step():
			break
	plyr.game.M = plyr.game.M.T
	return plyr.game

def get_moment(M, p, q):
	x, y = M.shape[0] // 2, M.shape[1] // 2
	Z = 0
	for m in range(M.shape[0]):
		for n in range(M.shape[1]):
			Z += (m - x)**q * (n - y)**p * 2**M[m, n]
	return Z

def align(M):
	LR = fliplr(M)
	if get_moment(M, p = 1, q = 0) < get_moment(LR, p = 1, q = 0):
		M = LR
	UD = flipud(M)
	if get_moment(M, p = 0, q = 1) < get_moment(UD, p = 0, q = 1):
		M = UD
	if tril(M).sum() < triu(M).sum():
		M = M.T.copy()
	return M


