#!/bin/bash

echo 'plotting RTSS experiments'
python plot.py -i rtss -u 50 -s 10 -m 0.025 -f 0.025 -h 1 -r -v prob_log
sleep 1

#cp *.pdf ../../Paper/figures/
