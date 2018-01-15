import tensorflow as tf
import numpy as np

SEED = 42
learning_rate = 0.02

layer_sizes = [4, [6, 5, 7], 4]


class NeuralNetwork():
    LR = learning_rate

    def __init__(self, nodes, graph=True):
        if type(nodes) == np.ndarray:
            nodes = nodes.flatten()
            self.n_lyr = nodes.shape[0]
            self.n_inp = nodes[0]
            self.n_hid = nodes[1:-1]
            self.n_out = nodes[-1]
        else:
            raise ValueError("Please supply a `numpy` array with your nodes, of the form...:\n  `np.array([i, [h1, h2, ..., hx], o])`")

        self.layers  = [Layer(nodes[0], nodes[1], "input")]
        self.layers += [Layer(nodes[x], nodes[x + 1], "hidden{}".format(x)) for x in xrange(1, self.n_hid)]
        self.layers  = [Layer(nodes[-2], nodes[-1], "output")]

        self.data = mnist
        pass

    def train(self):

        for layer in self.layers:
            layer.run_weights()
        pass


    def query(self):
        pass


    def backquery(self):
        pass

    class Layer:
        count = 0
        def __init__(self, n, np1, name):
            self.n   = n
            self.np1 = np1
            self.name = name
            count += 1
            with tf.name_scope(name):
                self.weights = tf.Variable(
                                tf.truncated_normal([self.n, self.np1], stddev=pow(self.np1, -0.5), seed=SEED),
                               name="weights")
                self.biases = tf.Variable(tf.zeros([self.np1]), name="biases")

        def __sigdx(self, x):
            return x * (1 - x)

        def run_weights(self, inp):
            self.out_sum = tf.matmul(inp, self.weights) + biases

        def run_sigmoid(self):
            self.out_sig = tf.nn.sigmoid(self.out_sum) if self.name != "output" else tf.nn.softmax(self.out_sum)

        def run_loss(self, target):
            if self.name == "output":
                target = tf.Variable(target, dtype=tf.float32)
                self.error = target - self.out_sig
                self.update = Network.LR * tf.matmul(self.error * self.__sigdx(self.out_sig), self.out_sig.T)
                self.weights += self.update
            else:
                self.error = tf.matmul(self.weights.T, target)
                self.update = Network.LR * tf.matmul(self.error * self.__sigdx(self.out_sig), self.out_sig.T)
                self.weights += self.update
