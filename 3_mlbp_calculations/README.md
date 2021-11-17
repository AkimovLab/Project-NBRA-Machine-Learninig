# Content:  atomistic problem, ML-BP

   - res_mb_sp : the vibronic Hamiltonian and time-overlaps data from 
     [here](https://github.com/AkimovLab/Project_ML-BP/tree/main/4_analysis/pbe_plus_u/divac1)

   - `2state_model.tar.bz2` - the dynamics with 2 states

   - `5state_model.tar.bz2` - the dynamics with 5 states


# How to run the jobs (exemplified with the 5-state calculations  set)

1. First, unpack the atomistic-derived vibronic Hamiltonians data:


        tar -xjf res_mb_sp.tar.bz2


2. Prepare the data for the ANN training from the available files:


        cd 5state_model

        python run_datagen.py


3. Train the NAC and band gap ANNs:

        cd 5state_model/training1
        cp ../*.MATRIX .
        cp ../*.json
        python run_training.py > training.out

   the last instruction can be run via SLURM - uncomment the `#python run_training.py > training.out` line and

        sbatch submit.slm


4. Change the naming of the computed ANN files, if needed (e.g. if you use the default prefixes in the training step):

        python copy_files.py


5. Compute the dynamics:

  5.1. Compute the direct dynamics:

   * in the `run_namd.py` set the last lines to:

        main("direct", what)
        #main("ann", what)

   * submit the calculations:

        python run_namd.py > namd_regular.out

      or uncomment the line `#python run_namd.py > namd_regular.out` and submit via SLURM
 
        sbatch submit.slm

  5.2. Compute the ANN dynamics:

   * in the `run_namd.py` set the last lines to:

        #main("direct", what)
        main("ann", what)

   * submit the calculations:

        python run_namd.py > namd_ann.out

      or uncomment the line `#python run_namd.py > namd_ann.out` and submit via SLURM
 
        sbatch submit.slm


  5.3. Compute the long-time dynamics with the ANN:

   * in the `run_namd.py` set the last lines to:

        #main("direct", what)
        main("ann", what)

   * submit the calculations:

        python run_namd_long.py > namd_ann_long.out

      or uncomment the line `#python run_namd_long.py > namd_ann_long.out` and submit via SLURM
 
        sbatch submit.slm


6. Compute the fits and the timescales, do the plotting:

   * Edit the file `do_plots.py` as needed

   * Compute the plots (very fast):

        python do_plots.py
 

