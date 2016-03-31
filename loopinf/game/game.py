from numpy import zeros


class Cell:
	def __init__(self, left=False, right=False, top=False, bottom=False):
		self.left = bool(left)
		self.right = bool(right)
		self.top = bool(top)
		self.bottom = bool(bottom)

	@classmethod
	def create_from_int(cls, val):
		inst = cls()
		inst.update_from_int(val)
		return inst

	def update_from_int(self, val):
		assert 0 <= val <= 15
		self.left = bool(val % 2)
		self.right = bool((val // 2) % 2)
		self.top = bool((val // 4) % 2)
		self.bottom = bool((val // 8))

	def to_int(self):
		return sum((
			1 if self.left else 0,
			2 if self.right else 0,
			4 if self.top else 0,
			8 if self.bottom else 0,
		))

	symbols = {
		# left, right, top, bottom
		(False, False, False, False): u' ',  # 0
		(False, False, False, True ): u'∨',
		(False, False, True , False): u'∧',
		(False, False, True , True ): u'║',
		(False, True , False, False): u'>',  # 4
		(False, True , False, True ): u'╔',
		(False, True , True , False): u'╚',
		(False, True , True , True ): u'╠',
		(True , False, False, False): u'<',  # 8
		(True , False, False, True ): u'╗',
		(True , False, True , False): u'╝',
		(True , False, True , True ): u'╣',
		(True , True , False, False): u'═',  # 12
		(True , True , False, True ): u'╦',
		(True , True , True , False): u'╩',
		(True , True , True , True ): u'╬',
	}

	def __str__(self):
		return self.symbols[self.left, self.right, self.top, self.bottom]

	def turn_right(self):
		self.right, self.top, self.left, self.bottom = self.top, self.left, self.bottom, self.right

	def is_empty(self):
		return not(self.left or self.right or self.top or self.bottom)


class Grid:
	def __init__(self, width=6, height=10):
		self.width = width
		self.height = height
		self.cells = []
		for k in range(height):
			self.cells.append(list(Cell() for m in range(width)))

	def __getitem__(self, indx):
		if len(indx) != 2:
			raise IndexError('Grid needs a 2D index, not <{0:}>'.format(indx))
		if indx[0] < 0 or indx[1] < 0:
			raise IndexError('Grid does not accept negative indices <{0:}, {1:}>'.format(*indx))
		# if indx[0] < 0 or indx[0] >= self.height or indx[1] < 0 or indx[1] >= self.width:
		# 	return Cell()
		return self.cells[indx[0]][indx[1]]

	def __setitem__(self, indx, val):
		#unused?
		if len(indx) != 2:
			raise IndexError('Grid needs a 2D index')
		if not isinstance(val, Cell):
			raise ValueError('Grid can only store Cells, not <{0:}>'.format(val))
		self.cells[indx[0]][indx[1]] = val

	def get_txt(self):
		parts = ['  ']
		for m in range(len(self.cells[0])):
			parts.append('{0:2d}'.format(m + 1))
		parts.append('\n')
		for k, row in enumerate(self.cells):
			parts.append('{0:2d} '.format(k + 1))
			for value in row:
				parts.append(str(value) + ' ')
			parts.append('\n')
		return ''.join(parts[:-1])

	def __str__(self):
		return self.get_txt()

	def to_ints(self):
		data = []
		for row in self.cells:
			data.append(list(val.to_int() for val in row))
		return data

	@classmethod
	def from_ints(cls, data):
		assert len(data)
		width = len(data[0])
		grid = cls(width=width, height=len(data))
		for k, row in enumerate(data):
			assert len(row) == width
			for n, val in enumerate(row):
				grid[k, n].update_from_int(val)
		return grid

	hex_map = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'E'}
	hex_map_rev = {v: k for k, v in hex_map.items()}

	def save(self, path):
		data = self.to_ints()
		with open(path, 'w+') as fh:
			for k, row in enumerate(data):
				if k > 0:
					fh.write('\n')
				fh.write(''.join(self.hex_map[val] for val in row))

	@classmethod
	def load(cls, path):
		data = []
		with open(path, 'r') as fh:
			for line in fh.read().splitlines():
				data.append(list(cls.hex_map_rev[val] for val in line))
		return cls.from_ints(data)

	def __iter__(self):
		for k, row in enumerate(self.cells):
			for m, cell in enumerate(row):
				# if not cell.is_empty():
				yield k, m, cell


if __name__ == '__main__':
	field = Grid.load('../levels/10')
	print(str(field))
	field = Grid()
	field[3,0] = Cell(left=True, right=True)
	print(str(field))


