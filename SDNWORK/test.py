import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
	
def zc_read_csv(n,m):
    zc_dataframe = pd.read_csv("./data.csv", sep=",")
    x = np.array([[0,0,0,0,0,0,0,0,0,0]])
    y = np.array([[0,0]])
    listy = [0,0]
    flag = 0
    for i in zc_dataframe.index:
        zc_row = zc_dataframe.loc[n+i]
        private = np.array([(zc_row)],float)
	listy[0] = zc_row[8]
	listy[1] = zc_row[9]
	private_y = np.array([(listy)],float)
        x = np.concatenate((x,private),axis=0)
	y = np.concatenate((y,private_y),axis=0)
	flag += 1 
	if(flag ==m):
		break;
    y=y[1:,:]
    x=x[1:,:-2]
    return (x,y)

def RNN(X, weights, biases):
    X_in = tf.matmul(X, weights['in'] + biases['in'])
    X_in = tf.reshape(X_in, [-1, n_steps, n_hidden_units])
    lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(n_hidden_units, forget_bias=1.0, state_is_tuple=True)
    _init_state = lstm_cell.zero_state(batch_size, dtype=tf.float32)
    outputs, states = tf.nn.dynamic_rnn(lstm_cell, X_in, initial_state=_init_state, time_major=False)
    results = tf.matmul(states[1], weights['out']) + biases['out']
    return results	

lr = 0.0001
training_iters = 2048
batch_size = 128
n_inputs = 8 
n_steps = 1
n_hidden_units = 128 
n_classes = 2


w = {
    'in': tf.Variable(tf.random_normal([n_inputs, n_hidden_units])),
    'out': tf.Variable(tf.random_normal([n_hidden_units, n_classes]))
}

b = {
    'in': tf.Variable(tf.constant(0.1, shape=[n_hidden_units, ])),
    'out': tf.Variable(tf.constant(0.1, shape=[n_classes]))
}


X=tf.placeholder(tf.float32,name='X',shape=[None,n_inputs])
Y=tf.placeholder(tf.float32,name='Y',shape=[None,n_classes])
pred=tf.placeholder(tf.float32,name='pred',shape=[None,n_classes])
pred = RNN(X, w, b)
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=Y))
train_op = tf.train.AdamOptimizer(lr).minimize(cost)
correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(Y, 1)) 
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

total = []
saver = tf.train.Saver()

init_op = tf.global_variables_initializer()

with tf.Session() as sess:
	step = 0
	while step * batch_size < training_iters:
		X_test,Y_test =zc_read_csv(step * batch_size,128)
		sess.run(tf.global_variables_initializer())
        	saver.restore(sess, "./model/model")
		total.append(sess.run(accuracy,feed_dict={X: X_test,Y:Y_test}))
		step +=1
plt.plot(total)
plt.show()
