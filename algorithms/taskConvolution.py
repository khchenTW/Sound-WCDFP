from __future__ import division
from importlib.metadata import distribution
from pickle import FALSE
import random
import math
import sys
from tkinter import W
import numpy as np
from operator import itemgetter, attrgetter
from pkg_resources import get_distribution
import mpmath as mp

sys.path.append('../')
from algorithms import TDA

''' Calculates the probability of deadline miss with safe upper bounds (Carry-in or inflation), varience of ECRTS'18 implementation

'tasks represents' the given task set,
'prob_abnormal' the probability of abnormal execution, i.e., higher WCET.
'probabilities' tracks the calculated probabilities for each time point
'states' tracks the number of states considered for each time point '''

def calculate_safe(tasks, prob_abnormal, probabilties, states, bound, sortedList=False):
    if sortedList == True:
        tasks = sort(tasks, 'deadline', False)
    # suppose that we are checking for the last index task
    deadline = tasks[len(tasks)-1]['deadline']
    min_time = TDA.min_time(tasks, 'execution')
    if sortedList == True:
        tasks = sort(tasks, 'execution', True)
    all_times = all_releases(tasks, deadline)
    times = []
    for i in all_times:
       if i >= min_time:
           times.append(i)
    times.sort()
    for time in times:
        prob = calculate_probabiltiy_safe(tasks, time, prob_abnormal, states, bound, False)        
        probabilties.append(prob)
    probability = 1
    for i in range(0, len(times),1):
        if (probabilties[i]<probability):
            probability = probabilties[i]
    return probability

''' Calculates the probability of deadline miss as detailed in Section 5 (ECRTS'18).
All job releases of higher priority tasks are considered.

'tasks represents' the given task set,
'prob_abnormal' the probability of abnormal execution, i.e., higher WCET.
'probabilities' tracks the calculated probabilities for each time point
'states' tracks the number of states considered for each time point '''

def calculate(tasks, prob_abnormal, probabilties, states, sortedList=False):
    if sortedList == True:
        tasks = sort(tasks, 'deadline', False)
    deadline = tasks[len(tasks)-1]['deadline']
    min_time = TDA.min_time(tasks, 'execution')
    if sortedList == True:
        tasks = sort(tasks, 'execution', True)
    all_times = all_releases(tasks, deadline)
    times = []
    for i in all_times:
        if i > min_time:
            times.append(i)
    times.sort()
    for time in times:
        prob = calculate_probabiltiy(tasks, time, prob_abnormal, states)
        probabilties.append(prob)
    probability = 1
    for i in range(0, len(times),1):
        if (probabilties[i]<probability):
            probability = probabilties[i]
    return probability

''' Calculates the deadline miss probability for a given point in time'''
def calculate_probabiltiy_safe(tasks, time, prob_abnormal, states, bound, sortedList=False):  
    if sortedList == True:  
        order = sort(tasks, 'period', True) 
    else:
        order = tasks   
    distributions = []
    if bound == 'Carryin':
        for task in order:            
            if task == order[len(order)-1]:
                # if this is the lowest priority task k                
                distributions.append(get_distribution(task, time, prob_abnormal))
            else:    
                distributions.append(get_distribution_carryin(task, time, prob_abnormal))            
    elif bound == 'Inflation':        
        # Generates the binomial distribution of the tasks        
        for task in order:         
            if task == order[len(order)-1]:
                # if this is the lowest priority task k
                distributions.append(get_distribution(task, time, prob_abnormal))   
            else:
                if sortedList == True:
                    tasks = sort(tasks, 'deadline', False)
                saiTasks = []
                flag = False
                for i in range(0, len(tasks)-1, 1):
                    if tasks[i] == task:
                        flag = True
                    if flag == True:
                        saiTasks.append(tasks[i]) 
                exttime = sum(tsk['deadline'] for tsk in saiTasks)                            
                distributions.append(get_distribution_inflation(task, time, exttime, prob_abnormal))
    # creates an empty distribution as starting point for the convolution
    distri = empty_distri()
    # successively convolutes the starting distribution with the
    for i in range(0,len(distributions),1):
        distri = convolute(distri, distributions[i])    
    prob =  calculate_miss_prob(distri, time)    
    #states.append(len(distri))
    return prob

''' Calculates the deadline miss probability for a given point in time'''
def calculate_probabiltiy(tasks, time, prob_abnormal, states):
    order = sort(tasks, 'execution', True)
    distributions = []
    # Generates the binomial distribution of the tasks
    for task in order:
        distributions.append(get_distribution(task, time, prob_abnormal))
    # creates an empty distribution as starting point for the convolution
    distri = empty_distri()
    # successively convolutes the starting distribution with the
    for i in range(0,len(distributions),1):
        distri = convolute(distri, distributions[i])
    prob =  calculate_miss_prob(distri, time)
    #states.append(len(distri))
    return prob

# calculates the binomial distribution with the inflated pdf
def get_distribution_inflation(task, time, exttime, prob_abnormal):
    distribution = []    
    a = math.ceil(time/task['deadline'])
    b = math.ceil((time+exttime)/task['deadline'])
    for k in range(0, int(a) + 1, 1):
        pair={}
        pair['misses']=k        
            
        if k == a:            
            pair['prob'] = 1 - sum([p['prob'] for p in distribution])
        else:
            pair['prob'] = (math.factorial(b)/(math.factorial(k)*math.factorial(b-k)))*math.pow(prob_abnormal, k)*math.pow((1-prob_abnormal),(b-k))
        pair['execution']=k*task['abnormal_exe']+(a-k)*task['execution']
        distribution.append(pair)
    #print (distribution)
    return distribution

# calculates the binomial distribution with carryin
def get_distribution_carryin(task, time, prob_abnormal):
    distribution = []    
    n = math.ceil((time+task['deadline'])/task['deadline'])
    for k in range(0, int(n) + 1, 1):
        pair={}
        pair['misses']=k
        pair['prob']= (math.factorial(n)/(math.factorial(k)*math.factorial(n-k)))*math.pow(prob_abnormal, k)*math.pow((1-prob_abnormal),(n-k))
        pair['execution']=k*task['abnormal_exe']+(n-k)*task['execution']
        distribution.append(pair)
    return distribution

# calculates the binomial distribution for a given task, time, and probability of abnormal execution
def get_distribution(task, time, prob_abnormal):
    distribution = []
    n = math.ceil(time/task['deadline'])
    for k in range(0, int(n) + 1, 1):
        pair={}
        pair['misses']=k
        pair['prob']= (math.factorial(n)/(math.factorial(k)*math.factorial(n-k)))*math.pow(prob_abnormal, k)*math.pow((1-prob_abnormal),(n-k))
        pair['execution']=k*task['abnormal_exe']+(n-k)*task['execution']
        distribution.append(pair)
    return distribution

# direct convolution of two distributions
def convolute(dist1, dist2):
    dist = []
    for state1 in dist1:
        for state2 in dist2:
            pair={}
            pair['prob']=state1['prob']*state2['prob']
            pair['execution']=state1['execution']+state2['execution']
            dist.append(pair)
    return dist

# ''' direct convolution of two distributions. The pruning techniques presented in
# Section 6.2 (ECRTS'18) are used to prune away unnecessary states. '''
def convolute_prune(dist1, dist2, minimum, maximum, num_states, pruned, prob_cut, time):
    prob = 0.0
    dist = []
    prune = 0
    states = 0
    for state1 in dist1:
        for state2 in dist2:
            states = states + 1
            pair={}
            pair['prob']=state1['prob']*state2['prob']
            pair['execution']=state1['execution']+state2['execution']
            # if a new state will always result in a deadline miss it can be pruned
            # probability of the state is added to the miss probabiltiy
            if ((pair['execution'] + minimum) > time):
                prune = prune + 1
                prob = prob + pair['prob']
            # if a new state will never result in a deadline miss it can be pruned
            elif((pair['execution'] + maximum) < time):
                prune = prune + 1
            # otherwise, it has to be considered further
            else:
                dist.append(pair)
    prob_cut.append(prob)
    pruned.append(prune)
    num_states.append(states)
    return dist

# Calculates the deadline miss probability for a given distribution and the time,
# i.e., tests if the workload is larger than the execution time and sums up the
# related probabilities.
def calculate_miss_prob(distribution, time):
    #print(distribution)
    #prob = np.longdouble(0.0)
    prob = mp.mpf(0.0)
    for dist in distribution:
        if (dist['execution']>time):
            prob = prob + dist['prob']
    return prob

# calculates the time for the last releases of all tasks before the deadline (and adds the deadline)
# (Binomial based approach)
def last_release(tasks, deadline):
    times = []
    for task in tasks:
        times.append(math.floor(deadline/task['deadline'])*task['deadline'])
    return times

# calculates the time for all releases of all tasks before the deadline (and adds the deadline)
# (Binomial based approach)
def all_releases(tasks, deadline):
    times = []
    times.append(deadline)
    for task in tasks:
        count = task['period']
        while(count < deadline):
            times.append(count)
            count = count + task['period']
    return times

# creates the jobs that have to be convoluted in the convolution based approach
def calculate_releases(tasks, deadline, releases, prob_abnormal):
    for task in tasks:
        time = 0.0
        while(time < deadline):
            distribution = []
            for k in range(0, 2, 1):
                pair={}
                pair['time']=time
                pair['prob']= math.pow(prob_abnormal, k)*math.pow((1-prob_abnormal),(1-k))
                pair['execution']=k*task['abnormal_exe']+(1-k)*task['execution']
                distribution.append(pair)
            releases.append(distribution)
            time = time + task['period']

def sort(tasks, criteria, reverse_order):
    return sorted(tasks, key=lambda item:item[criteria], reverse=reverse_order)

# initializes an empty distribution (workload 0 with probability 1)
def empty_distri():
    distri = []
    pair={}
    pair['misses']=''
    #pair['prob']=np.longdouble(1.0)
    pair['prob']=mp.mpf(1.0)
    pair['execution']=0.0
    distri.append(pair)
    return distri
