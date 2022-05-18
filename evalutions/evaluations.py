from __future__ import division
from multiprocessing import Pool, freeze_support
import itertools

import sys, time, getopt
import numpy as np

sys.path.append('../')
from algorithms import chernoff

def func_star(a_b):
    #Covert f([a,b,c,d,e,f]) to f(a,b,c,d,e,f) call
    return insideroutine(*a_b)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:n:s:m:f:h:r:p", ["ident=", "num_tasks=", "num_sets=", "max_fault_rate=", "fault_rate_step_size=", "hard_task_factor=", "rounded", "parallel"])
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
            print ('Evaluating: %d tasksets, %d tasks, fault probability: %f, rounded: %r' % (num_sets, num_tasks, fault_rate, rounded))
            #for utilization in np.arange(5, 100, 5):
            #for utilization in np.arange(50, 55, 20):
            for utilization in np.arange(70, 75, 20):
                try:
                    if ident is not None:
                        filename = 'tasksets_' + ident + '_n_' + str(num_tasks) + 'u_' + str(utilization) + '_m' + str(num_sets) + 's_'+ str(max_fault_rate) + 'f_' + str(step_size_fault_rate) + str('r' if rounded else '')

                        # Load the generated tasksets
                        try:
                            tasksets = np.load('../tasksets/' + filename + '.npy', allow_pickle=True)
                        except:
                            raise Exception("Could not read")

                        # Init lists for storing Calculated DMP
                        results_chernoff = []
                        results_carry = []
                        results_inflation = []
                        rel = []

                        # Distribute to multiprocesses
                        if __name__=='__main__':
                            freeze_support()
                            p = Pool(5)
                            rel = (p.map(func_star, zip(tasksets,itertools.repeat(max_fault_rate))))
                        print(rel)
                        for i in rel:
                            results_chernoff.append(i[0])
                        np.save('../results/mp_res_chernoff_' + filename + '.npy', results_chernoff)
                    else:
                        raise Exception("Please specify an identifier!")

                except IOError:
                    print('Could not write filename %s' % filename)

    else:
        # single thread version
        print ("This is not ready for use")
        for fault_rate in np.arange(step_size_fault_rate, max_fault_rate + step_size_fault_rate, step_size_fault_rate):
            print('Evaluating: %d tasksets, %d tasks, fault probability: %f, rounded: %r' % (num_sets, num_tasks, fault_rate, rounded))
            for utilization in np.arange(70, 75, 20):
                try:
                    if ident is not None:
                        filename = 'tasksets_' + ident + '_n_' + str(num_tasks) + 'u_' + str(utilization) + '_m' + str(num_sets) + 's_'+ str(max_fault_rate) + 'f_' + str(step_size_fault_rate) + str('r' if rounded else '')

                        # Load the generated tasksets
                        try:
                            tasksets = np.load('../tasksets/' + filename + '.npy', allow_pickle=True)
                        except:
                            raise Exception("Could not read")
                        
                        # Init lists for storing Calculated DMP
                        results_chernoff = []
                        results_carry = []
                        results_inflation = []
                        for taskset in tasksets:
                            results_chernoff.append(chernoff.optimal_chernoff_taskset_all(taskset))
                        np.save('../results/res_chernoff_' + filename + '.npy', results_chernoff)
                    else:
                        raise Exception("Please specify an identifier!")
                except IOError:
                    print ('Could not write filename %s' % filename)
        

def insideroutine(taskset, max_fault_rate):
    print(taskset[0])
    results_chernoff = []
    results_carry = []
    results_inflation = []
    
    print('Computing the original chernoff bounds')
    results_chernoff.append(chernoff.optimal_chernoff_taskset_lowest(taskset))
    
    print('Computing the chernoff bounds with Carry-in')
    results_carry.append(chernoff.optimal_chernoff_taskset_lowest(taskset))
    
    print('Computing the chernoff bounds with Inflation')
    results_inflation.append(chernoff.optimal_chernoff_taskset_lowest(taskset))
    
    print('DONE!')
    return [results_chernoff, results_carry, results_inflation]

if __name__=="__main__":
    main()
