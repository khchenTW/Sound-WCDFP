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

To run the experiments Python 3.10 was adopted in the evaluation of the paper. Note that another version of Python 3 might also work. 

Assuming that Python 3.10 is installed in the targeted machine, to install the required packages:
```
pip3 install matplotlib numpy scipy sympy
```
or
```
python3.10 -m pip install matplotlib numpy scipy sympy
```
Note that there could be unlisted dependncies, depending on the adopted version of Python. Please install them by yourself.

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

The following steps explain how to repeat the evaluation of the paper on a common platform. 

### Synthesize Tasksets

First, synthesize tasksets for analysis.
```
cd Sound-WCDFP/task_generator
./generate.sh
```
Once the tasksets are successfully generated, you can find quite a few ```.npy``` files are generated in the folder ```tasksets``` for further usage.

### Applying the proposed analyses

Second, apply the proposed analyses on the generated tasksets.
```
cd Sound-WCDFP/evaluations
./evaluate.sh
```
In this script, we partition the experiments according to the figures in the paper. The setup of 10 sets was for quick testing and artifact evaluation.

As a reference, we employed a laptop running Archlinux 5.17.3-arch1-1 x86_64 GNU/Linux, with i7-10610U CPU and 16 GB main memory. The following table reports the time it took for each experiment, when the number of processes was set to 4 with only 10 sets per configuration:

| Paper Figure    |  Elapsed Time (avg)        |
|-----------------|----------------------------|
| Fig. 6          |  46.88s                    |
| Fig. 7          |  (a) 504.45s, (b) 144.06s  |
| Fig. 8          |  504.45s                   |
| Fig. 9          |  19.71s                    |
| Fig. 10         |  38.85s                    |
| Fig. 11         |  (a) 535.64s, (b) 4391.27s |

Please note that the evaluation in the paper adopted 100 sets per configuration. Quite a few ```.npy``` intermediate data will be resulted in ```Sound-WCDFP/results```.

### Plotting the figures

Finally, plot the analyzed results.
```
cd Sound-WCDFP/plots
./plot.sh
```
You can find the plotted figures in the folder ```outputs```. The following table describes the mapping between the figures and the outputed pdfs.

| Paper Figure    |  Plot in ```plots/outputs```      |
|-----------------|-----------------------------------|
| Fig. 6          |  Fig6_u60 and Fig6_u80            |
| Fig. 7          |  Fig7_u60 and Fig7_u80            |
| Fig. 8          |  Fig8                             |
| Fig. 9          |  Fig9_2tasks and Fig9_5tasks      |
| Fig. 10         |  Fig10_2tasks and Fig10_5tasks    |
| Fig. 11         |  Fig11_15tasks and Fig11_25tasks  |

## Overview of the corresponding functions

The following table describes the mapping between content and the source code in this repository.

On Paper | Source code 
--- | --- 
Theorem 8 (Refuted) | taskConvolution.calculate()
Theorem 9 (Refuted) | chernoff.optimal_chernoff_taskset_lowest(taskset, 'Original')
Corollary 12 | taskConvolution.calculate_safe()
Corollary 15 | chernoff.optimal_chernoff_taskset_lowest(taskset, 'Carry' or 'Inflation')

The implementations of task-level convolution and Chernoff-bound are from the corresponding papers, respectively:
- Georg von der Brüggen, Nico Piatkowski, Kuan-Hsun Chen, Jian-Jia Chen, Katharina Morik: Efficiently Approximating the Probability of Deadline Misses in Real-Time Systems. ECRTS 2018: 6:1-6:22
- Kuan-Hsun Chen, Niklas Ueter, Georg von der Brüggen, Jian-Jia Chen: Efficient Computation of Deadline-Miss Probability and Potential Pitfalls. DATE 2019: 896-901


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
