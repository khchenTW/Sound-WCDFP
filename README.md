# Evaluating WCDFP with Sound Analyses

This repository is used to reproduce the evaluation from

_Critical Instant for Worst-Case Deadline Failure Probability: Refuted and Revisited_

for RTSS 2022 submission. This document is explaining how to use the artifact to repeat the experiments presented in the paper, i.e., Section VI. Please cite the above paper when reporting, reproducing or extending the results.

The rest of the document is organized as follows:
1. [Environment Setup](#environment-setup)
2. [How to deploy](#how-to-deploy)
3. [How to run the experiments](#how-to-run-the-experiments)
4. [Overview of the corresponding functions](#overview-of-the-corresponding-functions)
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
Note that Python 3.10 might not require all dependncies listed above.

## File Structure
    .
    ├── algorithms              # Resource packages
    │   ├── chernoff.py         # Optimized Chernoff Bound approach
    │   ├── task_convolution.py # Convlution methods
    │   └── TDA.py              # Time-demand analysis routines	
    ├── evaluations             # Evaluation scripts
    ├── plots                   # Plotter and Plots 
    ├── results                 # Results of Evaluations
    ├── task_generator          # Taskset Generator
    ├── tasksets                # Generated Tasksets
    └── README.md

## How to deploy

First, clone the git repository or download the [zip file](https://github.com/khchenTW/Sound-WCDFP/archive/refs/heads/main.zip):
```
git clone https://github.com/khchenTW/Sound-WCDFP.git
```

Switch to each subfolder and change the permission of the shell scripts to be executable as follows:

```
cd Sound-WCDFP/task_generator
chmod 777 generate.sh
cd ..

cd Sound-WCDFP/evaluations
chmod 777 evaluate.sh
cd ..

cd Sound-WCDFP/plots
chmod 777 plot.sh
cd ..
```

## How to run the experiments

The following steps explain how to repeat the evaluation of the paper on a common platform. Please note that, the number of tasksets is set to 20 to have a quick test. The evaluation in the paper set s as 100. 

### Synthesize Tasksets:

First, synthesize tasksets for analysis.
```
cd Sound-WCDFP/task_generator
./generate.sh
```
Once the tasksets are successfully generated, you can find quite a few ```*.npy``` files are generated in the folder ```tasksets``` for further usage.

### Applying the proposed analyses:

Second, apply the proposed analyses on the generated tasksets.
```
cd Sound-WCDFP/evaluations
./evaluate.sh
```
As a reference, we utilize a machine running Archlinux 5.17.3-arch1-1 x86_64 GNU/Linux,with i7-10610U CPU and 16 GB main memory. It takes about xxx seconds with this machine to obtain these figures, when set ```num_processes = 2``` in ```main.py```.

### Plotting the figures
```
cd Sound-WCDFP/plots
./plot.sh
```
You can find the plotted figures in the same folder ```plots```. 

| Paper figure    | Plot in plots            |
|-----------------|--------------------------|
| Fig. 6          |                          |
| Fig. 7          |                          |
| Fig. 8          |                          |
| Fig. 9          |                          |
| Fig. 10         |                          |
| Fig. 11         |                          |

## Overview of the corresponding functions

The following tables describe the mapping between content of our paper and the source code in this repository.

**Section 4** (Safe Bounds for WCDFP and WCRTEP):
On Paper | Source code 
--- | --- 
Corollary 12 | rtc_cb.wcrt_analysis_single()
Corollary 15 | our_analysis.wcrt_analysis_single()

## Miscellaneous

### Authors

* Kuan-Hsun Chen (University of Twente)
* Mario Günzel (TU Dortmund University)
* Niklas Ueter (TU Dortmund University)
* Georg von der Brüggen (TU Dortmund University)
* Jian-Jia Chen (TU Dortmund University)

Note that Kuan-Hsun Chen and Mario Günzel both contributed equally.

### Acknowledgments

This work has been supported by Deutsche Forschungsgemeinschaft (DFG), as part of Sus-Aware (Project No.398602212). This result is part of a project (PropRT) that has received funding from the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation programme (grant agreement No. 865170).

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
