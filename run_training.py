import os
import sys
import math
import time
import matplotlib.pyplot as plt

from liblibra_core import *
from libra_py import units as units
import libra_py.workflows.nbra.ann as ann

import ham


rnd = Random()


#==================== GAPs training =====================

params = { "input_files_prefix":"e01", "ann_arch":[10,10] , "mode1":0, "mode2":1   }

ann_params = { "num_epochs":25, 
               "steps_per_epoch":100, 
               "error_collect_frequency":1,
               "epoch_size":250, 
               "learning_method":2,
               "learning_rate":0.001,
               "weight_decay_lambda":0.000,
               "etha":1.0,
               "momentum_term": 0.75,
               "verbosity":1,
               "a_plus":1.1, "a_minus":0.75,
               "dB_min":0.000001, "dB_max":10.1,
               "dW_min":0.000001, "dW_max":10.1,
             }

ann.step2_workflow(params, ann_params, rnd, plt)


#================== NACs training ===============

params = { "input_files_prefix":"nac01", "ann_arch":[10,10] , "mode1":0, "mode2":1   }

ann_params = { "num_epochs":25, 
               "steps_per_epoch":100, 
               "error_collect_frequency":1,
               "epoch_size":250, 
               "learning_method":2,
               "learning_rate":0.001,
               "weight_decay_lambda":0.000,
               "etha":1.0,
               "momentum_term": 0.75,
               "verbosity":1,
               "a_plus":1.1, "a_minus":0.75,
               "dB_min":0.000001, "dB_max":10.1,
               "dW_min":0.000001, "dW_max":10.1,
             }

ann.step2_workflow(params, ann_params, rnd, plt)
