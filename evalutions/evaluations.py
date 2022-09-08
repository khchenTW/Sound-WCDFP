from __future__ import division
from multiprocessing import Pool, freeze_support
import itertools

import sys, time, getopt
import numpy as np

sys.path.append('../')
from algorithms import chernoff, taskConvolution

'''
@function this is for parellel execution
'''
def func_star(a_b):
    #Covert f([a,b,c,d,e,f]) to f(a,b,c,d,e,f) call
    return insideroutine(*a_b)

'''
@function this is for parellel execution
'''
def func_star_CB(a_b):
    #Covert f([a,b,c,d,e,f]) to f(a,b,c,d,e,f) call
    return insideroutine_CB(*a_b)

'''
@function this is for parellel execution
'''
def insideroutine(taskset, fault_rate):
    results_conv_ori = []
    results_conv_carry = []
    results_conv_inflation = []
    results_ori = []
    results_carry = []
    results_inflation = []

    #print('Computing the convolution with Original')
    results_conv_ori.append(taskConvolution.calculate(taskset, fault_rate, [], [], True))
    #print('Computing the convolution with Carry-in')
    results_conv_carry.append(taskConvolution.calculate_safe(taskset, fault_rate, [], [], 'Carryin', True))
    #print('Computing the convolution with Inflation')
    results_conv_inflation.append(taskConvolution.calculate_safe(taskset, fault_rate, [], [], 'Inflation', True))
                            
    #print('Computing the chernoff bounds with Original')
    results_ori.append(chernoff.optimal_chernoff_taskset_lowest(taskset, 'Original'))
    #print('Computing the chernoff bounds with Carry-in')
    results_carry.append(chernoff.optimal_chernoff_taskset_lowest(taskset, 'Carry'))
    #print('Computing the chernoff bounds with Inflation')
    results_inflation.append(chernoff.optimal_chernoff_taskset_lowest(taskset, 'Inflation'))
    
    #print ([results_conv_ori, results_conv_carry, results_conv_inflation, results_ori, results_carry, results_inflation])
    return [results_conv_ori, results_conv_carry, results_conv_inflation, results_ori, results_carry, results_inflation]

'''
@function this is for parellel execution (CB only)
'''
def insideroutine_CB(taskset, fault_rate):
    results_conv_ori = []
    results_conv_carry = []
    results_conv_inflation = []
    results_ori = []
    results_carry = []
    results_inflation = []

    #print('Computing the convolution with Original')
    results_conv_ori.append(0)
    #print('Computing the convolution with Carry-in')
    results_conv_carry.append(0)
    #print('Computing the convolution with Inflation')
    results_conv_inflation.append(0)
                            
    #print('Computing the chernoff bounds with Original')
    results_ori.append(chernoff.optimal_chernoff_taskset_lowest(taskset, 'Original'))
    #print('Computing the chernoff bounds with Carry-in')
    results_carry.append(chernoff.optimal_chernoff_taskset_lowest(taskset, 'Carry'))
    #print('Computing the chernoff bounds with Inflation')
    results_inflation.append(chernoff.optimal_chernoff_taskset_lowest(taskset, 'Inflation'))
    
    #print ([results_conv_ori, results_conv_carry, results_conv_inflation, results_ori, results_carry, results_inflation])
    return [results_conv_ori, results_conv_carry, results_conv_inflation, results_ori, results_carry, results_inflation]

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:n:s:f:h:p:u:lo", ["ident=", "num_tasks=", "num_sets=", "fault_rate=", "hard_task_factor=", "processes=", "utilization=", "limited", "onlyCB"])
    except getopt.GetoptError as err:
        print (str(err))
        sys.exit(2)

    num_tasks, num_sets, fault_rate, processes, utilization = 0, 0, 0, 1, 45
    ident = None
    limited = False
    onlyCB = False

    for opt, arg in opts:
        if opt in ('-i', '--ident'):
            ident = str(arg)
        if opt in ('-n', '--num_tasks'):
            num_tasks = int(arg)
        if opt in ('-s', '--num_sets'):
            num_sets = int(arg)
        if opt in ('-f', '--fault_rate'):
            fault_rate = min(1.0, float(arg))
        if opt in ('-h', '--hard_task_factor'):
            hard_task_factor = float(arg)
        if opt in ('-p', '--processes'):
            processes = int(arg)
        if opt in ('-u', '--utilization'):
            utilization = int(arg)
        if opt in ('-l', '--limited'):
            limited = True
        if opt in ('-o', '--onlyCB'):
            onlyCB = True
    
    print ('Evaluating: %d tasksets, %d tasks, fault probability: %f, processes: %r, utilization: %r, limited: %r ' % (num_sets, num_tasks, fault_rate, processes, utilization, limited))
    try:
        if ident is not None:
            filename = 'tasksets_' + ident + '_n_' + str(num_tasks) + 'u_' + str(utilization) + 's_' + str(num_sets) + 'f_'+ str(fault_rate) + 'h_'+ str(hard_task_factor) + str('l' if limited else '')

            # Load the generated tasksets
            try:
                tasksets = np.load('../tasksets/' + filename + '.npy', allow_pickle=True)
            except:
                raise Exception("Could not read")

            # Init lists for storing Calculated DMP
            results_conv_ori = []
            results_conv_carry = []
            results_conv_inflation = []
            results_ori = []
            results_carry = []
            results_inflation = []
            rel = []

            # Distribute to multiprocesses
            if __name__=='__main__':
                freeze_support()                
                p = Pool(processes)
                if onlyCB == True:
                    rel = (p.map(func_star_CB, zip(tasksets,itertools.repeat(fault_rate))))
                else:
                    rel = (p.map(func_star, zip(tasksets,itertools.repeat(fault_rate))))
            
            print('Parallel execution is finished!')
            # Distribute the results into each pile
            for i in rel:
                results_conv_ori.append(i[0][0])
                results_conv_carry.append(i[1][0])
                results_conv_inflation.append(i[2][0])
                results_ori.append(i[3][0])
                results_carry.append(i[4][0])
                results_inflation.append(i[5][0])
                
            np.save('../results/mp_res_conv_ori_' + filename + '.npy', results_conv_ori)
            np.save('../results/mp_res_conv_carry_' + filename + '.npy', results_conv_carry)
            np.save('../results/mp_res_conv_inflation_' + filename + '.npy', results_conv_inflation)
            np.save('../results/mp_res_ori_' + filename + '.npy', results_ori)
            np.save('../results/mp_res_carry_' + filename + '.npy', results_carry)
            np.save('../results/mp_res_inflation_' + filename + '.npy', results_inflation)
        else:
            raise Exception("Please specify an identifier!")

    except IOError:
        print('Could not write filename %s' % filename)


if __name__=="__main__":
    main()
