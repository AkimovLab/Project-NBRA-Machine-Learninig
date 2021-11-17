import os
import sys
import math
import time

import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt

from liblibra_core import *
import util.libutil as comn
from libra_py import units as units
from libra_py import data_conv, data_stat, data_outs, data_read
import libra_py.workflows.nbra.decoherence_times as decoherence_times
import libra_py.workflows.nbra.step4 as step4
import libra_py.workflows.nbra.ann as ann

import ham


def compute_model(q, params, full_id):
    model = params["model"]
    res = None    

    if model==1:        
        pass
    elif model==2:
        res = ham.compute_model_nbra_2state_direct(q, params, full_id)        
    elif model==3:
        res = ann.compute_model_nbra_ann(q, params, full_id)
    return res



def main(case, what):

    

    if case=="direct" and what in [0, 2] :
        os.system("mkdir namd_regular")
    elif case=="ann" and what in [0, 2]:
        os.system("mkdir namd_ann")


    nthreads = 4
    methods = {0:"FSSH", 1:"IDA", 2:"mSDM", 3:"DISH", 21:"mSDM2", 31:"DISH2" }
    init_states = [1]
    tsh_methods = [0]
    batches = list(range(4))

   
    


    #================== SET UP THE DYNAMICS AND DISTRIBUTED COMPUTING SCHEME  ===============                      

    rnd = Random()   

    rates = None
    gaps = None
    
    params_common = { "nsteps":2000, "dt":1.0*units.fs2au, 
                      "ntraj":100, "x0":[-4.0], "p0":[4.0], "masses":[2000.0], "k":[0.01],                  
                      "nstates":2, "istate":[1, 0],
                      "which_adi_states":range(2), "which_dia_states":range(2),
                      "rep_ham":1, "tsh_method":0, "force_method":0, "nac_update_method":0,
                      "hop_acceptance_algo":31, "momenta_rescaling_algo":0,
                      "time_overlap_method":1, "mem_output_level":-1,  "txt_output_level":4,
                      "properties_to_save": ['timestep', 'time', 'SH_pop', 'SH_pop_raw'],
                      "state_tracking_algo":0, "convergence":0,  "max_number_attempts":100, 
                      "min_probability_reordering":0.01, "decoherence_algo":0, "Temperature": 300.0                    
                    }


    #=========================== DIRECT ==============================

    if case == "direct":

        model_params_direct = {"model":2, "nstates":2, "filename":None, "istep":0 }
        print(model_params_direct)

        dyn_params = dict(params_common)
        dyn_params.update({ "dir_prefix":"namd_regular" })

       
        if what in [0, 2]:
            step4.namd_workflow(dyn_params, compute_model, model_params_direct, rnd, nthreads, 
                                methods, init_states, tsh_methods, batches, "fork", True)

        if what in [1, 2]:
            step4.nice_plots(dyn_params, init_states, tsh_methods, methods, batches, fig_label="Direct NA-MD")

    #=========================== ANN =================================

    elif case == "ann":

        model_params_ann = {"model":3, "nstates":2, "filename":None, "istep":0, "dt":1.0*units.fs2au, "timestep":0 }    
        ann.load_ann_and_parameters(model_params_ann, nstates=2, prefix="./")    
        print(model_params_ann)

        dyn_params = dict(params_common)
        dyn_params.update({ "dir_prefix":"namd_ann" })


        if what in [0, 2]:
            step4.namd_workflow(dyn_params, compute_model, model_params_ann, rnd, nthreads, 
                                methods, init_states, tsh_methods, batches, "fork", True)
    
        if what in [1, 2]:
            step4.nice_plots(dyn_params, init_states, tsh_methods, methods, batches, fig_label="Ann NA-MD")



what = 2
main("direct", what)
main("ann", what)


