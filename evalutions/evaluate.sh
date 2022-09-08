#!/bin/bash

# each line represents one specific configuration
# - i is the meta name
# - n is the number of tasks per set  
# - s is the number of sets 
# - f is the fault rate 
# - h is the execution time of the longer version 
# - p is the number of processes (default is 1)
# - u is the total utilization
# - l is the flag for limited range [1,10] (default is [1,100])

# Fig 6
#python evaluations.py -i rtss -n 5 -s 10 -f 0.025 -h 1.83 -p 2 -u 60 -l 
#python evaluations.py -i rtss -n 5 -s 10 -f 0.025 -h 1.83 -p 2 -u 80 -l

# Fig 7, 8
#python evaluations.py -i rtss -n 5 -s 10 -f 0.025 -h 1.83 -p 2 -u 60 
#python evaluations.py -i rtss -n 5 -s 10 -f 0.025 -h 1.83 -p 2 -u 80

# Fig 9
python evaluations.py -i rtss -n 2 -s 10 -f 0.025 -h 1.83 -p 2 -u 45 -l # only CB
#python evaluations.py -i rtss -n 5 -s 10 -f 0.025 -h 1.83 -p 2 -u 45 -l # only CB

# Fig 10
#python evaluations.py -i rtss -n 2 -s 10 -f 0.025 -h 1.83 -p 2 -u 45 # only CB
#python evaluations.py -i rtss -n 5 -s 10 -f 0.025 -h 1.83 -p 2 -u 45 # only CB

# Fig 11
#python evaluations.py -i rtss -n 15 -s 10 -f 0.025 -h 1.83 -p 2 -u 45  # only CB
#python evaluations.py -i rtss -n 25 -s 10 -f 0.025 -h 1.83 -p 2 -u 45  # only CB

sleep 1
