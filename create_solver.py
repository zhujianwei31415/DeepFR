#! /usr/bin/env python
#
# Copyright
# Author: zhujianwei@ict.ac.cn (Jianwei Zhu)
import sys

caffe_root = '/home/zhujianwei/workspace/caffe_zjw/'
sys.path.insert(0, caffe_root + 'python')
import caffe
from caffe.proto import caffe_pb2

def solver(caffenet, prefix):
    s = caffe_pb2.SolverParameter()

    # Set a seed for reproducible experiments: this controls for randomization in training.
    #s.random_seed = 0xCAFFE

    # Specify locations of the train and (maybe) test networks.
    s.net = caffenet

    # Test after every 1000 training iterations.
    s.test_interval = 1000
    
    # Test on 1000 batches each time we test.
    s.test_iter.append(1000)

    # EDIT HERE to try different solvers: "SGD", "Adam", and "Nesterov" among others.
    #s.type = "SGD"

    # Set the initial learning rate for SGD. EDIT HERE to try different learning rates
    s.base_lr = 0.01
    
    # Set momentum to accelerate learning by taking weighted average of current and previous updates.
    s.momentum = 0.9
    
    # Set weight decay to regularize and prevent overfitting
    s.weight_decay = 5e-4

    # Set `lr_policy` to define how the learning rate changes during training.
    s.lr_policy = 'step'
    # EDIT HERE to try the fixed rate (and compare with adaptive solvers) `fixed` is the simplest policy that keeps the learning rate constant.
    # s.lr_policy = 'fixed'

    # drop the learning rate by a factor of 10 (i.e., multiply it by a factor of gamma = 0.1)
    s.gamma = 0.1
    
    # drop the learning rate every 100K iterations
    s.stepsize=100000

    # no. of times to update the net (training iterations)
    s.max_iter = 450000

    # Display the current training loss and accuracy every 1000 iterations.
    s.display = 20

    # Snapshots are files used to store networks we've trained. We'll snapshot every 10K iterations -- twice during training.
    s.snapshot = 10000
    
    # File path prefix for snapshotting model weights and solver state.
    # Note: this is relative to the invocation of the `caffe` utility, not the solver definition file.
    s.snapshot_prefix = prefix

    # Train on the GPU
    s.solver_mode = caffe_pb2.SolverParameter.GPU
    
    return str(s)

if __name__ == '__main__':
    solver_str = solver('train_test.prototxt', 'caffe_alexnet_train')

    with open('solver.prototxt', 'w') as f:
        f.write(solver_str)
        print(f.name)
