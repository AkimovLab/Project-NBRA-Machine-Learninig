import os
import sys
import math
import time
import numpy as np
from liblibra_core import *
from libra_py import units as units


def H00(step, istep):
    return 0.0

def H11(step, istep):    
    dt = 1.0 * units.fs2au
    t = (istep + step) * dt
    
    w11 = 100*units.wavn2au
    w12 = 125*units.wavn2au
    w13 = 50*units.wavn2au
                
    # Energy gap
    de01 = (1.2 + 0.02 * math.sin(w11*t) + 0.032 * math.sin(w12*t) - 0.01 * math.sin(w13*t) ) * 0.1
        
    return de01


def H01(step, istep):  
    
    dt = 1.0 * units.fs2au
    t = (istep + step) * dt
    
    w21 = 200*units.wavn2au
    w22 = 225*units.wavn2au
    w23 = 375*units.wavn2au
    w24 = 1175*units.wavn2au
    
    de01 = H11(step, istep)        
        
    # NACs
    nac01 = 0.2 * math.sin(w21*t) + 0.12 * math.sin(w22*t) - 0.1 * math.sin(w23*t) + 0.01 * math.sin(w24*t) 
    nac01 = 0.005 * nac01/de01
        
    
    return nac01

    
def create_Hvib2(nsteps, istep=0):
    """
    Model 2-state Hamiltonian
    
    """            
    times = np.zeros(nsteps) # time in a.u.
    de01 = np.zeros(nsteps)  # energy gap in a.u.
    nac01 = np.zeros(nsteps) # NACs in a.u. 
    
    dt = 1.0 * units.fs2au
       
    for step in range(nsteps):
        t = (istep + step) * dt
        
        # Time
        times[step] = t 
        
        # Energy gap
        de01[step] = H11(step, istep)
        
        # NACs
        nac01[step] = H01(step, istep)
            
    return times, de01, nac01



class tmp:
    pass

def compute_model_nbra_2state_direct(q, params, full_id):
    """   
    Read in the vibronic Hamiltonians along the trajectories    

    Args: 
        q ( MATRIX(1,1) ): coordinates of the particle, ndof, but they do not really affect anything
        params ( dictionary ): model parameters

            * **params["timestep"]** ( int ):  [ index of the file to read ]
            * **params["prefix"]**   ( string ):  [ the directory where the hdf5 file is located ]
            * **params["filename"]** ( string ):  [ the name of the HDF5 file ]
        
    Returns:       
        PyObject: obj, with the members:

            * obj.hvib_adi ( CMATRIX(n,n) ): adiabatic vibronic Hamiltonian 
            
    """
                                    
    hvib_adi, basis_transform, time_overlap_adi = None, None, None
  
    Id = Cpp2Py(full_id)
    indx = Id[-1]    
    timestep = params["timestep"]
    istep = params["istep"]
    nadi = 2 # params["nstates"]
        
    #============ Electronic Hamiltonian =========== 
    ham_adi = CMATRIX(2,2)
    h11 = H11(timestep, istep)
    ham_adi.set(1,1,  h11 * (1.0+0.0j) )     
    
    #============ NAC ===========        
    nac_adi = CMATRIX(2,2)    
    nac = H01(timestep, istep)
    nac_adi.set(0,1, nac * (1.0+0.0j) )    
    nac_adi.set(1,0,-nac * (1.0+0.0j) )       
    
    #============ Vibronic Hamiltonian ===========        
    hvib_adi = CMATRIX(2, 2)
    hvib_adi = ham_adi - 1j * nac_adi
        
    #=========== Basis transform, if available =====
    basis_transform = CMATRIX(2, 2)            
    basis_transform.identity()        
                                                
    #========= Time-overlap matrices ===================
    time_overlap_adi = CMATRIX(2, 2)            
    time_overlap_adi.identity()    
    
    
    obj = tmp()
    obj.ham_adi = ham_adi
    obj.nac_adi = nac_adi
    obj.hvib_adi = hvib_adi
    obj.basis_transform = basis_transform
    obj.time_overlap_adi = time_overlap_adi
            
    return obj


