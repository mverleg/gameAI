



net0 = NeuralNet(
	layers=layers0,

	input_shape=(None, num_features),
	dense0_num_units=200,
	dropout_p=0.5,
	dense1_num_units=200,
	output_num_units=num_classes,
	output_nonlinearity=softmax,

	update=nesterov_momentum,
	update_learning_rate=0.01,
	update_momentum=0.9,

	eval_size=0.2,
	verbose=1,
	max_epochs=20)

