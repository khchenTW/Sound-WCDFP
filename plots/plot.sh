#!/bin/bash

# Figure 6
python plot6.py -i rtss -n 5 -u 60 -s 10 -f 0.025 -h 1.83 -l
python plot6.py -i rtss -n 5 -u 80 -s 10 -f 0.025 -h 1.83 -l

# Figure 7
python plot7.py -i rtss -n 5 -u 60 -s 10 -f 0.025 -h 1.83 
python plot7.py -i rtss -n 5 -u 80 -s 10 -f 0.025 -h 1.83 

# Figure 8
python plot8.py -i rtss -n 5 -u 60 -s 10 -f 0.025 -h 1.83 

# Figure 9
python plot9.py -i rtss -n 2 -u 45 -s 10 -f 0.025 -h 1.83 -l
python plot9.py -i rtss -n 5 -u 45 -s 10 -f 0.025 -h 1.83 -l

# Figure 10
python plot10.py -i rtss -n 2 -u 45 -s 10 -f 0.025 -h 1.83 
python plot10.py -i rtss -n 5 -u 45 -s 10 -f 0.025 -h 1.83 

# Figure 11
python plot11.py -i rtss -n 15 -u 45 -s 10 -f 0.025 -h 1.83 
python plot11.py -i rtss -n 25 -u 45 -s 10 -f 0.025 -h 1.83 

sleep 1

