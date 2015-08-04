
from game import Game
from numpy import copy, array, zeros, clip, float32
from numpy.random import RandomState
import pickle
from nnet import make_net


def move_pred(game, predictions):
	directions = predictions.argsort()[::-1]
	for dir in directions:
		running = game.act(direction = dir)
		if running is not None:
			break
	else:
		raise AssertionError('no legal moves')
	return running, dir


class BaseAI():
	def __init__(self, game={}):
		self.game = game
		#print(self.__class__.__name__)


class RandomAI(BaseAI):
	"""
		Make random moves.
	"""
	def __init__(self, game, seed = None):
		super().__init__(game = game)
		self.random = RandomState(seed)

	def play(self):
		running = True
		while running:
			predictions = self.random.rand(4)
			running = move_pred(self.game, predictions)[0]


class StayDownAI(BaseAI):
	"""
		Optimize free space among current moves, and don't move down unless you have to.
	"""
	def play(self):
		running = True
		while running:
			scores = array([1, 2, 1, 0])
			running = move_pred(self.game, scores)[0]


class FreeAI(BaseAI):
	"""
		Optimize free space among current moves, and don't move down unless you have to.
	"""
	def score(self, M):
		return (M == 0).sum()

	def play(self):
		running = True
		while running:
			scores = array([
				self.score(self.game.board_move(copy(self.game.M), 0, hor = True, dir = +1, test = False)[1]),
				self.score(self.game.board_move(copy(self.game.M), 0, hor = False, dir = +1, test = False)[1]),
				self.score(self.game.board_move(copy(self.game.M), 0, hor = True, dir = -1, test = False)[1]),
				self.score(self.game.board_move(copy(self.game.M), 0, hor = False, dir = -1, test = False)[1])
			])
			scores[1] += 1
			running = move_pred(self.game, scores)[0]


class NeighbourAI(BaseAI):
	"""
		Optimize free space among current moves, and don't move down unless you have to.
	"""
	def score(self, M):
		S = 0
		for x in range(M.shape[0] - 1):
			for y in range(M.shape[1] - 1):
				if M[x, y] > 0:
					if M[x + 1, y] > 0:
						S += abs(int(M[x, y]) - int(M[x + 1, y]))
					if M[x, y + 1] > 0:
						S += abs(int(M[x, y]) - int(M[x, y + 1]))
		return -S  # about 30

	def play_step(self):
		scores = array([
			self.score(self.game.board_move(copy(self.game.M), 0, hor = True, dir = +1, test = False)[1]),
			self.score(self.game.board_move(copy(self.game.M), 0, hor = False, dir = +1, test = False)[1]),
			self.score(self.game.board_move(copy(self.game.M), 0, hor = True, dir = -1, test = False)[1]),
			self.score(self.game.board_move(copy(self.game.M), 0, hor = False, dir = -1, test = False)[1])
		])
		scores[1] += 1
		return move_pred(self.game, scores)

	def play(self):
		running = True
		while running:
			running = self.play_step()[0]


class Moment11(BaseAI):
	"""
		Make the (1,1) image moment as high as possible (meaning high values are in a specific corner).
	"""
	def score(self, M):
		Z = 0
		for m in range(self.game.M.shape[0]):
			for n in range(self.game.M.shape[1]):
				Z += (m + n) * 2**M[m, n]
		return Z

	def play_step(self):
		scores = array([
			self.score(self.game.board_move(copy(self.game.M), 0, hor = True, dir = +1, test = False)[1]),
			self.score(self.game.board_move(copy(self.game.M), 0, hor = False, dir = +1, test = False)[1]),
			self.score(self.game.board_move(copy(self.game.M), 0, hor = True, dir = -1, test = False)[1]),
			self.score(self.game.board_move(copy(self.game.M), 0, hor = False, dir = -1, test = False)[1])
		])
		scores[1] += 1
		return move_pred(self.game, scores)

	def play(self):
		running = True
		while running:
			running = self.play_step()[0]


class FreeNBDownAI(BaseAI):
	"""
		Combination of the above
	"""
	def __init__(self, game, neighbour_strength = 6):
		super().__init__(game = game)
		self.neighbour_strength = neighbour_strength

	def score(self, M):
		S = 0.
		for x in range(M.shape[0] - 1):
			for y in range(M.shape[1] - 1):
				if M[x, y] > 0:
					if M[x + 1, y] > 0:
						S += abs(int(M[x, y]) - int(M[x + 1, y]))
					if M[x, y + 1] > 0:
						S += abs(int(M[x, y]) - int(M[x, y + 1]))
		return (M == 0).sum() - S / self.neighbour_strength

	def play(self):
		running = True
		while running:
			scores = array([
				2 * self.score(self.game.board_move(copy(self.game.M), 0, hor = True, dir = +1, test = False)[1]),
				2 * self.score(self.game.board_move(copy(self.game.M), 0, hor = False, dir = +1, test = False)[1]) + 1,
				2 * self.score(self.game.board_move(copy(self.game.M), 0, hor = True, dir = -1, test = False)[1]),
				-1,
			])
			scores[1] += 1
			running = move_pred(self.game, scores)[0]



class AltDownRight(BaseAI):

	def __init__(self, game, neighbour_strength = 6):
		super().__init__(game = game)
		self.current = array([4, 3, 2, 1])
		self.next = array([3, 4, 2, 1])

	def play(self):
		running = True
		while running:
			self.current, self.next = self.next, self.current
			running = move_pred(self.game, self.current)[0]


class NNAI(BaseAI):
	"""
		Use Lasagne neural network to teach the AI to play.
	"""
	def __init__(self, game):
		super().__init__(game = game)
		self.nn = make_net(self.game.W, self.game.H, size1 = 45, size2 = 35)

	@classmethod
	def load(self, fname):
		with open(fname, 'rb') as fh:
			return pickle.load(fh)

	def save(self, fname):
		with open(fname, 'wb+') as fh:
			pickle.dump(self, fh)

	def train(self, batch, results, choices, rounds = 3):
		#todo: more than 3 doesn't seem to do much atm, check later
		for rnd in range(rounds):
			wanted = self.nn.predict_proba(batch).astype(float32)
			offset = zeros(wanted.shape, dtype = float32)
			for k, choice in enumerate(choices):
				offset[k, choice] = results[k] / 3
			goal = clip(wanted + offset, 0, 1)
			self.nn.fit(batch, goal)

	def predict(self, D):
		"""
			Predict one sample (no batches).

			:param D: Flattened playing board
		"""
		if len(D.shape) == 1:
			D = array([D])
		return self.nn.predict_proba(D)[0]

	def play(self):
		running = True
		while running:
			D = array(self.game.M.flat)
			scores = self.predict(D)
			running = move_pred(self.game, scores)[0]


if __name__ == '__main__':
	def nngen(game):
		nngen.__name__ = 'NeuralNet'
		return NNAI.load('basic.net')
	N = 20
	AIs = (RandomAI, FreeAI, NeighbourAI, Moment11, StayDownAI, FreeNBDownAI, AltDownRight)#, NNAI, nngen)
	print('comparing {0:d} AIs, {1:d} iterations each'.format(len(AIs), N))
	print('AI name           turns  score    max')
	for AI in AIs:
		Q = zeros((N, 3), dtype = int)
		for k in range(N):
			game = Game(seed = 4242 + k, quiet = True)
			plyr = AI(game = game)
			plyr.play()
			Q[k, :] = plyr.game.turn, plyr.game.score, 2**plyr.game.M.max()
		print('{0:16s}  {1:5d}  {2:5d}  {3:5d}'.format(AI.__name__, *Q.sum(0) // N))


