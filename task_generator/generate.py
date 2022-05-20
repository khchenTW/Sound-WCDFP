from __future__ import division

import task_generator
import mixed_task_builder
import getopt, sys, os
import numpy as np

sys.path.append('../')
from algorithms import TDA

'''
 @method Generates tasksets that can pass the time-demand analysis
 @param utilization: Taskset utilizations
 @param hard_task_factor: Multiplier in case of abnormal mode
 @param fault_rate: Probability of a job being in abnormal mode
 @param num_task: Number of tasks in a taskset
 @param num_sets: Number of generated tasksets
'''

def tasksets_gen_with_tda(utilization, hard_task_factor, fault_rate, num_task, num_sets, rounded):
    def taskset_gen_with_tda(utilization, hard_task_factor, fault_rate, num_task):
        while True:
            if rounded is True:
                tasks = task_generator.taskGeneration_rounded(num_task, utilization)
            else:
                tasks = task_generator.taskGeneration_p(num_task, utilization)
            tasks = mixed_task_builder.mixed_task_set(tasks, hard_task_factor, fault_rate)
            tasks = mixed_task_builder.pdfForm(tasks)
            if TDA.TDAtest(tasks) == 0:
                break
            else:
                pass
        return tasks
    return [taskset_gen_with_tda(utilization, hard_task_factor, fault_rate, num_task) for i in range(num_sets)]

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:n:s:m:f:h:r", ["ident=", "num_tasks=", "num_sets=", "max_fault_rate=", "fault_rate_step_size=", "hard_task_factor=", "rounded"])
    except getopt.GetoptError as err:
        print (str(err))
        sys.exit(2)

    num_tasks, num_sets, max_fault_rate, step_size_fault_rate, hard_task_factor = 0, 0, 0, 0, 0
    ident = None
    rounded = False
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

    for fault_rate in np.arange(step_size_fault_rate, max_fault_rate + step_size_fault_rate, step_size_fault_rate):
        print('Generating: %d tasksets, %d tasks, fault probability: %f, rounded: %r' % (num_sets, num_tasks, fault_rate, rounded))
        #for utilization in np.arange(5, 95, 5):
        for utilization in np.arange(50, 75, 20):
            tasksets = tasksets_gen_with_tda(utilization, hard_task_factor, fault_rate, num_tasks, num_sets, rounded)
            try:
                if ident is not None:
                    filename = '../tasksets/tasksets_' + ident + '_n_' + str(num_tasks) + 'u_' + str(utilization) + '_m' + str(num_sets) + 's_'+ str(max_fault_rate) + 'f_' + str(step_size_fault_rate) + str('r' if rounded else '')
                    np.save(filename, tasksets)
                else:
                    raise Exception ("Please specify an identifier!")
            except IOError:
                print('Could not write filename %s' % filename)

if __name__=="__main__":
    main()
