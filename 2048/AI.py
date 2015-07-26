
from game import Game
from numpy import copy, array, zeros, clip, float32
from numpy.random import RandomState
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
	def __init__(self, game_kwargs = {}):
		self.game = Game(**game_kwargs)
		#print(self.__class__.__name__)


class RandomAI(BaseAI):
	"""
		Make random moves.
	"""
	def __init__(self, seed = 4242, game_kwargs = {}):
		super().__init__(game_kwargs = game_kwargs)
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


class FreeNBDownAI(BaseAI):
	"""
		Combination of the above
	"""
	def __init__(self, neighbour_strength = 6, game_kwargs = {}):
		super().__init__(game_kwargs = game_kwargs)
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


class NNAI(BaseAI):
	"""
		Use Lasagne neural network to teach the AI to play.
	"""
	def __init__(self, game_kwargs = {}):
		super().__init__(game_kwargs = game_kwargs)
		self.nn = make_net(self.game.W, self.game.H)

	def train(self, batch, results, choices):
		wanted = self.nn.predict_proba(batch).astype(float32)
		#print(wanted[:, choices].mean())
		#print(abs(results).mean())
		#wanted[:, choices] += results / 5
		offset = zeros(wanted.shape, dtype = float32)
		for k, choice in enumerate(choices):
			offset[k, choice] = results[k] / 3
		#print(Q)
		#print(self.nn.predict_proba(batch) - wanted)
		#print(choices)
		goal = clip(wanted + offset, 0, 1)
		print(self.nn.fit(batch, goal))

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
	N = 5
	AIs = (RandomAI, FreeAI, NeighbourAI, StayDownAI, FreeNBDownAI, NNAI)
	print('comparing {0:d} AIs, {1:d} iterations each'.format(len(AIs), N))
	print('AI name           turns  score    max')
	for AI in AIs:
		Q = zeros((N, 3), dtype = int)
		for k in range(N):
			plyr = AI(game_kwargs = {'seed': 4242 + k, 'quiet': True})
			plyr.play()
			Q[k, :] = plyr.game.turn, plyr.game.score, 2**plyr.game.M.max()
		print('{0:16s}  {1:5d}  {2:5d}  {3:5d}'.format(AI.__name__, *Q.sum(0) // N))


