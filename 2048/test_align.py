
from numpy import array, flipud, fliplr, rot90, array_equal
from align import align


M = align(array([
		[ 0, 0, 1, 2],
		[ 1, 3, 4, 1],
		[ 3, 5, 6, 5],
		[ 4, 7, 4, 1],
]))

def check_invariant(T, msg = 'found operation that alignment doesn\'t undo'):
	P = align(T)
	if not array_equal(P, M):
		print('before\n', 2**M)
		print('operation\n', 2**T)
		print('realigned\n', 2**P)
		raise AssertionError(msg)


def test_hor_ver_mirror():
	check_invariant(flipud(M))
	check_invariant(fliplr(M))
	check_invariant(flipud(fliplr(M)))


def test_rotations():
	check_invariant(rot90(M, 1), 'rotating 90 is not realigned')
	check_invariant(rot90(M, 2), 'rotating 180 is not realigned')
	check_invariant(rot90(M, 3), 'rotating -90 is not realigned')


def test_inverse():
	check_invariant(M[::-1, ::-1], 'inversion is not realigned')


def test_diag_mirror():
	check_invariant(M.T, 'diagonal mirror \ is not realigned')
	check_invariant(rot90(rot90(M, 1).T, 3), 'diagonal mirror / is not realigned')


def test_combinations():
	for k, N in enumerate([
		fliplr(M),
		M[::-1, ::-1],
		M.T,
		flipud(rot90(M.T, 2)),
		rot90(M).T[::-1, ::-1],
	]):
		assert array_equal(M, align(N)), 'alignment didn\'t work a combination of operations (k={0:d})'.format(k)


def test_invalid():
	N = align(array([
		[  0,   0,   4,   2],
		[  2,   8,  16,   2],
		[  8,  16,  64,  32],
		[ 16, 128,  32,   2],
	]))
	assert not array_equal(M, align(N)), 'incompatible arrays somehow aligned to be the same'


def test_idempotent():
	for k, N in enumerate([
		fliplr(M),
		M[::-1, ::-1],
		M.T,
		flipud(rot90(M.T, 2)),
		rot90(M).T[::-1, ::-1],
	]):
		assert array_equal(align(N), align(align(N))), 'aligning twice gives different result (k={0:d})'.format(k)


