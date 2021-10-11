# Machine_Learning_Libra

To run the project, do the following:

1. Define the Hamiltonian in the `ham.py` file

2. Generate the data using `run_datagen.py` file

    It generates:

    - `e01-t.png` - energy gap vs. time
    - `e01-acf-ifs.png` - ACF and Influence spectrum plots
    - `e01-meta.json` - the descriptive analysis of the data - the leading frequencies, etc.
    - `e01-traininig-input.MATRIX` - a binary file containinig all the input patters 
       for the traininig as generated by the Hamiltonian used
    - `e01-traininig-target.MATRIX` - a binary file containinig all the expected outputs for the
       input patters considered 

    - for other gaps, the prefixes are `e12`, `e23`, etc.

    - analogous files are generated for NACs, they start with `nac01`, `nac02`,... `nac12`, ...


3. Train the ANNs using `run_training.py` file

    It generates:

    - `e01-ann.xml` - trained ANN
    - `e01-ann-error.png` - error vs. epoch number
    - `e01-ann-training.png` - predicted property vs. time and predicted property vs 2 of the modes

    - for other gaps, the prefixes are `e12`, `e23`, etc.

    - analogous files are generated for NACs, they start with `nac01`, `nac02`,... `nac12`, ...
     

4. Do the NAMD using `run_namd.py` file

    - First make sure you have created empty folders 
     `namd_ann` and `namd_regular` - the results of NA-MD calculations will be stored in those 
      directories.


    
