
from game import Game
from numpy import array, equal


def test_board_01():
	"""
		Test board initialization.
	"""
	g1 = Game(W = 5, H = 3, empty = True, quiet = True)
	assert g1.M.sum() == 0
	g2 = Game(W = 6, H = 5, empty = False, quiet = True)
	assert 2 <= (g2.M).sum() <= 4
	assert g2.M.shape[0] == 6 and g2.M.shape[1] == 5


def li2a(li):
	return array([li])


def run_move_test(tests):
	for actions, W, H, init, result in tests:
		g = Game(W = W, H = H, empty = True, quiet = True)
		g.M[: :] = init
		for action in actions:
			getattr(g, action)(test = False)
		assert equal(g.M, result).all(), 'Failed for {0:s} {1:s} -> {2:s}, got {3:s}'.format(action, str(init), str(result), str(g.M))


def test_moves_01():
	"""
		222.
	"""
	run_move_test(tests = (
		(('move_left',), 4, 1, li2a([1, 1, 1, 0]).T, li2a([2, 1, 0, 0]).T),
		(('move_right',), 4, 1, li2a([1, 1, 1, 0]).T, li2a([0, 0, 1, 2]).T),
		(('move_up',), 1, 4, li2a([1, 1, 1, 0]), li2a([2, 1, 0, 0])),
		(('move_down',), 1, 4, li2a([1, 1, 1, 0]), li2a([0, 0, 1, 2])),
	))


def test_moves_02():
	"""
		2222
	"""
	run_move_test(tests = (
		(('move_left',), 4, 1, li2a([1, 1, 1, 1]).T, li2a([2, 2, 0, 0]).T),
		(('move_right',), 4, 1, li2a([1, 1, 1, 1]).T, li2a([0, 0, 2, 2]).T),
		(('move_up',), 1, 4, li2a([1, 1, 1, 1]), li2a([2, 2, 0, 0])),
		(('move_down',), 1, 4, li2a([1, 1, 1, 1]), li2a([0, 0, 2, 2])),
	))


def test_moves_03():
	"""
		22.4
	"""
	run_move_test(tests = (
		(('move_left',), 4, 1, li2a([1, 1, 0, 2]).T, li2a([2, 2, 0, 0]).T),
		(('move_right',), 4, 1, li2a([1, 1, 0, 2]).T, li2a([0, 0, 2, 2]).T),
		(('move_up',), 1, 4, li2a([1, 1, 0, 2]), li2a([2, 2, 0, 0])),
		(('move_down',), 1, 4, li2a([1, 1, 0, 2]), li2a([0, 0, 2, 2])),
	))


def test_play_01():
	"""
		Play a full board without random additions.
	"""
	g = Game(W = 4, H = 3, empty = True, quiet = True)
	g.M[:, :] = array([[1, 1, 1, 1], [1, 1, 2, 2], [3, 1, 1, 3]]).T
	g.move_left(test = False)
	g.move_right(test = False)
	g.move_down(test = False)
	g.move_right(test = False)
	g.move_right(test = False)
	assert g.score == 104
	assert g.M[3, 2] == 5
	assert g.M[3, 1] == 3
	assert g.move_right(test = True) is False
	assert g.move_left(test = True) is True
	assert g.move_down(test = True) is False
	assert g.move_up(test = True) is True


def test_full_continue():
	"""
		Test that a full board with moves isn't game over.
	"""
	g = Game(W = 3, H = 3, empty = True, quiet = True)
	g.M[:, :] = array([[1, 1, 2], [3, 2, 1], [2, 1, 2]]).T
	assert g.move_right(test = True) is True
	assert g.move_left(test = True) is True
	assert g.move_down(test = True) is False
	assert g.move_up(test = True) is False
	assert not g.game_over()


def test_defeat():
	"""
		Test that no more moves results in game over.
	"""
	g = Game(W = 3, H = 3, empty = True, quiet = True)
	g.M[:, :] = array([[1, 2, 1], [2, 1, 2], [1, 2, 1]])
	assert g.move_right(test = True) is False
	assert g.move_left(test = True) is False
	assert g.move_down(test = True) is False
	assert g.move_up(test = True) is False
	assert g.game_over()


def test_seeding():
	"""
		Test that seeded games behave identically.
	"""
	g1 = Game(W = 4, H = 4, seed = 42, quiet = True)
	g1.move_left()
	g1.move_up()
	g1.move_right()
	g1.move_down()
	g2 = Game(W = 4, H = 4, seed = 42, quiet = True)
	g2.move_left()
	g2.move_up()
	g2.move_right()
	g2.move_down()
	assert equal(g1.M, g2.M).all()


