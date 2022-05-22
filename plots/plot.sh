#!/bin/bash

echo 'plotting RTSS experiments'
python plot.py -i rtss -u 30 -s 10 -m 0.001 -f 0.001 -h 1.83 -r -v prob_log
python plot.py -i rtss -u 50 -s 10 -m 0.001 -f 0.001 -h 1.83 -r -v prob_log
python plot.py -i rtss -u 30 -s 10 -m 0.001 -f 0.001 -h 1.2 -r -v prob_log
python plot.py -i rtss -u 50 -s 10 -m 0.001 -f 0.001 -h 1.2 -r -v prob_log
python plot.py -i rtss -u 30 -s 10 -m 0.025 -f 0.025 -h 1.83 -r -v prob_log
python plot.py -i rtss -u 50 -s 10 -m 0.025 -f 0.025 -h 1.83 -r -v prob_log
python plot.py -i rtss -u 30 -s 10 -m 0.025 -f 0.025 -h 1.2 -r -v prob_log
python plot.py -i rtss -u 50 -s 10 -m 0.025 -f 0.025 -h 1.2 -r -v prob_log
#python plot.py -i rtss -u 70 -s 10 -m 0.001 -f 0.001 -h 1.83 -r -v prob_log
#python plot.py -i rtss -u 30 -s 10 -m 0.001 -f 0.001 -h 1.2 -r -v counter
#python plot.py -i rtss -u 50 -s 10 -m 0.001 -f 0.001 -h 1.2 -r -v counter
#python plot.py -i rtss -u 70 -s 10 -m 0.001 -f 0.001 -h 1.2 -r -v counter

#python plot.py -i rtss -u 30 -s 20 -m 0.001 -f 0.001 -h 1.1 -r -v counter
#python plot.py -i rtss -u 50 -s 20 -m 0.001 -f 0.001 -h 1.1 -r -v counter
#python plot.py -i rtss -u 70 -s 20 -m 0.001 -f 0.001 -h 1.1 -r -v counter
#python plot.py -i rtss -u 30 -s 20 -m 0.025 -f 0.025 -h 1.1 -r -v counter
#python plot.py -i rtss -u 50 -s 20 -m 0.025 -f 0.025 -h 1.1 -r -v counter
#python plot.py -i rtss -u 70 -s 20 -m 0.025 -f 0.025 -h 1.1 -r -v counter

#python plot.py -i rtss -u 30 -s 20 -m 0.001 -f 0.001 -h 1.2 -r -v counter
#python plot.py -i rtss -u 50 -s 20 -m 0.001 -f 0.001 -h 1.2 -r -v counter
#python plot.py -i rtss -u 70 -s 20 -m 0.001 -f 0.001 -h 1.2 -r -v counter
#python plot.py -i rtss -u 30 -s 20 -m 0.025 -f 0.025 -h 1.2 -r -v counter
#python plot.py -i rtss -u 50 -s 20 -m 0.025 -f 0.025 -h 1.2 -r -v counter
#python plot.py -i rtss -u 70 -s 20 -m 0.025 -f 0.025 -h 1.2 -r -v counter

#python plot.py -i rtss -u 30 -s 20 -m 0.001 -f 0.001 -h 1.83 -r -v counter
#python plot.py -i rtss -u 50 -s 20 -m 0.001 -f 0.001 -h 1.83 -r -v counter
#python plot.py -i rtss -u 70 -s 20 -m 0.001 -f 0.001 -h 1.83 -r -v counter
#python plot.py -i rtss -u 30 -s 20 -m 0.025 -f 0.025 -h 1.83 -r -v counter
#python plot.py -i rtss -u 50 -s 20 -m 0.025 -f 0.025 -h 1.83 -r -v counter
#python plot.py -i rtss -u 70 -s 20 -m 0.025 -f 0.025 -h 1.83 -r -v counter

sleep 1

#cp *.pdf ../../Paper/figures/
