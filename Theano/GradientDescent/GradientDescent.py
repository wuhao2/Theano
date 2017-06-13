# -*- coding:utf-8 -*-
import numpy as np

import random

from theano.tensor.nnet import sigmoid


class NetWork(object):

    def __init__(self,sizes):#sizes: 每层神经元的个数, 例如: 第一层2个神经元,第二层3个神经元:
        self.num_layers = len(sizes) #返回层数
        self.sizes = sizes
        self.biases = [np.random.rand(y,1) for y in sizes[1:]]#从高斯分布中随机产生一个数，老初始化偏向b
        self.weights = [np.random.rand(y,x) for x, y in zip(sizes[:-1], sizes[1:])]
        # sizes = [2,3,1]
        # print (sizes[1:])
        # print x,y   #用于调试
        # np.random.rand(y, 1): 随机从正态分布(均值0, 方差1)中生成
        # net.weights[1] 存储连接第二层和第三层的权重 (Python索引从0开始数)

    def feedforward(self, a):
        """Return the output of the network if "a" is input."""
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b) #求内积
        return a

net = NetWork([2,3,1]) #表示输入层神经元个数为2，隐藏层神经元个数为3，输出层个数为1
print "layers:", net.num_layers
print "neure counts per layer:", net.sizes
print "bias:", net.biases
print "***********************************************"
print "weights:", net.weights


def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
    """
    Train the neural network using mini-batch stochastic
    gradient descent.  The "training_data" is a list of tuples
    "(x, y)" representing the training inputs and the desired
    outputs.  The other non-optional parameters are
    self-explanatory.  If "test_data" is provided then the
    network will be evaluated against the test data after each
    epoch, and partial progress printed out.  This is useful for
    tracking progress, but slows things down substantially.
    """
    if test_data:
        n_test = len(test_data)
    n = len(training_data) #训练实例的个数

    for j in xrange(epochs):
        random.shuffle(training_data) #随机shuffle洗牌打乱图片顺序
        mini_batches = [
            training_data[k:k + mini_batch_size]
            for k in xrange(0, n, mini_batch_size)] #0,100,200,......900循环 ; #将5000个训练数据，按照mini_batch取出

        for mini_batch in mini_batches:
            self.update_mini_batch(mini_batch, eta) #更新w , b

        if test_data:
            print "Epoch {0}: {1} / {2}".format(
                j, self.evaluate(test_data), n_test) #格式化打印，第几轮: 准确率
        else:
            print "Epoch {0} complete".format(j)


def update_mini_batch(self, mini_batch, eta):
    """
    Update the network's weights and biases by applying
    gradient descent using backpropagation to a single mini batch.
    The "mini_batch" is a list of tuples "(x, y)", and "eta"is the learning rate.
    """
    nabla_b = [np.zeros(b.shape) for b in self.biases]
    nabla_w = [np.zeros(w.shape) for w in self.weights]

    for x, y in mini_batch:
        delta_nabla_b, delta_nabla_w = self.backprop(x, y) #
        nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
        nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
    self.weights = [w - (eta / len(mini_batch)) * nw
                    for w, nw in zip(self.weights, nabla_w)]
    self.biases = [b - (eta / len(mini_batch)) * nb
                   for b, nb in zip(self.biases, nabla_b)]



    def backprop(self, x, y):
        """Return a tuple ``(nabla_b, nabla_w)`` representing the
        gradient for the cost function C_x.  ``nabla_b`` and
        ``nabla_w`` are layer-by-layer lists of numpy arrays, similar
        to ``self.biases`` and ``self.weights``."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # feedforward
        activation = x
        activations = [x] # list to store all the activations, layer by layer
        zs = [] # list to store all the z vectors, layer by layer
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation)+b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # backward pass
        delta = self.cost_derivative(activations[-1], y) * \
            sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        # Note that the variable l in the loop below is used a little
        # differently to the notation in Chapter 2 of the book.  Here,
        # l = 1 means the last layer of neurons, l = 2 is the
        # second-last layer, and so on.  It's a renumbering of the
        # scheme in the book, used here to take advantage of the fact
        # that Python can use negative indices in lists.
        for l in xrange(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return (nabla_b, nabla_w)

    #### Miscellaneous functions
    def sigmoid(z):
        """The sigmoid function."""
        return 1.0 / (1.0 + np.exp(-z))

    def sigmoid_prime(z):
        """Derivative of the sigmoid function."""
        return sigmoid(z) * (1 - sigmoid(z))
