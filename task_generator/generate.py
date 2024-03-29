from __future__ import division

import task_generator
import mixed_task_builder
import getopt, sys, os
import numpy as np

sys.path.append('../')
from algorithms import TDA

'''
 @method Generates tasksets that can pass the time-demand analysis with only normal execution time
 @param utilization: Taskset utilizations
 @param hard_task_factor: Multiplier in case of abnormal mode
 @param fault_rate: Probability of a job being in abnormal mode
 @param num_task: Number of tasks in a taskset
 @param num_sets: Number of generated tasksets
'''

def tasksets_gen_with_tda(utilization, hard_task_factor, fault_rate, num_task, num_sets, rounded, limited):
    def taskset_gen_with_tda(utilization, hard_task_factor, fault_rate, num_task):
        while True:
            if limited is True:
                tasks = task_generator.taskGeneration_limited(num_task, utilization)
            elif rounded is True:
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
        opts, args = getopt.getopt(sys.argv[1:], "i:n:s:f:h:rl", ["ident=", "num_tasks=", "num_sets=", "fault_rate=", "hard_task_factor=", "rounded", "limited"])
    except getopt.GetoptError as err:
        print (str(err))
        sys.exit(2)

    num_tasks, num_sets, fault_rate, hard_task_factor = 0, 0, 0, 0
    ident = None
    rounded = False
    limited = False
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
        if opt in ('-r', '--rounded'):
            rounded = True
        if opt in ('-l', '--limited'):
            limited = True

    print('Generating: %d tasksets, %d tasks, fault probability: %f, rounded: %r' % (num_sets, num_tasks, fault_rate, rounded))
    for utilization in (45, 60, 80):
        tasksets = tasksets_gen_with_tda(utilization, hard_task_factor, fault_rate, num_tasks, num_sets, rounded, limited)
        try:
            if ident is not None:
                filename = '../tasksets/tasksets_' + ident + '_n_' + str(num_tasks) + 'u_' + str(utilization) + 's_' + str(num_sets) + 'f_'+ str(fault_rate) + 'h_'+ str(hard_task_factor) + str('l' if limited else '')
                np.save(filename, tasksets)
            else:
                raise Exception ("Please specify an identifier!")
        except IOError:
            print('Could not write filename %s' % filename)

if __name__=="__main__":
    main()
