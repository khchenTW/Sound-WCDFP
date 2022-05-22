# Evaluating Chernoff Bound with new safe bounds

This repository is used to reproduce the evaluation from

_Critical Instant for Worst-Case Deadline Failure Probability: Refuted and Revisited_

for RTSS 2022. This document is explaining how to use the artifact to repeat the experiments presented in the paper, i.e., Section VI. Please cite the above paper when reporting, reproducing or extending the results.

The rest of the document is organized as follows:
1. [Environment Setup](#environment-setup)
2. [How to run the experiments](#how-to-run-the-experiments)
3. [Overview of the corresponding functions](#overview-of-the-corresponding-functions)
4. [Miscellaneous](#miscellaneous)

## Environment Setup
### Requirements

Some common software should be installed:
```
sudo apt-get install software-properties-common git python3.10
```
If the installation of Python3.10 doesn't work, likely you need to add deadsnakes PPA beforehand as it is not available on universe repo:
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
```

To run the experiments Python 3.10 is required (another version of Python 3 might also work). Moreover, the following packages are required:
```
getopt
math
matplotlib
multiprocessing
numpy
scipy
sympy
os
pickle
random
statistics
sys
```

Assuming that Python 3.10 is installed in the targeted machine, to install the required packages:
```
pip3 install matplotlib numpy scipy sympy
```
or
```
python3.10 -m pip install matplotlib numpy scipy sympy
```
In case any dependent packages are missing, please install them accordingly. 

According to the feedback of one reviewer, Python 3.10 might not require all dependncies listed above.

## File Structure
    .
    ├── algorithms              # Resource packages
    │   ├── chernoff.py         # DATE'19 Optimized Chernoff Bound approach
    │   ├── task_convolution.py # ECRTS'18 Task-level convlution methods
    │   └── TDA.py              # Time-demand analysis routines	
    ├── evaluations             # Evaluation scripts
    ├── plots                   # Plotter and Plots 
    ├── results                 # Results of Evaluations
    ├── task_generator          # Taskset Generator
    ├── tasksets                # Generated Tasksets
    └── README.md

### Deployment (Need to Update)

The following steps explain how to deploy this framework on a common PC:

First, clone the git repository or download the [zip file]():
```
git clone https://github.com/kuanhsunchen/SafeCB.git
```
Move into the extracted/cloned folder, change the permissions of the script to be executable, and generate tasksets:
```
cd SafeCB/task_generator
chmod 777 generate.sh
./generate.sh
```

execute:
```
cd SafeCB/evaluations
chmod 777 evaluate.sh
./evaluate.sh
```
and plot:
```
cd SafeCB/plots
chmod 777 plot.sh
./plot.sh
```
## How to run the experiments  (Need to Update)

- To reproduce the figures in the paper, ```./evaluate.sh``` should be executed.
- The plotted figures can be found in the folder plots.

As a reference, we utilize a machine running Archlinux 5.17.3-arch1-1 x86_64 GNU/Linux,with i7-10610U CPU and 16 GB main memory. 

## Miscellaneous

### Authors

* Kuan-Hsun Chen (University of Twente)
* Mario Günzel (TU Dortmund University)
* Niklas Ueter (TU Dortmund University)
* ‪Georg von der Brüggen (TU Dortmund University)
* Jian-Jia Chen (TU Dortmund University)

### Acknowledgments

This work has been supported by European Research Council (ERC) Consolidator Award 2019, as part of PropRT (Number 865170), and by Deutsche Forschungsgemeinschaft (DFG), as part of Sus-Aware (Project no. 398602212).

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
