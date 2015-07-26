
from sys import stdout
from numpy import copy, array, log2, savez, load, diff, zeros
from numpy.random import permutation
from AI import NeighbourAI, NNAI
from os.path import exists


def create_train(fname = 'traindata.npz', AI = NeighbourAI, foresight = 3):
	boards, directions, results = [], [], []
	while len(boards) < 1000000:#00
		stdout.write('.'); stdout.flush()
		gen = NeighbourAI({'quiet': True})
		steps, scores = [], []
		running = True
		while running:
			steps.append(copy(gen.game.M.flat))
			running, direction = gen.play_step()
			directions.append(direction)
			scores.append(gen.game.score)
		boards.extend(steps)
		scoreinc = [(scores[k + foresight] - scores[k]) / (10. * foresight) for k in range(len(scores) - 3*foresight)]
		scoreinc += [0]*foresight + [-6]*foresight + [-12]*foresight
		results.extend(scoreinc)
	stdout.write('\n')
	f = permutation(len(results))
	boards, directions, results = array(boards)[f], array(directions)[f], array(results)[f]
	savez(fname, boards = boards, directions = directions, results = results)


def train_NN(fname = 'traindata.npz'):
	net = NNAI(game_kwargs = {'quiet': True})
	with load(fname) as data:
		boards, directions, results = data['boards'], data['directions'], data['results']
	results -= results.mean()
	results /= results.std()
	net.train(boards, results, directions, rounds = 1)
	net.save('basic.net')


if __name__ == '__main__':
	if not exists('traindata.npz'):
		create_train()
	train_NN()


