
from nolearn.lasagne import NeuralNet, BatchIterator, TrainSplit
from numpy import inf, copy, float32
from lasagne.updates import nesterov_momentum
from lasagne.layers import InputLayer, DenseLayer
from lasagne.nonlinearities import softmax, LeakyRectify
from lasagne.init import HeNormal, Normal, Constant
from theano import shared


class StopWhenOverfitting(object):
	def __call__(self, nn, train_history):
		if train_history[-1]['epoch'] > 10:
			if train_history[-1]['train_loss'] / train_history[-1]['valid_loss'] < 0.8:
				raise StopIteration('overfitting')


class StopAfterMinimum(object):
	def __init__(self):
		self.best_valid = inf
		self.best_valid_epoch = 0
		self.best_weights = None

	def __call__(self, nn, train_history):
		current_valid = train_history[-1]['valid_loss']
		current_epoch = train_history[-1]['epoch']
		if current_valid < self.best_valid:
			self.best_valid = current_valid
			self.best_valid_epoch = current_epoch
			self.best_weights = copy(nn.get_all_params_values())
		elif self.best_valid_epoch + 30 < current_epoch and self.best_weights:
			nn.load_params_from(self.best_weights)
			raise StopIteration('loss increasing')


class AdjustVariable(object):
	def __init__(self, name, start = 1., stop = 0.005):
		self.start, self.stop = start, stop

	def __call__(self, nn, train_history):
		epoch = train_history[-1]['epoch']
		print(self.stop + (self.start - self.stop) * epoch / nn.max_epochs)
		new_value = float32(self.stop + (self.start - self.stop) * epoch / nn.max_epochs)
		getattr(nn, 'update_learning_rate').set_value(new_value)


inp = InputLayer(shape = (None, 16,))
DenseLayer(**{
	'W': HeNormal(),
	'nonlinearity': LeakyRectify(leakiness = 0.1),
	'incoming': inp,
	'num_units': 20,
	'b': Constant(),
	'name': 'dense1',
}) #todo


def make_net(W, H, size1 = 20, size2 = 15):
	net = NeuralNet(
		layers = [
			('input',  InputLayer),
			('dense1', DenseLayer),
			('dense2', DenseLayer),
			('output', DenseLayer),
		],

		input_shape = (None, W * H),

		dense1_num_units = size1,
		dense1_nonlinearity = LeakyRectify(leakiness = 0.1),
		dense1_W = HeNormal(),
		dense1_b = Constant(),

		dense2_num_units = size2,
		dense2_nonlinearity = LeakyRectify(leakiness = 0.1),
		dense2_W = HeNormal(),
		dense2_b = Constant(),

		output_num_units = 4,
		output_nonlinearity = softmax,
		output_W = HeNormal(),
		output_b = Constant(),

		update = nesterov_momentum,  # todo
		update_learning_rate = shared(float32(1.)),
		update_momentum = 0.7,

		max_epochs = 200,
		#on_epoch_finished = [
		#	StopWhenOverfitting(),
		#	StopAfterMinimum(),
		#],

		#label_encoder = False,
		regression = True,
		verbose = 1,

		batch_iterator_train = BatchIterator(batch_size = 128),  # todo
		batch_iterator_test = BatchIterator(batch_size = 128),

		train_split = TrainSplit(eval_size = 0.1),
	)
	net.initialize()

	return net


