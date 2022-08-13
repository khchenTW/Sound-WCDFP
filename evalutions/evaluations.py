from __future__ import division
from multiprocessing import Pool, freeze_support
import itertools

import sys, time, getopt
import numpy as np

sys.path.append('../')
from algorithms import chernoff, taskConvolution

'''
@function this is for parellel version
'''
def func_star(a_b):
    #Covert f([a,b,c,d,e,f]) to f(a,b,c,d,e,f) call
    return insideroutine(*a_b)
'''
@function this is for parellel version
'''
def insideroutine(taskset, max_fault_rate):
    #print(taskset[0])
    results_conv_ori = []
    results_conv_carry = []
    results_conv_inflation = []
    results_ori = []
    results_carry = []
    results_inflation = []

    print('Computing the convolution with Original')
    #results_conv_ori.append(taskConvolution.calculate(taskset, max_fault_rate, [], [], True))
    results_conv_ori.append(0)
    print('Computing the convolution with Carry-in')
    #results_conv_carry.append(taskConvolution.calculate_safe(taskset, max_fault_rate, [], [], 'Carryin', True))
    results_conv_carry.append(0)
    print('Computing the convolution with Inflation')
    #results_conv_inflation.append(taskConvolution.calculate_safe(taskset, max_fault_rate, [], [], 'Inflation', True))
    results_conv_inflation.append(0)
                            
    print('Computing the chernoff bounds with Original')
    results_ori.append(chernoff.optimal_chernoff_taskset_lowest(taskset, 'Original'))
    print('Computing the chernoff bounds with Carry-in')
    results_carry.append(chernoff.optimal_chernoff_taskset_lowest(taskset, 'Carry'))
    print('Computing the chernoff bounds with Inflation')
    results_inflation.append(chernoff.optimal_chernoff_taskset_lowest(taskset, 'Inflation'))
    print([results_conv_ori, results_conv_carry, results_conv_inflation, results_ori, results_carry, results_inflation])
    #print('DONE!')
    return [results_conv_ori, results_conv_carry, results_conv_inflation, results_ori, results_carry, results_inflation]

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:n:s:m:f:h:rp", ["ident=", "num_tasks=", "num_sets=", "max_fault_rate=", "fault_rate_step_size=", "hard_task_factor=", "rounded", "parallel"])
    except getopt.GetoptError as err:
        print (str(err))
        sys.exit(2)

    num_tasks, num_sets, max_fault_rate, step_size_fault_rate, hard_task_factor = 0, 0, 0, 0, 0
    ident = None
    rounded = False
    parallel = False

    for opt, arg in opts:
        if opt in ('-i', '--ident'):
            ident = str(arg)
        if opt in ('-n', '--num_tasks'):
            num_tasks = int(arg)
        if opt in ('-s', '--num_sets'):
            num_sets = int(arg)
        if opt in ('-m', '--max_fault_rate'):
            max_fault_rate = min(1.0, float(arg))
        if opt in ('-f', '--fault_rate_step_size'):
            step_size_fault_rate = min(1.0, float(arg))
        if opt in ('-h', '--hard_task_factor'):
            hard_task_factor = float(arg)
        if opt in ('-r', '--rounded'):
            rounded = True
        if opt in ('-p', '--parallel'):
            parallel = True
    if parallel == True:
        for fault_rate in np.arange(step_size_fault_rate, max_fault_rate + step_size_fault_rate, step_size_fault_rate):
            print ('Evaluating: %d tasksets, %d tasks, fault probability: %f, rounded: %r, parallel: %r' % (num_sets, num_tasks, fault_rate, rounded, parallel))
            #for utilization in np.arange(40, 45, 20):
            for utilization in np.arange(45, 50, 5): # U45
            #for utilization in np.arange(60, 65, 5): # U60
                try:
                    if ident is not None:
                        filename = 'tasksets_' + ident + '_n_' + str(num_tasks) + 'u_' + str(utilization) + '_m' + str(num_sets) + 's_'+ str(max_fault_rate) + 'f_' + str(step_size_fault_rate) + 'h_'+ str(hard_task_factor) + str('r' if rounded else '')

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
                            p = Pool(3)
                            rel = (p.map(func_star, zip(tasksets,itertools.repeat(max_fault_rate))))
                        #print(rel)
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
