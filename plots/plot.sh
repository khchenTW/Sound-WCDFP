#!/bin/bash

echo 'plotting RTSS experiments'
python plot.py -i rtss -u 30 -s 10 -m 0.001 -f 0.001 -h 1.83 -r -v prob_log
python plot.py -i rtss -u 50 -s 10 -m 0.001 -f 0.001 -h 1.83 -r -v prob_log
python plot.py -i rtss -u 70 -s 10 -m 0.001 -f 0.001 -h 1.83 -r -v prob_log
sleep 1

#cp *.pdf ../../Paper/figures/
