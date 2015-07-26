
from sys import stdout
from numpy import copy, array, log2, savez, load
from numpy.random import permutation
from AI import NeighbourAI, NNAI


def create_train(fname = 'traindata.npz', AI = NeighbourAI):
	win_score = log2(2048) * 2048
	boards, directions, scores = [], [], []
	while len(boards) < 50000:
		stdout.write('.'); stdout.flush()
		gen = NeighbourAI({'quiet': True})
		steps = []
		running = True
		while running:
			steps.append(copy(gen.game.M.flat))
			running, direction = gen.play_step()
			directions.append(direction)
		boards.extend(steps)
		scores.extend([gen.game.score] * len(steps))  #todo: update exponent
	stdout.write('\n')
	f = permutation(len(scores))
	boards, directions, scores = array(boards)[f], array(directions)[f], array(scores)[f]
	errors = scores / float(win_score)
	errors -= errors.mean()
	errors /= errors.std()
	savez(fname, boards = boards, errors = errors, scores = scores, directions = directions)


def train_NN(fname = 'traindata.npz'):
	net = NNAI()
	with load(fname) as data:
		boards, errors, scores, directions = data['boards'], data['errors'], data['scores'], data['directions']
	net.train(boards, errors, directions)
	#for k in range(len(errors)):
	#	print(net.predict(boards[k, :]))
	#	break


if __name__ == '__main__':
	#create_train()
	train_NN()


