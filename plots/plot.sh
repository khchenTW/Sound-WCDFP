#!/bin/bash

echo 'plotting RTSS experiments'
#python plot.py -i rtss -u 50 -s 20 -m 0.001 -f 0.001 -h 1.83 -r -v prob_log
#python plot.py -i rtss -u 60 -s 20 -m 0.001 -f 0.001 -h 1.83 -r -v prob_log
#python plot.py -i rtss -u 70 -s 20 -m 0.001 -f 0.001 -h 1.83 -r -v prob_log
#python plot.py -i rtss -u 80 -s 20 -m 0.001 -f 0.001 -h 1.83 -r -v prob_log
#python plot.py -i rtss -u 90 -s 20 -m 0.001 -f 0.001 -h 1.83 -r -v prob_log
#python plot.py -i rtss -u 40 -s 20 -m 0.025 -f 0.025 -h 1.83 -r -v prob_log
#python plot.py -i rtss -u 40 -s 100 -m 0.025 -f 0.025 -h 1.83 -r -v prob_log -p
#python plot.py -i rtss -u 45 -s 100 -m 0.025 -f 0.025 -h 1.83 -r -v prob_log -p
#python plot.py -i rtss -u 60 -s 100 -m 0.025 -f 0.025 -h 1.83 -r -v prob_log -p
#python plot.py -i rtss -u 80 -s 100 -m 0.025 -f 0.025 -h 1.83 -r -v prob_log -p

#python plot.py -i rtss -u 40 -s 20 -m 0.025 -f 0.025 -h 1.83 -r -v prob_log -p

#python plot.py -i rtss -u 50 -s 10 -m 0.001 -f 0.001 -h 1.83 -r -v counter
#python plot.py -i rtss -u 60 -s 10 -m 0.001 -f 0.001 -h 1.83 -r -v counter
#python plot.py -i rtss -u 70 -s 10 -m 0.001 -f 0.001 -h 1.83 -r -v counter
#python plot.py -i rtss -u 80 -s 10 -m 0.001 -f 0.001 -h 1.83 -r -v counter
#python plot.py -i rtss -u 90 -s 10 -m 0.001 -f 0.001 -h 1.83 -r -v counter
#python plot.py -i rtss -u 50 -s 10 -m 0.025 -f 0.025 -h 1.83 -r -v counter
#python plot.py -i rtss -u 60 -s 10 -m 0.025 -f 0.025 -h 1.83 -r -v counter
#python plot.py -i rtss -u 70 -s 10 -m 0.025 -f 0.025 -h 1.83 -r -v counter
#python plot.py -i rtss -u 80 -s 10 -m 0.025 -f 0.025 -h 1.83 -r -v counter
#python plot.py -i rtss -u 90 -s 10 -m 0.025 -f 0.025 -h 1.83 -r -v counter

# shepherding

#python plot.py -i rtss -u 45 -s 20 -m 0.025 -f 0.025 -h 1.83 -r -v prob_log -p
#python plot.py -i rtss -u 60 -s 100 -m 0.025 -f 0.025 -h 1.83 -r -v prob_log -p
#python plot.py -i rtss -u 80 -s 100 -m 0.025 -f 0.025 -h 1.83 -r -v prob_log -p
python plot.py -i rtss -u 60 -s 20 -m 0.025 -f 0.025 -h 1.83 -r -v prob_log -p

sleep 1

#cp *.pdf ../../Paper/figures/
