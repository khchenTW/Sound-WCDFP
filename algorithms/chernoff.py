'''
Author: Niklas Ueter, Kuan-Hsun Chen
'''

from __future__ import division
import scipy
from scipy.optimize import bisect
from scipy.optimize import newton
from scipy.optimize import minimize_scalar
from scipy.optimize import minimize
from scipy.optimize import root
from scipy.optimize import fsolve
from scipy import special
from numpy import *
from sympy import symbols, sympify, lambdify, plot, limit, oo, diff, simplify

import mpmath as mp
from functools import wraps
import time
import random
import numpy as np
import sys, getopt
import os
import math
import heapq
import itertools

def findpoints(task, higher_priority_tasks, mode = 0):
    points = []
    if mode == 0: #kpoints
        # pick up k testing points here
        for i in higher_priority_tasks:
            point = math.floor(task['deadline']/i['deadline'])*i['deadline']
            if point > 0:
                points.append(point)
        points.append(task['deadline'])
    else: #allpoints
        for i in higher_priority_tasks:
            for r in range(1, int(math.floor(task['period']/i['period']))+1):
                point = r*i['period']
            if point > 0:
                points.append(point)
        points.append(task['deadline'])
    return points

'''
@method: Generates the log-moment generating function (DATE'19).
@param task: Task under analysis
@param other: Higher-priority tasks
@param interval: Time interval t under analysis
'''
def logmgf_tasks(task, other, interval):
    def logmgf_task(task, interval):
        num_jobs_released = int(math.ceil(float(interval)/task['period']))
        return str(num_jobs_released) + '*ln(' + '+'.join(('exp(' + str(event) + '*' + 's' + ')*' + str(probability)) for (event, probability) in task['pdf']) + ')'
    s = symbols('s')
    func = '(' + '+'.join(logmgf_task(tsk, interval) for tsk in (np.concatenate(([task], other)) if other is not None else [task])) + ') -' + 's*' + str(interval)
    func = lambdify(s, sympify(func), 'mpmath')
    return func

'''
@method: Generates the log-moment generating function with the carry-in method.
@param task: Task under analysis
@param other: Higher-priority tasks
@param interval: Time interval t under analysis
'''
def logmgf_tasks_carry(task, other, interval):
    def logmgf_task(task, interval):
        num_jobs_released = int(math.ceil(float(interval+task['deadline'])/task['period']))
        return str(num_jobs_released) + '*ln(' + '+'.join(('exp(' + str(event) + '*' + 's' + ')*' + str(probability)) for (event, probability) in task['pdf']) + ')'
    s = symbols('s')
    func = '(' + '+'.join(logmgf_task(tsk, interval) for tsk in (np.concatenate(([task], other)) if other is not None else [task])) + ') -' + 's*' + str(interval)
    func = lambdify(s, sympify(func), 'mpmath')
    return func

'''
@method: Generate an inflation pdf based on Sample and Inflate directly with multi-normial distribution.
@param task: Task i under inflation
@param a: number of jobs released in the interval
@param b: jobs released over interval + relative deadlines of tasks that are affected by the task i, i.e., i to k-1.
'''
def sample_inflate_multi(task, a, b):
    print ('a:'+str(a)+' b:'+str(b))
    # Sample b the probabilistic execution time of task 
    # assume task only has two modes

    sample = list(itertools.product((0,1), repeat = b))
    #print (sample)

    events = list(itertools.combinations_with_replacement((0,1), a))
    #print (events)    

    # Select only a largest values among the samples as the inflated execution time

    select = list(heapq.nlargest(a, i) for i in sample)
    select = list(sum(i) for i in select)
    events = list(sum(i) for i in events)
    print (events)    
    numbers = list(select.count(i) for i in events)
    print (numbers)

    # TODO Return the inflated distribution
    #for event, probability in zip(events, probability ):
        #task['infpdf'].append((event*task['abnormal_exe']+(a-event)*task['execution'], probability)) 
    task['infpdf'] = [(task['execution'], 1-task['prob']), (task['abnormal_exe'], task['prob'])]
    return task

'''
@method: Generate an inflation pdf based on Sample and Inflate directly with bernoulli distribution.
@param task: Task i under inflation
@param a: number of jobs released in the interval
@param b: jobs released over interval + relative deadlines of tasks that are affected by the task i, i.e., i to k-1.
'''
def sample_inflate_bernoulli(task, a, b):
    task['infpdf'] = list()
    if a > b:
        print ("SAI is not applicable here, so no inflation")
        return task
    # assume task only has two modes
    for eventL in range(a+1):
        task['infpdf'].append(((eventL*task['abnormal_exe'] + (a-eventL)*task['execution']), (special.binom(b, eventL)*(task['prob'])**eventL)*((1-task['prob'])**(b-eventL))))
    return task

def sample_inflate_bernoulli_2(task, a, b):
    task['infpdf'] = list()
    if a > b:
        print ("SAI is not applicable here, so no inflation")
        return task
    # assume task only has two modes
    for eventL in range(a+1):
        val = eventL*task['abnormal_exe'] + (a-eventL)*task['execution']  # inflated value of the random variable for the case
        if eventL == a:
            prob = 1 - sum([p for v, p in task['inpdf']])  # remaining probability
        else:
            prob = special.binom(b, eventL) * (task['prob'] ** eventL) * ((1-task['prob']) ** (b-eventL))  # probability of the case
        task['infpdf'].append((val, prob))  # append one entry probability density function

    assert sum(sum([p for v, p in task['inpdf']])) == 1, 'No valid probability density function.'
    return task

'''
@method: Generates the log-moment generating function with the inflation method.
@param task: Task under analysis
@param other: Higher-priority tasks
@param interval: Time interval t under analysis
'''
def logmgf_tasks_inflation(task, other, interval):
    def logmgf_task(task, interval):
        # Calculate the number of jobs released in the interval
        num_jobs_released = int(math.ceil(float(interval)/task['period']))
        # Get the index of task -- if it is in the list of higher priority tasks
        result = np.where(other == task)
        if len(result) > 0 and len(result[0]) > 0:
            # the task is in hp(\tau_k)
            ind = result[0][0]
            # Calculate the extended interval
            extInterval = interval + sum(tsk['deadline'] for tsk in other[ind:])
            # make an inflated task
            task = sample_inflate_bernoulli(task, num_jobs_released, int(math.ceil(float(extInterval)/task['period'])))
            #print(task['infpdf'])

            # return the mgf form with the inflated task
            return str(num_jobs_released) + '*ln(' + '+'.join(('exp(' + str(event) + '*' + 's' + ')*' + str(probability)) for (event, probability) in task['infpdf']) + ')'
        else:
            #don't do inflation but return the function directly
            return str(num_jobs_released) + '*ln(' + '+'.join(('exp(' + str(event) + '*' + 's' + ')*' + str(probability)) for (event, probability) in task['pdf']) + ')'
    s = symbols('s')
    func = '(' + '+'.join(logmgf_task(tsk, interval) for tsk in (np.concatenate(([task], other)) if other is not None else [task])) + ') -' + 's*' + str(interval)
    #print(func)
    func = lambdify(s, sympify(func), 'mpmath')
    return func


'''
@method: Finds argmin function within tolerance.
@param function: Convex function to be minimized.
@param a: Beginning of the interval under analysis.
@param b: Ending of the interval under analysis.
@param tolerance: Resolution of solution
'''
def goldensectionsearch(function, a, b, tolerance=1e-5):
    invphi = (math.sqrt(5) - 1)/2                                                                                                                   
    invphi2 = (3 - math.sqrt(5))/2
    (a,b) = (min(a,b), max(a,b))
    h = b - a
    if h <= tolerance:
        return (a,b)                                                                                                                  
    n = int(math.ceil(math.log(tolerance/h)/math.log(invphi)))
    c = a + invphi2 * h
    d = a + invphi * h
    yc = function(c)
    yd = function(d)
    for k in range(n-1):
        if yc < yd:
            b = d
            d = c
            yd = yc
            h = invphi*h
            c = a + invphi2 * h
            yc = function(c)
        else:
            a = c
            c = d
            yc = yd
            h = invphi*h
            d = a + invphi * h
            yd = function(d)
    if yc < yd:
        return d
    else:
        return b

'''
@method: Computes the minimal chernoff bound.
@param taskset: Taskset under analysis.
@param bound: name of bound
@param s_min: Beginning of interval under analysis.
@param s_max: Ending of interval under analysis.
@return list of deadline miss probabilities for each task in the task set and runtime
'''
def optimal_chernoff_taskset_all(taskset, bound, s_min = 0, s_max = 10e100):
    results = []
    for i, task in enumerate(taskset):
        start_time = time.time()
        times = findpoints(task, taskset[:i])
        if bound == 'Inflation':
            functions = (logmgf_tasks_inflation(taskset[-1], taskset[:-1], time) for time in times)
        elif bound == 'Original':
            functions = (logmgf_tasks(taskset[-1], taskset[:-1], time) for time in times)
        else:
            functions = (logmgf_tasks_carry(taskset[-1], taskset[:-1], time) for time in times)

        #golden section search
        candidates = []
        for function in functions:
            optimal = goldensectionsearch(function, s_min, s_max)   
            candidates.append((optimal, function(optimal)))
        optimal = candidates[np.argmin([x[1] for x in candidates])]
        elapsed_time = time.time() - start_time
        results.append({'ErrProb' : min(1.0, mp.exp(str(optimal[1]))), 'ms' : elapsed_time})
    return results

def optimal_chernoff_taskset_lowest(taskset, bound, s_min = 0, s_max = 10e100):
    start_time = time.time()
    times = findpoints(taskset[-1], taskset[:-1])
    if bound == 'Inflation':
        functions = (logmgf_tasks_inflation(taskset[-1], taskset[:-1], time) for time in times)
    elif bound == 'Original':
        functions = (logmgf_tasks(taskset[-1], taskset[:-1], time) for time in times)
    else:
        functions = (logmgf_tasks_carry(taskset[-1], taskset[:-1], time) for time in times)

    #golden section search
    candidates = []
    for function in functions:
        optimal = goldensectionsearch(function, s_min, s_max)   
        candidates.append((optimal, function(optimal)))
    optimal = candidates[np.argmin([x[1] for x in candidates])]
    elapsed_time = time.time() - start_time
    return {'ErrProb' : min(1.0, mp.exp(str(optimal[1]))), 'ms' : elapsed_time}
