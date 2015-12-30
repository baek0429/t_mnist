import tensorflow as tf
import input_data

# get data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

# place holder, later filled with values
x = tf.placeholder(tf.float32,[None,784])

# weight 
W = tf.Variable([784,10]) 
# y: predicted probablity distribution. 0~9
y = tf.Variable([10]) 
y = tf.nn.softmax(tf.matmul(x,W)+b)

# y_ is true distribution, later calculated.
y_ = tf.placeholder(tf.float32,[None,10])
# minimize cross_entropy.
cross_entropy = -tf.reduce_sum(y_*tf.log(y))

# using Wackpropagation algorithm (tensorflow library)
# TensorFlow to minimize cross_entropy using 
# the gradient descent algorithm with a learning rate of 0.01.
# it moves toward the optimized point to minimize cross_entropy with rate of 0.01
# other optimzation tools : https://www.tensorflow.org/versions/master/api_docs/python/train.html#optimizers
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

# initialize.
init = tf.initialize_all_variables()

# set session. and run.
sess = tf.Session()
sess.run(init)

# get 100 radom smaple(batch) and train 1000 times. => stochastic gradient.
for i in range(1000):
	batch_xs, batch_ys = mnist.train.next_batch(100)
	sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

# see how well the model fits ideal.  91%
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))

