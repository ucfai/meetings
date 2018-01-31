import tensorflow as tf
import numpy as np
import colorlover as cl

import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go

SEED = 42
learning_rate = 0.02


class NeuralNetwork():
    LR = 0
    max_n = 0
    n_lyr = 0
    colors = None

    def __init__(self, kwargs):
        def __valid_args(args):
            def __key_type_errors(key, args, arg_type):
                if not (key in args):
                    raise KeyError("`{}` were an unspecifed argument. We can't make the Neural Network without it.".format(key))
                else:
                    raise TypeError("`{0}` must be {1}; you gave {2}".format(key, arg_type, type(args[key])))

            if "nodes" in args and type(args["nodes"]) == np.ndarray:
                self.nodes = args["nodes"].flatten()
                NeuralNetwork.n_lyr = self.nodes.shape[0]
                self.n_inp = self.nodes[0]
                self.n_hid = self.nodes[1:-1]
                self.n_out = self.nodes[-1]
                NeuralNetwork.max_n = self.nodes.max()
                NeuralNetwork.colors = cl.scales[str(NeuralNetwork.n_lyr)]["qual"]["Dark2"]
            else:
                __key_type_errors("nodes", args, np.ndarray)

            if "inp" in args and type(args["inp"]) == np.ndarray:
                self.input = args["inp"].flatten()
            else:
                __key_type_errors("inp", args, np.ndarray)

            if "out" in args and type(args["out"]) == np.ndarray:
                self.input = args["out"]
            else:
                __key_type_errors("out", args, np.ndarray)

            if "LR" in args and type(args["LR"]) == float:
                NeuralNetwork.LR = args["LR"]
            else:
                __key_type_errors("LR", args, float)

            self.graphing = args["graphing"] if "graphing" in args else False

        def __build_nets():
            self.layers  = [Layer(self.nodes[0], self.nodes[1], "input", 0)]
            self.layers += [Layer(self.nodes[x], self.nodes[x + 1], "hidden{}".format(x), x) for x in range(1, self.n_hid.shape[0] + 1)]
            self.layers += [Layer(self.nodes[-1], None, "output", len(self.layers))]
            Layer.count = len(self.layers)

            self.fwd_layers = [(self.layers[x - 1], l1) for x, l1 in enumerate(self.layers[ 1:])]
            self.bkp_layers = [(l1, self.layers[x + 1]) for x, l1 in enumerate(self.layers[:-1])][::-1]


        __valid_args(kwargs)
        __build_nets()


    def train(self, out):
        for l_prv, l_now in self.fwd_layers:
            l_now.run_weights(self.inp if l_now.name == "input" else l_prv.out_sig)
            l_now.run_sigmoid()

        for l_now, l_nxt in self.bkp_layers:
            l_now.run_loss(l_nxt.out_sig if l_nxt.name != "output" else out)
        pass


    def query(self, inp):
        pass


    def backquery(self):
        pass

    def graph(self):
        if self.graphing:
            def __connect(x1, x2):
                x = np.array([ np.array([
                    [x1.x[n1], x2.x[n2], None] for n2 in range(x2.n)
                ]) for n1 in range(x1.n)])

                y = np.array([ np.array([
                    [x1.y[n1], x2.y[n2], None] for n2 in range(x2.n)
                ]) for n1 in range(x1.n)])

                return x, y

            def __paint_lines(x, y, color):
                return [go.Scatter(
                            x=x[_], y=y[_],
                            line=dict(color=color),
                            showlegend=False,
                            ) for _ in range(len(x))]

            self.scatter_layers = [layer.graph() for layer in self.layers]
            self.scatter_lines = []
            for (x1, x2) in self.bkp_layers[::-1]:
                x, y = __connect(x1, x2)
                self.scatter_lines += __paint_lines(x, y, NeuralNetwork.colors[x1.at])

            print(self.scatter_lines + self.scatter_layers)

            return self.scatter_lines + self.scatter_layers
        else:
            raise Exception("You specified that we *_shouldn't_* be graphing the Neural Network. Please alter your input dictionary.")



class Layer:
    count = 0

    def __init__(self, n, np1, name, at):
        self.at  = at
        self.n   = n
        self.np1 = np1
        self.name = name
        if self.name != "output":
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
            self.update = NeuralNetwork.LR * tf.matmul(self.error * self.__sigdx(self.out_sig), self.out_sig.T)
            self.weights += self.update
        else:
            self.error = tf.matmul(self.weights.T, target)
            self.update = NeuralNetwork.LR * tf.matmul(self.error * self.__sigdx(self.out_sig), self.out_sig.T)
            self.weights += self.update

    def graph(self):
        self.x = [self.at for _ in range(0, self.n)]
        start = (NeuralNetwork.max_n - self.n) / 2
        self.y = [y for y in np.arange(start, start + self.n, 1)]
        self.plotted = go.Scatter(dict(
            name = self.name,
            mode = "markers",
            marker = dict(
                size  = 40,
                line  = dict(width = 2),
                color = NeuralNetwork.colors[self.at]
            ),
            x = self.x,
            y = self.y,
        ))
        return self.plotted
