import codecs
import os
import collections
from six.moves import cPickle
import numpy as np

class Args():
    def __init__(self, args=None):
        self.args = args
        self.keys = args.keys()
        
        self.data_dir = self.__loader("/data",     "data_dir")
        self.save_dir = self.__loader("/tmp/save", "save_dir")
        self.logs_dir = self.__loader("/tmp/logs", "logs_dir")
        
        for d in [self.data_dir, self.save_dir, self.logs_dir]:
            os.makedirs(d, exist_ok=True)
        
        self.rnn_size = self.__loader(128, "rnn_size")
        self.n_layers = self.__loader(  3, "n_layers")
        
        if "model" in self.args:
            assert self.args["model"] in ["rnn", "lstm", "gru", "nas"], "You specified an invalid model: `{}`".format(args["model"])
        self.model = self.__loader("lstm", "model")
        
        self.batch_size = self.__loader(50, "batch_size")
        self.seq_length = self.__loader(50, "seq_length")
        self.n_epochs   = self.__loader(50, "n_epochs")
        
        self.save_every = self.__loader(1000, "save_every")
        
        self.grad_clip = self.__loader(5., "grad_clip")
        self.lr = self.__loader(0.002, "lr")
        self.dr = self.__loader( 0.97, "dr")
        
        self.out_keep_prob = self.__loader(1., "out_keep_prob")
        self.inp_keep_prob = self.__loader(1., "inp_keep_prob")
        
        self.init_from = self.__loader(self.save_dir, "init_from")
        
        self.vocab_size = 0
        
    def __loader(self, default, key):
        return default if key not in self.keys else self.args[key]
       
    
class TextLoader():
    def __init__(self, data_dir, batch_size, seq_length, encoding='utf-8'):
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.seq_length = seq_length
        self.encoding = encoding

        file_input  = os.path.join(data_dir, "input.txt")
        file_vocab  = os.path.join(data_dir, "vocab.pkl")
        file_tensor = os.path.join(data_dir, "data.npy")

        if not (os.path.exists(file_vocab) and os.path.exists(file_tensor)):
            print("reading text file")
            self.preprocess(file_input, file_vocab, file_tensor)
        else:
            print("loading preprocessed files")
            self.load_preprocessed(file_vocab, file_tensor)
            
        self.create_batches()
        self.reset_batch_pointer()

    def preprocess(self, file_input, file_vocab, file_tensor):
        with codecs.open(file_input, "r", encoding=self.encoding) as f:
            data = f.read()
            
        counter = collections.Counter(data)
        count_pairs = sorted(counter.items(), key=lambda x: -x[1])
        
        self.chars, _ = zip(*count_pairs)
        self.vocab_size = len(self.chars)
        self.vocab = dict(zip(self.chars, range(len(self.chars))))
        
        with open(file_vocab, 'wb') as f:
            cPickle.dump(self.chars, f)
            
        self.tensor = np.array(list(map(self.vocab.get, data)))
        np.save(file_tensor, self.tensor)

    def load_preprocessed(self, file_vocab, file_tensor):
        with open(file_vocab, 'rb') as f:
            self.chars = cPickle.load(f)
            
        self.vocab_size = len(self.chars)
        self.vocab = dict(zip(self.chars, range(len(self.chars))))
        self.tensor = np.load(file_tensor)
        
        self.num_batches = int(self.tensor.size / (self.batch_size * self.seq_length))

    def create_batches(self):
        self.num_batches = int(self.tensor.size / (self.batch_size * self.seq_length))

        assert self.num_batches > 0, "Not enough data. Make `seq_length` and `batch_size` smaller."

        self.tensor = self.tensor[:self.num_batches * self.batch_size * self.seq_length]

        xdata = self.tensor
        
        ydata = np.copy(self.tensor)
        ydata[:-1] = xdata[1:]
        ydata[-1] = xdata[0]
        
        self.x_batches = np.split(xdata.reshape(self.batch_size, -1), self.num_batches, 1)
        self.y_batches = np.split(ydata.reshape(self.batch_size, -1), self.num_batches, 1)

    def next_batch(self):
        x, y = self.x_batches[self.pointer], self.y_batches[self.pointer]
        self.pointer += 1
        
        return x, y

    def reset_batch_pointer(self):
        self.pointer = 0
        
        
def pretty_print(strlen, epoch, offset, loss, start, end):
    print(("{:"+ strlen["batch"] +"}/").format(epoch * data_loader.num_batches + offset), end="")
    print(("{:"+ strlen["batch"] +"} ").format(args.num_epochs * data_loader.num_batches), end="")
    print(("{:"+ strlen["epoch"] +"},").format(epoch), end="")
    print(" loss={:3f},".format(loss), end="")
    print(" time/batch={:3f},".format(end - start))
    
    
def final_chkpt(sess, saver, save_dir, offset, n_epochs, n_batches, save_every):
    checkpoint = bool(offset % save_every == 0)
    checkpoint = checkpoint or bool((e == n_epochs - 1 and b == n_batches - 1))
    if checkpoint:
        checkpoint_path = data_dir + "shakespeare.ckpt"
        saver.save(sess, checkpoint_path, global_step=offset)
        print("Model saved to {}".format(checkpoint_path))