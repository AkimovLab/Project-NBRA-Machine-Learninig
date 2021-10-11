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



def nice_plot_data(_plt, x, y, x_label, y_label, fig_name, fig_label, clr):

    figure = _plt.figure(num=None, figsize=(3.21, 2.41), dpi=300, edgecolor='black', frameon=True)        
    _plt.title(F"{fig_label}",fontsize=9.5)
    _plt.legend(fontsize=6.75, ncol=1, loc='upper left')
    _plt.xlabel(x_label,fontsize=10)
    _plt.ylabel(y_label,fontsize=10)
    _plt.plot(x, y, color=clr)
    _plt.tight_layout()
    _plt.savefig(fig_name, dpi=300)
    _plt.show() 



#=============== Data gen ================
nsteps = 5001
t, E01, NAC01 = ham.create_Hvib2(nsteps)

nice_plot_data(plt, t * units.au2fs, E01, "Time, fs", "Energy gap, a.u.", "e01-t.png", "Energy", "red")
nice_plot_data(plt, t * units.au2fs, NAC01, "Time, fs", "NAC a.u.", "nac01-t.png", "NAC", "green")



#================ Gaps ====================
params = { "dt": 1.0, "wspan":500.0, "dw":1.0, "do_output":False, "do_center":True, 
           "acf_type":1, "data_type":0, 
           "leading_w_fraction":0.0001,  "deriv_scaling":50.0,
           "tau":[1000, 3000, 5000.0], "training_steps":list(range(0,5000)),
           "output_files_prefix":"e01"    
         }
ann.step1_workflow(E01, params, plt)


#================= NACs =====================

params = { "dt": 1.0, "wspan":500.0, "dw":1.0, "do_output":False, "do_center":True, 
           "acf_type":1, "data_type":0, 
           "leading_w_fraction":0.0001,  "deriv_scaling":50.0,
           "tau":[1000, 3000, 5000.0], "training_steps":list(range(0,5000)),
           "output_files_prefix":"nac01"    
         }

ann.step1_workflow(NAC01, params, plt)

