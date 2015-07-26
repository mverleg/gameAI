
from sys import stdout
from numpy import zeros, uint8
from numpy.random import RandomState


class Game():
	def __init__(self, W = 4, H = 4, empty = False, seed = None, quiet = False):
		self.W, self.H = W, H
		self.M = zeros((W, H), dtype = uint8)
		self.turn = 0
		self.score = 0
		self.random = RandomState(seed)
		self.quiet = quiet
		if not empty:
			self.add_rand()
			self.add_rand()
		self.show()

	def add_rand(self):
		assert not self.empty_space(), 'Board is full.'
		val = 1 + (self.random.rand() > 0.9)
		while True:
			x, y = self.random.randint(self.W), self.random.randint(self.H)
			if self.M[x, y] == 0:
				self.M[x, y] = val
				break

	def show(self, force = False):
		if self.quiet and not force:
			return
		stdout.write('\nturn {0:d}, score {1:d}\n'.format(self.turn, self.score))
		for row in self.M.T:
			stdout.write(''.join('{0:3d}'.format(2**v) if v else '  .' for v in row) + '\n')

	def move(self, hor = True, dir = -1, test = True):
		changed = False
		N = self.M if hor else self.M.T
		lim = N.shape[0] - 1 if dir > 0 else 0
		for y in range(N.shape[1]):
			mrgd = lim + dir
			for x in range(N.shape[0])[::-dir]:
				if N[x, y]:
					for q in range(x + dir, lim + dir, dir):
						if N[q, y] == N[x, y] and q != mrgd:
							if not test:
								N[q, y] += 1
								N[x, y] = 0
								self.score += 2**N[q, y]
								mrgd = q
							changed = True
							break
						elif N[q, y] > 0:
							if x != q - dir:
								if not test:
									N[q - dir, y] = N[x, y]
									N[x, y] = 0
								changed = True
							break
					else:
						if x != lim:
							if not test:
								N[lim, y] = N[x, y]
								N[x, y] = 0
							changed = True
		self.M = N if hor else N.T
		return changed

	def move_left(self, test = False):
		return self.move(hor = True, dir = -1, test = test)

	def move_right(self, test = False):
		return self.move(hor = True, dir = +1, test = test)

	def move_up(self, test = False):
		return self.move(hor = False, dir = -1, test = test)

	def move_down(self, test = False):
		return self.move(hor = False, dir = +1, test = test)

	def empty_space(self):
		return not (self.M == 0).any()

	def game_over(self):
		return not self.move_left(test = True) and not self.move_right(test = True) \
			and not self.move_up(test = True) and not self.move_down(test = True)

	def act(self, dx = 0, dy = 0):
		self.turn += 1
		if self.move(hor = True, dir = -1, test = True):
			self.move(hor = True, dir = -1, test = False)
		else:
			print('CANNOT MOVE THAT WAY!')
			exit()
		self.add_rand()
		self.show()
		if self.game_over():
			self.show()
			stdout.write('\nGAME OVER!\n\n')


if __name__ == '__main__':
	g = Game()
	for k in range(13):
		g.act()


